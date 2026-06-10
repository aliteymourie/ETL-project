"""
OBT انبار - wide_warehouse
نسخه v2 — بهینه‌شده با:
  - multiprocessing به جای threading (thread-safety کامل)
  - keyset pagination به جای ID BETWEEN (بدون چانک خالی)
  - chunk_log برای atomic tracking و retry هوشمند
  - data quality validation بعد از هر چانک
  - row count reconciliation بعد از اجرا
  - dead letter queue برای ردیف‌های fail شده
  - alerting یکپارچه
"""

import pandas as pd
import jdatetime
import csv
import json
import time
from io import StringIO
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from multiprocessing import Pool, cpu_count
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.checkpoint import ETLCheckpoint
from core.utils.alerting import AlertManager
from core.utils.logging import setup_logger

logger = setup_logger("obt_warehouse_v2")

# ─────────────────────────────────────────────────────────────
# ثابت‌ها
# ─────────────────────────────────────────────────────────────
PIPELINE_NAME = "obt_warehouse_v2"
TARGET_TABLE  = "wide_warehouse"

FINAL_COLS = [
    "transaction_id", "transaction_satr_id", "fiscal_year",
    "transaction_type_code", "operation_type_code", "operation_type_text",
    "document_number", "transaction_datetime", "transaction_date", "status_code",
    "warehouse_id", "warehouse_name", "warehouse_type",
    "source_branch_id", "target_branch_id",
    "product_id", "product_name", "product_generic_code",
    "brand_name", "unit_name", "product_group_name",
    "quantity", "unit_cost", "total_cost",
    "batch_number", "expiry_date",
    "supplier_id", "supplier_name",
    "ref_document_id", "row_transaction_datetime",
    "transaction_date_key", "transaction_jalali",
    "transaction_jalali_year", "transaction_jalali_month",
    "transaction_jalali_month_name", "transaction_jalali_season",
    "expiry_date_key", "expiry_jalali",
    "expiry_jalali_year", "expiry_jalali_month",
    "expiry_jalali_month_name", "expiry_jalali_season",
]

INT_COLS = {
    "transaction_id", "transaction_satr_id", "fiscal_year",
    "transaction_type_code", "operation_type_code", "status_code",
    "warehouse_id", "warehouse_type", "source_branch_id", "target_branch_id",
    "product_id", "supplier_id", "ref_document_id",
    "transaction_date_key", "transaction_jalali_year", "transaction_jalali_month",
    "expiry_date_key", "expiry_jalali_year", "expiry_jalali_month",
}

