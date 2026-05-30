# فایل: check_accounting.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.engine.extractor import DataExtractor
import pandas as pd

e = DataExtractor()

# لیست جداول Treasury
print('=' * 60)
print('📁 Treasury Tables')
print('=' * 60)
try:
    df = pd.read_sql_query(
        "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'Treasury'",
        e.src_engine
    )
    for t in df['TABLE_NAME']:
        print(f'  ✓ {t}')
except Exception as ex:
    print(f'  ❌ {ex}')

# لیست جداول AssetAccounting
print('\n' + '=' * 60)
print('📁 AssetAccounting Tables')
print('=' * 60)
try:
    df = pd.read_sql_query(
        "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'AssetAccounting'",
        e.src_engine
    )
    for t in df['TABLE_NAME']:
        print(f'  ✓ {t}')
except Exception as ex:
    print(f'  ❌ {ex}')

# بررسی ستون‌های FaktorKharidSatr
print('\n' + '=' * 60)
print('📊 Warehouse.FaktorKharidSatr')
print('=' * 60)
try:
    df = pd.read_sql_query(
        "SELECT TOP 3 * FROM Warehouse.FaktorKharidSatr",
        e.src_engine
    )
    print(f'ستون‌ها: {list(df.columns)}')
    print(f'\nنمونه داده:')
    print(df.to_string())
except Exception as ex:
    print(f'❌ {ex}')

# بررسی ستون‌های مهم Treasury
print('\n' + '=' * 60)
print('📊 Treasury Sample Tables')
print('=' * 60)
for table in ['Treasury.SanadDariaft', 'Treasury.Chek', 'Treasury.Vosol']:
    try:
        df = pd.read_sql_query(f"SELECT TOP 0 * FROM {table}", e.src_engine)
        cols = list(df.columns)
        print(f'\n✓ {table}: {len(cols)} ستون')
        
        # ستون‌های مهم
        important = [c for c in cols if any(kw in c.lower() for kw in 
            ['sanad', 'chek', 'vosol', 'mablagh', 'tarikh', 'cc', 'code', 'bed', 'bes'])]
        print(f'  ستون‌های مهم: {important[:15]}')
        
    except Exception as ex:
        print(f'✗ {table}: {str(ex)[:80]}')

# بررسی ستون‌های مهم AssetAccounting
print('\n' + '=' * 60)
print('📊 AssetAccounting Sample Tables')
print('=' * 60)
for table in ['AssetAccounting.Amval', 'AssetAccounting.Estehlak']:
    try:
        df = pd.read_sql_query(f"SELECT TOP 0 * FROM {table}", e.src_engine)
        cols = list(df.columns)
        print(f'\n✓ {table}: {len(cols)} ستون')
        
        # ستون‌های مهم
        important = [c for c in cols if any(kw in c.lower() for kw in 
            ['amval', 'gheymat', 'arzesh', 'estehlak', 'depreciation', 'tarikh', 'cc'])]
        print(f'  ستون‌های مهم: {important[:15]}')
        
    except Exception as ex:
        print(f'✗ {table}: {str(ex)[:80]}')

print('\n' + '=' * 60)
print('✅ پایان')