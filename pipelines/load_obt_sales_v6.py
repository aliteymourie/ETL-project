"""
OBT sales v6 - lightweight wide_sales loader.
Fast extract, per-worker temp staging, and clear ASCII logs.

Fixes vs original:
  1. DDL_CHECKPOINT added + created at startup  → fixes checkpoint ON CONFLICT error
  2. max_rows in test mode now limits actual rows fetched, not just ID range
  3. checkpoint incremental logic uses last_to_value as next lower bound
  4. process_chunk_range accepts max_rows_remaining to stop early in test mode
"""
import pandas as pd
import jdatetime
from sqlalchemy import text
from datetime import datetime
from io import StringIO
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.checkpoint import ETLCheckpoint
from core.utils.logging import setup_logger

logger = setup_logger("obt_sales_v6")

# ------------------------------------------------------------
# Configurations
# ------------------------------------------------------------
PIPELINE_NAME     = "obt_sales_v6"
TARGET_TABLE      = "wide_sales"
PK_COLS           = ("faktorsatr_id", "fiscal_year")
JALALI_1403_START = "2024-03-20 00:00:00"

FINAL_COLS = [
    "faktorsatr_id", "faktor_id", "fiscal_year", "invoice_index",
    "invoice_number", "request_number",
    "invoice_datetime", "invoice_date", "order_datetime", "order_date",
    "ship_datetime", "ship_date", "delivery_datetime", "delivery_date",
    "estimated_delivery_datetime", "expiry_datetime", "entry_datetime", "header_modified_date",
    "invoice_status_code", "invoice_status_text", "invoice_type_code", "invoice_subtype",
    "entry_type_code", "collection_type_code", "transport_type_code",
    "discount_type", "discount_subtype", "is_formal", "is_telephone_order", "is_cooperative",
    "is_legalized", "settlement_base", "inventory_code", "serial_number",
    "cancel_reason", "invoice_note", "reference_number", "device_charge_status", "print_count",
    "gps_longitude", "gps_latitude", "store_entry_time", "store_exit_time",
    "collection_days", "tracking_days", "current_credit", "customer_balance",
    "treasury_discount_pct", "total_box_count", "row_count",
    "request_gross_amount", "request_header_discount", "request_row_discount", "request_net_amount",
    "invoice_gross_total", "invoice_header_discount", "invoice_row_discount",
    "invoice_cooperative_discount", "invoice_extra_charges", "invoice_net_total",
    "invoice_payment_received", "invoice_tax_total", "invoice_surcharge_total",
    "customer_id", "customer_name", "customer_signboard_name", "customer_economic_code",
    "customer_national_id", "customer_postal_code", "customer_phone", "customer_fax",
    "customer_type_code", "customer_rank", "customer_credit_limit", "customer_suggested_credit",
    "customer_daily_sale_estimate", "customer_status_code", "customer_intro_date",
    "customer_gps_longitude", "customer_gps_latitude", "customer_city_name", "customer_ownership_type",
    "seller_id", "seller_name", "seller_code_old", "seller_mobile", "seller_status_code",
    "sales_group_id", "sales_group_code", "sales_group_name",
    "branch_id", "branch_name", "region_id", "region_name", "route_id",
    "batch_number", "batch_number_multi", "production_date", "expiry_date_row",
    "quantity", "quantity2", "quantity3", "quantity_piece", "quantity_box", "quantity_carton",
    "unit_price", "requested_unit_price", "gross_amount",
    "request_row_discount_amt", "row_discount", "manual_discount",
    "cooperative_discount_pct", "cash_discount_per_unit", "row_tax", "row_surcharge", "row_net_amount",
    "avg_cost_price", "purchase_price", "available_stock_at_sale",
    "row_status_code", "no_prize_flag", "row_modified_date",
    "product_id", "product_code_id", "product_name", "product_invoice_name", "product_latin_name",
    "product_code", "product_code_old", "product_generic_code", "product_iran_code",
    "product_gs1_code", "product_barcode", "product_official_drug_code", "product_identifier",
    "product_type_code", "product_tax_eligible", "product_surcharge_eligible", "product_subsidy_eligible",
    "product_net_weight", "product_gross_weight", "product_carton_weight", "units_per_carton", "units_per_box",
    "brand_id", "brand_name", "supplier_id",
    "invoice_date_key", "invoice_jalali", "invoice_jalali_year", "invoice_jalali_month", "invoice_jalali_month_name", "invoice_jalali_season", "invoice_jalali_key",
    "order_date_key", "order_jalali", "order_jalali_year", "order_jalali_month", "order_jalali_month_name", "order_jalali_season", "order_jalali_key",
    "ship_date_key", "ship_jalali", "ship_jalali_year", "ship_jalali_month", "ship_jalali_month_name", "ship_jalali_season", "ship_jalali_key",
    "delivery_date_key", "delivery_jalali", "delivery_jalali_year", "delivery_jalali_month", "delivery_jalali_month_name", "delivery_jalali_season", "delivery_jalali_key",
    "etl_updated_at",
]

