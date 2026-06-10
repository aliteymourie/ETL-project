"""
Dim_Branch Pipeline — بارگذاری بعد مرکز پخش

استراتژی: Full-Refresh (truncate + insert)
چون جدول Branch کوچک است و PK ساده دارد، هر بار کل جدول جایگزین می‌شود.
"""
import pandas as pd
from io import StringIO
import csv
from datetime import datetime
from sqlalchemy import text

from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.logging import setup_logger

logger = setup_logger("dim_branch")

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────
PIPELINE_NAME = "dim_branch"
TARGET_TABLE  = "dim_branch"
PK_COLS       = ("branch_key",)

FINAL_COLS = [
    "branch_key",
    "branch_name",
    "etl_updated_at",
]

# ─────────────────────────────────────────────
# DDL
# ─────────────────────────────────────────────
DDL_DIM_BRANCH = """
CREATE TABLE IF NOT EXISTS dim_branch (
    branch_key      INT             NOT NULL,
    branch_name     VARCHAR(200),
    etl_updated_at  TIMESTAMP       DEFAULT NOW(),
    PRIMARY KEY (branch_key)
);
CREATE INDEX IF NOT EXISTS idx_dim_branch_key ON dim_branch (branch_key);
"""

# ─────────────────────────────────────────────
# Extract SQL
# ─────────────────────────────────────────────
EXTRACT_SQL = """
SELECT
    mp.ccMarkazPakhsh   AS branch_key,
    mp.NameMarkazPakhsh AS branch_name
FROM Pakhsh.Global.MarkazPakhsh mp;
"""

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def execute_ddl(loader: DataLoader, ddl_sql: str, label: str):
    with loader.tgt_engine.begin() as conn:
        conn.execute(text(ddl_sql))
    logger.info(f"DDL ok: {label}")


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

    df["branch_key"] = pd.to_numeric(df["branch_key"], errors="coerce").astype("Int64")
    df["etl_updated_at"] = datetime.now()

    return df.reindex(columns=FINAL_COLS)


def load(df: pd.DataFrame, loader: DataLoader):
    """Truncate-and-insert: برای ابعاد کوچک بهترین رویکرد است."""
    if df.empty:
        logger.warning("No data to load for dim_branch.")
        return 0

    cols_to_load = [c for c in FINAL_COLS if c != "etl_updated_at"]

    output = StringIO()
    df[cols_to_load].to_csv(
        output, sep="\t", header=False, index=False, na_rep="\\N", quoting=csv.QUOTE_MINIMAL
    )
    output.seek(0)

    with loader.tgt_engine.begin() as conn:
        with conn.connection.cursor() as cursor:
            cursor.execute(f"TRUNCATE TABLE {TARGET_TABLE};")
            cursor.copy_from(output, TARGET_TABLE, columns=cols_to_load, null="\\N")

    logger.info(f"✅ {len(df):,} rows loaded into {TARGET_TABLE}.")
    return len(df)


# ─────────────────────────────────────────────
# Main Pipeline
# ─────────────────────────────────────────────
def run_dim_branch_pipeline() -> int:
    logger.info("=" * 60)
    logger.info(f"Starting {PIPELINE_NAME} pipeline (Full-Refresh)")
    start_time = datetime.now()

    extractor = DataExtractor()
    loader    = DataLoader()

    try:
        execute_ddl(loader, DDL_DIM_BRANCH, TARGET_TABLE)

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
    run_dim_branch_pipeline()
