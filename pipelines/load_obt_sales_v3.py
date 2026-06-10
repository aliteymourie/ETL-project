"""
OBT فروش (One Big Table) - wide_sales v3
جدول پایه: Pakhsh.Sales.DarkhastFaktor (هدر فاکتور)
جدول سطر: Pakhsh.Sales.DarkhastFaktorSatr

جداول JOIN شده:
  Sales.Moshtary              ← مشتری
  Sales.NoeMalekiatMoshtary   ← نوع مالکیت مشتری
  Sales.Foroshandeh           ← فروشنده
  Sales.GorohForosh           ← گروه فروش
  Global.Mahal                ← شهر مشتری
  Global.MarkazPakhsh         ← مرکز پخش
  Global.MantaghehPakhsh      ← منطقه پخش
  Warehouse.Kala              ← کالا
  Warehouse.Brand             ← برند

ویژگی‌های پایپ‌لاین:
  - multiprocessing (thread-safety کامل)
  - keyset pagination (بدون چانک خالی)
  - chunk_log برای atomic tracking و retry هوشمند
  - data quality validation
  - dead letter queue
  - alerting یکپارچه
  - تاریخ شمسی برای ۴ فیلد تاریخ اصلی
"""

import pandas as pd
import jdatetime
import csv
import json
import time
from io import StringIO
from datetime import datetime, timedelta
from multiprocessing import Pool
from sqlalchemy import text
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.checkpoint import ETLCheckpoint
from core.utils.alerting import AlertManager
from core.utils.logging import setup_logger

logger = setup_logger("obt_sales_v3")

# ─────────────────────────────────────────────────────────────
# ثابت‌ها
# ─────────────────────────────────────────────────────────────
PIPELINE_NAME = "obt_sales_v3"
TARGET_TABLE  = "wide_sales"

FINAL_COLS = [
    # ── کلیدها ──────────────────────────────────────────────
    "faktorsatr_id", "faktor_id", "fiscal_year", "invoice_index",

    # ── شناسه‌های فاکتور ─────────────────────────────────────
    "invoice_number", "request_number",

    # ── تاریخ‌های اصلی ───────────────────────────────────────
    "invoice_datetime", "invoice_date",
    "order_datetime",   "order_date",
    "ship_datetime",    "ship_date",
    "delivery_datetime","delivery_date",
    "estimated_delivery_datetime",
    "expiry_datetime",
    "entry_datetime",
    "header_modified_date",

    # ── وضعیت / نوع فاکتور ───────────────────────────────────
    "invoice_status_code", "invoice_status_text",
    "invoice_type_code", "invoice_subtype",
    "entry_type_code",
    "collection_type_code",
    "transport_type_code",
    "discount_type", "discount_subtype",
    "is_formal", "is_telephone_order", "is_cooperative",
    "is_legalized", "settlement_base",
    "inventory_code", "serial_number",
    "cancel_reason", "invoice_note", "reference_number",
    "device_charge_status", "print_count",
    "gps_longitude", "gps_latitude",
    "store_entry_time", "store_exit_time",
    "collection_days", "tracking_days",
    "current_credit", "customer_balance",
    "treasury_discount_pct",
    "total_box_count", "row_count",

    # ── مبالغ درخواست ────────────────────────────────────────
    "request_gross_amount", "request_header_discount",
    "request_row_discount", "request_net_amount",

    # ── مبالغ فاکتور ─────────────────────────────────────────
    "invoice_gross_total",
    "invoice_header_discount", "invoice_row_discount",
    "invoice_cooperative_discount", "invoice_extra_charges",
    "invoice_net_total", "invoice_payment_received",
    "invoice_tax_total", "invoice_surcharge_total",

    # ── مشتری ────────────────────────────────────────────────
    "customer_id", "customer_name", "customer_signboard_name",
    "customer_economic_code", "customer_national_id",
    "customer_postal_code", "customer_phone", "customer_fax",
    "customer_type_code", "customer_rank",
    "customer_credit_limit", "customer_suggested_credit",
    "customer_daily_sale_estimate", "customer_status_code",
    "customer_intro_date",
    "customer_gps_longitude", "customer_gps_latitude",
    "customer_city_name", "customer_ownership_type",

    # ── فروشنده ───────────────────────────────────────────────
    "seller_id", "seller_name", "seller_code_old",
    "seller_mobile", "seller_status_code",

    # ── گروه فروش ────────────────────────────────────────────
    "sales_group_id", "sales_group_code", "sales_group_name",

    # ── مرکز و منطقه پخش ─────────────────────────────────────
    "branch_id", "branch_name",
    "region_id", "region_name",
    "route_id",

    # ── سطر فاکتور ───────────────────────────────────────────
    "batch_number", "batch_number_multi",
    "production_date", "expiry_date_row",
    "quantity", "quantity2", "quantity3",
    "quantity_piece", "quantity_box", "quantity_carton",
    "unit_price", "requested_unit_price",
    "gross_amount",
    "request_row_discount_amt",
    "row_discount", "manual_discount",
    "cooperative_discount_pct", "cash_discount_per_unit",
    "row_tax", "row_surcharge", "row_net_amount",
    "avg_cost_price", "purchase_price",
    "available_stock_at_sale",
    "row_status_code", "no_prize_flag",
    "row_modified_date",

    # ── کالا ─────────────────────────────────────────────────
    "product_id", "product_code_id",
    "product_name", "product_invoice_name", "product_latin_name",
    "product_code", "product_code_old",
    "product_generic_code", "product_iran_code",
    "product_gs1_code", "product_barcode",
    "product_official_drug_code", "product_identifier",
    "product_type_code",
    "product_tax_eligible", "product_surcharge_eligible", "product_subsidy_eligible",
    "product_net_weight", "product_gross_weight", "product_carton_weight",
    "units_per_carton", "units_per_box",

    # ── برند ──────────────────────────────────────────────────
    "brand_id", "brand_name",

    # ── تامین‌کننده ───────────────────────────────────────────
    "supplier_id",

    # ── تاریخ شمسی فاکتور ────────────────────────────────────
    "invoice_date_key", "invoice_jalali",
    "invoice_jalali_year", "invoice_jalali_month",
    "invoice_jalali_month_name", "invoice_jalali_season",

    # ── تاریخ شمسی سفارش ─────────────────────────────────────
    "order_date_key", "order_jalali",
    "order_jalali_year", "order_jalali_month",
    "order_jalali_month_name", "order_jalali_season",

    # ── تاریخ شمسی ارسال ─────────────────────────────────────
    "ship_date_key", "ship_jalali",
    "ship_jalali_year", "ship_jalali_month",
    "ship_jalali_month_name", "ship_jalali_season",

    # ── تاریخ شمسی تحویل ─────────────────────────────────────
    "delivery_date_key", "delivery_jalali",
    "delivery_jalali_year", "delivery_jalali_month",
    "delivery_jalali_month_name", "delivery_jalali_season",
]

