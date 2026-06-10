"""
Dim_Product Pipeline — بارگذاری بعد کالا

استراتژی: Upsert بر اساس cc_kala (کلید طبیعی)
ModifiedDate برای تشخیص تغییرات استفاده می‌شود.
با توجه به ابعاد متوسط کالاها، به صورت Incremental اجرا می‌شود.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
from io import StringIO
import csv
from datetime import datetime
from sqlalchemy import text

from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.logging import setup_logger
from core.utils.checkpoint import ETLCheckpoint

logger = setup_logger("dim_product")

PIPELINE_NAME = "dim_product"
TARGET_TABLE  = "dim_product"
PK_COLS       = ("cc_kala",)

FINAL_COLS = [
    "cc_kala",
    "name_kala",
    "generic_code",
    "brand_name",
    "cc_tamin_konandeh",
    "cc_tolid_konandeh",
    "is_active",
    "etl_updated_at",
]

INT_COLS = {"cc_kala", "cc_tamin_konandeh", "cc_tolid_konandeh"}

DDL_DIM_PRODUCT = """
CREATE TABLE IF NOT EXISTS dim_product (
    product_key         SERIAL,
    cc_kala             INTEGER         NOT NULL,
    name_kala           VARCHAR(256),
    generic_code        VARCHAR(20),
    brand_name          VARCHAR(100),
    cc_tamin_konandeh   INTEGER,
    cc_tolid_konandeh   INTEGER,
    is_active           BOOLEAN         DEFAULT TRUE,
    etl_updated_at      TIMESTAMP       DEFAULT NOW(),
    PRIMARY KEY (cc_kala)
);
CREATE INDEX IF NOT EXISTS idx_dim_product_cc_kala ON dim_product (cc_kala);
"""

DDL_CHECKPOINT = """
CREATE TABLE IF NOT EXISTS etl_metadata.etl_checkpoint (
    pipeline_name   VARCHAR(100) PRIMARY KEY,
    last_run_at     TIMESTAMP,
    last_success_at TIMESTAMP,
    last_from_value VARCHAR(100),
    last_to_value   VARCHAR(100),
    rows_processed  BIGINT        DEFAULT 0,
    status          VARCHAR(20),
    error_message   TEXT,
    updated_at      TIMESTAMP     DEFAULT NOW()
);
"""

DDL_CHECKPOINT_PK = """
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints
        WHERE constraint_schema = 'etl_metadata'
          AND table_name = 'etl_checkpoint'
          AND constraint_type = 'PRIMARY KEY'
    ) THEN
        EXECUTE 'ALTER TABLE etl_metadata.etl_checkpoint ADD PRIMARY KEY (pipeline_name)';
    END IF;
END;
$$;
"""

TMP_STAGING_DDL = """
    CREATE TEMP TABLE tmp_staging (
        cc_kala INTEGER NOT NULL,
        name_kala VARCHAR(256),
        generic_code VARCHAR(20),
        brand_name VARCHAR(100),
        cc_tamin_konandeh INTEGER,
        cc_tolid_konandeh INTEGER,
        is_active BOOLEAN
    ) ON COMMIT DROP;
"""

MIN_MAX_SQL = """
SELECT
    MIN(k.ccKala) AS min_id,
    MAX(k.ccKala) AS max_id,
    COUNT(*)      AS total_rows
FROM Pakhsh.Warehouse.Kala k
WHERE k.ModifiedDate >= CONVERT(DATETIME, '{last_modified}', 120)
"""

EXTRACT_SQL = """
SELECT
    k.ccKala                AS cc_kala,
    k.NameKala              AS name_kala,
    k.CodeJenerik           AS generic_code,
    b.NameBrand             AS brand_name,
    k.ccTaminkonandeh       AS cc_tamin_konandeh,
    k.ccTolidkonandeh       AS cc_tolid_konandeh,
    CASE WHEN k.CodeVazeiat = 0 THEN 1 ELSE 0 END AS is_active