INT_COLS = {
    # BIGINT / INT
    "faktorsatr_id", "faktor_id", "invoice_index", "invoice_number", "request_number",
    "invoice_subtype", "discount_type", "discount_subtype", "serial_number",
    "device_charge_status", "total_box_count", "row_count",
    "customer_id", "customer_type_code", "sales_group_id", "branch_id", "region_id", "route_id",
    "seller_id", "product_id", "product_code_id", "product_generic_code",
    "units_per_carton", "units_per_box", "brand_id", "supplier_id",
    "invoice_date_key", "invoice_jalali_key",
    "order_date_key",   "order_jalali_key",
    "ship_date_key",    "ship_jalali_key",
    "delivery_date_key","delivery_jalali_key",
    # SMALLINT — pandas would read nullable int columns as float64 without explicit cast
    "fiscal_year",
    "invoice_status_code", "invoice_type_code", "entry_type_code", "collection_type_code",
    "transport_type_code", "inventory_code", "print_count", "collection_days", "tracking_days",
    "is_cooperative", "is_legalized", "settlement_base",          # <-- these were missing
    "customer_status_code", "seller_status_code",
    "row_status_code", "product_type_code",
    "invoice_jalali_year", "invoice_jalali_month",
    "order_jalali_year",   "order_jalali_month",
    "ship_jalali_year",    "ship_jalali_month",
    "delivery_jalali_year","delivery_jalali_month",
}

BOOL_COLS = {
    "is_formal", "is_telephone_order", "no_prize_flag",
    "product_tax_eligible", "product_surcharge_eligible", "product_subsidy_eligible",
}