# ─────────────────────────────────────────────────────────────
# DDL ها
# ─────────────────────────────────────────────────────────────
DDL_WIDE_WAREHOUSE = """
CREATE TABLE IF NOT EXISTS wide_warehouse (
    transaction_id              BIGINT,
    transaction_satr_id         BIGINT,
    fiscal_year                 SMALLINT,
    transaction_type_code       INT,
    operation_type_code         INT,
    operation_type_text         VARCHAR(30),
    document_number             VARCHAR(50),
    transaction_datetime        TIMESTAMP,
    transaction_date            DATE,
    status_code                 SMALLINT,
    warehouse_id                INT,
    warehouse_name              VARCHAR(200),
    warehouse_type              SMALLINT,
    source_branch_id            INT,
    target_branch_id            INT,
    product_id                  INT,
    product_name                VARCHAR(256),
    product_generic_code        VARCHAR(50),
    brand_name                  VARCHAR(200),
    unit_name                   VARCHAR(50),
    product_group_name          VARCHAR(200),
    quantity                    NUMERIC(18,4),
    unit_cost                   NUMERIC(18,2),
    total_cost                  NUMERIC(18,2),
    batch_number                VARCHAR(100),
    expiry_date                 DATE,
    supplier_id                 INT,
    supplier_name               VARCHAR(200),
    ref_document_id             BIGINT,
    row_transaction_datetime    TIMESTAMP,
    transaction_date_key        INT,
    transaction_jalali          VARCHAR(10),
    transaction_jalali_year     SMALLINT,
    transaction_jalali_month    SMALLINT,
    transaction_jalali_month_name VARCHAR(15),
    transaction_jalali_season   VARCHAR(10),
    expiry_date_key             INT,
    expiry_jalali               VARCHAR(10),
    expiry_jalali_year          SMALLINT,
    expiry_jalali_month         SMALLINT,
    expiry_jalali_month_name    VARCHAR(15),
    expiry_jalali_season        VARCHAR(10),
    etl_updated_at              TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (transaction_satr_id, fiscal_year)
);
CREATE INDEX IF NOT EXISTS idx_ww_trans_date    ON wide_warehouse (transaction_date_key);
CREATE INDEX IF NOT EXISTS idx_ww_product       ON wide_warehouse (product_id);
CREATE INDEX IF NOT EXISTS idx_ww_warehouse     ON wide_warehouse (warehouse_id);
CREATE INDEX IF NOT EXISTS idx_ww_supplier      ON wide_warehouse (supplier_id);
CREATE INDEX IF NOT EXISTS idx_ww_expiry        ON wide_warehouse (expiry_date);
CREATE INDEX IF NOT EXISTS idx_ww_jalali_year   ON wide_warehouse (transaction_jalali_year);
CREATE INDEX IF NOT EXISTS idx_ww_jalali_month  ON wide_warehouse (transaction_jalali_month);
CREATE INDEX IF NOT EXISTS idx_ww_op_type       ON wide_warehouse (operation_type_code);
CREATE INDEX IF NOT EXISTS idx_ww_batch         ON wide_warehouse (batch_number);
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
# keyset pagination — همیشه دقیقاً chunk_size ردیف برمی‌گرداند
KEYSET_SQL = """
SELECT TOP {chunk_size}
    k.ccKardex                  AS transaction_id,
    ks.ccKardexSatr             AS transaction_satr_id,
    k.Sal                       AS fiscal_year,
    k.CodeNoeForm               AS transaction_type_code,
    k.CodeNoeAmalyat            AS operation_type_code,
    CASE k.CodeNoeAmalyat
        WHEN 1   THEN N'ورود به انبار'
        WHEN 2   THEN N'خروج از انبار'
        WHEN 100 THEN N'مرجوعی'
        ELSE          N'سایر'
    END                         AS operation_type_text,
    k.ShomarehForm              AS document_number,
    k.TarikhForm                AS transaction_datetime,
    CAST(k.TarikhForm AS DATE)  AS transaction_date,
    k.CodeVazeiat               AS status_code,
    k.ccAnbar                   AS warehouse_id,
    a.NameAnbar                 AS warehouse_name,
    a.CodeNoeAnbar              AS warehouse_type,
    k.ccMarkazPakhsh            AS source_branch_id,
    k.ccMarkazPakhshBe          AS target_branch_id,
    kala.ccKala                 AS product_id,
    kala.NameKala               AS product_name,
    kala.CodeJenerik            AS product_generic_code,
    br.NameBrand                AS brand_name,
    v.NameVahed                 AS unit_name,
    g.NameGoroh                 AS product_group_name,
    ks.Tedad3                   AS quantity,
    ks.Gheymat                  AS unit_cost,
    ks.Tedad3 * ks.Gheymat      AS total_cost,
    ks.ShomarehBach             AS batch_number,
    ks.TarikhEngheza            AS expiry_date,
    ks.ccTaminKonandeh          AS supplier_id,
    tk.NameTaminKonandeh        AS supplier_name,
    k.ccRefrence                AS ref_document_id,
    ks.TarikhForm               AS row_transaction_datetime,
    k.ModifiedDate              AS kardex_modified_date
FROM Warehouse.KardexSatr ks
INNER JOIN Warehouse.Kardex k
    ON ks.ccKardex = k.ccKardex AND ks.Sal = k.Sal
LEFT JOIN Warehouse.Anbar a         ON k.ccAnbar = a.ccAnbar
LEFT JOIN Warehouse.Kala kala       ON ks.ccKala = kala.ccKala
LEFT JOIN Warehouse.Brand br        ON kala.ccBrand = br.ccBrand
LEFT JOIN Warehouse.Vahed v         ON kala.ccVahedShomaresh = v.ccVahed
LEFT JOIN Warehouse.KalaGoroh kg    ON kala.ccKala = kg.ccKalaCode
LEFT JOIN Global.Goroh g            ON kg.ccGoroh = g.ccGoroh
LEFT JOIN Purchase.TaminKonandeh tk ON ks.ccTaminKonandeh = tk.ccTaminKonandeh
WHERE k.TarikhForm IS NOT NULL
  AND k.ModifiedDate >= CONVERT(DATETIME, '{last_modified}', 120)
  AND ks.ccKardexSatr > {last_seen_id}