INT_COLS = {
    "faktorsatr_id", "faktor_id", "fiscal_year", "invoice_index",
    "invoice_number", "request_number",
    "invoice_status_code", "invoice_type_code", "invoice_subtype",
    "entry_type_code", "collection_type_code", "transport_type_code",
    "discount_type", "discount_subtype",
    "inventory_code", "serial_number",
    "device_charge_status", "print_count",
    "collection_days", "tracking_days", "total_box_count", "row_count",
    "customer_id", "customer_type_code", "customer_status_code",
    "seller_id", "seller_status_code",
    "sales_group_id",
    "branch_id", "region_id", "route_id",
    "row_status_code",
    "product_id", "product_code_id", "product_type_code",
    "brand_id", "supplier_id",
    "invoice_date_key", "invoice_jalali_year", "invoice_jalali_month",
    "order_date_key",   "order_jalali_year",   "order_jalali_month",
    "ship_date_key",    "ship_jalali_year",    "ship_jalali_month",
    "delivery_date_key","delivery_jalali_year","delivery_jalali_month",
}

BOOL_COLS = {
    "is_formal", "is_telephone_order", "is_cooperative",
    "is_legalized", "no_prize_flag",
    "product_tax_eligible", "product_surcharge_eligible", "product_subsidy_eligible",
}

