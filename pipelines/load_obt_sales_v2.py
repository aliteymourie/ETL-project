"""
OBT فروش (One Big Table) - wide_sales v2
نسخه پیشرفته با:
  - multiprocessing (thread-safety کامل)
  - keyset pagination (بدون چانک خالی)
  - chunk_log برای atomic tracking و retry هوشمند
  - data quality validation
  - dead letter queue
  - alerting یکپارچه
"""

import pandas as pd
import jdatetime
import csv
import json
import time
from io import StringIO
from datetime import datetime, timedelta
from multiprocessing import Pool
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.checkpoint import ETLCheckpoint
from core.utils.alerting import AlertManager
from core.utils.logging import setup_logger

logger = setup_logger("obt_sales_v2")

# ─────────────────────────────────────────────────────────────
# ثابت‌ها
# ─────────────────────────────────────────────────────────────
PIPELINE_NAME = "obt_sales_v2"
TARGET_TABLE  = "wide_sales"

FINAL_COLS = [
    "faktorsatr_id", "faktor_id", "fiscal_year", "invoice_number",
    "invoice_datetime", "invoice_date", "invoice_status_code", "invoice_status_text",
    "customer_id", "customer_name", "customer_economic_code", "customer_phone", "customer_city_name",
    "seller_id", "seller_name", "branch_id", "branch_name",
    "product_id", "product_name", "product_latin_name", "product_generic_code", "brand_name", "product_type_code",
    "quantity", "unit_price", "total_gross_amount",
    "row_discount", "row_tax", "row_other_charges", "row_net_amount",
    "invoice_net_total", "invoice_header_discount", "invoice_extra_charges",
    "order_datetime", "ship_datetime", "delivery_datetime",
    "invoice_date_key", "invoice_jalali", "invoice_jalali_year", "invoice_jalali_month",
    "invoice_jalali_month_name", "invoice_jalali_season",
    "ship_date_key", "ship_jalali", "ship_jalali_year", "ship_jalali_month",
    "ship_jalali_month_name", "ship_jalali_season",
    "delivery_date_key", "delivery_jalali", "delivery_jalali_year", "delivery_jalali_month",
    "delivery_jalali_month_name", "delivery_jalali_season",
]

INT_COLS = {
    "faktorsatr_id", "faktor_id", "fiscal_year",
    "invoice_status_code", "customer_id", "seller_id", "branch_id",
    "product_id", "product_type_code",
    "invoice_date_key", "invoice_jalali_year", "invoice_jalali_month",
    "ship_date_key", "ship_jalali_year", "ship_jalali_month",
    "delivery_date_key", "delivery_jalali_year", "delivery_jalali_month",
}

