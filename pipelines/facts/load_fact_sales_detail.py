"""
Fact_Sales_Detail Pipeline — بارگذاری سطور فاکتورهای فروش

استراتژی: Incremental Upsert بر اساس sales_fact_id (PK اصلی سطر)
watermark: از طریق join با هدر بر اساس ModifiedDate فاکتور
"""
import pandas as pd
from io import StringIO
import csv
from datetime import datetime
from sqlalchemy import text
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.checkpoint import ETLCheckpoint
from core.utils.logging import setup_logger

logger = setup_logger("fact_sales_detail")

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────
PIPELINE_NAME     = "fact_sales_detail"
TARGET_TABLE      = "fact_sales_detail"
PK_COLS           = ("sales_fact_id",)
JALALI_1403_START = "2024-03-20 00:00:00"

FINAL_COLS = [
    "sales_fact_id",
    "invoice_id",
    "fiscal_year",
    "product_key",
    "quantity_carton",
    "quantity_box",
    "quantity_unit",
    "unit_price",
    "row_discount_amount",
    "row_tax",
    "row_surcharge",
    "row_net_amount",
    "etl_updated_at",
]

INT_COLS    = {"sales_fact_id", "invoice_id", "fiscal_year", "product_key"}
NUMERIC_COLS = {
    "quantity_carton", "quantity_box", "quantity_unit",
    "unit_price", "row_discount_amount", "row_tax", "row_surcharge", "row_net_amount",
}

# ─────────────────────────────────────────────
# DDL
# ─────────────────────────────────────────────
DDL_FACT_SALES_DETAIL = """
CREATE TABLE IF NOT EXISTS fact_sales_detail (
    sales_fact_id       BIGINT          NOT NULL,
    invoice_id          BIGINT          NOT NULL,
    fiscal_year         SMALLINT        NOT NULL,
    product_key         INT,
    quantity_carton     NUMERIC(18,4),
    quantity_box        NUMERIC(18,4),
    quantity_unit       NUMERIC(18,4),
    unit_price          NUMERIC(18,2),
    row_discount_amount NUMERIC(18,2),
    row_tax             NUMERIC(18,2),
    row_surcharge       NUMERIC(18,2),
    row_net_amount      NUMERIC(18,2),
    etl_updated_at      TIMESTAMP       DEFAULT NOW(),
    PRIMARY KEY (sales_fact_id)
);
CREATE INDEX IF NOT EXISTS idx_fsd_invoice_id   ON fact_sales_detail (invoice_id, fiscal_year);
CREATE INDEX IF NOT EXISTS idx_fsd_product_key  ON fact_sales_detail (product_key);
CREATE INDEX IF NOT EXISTS idx_fsd_fiscal_year  ON fact_sales_detail (fiscal_year);
"""

DDL_CHECKPOINT = """
CREATE TABLE IF NOT EXISTS etl_metadata.etl_checkpoint (
    pipeline_name   VARCHAR(100),
    last_run_at     TIMESTAMP,
    last_success_at TIMESTAMP,
    last_from_value VARCHAR(100),
    last_to_value   VARCHAR(100),
    rows_processed  BIGINT        DEFAULT 0,
    status          VARCHAR(20),
    error_message   TEXT,
    updated_at      TIMESTAMP     DEFAULT NOW()
);
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conrelid = 'etl_metadata.etl_checkpoint'::regclass
          AND contype  = 'p'
    ) THEN
        ALTER TABLE etl_metadata.etl_checkpoint
            ADD CONSTRAINT etl_checkpoint_pkey PRIMARY KEY (pipeline_name);
    END IF;
END;
$$;
"""

# ─────────────────────────────────────────────
# SQLs
# ─────────────────────────────────────────────
MIN_MAX_SQL = """
SELECT
    MIN(dfs.ccDarkhastFaktorSatr) AS min_id,
    MAX(dfs.ccDarkhastFaktorSatr) AS max_id,
    COUNT(*)                      AS total_rows
FROM Pakhsh.Sales.DarkhastFaktorSatr dfs
INNER JOIN Pakhsh.Sales.DarkhastFaktor df
    ON  df.ccDarkhastFaktor = dfs.ccDarkhastFaktor
    AND df.Sal              = dfs.Sal
WHERE df.TarikhFaktor IS NOT NULL
  AND df.ModifiedDate >= CONVERT(DATETIME, '{last_modified}', 120)
"""