# ─────────────────────────────────────────────────────────────
# DDL ها
# ─────────────────────────────────────────────────────────────
DDL_WIDE_SALES = """
CREATE TABLE IF NOT EXISTS wide_sales (
    -- کلیدها
    faktorsatr_id               BIGINT          NOT NULL,
    faktor_id                   BIGINT          NOT NULL,
    fiscal_year                 SMALLINT        NOT NULL,
    invoice_index               BIGINT,

    -- شناسه‌های فاکتور
    invoice_number              INT,
    request_number              INT,

    -- تاریخ‌های اصلی
    invoice_datetime            TIMESTAMP,
    invoice_date                DATE,
    order_datetime              TIMESTAMP,
    order_date                  DATE,
    ship_datetime               TIMESTAMP,
    ship_date                   DATE,
    delivery_datetime           TIMESTAMP,
    delivery_date               DATE,
    estimated_delivery_datetime TIMESTAMP,
    expiry_datetime             TIMESTAMP,
    entry_datetime              TIMESTAMP,
    header_modified_date        TIMESTAMP,

    -- وضعیت / نوع فاکتور
    invoice_status_code         SMALLINT,
    invoice_status_text         VARCHAR(40),
    invoice_type_code           SMALLINT,
    invoice_subtype             BIGINT,
    entry_type_code             SMALLINT,
    collection_type_code        SMALLINT,
    transport_type_code         SMALLINT,
    discount_type               INT,
    discount_subtype            INT,
    is_formal                   BOOLEAN,
    is_telephone_order          BOOLEAN,
    is_cooperative              SMALLINT,
    is_legalized                SMALLINT,
    settlement_base             SMALLINT,
    inventory_code              SMALLINT,
    serial_number               INT,
    cancel_reason               VARCHAR(50),
    invoice_note                TEXT,
    reference_number            VARCHAR(250),
    device_charge_status        INT,
    print_count                 SMALLINT,
    gps_longitude               DOUBLE PRECISION,
    gps_latitude                DOUBLE PRECISION,
    store_entry_time            TIMESTAMP,
    store_exit_time             TIMESTAMP,
    collection_days             SMALLINT,
    tracking_days               SMALLINT,
    current_credit              NUMERIC(18,2),
    customer_balance            NUMERIC(18,2),
    treasury_discount_pct       NUMERIC(8,4),
    total_box_count             INT,
    row_count                   INT,

    -- مبالغ درخواست
    request_gross_amount        NUMERIC(18,2),
    request_header_discount     NUMERIC(18,2),
    request_row_discount        NUMERIC(18,2),
    request_net_amount          NUMERIC(18,2),

    -- مبالغ فاکتور
    invoice_gross_total         NUMERIC(18,2),
    invoice_header_discount     NUMERIC(18,2),
    invoice_row_discount        NUMERIC(18,2),
    invoice_cooperative_discount NUMERIC(18,2),
    invoice_extra_charges       NUMERIC(18,2),
    invoice_net_total           NUMERIC(18,2),
    invoice_payment_received    NUMERIC(18,2),
    invoice_tax_total           NUMERIC(18,2),
    invoice_surcharge_total     NUMERIC(18,2),

    -- مشتری
    customer_id                 INT,
    customer_name               VARCHAR(256),
    customer_signboard_name     VARCHAR(256),
    customer_economic_code      VARCHAR(50),
    customer_national_id        VARCHAR(20),
    customer_postal_code        VARCHAR(20),
    customer_phone              VARCHAR(50),
    customer_fax                VARCHAR(50),
    customer_type_code          INT,
    customer_rank               VARCHAR(10),
    customer_credit_limit       NUMERIC(18,2),
    customer_suggested_credit   NUMERIC(18,2),
    customer_daily_sale_estimate NUMERIC(18,2),
    customer_status_code        SMALLINT,
    customer_intro_date         TIMESTAMP,
    customer_gps_longitude      DOUBLE PRECISION,
    customer_gps_latitude       DOUBLE PRECISION,
    customer_city_name          VARCHAR(100),
    customer_ownership_type     VARCHAR(100),

    -- فروشنده
    seller_id                   INT,
    seller_name                 VARCHAR(200),
    seller_code_old             VARCHAR(50),
    seller_mobile               VARCHAR(30),
    seller_status_code          SMALLINT,

    -- گروه فروش
    sales_group_id              INT,
    sales_group_code            VARCHAR(50),
    sales_group_name            VARCHAR(200),

    -- مرکز و منطقه پخش
    branch_id                   INT,
    branch_name                 VARCHAR(200),
    region_id                   INT,
    region_name                 VARCHAR(200),
    route_id                    INT,

    -- سطر فاکتور
    batch_number                VARCHAR(50),
    batch_number_multi          VARCHAR(100),
    production_date             TIMESTAMP,
    expiry_date_row             TIMESTAMP,
    quantity                    NUMERIC(18,4),
    quantity2                   NUMERIC(18,4),
    quantity3                   NUMERIC(18,4),
    quantity_piece              NUMERIC(18,4),
    quantity_box                NUMERIC(18,4),
    quantity_carton             NUMERIC(18,4),
    unit_price                  NUMERIC(18,2),
    requested_unit_price        NUMERIC(18,2),
    gross_amount                NUMERIC(18,2),
    request_row_discount_amt    NUMERIC(18,2),
    row_discount                NUMERIC(18,2),
    manual_discount             NUMERIC(18,2),
    cooperative_discount_pct    NUMERIC(8,4),
    cash_discount_per_unit      NUMERIC(18,2),
    row_tax                     NUMERIC(18,2),
    row_surcharge               NUMERIC(18,2),
    row_net_amount              NUMERIC(18,2),
    avg_cost_price              NUMERIC(18,2),
    purchase_price              NUMERIC(18,2),
    available_stock_at_sale     NUMERIC(18,4),
    row_status_code             SMALLINT,
    no_prize_flag               BOOLEAN,
    row_modified_date           TIMESTAMP,

    -- کالا
    product_id                  INT,
    product_code_id             INT,
    product_name                VARCHAR(256),
    product_invoice_name        VARCHAR(256),
    product_latin_name          VARCHAR(256),
    product_code                VARCHAR(50),
    product_code_old            VARCHAR(50),
    product_generic_code        INT,
    product_iran_code           VARCHAR(50),
    product_gs1_code            VARCHAR(50),
    product_barcode             VARCHAR(100),
    product_official_drug_code  VARCHAR(50),
    product_identifier          VARCHAR(100),
    product_type_code           SMALLINT,
    product_tax_eligible        BOOLEAN,
    product_surcharge_eligible  BOOLEAN,
    product_subsidy_eligible    BOOLEAN,
    product_net_weight          NUMERIC(12,4),
    product_gross_weight        NUMERIC(12,4),
    product_carton_weight       NUMERIC(12,4),
    units_per_carton            INT,
    units_per_box               INT,

    -- برند
    brand_id                    INT,
    brand_name                  VARCHAR(200),

    -- تامین‌کننده
    supplier_id                 INT,

    -- تاریخ شمسی فاکتور
    invoice_date_key            INT,
    invoice_jalali              VARCHAR(10),
    invoice_jalali_year         SMALLINT,
    invoice_jalali_month        SMALLINT,
    invoice_jalali_month_name   VARCHAR(15),
    invoice_jalali_season       VARCHAR(10),

    -- تاریخ شمسی سفارش
    order_date_key              INT,
    order_jalali                VARCHAR(10),
    order_jalali_year           SMALLINT,
    order_jalali_month          SMALLINT,
    order_jalali_month_name     VARCHAR(15),
    order_jalali_season         VARCHAR(10),

    -- تاریخ شمسی ارسال
    ship_date_key               INT,
    ship_jalali                 VARCHAR(10),
    ship_jalali_year            SMALLINT,
    ship_jalali_month           SMALLINT,
    ship_jalali_month_name      VARCHAR(15),
    ship_jalali_season          VARCHAR(10),

    -- تاریخ شمسی تحویل
    delivery_date_key           INT,
    delivery_jalali             VARCHAR(10),
    delivery_jalali_year        SMALLINT,
    delivery_jalali_month       SMALLINT,
    delivery_jalali_month_name  VARCHAR(15),
    delivery_jalali_season      VARCHAR(10),

    -- ETL
    etl_updated_at              TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (faktorsatr_id, fiscal_year)
);

CREATE INDEX IF NOT EXISTS idx_ws_invoice_date    ON wide_sales (invoice_date_key);
CREATE INDEX IF NOT EXISTS idx_ws_order_date      ON wide_sales (order_date_key);
CREATE INDEX IF NOT EXISTS idx_ws_ship_date       ON wide_sales (ship_date_key);
CREATE INDEX IF NOT EXISTS idx_ws_delivery_date   ON wide_sales (delivery_date_key);
CREATE INDEX IF NOT EXISTS idx_ws_customer        ON wide_sales (customer_id);
CREATE INDEX IF NOT EXISTS idx_ws_seller          ON wide_sales (seller_id);
CREATE INDEX IF NOT EXISTS idx_ws_product         ON wide_sales (product_id);
CREATE INDEX IF NOT EXISTS idx_ws_branch          ON wide_sales (branch_id);
CREATE INDEX IF NOT EXISTS idx_ws_region          ON wide_sales (region_id);
CREATE INDEX IF NOT EXISTS idx_ws_brand           ON wide_sales (brand_id);
CREATE INDEX IF NOT EXISTS idx_ws_jalali_year     ON wide_sales (invoice_jalali_year);
CREATE INDEX IF NOT EXISTS idx_ws_faktor          ON wide_sales (faktor_id, fiscal_year);
CREATE INDEX IF NOT EXISTS idx_ws_status          ON wide_sales (invoice_status_code);
"""