# ------------------------------------------------------------
# DDLs
# ------------------------------------------------------------
DDL_WIDE_SALES = """
CREATE TABLE IF NOT EXISTS wide_sales (
    faktorsatr_id               BIGINT          NOT NULL,
    faktor_id                   BIGINT          NOT NULL,
    fiscal_year                 SMALLINT        NOT NULL,
    invoice_index               BIGINT,
    invoice_number              INT,
    request_number              INT,
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
    request_gross_amount        NUMERIC(18,2),
    request_header_discount     NUMERIC(18,2),
    request_row_discount        NUMERIC(18,2),
    request_net_amount          NUMERIC(18,2),
    invoice_gross_total         NUMERIC(18,2),
    invoice_header_discount     NUMERIC(18,2),
    invoice_row_discount        NUMERIC(18,2),
    invoice_cooperative_discount NUMERIC(18,2),
    invoice_extra_charges       NUMERIC(18,2),
    invoice_net_total           NUMERIC(18,2),
    invoice_payment_received    NUMERIC(18,2),
    invoice_tax_total           NUMERIC(18,2),
    invoice_surcharge_total     NUMERIC(18,2),
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
    seller_id                   INT,
    seller_name                 VARCHAR(200),
    seller_code_old             VARCHAR(50),
    seller_mobile               VARCHAR(30),
    seller_status_code          SMALLINT,
    sales_group_id              INT,
    sales_group_code            VARCHAR(50),
    sales_group_name            VARCHAR(200),
    branch_id                   INT,
    branch_name                 VARCHAR(200),
    region_id                   INT,
    region_name                 VARCHAR(200),
    route_id                    INT,
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
    brand_id                    INT,
    brand_name                  VARCHAR(200),
    supplier_id                 INT,
    invoice_date_key            INT,
    invoice_jalali              VARCHAR(10),
    invoice_jalali_year         SMALLINT,
    invoice_jalali_month        SMALLINT,
    invoice_jalali_month_name   VARCHAR(15),
    invoice_jalali_season       VARCHAR(10),
    invoice_jalali_key          INT,
    order_date_key              INT,
    order_jalali                VARCHAR(10),
    order_jalali_year           SMALLINT,
    order_jalali_month          SMALLINT,
    order_jalali_month_name     VARCHAR(15),
    order_jalali_season         VARCHAR(10),
    order_jalali_key            INT,
    ship_date_key               INT,
    ship_jalali                 VARCHAR(10),
    ship_jalali_year            SMALLINT,
    ship_jalali_month           SMALLINT,
    ship_jalali_month_name      VARCHAR(15),
    ship_jalali_season          VARCHAR(10),
    ship_jalali_key             INT,
    delivery_date_key           INT,
    delivery_jalali             VARCHAR(10),
    delivery_jalali_year        SMALLINT,
    delivery_jalali_month       SMALLINT,
    delivery_jalali_month_name  VARCHAR(15),
    delivery_jalali_season      VARCHAR(10),
    delivery_jalali_key         INT,
    etl_updated_at              TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (faktorsatr_id, fiscal_year)
);
CREATE INDEX IF NOT EXISTS idx_ws_invoice_date  ON wide_sales (invoice_date_key);
CREATE INDEX IF NOT EXISTS idx_ws_order_date    ON wide_sales (order_date_key);
CREATE INDEX IF NOT EXISTS idx_ws_ship_date     ON wide_sales (ship_date_key);
CREATE INDEX IF NOT EXISTS idx_ws_delivery_date ON wide_sales (delivery_date_key);
CREATE INDEX IF NOT EXISTS idx_ws_customer      ON wide_sales (customer_id);
CREATE INDEX IF NOT EXISTS idx_ws_seller        ON wide_sales (seller_id);
CREATE INDEX IF NOT EXISTS idx_ws_product       ON wide_sales (product_id);
CREATE INDEX IF NOT EXISTS idx_ws_branch        ON wide_sales (branch_id);
CREATE INDEX IF NOT EXISTS idx_ws_region        ON wide_sales (region_id);
CREATE INDEX IF NOT EXISTS idx_ws_brand         ON wide_sales (brand_id);
CREATE INDEX IF NOT EXISTS idx_ws_jalali_year   ON wide_sales (invoice_jalali_year);
CREATE INDEX IF NOT EXISTS idx_ws_jalali_key    ON wide_sales (invoice_jalali_key);
CREATE INDEX IF NOT EXISTS idx_ws_faktor        ON wide_sales (faktor_id, fiscal_year);
CREATE INDEX IF NOT EXISTS idx_ws_status        ON wide_sales (invoice_status_code);
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

# FIX 1: DDL for checkpoint table was missing — caused the ON CONFLICT error.
# The DO block handles the case where the table already exists without a PK
# (e.g. created by an earlier broken run) and adds the constraint safely.
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

# ------------------------------------------------------------
# SQLs
# ------------------------------------------------------------
MIN_MAX_SQL = """
SELECT
    MIN(dfs.ccDarkhastFaktorSatr) AS min_id,
    MAX(dfs.ccDarkhastFaktorSatr) AS max_id,
    COUNT(*)                      AS total_rows
FROM Pakhsh.Sales.DarkhastFaktorSatr dfs
INNER JOIN Pakhsh.Sales.DarkhastFaktor df
    ON  df.ccDarkhastFaktor = dfs.ccDarkhastFaktor
    AND df.Sal              = dfs.Sal
WHERE df.TarikhFaktor IS NOT NULL
  AND df.ModifiedDate >= CONVERT(DATETIME, '{last_modified}', 120)