# ─────────────────────────────────────────────────────────────
# DDL ها
# ─────────────────────────────────────────────────────────────
DDL_WIDE_SALES = """
CREATE TABLE IF NOT EXISTS wide_sales (
    faktorsatr_id               BIGINT, faktor_id BIGINT, fiscal_year SMALLINT,
    invoice_number              VARCHAR(50), invoice_datetime TIMESTAMP, invoice_date DATE,
    invoice_status_code         SMALLINT, invoice_status_text VARCHAR(30),
    customer_id                 INT, customer_name VARCHAR(256), customer_economic_code VARCHAR(50),
    customer_phone              VARCHAR(50), customer_city_name VARCHAR(100),
    seller_id                   INT, seller_name VARCHAR(200), branch_id INT, branch_name VARCHAR(200),
    product_id                  INT, product_name VARCHAR(256), product_latin_name VARCHAR(256),
    product_generic_code        VARCHAR(50), brand_name VARCHAR(200), product_type_code SMALLINT,
    quantity                    NUMERIC(18,4), unit_price NUMERIC(18,2), total_gross_amount NUMERIC(18,2),
    row_discount                NUMERIC(18,2), row_tax NUMERIC(18,2), row_other_charges NUMERIC(18,2),
    row_net_amount              NUMERIC(18,2), invoice_net_total NUMERIC(18,2),
    invoice_header_discount     NUMERIC(18,2), invoice_extra_charges NUMERIC(18,2),
    order_datetime              TIMESTAMP, ship_datetime TIMESTAMP, delivery_datetime TIMESTAMP,
    invoice_date_key            INT, invoice_jalali VARCHAR(10), invoice_jalali_year SMALLINT,
    invoice_jalali_month        SMALLINT, invoice_jalali_month_name VARCHAR(15), invoice_jalali_season VARCHAR(10),
    ship_date_key               INT, ship_jalali VARCHAR(10), ship_jalali_year SMALLINT,
    ship_jalali_month           SMALLINT, ship_jalali_month_name VARCHAR(15), ship_jalali_season VARCHAR(10),
    delivery_date_key           INT, delivery_jalali VARCHAR(10), delivery_jalali_year SMALLINT,
    delivery_jalali_month       SMALLINT, delivery_jalali_month_name VARCHAR(15), delivery_jalali_season VARCHAR(10),
    etl_updated_at              TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (faktorsatr_id, fiscal_year)
);
CREATE INDEX IF NOT EXISTS idx_ws_invoice_date ON wide_sales (invoice_date_key);
CREATE INDEX IF NOT EXISTS idx_ws_customer ON wide_sales (customer_id);
CREATE INDEX IF NOT EXISTS idx_ws_product ON wide_sales (product_id);
CREATE INDEX IF NOT EXISTS idx_ws_jalali_year ON wide_sales (invoice_jalali_year);
"""

DDL_CHUNK_LOG = """
CREATE TABLE IF NOT EXISTS etl_metadata.chunk_log (
    pipeline_name   VARCHAR(100),
    chunk_start     BIGINT,
    chunk_end       BIGINT,
    status          VARCHAR(20) DEFAULT 'PENDING',
    rows_extracted  INT DEFAULT 0,
    rows_inserted   INT DEFAULT 0,
    error_message   TEXT,
    started_at      TIMESTAMP,
    finished_at     TIMESTAMP,
    PRIMARY KEY (pipeline_name, chunk_start)
);
"""

DDL_DEAD_LETTER = """
CREATE TABLE IF NOT EXISTS etl_metadata.failed_rows (
    id              BIGSERIAL PRIMARY KEY,
    pipeline_name   VARCHAR(100),
    chunk_start     BIGINT,
    row_data        JSONB,
    error_message   TEXT,
    created_at      TIMESTAMP DEFAULT NOW()
);
"""

