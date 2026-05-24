"""
تولید DDL برای Data Warehouse فروش
نسخه اصلاح شده با نگاشت دقیق نوع داده‌ها
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_FILE = ROOT / 'mother data base guide' / 'sales_schema.json'
OUT_DIR = ROOT / 'warehouse_tables' / 'final'


def load_json(path: Path) -> dict:
    """لود فایل JSON schema"""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def map_sql_type(col_name: str, meta: dict) -> str:
    """
    نگاشت دقیق نوع داده SQL Server به PostgreSQL
    
    Args:
        col_name: نام ستون
        meta: متادیتای ستون از schema
        
    Returns:
        نوع داده PostgreSQL
    """
    data_type = meta.get('data_type', '').lower()
    
    # نگاشت مستقیم بر اساس data_type
    type_mapping = {
        'bigint': 'BIGINT',
        'int': 'INTEGER',
        'smallint': 'SMALLINT',
        'tinyint': 'SMALLINT',
        'bit': 'BOOLEAN',
        'float': 'DOUBLE PRECISION',
        'real': 'REAL',
        'money': 'DECIMAL(18,2)',
        'decimal': 'DECIMAL(18,2)',
        'numeric': 'NUMERIC',
        'datetime': 'TIMESTAMP',
        'date': 'DATE',
        'time': 'TIME',
        'varchar': 'VARCHAR(255)',
        'nvarchar': 'VARCHAR(500)',
        'nchar': 'CHAR(10)',
        'char': 'CHAR(1)',
        'text': 'TEXT',
        'uniqueidentifier': 'UUID',
        'varbinary': 'BYTEA',
    }
    
    if data_type in type_mapping:
        return type_mapping[data_type]
    
    # نگاشت کمکی بر اساس نام ستون (فال‌بک)
    col_lower = col_name.lower()
    
    if col_lower.startswith('cc'):
        return 'INTEGER'
    elif any(word in col_lower for word in ['tarikh', 'date', 'time']):
        return 'TIMESTAMP'
    elif any(word in col_lower for word in ['mablagh', 'price', 'gheymat', 'rial', 'fee']):
        return 'DECIMAL(18,2)'
    elif any(word in col_lower for word in ['tedad', 'count', 'quantity']):
        return 'DECIMAL(18,3)'
    elif any(word in col_lower for word in ['darsad', 'percent']):
        return 'DECIMAL(5,2)'
    elif col_lower.startswith('shomareh') or col_lower.startswith('code'):
        if col_lower.endswith(('id', 'code')):
            return 'INTEGER'
        return 'VARCHAR(100)'
    elif 'name' in col_lower or 'sharh' in col_lower:
        return 'VARCHAR(500)'
    elif 'tozihat' in col_lower or 'description' in col_lower:
        return 'TEXT'
    elif 'guid' in col_lower:
        return 'UUID'
    
    # پیش‌فرض
    return 'TEXT'


def generate_create_table(name: str, table_meta: dict, pk: List[str] = None) -> str:
    """
    تولید DDL CREATE TABLE
    
    Args:
        name: نام جدول مقصد
        table_meta: متادیتای جدول از schema
        pk: لیست کلیدهای اصلی
        
    Returns:
        دستور SQL
    """
    cols = table_meta.get('columns', {})
    
    if not cols:
        return f"-- جدول {name} بدون ستون است\n"
    
    lines = []
    for col_name, meta in cols.items():
        dtype = map_sql_type(col_name, meta)
        # اطمینان از نام‌گذاری صحیح ستون
        safe_name = col_name.replace(' ', '_').replace('-', '_')
        lines.append(f'    "{safe_name}" {dtype}')
    
    # اضافه کردن PRIMARY KEY
    if pk:
        pk_cols = ', '.join([f'"{p}"' for p in pk])
        lines.append(f'    PRIMARY KEY ({pk_cols})')
    
    # اضافه کردن ستون ETL
    lines.append(f'    etl_loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    
    ddl = f'CREATE TABLE IF NOT EXISTS {name} (\n'
    ddl += ',\n'.join(lines)
    ddl += '\n);\n'
    
    return ddl


def generate_fact_sales_header() -> str:
    """تولید DDL جدول fact_sales_header"""
    return """
CREATE TABLE IF NOT EXISTS fact_sales_header (
    sales_header_id BIGINT NOT NULL,
    year INT NOT NULL,
    customer_id INT,
    salesman_id INT,
    distribution_center_id INT,
    sales_group_id INT,
    invoice_number INT,
    invoice_date TIMESTAMP,
    gross_amount DECIMAL(18,2) DEFAULT 0,
    header_discount_amount DECIMAL(18,2) DEFAULT 0,
    line_discount_amount DECIMAL(18,2) DEFAULT 0,
    additional_amount DECIMAL(18,2) DEFAULT 0,
    net_amount DECIMAL(18,2) DEFAULT 0,
    tax_amount DECIMAL(18,2) DEFAULT 0,
    duty_amount DECIMAL(18,2) DEFAULT 0,
    status_code SMALLINT DEFAULT 1,
    invoice_type SMALLINT,
    fiscal_period_id INT,
    modified_date TIMESTAMP,
    created_date TIMESTAMP,
    etl_loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (sales_header_id, year)
);