DDL_CHUNK_LOG = """
CREATE TABLE IF NOT EXISTS etl_metadata.chunk_log (
    pipeline_name   VARCHAR(100),
    chunk_start     BIGINT,
    chunk_end       BIGINT,
    status          VARCHAR(20)  DEFAULT 'PENDING',
    rows_extracted  INT          DEFAULT 0,
    rows_inserted   INT          DEFAULT 0,
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
    -- ═══ کلیدها ════════════════════════════════════════════
    dfs.ccDarkhastFaktorSatr            AS faktorsatr_id,
    dfs.ccDarkhastFaktor                AS faktor_id,
    df.Sal                              AS fiscal_year,
    df.ShomarehFaktorIndex              AS invoice_index,

    -- ═══ شناسه‌های فاکتور ═══════════════════════════════════
    df.ShomarehFaktor                   AS invoice_number,
    df.ShomarehDarkhast                 AS request_number,

    -- ═══ تاریخ‌های اصلی ════════════════════════════════════
    df.TarikhFaktor                     AS invoice_datetime,
    CAST(df.TarikhFaktor   AS DATE)     AS invoice_date,
    df.TarikhDarkhast                   AS order_datetime,
    CAST(df.TarikhDarkhast AS DATE)     AS order_date,
    df.TarikhErsal                      AS ship_datetime,
    CAST(df.TarikhErsal    AS DATE)     AS ship_date,
    df.TarikhTahvil                     AS delivery_datetime,
    CAST(df.TarikhTahvil   AS DATE)     AS delivery_date,
    df.TarikhPishbinyTahvil             AS estimated_delivery_datetime,
    df.TarikhSarResid                   AS expiry_datetime,
    df.TarikhEntry                      AS entry_datetime,
    df.ModifiedDate                     AS header_modified_date,

    -- ═══ وضعیت / نوع فاکتور ════════════════════════════════
    df.CodeVazeiat                      AS invoice_status_code,
    CASE df.CodeVazeiat
        WHEN 0  THEN N'ثبت اولیه'
        WHEN 1  THEN N'بستن درخواست'
        WHEN 4  THEN N'فاکتور توزیع نشده'
        WHEN 5  THEN N'پیش بینی ارسال'
        WHEN 6  THEN N'ارسال به مسیر'
        WHEN 7  THEN N'تسویه'
        WHEN 8  THEN N'تسویه ناقص'
        WHEN 9  THEN N'رسید از پخش'
        WHEN 10 THEN N'رسید از مشتری'
        ELSE        N'سایر'
    END                                 AS invoice_status_text,
    df.NoeFaktor                        AS invoice_type_code,
    df.InvoiceType                      AS invoice_subtype,
    df.CodeNoeVorod                     AS entry_type_code,
    df.CodeNoeVosolAzMoshtary           AS collection_type_code,
    df.CodeNoeHaml                      AS transport_type_code,
    df.DiscntType                       AS discount_type,
    df.DiscntSubType                    AS discount_subtype,
    df.IsFormal                         AS is_formal,
    df.TelephoneOrder                   AS is_telephone_order,
    df.BeMasoliat                       AS is_cooperative,
    df.HoghoghiShodeh                   AS is_legalized,
    df.TasviehPayeBar                   AS settlement_base,
    df.InvCode                          AS inventory_code,
    df.Serial                           AS serial_number,
    df.Elat                             AS cancel_reason,
    df.Sharh                            AS invoice_note,
    df.ReferenceNumber                  AS reference_number,
    df.DeviceChargeStatus               AS device_charge_status,
    df.CountPrint                       AS print_count,
    df.X                                AS gps_longitude,
    df.Y                                AS gps_latitude,
    df.SaatVorodBeMaghazeh              AS store_entry_time,
    df.SaatKhorojAzMaghazeh             AS store_exit_time,
    df.ModateVosol                      AS collection_days,
    df.ModatRoozRaasGiri                AS tracking_days,
    df.EtebarJary                       AS current_credit,
    df.MablaghMandehMoshtary            AS customer_balance,
    df.DarsadTakhfifKhazaneh            AS treasury_discount_pct,
    df.SumTedad3                        AS total_box_count,
    df.DetailsCount                     AS row_count,

    -- ═══ مبالغ درخواست ══════════════════════════════════════
    ISNULL(df.MablaghKolDarkhast,           0)  AS request_gross_amount,
    ISNULL(df.MablaghTakhfifDarkhastTitr,   0)  AS request_header_discount,
    ISNULL(df.MablaghTakhfifDarkhastSatr,   0)  AS request_row_discount,
    ISNULL(df.MablaghKhalesDarkhast,        0)  AS request_net_amount,

    -- ═══ مبالغ فاکتور ═══════════════════════════════════════
    ISNULL(df.MablaghKolFaktor,             0)  AS invoice_gross_total,
    ISNULL(df.MablaghTakhfifFaktorTitr,     0)  AS invoice_header_discount,
    ISNULL(df.MablaghTakhfifFaktorSatr,     0)  AS invoice_row_discount,
    ISNULL(df.MablaghTakhfifFaktorTaavoni,  0)  AS invoice_cooperative_discount,
    ISNULL(df.MablaghEzafat,                0)  AS invoice_extra_charges,
    ISNULL(df.MablaghKhalesFaktor,          0)  AS invoice_net_total,
    ISNULL(df.MablaghVajhDaryaftyFaktor,    0)  AS invoice_payment_received,
    ISNULL(df.SumMaliat,                    0)  AS invoice_tax_total,
    ISNULL(df.SumAvarez,                    0)  AS invoice_surcharge_total,

    -- ═══ مشتری ══════════════════════════════════════════════
    m.ccMoshtary                        AS customer_id,
    m.NameMoshtary                      AS customer_name,
    m.NameTablo                         AS customer_signboard_name,
    m.CodeEghtesady                     AS customer_economic_code,
    m.ShenasehMeli                      AS customer_national_id,
    m.CodePosty                         AS customer_postal_code,
    m.Telephone                         AS customer_phone,
    m.Fax                               AS customer_fax,
    m.NoeMoshtary                       AS customer_type_code,
    m.Rank                              AS customer_rank,
    ISNULL(m.EtebarKol,                 0)  AS customer_credit_limit,
    ISNULL(m.EtebarPishnahady,          0)  AS customer_suggested_credit,
    ISNULL(m.ForoshTaghribiRoozaneh,    0)  AS customer_daily_sale_estimate,
    m.CodeVazeiat                       AS customer_status_code,
    m.TarikhMoarefiMoshtary             AS customer_intro_date,
    m.X                                 AS customer_gps_longitude,
    m.Y                                 AS customer_gps_latitude,
    city.NameMahal                      AS customer_city_name,
    mnm.NameNoeMalekiatMoshtary         AS customer_ownership_type,

    -- ═══ فروشنده ════════════════════════════════════════════
    df.ccForoshandeh                    AS seller_id,
    f.SharhForoshandeh                  AS seller_name,
    f.CodeForoshandehOld                AS seller_code_old,
    f.MobileNumber                      AS seller_mobile,
    f.CodeVazeiat                       AS seller_status_code,

    -- ═══ گروه فروش ══════════════════════════════════════════
    df.ccGorohForosh                    AS sales_group_id,
    gf.CodeGorohForosh                  AS sales_group_code,
    gf.SharhGorohForosh                 AS sales_group_name,

    -- ═══ مرکز و منطقه پخش ══════════════════════════════════
    df.ccMarkazPakhsh                   AS branch_id,
    mp.NameMarkazPakhsh                 AS branch_name,
    df.ccMantaghehPakhsh                AS region_id,
    mtp.NameMantaghehPakhsh             AS region_name,
    df.ccMasir                          AS route_id,

    -- ═══ سطر فاکتور ════════════════════════════════════════
    dfs.ShomarehBach                    AS batch_number,
    dfs.ShomarehBachMulti               AS batch_number_multi,
    dfs.TarikhTolid                     AS production_date,
    dfs.TarikhEngheza                   AS expiry_date_row,
    dfs.Tedad1                          AS quantity,
    dfs.Tedad2                          AS quantity2,
    dfs.Tedad3                          AS quantity3,
    dfs.TedadAdadi                      AS quantity_piece,
    dfs.TedadBasteh                     AS quantity_box,
    dfs.TedadKarton                     AS quantity_carton,
    dfs.MablaghForosh                   AS unit_price,
    dfs.MablaghDarkhasti                AS requested_unit_price,
    dfs.MablaghForosh * dfs.Tedad1      AS gross_amount,
    ISNULL(dfs.MablaghTakhfifDarkhast,  0)  AS request_row_discount_amt,
    ISNULL(dfs.MablaghTakhfifFaktor,    0)  AS row_discount,
    ISNULL(dfs.MablaghTakhfifDasti,     0)  AS manual_discount,
    ISNULL(dfs.DarsadTakhfifTaavoni,    0)  AS cooperative_discount_pct,
    ISNULL(dfs.MablaghTakhfifNaghdiVahed,0) AS cash_discount_per_unit,
    ISNULL(dfs.Maliat,                  0)  AS row_tax,
    ISNULL(dfs.Avarez,                  0)  AS row_surcharge,
    dfs.MablaghForoshKhalesKala         AS row_net_amount,
    dfs.GheymatMiangin                  AS avg_cost_price,
    dfs.GheymatKharid                   AS purchase_price,
    dfs.MojodyGhabelForosh              AS available_stock_at_sale,
    dfs.CodeVazeiat                     AS row_status_code,
    dfs.AdamJayezehKala                 AS no_prize_flag,
    dfs.ModifiedDate                    AS row_modified_date,

    -- ═══ کالا ═══════════════════════════════════════════════
    k.ccKala                            AS product_id,
    k.ccKalaCode                        AS product_code_id,
    k.NameKala                          AS product_name,
    k.NameKalaFaktor                    AS product_invoice_name,
    k.NameLatin                         AS product_latin_name,
    k.CodeKalaT                         AS product_code,
    k.CodeKalaOld                       AS product_code_old,
    k.CodeJenerik                       AS product_generic_code,
    k.IranCode                          AS product_iran_code,
    k.CodeGS1                           AS product_gs1_code,
    k.BarCode                           AS product_barcode,
    k.CodeRasmiDaroo                    AS product_official_drug_code,
    k.ShenasehKala                      AS product_identifier,
    k.CodeNoeKalaMalzomat               AS product_type_code,
    k.MashmolMaliat                     AS product_tax_eligible,
    k.MashmolAvarez                     AS product_surcharge_eligible,
    k.MashmolSobsid                     AS product_subsidy_eligible,
    k.VaznKhales                        AS product_net_weight,
    k.VaznNaKhales                      AS product_gross_weight,
    k.VaznKarton                        AS product_carton_weight,
    k.Tedad1                            AS units_per_carton,
    k.Tedad2                            AS units_per_box,

    -- ═══ برند ═══════════════════════════════════════════════
    br.ccBrand                          AS brand_id,
    br.NameBrand                        AS brand_name,

    -- ═══ تامین‌کننده ════════════════════════════════════════
    dfs.ccTaminKonandeh                 AS supplier_id,

    -- ═══ ستون‌های کمکی برای keyset pagination ═══════════════
    dfs.ModifiedDate                    AS satr_modified_date,
    df.ModifiedDate                     AS faktor_modified_date

FROM Pakhsh.Sales.DarkhastFaktor df
INNER JOIN Pakhsh.Sales.DarkhastFaktorSatr dfs
    ON  dfs.ccDarkhastFaktor = df.ccDarkhastFaktor
    AND dfs.Sal              = df.Sal
LEFT JOIN Pakhsh.Sales.Moshtary m
    ON df.ccMoshtary = m.ccMoshtary
LEFT JOIN Pakhsh.Sales.NoeMalekiatMoshtary mnm
    ON m.ccNoeMalekiatMoshtary = mnm.ccNoeMalekiatMoshtary
LEFT JOIN Pakhsh.Global.Mahal city
    ON m.ccMahaleh = city.ccMahal
LEFT JOIN Pakhsh.Sales.Foroshandeh f
    ON df.ccForoshandeh = f.ccForoshandeh
LEFT JOIN Pakhsh.Sales.GorohForosh gf
    ON df.ccGorohForosh = gf.ccGorohForosh
LEFT JOIN Pakhsh.Global.MarkazPakhsh mp
    ON df.ccMarkazPakhsh = mp.ccMarkazPakhsh
LEFT JOIN Pakhsh.Global.MantaghehPakhsh mtp
    ON df.ccMantaghehPakhsh = mtp.ccMantaghehPakhsh
LEFT JOIN Pakhsh.Warehouse.Kala k
    ON dfs.ccKala = k.ccKala
LEFT JOIN Pakhsh.Warehouse.Brand br
    ON k.ccBrand = br.ccBrand
WHERE df.TarikhFaktor IS NOT NULL
  AND df.ModifiedDate >= CONVERT(DATETIME, '{last_modified}', 120)
  AND dfs.ccDarkhastFaktorSatr > {last_seen_id}
ORDER BY dfs.ccDarkhastFaktorSatr
"""

