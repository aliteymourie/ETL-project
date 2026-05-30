-- ============================================
-- ایجاد جداول ابعاد منطبق با ساختار واقعی منبع
-- ============================================

-- 1. بعد تاریخ (DimDate)
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,        -- فرمت: 14050101
    Tarikh DATE NOT NULL,                -- تاریخ میلادی
    Sal INTEGER NOT NULL,                -- سال شمسی (مثلاً 1405)
    Mah INTEGER NOT NULL,                -- ماه شمسی (1-12)
    NameMah VARCHAR(20) NOT NULL,        -- نام ماه (فروردین، اردیبهشت، ...)
    Fasl VARCHAR(15) NOT NULL,           -- فصل (بهار، تابستان، ...)
    IsTatil BOOLEAN DEFAULT FALSE,       -- تعطیل رسمی
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_dim_date_sal ON dim_date(Sal);
CREATE INDEX idx_dim_date_mah ON dim_date(Sal, Mah);

-- 2. بعد کالا (DimProduct)
CREATE TABLE IF NOT EXISTS dim_product (
    product_key SERIAL PRIMARY KEY,
    ccKala INTEGER NOT NULL UNIQUE,      -- کد کالا
    NameKala VARCHAR(256) NOT NULL,      -- نام کالا
    GenericCode VARCHAR(100),            -- کد ژنریک
    GroupDaraeeName VARCHAR(150),        -- گروه دارویی
    ccTaminKonandeh INTEGER,             -- کد تأمین‌کننده
    NameTaminKonandeh VARCHAR(150),      -- نام تأمین‌کننده
    NameTolidKonandeh VARCHAR(150),      -- نام تولیدکننده
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_dim_product_ccKala ON dim_product(ccKala);
CREATE INDEX idx_dim_product_ccTamin ON dim_product(ccTaminKonandeh);

-- 3. بعد مشتری (DimCustomer)
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key SERIAL PRIMARY KEY,
    ccMoshtary INTEGER NOT NULL UNIQUE,   -- کد مشتری
    NameMoshtary VARCHAR(256) NOT NULL,   -- نام مشتری
    ccMantagheh INTEGER,                  -- کد منطقه
    ccShahrMoshtary INTEGER,              -- کد شهر
    MablaghEtebar FLOAT DEFAULT 0,        -- مبلغ اعتبار
    ShomarehHesabNew VARCHAR(30),         -- شماره حساب
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_dim_customer_ccMoshtary ON dim_customer(ccMoshtary);
CREATE INDEX idx_dim_customer_mantagheh ON dim_customer(ccMantagheh);

-- 4. بعد فروشنده/کارمند (DimEmployee)
CREATE TABLE IF NOT EXISTS dim_employee (
    employee_key SERIAL PRIMARY KEY,
    ccAfrad INTEGER NOT NULL UNIQUE,      -- کد فرد (فروشنده)
    FullName VARCHAR(150) NOT NULL,       -- نام کامل
    IsInListBank BOOLEAN DEFAULT FALSE,   -- عضو لیست بانک
    Meliat VARCHAR(50),                   -- ملیت
    JamdarName VARCHAR(100),              -- نام جمع‌دار
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_dim_employee_ccAfrad ON dim_employee(ccAfrad);

-- 5. بعد مرکز پخش (DimDistCenter)
CREATE TABLE IF NOT EXISTS dim_dist_center (
    dist_center_key SERIAL PRIMARY KEY,
    ccMarkazPakhsh INTEGER NOT NULL UNIQUE, -- کد مرکز پخش
    NameMarkazPakhsh VARCHAR(100) NOT NULL, -- نام مرکز پخش
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_dim_dist_center_ccMarkaz ON dim_dist_center(ccMarkazPakhsh);

-- 6. جدول مانیتورینگ
CREATE SCHEMA IF NOT EXISTS etl_metadata;

CREATE TABLE IF NOT EXISTS etl_metadata.monitoring_log (
    id SERIAL PRIMARY KEY,
    pipeline_name VARCHAR(100) NOT NULL,
    run_id VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    rows_processed INTEGER DEFAULT 0,
    start_time TIMESTAMP DEFAULT NOW(),
    end_time TIMESTAMP,
    duration_seconds NUMERIC(10,2),
    error_message TEXT,
    additional_info JSONB
);


-- ============================================
-- ابعاد جدید برای Fact‌های Inventory, Purchase, Ledger, Asset
-- ============================================

-- 1. dim_warehouse (انبار)
CREATE TABLE IF NOT EXISTS dim_warehouse (
    warehouse_key SERIAL PRIMARY KEY,
    cc_anbar INTEGER NOT NULL UNIQUE,
    name_anbar VARCHAR(200) NOT NULL,
    cc_markaz_pakhsh INTEGER,
    code_noe_anbar INTEGER,
    cc_address INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_dim_warehouse_cc ON dim_warehouse(cc_anbar);

-- 2. dim_supplier (تأمین‌کننده)
CREATE TABLE IF NOT EXISTS dim_supplier (
    supplier_key SERIAL PRIMARY KEY,
    cc_tamin_konandeh INTEGER NOT NULL UNIQUE,
    name_tamin_konandeh VARCHAR(200) DEFAULT 'نامشخص',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_dim_supplier_cc ON dim_supplier(cc_tamin_konandeh);

-- 3. dim_tafsily (تفصیلی شناور - از Fact استخراج می‌شود)
CREATE TABLE IF NOT EXISTS dim_tafsily (
    tafsily_key SERIAL PRIMARY KEY,
    cc_tafsily INTEGER NOT NULL UNIQUE,
    name_tafsily VARCHAR(200) DEFAULT 'نامشخص',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 4. dim_moien (معین شناور - از Fact استخراج می‌شود)
CREATE TABLE IF NOT EXISTS dim_moien (
    moien_key SERIAL PRIMARY KEY,
    cc_moien INTEGER NOT NULL UNIQUE,
    name_moien VARCHAR(200) DEFAULT 'نامشخص',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 5. dim_asset_group (گروه دارایی)
CREATE TABLE IF NOT EXISTS dim_asset_group (
    asset_group_key SERIAL PRIMARY KEY,
    cc_goroh_daraee INTEGER NOT NULL UNIQUE,
    name_goroh_daraee VARCHAR(200) DEFAULT 'نامشخص',
    cc_goroh_asly_daraee INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_dim_asset_group_cc ON dim_asset_group(cc_goroh_daraee);