# فایل: check_table_structure.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.engine.extractor import DataExtractor
from sqlalchemy import text

extractor = DataExtractor()

# 1. لیست تمام جداول اسکیمای Warehouse
print("=" * 80)
print("📋 جداول موجود در اسکیمای Warehouse:")
print("=" * 80)

query_tables = """
    SELECT TABLE_SCHEMA, TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'Warehouse' 
      AND TABLE_TYPE = 'BASE TABLE'
    ORDER BY TABLE_NAME
"""

with extractor.src_engine.connect() as conn:
    tables = conn.execute(text(query_tables))
    for table in tables:
        print(f"  📁 {table[0]}.{table[1]}")

# 2. ستون‌های جدول Kala
print("\n" + "=" * 80)
print("🔍 ستون‌های جدول Warehouse.Kala:")
print("=" * 80)

query_columns = """
    SELECT 
        COLUMN_NAME,
        DATA_TYPE,
        CHARACTER_MAXIMUM_LENGTH,
        IS_NULLABLE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'Warehouse' 
      AND TABLE_NAME = 'Kala'
    ORDER BY ORDINAL_POSITION
"""

with extractor.src_engine.connect() as conn:
    columns = conn.execute(text(query_columns))
    for col in columns:
        print(f"  • {col[0]:<30} {col[1]:<15} length={col[2]} nullable={col[3]}")

# 3. نمونه داده‌ها (10 ردیف اول)
print("\n" + "=" * 80)
print("📊 10 ردیف اول از جدول Kala:")
print("=" * 80)

try:
    query_sample = "SELECT TOP 10 * FROM Warehouse.Kala"
    import pandas as pd
    df = pd.read_sql_query(query_sample, extractor.src_engine)
    print(df.to_string())
    print(f"\nتعداد کل ستون‌ها: {len(df.columns)}")
    print(f"نام ستون‌ها: {list(df.columns)}")
except Exception as e:
    print(f"❌ خطا: {e}")

# 4. بررسی جداول مرتبط (GroupDaraee و TaminKonandeh)
print("\n" + "=" * 80)
print("🔍 بررسی وجود جداول GroupDaraee و TaminKonandeh:")
print("=" * 80)

for table_name in ['GroupDaraee', 'TaminKonandeh']:
    query = f"""
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = 'Warehouse' 
          AND TABLE_NAME = '{table_name}'
    """
    with extractor.src_engine.connect() as conn:
        result = conn.execute(text(query))
        exists = result.scalar() > 0
        print(f"  {table_name}: {'✅ موجود' if exists else '❌ وجود ندارد'}")
    
    if exists:
        query_cols = f"""
            SELECT COLUMN_NAME, DATA_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'Warehouse' 
              AND TABLE_NAME = '{table_name}'
            ORDER BY ORDINAL_POSITION
        """
        with extractor.src_engine.connect() as conn:
            cols = conn.execute(text(query_cols))
            print("    ستون‌ها:")
            for col in cols:
                print(f"      - {col[0]} ({col[1]})")