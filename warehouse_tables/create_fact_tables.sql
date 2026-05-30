-- ============================================
-- DDL نهایی ۶ جدول Fact - انبار داده
-- ============================================

-- 1. FactSales (فروش) - کامل شده ✅
CREATE TABLE IF NOT EXISTS fact_sales (
    date_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,
    employee_key INTEGER NOT NULL,
    dist_center_key INTEGER NOT NULL,
    cc_darkhast_faktor BIGINT NOT NULL,
    sal_mali INTEGER NOT NULL,
    tedad_faktor NUMERIC(18,2),
    tedad_faktor_kartony NUMERIC(18,2),
    fi_forosh NUMERIC(18,2),
    mablagh_khales_satr NUMERIC(18,2),
    mablagh_takhfif NUMERIC(18,2),
    etl_created_at TIMESTAMP DEFAULT NOW(),
    etl_updated_at TIMESTAMP DEFAULT NOW(),
    etl_batch_id VARCHAR(20),
    PRIMARY KEY (cc_darkhast_faktor, sal_mali, product_key)
);

-- 2. FactInventory (موجودی)
CREATE TABLE IF NOT EXISTS fact_inventory (
    date_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    dist_center_key INTEGER NOT NULL,
    cc_anbar INTEGER NOT NULL,                   -- کد انبار
    mojody_anbar_tedady NUMERIC(18,2) DEFAULT 0, -- موجودی عددی
    mojody_anbar_kartony NUMERIC(18,2) DEFAULT 0,-- موجودی کارتنی
    mojody_anbar_rialy NUMERIC(18,2) DEFAULT 0,  -- موجودی ریالی
    faktor_tozi_nashodeh_rialy NUMERIC(18,2) DEFAULT 0,
    tedad_aghlam_nazdik NUMERIC(18,2) DEFAULT 0,  -- اقلام نزدیک انقضا
    etl_created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (date_key, product_key, dist_center_key, cc_anbar)
);

-- 3. FactPurchase (خرید)
CREATE TABLE IF NOT EXISTS fact_purchase (
    date_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    dist_center_key INTEGER NOT NULL,
    cc_tamin_konandeh INTEGER NOT NULL,          -- تأمین‌کننده
    cc_faktor_kharid INTEGER NOT NULL,            -- فاکتور خرید
    cc_faktor_kharid_satr INTEGER NOT NULL,       -- سطر فاکتور خرید
    az_mablagh NUMERIC(18,2) DEFAULT 0,           -- از مبلغ (بازه قیمت)
    ta_mablagh NUMERIC(18,2) DEFAULT 0,           -- تا مبلغ
    tedad_kharid NUMERIC(18,2) DEFAULT 0,         -- تعداد خرید
    fi_kharid NUMERIC(18,2) DEFAULT 0,            -- فی خرید
    etl_created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (cc_faktor_kharid, cc_faktor_kharid_satr)
);

-- 4. FactTreasury (خزانه‌داری)
CREATE TABLE IF NOT EXISTS fact_treasury (
    date_key INTEGER NOT NULL,
    customer_key INTEGER DEFAULT 1,
    employee_key INTEGER DEFAULT 1,
    dist_center_key INTEGER DEFAULT 1,
    cc_sanad_dariaft INTEGER NOT NULL,            -- کد سند دریافت
    mablagh_sanad NUMERIC(18,2) DEFAULT 0,        -- مبلغ سند
    chek_bargashty NUMERIC(18,2) DEFAULT 0,       -- چک برگشتی
    takhfif_naghdi_20 NUMERIC(18,2) DEFAULT 0,    -- تخفیف نقدی ۲۰٪
    naghs_chek NUMERIC(18,2) DEFAULT 0,           -- ناقص چک
    etl_created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (cc_sanad_dariaft)
);

-- 5. FactLedger (دفتر کل)
CREATE TABLE IF NOT EXISTS fact_ledger (
    date_key INTEGER NOT NULL,
    dist_center_key INTEGER DEFAULT 1,
    employee_key INTEGER DEFAULT 1,
    cc_tafsily INTEGER NOT NULL,                  -- کد تفصیلی
    cc_moien INTEGER NOT NULL,                    -- کد معین
    bed NUMERIC(18,2) DEFAULT 0,                  -- بدهکار
    bes NUMERIC(18,2) DEFAULT 0,                  -- بستانکار
    sum_bed NUMERIC(18,2) DEFAULT 0,              -- جمع بدهکار
    sum_bes NUMERIC(18,2) DEFAULT 0,              -- جمع بستانکار
    etl_created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (date_key, cc_tafsily, cc_moien)
);

-- 6. FactAsset (اموال)
CREATE TABLE IF NOT EXISTS fact_asset (
    date_key INTEGER NOT NULL,
    dist_center_key INTEGER DEFAULT 1,
    employee_key INTEGER DEFAULT 1,
    cc_amval INTEGER NOT NULL,                    -- کد اموال (DD)
    gheymat_tamam_shodeh NUMERIC(18,2) DEFAULT 0, -- قیمت تمام شده
    arzesh_daftary NUMERIC(18,2) DEFAULT 0,       -- ارزش دفتری
    estehlak_anbashteh NUMERIC(18,2) DEFAULT 0,   -- استهلاک انباشته
    depreciation_rate NUMERIC(5,2) DEFAULT 0,     -- نرخ استهلاک
    etl_created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (date_key, cc_amval)
);

-- ============================================
-- ایندکس‌های عملکردی
-- ============================================
CREATE INDEX IF NOT EXISTS idx_fact_sales_date ON fact_sales(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_inventory_date ON fact_inventory(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_purchase_date ON fact_purchase(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_treasury_date ON fact_treasury(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_ledger_date ON fact_ledger(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_asset_date ON fact_asset(date_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_product ON fact_sales(product_key);
CREATE INDEX IF NOT EXISTS idx_fact_inventory_product ON fact_inventory(product_key);
CREATE INDEX IF NOT EXISTS idx_fact_purchase_product ON fact_purchase(product_key);

CREATE INDEX IF NOT EXISTS idx_fact_treasury_customer ON fact_treasury(customer_key);
CREATE INDEX IF NOT EXISTS idx_fact_ledger_center ON fact_ledger(dist_center_key);
CREATE INDEX IF NOT EXISTS idx_fact_asset_center ON fact_asset(dist_center_key);