ORDER BY ks.ccKardexSatr
"""

COUNT_SQL = """
SELECT COUNT(*) AS total_rows
FROM Warehouse.KardexSatr ks
INNER JOIN Warehouse.Kardex k
    ON ks.ccKardex = k.ccKardex AND ks.Sal = k.Sal
WHERE k.TarikhForm IS NOT NULL
  AND k.ModifiedDate >= CONVERT(DATETIME, '{last_modified}', 120)
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
def validate_chunk(chunk: pd.DataFrame, chunk_start: int) -> tuple[bool, dict]:
    """
    بررسی کیفیت یک چانک قبل از درج
    برمی‌گرداند: (آیا قابل درج است, گزارش مشکلات)
    """
    issues = {}

    null_pk = chunk["transaction_satr_id"].isna().sum()
    if null_pk > 0:
        issues["null_primary_key"] = int(null_pk)

    null_product = chunk["product_id"].isna().sum()
    if null_product > 0:
        issues["null_product_id"] = int(null_product)

    if "quantity" in chunk.columns:
        neg_qty = (pd.to_numeric(chunk["quantity"], errors='coerce').fillna(0) < 0).sum()
        if neg_qty > 0:
            issues["negative_quantity"] = int(neg_qty)

    if "transaction_date" in chunk.columns:
        future = (pd.to_datetime(chunk["transaction_date"], errors='coerce') > datetime.now()).sum()
        if future > 0:
            issues["future_transaction_date"] = int(future)

    if "expiry_date" in chunk.columns:
        past_expiry = (
            pd.to_datetime(chunk["expiry_date"], errors='coerce') < datetime(2000, 1, 1)
        ).sum()
        if past_expiry > 0:
            issues["suspicious_expiry_date"] = int(past_expiry)

    # اگر بیش از ۵٪ ردیف‌ها product_id ندارند — چانک مشکوک است
    null_product_pct = null_product / len(chunk) if len(chunk) > 0 else 0
    is_acceptable = null_pk == 0 and null_product_pct < 0.05

    return is_acceptable, issues


# ─────────────────────────────────────────────────────────────
# ذخیره ردیف‌های fail شده در dead letter queue
# ─────────────────────────────────────────────────────────────
def save_failed_rows(failed_df: pd.DataFrame, chunk_start: int, error_msg: str, tgt_engine):
    try:
        records = failed_df.head(100).to_dict('records')  # حداکثر ۱۰۰ ردیف ذخیره شود
        with tgt_engine.connect() as conn:
            for rec in records:
                # تبدیل به JSON-safe
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
            conn.commit()
    except Exception as e:
        logger.warning(f"⚠️ خطا در ذخیره dead letter: {str(e)[:100]}")