"""

EXTRACT_SQL = """
SELECT
    -- ═══ کلیدها ══════════════════════════════════════════════════════
    dfs.ccDarkhastFaktorSatr                AS faktorsatr_id,
    dfs.ccDarkhastFaktor                    AS faktor_id,
    df.Sal                                  AS fiscal_year,
    df.ShomarehFaktorIndex                  AS invoice_index,

    -- ═══ شناسه‌های فاکتور ══════════════════════════════════════════════
    df.ShomarehFaktor                       AS invoice_number,
    df.ShomarehDarkhast                     AS request_number,

    -- ═══ تاریخ‌های اصلی ════════════════════════════════════════════════
    df.TarikhFaktor                         AS invoice_datetime,
    CAST(df.TarikhFaktor   AS DATE)         AS invoice_date,
    df.TarikhDarkhast                       AS order_datetime,
    CAST(df.TarikhDarkhast AS DATE)         AS order_date,
    df.TarikhErsal                          AS ship_datetime,
    CAST(df.TarikhErsal    AS DATE)         AS ship_date,
    df.TarikhTahvil                         AS delivery_datetime,
    CAST(df.TarikhTahvil   AS DATE)         AS delivery_date,
    df.TarikhPishbinyTahvil                 AS estimated_delivery_datetime,
    df.TarikhSarResid                       AS expiry_datetime,
    df.TarikhEntry                          AS entry_datetime,
    df.ModifiedDate                         AS header_modified_date,

    -- ═══ وضعیت / نوع فاکتور ═══════════════════════════════════════════════
    df.CodeVazeiat                          AS invoice_status_code,
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
    END                                     AS invoice_status_text,
    df.NoeFaktor                            AS invoice_type_code,
    df.InvoiceType                          AS invoice_subtype,
    df.CodeNoeVorod                         AS entry_type_code,
    df.CodeNoeVosolAzMoshtary               AS collection_type_code,
    df.CodeNoeHaml                          AS transport_type_code,
    df.DiscntType                           AS discount_type,
    df.DiscntSubType                        AS discount_subtype,
    df.IsFormal                             AS is_formal,
    df.TelephoneOrder                       AS is_telephone_order,
    df.BeMasoliat                           AS is_cooperative,
    df.HoghoghiShodeh                       AS is_legalized,
    df.TasviehPayeBar                       AS settlement_base,
    df.InvCode                              AS inventory_code,
    df.Serial                               AS serial_number,
    df.Elat                                 AS cancel_reason,
    df.Sharh                                AS invoice_note,
    df.ReferenceNumber                      AS reference_number,
    df.DeviceChargeStatus                   AS device_charge_status,
    df.CountPrint                           AS print_count,
    df.X                                    AS gps_longitude,
    df.Y                                    AS gps_latitude,
    df.SaatVorodBeMaghazeh                  AS store_entry_time,
    df.SaatKhorojAzMaghazeh                 AS store_exit_time,
    df.ModateVosol                          AS collection_days,
    df.ModatRoozRaasGiri                    AS tracking_days,
    df.EtebarJary                           AS current_credit,
    df.MablaghMandehMoshtary                AS customer_balance,
    df.DarsadTakhfifKhazaneh                AS treasury_discount_pct,
    df.SumTedad3                            AS total_box_count,
    df.DetailsCount                         AS row_count,

    -- ═══ مبالغ درخواست ══════════════════════════════════════════════════
    ISNULL(df.MablaghKolDarkhast,           0)  AS request_gross_amount,
    ISNULL(df.MablaghTakhfifDarkhastTitr,   0)  AS request_header_discount,
    ISNULL(df.MablaghTakhfifDarkhastSatr,   0)  AS request_row_discount,
    ISNULL(df.MablaghKhalesDarkhast,        0)  AS request_net_amount,

    -- ═══ مبالغ فاکتور ═══════════════════════════════════════════════════
    ISNULL(df.MablaghKolFaktor,             0)  AS invoice_gross_total,
    ISNULL(df.MablaghTakhfifFaktorTitr,     0)  AS invoice_header_discount,
    ISNULL(df.MablaghTakhfifFaktorSatr,     0)  AS invoice_row_discount,
    ISNULL(df.MablaghTakhfifFaktorTaavoni,  0)  AS invoice_cooperative_discount,
    ISNULL(df.MablaghEzafat,                0)  AS invoice_extra_charges,
    ISNULL(df.MablaghKhalesFaktor,          0)  AS invoice_net_total,
    ISNULL(df.MablaghVajhDaryaftyFaktor,    0)  AS invoice_payment_received,
    ISNULL(df.SumMaliat,                    0)  AS invoice_tax_total,
    ISNULL(df.SumAvarez,                    0)  AS invoice_surcharge_total,

    -- ═══ مشتری ════════════════════════════════════════════════════════════
    m.ccMoshtary                            AS customer_id,
    m.NameMoshtary                          AS customer_name,
    m.CodeVazeiat                           AS customer_status_code,
    m.TarikhMoarefiMoshtary                 AS customer_intro_date,
    city.NameMahal                          AS customer_city_name,
    mnm.NameNoeMalekiatMoshtary             AS customer_ownership_type,

    -- ═══ فروشنده ════════════════════════════════════════════════════════
    df.ccForoshandeh                        AS seller_id,
    f.SharhForoshandeh                      AS seller_name,
    f.CodeForoshandehOld                    AS seller_code_old,
    f.MobileNumber                          AS seller_mobile,
    f.CodeVazeiat                           AS seller_status_code,

    -- ═══ گروه فروش ══════════════════════════════════════════════════════════
    df.ccGorohForosh                        AS sales_group_id,
    gf.CodeGorohForosh                      AS sales_group_code,
    gf.SharhGorohForosh                     AS sales_group_name,

    -- ═══ مرکز و منطقه پخش ═══════════════════════════════════════════════════════════════
    df.ccMarkazPakhsh                       AS branch_id,
    mp.NameMarkazPakhsh                     AS branch_name,
    df.ccMantaghehPakhsh                    AS region_id,
    mtp.NameMantaghehPakhsh                 AS region_name,
    df.ccMasir                              AS route_id,

    -- ═══ سطر فاکتور ══════════════════════════════════════════════════════════════
    dfs.Tedad1                              AS quantity,
    dfs.Tedad2                              AS quantity2,
    dfs.Tedad3                              AS quantity3,
    dfs.MablaghForosh                       AS unit_price,
    dfs.MablaghDarkhasti                    AS requested_unit_price,
    dfs.MablaghForosh * dfs.Tedad1          AS gross_amount,
    ISNULL(dfs.MablaghTakhfifDarkhast,  0)  AS request_row_discount_amt,
    ISNULL(dfs.MablaghTakhfifFaktor,    0)  AS row_discount,
    ISNULL(dfs.MablaghTakhfifDasti,     0)  AS manual_discount,
    ISNULL(dfs.DarsadTakhfifTaavoni,    0)  AS cooperative_discount_pct,
    ISNULL(dfs.MablaghTakhfifNaghdiVahed,0) AS cash_discount_per_unit,
    ISNULL(dfs.Maliat,                  0)  AS row_tax,
    ISNULL(dfs.Avarez,                  0)  AS row_surcharge,
    dfs.MablaghForoshKhalesKala             AS row_net_amount,
    dfs.GheymatMiangin                      AS avg_cost_price,
    dfs.GheymatKharid                       AS purchase_price,
    dfs.MojodyGhabelForosh                  AS available_stock_at_sale,
    dfs.CodeVazeiat                         AS row_status_code,
    dfs.AdamJayezehKala                     AS no_prize_flag,
    dfs.ModifiedDate                        AS row_modified_date,

    -- ═══ کالا ═══════════════════════════════════════════════════════════════════
    k.ccKala                                AS product_id,
    k.ccKalaCode                            AS product_code_id,
    k.NameKala                              AS product_name,
    k.NameKalaFaktor                        AS product_invoice_name,
    k.NameLatin                             AS product_latin_name,
    k.CodeKalaT                             AS product_code,
    k.CodeKalaOld                           AS product_code_old,
    k.CodeJenerik                           AS product_generic_code,
    k.IranCode                              AS product_iran_code,
    k.CodeGS1                               AS product_gs1_code,
    k.BarCode                               AS product_barcode,
    k.CodeRasmiDaroo                        AS product_official_drug_code,
    k.ShenasehKala                          AS product_identifier,
    k.Tedad1                                AS units_per_carton,
    k.Tedad2                                AS units_per_box,

    -- ═══ برند ═══════════════════════════════════════════════════════════════════
    br.ccBrand                              AS brand_id,
    br.NameBrand                            AS brand_name,

    -- ═══ تامین‌کننده ═══════════════════════════════════════════════════════════════════
    dfs.ccTaminKonandeh                     AS supplier_id

