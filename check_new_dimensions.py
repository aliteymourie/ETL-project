# فایل: check_new_dimensions.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.engine.extractor import DataExtractor
import pandas as pd

e = DataExtractor()

checks = {
    'dim_warehouse (انبار)': {
        'tables': ['Warehouse.Anbar', 'Warehouse.Anbarghesmat'],
        'key_col': 'ccAnbar',
        'name_col': 'NameAnbar'
    },
    'dim_supplier (تأمین‌کننده)': {
        'tables': ['Warehouse.KalaTaminKonandeh', 'Warehouse.TaminKonandeh', 'Sales.TaminKonandeh'],
        'key_col': 'ccTaminKonandeh',
        'name_col': 'NameTaminKonandeh'
    },
    'dim_tafsily (تفصیلی)': {
        'tables': ['Treasury.DariaftPardakhtTafsily', 'Accounting.Tafsily', 'Treasury.vDariaftPardakhtTafsily'],
        'key_col': 'ccTafsily',
        'name_col': 'NameTafsily'
    },
    'dim_moien (معین)': {
        'tables': ['Accounting.Moien', 'Treasury.Moien'],
        'key_col': 'ccMoien',
        'name_col': 'NameMoien'
    },
    'dim_asset_group (گروه دارایی)': {
        'tables': ['AssetAccounting.GorohDaraee', 'AssetAccounting.GorohAslyDaraee'],
        'key_col': 'ccGorohDaraee',
        'name_col': 'NameGorohDaraee'
    }
}

for dim_name, config in checks.items():
    print(f"\n{'='*60}")
    print(f"📁 {dim_name}")
    print(f"{'='*60}")
    
    found = False
    for table in config['tables']:
        try:
            df = pd.read_sql_query(f"SELECT TOP 0 * FROM {table}", e.src_engine)
            cols = list(df.columns)
            
            has_key = config['key_col'] in cols
            has_name = config['name_col'] in cols
            
            if has_key:
                print(f"  ✅ {table} ({len(cols)} ستون)")
                print(f"     ✓ {config['key_col']}: {'✅' if has_key else '❌'}")
                print(f"     ✓ {config['name_col']}: {'✅' if has_name else '❌'}")
                
                # ستون‌های مهم دیگر
                important = [c for c in cols if any(kw in c.lower() for kw in 
                    ['name', 'code', 'cc', 'active', 'vazeiat', 'type'])]
                print(f"     ستون‌های مهم: {important[:10]}")
                
                # نمونه
                sample = pd.read_sql_query(f"SELECT TOP 1 * FROM {table}", e.src_engine)
                if not sample.empty:
                    print(f"     نمونه: {config['key_col']}={sample[config['key_col']].iloc[0]}, "
                          f"{config['name_col']}={sample[config['name_col']].iloc[0] if has_name else 'N/A'}")
                
                found = True
                break
                
        except Exception as ex:
            continue
    
    if not found:
        print(f"  ❌ هیچ جدولی پیدا نشد")
        print(f"     جداول امتحان شده: {config['tables']}")
        print(f"     💡 پیشنهاد: از Fact اصلی Distinct بگیریم")

print(f"\n{'='*60}")
print("✅ پایان بررسی")