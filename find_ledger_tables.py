# فایل: check_financial_accounting.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.engine.extractor import DataExtractor
import pandas as pd

e = DataExtractor()

# جداول کلیدی FinancialAccounting
tables_to_check = [
    'FinancialAccounting.Tafsily',
    'FinancialAccounting.vTafsily',
    'FinancialAccounting.NoeTafsily',
    'FinancialAccounting.SaierTafsily',
    'FinancialAccounting.vCodeMoeenNoeTafsily',
]

for table in tables_to_check:
    print(f"\n{'='*60}")
    print(f"📊 {table}")
    try:
        df = pd.read_sql_query(f"SELECT TOP 0 * FROM {table}", e.src_engine)
        cols = list(df.columns)
        print(f"   ستون‌ها: {cols[:20]}")
        
        # نمونه
        sample = pd.read_sql_query(f"SELECT TOP 1 * FROM {table}", e.src_engine)
        if not sample.empty:
            print(f"   نمونه: {sample.iloc[0].to_dict()}")
    except Exception as ex:
        print(f"   ❌ {str(ex)[:100]}")

# همچنین دنبال Moien و Ledger بگردیم
print(f"\n{'='*60}")
print("🔍 جستجوی Moien و Ledger")

query = """
    SELECT TABLE_SCHEMA, TABLE_NAME
    FROM INFORMATION_SCHEMA.TABLES
    WHERE (TABLE_NAME LIKE '%Moien%' 
        OR TABLE_NAME LIKE '%Moeen%'
        OR TABLE_NAME LIKE '%Ledger%'
        OR TABLE_NAME LIKE '%DaftarKol%')
      AND TABLE_SCHEMA NOT IN ('dbo', 'Legal', 'Payroll')
    ORDER BY TABLE_SCHEMA, TABLE_NAME
"""
df = pd.read_sql_query(query, e.src_engine)
for _, row in df.iterrows():
    print(f"  📁 {row['TABLE_SCHEMA']}.{row['TABLE_NAME']}")

print("\n✅ پایان")