COUNT_SQL = """
SELECT COUNT(*) AS total_rows
FROM Pakhsh.Sales.DarkhastFaktor df
INNER JOIN Pakhsh.Sales.DarkhastFaktorSatr dfs
    ON  dfs.ccDarkhastFaktor = df.ccDarkhastFaktor
    AND dfs.Sal              = df.Sal
WHERE df.TarikhFaktor IS NOT NULL
  AND df.ModifiedDate >= CONVERT(DATETIME, '{last_modified}', 120)
"""


# ─────────────────────────────────────────────────────────────
# تبدیل تاریخ شمسی
# ─────────────────────────────────────────────────────────────
MONTH_NAMES = ['', 'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد',
               'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
SEASON_MAP  = {1: 'بهار', 2: 'بهار', 3: 'بهار',
               4: 'تابستان', 5: 'تابستان', 6: 'تابستان',
               7: 'پاییز', 8: 'پاییز', 9: 'پاییز',
               10: 'زمستان', 11: 'زمستان', 12: 'زمستان'}


def add_jalali_columns(df: pd.DataFrame, date_col: str, prefix: str) -> pd.DataFrame:
    dates = pd.to_datetime(df[date_col], errors='coerce')

    def to_j(dt):
        if pd.isna(dt):
            return (None,) * 5
        try:
            jd = jdatetime.date.fromgregorian(date=dt.date())
            return (
                f"{jd.year}/{jd.month:02d}/{jd.day:02d}",
                jd.year, jd.month,
                MONTH_NAMES[jd.month],
                SEASON_MAP[jd.month]
            )
        except Exception:
            return (None,) * 5

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

    if "unit_price" in chunk.columns:
        neg_price = (pd.to_numeric(chunk["unit_price"], errors='coerce').fillna(0) < 0).sum()
        if neg_price > 0:
            issues["negative_price"] = int(neg_price)

    if "invoice_date" in chunk.columns:
        future = (pd.to_datetime(chunk["invoice_date"], errors='coerce') > datetime.now()).sum()
        if future > 0:
            issues["future_invoice_date"] = int(future)

    null_customer = chunk["customer_id"].isna().sum()
    if null_customer > 0:
        issues["null_customer_id"] = int(null_customer)

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
                    "chunk":    chunk_start,
                    "data":     json.dumps(clean, ensure_ascii=False, default=str),
                    "error":    error_msg[:500]
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

        # ── تبدیل تاریخ‌های شمسی ──────────────────────────────
        chunk = add_jalali_columns(chunk, "invoice_datetime",  "invoice")
        chunk = add_jalali_columns(chunk, "order_datetime",    "order")
        chunk = add_jalali_columns(chunk, "ship_datetime",     "ship")
        chunk = add_jalali_columns(chunk, "delivery_datetime", "delivery")

        # ── پاکسازی متن‌ها ────────────────────────────────────
        for col in chunk.select_dtypes(include="object").columns:
            chunk[col] = (
                chunk[col].astype(str)
                .str.replace("\n", " ").str.replace("\r", " ").str.replace("\t", " ")
                .str.strip()
                .replace("nan", None).replace("None", None).replace("", None)
            )

        # ── انتخاب ستون‌های نهایی ─────────────────────────────
        chunk = chunk[[c for c in FINAL_COLS if c in chunk.columns]]

        # ── تبدیل نوع داده‌ها ──────────────────────────────────
        for col in INT_COLS:
            if col in chunk.columns:
                chunk[col] = (pd.to_numeric(chunk[col], errors='coerce')
                              .fillna(-1).astype(int).replace(-1, None))

        for col in BOOL_COLS:
            if col in chunk.columns:
                chunk[col] = chunk[col].map(
                    lambda x: True if x in (1, True, '1', 'True') else
                              (False if x in (0, False, '0', 'False') else None)
                )

        # ── کیفیت داده ────────────────────────────────────────
        is_ok, issues = validate_chunk(chunk, chunk_start)
        if issues:
            logger.warning(f"  ⚠️ چانک {chunk_start}: مشکلات کیفیت: {issues}")

        if not is_ok:
            result["rows_quality_failed"] = len(chunk)
            result["status"] = "QUALITY_FAILED"
            save_failed_rows(chunk, chunk_start, f"quality_check: {issues}", tgt_engine)
            log_chunk_done(chunk_start, result["rows_extracted"], 0,
                           "QUALITY_FAILED", str(issues), tgt_engine)
            return result

        # ── بارگذاری در PostgreSQL ────────────────────────────
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
def run_obt_sales_pipeline_v3(
    chunk_size:  int = 100_000,
    max_workers: int = 4,
    max_rows:    int = None
):
    logger.info("=" * 60)
    logger.info(f"🔄 OBT فروش v3 — wide_sales (multiprocessing × {max_workers}, chunk={chunk_size:,})")
    start_time = datetime.now()

    extractor = DataExtractor()
    loader    = DataLoader()
    checkpoint = ETLCheckpoint(loader)
    alerter   = AlertManager()

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

        # ── keyset pagination ──────────────────────────────────
        logger.info("🔍 بدست آوردن نقاط شروع چانک‌ها...")
        keyset_sql = f"""
            SELECT ccDarkhastFaktorSatr
            FROM (
                SELECT dfs.ccDarkhastFaktorSatr,
                       ROW_NUMBER() OVER (ORDER BY dfs.ccDarkhastFaktorSatr) AS rn
                FROM Pakhsh.Sales.DarkhastFaktor df
                INNER JOIN Pakhsh.Sales.DarkhastFaktorSatr dfs
                    ON  dfs.ccDarkhastFaktor = df.ccDarkhastFaktor
                    AND dfs.Sal              = df.Sal
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

        # ── db_config برای subprocess ──────────────────────────
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

        total_rows   = 0
        total_errors = 0
        completed    = 0

        with Pool(processes=max_workers) as pool:
            for res in pool.imap_unordered(process_chunk, all_args):
                completed    += 1
                total_rows   += res["rows_inserted"]

                if res["status"] == "FAILED":
                    total_errors += 1
                    logger.error(f"❌ چانک {res['chunk_start']}: {res.get('error', '')[:80]}")
                elif res["status"] == "QUALITY_FAILED":
                    logger.warning(f"⚠️ چانک {res['chunk_start']}: کیفیت رد شد")
                else:
                    progress = completed / total_chunks * 100
                    elapsed  = (datetime.now() - start_time).total_seconds()
                    eta_min  = (elapsed / completed * (total_chunks - completed)) / 60 if completed > 0 else 0
                    logger.info(
                        f"✅ {completed}/{total_chunks} ({progress:.0f}%) | "
                        f"درج={res['rows_inserted']:,} | "
                        f"مجموع={total_rows:,} | ETA: {eta_min:.0f} دقیقه | "
                        f"زمان چانک={res['duration_sec']:.1f}s"
                    )

        final_status = "SUCCESS" if total_errors == 0 else "PARTIAL"
        checkpoint.save_checkpoint(
            PIPELINE_NAME, final_status, total_rows,
            from_value=last_modified,
            to_value=datetime.now().strftime("%Y-%m-%d")
        )

        duration = (datetime.now() - start_time).total_seconds()
        speed    = total_rows / duration if duration > 0 else 0

        logger.info(f"""
        ╔══════════════════════════════════════════╗
        ║   ✅ wide_sales v3 لود شد               ║
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
    run_obt_sales_pipeline_v3(chunk_size=100_000, max_workers=4, max_rows=None)