EXTRACT_SQL = """
SELECT
    dfs.ccDarkhastFaktorSatr                AS sales_fact_id,
    dfs.ccDarkhastFaktor                    AS invoice_id,
    dfs.Sal                                 AS fiscal_year,
    dfs.ccKala                              AS product_key,
    ISNULL(dfs.Tedad1, 0)                   AS quantity_carton,
    ISNULL(dfs.Tedad2, 0)                   AS quantity_box,
    ISNULL(dfs.Tedad3, 0)                   AS quantity_unit,
    ISNULL(dfs.MablaghForosh, 0)            AS unit_price,
    ISNULL(dfs.MablaghTakhfifFaktor, 0)     AS row_discount_amount,
    ISNULL(dfs.Maliat, 0)                   AS row_tax,
    ISNULL(dfs.Avarez, 0)                   AS row_surcharge,
    ISNULL(dfs.MablaghForoshKhalesKala, 0)  AS row_net_amount
FROM Pakhsh.Sales.DarkhastFaktorSatr dfs
INNER JOIN Pakhsh.Sales.DarkhastFaktor df
    ON  df.ccDarkhastFaktor = dfs.ccDarkhastFaktor
    AND df.Sal              = dfs.Sal
WHERE df.TarikhFaktor IS NOT NULL
  AND df.ModifiedDate >= CONVERT(DATETIME, '{last_modified}', 120)
  AND dfs.ccDarkhastFaktorSatr BETWEEN {start_id} AND {end_id}
ORDER BY dfs.ccDarkhastFaktorSatr
"""

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def execute_ddl(loader: DataLoader, ddl_sql: str, label: str):
    with loader.tgt_engine.begin() as conn:
        conn.execute(text(ddl_sql))
    logger.info(f"DDL ok: {label}")


def build_upsert_sql(columns: list) -> str:
    non_pk = [c for c in columns if c not in PK_COLS and c != "etl_updated_at"]
    set_clause = ",\n            ".join([f"{c} = EXCLUDED.{c}" for c in non_pk])
    set_clause += ",\n            etl_updated_at = NOW()"
    cols = ", ".join(columns)
    return f"""
        INSERT INTO {TARGET_TABLE} ({cols})
        SELECT {cols} FROM tmp_staging
        ON CONFLICT ({", ".join(PK_COLS)}) DO UPDATE SET
            {set_clause}
    """


