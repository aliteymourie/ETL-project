"""
Dim_Asset_Group Pipeline — بارگذاری بعد گروه دارایی

استراتژی: Upsert بر اساس cc_goroh_daraee (کلید طبیعی)
منبع: Pakhsh.AssetAccounting.GorohDaraee + GorohAslyDaraee
جدول بسیار کوچک، یکجا بارگذاری می‌شود.
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

logger = setup_logger("dim_asset_group")

PIPELINE_NAME = "dim_asset_group"
TARGET_TABLE  = "dim_asset_group"
PK_COLS       = ("cc_goroh_daraee",)

FINAL_COLS = [
    "cc_goroh_daraee",
    "name_goroh_daraee",
    "cc_goroh_asly_daraee",
    "name_goroh_asly_daraee",
    "is_active",
    "etl_updated_at",
]

INT_COLS = {"cc_goroh_daraee", "cc_goroh_asly_daraee"}

DDL_DIM_ASSET_GROUP = """
CREATE TABLE IF NOT EXISTS dim_asset_group (
    asset_group_key         SERIAL,
    cc_goroh_daraee         INTEGER         NOT NULL,
    name_goroh_daraee       VARCHAR(200),
    cc_goroh_asly_daraee    INTEGER,
    name_goroh_asly_daraee  VARCHAR(200),
    is_active               BOOLEAN         DEFAULT TRUE,
    etl_updated_at          TIMESTAMP       DEFAULT NOW(),
    PRIMARY KEY (cc_goroh_daraee)
);
CREATE INDEX IF NOT EXISTS idx_dim_asset_group_cc ON dim_asset_group (cc_goroh_daraee);
"""

EXTRACT_SQL = """
SELECT
    gd.ccGorohDaraee            AS cc_goroh_daraee,
    gd.Sharh                    AS name_goroh_daraee,
    gd.ccGorohAslyDaraee       AS cc_goroh_asly_daraee,
    gad.NameGorohAslyDaraee     AS name_goroh_asly_daraee
FROM Pakhsh.AssetAccounting.GorohDaraee gd
LEFT JOIN Pakhsh.AssetAccounting.GorohAslyDaraee gad
    ON gd.ccGorohAslyDaraee = gad.ccGorohAslyDaraee
ORDER BY gd.ccGorohDaraee
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

    df["is_active"] = True
    df["etl_updated_at"] = datetime.now()
    return df.reindex(columns=FINAL_COLS)


def load(df: pd.DataFrame, loader: DataLoader) -> int:
    if df.empty:
        logger.warning("No data to load for dim_asset_group.")
        return 0

    cols_to_load = [c for c in FINAL_COLS if c != "etl_updated_at"]
    upsert_sql   = build_upsert_sql(cols_to_load)

    output = StringIO()
    df[cols_to_load].to_csv(
        output, sep="\t", header=False, index=False, na_rep="\\N", quoting=csv.QUOTE_MINIMAL
    )
    output.seek(0)

    with loader.tgt_engine.begin() as conn:
        with conn.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TEMP TABLE tmp_staging (
                    cc_goroh_daraee INTEGER NOT NULL,
                    name_goroh_daraee VARCHAR(200),
                    cc_goroh_asly_daraee INTEGER,
                    name_goroh_asly_daraee VARCHAR(200),
                    is_active BOOLEAN
                ) ON COMMIT DROP;
            """)
            cursor.copy_from(output, "tmp_staging", columns=cols_to_load, null="\\N")
            cursor.execute(upsert_sql)

    logger.info(f"✅ {len(df):,} rows upserted into {TARGET_TABLE}.")
    return len(df)


def run_dim_asset_group_pipeline() -> int:
    logger.info("=" * 60)
    logger.info(f"Starting {PIPELINE_NAME} pipeline (Upsert)")
    start_time = datetime.now()

    extractor = DataExtractor()
    loader    = DataLoader()

    try:
        execute_ddl(loader, DDL_DIM_ASSET_GROUP, TARGET_TABLE)

        logger.info("Extracting from source...")
        df = pd.read_sql(EXTRACT_SQL, extractor.src_engine)
        logger.info(f"Extracted {len(df):,} rows from source.")

        df = transform(df)
        total = load(df, loader)

        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(f"Pipeline done: {total:,} rows | {elapsed:.1f}s")
        return total

    except Exception as e:
        logger.error(f"Pipeline {PIPELINE_NAME} failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    run_dim_asset_group_pipeline()