# ─────────────────────────────────────────────────────────────
# SQL های اصلی
# ─────────────────────────────────────────────────────────────
KEYSET_SQL = """
SELECT TOP {chunk_size}
    dfs.ccDarkhastFaktorSatr    AS faktorsatr_id,
    dfs.ccDarkhastFaktor        AS faktor_id,
    df.Sal                      AS fiscal_year,
    df.ShomarehFaktor           AS invoice_number,
    df.TarikhFaktor             AS invoice_datetime,
    CAST(df.TarikhFaktor AS DATE) AS invoice_date,
    df.CodeVazeiat              AS invoice_status_code,
    CASE df.CodeVazeiat
        WHEN 0  THEN N'ثبت اولیه' WHEN 1  THEN N'بستن درخواست'
        WHEN 4  THEN N'فاکتور توزیع نشده' WHEN 5  THEN N'پیش بینی ارسال'
        WHEN 6  THEN N'ارسال به مسیر' WHEN 7  THEN N'تسویه'
        WHEN 8  THEN N'تسویه ناقص' WHEN 9  THEN N'رسید از پخش'
        WHEN 10 THEN N'رسید از مشتری' ELSE N'سایر'
    END                         AS invoice_status_text,
    m.ccMoshtary                AS customer_id,
    m.NameMoshtary              AS customer_name,
    m.CodeEghtesady             AS customer_economic_code,
    m.Telephone                 AS customer_phone,
    city.NameMahal              AS customer_city_name,
    f.ccForoshandeh             AS seller_id,
    f.SharhForoshandeh          AS seller_name,
    mp.NameMarkazPakhsh         AS branch_name,
    df.ccMarkazPakhsh           AS branch_id,
    k.ccKala                    AS product_id,
    k.NameKala                  AS product_name,
    k.NameLatin                 AS product_latin_name,
    k.CodeJenerik               AS product_generic_code,
    br.NameBrand                AS brand_name,
    k.CodeNoeKalaMalzomat       AS product_type_code,
    dfs.Tedad1                  AS quantity,
    dfs.MablaghForosh           AS unit_price,
    dfs.MablaghForosh * dfs.Tedad1 AS total_gross_amount,
    ISNULL(dfs.MablaghTakhfifFaktor, 0) AS row_discount,
    ISNULL(dfs.Maliat,   0)     AS row_tax,
    ISNULL(dfs.Avarez,   0)     AS row_other_charges,
    dfs.MablaghForoshKhalesKala AS row_net_amount,
    df.MablaghKhalesFaktor      AS invoice_net_total,
    ISNULL(df.MablaghTakhfifFaktorTitr, 0) AS invoice_header_discount,
    ISNULL(df.MablaghEzafat,    0) AS invoice_extra_charges,
    df.TarikhDarkhast           AS order_datetime,
    df.TarikhErsal              AS ship_datetime,
    df.TarikhTahvil             AS delivery_datetime,
    dfs.ModifiedDate            AS satr_modified_date,
    df.ModifiedDate             AS faktor_modified_date
FROM Sales.DarkhastFaktorSatr dfs
INNER JOIN Sales.DarkhastFaktor df ON dfs.ccDarkhastFaktor = df.ccDarkhastFaktor AND dfs.Sal = df.Sal
LEFT JOIN Sales.Moshtary m ON df.ccMoshtary = m.ccMoshtary
LEFT JOIN Global.Mahal city ON m.ccMahaleh = city.ccMahal
LEFT JOIN Sales.Foroshandeh f ON df.ccForoshandeh = f.ccForoshandeh
LEFT JOIN Global.MarkazPakhsh mp ON df.ccMarkazPakhsh = mp.ccMarkazPakhsh
LEFT JOIN Warehouse.Kala k ON dfs.ccKala = k.ccKala
LEFT JOIN Warehouse.Brand br ON k.ccBrand = br.ccBrand
WHERE df.TarikhFaktor IS NOT NULL
  AND df.ModifiedDate >= CONVERT(DATETIME, '{last_modified}', 120)
  AND dfs.ccDarkhastFaktorSatr > {last_seen_id}
ORDER BY dfs.ccDarkhastFaktorSatr
"""

COUNT_SQL = """
SELECT COUNT(*) AS total_rows
FROM Sales.DarkhastFaktorSatr dfs
INNER JOIN Sales.DarkhastFaktor df ON dfs.ccDarkhastFaktor = df.ccDarkhastFaktor AND dfs.Sal = df.Sal
WHERE df.TarikhFaktor IS NOT NULL
  AND df.ModifiedDate >= CONVERT(DATETIME, '{last_modified}', 120)
"""


# ─────────────────────────────────────────────────────────────
# تبدیل تاریخ شمسی
# ─────────────────────────────────────────────────────────────
def add_jalali_columns(df: pd.DataFrame, date_col: str, prefix: str) -> pd.DataFrame:
    dates = pd.to_datetime(df[date_col], errors='coerce')
    month_names = ['','فروردین','اردیبهشت','خرداد','تیر','مرداد',
                   'شهریور','مهر','آبان','آذر','دی','بهمن','اسفند']
    season_map  = {1:'بهار',2:'بهار',3:'بهار',4:'تابستان',5:'تابستان',6:'تابستان',
                   7:'پاییز',8:'پاییز',9:'پاییز',10:'زمستان',11:'زمستان',12:'زمستان'}
    def to_j(dt):
        if pd.isna(dt): return (None,)*5
        try:
            jd = jdatetime.date.fromgregorian(date=dt.date())
            return (f"{jd.year}/{jd.month:02d}/{jd.day:02d}",
                    jd.year, jd.month, month_names[jd.month], season_map[jd.month])
        except: return (None,)*5
    res = dates.map(to_j)
    df[f"{prefix}_jalali"]            = res.map(lambda x: x[0])
    df[f"{prefix}_jalali_year"]       = res.map(lambda x: x[1])
    df[f"{prefix}_jalali_month"]      = res.map(lambda x: x[2])
    df[f"{prefix}_jalali_month_name"] = res.map(lambda x: x[3])
    df[f"{prefix}_jalali_season"]     = res.map(lambda x: x[4])
    df[f"{prefix}_date_key"] = pd.to_numeric(
        dates.dt.strftime('%Y%m%d').where(dates.notna(), None), errors='coerce'
    ).astype('Int64')
    return df


