# فایل: check_treasury_details.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.engine.extractor import DataExtractor
import pandas as pd

e = DataExtractor()

# مهمترین جداول Treasury
key_tables = [
    'Treasury.DariaftPardakht',
    'Treasury.DariaftPardakhtDarkhastFaktor',
    'Treasury.vDariaftPardakht',
    'Treasury.DastehCheck',
    'Treasury.DastehCheckBarg',
    'Treasury.Safteh',
]

for table in key_tables:
    print(f"\n{'='*60}")
    print(f"📊 {table}")
    print(f"{'='*60}")
    try:
        df = pd.read_sql_query(f"SELECT TOP 0 * FROM {table}", e.src_engine)
        cols = list(df.columns)
        print(f"   ستون‌ها ({len(cols)}):")
        
        # ستون‌های مهم مالی
        important = [c for c in cols if any(kw in c.lower() for kw in [
            'mablagh', 'bed', 'bes', 'chek', 'sanad', 'tarikh', 'cc', 'code', 
            'vosol', 'etebar', 'takhfif', 'naghs', 'bargasht'
        ])]
        for col in important[:20]:
            print(f"      ✓ {col}")
        
        # نمونه
        sample = pd.read_sql_query(f"SELECT TOP 1 * FROM {table}", e.src_engine)
        if not sample.empty:
            print(f"\n   نمونه:")
            for col in important[:5]:
                print(f"      {col}: {sample[col].iloc[0]}")
                
    except Exception as ex:
        print(f"   ❌ {str(ex)[:100]}")

print(f"\n{'='*60}")
print("✅ پایان")