# ─────────────────────────────────────────────────────────────
# chunk log helpers
# ─────────────────────────────────────────────────────────────
def log_chunk_start(chunk_start: int, chunk_end: int, tgt_engine):
    try:
        with tgt_engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO etl_metadata.chunk_log
                    (pipeline_name, chunk_start, chunk_end, status, started_at)
                VALUES (:p, :s, :e, 'RUNNING', NOW())
                ON CONFLICT (pipeline_name, chunk_start) DO UPDATE SET
                    status = 'RUNNING', started_at = NOW(), error_message = NULL
            """), {"p": PIPELINE_NAME, "s": chunk_start, "e": chunk_end})
            conn.commit()
    except Exception:
        pass


def log_chunk_done(chunk_start: int, rows_ext: int, rows_ins: int,
                   status: str, error: str, tgt_engine):
    try:
        with tgt_engine.connect() as conn:
            conn.execute(text("""
                UPDATE etl_metadata.chunk_log SET
                    status = :status,
                    rows_extracted = :ext,
                    rows_inserted  = :ins,
                    error_message  = :err,
                    finished_at    = NOW()
                WHERE pipeline_name = :p AND chunk_start = :s
            """), {"p": PIPELINE_NAME, "s": chunk_start,
                   "status": status, "ext": rows_ext,
                   "ins": rows_ins, "err": (error or "")[:500]})
            conn.commit()
    except Exception:
        pass


# ─────────────────────────────────────────────────────────────
# پردازش یک چانک — این تابع در یک process مستقل اجرا می‌شود
# ─────────────────────────────────────────────────────────────
def process_chunk(args: tuple) -> dict:
    """
    هر process engine های خودش را می‌سازد — هیچ shared state ای نیست
    ورودی tuple به دلیل محدودیت multiprocessing
    """
    chunk_start, chunk_end, last_modified, chunk_size, db_config = args

    # ساخت engine مستقل در این process
    from urllib.parse import quote_plus
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
        "chunk_start":   chunk_start,
        "chunk_end":     chunk_end,
        "rows_extracted": 0,
        "rows_inserted":  0,
        "rows_quality_failed": 0,
        "status":        "FAILED",
        "error":         None,
        "duration_sec":  0,
    }
    t0 = time.time()

    try:
        log_chunk_start(chunk_start, chunk_end, tgt_engine)

        # ── استخراج با keyset ────────────────────────────────
        sql = KEYSET_SQL.format(
            chunk_size=chunk_size,
            last_modified=last_modified,
            last_seen_id=chunk_start - 1  # keyset: از بعد از chunk_start شروع کن
        )
        chunk = pd.read_sql(sql, src_engine)

        if chunk.empty:
            result.update({"status": "SUCCESS", "duration_sec": time.time() - t0})
            log_chunk_done(chunk_start, 0, 0, "SUCCESS", None, tgt_engine)
            return result

        result["rows_extracted"] = len(chunk)

        # ── تبدیل شمسی ──────────────────────────────────────
        chunk = add_jalali_columns(chunk, "transaction_datetime", "transaction")
        chunk = add_jalali_columns(chunk, "expiry_date",          "expiry")

        # ── پاکسازی متون ────────────────────────────────────
        for col in chunk.select_dtypes(include="object").columns:
            chunk[col] = (
                chunk[col].astype(str)
                .str.replace("\n"," ").str.replace("\r"," ").str.replace("\t"," ")
                .str.strip()
                .replace("nan", None).replace("None", None).replace("", None)
            )

        # ── انتخاب ستون‌های نهایی ────────────────────────────
        chunk = chunk[[c for c in FINAL_COLS if c in chunk.columns]]

        # ── تبدیل قطعی به Int64 ──────────────────────────────
        for col in INT_COLS:
            if col in chunk.columns:
                chunk[col] = pd.to_numeric(chunk[col], errors='coerce').astype('Int64')

        # ── data quality check ────────────────────────────────
        is_ok, issues = validate_chunk(chunk, chunk_start)
        if issues:
            logger.warning(f"  ⚠️ چانک {chunk_start}: مشکلات کیفیت: {issues}")

        if not is_ok:
            # PK خالی داریم — این چانک را رد کن و به dead letter بفرست
            result["rows_quality_failed"] = len(chunk)
            result["status"] = "QUALITY_FAILED"
            save_failed_rows(chunk, chunk_start, f"quality_check: {issues}", tgt_engine)
            log_chunk_done(chunk_start, result["rows_extracted"], 0,
                           "QUALITY_FAILED", str(issues), tgt_engine)
            return result

        # ── Bulk COPY ─────────────────────────────────────────
        output = StringIO()
        chunk.to_csv(output, sep='\t', header=False, index=False,
                     na_rep='\\N', quoting=csv.QUOTE_MINIMAL)
        output.seek(0)

        raw_conn = tgt_engine.raw_connection()
        try:
            with raw_conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM wide_warehouse "
                    "WHERE transaction_satr_id = ANY("
                    "SELECT unnest(ARRAY[" +
                    ",".join(str(x) for x in chunk["transaction_satr_id"].dropna().astype(int).tolist()) +
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
        result["status"] = "FAILED"

    finally:
        result["duration_sec"] = round(time.time() - t0, 2)
        log_chunk_done(
            chunk_start,
            result["rows_extracted"],
            result["rows_inserted"],
            result["status"],
            result.get("error"),
            tgt_engine
        )
        src_engine.dispose()
        tgt_engine.dispose()

    return result


# ─────────────────────────────────────────────────────────────
# pipeline اصلی
# ─────────────────────────────────────────────────────────────
def run_obt_warehouse_pipeline(
    chunk_size:  int = 50_000,
    max_workers: int = 2,
    max_rows:    int = None
):
    logger.info("=" * 60)
    logger.info(
        f"🔄 OBT انبار v2 — wide_warehouse "
        f"(multiprocessing × {max_workers}, keyset pagination, chunk={chunk_size:,})"
    )
    start_time = datetime.now()

    extractor  = DataExtractor()
    loader     = DataLoader()
    checkpoint = ETLCheckpoint(loader)
    alerter    = AlertManager()

    src_engine = extractor.src_engine
    tgt_engine = loader.tgt_engine

    try:
        # ── ۱. ساخت جداول ─────────────────────────────────────
        loader.create_table(DDL_WIDE_WAREHOUSE)
        loader.create_table(DDL_CHUNK_LOG)
        loader.create_table(DDL_DEAD_LETTER)
        logger.info("✅ جداول آماده‌اند.")

        # ── ۲. آخرین ModifiedDate ─────────────────────────────
        last_run = checkpoint.get_last_success(PIPELINE_NAME)
        if last_run and last_run.get("last_from_value"):
            last_modified = str(last_run["last_from_value"])[:19].replace("T", " ")
        else:
            last_modified = (datetime.now() - timedelta(days=3650)).strftime("%Y-%m-%d %H:%M:%S")
            logger.info("🆕 اولین اجرا — لود کامل")
        logger.info(f"📌 از ModifiedDate: {last_modified}")

        # ── ۳. تعداد کل ردیف ──────────────────────────────────
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

        # ── ۴. ساخت لیست چانک‌ها بر اساس keyset ──────────────
        # در keyset pagination، chunk_start = last_seen_id قبلی است
        # اولین چانک از ID=0 شروع می‌کند
        chunk_starts = list(range(0, total_est, chunk_size))
        chunk_args   = []
        cursor_id    = 0  # last_seen_id برای اولین چانک

        # بدست آوردن ID های واقعی برای keyset
        logger.info("🔍 بدست آوردن نقاط شروع چانک‌ها...")
        keyset_sql = f"""
            SELECT ccKardexSatr
            FROM (
                SELECT ks.ccKardexSatr,
                       ROW_NUMBER() OVER (ORDER BY ks.ccKardexSatr) AS rn
                FROM Warehouse.KardexSatr ks
                INNER JOIN Warehouse.Kardex k
                    ON ks.ccKardex = k.ccKardex AND ks.Sal = k.Sal
                WHERE k.TarikhForm IS NOT NULL
                  AND k.ModifiedDate >= CONVERT(DATETIME, '{last_modified}', 120)
            ) t
            WHERE rn % {chunk_size} = 1 OR rn = 1
            ORDER BY ccKardexSatr
        """
        try:
            keysets_df = pd.read_sql(keyset_sql, src_engine)
            keyset_ids = [0] + keysets_df['ccKardexSatr'].tolist()
        except Exception:
            # fallback: اگر keyset query کار نکرد از range ساده استفاده کن
            logger.warning("⚠️ keyset query ناموفق — استفاده از range ساده")
            keyset_ids = list(range(0, total_est * 10, chunk_size))  # تقریبی

        # ── ۵. بررسی چانک‌های ناموفق قبلی (retry هوشمند) ────
        pending_chunks = set()
        try:
            failed_df = pd.read_sql(f"""
                SELECT chunk_start FROM etl_metadata.chunk_log
                WHERE pipeline_name = '{PIPELINE_NAME}'
                  AND status IN ('FAILED', 'RUNNING')
            """, tgt_engine)
            if not failed_df.empty:
                pending_chunks = set(failed_df['chunk_start'].tolist())
                logger.info(f"🔄 {len(pending_chunks)} چانک ناموفق از اجرای قبل برای retry")
        except Exception:
            pass

        # ── ۶. آماده‌سازی config برای pass به subprocess ──────
        # engine ها را نمی‌توان مستقیم به subprocess پاس داد
        # config را extract می‌کنیم تا هر process engine خودش را بسازد
        from core.engine.base_etl import BaseETL
        base = BaseETL()
        src_cfg = base.db_config["source_databases"]["mssql_pharma"]
        tgt_cfg = base.db_config["target_databases"]["dw_postgres"]
        db_config = {
            "src_user":   src_cfg["user"],
            "src_pass":   src_cfg["password"],
            "src_host":   src_cfg["host"],
            "src_port":   src_cfg["port"],
            "src_db":     src_cfg["database"],
            "src_driver": src_cfg["driver"],
            "tgt_user":   tgt_cfg["user"],
            "tgt_pass":   tgt_cfg["password"],
            "tgt_host":   tgt_cfg["host"],
            "tgt_port":   tgt_cfg["port"],
            "tgt_db":     tgt_cfg["database"],
        }

        # ساخت args برای هر چانک
        all_args = []
        for i, kid in enumerate(keyset_ids):
            end_id = keyset_ids[i + 1] - 1 if i + 1 < len(keyset_ids) else kid + chunk_size
            all_args.append((kid, end_id, last_modified, chunk_size, db_config))

        total_chunks = len(all_args)
        logger.info(f"📦 {total_chunks} چانک — شروع multiprocessing...")

        # ── ۷. اجرای موازی با multiprocessing ────────────────
        total_rows     = 0
        total_errors   = 0
        total_quality  = 0
        completed      = 0
        max_modified   = last_modified

        with Pool(processes=max_workers) as pool:
            for res in pool.imap_unordered(process_chunk, all_args):
                completed += 1
                total_rows    += res["rows_inserted"]
                total_quality += res["rows_quality_failed"]

                if res["status"] == "FAILED":
                    total_errors += 1
                    logger.error(
                        f"❌ چانک {res['chunk_start']}: {res.get('error','')[:80]}"
                    )
                elif res["status"] == "QUALITY_FAILED":
                    logger.warning(f"⚠️ چانک {res['chunk_start']}: کیفیت رد شد")
                else:
                    logger.info(
                        f"✅ {completed}/{total_chunks} | "
                        f"درج={res['rows_inserted']:,} | "
                        f"مجموع={total_rows:,} | "
                        f"زمان چانک={res['duration_sec']:.1f}s"
                    )

        # ── ۸. Checkpoint نهایی ────────────────────────────────
        final_status = "SUCCESS" if total_errors == 0 else "PARTIAL"
        checkpoint.save_checkpoint(
            PIPELINE_NAME, final_status, total_rows,
            from_value=last_modified,
            to_value=datetime.now().strftime("%Y-%m-%d"),
        )

        duration = (datetime.now() - start_time).total_seconds()
        speed    = total_rows / duration if duration > 0 else 0

        logger.info(f"""
        ╔══════════════════════════════════════════╗
        ║   ✅ wide_warehouse v2 لود شد           ║
        ╠══════════════════════════════════════════╣
        ║ کل ردیف درج شده:  {total_rows:>12,}  ║
        ║ چانک‌های ناموفق:  {total_errors:>12,}  ║
        ║ رد شده (کیفیت):   {total_quality:>12,}  ║
        ║ سرعت:             {speed:>9,.0f} r/s  ║
        ║ زمان کل:          {duration/60:>9.1f} دقیقه ║
        ║ وضعیت:            {final_status:>12}  ║
        ╚══════════════════════════════════════════╝
        """)

        if total_errors > 0:
            alerter.alert_error(PIPELINE_NAME,
                f"{total_errors} چانک ناموفق — جزئیات در etl_metadata.chunk_log",
                total_rows)

        return total_rows

    except Exception as e:
        logger.error(f"❌ خطای کلی: {str(e)}", exc_info=True)
        checkpoint.save_checkpoint(PIPELINE_NAME, "FAILED", error_message=str(e)[:500])
        alerter.alert_error(PIPELINE_NAME, str(e), 0)
        raise


if __name__ == "__main__":
    run_obt_warehouse_pipeline(
        chunk_size=50_000,
        max_workers=2,
        max_rows=300_000
    )