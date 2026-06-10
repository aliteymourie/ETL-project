"""
Fact_Inventory_Header Pipeline — بارگذاری هدر کاردکس انبار

استراتژی: Incremental Upsert بر اساس kardex_header_key + fiscal_year (PK ترکیبی)
watermark: ستون TarikhForm جدول Kardex (تاریخ سند)
پشتیبانی از تاریخ جلالی برای form_date و invoice_date.
"""
import pandas as pd
import jdatetime
from io import StringIO
import csv
from datetime import datetime
from sqlalchemy import text
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.checkpoint import ETLCheckpoint
from core.utils.logging import setup_logger

logger = setup_logger("fact_inventory_header")

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────
PIPELINE_NAME     = "fact_inventory_header"
TARGET_TABLE      = "fact_inventory_header"
PK_COLS           = ("kardex_header_key", "fiscal_year")
JALALI_1403_START = "2024-03-20 00:00:00"

FINAL_COLS = [
    "kardex_header_key",
    "fiscal_year",
    "document_number",
    "invoice_number",
    "form_type_code",
    "operation_type_code",
    "warehouse_type_code",
    "status_code",
    "header_reason",
    "is_fully_returned",
    "branch_key",
    "warehouse_key",
    "customer_key",
    "seller_key",
    "target_branch_key",
    "form_date_key",
    "invoice_date_key",
    "total_return_amount",
    "total_return_quantity",
    "total_tax_amount",
    "total_surcharge_amount",
    "header_discount_amount_1",
    "header_discount_amount_2",
    "etl_updated_at",
]

INT_COLS = {
    "kardex_header_key", "fiscal_year",
    "form_type_code", "operation_type_code", "warehouse_type_code", "status_code",
    "branch_key", "warehouse_key", "customer_key", "seller_key", "target_branch_key",
    "form_date_key", "invoice_date_key",
}
NUMERIC_COLS = {
    "total_return_amount", "total_return_quantity",
    "total_tax_amount", "total_surcharge_amount",
    "header_discount_amount_1", "header_discount_amount_2",
}

# ─────────────────────────────────────────────
# DDL
# ─────────────────────────────────────────────
DDL_FACT_INVENTORY_HEADER = """
CREATE TABLE IF NOT EXISTS fact_inventory_header (
    kardex_header_key       BIGINT          NOT NULL,
    fiscal_year             SMALLINT        NOT NULL,
    document_number         INT,
    invoice_number          INT,
    form_type_code          SMALLINT,
    operation_type_code     SMALLINT,
    warehouse_type_code     SMALLINT,
    status_code             SMALLINT,
    header_reason           VARCHAR(500),
    is_fully_returned       BOOLEAN,
    branch_key              INT,
    warehouse_key           INT,
    customer_key            INT,
    seller_key              INT,
    target_branch_key       INT,
    form_date_key           INT,
    invoice_date_key        INT,
    total_return_amount     NUMERIC(18,2),
    total_return_quantity   NUMERIC(18,4),
    total_tax_amount        NUMERIC(18,2),
    total_surcharge_amount  NUMERIC(18,2),
    header_discount_amount_1 NUMERIC(18,2),
    header_discount_amount_2 NUMERIC(18,2),
    etl_updated_at          TIMESTAMP       DEFAULT NOW(),
    PRIMARY KEY (kardex_header_key, fiscal_year)
);
CREATE INDEX IF NOT EXISTS idx_fih_branch_key     ON fact_inventory_header (branch_key);
CREATE INDEX IF NOT EXISTS idx_fih_warehouse_key  ON fact_inventory_header (warehouse_key);
CREATE INDEX IF NOT EXISTS idx_fih_customer_key   ON fact_inventory_header (customer_key);
CREATE INDEX IF NOT EXISTS idx_fih_seller_key     ON fact_inventory_header (seller_key);
CREATE INDEX IF NOT EXISTS idx_fih_form_date      ON fact_inventory_header (form_date_key);
CREATE INDEX IF NOT EXISTS idx_fih_invoice_date   ON fact_inventory_header (invoice_date_key);
CREATE INDEX IF NOT EXISTS idx_fih_fiscal_year    ON fact_inventory_header (fiscal_year);
CREATE INDEX IF NOT EXISTS idx_fih_status         ON fact_inventory_header (status_code);
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
    MIN(k.ccKardex) AS min_id,
    MAX(k.ccKardex) AS max_id,
    COUNT(*)        AS total_rows
FROM [Pakhsh].[Warehouse].[Kardex] k
WHERE k.TarikhForm IS NOT NULL
  AND k.TarikhForm >= CONVERT(DATETIME, '{last_modified}', 120)
"""

