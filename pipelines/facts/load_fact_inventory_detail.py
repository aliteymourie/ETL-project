"""
Fact_Inventory_Detail Pipeline — بارگذاری سطور کاردکس انبار

استراتژی: Incremental Upsert بر اساس kardex_detail_key (PK اصلی سطر)
watermark: از طریق join با هدر کاردکس بر اساس TarikhForm
این جدول بزرگ‌ترین fact است؛ chunk_size بزرگ و parallel workers بیشتری استفاده می‌شود.
Cross-Fact Bridge: linked_invoice_id و linked_sales_fact_id ارتباط مستقیم به Fact_Sales دارند.
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

logger = setup_logger("fact_inventory_detail")

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────
PIPELINE_NAME     = "fact_inventory_detail"
TARGET_TABLE      = "fact_inventory_detail"
PK_COLS           = ("kardex_detail_key",)
JALALI_1403_START = "2024-03-20 00:00:00"

FINAL_COLS = [
    "kardex_detail_key",
    "kardex_header_key",
    "fiscal_year",
    "product_key",
    "supplier_key",
    "row_reason_key",
    "person_key",
    "batch_number",
    "production_date",
    "expiry_date",
    "product_type_code",
    "is_firm_or_consignment",
    "row_description",
    "linked_invoice_id",
    "linked_sales_fact_id",
    "quantity_carton",
    "quantity_box",
    "quantity_unit",
    "quantity_alt",
    "stock_effect_qty",
    "price_level_1",
    "price_level_2",
    "price_level_3",
    "price_level_4",
    "price_level_5",
    "price_level_6",
    "price_level_7",
    "total_row_amount",
    "temp_price",
    "last_temp_price",
    "etl_updated_at",
]

INT_COLS = {
    "kardex_detail_key", "kardex_header_key", "fiscal_year",
    "product_key", "supplier_key", "row_reason_key", "person_key",
    "product_type_code", "is_firm_or_consignment",
    "linked_invoice_id", "linked_sales_fact_id",
}
NUMERIC_COLS = {
    "quantity_carton", "quantity_box", "quantity_unit", "quantity_alt", "stock_effect_qty",
    "price_level_1", "price_level_2", "price_level_3", "price_level_4",
    "price_level_5", "price_level_6", "price_level_7",
    "total_row_amount", "temp_price", "last_temp_price",
}

# ─────────────────────────────────────────────
# DDL
# ─────────────────────────────────────────────
DDL_FACT_INVENTORY_DETAIL = """
CREATE TABLE IF NOT EXISTS fact_inventory_detail (
    kardex_detail_key       BIGINT          NOT NULL,
    kardex_header_key       BIGINT          NOT NULL,
    fiscal_year             SMALLINT        NOT NULL,
    product_key             INT,
    supplier_key            INT,
    row_reason_key          INT,
    person_key              INT,
    batch_number            VARCHAR(50),
    production_date         TIMESTAMP,
    expiry_date             TIMESTAMP,
    product_type_code       SMALLINT,
    is_firm_or_consignment  SMALLINT,
    row_description         TEXT,
    linked_invoice_id       BIGINT,
    linked_sales_fact_id    BIGINT,
    quantity_carton         NUMERIC(18,4),
    quantity_box            NUMERIC(18,4),
    quantity_unit           NUMERIC(18,4),
    quantity_alt            NUMERIC(18,4),
    stock_effect_qty        NUMERIC(18,4),
    price_level_1           NUMERIC(18,2),
    price_level_2           NUMERIC(18,2),
    price_level_3           NUMERIC(18,2),
    price_level_4           NUMERIC(18,2),
    price_level_5           NUMERIC(18,2),
    price_level_6           NUMERIC(18,2),
    price_level_7           NUMERIC(18,2),
    total_row_amount        NUMERIC(18,2),
    temp_price              NUMERIC(18,2),
    last_temp_price         NUMERIC(18,2),
    etl_updated_at          TIMESTAMP       DEFAULT NOW(),
    PRIMARY KEY (kardex_detail_key)
);
CREATE INDEX IF NOT EXISTS idx_fid_header_key       ON fact_inventory_detail (kardex_header_key);
CREATE INDEX IF NOT EXISTS idx_fid_product_key      ON fact_inventory_detail (product_key);
CREATE INDEX IF NOT EXISTS idx_fid_supplier_key     ON fact_inventory_detail (supplier_key);
CREATE INDEX IF NOT EXISTS idx_fid_fiscal_year      ON fact_inventory_detail (fiscal_year);
CREATE INDEX IF NOT EXISTS idx_fid_linked_invoice   ON fact_inventory_detail (linked_invoice_id);
CREATE INDEX IF NOT EXISTS idx_fid_linked_sales     ON fact_inventory_detail (linked_sales_fact_id);
CREATE INDEX IF NOT EXISTS idx_fid_batch_number     ON fact_inventory_detail (batch_number);
CREATE INDEX IF NOT EXISTS idx_fid_expiry_date      ON fact_inventory_detail (expiry_date);
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
    MIN(ks.ccKardexSatr) AS min_id,
    MAX(ks.ccKardexSatr) AS max_id,
    COUNT(*)             AS total_rows
FROM [Pakhsh].[Warehouse].[KardexSatr] ks
INNER JOIN [Pakhsh].[Warehouse].[Kardex] k
    ON k.ccKardex = ks.ccKardex
WHERE k.TarikhForm IS NOT NULL
  AND k.TarikhForm >= CONVERT(DATETIME, '{last_modified}', 120)