# ─────────────────────────────────────────────────────────────
# data quality validation
# ─────────────────────────────────────────────────────────────
def validate_chunk(chunk: pd.DataFrame, chunk_start: int) -> tuple:
    issues = {}
    
    null_pk = chunk["faktorsatr_id"].isna().sum()
    if null_pk > 0:
        issues["null_primary_key"] = int(null_pk)
    
    null_product = chunk["product_id"].isna().sum()
    if null_product > 0:
        issues["null_product_id"] = int(null_product)
    
    if "quantity" in chunk.columns:
        neg_qty = (pd.to_numeric(chunk["quantity"], errors='coerce').fillna(0) < 0).sum()
        if neg_qty > 0:
            issues["negative_quantity"] = int(neg_qty)
    
    if "fi_forosh" in chunk.columns:
        neg_price = (pd.to_numeric(chunk["unit_price"], errors='coerce').fillna(0) < 0).sum()
        if neg_price > 0:
            issues["negative_price"] = int(neg_price)
    
    if "invoice_date" in chunk.columns:
        future = (pd.to_datetime(chunk["invoice_date"], errors='coerce') > datetime.now()).sum()
        if future > 0:
            issues["future_invoice_date"] = int(future)
    
    null_product_pct = null_product / len(chunk) if len(chunk) > 0 else 0
    is_acceptable = null_pk == 0 and null_product_pct < 0.05
    
    return is_acceptable, issues


# ─────────────────────────────────────────────────────────────
# dead letter queue
# ─────────────────────────────────────────────────────────────
def save_failed_rows(failed_df: pd.DataFrame, chunk_start: int, error_msg: str, tgt_engine):
    try:
        records = failed_df.head(100).to_dict('records')
        with tgt_engine.begin() as conn:
            for rec in records:
                clean = {k: (str(v) if not isinstance(v, (int, float, str, type(None))) else v)
                         for k, v in rec.items()}
                conn.execute(text("""
                    INSERT INTO etl_metadata.failed_rows
                        (pipeline_name, chunk_start, row_data, error_message)
                    VALUES (:pipeline, :chunk, :data, :error)
                """), {
                    "pipeline": PIPELINE_NAME,
                    "chunk": chunk_start,
                    "data": json.dumps(clean, ensure_ascii=False, default=str),
                    "error": error_msg[:500]
                })
    except Exception as e:
        logger.warning(f"⚠️ خطا در ذخیره dead letter: {str(e)[:100]}")