EXTRACT_SQL = """
SELECT
    k.ccKardex                      AS kardex_header_key,
    k.Sal                           AS fiscal_year,
    k.ShomarehForm                  AS document_number,
    k.ShomarehFaktor                AS invoice_number,
    k.CodeNoeForm                   AS form_type_code,
    k.CodeNoeAmalyat                AS operation_type_code,
    k.CodeNoeAnbar                  AS warehouse_type_code,
    k.CodeVazeiat                   AS status_code,
    k.Elat                          AS header_reason,
    k.MarjoeeKamel                  AS is_fully_returned,
    k.ccMarkazPakhsh                AS branch_key,
    k.ccAnbar                       AS warehouse_key,
    k.ccMoshtary                    AS customer_key,
    k.ccForoshandeh                 AS seller_key,
    k.ccMarkazPakhshBe              AS target_branch_key,
    CASE
        WHEN k.TarikhForm IS NOT NULL
        THEN CONVERT(INT, FORMAT(k.TarikhForm, 'yyyyMMdd'))
        ELSE NULL
    END                             AS form_date_key,
    CASE
        WHEN k.TarikhFaktor IS NOT NULL
        THEN CONVERT(INT, FORMAT(k.TarikhFaktor, 'yyyyMMdd'))
        ELSE NULL
    END                             AS invoice_date_key,
    ISNULL(k.SumGheymatMarjoee, 0)  AS total_return_amount,
    ISNULL(k.SumTedadMarjoee, 0)    AS total_return_quantity,
    ISNULL(k.SumMaliat, 0)          AS total_tax_amount,
    ISNULL(k.SumAvarez, 0)          AS total_surcharge_amount,
    ISNULL(k.TakhfifFaktor, 0)      AS header_discount_amount_1,
    ISNULL(k.MablaghTakhfif, 0)     AS header_discount_amount_2
FROM [Pakhsh].[Warehouse].[Kardex] k
WHERE k.TarikhForm IS NOT NULL
  AND k.TarikhForm >= CONVERT(DATETIME, '{last_modified}', 120)
  AND k.ccKardex BETWEEN {start_id} AND {end_id}
ORDER BY k.ccKardex
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

    # is_fully_returned: بیت به Boolean
    if "is_fully_returned" in df.columns:
        df["is_fully_returned"] = df["is_fully_returned"].map(
            lambda x: True if str(x) in ("1", "True", "true") else (False if pd.notna(x) else None)
        )

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
                "(LIKE fact_inventory_header EXCLUDING INDEXES EXCLUDING CONSTRAINTS) "
                "ON COMMIT DROP;"
            )
            cursor.copy_from(output, "tmp_staging", columns=cols_to_load, null="\\N")
            cursor.execute(upsert_sql)

    return rows_from_db, len(chunk)


# ─────────────────────────────────────────────
# Main Pipeline
# ─────────────────────────────────────────────
def run_fact_inventory_header_pipeline(
    chunk_size: int  = 200_000,
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
        execute_ddl(loader, DDL_FACT_INVENTORY_HEADER, TARGET_TABLE)
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
    run_fact_inventory_header_pipeline(chunk_size=200_000, max_workers=4)