FROM Pakhsh.Sales.DarkhastFaktor df
INNER JOIN Pakhsh.Sales.DarkhastFaktorSatr dfs
    ON  dfs.ccDarkhastFaktor = df.ccDarkhastFaktor
    AND dfs.Sal              = df.Sal
LEFT JOIN Pakhsh.Sales.Moshtary m
    ON  df.ccMoshtary = m.ccMoshtary
LEFT JOIN Pakhsh.Sales.NoeMalekiatMoshtary mnm
    ON  m.ccNoeMalekiatMoshtary = mnm.ccNoeMalekiatMoshtary
LEFT JOIN Pakhsh.Global.Mahal city
    ON  m.ccMahaleh = city.ccMahal
LEFT JOIN Pakhsh.Sales.Foroshandeh f
    ON  df.ccForoshandeh = f.ccForoshandeh
LEFT JOIN Pakhsh.Sales.GorohForosh gf
    ON  df.ccGorohForosh = gf.ccGorohForosh
LEFT JOIN Pakhsh.Global.MarkazPakhsh mp
    ON  df.ccMarkazPakhsh = mp.ccMarkazPakhsh
LEFT JOIN Pakhsh.Global.MantaghehPakhsh mtp
    ON  df.ccMantaghehPakhsh = mtp.ccMantaghehPakhsh