CREATE INDEX IF NOT EXISTS idx_fh_invoice_date ON fact_sales_header(invoice_date);
CREATE INDEX IF NOT EXISTS idx_fh_customer ON fact_sales_header(customer_id);
CREATE INDEX IF NOT EXISTS idx_fh_salesman ON fact_sales_header(salesman_id);
"""


def generate_fact_sales_detail() -> str:
    """تولید DDL جدول fact_sales_detail"""
    return """
CREATE TABLE IF NOT EXISTS fact_sales_detail (
    sales_detail_id BIGINT NOT NULL,
    year INT NOT NULL,
    sales_header_id BIGINT,
    product_id INT,
    product_code_id INT,
    batch_number VARCHAR(100),
    production_date TIMESTAMP,
    expiry_date TIMESTAMP,
    quantity_pack DECIMAL(18,3) DEFAULT 0,
    quantity_box DECIMAL(18,3) DEFAULT 0,
    quantity_unit DECIMAL(18,3) DEFAULT 0,
    total_quantity DECIMAL(18,3) DEFAULT 0,
    unit_price DECIMAL(18,2) DEFAULT 0,
    discount_amount DECIMAL(18,2) DEFAULT 0,
    tax_amount DECIMAL(18,2) DEFAULT 0,
    duty_amount DECIMAL(18,2) DEFAULT 0,
    net_line_amount DECIMAL(18,2) DEFAULT 0,
    status_code SMALLINT DEFAULT 1,
    modified_date TIMESTAMP,
    created_date TIMESTAMP,
    etl_loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (sales_detail_id, year),
    FOREIGN KEY (sales_header_id, year) 
        REFERENCES fact_sales_header(sales_header_id, year)
);

CREATE INDEX IF NOT EXISTS idx_fd_header ON fact_sales_detail(sales_header_id);
CREATE INDEX IF NOT EXISTS idx_fd_product ON fact_sales_detail(product_id);
"""


def generate_agg_tables() -> str:
    """تولید DDL جداول تجمیعی"""
    return """
CREATE TABLE IF NOT EXISTS agg_daily_sales (
    date_id INTEGER PRIMARY KEY,
    total_net DECIMAL(18,2) DEFAULT 0,
    total_units DECIMAL(18,3) DEFAULT 0,
    orders_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agg_weekly_sales (
    year INTEGER NOT NULL,
    week INTEGER NOT NULL,
    total_net DECIMAL(18,2) DEFAULT 0,
    total_units DECIMAL(18,3) DEFAULT 0,
    orders_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (year, week)
);

CREATE TABLE IF NOT EXISTS agg_monthly_sales (
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    total_net DECIMAL(18,2) DEFAULT 0,
    total_units DECIMAL(18,3) DEFAULT 0,
    orders_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (year, month)
);
"""


def main():
    """تولید همه فایل‌های DDL"""
    schema = load_json(SCHEMA_FILE)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    output_files = {
        '01_fact_sales_header.sql': generate_fact_sales_header(),
        '02_fact_sales_detail.sql': generate_fact_sales_detail(),
        '03_agg_tables.sql': generate_agg_tables(),
    }
    
    # تولید DDL برای جداول Staging (اختیاری)
    staging_tables = {
        'DarkhastFaktor': '04_stg_sales_header.sql',
        'DarkhastFaktorSatr': '05_stg_sales_detail.sql',
    }
    
    for source_table, filename in staging_tables.items():
        if source_table in schema:
            ddl = generate_create_table(
                f'stg_{source_table.lower()}',
                schema[source_table],
                pk=schema[source_table].get('primary_keys', [])
            )
            output_files[filename] = ddl
    
    # نوشتن فایل‌ها
    for filename, ddl in output_files.items():
        path = OUT_DIR / filename
        with open(path, 'w', encoding='utf-8') as f:
            f.write('-- ============================================\n')
            f.write(f'-- {filename}\n')
            f.write('-- تولید شده به صورت خودکار\n')
            f.write('-- ============================================\n\n')
            f.write(ddl)
        print(f'✅ {path}')
    
    # نوشتن فایل کامل
    all_ddl_path = OUT_DIR / '00_all_sales_ddl.sql'
    with open(all_ddl_path, 'w', encoding='utf-8') as f:
        f.write('-- ============================================\n')
        f.write('-- DDL کامل Data Warehouse فروش\n')
        f.write('-- ============================================\n\n')
        for filename, ddl in output_files.items():
            f.write(f'\n-- {filename}\n')
            f.write(ddl)
            f.write('\n')
    print(f'✅ {all_ddl_path}')


if __name__ == '__main__':
    main()