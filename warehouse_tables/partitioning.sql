-- ============================================
-- پارتیشن‌بندی جداول Fact برای عملکرد بهتر
-- مخصوص ۱۸ میلیون+ رکورد
-- ============================================

-- توجه: این اسکریپت را روی سرور اصلی اجرا کنید
-- در لپ‌تاپ تست لازم نیست

-- 1. تبدیل fact_sales به جدول پارتیشن‌بندی شده بر اساس date_key
-- (ماهانه = JAN, FEB, MAR, ...)

-- ابتدا جدول اصلی را به صورت پارتیشن‌بندی شده بازسازی می‌کنیم

-- Step 1: ایجاد جدول جدید پارتیشن‌بندی شده
CREATE TABLE fact_sales_partitioned (
    date_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,
    employee_key INTEGER NOT NULL,
    dist_center_key INTEGER NOT NULL,
    cc_darkhast_faktor INTEGER NOT NULL,
    sal_mali INTEGER NOT NULL,
    tedad_faktor NUMERIC(18,2),
    tedad_faktor_kartony NUMERIC(18,2),
    fi_forosh NUMERIC(18,2),
    mablagh_takhfif NUMERIC(18,2),
    mablagh_khales_satr NUMERIC(18,2),
    etl_created_at TIMESTAMP DEFAULT NOW(),
    etl_updated_at TIMESTAMP DEFAULT NOW(),
    etl_batch_id VARCHAR(20),
    PRIMARY KEY (cc_darkhast_faktor, sal_mali, product_key, date_key)
) PARTITION BY RANGE (date_key);

-- Step 2: ایجاد پارتیشن‌ها برای هر ماه از ۲۰۲۱ تا ۲۰۲۶
-- پارتیشن‌های ماهانه
CREATE TABLE fact_sales_202101 PARTITION OF fact_sales_partitioned
    FOR VALUES FROM (20210101) TO (20210201);
CREATE TABLE fact_sales_202102 PARTITION OF fact_sales_partitioned
    FOR VALUES FROM (20210201) TO (20210301);
CREATE TABLE fact_sales_202103 PARTITION OF fact_sales_partitioned
    FOR VALUES FROM (20210301) TO (20210401);
CREATE TABLE fact_sales_202104 PARTITION OF fact_sales_partitioned
    FOR VALUES FROM (20210401) TO (20210501);
CREATE TABLE fact_sales_202105 PARTITION OF fact_sales_partitioned
    FOR VALUES FROM (20210501) TO (20210601);
CREATE TABLE fact_sales_202106 PARTITION OF fact_sales_partitioned
    FOR VALUES FROM (20210601) TO (20210701);
CREATE TABLE fact_sales_202107 PARTITION OF fact_sales_partitioned
    FOR VALUES FROM (20210701) TO (20210801);
CREATE TABLE fact_sales_202108 PARTITION OF fact_sales_partitioned
    FOR VALUES FROM (20210801) TO (20210901);
CREATE TABLE fact_sales_202109 PARTITION OF fact_sales_partitioned
    FOR VALUES FROM (20210901) TO (20211001);
CREATE TABLE fact_sales_202110 PARTITION OF fact_sales_partitioned
    FOR VALUES FROM (20211001) TO (20211101);
CREATE TABLE fact_sales_202111 PARTITION OF fact_sales_partitioned
    FOR VALUES FROM (20211101) TO (20211201);
CREATE TABLE fact_sales_202112 PARTITION OF fact_sales_partitioned
    FOR VALUES FROM (20211201) TO (20220101);

-- ... تا ۲۰۲۶ (۶۰ پارتیشن)

-- Step 3: ایجاد ایندکس روی هر پارتیشن (Brin Index برای داده‌های مرتب)
CREATE INDEX idx_fact_sales_202101_date ON fact_sales_202101 USING BRIN (date_key);
CREATE INDEX idx_fact_sales_202102_date ON fact_sales_202102 USING BRIN (date_key);
-- ... برای همه پارتیشن‌ها


-- ============================================
-- نکات مهم پارتیشن‌بندی:
-- ============================================
-- 1. Brin Index برای date_key: حجم کم، سرعت بالا
-- 2. پارتیشن ماهانه: مدیریت آسان، حذف داده‌های قدیمی
-- 3. PRIMARY KEY باید شامل date_key باشد
-- 4. قبل از Backfill، ایندکس‌ها را غیرفعال کنید