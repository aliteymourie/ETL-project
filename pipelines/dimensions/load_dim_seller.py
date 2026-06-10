"""
Dim_Seller Pipeline — بارگذاری بعد فروشندگان

استراتژی: Upsert بر اساس seller_key
فروشندگان ممکن است وضعیت یا موبایلشان تغییر کند،
پس upsert از full-refresh بهتر است.
"""
import pandas as pd
from io import StringIO
import csv
from datetime import datetime
from sqlalchemy import text

from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.logging import setup_logger

logger = setup_logger("dim_seller")

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────
PIPELINE_NAME = "dim_seller"
TARGET_TABLE  = "dim_seller"
PK_COLS       = ("seller_key",)

FINAL_COLS = [
    "seller_key",
    "seller_name",
    "seller_code_old",
    "seller_mobile",
    "seller_status_code",
    "etl_updated_at",
]

INT_COLS = {"seller_key", "seller_status_code"}

# ─────────────────────────────────────────────
# DDL
# ─────────────────────────────────────────────
DDL_DIM_SELLER = """
CREATE TABLE IF NOT EXISTS dim_seller (
    seller_key          INT             NOT NULL,
    seller_name         VARCHAR(200),
    seller_code_old     VARCHAR(50),
    seller_mobile       VARCHAR(30),
    seller_status_code  SMALLINT,
    etl_updated_at      TIMESTAMP       DEFAULT NOW(),
    PRIMARY KEY (seller_key)
);
CREATE INDEX IF NOT EXISTS idx_dim_seller_key ON dim_seller (seller_key);
"""

# ─────────────────────────────────────────────
# Extract SQL
# ─────────────────────────────────────────────
EXTRACT_SQL = """
SELECT
    f.ccForoshandeh      AS seller_key,
    f.SharhForoshandeh   AS seller_name,
    f.CodeForoshandehOld AS seller_code_old,
    f.MobileNumber       AS seller_mobile,
    f.CodeVazeiat        AS seller_status_code
FROM Pakhsh.Sales.Foroshandeh f;
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

    df["etl_updated_at"] = datetime.now()
    return df.reindex(columns=FINAL_COLS)


def load(df: pd.DataFrame, loader: DataLoader) -> int:
    if df.empty:
        logger.warning("No data to load for dim_seller.")
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
            cursor.execute(
                "CREATE TEMP TABLE tmp_staging "
                "(LIKE dim_seller EXCLUDING INDEXES EXCLUDING CONSTRAINTS) "
                "ON COMMIT DROP;"
            )
            cursor.copy_from(output, "tmp_staging", columns=cols_to_load, null="\\N")
            cursor.execute(upsert_sql)

    logger.info(f"✅ {len(df):,} rows upserted into {TARGET_TABLE}.")
    return len(df)


# ─────────────────────────────────────────────
# Main Pipeline
# ─────────────────────────────────────────────
def run_dim_seller_pipeline() -> int:
    logger.info("=" * 60)
    logger.info(f"Starting {PIPELINE_NAME} pipeline (Upsert)")
    start_time = datetime.now()

    extractor = DataExtractor()
    loader    = DataLoader()

    try:
        execute_ddl(loader, DDL_DIM_SELLER, TARGET_TABLE)

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
    run_dim_seller_pipeline()