def transform(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    for col in df.select_dtypes(include="object").columns:
        df[col] = (
            df[col].astype(str)
            .str.replace("\n", " ").str.replace("\r", " ").str.replace("\t", " ")
            .str.strip()
        )
        df[col] = df[col].replace({"nan": None, "None": None, "": None})

    for col in INT_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["etl_updated_at"] = datetime.now()
    return df.reindex(columns=FINAL_COLS)


def process_chunk(start_id: int, end_id: int, last_modified: str):
    extractor = DataExtractor()
    loader    = DataLoader()

    sql   = EXTRACT_SQL.format(last_modified=last_modified, start_id=start_id, end_id=end_id)
    chunk = pd.read_sql(sql, extractor.src_engine)

    if chunk.empty:
        return 0, 0

    rows_from_db = len(chunk)
    chunk        = transform(chunk)

    cols_to_load = [c for c in FINAL_COLS if c != "etl_updated_at"]
    upsert_sql   = build_upsert_sql(cols_to_load)

    output = StringIO()
    chunk[cols_to_load].to_csv(
        output, sep="\t", header=False, index=False, na_rep="\\N", quoting=csv.QUOTE_MINIMAL
    )
    output.seek(0)

    with loader.tgt_engine.begin() as conn:
        with conn.connection.cursor() as cursor:
            cursor.execute(
                "CREATE TEMP TABLE tmp_staging "
                "(LIKE fact_sales_detail EXCLUDING INDEXES EXCLUDING CONSTRAINTS) "
                "ON COMMIT DROP;"
            )
            cursor.copy_from(output, "tmp_staging", columns=cols_to_load, null="\\N")
            cursor.execute(upsert_sql)

    return rows_from_db, len(chunk)


# ─────────────────────────────────────────────
# Main Pipeline
# ─────────────────────────────────────────────
def run_fact_sales_detail_pipeline(
    chunk_size: int  = 500_000,
    max_workers: int = 4,
    max_rows: int    = None,
) -> int:
    logger.info("=" * 60)
    logger.info(f"Starting {PIPELINE_NAME} pipeline (Incremental Upsert)")
    start_time = datetime.now()

    extractor  = DataExtractor()
    loader     = DataLoader()
    checkpoint = ETLCheckpoint(loader)

    try:
        execute_ddl(loader, DDL_FACT_SALES_DETAIL, TARGET_TABLE)
        try:
            execute_ddl(loader, "CREATE SCHEMA IF NOT EXISTS etl_metadata;", "etl_metadata schema")
            execute_ddl(loader, DDL_CHECKPOINT, "etl_metadata.etl_checkpoint")
        except Exception as e:
            logger.warning(f"metadata setup skipped: {e}")

        last_run = checkpoint.get_last_success(PIPELINE_NAME)
        last_modified = (
            str(last_run["last_to_value"])[:19].replace("T", " ")
            if last_run and last_run.get("last_to_value")
            else JALALI_1403_START
        )
        logger.info(f"ModifiedDate lower bound: {last_modified}")

        meta = pd.read_sql(MIN_MAX_SQL.format(last_modified=last_modified), extractor.src_engine)
        min_id    = int(meta["min_id"].iloc[0]) if pd.notna(meta["min_id"].iloc[0]) else 0
        max_id    = int(meta["max_id"].iloc[0]) if pd.notna(meta["max_id"].iloc[0]) else 0
        total_est = int(meta["total_rows"].iloc[0]) if pd.notna(meta["total_rows"].iloc[0]) else 0

        if min_id == 0 or max_id == 0:
            logger.info("No new rows found.")
            return 0

        logger.info(f"Source: ~{total_est:,} rows | ID range {min_id:,} → {max_id:,}")

        ranges       = [(s, min(s + chunk_size - 1, max_id)) for s in range(min_id, max_id + 1, chunk_size)]
        total_chunks = len(ranges)
        total_rows   = 0
        completed    = 0

        logger.info(f"Chunks planned: {total_chunks:,} (chunk_size={chunk_size:,}, workers={max_workers})")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(process_chunk, s, e, last_modified): (s, e)
                for s, e in ranges
            }
            for future in as_completed(futures):
                start, end = futures[future]
                completed += 1
                try:
                    rows_from_db, inserted = future.result()
                    total_rows += inserted
                    pct = completed / total_chunks * 100
                    logger.info(
                        f"chunk {completed}/{total_chunks} ({pct:.0f}%) "
                        f"range={start}-{end} extracted={rows_from_db:,} inserted={inserted:,} total={total_rows:,}"
                    )
                    if max_rows and total_rows >= max_rows:
                        logger.info(f"max_rows cap reached ({total_rows:,}). Stopping.")
                        break
                except Exception as e:
                    logger.error(f"chunk failed range={start}-{end}: {e}")

        run_end_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        checkpoint.save_checkpoint(
            PIPELINE_NAME, "SUCCESS", total_rows,
            from_value=last_modified,
            to_value=run_end_ts if total_rows > 0 else last_modified,
        )

        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(f"Pipeline done: {total_rows:,} rows | {elapsed:.1f}s")
        return total_rows

    except Exception as e:
        logger.error(f"Pipeline {PIPELINE_NAME} failed: {e}", exc_info=True)
        checkpoint.save_checkpoint(PIPELINE_NAME, "FAILED", error_message=str(e)[:500])
        raise


if __name__ == "__main__":
    run_fact_sales_detail_pipeline(chunk_size=500_000, max_workers=4)
