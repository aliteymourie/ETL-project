import psycopg2

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    user='postgres',
    password='1234ali1380',
    database='dw_test'
)
conn.autocommit = True
cursor = conn.cursor()

sql1 = """
CREATE TABLE IF NOT EXISTS fact_sales_header (
    sales_header_id BIGINT NOT NULL,
    year INT NOT NULL,
    customer_id INT,
    salesman_id INT,
    invoice_date TIMESTAMP,
    gross_amount DECIMAL(18,2),
    net_amount DECIMAL(18,2),
    tax_amount DECIMAL(18,2),
    modified_date TIMESTAMP,
    etl_loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (sales_header_id, year)
)
"""

sql2 = """
CREATE TABLE IF NOT EXISTS fact_sales_detail (
    sales_detail_id BIGINT NOT NULL,
    year INT NOT NULL,
    sales_header_id BIGINT,
    product_id INT,
    total_quantity DECIMAL(18,3),
    unit_price DECIMAL(18,2),
    discount_amount DECIMAL(18,2),
    net_line_amount DECIMAL(18,2),
    modified_date TIMESTAMP,
    etl_loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (sales_detail_id, year)
)
"""

sql3 = """
CREATE TABLE IF NOT EXISTS agg_daily_sales (
    date_id INTEGER PRIMARY KEY,
    total_net DECIMAL(18,2),
    total_units DECIMAL(18,3),
    orders_count INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

try:
    cursor.execute(sql1)
    print('✅ fact_sales_header ساخته شد')
except Exception as e:
    print(f'❌ خطا: {e}')

try:
    cursor.execute(sql2)
    print('✅ fact_sales_detail ساخته شد')
except Exception as e:
    print(f'❌ خطا: {e}')

try:
    cursor.execute(sql3)
    print('✅ agg_daily_sales ساخته شد')
except Exception as e:
    print(f'❌ خطا: {e}')

cursor.close()
conn.close()
print('🏁 تمام شد')