FROM Pakhsh.Warehouse.Kala k
LEFT JOIN Pakhsh.Warehouse.Brand b ON k.ccBrand = b.ccBrand
WHERE k.ccKala BETWEEN {start_id} AND {end_id}
ORDER BY k.ccKala
"""


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

    for col in df.select_dtypes(include="str").columns:
        df[col] = (
            df[col].astype(str)
            .str.replace("\n", " ").str.replace("\r", " ").str.replace("\t", " ")
            .str.strip()
        )
        df[col] = df[col].replace({"nan": None, "None": None, "": None})

    for col in INT_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    if "is_active" in df.columns:
        df["is_active"] = df["is_active"].map(
            lambda x: True if str(x) in ("1", "True", "true") else (False if pd.notna(x) else None)
        )

    df["etl_updated_at"] = datetime.now()
    return df.reindex(columns=FINAL_COLS)


def process_chunk(start_id: int, end_id: int, last_modified: str):
    extractor = DataExtractor()
    loader    = DataLoader()

    sql   = EXTRACT_SQL.format(start_id=start_id, end_id=end_id)
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
            cursor.execute(TMP_STAGING_DDL)
            cursor.copy_from(output, "tmp_staging", columns=cols_to_load, null="\\N")
            cursor.execute(upsert_sql)

    return rows_from_db, len(chunk)


def run_dim_product_pipeline(chunk_size: int = 50_000, max_workers: int = 4, max_rows: int = None) -> int:
    logger.info("=" * 60)
    logger.info(f"Starting {PIPELINE_NAME} pipeline (Incremental Upsert)")
    start_time = datetime.now()

    extractor  = DataExtractor()
    loader     = DataLoader()
    checkpoint = ETLCheckpoint(loader)

    try:
        execute_ddl(loader, DDL_DIM_PRODUCT, TARGET_TABLE)
        try:
            execute_ddl(loader, "CREATE SCHEMA IF NOT EXISTS etl_metadata;", "etl_metadata schema")
            execute_ddl(loader, DDL_CHECKPOINT, "etl_metadata.etl_checkpoint")
            execute_ddl(loader, DDL_CHECKPOINT_PK, "etl_metadata.etl_checkpoint PK")
        except Exception as e:
            logger.warning(f"metadata setup skipped: {e}")

        last_run = checkpoint.get_last_success(PIPELINE_NAME)
        last_modified = (
            str(last_run["last_to_value"])[:19].replace("T", " ")
            if last_run and last_run.get("last_to_value")
            else "2020-01-01 00:00:00"
        )
        logger.info(f"ModifiedDate lower bound: {last_modified}")

        meta = pd.read_sql(MIN_MAX_SQL.format(last_modified=last_modified), extractor.src_engine)
        min_id    = int(meta["min_id"].iloc[0]) if pd.notna(meta["min_id"].iloc[0]) else 0
        max_id    = int(meta["max_id"].iloc[0]) if pd.notna(meta["max_id"].iloc[0]) else 0
        total_est = int(meta["total_rows"].iloc[0]) if pd.notna(meta["total_rows"].iloc[0]) else 0

        if min_id == 0 or max_id == 0:
            logger.info("No rows found in source.")
            return 0

        logger.info(f"Source: ~{total_est:,} rows | ID range {min_id:,} → {max_id:,}")

        ranges       = [(s, min(s + chunk_size - 1, max_id)) for s in range(min_id, max_id + 1, chunk_size)]
        total_chunks = len(ranges)
        total_rows   = 0
        completed    = 0

        logger.info(f"Chunks planned: {total_chunks:,} (chunk_size={chunk_size:,}, workers={max_workers})")

        from concurrent.futures import ThreadPoolExecutor, as_completed

        ranges_iter = iter(ranges)
        active = {}

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
            for _ in range(min(max_workers, total_chunks)):
                submit_next(executor, active)

            while active:
                done = next(as_completed(active))
                start, end = active.pop(done)
                completed += 1
                try:
                    rows_from_db, inserted = done.result()
                    total_rows += inserted
                    pct = completed / total_chunks * 100
                    logger.info(
                        f"chunk {completed}/{total_chunks} ({pct:.0f}%) "
                        f"range={start}-{end} extracted={rows_from_db:,} inserted={inserted:,} total={total_rows:,}"
                    )
                    if max_rows and total_rows >= max_rows:
                        logger.info(f"max_rows cap reached ({total_rows:,}). Stopping.")
                    else:
                        submit_next(executor, active)
                except Exception as e:
                    logger.error(f"chunk failed range={start}-{end}: {str(e)[:300]}")
                    submit_next(executor, active)

        run_end_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        to_value = run_end_ts if total_rows > 0 else last_modified
        with loader.tgt_engine.begin() as conn:
            conn.execute(text("""
                DELETE FROM etl_metadata.etl_checkpoint
                WHERE pipeline_name = :name
            """), {"name": PIPELINE_NAME})
            conn.execute(text("""
                INSERT INTO etl_metadata.etl_checkpoint
                    (pipeline_name, last_run_at, last_success_at,
                     last_from_value, last_to_value, rows_processed, status)
                VALUES
                    (:name, NOW(), NOW(), :from_val, :to_val, :rows, 'SUCCESS')
            """), {"name": PIPELINE_NAME, "from_val": last_modified, "to_val": to_value, "rows": total_rows})

        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(f"Pipeline done: {total_rows:,} rows | {elapsed:.1f}s")
        return total_rows

    except Exception as e:
        logger.error(f"Pipeline {PIPELINE_NAME} failed: {e}", exc_info=True)
        try:
            with loader.tgt_engine.begin() as conn:
                conn.execute(text("""
                    DELETE FROM etl_metadata.etl_checkpoint
                    WHERE pipeline_name = :name
                """), {"name": PIPELINE_NAME})
                conn.execute(text("""
                    INSERT INTO etl_metadata.etl_checkpoint
                        (pipeline_name, status, error_message)
                    VALUES (:name, 'FAILED', :error)
                """), {"name": PIPELINE_NAME, "error": str(e)[:500]})
        except Exception as cp_err:
            logger.warning(f"checkpoint save failed: {cp_err}")
        raise


if __name__ == "__main__":
    run_dim_product_pipeline(chunk_size=50_000, max_workers=4)