"""

EXTRACT_SQL = """
SELECT
    ks.ccKardexSatr                 AS kardex_detail_key,
    ks.ccKardex                     AS kardex_header_key,
    ks.Sal                          AS fiscal_year,
    ks.ccKala                       AS product_key,
    ks.ccTaminKonandeh              AS supplier_key,
    ks.ccElat                       AS row_reason_key,
    ks.ccAfrad                      AS person_key,
    ks.ShomarehBach                 AS batch_number,
    ks.TarikhTolid                  AS production_date,
    ks.TarikhEngheza                AS expiry_date,
    ks.CodeNoeKala                  AS product_type_code,
    ks.GhatiAmani                   AS is_firm_or_consignment,
    ks.Sharh                        AS row_description,
    ks.ccDarkhastFaktor             AS linked_invoice_id,
    ks.ccDarkhastFaktorSatr         AS linked_sales_fact_id,
    ISNULL(ks.Tedad1, 0)            AS quantity_carton,
    ISNULL(ks.Tedad2, 0)            AS quantity_box,
    ISNULL(ks.Tedad3, 0)            AS quantity_unit,
    ISNULL(ks.Tedad4, 0)            AS quantity_alt,
    ISNULL(ks.Mojody, 0)            AS stock_effect_qty,
    ISNULL(ks.Gheymat, 0)           AS price_level_1,
    ISNULL(ks.Gheymat2, 0)          AS price_level_2,
    ISNULL(ks.Gheymat3, 0)          AS price_level_3,
    ISNULL(ks.Gheymat4, 0)          AS price_level_4,
    ISNULL(ks.Gheymat5, 0)          AS price_level_5,
    ISNULL(ks.Gheymat6, 0)          AS price_level_6,
    ISNULL(ks.Gheymat7, 0)          AS price_level_7,
    ISNULL(ks.GheymatKolM, 0)       AS total_row_amount,
    ISNULL(ks.GheymatTemp, 0)       AS temp_price,
    ISNULL(ks.GheymatTempLast, 0)   AS last_temp_price
FROM [Pakhsh].[Warehouse].[KardexSatr] ks
INNER JOIN [Pakhsh].[Warehouse].[Kardex] k
    ON k.ccKardex = ks.ccKardex
WHERE k.TarikhForm IS NOT NULL
  AND k.TarikhForm >= CONVERT(DATETIME, '{last_modified}', 120)
  AND ks.ccKardexSatr BETWEEN {start_id} AND {end_id}
ORDER BY ks.ccKardexSatr
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

    # پاکسازی متن
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

    for date_col in ("production_date", "expiry_date"):
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

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

    try:
        with loader.tgt_engine.begin() as conn:
            with conn.connection.cursor() as cursor:
                cursor.execute(
                    "CREATE TEMP TABLE tmp_staging "
                    "(LIKE fact_inventory_detail EXCLUDING INDEXES EXCLUDING CONSTRAINTS) "
                    "ON COMMIT DROP;"
                )
                cursor.copy_from(output, "tmp_staging", columns=cols_to_load, null="\\N")
                cursor.execute(upsert_sql)
        return rows_from_db, len(chunk)
    except Exception as e:
        logger.error(f"chunk failed range={start_id}-{end_id}: {str(e)[:300]}")
        raise


# ─────────────────────────────────────────────
# Main Pipeline
# ─────────────────────────────────────────────
def run_fact_inventory_detail_pipeline(
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
        execute_ddl(loader, DDL_FACT_INVENTORY_DETAIL, TARGET_TABLE)
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
        logger.info(f"TarikhForm lower bound: {last_modified}")

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
        total_errors = 0
        completed    = 0

        logger.info(f"Chunks planned: {total_chunks:,} (chunk_size={chunk_size:,}, workers={max_workers})")

        # Lazy submission — مثل v6، تا cap رسیده نشود chunk جدید submit می‌شود
        ranges_iter = iter(ranges)

        def submit_next(executor, futures_dict):
            if max_rows and total_rows >= max_rows:
                return
            try:
                s, e = next(ranges_iter)
                f = executor.submit(process_chunk, s, e, last_modified)
                futures_dict[f] = (s, e)
            except StopIteration:
                pass

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            active = {}
            for _ in range(max_workers):
                submit_next(executor, active)

            while active:
                done = next(as_completed(active))
                start, end = active.pop(done)
                completed += 1
                try:
                    rows_from_db, inserted = done.result()
                    total_rows += inserted
                    pct = completed / total_chunks * 100
                    elapsed = (datetime.now() - start_time).total_seconds()
                    eta_min = (elapsed / completed * (total_chunks - completed)) / 60 if completed > 0 else 0
                    logger.info(
                        f"chunk {completed}/{total_chunks} ({pct:.0f}%) "
                        f"range={start}-{end} extracted={rows_from_db:,} inserted={inserted:,} "
                        f"total={total_rows:,} eta_min={eta_min:.0f}"
                    )
                    if max_rows and total_rows >= max_rows:
                        logger.info(f"max_rows cap reached ({total_rows:,}). Stopping.")
                    else:
                        submit_next(executor, active)
                except Exception as e:
                    total_errors += 1
                    logger.error(f"chunk failed range={start}-{end}: {str(e)[:300]}")
                    submit_next(executor, active)

        if total_errors:
            msg = f"Finished with errors: loaded={total_rows:,}, failed_chunks={total_errors:,}"
            checkpoint.save_checkpoint(PIPELINE_NAME, "FAILED", total_rows, error_message=msg[:500])
            logger.error(msg)
            raise RuntimeError(msg)

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
    run_fact_inventory_detail_pipeline(chunk_size=500_000, max_workers=4)
