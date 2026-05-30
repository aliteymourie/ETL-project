# فایل: check_all_fact_sources.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from core.engine.extractor import DataExtractor

extractor = DataExtractor()

# نقشه کامل Fact ها و جداول منبع
fact_mapping = {
    'FactSales': {
        'table': 'Sales.DarkhastFaktor + Sales.DarkhastFaktorSatr',
        'columns_needed': [
            'ccDarkhastFaktor', 'Sal', 'ccMoshtary', 'ccForoshandeh', 
            'ccMarkazPakhsh', 'TarikhFaktor',
            'TedadAdadi', 'TedadKarton', 'MablaghForosh', 
            'MablaghTakhfifFaktor', 'MablaghForoshKhalesKala'
        ]
    },
    'FactInventory': {
        'tables': ['Warehouse.Mojody', 'Warehouse.MojodyRooz', 'Warehouse.KalaAnbar'],
        'columns_needed': [
            'ccKala', 'ccAnbar', 'Mojody', 'MojodyAnbarKartony', 
            'MojodyAnbarTedady', 'MojodyAnbarRialy',
            'FaktorToziNashodehRialy', 'Tedad_AghlamNazdik'
        ]
    },
    'FactPurchase': {
        'tables': ['Warehouse.FaktorKharid', 'Warehouse.FaktorKharidSatr'],
        'columns_needed': [
            'ccFaktorKharid', 'ccMarkazPakhsh', 'ccTaminKonandeh',
            'TarikhFaktorKharid', 'AzMablagh', 'TaMablagh', 'TedadKharid'
        ]
    },
    'FactTreasury': {
        'tables': ['Accounting.SanadDariaft', 'Accounting.Chek'],
        'columns_needed': [
            'ccSanadDariaft', 'ccMoshtary', 'ccForoshandeh', 'ccMarkazPakhsh',
            'TarikhSanad', 'MablaghSanad', 'ChekBargashty', 
            'TakhfifNaghdi20', 'NaghsChek'
        ]
    },
    'FactLedger': {
        'tables': ['Accounting.Ledger', 'Accounting.Moien'],
        'columns_needed': [
            'ccTafsily', 'ccMoien', 'ccMarkazPakhsh', 'ccAfrad',
            'Tarikh', 'Bed', 'Bes', 'SumBed', 'SumBes'
        ]
    },
    'FactAsset': {
        'tables': ['Accounting.Amval', 'Accounting.Estehlak'],
        'columns_needed': [
            'ccAmval', 'ccMarkazPakhsh', 'ccAfrad',
            'GheymatTamamShodeh', 'ArzeshDaftary', 
            'EstehlakAnbashteh', 'DepreciationRate'
        ]
    }
}

print("=" * 80)
print("🔍 بررسی ستون‌های واقعی برای هر Fact")
print("=" * 80)

for fact_name, config in fact_mapping.items():
    print(f"\n{'='*80}")
    print(f"📊 {fact_name}")
    print(f"{'='*80}")
    
    tables = config.get('tables', [config.get('table', '')])
    
    for table in tables:
        if not table or '+' in table:
            continue
            
        print(f"\n🔹 جدول: {table}")
        
        try:
            df = pd.read_sql_query(f"SELECT TOP 0 * FROM {table}", extractor.src_engine)
            all_cols = list(df.columns)
            
            # ستون‌های موجود
            found_cols = [c for c in config['columns_needed'] if c in all_cols]
            missing_cols = [c for c in config['columns_needed'] if c not in all_cols]
            
            print(f"   ✅ ستون‌های پیدا شده ({len(found_cols)}):")
            for col in found_cols:
                print(f"      ✓ {col}")
            
            if missing_cols:
                print(f"   ❌ ستون‌های ناموجود ({len(missing_cols)}):")
                for col in missing_cols:
                    print(f"      ✗ {col}")
                
                # پیشنهاد جایگزین
                print(f"   💡 ستون‌های مشابه موجود:")
                similar = [c for c in all_cols if any(
                    m.lower() in c.lower() 
                    for m in missing_cols[0].lower().split('_')[:2]
                )]
                for col in similar[:10]:
                    print(f"      → {col}")
            
            # نمونه داده
            sample = pd.read_sql_query(f"SELECT TOP 1 * FROM {table}", extractor.src_engine)
            if not sample.empty:
                print(f"\n   📝 نمونه مقادیر:")
                for col in found_cols[:5]:
                    print(f"      {col}: {sample[col].iloc[0]}")
                    
        except Exception as e:
            print(f"   ❌ خطا: {str(e)[:100]}")
    
    print()

print("=" * 80)
print("✅ بررسی پایان یافت")