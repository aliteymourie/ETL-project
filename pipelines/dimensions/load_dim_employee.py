"""
Dim_Employee Pipeline — بارگذاری بعد کارکنان/فروشندگان

استراتژی: Upsert بر اساس cc_afrad (کلید طبیعی)
منبع: Pakhsh.Global.Afrad
این جدول نسبتاً کوچک است، به صورت یکجا با upsert انجام می‌شود.
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

logger = setup_logger("dim_employee")

PIPELINE_NAME = "dim_employee"
TARGET_TABLE  = "dim_employee"
PK_COLS       = ("cc_afrad",)

FINAL_COLS = [
    "cc_afrad",
    "full_name",
    "code_mely",
    "mobile",
    "title",
    "email",
    "code_jensiat",
    "tarikh_tavalod",
    "is_admin",
    "enable_login",
    "is_active",
    "etl_updated_at",
]

INT_COLS = {"cc_afrad", "code_jensiat"}

DDL_DIM_EMPLOYEE = """
CREATE TABLE IF NOT EXISTS dim_employee (
    employee_key    SERIAL,
    cc_afrad        INTEGER         NOT NULL,
    full_name       VARCHAR(200),
    code_mely       VARCHAR(20),
    mobile          VARCHAR(30),
    title           VARCHAR(100),
    email           VARCHAR(100),
    code_jensiat    SMALLINT,
    tarikh_tavalod  TIMESTAMP,
    is_admin        BOOLEAN         DEFAULT FALSE,
    enable_login    BOOLEAN         DEFAULT FALSE,
    is_active       BOOLEAN         DEFAULT TRUE,
    etl_updated_at  TIMESTAMP       DEFAULT NOW(),
    PRIMARY KEY (cc_afrad)
);
CREATE INDEX IF NOT EXISTS idx_dim_employee_cc_afrad ON dim_employee (cc_afrad);
"""

EXTRACT_SQL = """
SELECT
    a.ccAfrad               AS cc_afrad,
    LTRIM(RTRIM(a.FName + ' ' + a.LName)) AS full_name,
    a.CodeMely              AS code_mely,
    a.Mobile                AS mobile,
    a.Title                 AS title,
    a.Email                 AS email,
    a.CodeJensiat           AS code_jensiat,
    a.TarikhTavalod         AS tarikh_tavalod,
    a.IsAdmin               AS is_admin,
    a.EnableLogin           AS enable_login
FROM Pakhsh.Global.Afrad a
WHERE a.ccAfrad IS NOT NULL
ORDER BY a.ccAfrad
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

    for bool_col in ("is_admin", "enable_login", "is_active"):
        if bool_col in df.columns:
            df[bool_col] = df[bool_col].map(
                lambda x: True if str(x) in ("1", "True", "true") else (False if pd.notna(x) else None)
            )

    if "tarikh_tavalod" in df.columns:
        df["tarikh_tavalod"] = pd.to_datetime(df["tarikh_tavalod"], errors="coerce")

    df["is_active"] = True
    df["etl_updated_at"] = datetime.now()
    return df.reindex(columns=FINAL_COLS)


def load(df: pd.DataFrame, loader: DataLoader) -> int:
    if df.empty:
        logger.warning("No data to load for dim_employee.")
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
                    cc_afrad INTEGER NOT NULL,
                    full_name VARCHAR(200),
                    code_mely VARCHAR(20),
                    mobile VARCHAR(30),
                    title VARCHAR(100),
                    email VARCHAR(100),
                    code_jensiat SMALLINT,
                    tarikh_tavalod TIMESTAMP,
                    is_admin BOOLEAN,
                    enable_login BOOLEAN,
                    is_active BOOLEAN
                ) ON COMMIT DROP;
            """)
            cursor.copy_from(output, "tmp_staging", columns=cols_to_load, null="\\N")
            cursor.execute(upsert_sql)

    logger.info(f"✅ {len(df):,} rows upserted into {TARGET_TABLE}.")
    return len(df)


def run_dim_employee_pipeline() -> int:
    logger.info("=" * 60)
    logger.info(f"Starting {PIPELINE_NAME} pipeline (Upsert)")
    start_time = datetime.now()

    extractor = DataExtractor()
    loader    = DataLoader()

    try:
        execute_ddl(loader, DDL_DIM_EMPLOYEE, TARGET_TABLE)

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
    run_dim_employee_pipeline()