LEFT JOIN Pakhsh.Warehouse.Kala k
    ON  dfs.ccKala = k.ccKala
LEFT JOIN Pakhsh.Warehouse.Brand br
    ON  k.ccBrand = br.ccBrand

WHERE df.TarikhFaktor IS NOT NULL
  AND df.ModifiedDate >= CONVERT(DATETIME, '{last_modified}', 120)
  AND dfs.ccDarkhastFaktorSatr BETWEEN {start_id} AND {end_id}

ORDER BY dfs.ccDarkhastFaktorSatr
"""

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def build_upsert_sql(columns, staging_table="tmp_staging", update_columns=None):
    update_columns = update_columns or columns
    non_pk = [c for c in update_columns if c not in PK_COLS and c != "etl_updated_at"]
    set_parts = [f"{c} = EXCLUDED.{c}" for c in non_pk]
    set_parts.append("etl_updated_at = NOW()")
    cols = ", ".join(columns)
    set_clause = ",\n            ".join(set_parts)
    return f"""
        INSERT INTO {TARGET_TABLE} ({cols})
        SELECT {cols} FROM {staging_table}
        ON CONFLICT ({", ".join(PK_COLS)}) DO UPDATE SET
            {set_clause}
    """

MONTH_NAMES = [
    "",
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند",
]
SEASON_MAP = {
    1: "بهار",    2: "بهار",    3: "بهار",
    4: "تابستان", 5: "تابستان", 6: "تابستان",
    7: "پاییز",    8: "پاییز",    9: "پاییز",
    10: "زمستان", 11: "زمستان", 12: "زمستان",
}

def execute_ddl(loader, ddl_sql, label):
    with loader.tgt_engine.begin() as conn:
        conn.execute(text(ddl_sql))
    logger.info(f"DDL ok: {label}")

def add_jalali_columns(df, date_col, prefix):
    dates = pd.to_datetime(df[date_col], errors='coerce')
    def to_j(dt):
        if pd.isna(dt): return (None,) * 6
        try:
            jd = jdatetime.date.fromgregorian(date=dt.date())
            return (f"{jd.year}/{jd.month:02d}/{jd.day:02d}", jd.year, jd.month,
                    MONTH_NAMES[jd.month], SEASON_MAP[jd.month], int(f"{jd.year}{jd.month:02d}{jd.day:02d}"))
        except Exception:
            return (None,) * 6

    res = dates.map(to_j)
    df[f"{prefix}_jalali"]            = res.map(lambda x: x[0])
    df[f"{prefix}_jalali_year"]       = res.map(lambda x: x[1])
    df[f"{prefix}_jalali_month"]      = res.map(lambda x: x[2])
    df[f"{prefix}_jalali_month_name"] = res.map(lambda x: x[3])
    df[f"{prefix}_jalali_season"]     = res.map(lambda x: x[4])
    df[f"{prefix}_jalali_key"]        = res.map(lambda x: x[5])
    df[f"{prefix}_date_key"] = pd.to_numeric(
        dates.dt.strftime('%Y%m%d').where(dates.notna(), None), errors='coerce'
    ).astype('Int64')
    return df


def process_chunk_range(start_id, end_id, last_modified, max_rows_remaining=None):
    """
    Extract one ID-range chunk, transform, and upsert into wide_sales.

    Args:
        start_id / end_id       : ID bounds for this chunk (inclusive).
        last_modified           : ModifiedDate lower bound (str, 'YYYY-MM-DD HH:MM:SS').
        max_rows_remaining      : FIX 2 — if set, truncate the extracted DataFrame so
                                  that the pipeline stops after exactly max_rows total.
                                  This makes --max-rows actually limit real rows, not
                                  just the ID scan window.
    Returns:
        (rows_from_db, inserted, errors)
    """
    extractor = DataExtractor()
    loader    = DataLoader()

    chunk_sql = EXTRACT_SQL.format(last_modified=last_modified, start_id=start_id, end_id=end_id)
    chunk = pd.read_sql(chunk_sql, extractor.src_engine)

    if chunk.empty:
        return 0, 0, 0

    rows_from_db = len(chunk)

    # FIX 2: honour the real row cap in test mode
    if max_rows_remaining is not None and len(chunk) > max_rows_remaining:
        chunk = chunk.iloc[:max_rows_remaining].copy()

    chunk = add_jalali_columns(chunk, "invoice_datetime", "invoice")
    chunk = add_jalali_columns(chunk, "order_datetime",   "order")
    chunk = add_jalali_columns(chunk, "ship_datetime",    "ship")
    chunk = add_jalali_columns(chunk, "delivery_datetime","delivery")

    str_cols = chunk.select_dtypes(include="object").columns
    for col in str_cols:
        chunk[col] = (
            chunk[col].astype(str)
            .str.replace("\n", " ").str.replace("\r", " ").str.replace("\t", " ")
            .str.strip()
        )
        chunk[col] = chunk[col].replace({"nan": None, "None": None, "": None})

    for col in INT_COLS:
        if col in chunk.columns:
            chunk[col] = pd.to_numeric(chunk[col], errors='coerce').astype('Int64')
    for col in BOOL_COLS:
        if col in chunk.columns:
            chunk[col] = pd.to_numeric(chunk[col], errors='coerce').astype('Int64')

    cols_to_load = [c for c in FINAL_COLS if c != "etl_updated_at"]
    update_cols  = [c for c in cols_to_load if c in chunk.columns]
    chunk        = chunk.reindex(columns=cols_to_load).copy()

    if chunk.empty:
        return rows_from_db, 0, 0

    inserted = 0
    errors   = 0
    try:
        output = StringIO()
        chunk.to_csv(output, sep='\t', header=False, index=False, na_rep='\\N', quoting=csv.QUOTE_MINIMAL)
        output.seek(0)

        with loader.tgt_engine.begin() as conn:
            with conn.connection.cursor() as cursor:
                cursor.execute(
                    "CREATE TEMP TABLE tmp_staging "
                    "(LIKE wide_sales EXCLUDING INDEXES EXCLUDING CONSTRAINTS) "
                    "ON COMMIT DROP;"
                )
                cursor.copy_from(output, 'tmp_staging', columns=cols_to_load, null='\\N')
                cursor.execute(build_upsert_sql(cols_to_load, "tmp_staging", update_cols))
        inserted = len(chunk)
    except Exception as e:
        errors = len(chunk)
        logger.error(f"chunk_failed range={start_id}-{end_id} rows={len(chunk):,} error={str(e)[:500]}")

    return rows_from_db, inserted, errors


def run_obt_sales_pipeline(chunk_size: int = 500_000, max_workers: int = 2, max_rows: int = None):
    logger.info("=" * 60)
    logger.info(f"Starting OBT sales v6 target={TARGET_TABLE} workers={max_workers} chunk_size={chunk_size:,}")
    start_time = datetime.now()

    extractor  = DataExtractor()
    loader     = DataLoader()
    checkpoint = ETLCheckpoint(loader)

    try:
        execute_ddl(loader, DDL_WIDE_SALES, TARGET_TABLE)
        logger.info("Target table is ready.")

        # FIX 1: always create the etl_metadata schema + both support tables before
        # calling checkpoint.get_last_success / save_checkpoint so the ON CONFLICT
        # clause finds the required PRIMARY KEY constraint on pipeline_name.
        try:
            execute_ddl(loader, "CREATE SCHEMA IF NOT EXISTS etl_metadata;", "etl_metadata schema")
            execute_ddl(loader, DDL_CHECKPOINT, "etl_metadata.etl_checkpoint")
            execute_ddl(loader, DDL_CHUNK_LOG,  "etl_metadata.chunk_log")
        except Exception as e:
            logger.warning(f"metadata table setup skipped: {str(e)[:200]}")

        # FIX 3: use last_to_value (the run-end timestamp) as the next lower bound
        # so incremental runs don't re-scan already-loaded data.
        last_run = checkpoint.get_last_success(PIPELINE_NAME)
        if last_run and last_run.get("last_to_value"):
            last_modified = str(last_run["last_to_value"])[:19].replace("T", " ")
            logger.info(f"Checkpoint found. Resuming from: {last_modified}")
        else:
            last_modified = JALALI_1403_START
            logger.info(f"No checkpoint found. Starting from {JALALI_1403_START}")

        logger.info(f"ModifiedDate lower bound: {last_modified}")
        min_max_df = pd.read_sql(MIN_MAX_SQL.format(last_modified=last_modified), extractor.src_engine)

        min_id    = int(min_max_df['min_id'].iloc[0])    if pd.notna(min_max_df['min_id'].iloc[0])    else 0
        max_id    = int(min_max_df['max_id'].iloc[0])    if pd.notna(min_max_df['max_id'].iloc[0])    else 0
        total_est = int(min_max_df['total_rows'].iloc[0]) if pd.notna(min_max_df['total_rows'].iloc[0]) else 0

        if min_id == 0 or max_id == 0:
            logger.info("No rows found for this run.")
            return 0

        logger.info(f"Source estimate rows={total_est:,} id_range={min_id:,}-{max_id:,}")

        # FIX 2: in test mode keep the full ID range intact so the actual data
        # is scanned correctly; instead pass max_rows_remaining per-chunk so
        # workers stop as soon as the real row cap is reached.
        test_mode   = max_rows is not None and max_rows < total_est
        rows_cap    = max_rows if test_mode else None
        if test_mode:
            logger.info(f"Test limit active: max_rows={max_rows:,} (row-level cap, not ID range)")

        ranges       = [(s, min(s + chunk_size - 1, max_id)) for s in range(min_id, max_id + 1, chunk_size)]
        total_chunks = len(ranges)
        logger.info(f"Chunks planned: {total_chunks:,}")

        total_rows   = 0
        total_errors = 0
        completed    = 0

        # FIX 2 (revised): submit chunks lazily — max_workers at a time — so that
        # once the row cap is hit we stop submitting new work instead of waiting for
        # 100+ already-queued futures to drain.
        ranges_iter = iter(ranges)

        def submit_next(executor, futures_dict):
            """Submit the next range if one exists and the cap hasn't been hit."""
            if rows_cap is not None and total_rows >= rows_cap:
                return
            try:
                start, end = next(ranges_iter)
                remaining  = (rows_cap - total_rows) if rows_cap is not None else None
                f = executor.submit(process_chunk_range, start, end, last_modified, remaining)
                futures_dict[f] = (start, end)
            except StopIteration:
                pass

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            active = {}
            # Seed the pool with up to max_workers initial chunks
            for _ in range(max_workers):
                submit_next(executor, active)

            while active:
                # Wait for the next completed future
                done_future = next(as_completed(active))
                start, end  = active.pop(done_future)
                completed  += 1
                try:
                    rows_from_db, inserted, errors = done_future.result()
                    total_rows   += inserted
                    total_errors += errors
                    progress      = completed / total_chunks * 100
                    elapsed       = (datetime.now() - start_time).total_seconds()
                    eta_min       = (elapsed / completed * (total_chunks - completed)) / 60 if completed > 0 else 0
                    logger.info(
                        f"chunk_done {completed}/{total_chunks} ({progress:.0f}%) "
                        f"range={start}-{end} extracted={rows_from_db:,} loaded={inserted:,} "
                        f"errors={errors:,} total_loaded={total_rows:,} eta_min={eta_min:.0f}"
                    )
                    if rows_cap is not None and total_rows >= rows_cap:
                        logger.info(f"Test row cap reached ({total_rows:,}/{rows_cap:,}). No more chunks will be submitted.")
                    else:
                        # Submit the next chunk only if we still need more rows
                        submit_next(executor, active)
                except Exception as e:
                    total_errors += 1
                    logger.error(f"chunk_future_failed range={start}-{end} error={str(e)[:300]}")
                    submit_next(executor, active)

        if total_errors:
            message = f"Load finished with errors: total_loaded={total_rows:,}, failed_rows_or_chunks={total_errors:,}"
            checkpoint.save_checkpoint(PIPELINE_NAME, "FAILED", total_rows, error_message=message[:500])
            logger.error(message)
            raise RuntimeError(message)

        # FIX 3: save the run-start time as last_to_value so the next run picks
        # up exactly from here (avoids re-processing rows modified during this run).
        run_end_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        checkpoint.save_checkpoint(
            PIPELINE_NAME, "SUCCESS", total_rows,
            from_value=last_modified,
            to_value=run_end_ts if total_rows > 0 else last_modified,
        )

        minutes = (datetime.now() - start_time).total_seconds() / 60
        logger.info(f"Load complete: total_loaded={total_rows:,}, errors={total_errors:,}, minutes={minutes:.1f}")
        return total_rows

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
        checkpoint.save_checkpoint(PIPELINE_NAME, "FAILED", error_message=str(e)[:500])
        raise


if __name__ == "__main__":
    run_obt_sales_pipeline(chunk_size=50_000, max_workers=2, max_rows=100_000)