# ─────────────────────────────────────────────────────────────
# chunk log helpers
# ─────────────────────────────────────────────────────────────
def log_chunk_start(chunk_start: int, chunk_end: int, tgt_engine):
    try:
        with tgt_engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO etl_metadata.chunk_log
                    (pipeline_name, chunk_start, chunk_end, status, started_at)
                VALUES (:p, :s, :e, 'RUNNING', NOW())
                ON CONFLICT (pipeline_name, chunk_start) DO UPDATE SET
                    status = 'RUNNING', started_at = NOW(), error_message = NULL
            """), {"p": PIPELINE_NAME, "s": chunk_start, "e": chunk_end})
    except Exception:
        pass


def log_chunk_done(chunk_start: int, rows_ext: int, rows_ins: int,
                   status: str, error: str, tgt_engine):
    try:
        with tgt_engine.begin() as conn:
            conn.execute(text("""
                UPDATE etl_metadata.chunk_log SET
                    status = :status, rows_extracted = :ext, rows_inserted = :ins,
                    error_message = :err, finished_at = NOW()
                WHERE pipeline_name = :p AND chunk_start = :s
            """), {"p": PIPELINE_NAME, "s": chunk_start,
                   "status": status, "ext": rows_ext,
                   "ins": rows_ins, "err": (error or "")[:500]})
    except Exception:
        pass


# ─────────────────────────────────────────────────────────────
# پردازش یک چانک - multiprocessing
# ─────────────────────────────────────────────────────────────
def process_chunk(args: tuple) -> dict:
    chunk_start, chunk_end, last_modified, chunk_size, db_config = args
    
    from urllib.parse import quote_plus
    from sqlalchemy import create_engine
    
    src_conn = (
        f"mssql+pyodbc://{db_config['src_user']}:{quote_plus(db_config['src_pass'])}"
        f"@{db_config['src_host']}:{db_config['src_port']}/{db_config['src_db']}"
        f"?driver={db_config['src_driver'].replace(' ', '+')}"
    )
    tgt_conn = (
        f"postgresql://{db_config['tgt_user']}:{db_config['tgt_pass']}"
        f"@{db_config['tgt_host']}:{db_config['tgt_port']}/{db_config['tgt_db']}"
    )
    src_engine = create_engine(src_conn, fast_executemany=True, pool_pre_ping=True)
    tgt_engine = create_engine(tgt_conn, pool_pre_ping=True)

    result = {
        "chunk_start": chunk_start, "chunk_end": chunk_end,
        "rows_extracted": 0, "rows_inserted": 0,
        "rows_quality_failed": 0, "status": "FAILED",
        "error": None, "duration_sec": 0,
    }
    t0 = time.time()

    try:
        log_chunk_start(chunk_start, chunk_end, tgt_engine)

        sql = KEYSET_SQL.format(
            chunk_size=chunk_size,
            last_modified=last_modified,
            last_seen_id=chunk_start - 1
        )
        chunk = pd.read_sql(sql, src_engine)

        if chunk.empty:
            result.update({"status": "SUCCESS", "duration_sec": time.time() - t0})
            log_chunk_done(chunk_start, 0, 0, "SUCCESS", None, tgt_engine)
            return result

        result["rows_extracted"] = len(chunk)

        chunk = add_jalali_columns(chunk, "invoice_datetime", "invoice")
        chunk = add_jalali_columns(chunk, "ship_datetime", "ship")
        chunk = add_jalali_columns(chunk, "delivery_datetime", "delivery")

        for col in chunk.select_dtypes(include="object").columns:
            chunk[col] = (
                chunk[col].astype(str)
                .str.replace("\n"," ").str.replace("\r"," ").str.replace("\t"," ")
                .str.strip()
                .replace("nan", None).replace("None", None).replace("", None)
            )

        chunk = chunk[[c for c in FINAL_COLS if c in chunk.columns]]

        for col in INT_COLS:
            if col in chunk.columns:
                chunk[col] = pd.to_numeric(chunk[col], errors='coerce').fillna(-1).astype(int).replace(-1, None)

        is_ok, issues = validate_chunk(chunk, chunk_start)
        if issues:
            logger.warning(f"  ⚠️ چانک {chunk_start}: مشکلات کیفیت: {issues}")

        if not is_ok:
            result["rows_quality_failed"] = len(chunk)
            result["status"] = "QUALITY_FAILED"
            save_failed_rows(chunk, chunk_start, f"quality_check: {issues}", tgt_engine)
            log_chunk_done(chunk_start, result["rows_extracted"], 0, "QUALITY_FAILED", str(issues), tgt_engine)
            return result

        output = StringIO()
        chunk.to_csv(output, sep='\t', header=False, index=False,
                     na_rep='\\N', quoting=csv.QUOTE_MINIMAL)
        output.seek(0)

        raw_conn = tgt_engine.raw_connection()
        try:
            with raw_conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM wide_sales WHERE faktorsatr_id = ANY("
                    "SELECT unnest(ARRAY[" +
                    ",".join(str(x) for x in chunk["faktorsatr_id"].dropna().astype(int).tolist()) +
                    "]))"
                )
                cursor.copy_from(
                    output, TARGET_TABLE,
                    columns=[c for c in FINAL_COLS if c in chunk.columns],
                    null='\\N'
                )
            raw_conn.commit()
            result["rows_inserted"] = len(chunk)
            result["status"] = "SUCCESS"
        except Exception as e:
            raw_conn.rollback()
            result["error"] = str(e)[:300]
            result["status"] = "FAILED"
            save_failed_rows(chunk, chunk_start, str(e), tgt_engine)
            raise
        finally:
            raw_conn.close()

    except Exception as e:
        result["error"] = str(e)[:300]
    finally:
        result["duration_sec"] = round(time.time() - t0, 2)
        log_chunk_done(chunk_start, result["rows_extracted"], result["rows_inserted"],
                       result["status"], result.get("error"), tgt_engine)
        src_engine.dispose()
        tgt_engine.dispose()

    return result


# ─────────────────────────────────────────────────────────────
# pipeline اصلی
# ─────────────────────────────────────────────────────────────
def run_obt_sales_pipeline_v2(
    chunk_size:  int = 100_000,
    max_workers: int = 4,
    max_rows:    int = None
):
    logger.info("=" * 60)
    logger.info(f"🔄 OBT فروش v2 — wide_sales (multiprocessing × {max_workers}, chunk={chunk_size:,})")
    start_time = datetime.now()

    extractor = DataExtractor()
    loader = DataLoader()
    checkpoint = ETLCheckpoint(loader)
    alerter = AlertManager()

    src_engine = extractor.src_engine
    tgt_engine = loader.tgt_engine

    try:
        loader.create_table(DDL_WIDE_SALES)
        loader.create_table(DDL_CHUNK_LOG)
        loader.create_table(DDL_DEAD_LETTER)
        logger.info("✅ جداول آماده‌اند.")

        last_run = checkpoint.get_last_success(PIPELINE_NAME)
        if last_run and last_run.get("last_from_value"):
            last_modified = str(last_run["last_from_value"])[:19].replace("T", " ")
        else:
            last_modified = (datetime.now() - timedelta(days=3650)).strftime("%Y-%m-%d %H:%M:%S")
            logger.info("🆕 اولین اجرا — لود کامل")
        logger.info(f"📌 از ModifiedDate: {last_modified}")

        logger.info("🔍 شمارش ردیف‌های جدید...")
        total_est = pd.read_sql(
            COUNT_SQL.format(last_modified=last_modified), src_engine
        )['total_rows'].iloc[0]

        if total_est == 0:
            logger.info("✅ هیچ داده جدیدی یافت نشد.")
            checkpoint.save_checkpoint(PIPELINE_NAME, "SUCCESS", 0)
            return 0

        logger.info(f"📊 {total_est:,} ردیف برای پردازش")

        if max_rows:
            total_est = min(total_est, max_rows)
            logger.info(f"🧪 محدودیت تست: {total_est:,} ردیف")

        # keyset pagination
        logger.info("🔍 بدست آوردن نقاط شروع چانک‌ها...")
        keyset_sql = f"""
            SELECT ccDarkhastFaktorSatr
            FROM (
                SELECT dfs.ccDarkhastFaktorSatr,
                       ROW_NUMBER() OVER (ORDER BY dfs.ccDarkhastFaktorSatr) AS rn
                FROM Sales.DarkhastFaktorSatr dfs
                INNER JOIN Sales.DarkhastFaktor df
                    ON dfs.ccDarkhastFaktor = df.ccDarkhastFaktor AND dfs.Sal = df.Sal
                WHERE df.TarikhFaktor IS NOT NULL
                  AND df.ModifiedDate >= CONVERT(DATETIME, '{last_modified}', 120)
            ) t
            WHERE rn % {chunk_size} = 1 OR rn = 1
            ORDER BY ccDarkhastFaktorSatr
        """
        try:
            keysets_df = pd.read_sql(keyset_sql, src_engine)
            keyset_ids = [0] + keysets_df['ccDarkhastFaktorSatr'].tolist()
        except Exception:
            logger.warning("⚠️ keyset query ناموفق — استفاده از range ساده")
            keyset_ids = list(range(0, total_est * 100, chunk_size))

        # db_config برای subprocess
        from urllib.parse import quote_plus
        db_config = {
            "src_user":   extractor.src_engine.url.username,
            "src_pass":   extractor.src_engine.url.password,
            "src_host":   extractor.src_engine.url.host,
            "src_port":   extractor.src_engine.url.port or 1433,
            "src_db":     extractor.src_engine.url.database,
            "src_driver": "ODBC+Driver+17+for+SQL+Server",
            "tgt_user":   loader.tgt_engine.url.username,
            "tgt_pass":   loader.tgt_engine.url.password,
            "tgt_host":   loader.tgt_engine.url.host,
            "tgt_port":   loader.tgt_engine.url.port or 5432,
            "tgt_db":     loader.tgt_engine.url.database,
        }

        all_args = []
        for i, kid in enumerate(keyset_ids):
            end_id = keyset_ids[i + 1] - 1 if i + 1 < len(keyset_ids) else kid + chunk_size
            all_args.append((kid, end_id, last_modified, chunk_size, db_config))

        total_chunks = len(all_args)
        logger.info(f"📦 {total_chunks} چانک — شروع multiprocessing...")

        total_rows = 0
        total_errors = 0
        completed = 0

        with Pool(processes=max_workers) as pool:
            for res in pool.imap_unordered(process_chunk, all_args):
                completed += 1
                total_rows += res["rows_inserted"]
                
                if res["status"] == "FAILED":
                    total_errors += 1
                    logger.error(f"❌ چانک {res['chunk_start']}: {res.get('error','')[:80]}")
                elif res["status"] == "QUALITY_FAILED":
                    logger.warning(f"⚠️ چانک {res['chunk_start']}: کیفیت رد شد")
                else:
                    progress = completed / total_chunks * 100
                    elapsed = (datetime.now() - start_time).total_seconds()
                    eta_min = (elapsed / completed * (total_chunks - completed)) / 60 if completed > 0 else 0
                    logger.info(
                        f"✅ {completed}/{total_chunks} ({progress:.0f}%) | "
                        f"درج={res['rows_inserted']:,} | "
                        f"مجموع={total_rows:,} | ETA: {eta_min:.0f} دقیقه | "
                        f"زمان چانک={res['duration_sec']:.1f}s"
                    )

        final_status = "SUCCESS" if total_errors == 0 else "PARTIAL"
        checkpoint.save_checkpoint(PIPELINE_NAME, final_status, total_rows,
                                  from_value=last_modified, to_value=datetime.now().strftime("%Y-%m-%d"))

        duration = (datetime.now() - start_time).total_seconds()
        speed = total_rows / duration if duration > 0 else 0

        logger.info(f"""
        ╔══════════════════════════════════════════╗
        ║   ✅ wide_sales v2 لود شد               ║
        ╠══════════════════════════════════════════╣
        ║ کل ردیف:  {total_rows:>15,}  ║
        ║ خطا:      {total_errors:>15,}  ║
        ║ سرعت:     {speed:>12,.0f} r/s  ║
        ║ زمان:     {duration/60:>12.1f} دقیقه ║
        ║ وضعیت:    {final_status:>15}  ║
        ╚══════════════════════════════════════════╝
        """)

        if total_errors > 0:
            alerter.alert_error(PIPELINE_NAME, f"{total_errors} چانک ناموفق", total_rows)

        return total_rows

    except Exception as e:
        logger.error(f"❌ خطای کلی: {str(e)}", exc_info=True)
        checkpoint.save_checkpoint(PIPELINE_NAME, "FAILED", error_message=str(e)[:500])
        alerter.alert_error(PIPELINE_NAME, str(e), 0)
        raise


if __name__ == "__main__":
    run_obt_sales_pipeline_v2(chunk_size=100_000, max_workers=4, max_rows=300_000)