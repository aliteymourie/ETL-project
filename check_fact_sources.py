# فایل: check_fact_sources.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from core.engine.extractor import DataExtractor
from sqlalchemy import text

extractor = DataExtractor()

# لیست جداول احتمالی برای هر Fact
fact_sources = {
    'موجودی (Inventory)': [
        'Warehouse.Mojody',
        'Warehouse.MojodyRooz', 
        'Warehouse.KalaAnbar',
        'Warehouse.Anbar',
    ],
    'خرید (Purchases)': [
        'Warehouse.FaktorKharid',
        'Warehouse.FaktorKharidSatr',
        'Warehouse.Sefaresh',
        'Warehouse.SefareshSatr',
    ],
    'مرجوعی (Returns)': [
        'Warehouse.MarjoeeJavayez',
        'Sales.DarkhastFaktor',  # ممکنه با CodeVazeiat مشخص بشه
    ],
    'پرداخت/وصول (Payments)': [
        'Sales.DarkhastFaktor',  # احتمالاً ستون‌های مالی داره
    ]
}

print("=" * 80)
print("🔍 بررسی جداول منبع برای Fact‌های جدید")
print("=" * 80)

for fact_name, tables in fact_sources.items():
    print(f"\n{'='*80}")
    print(f"📊 {fact_name}")
    print(f"{'='*80}")
    
    found = False
    for table_name in tables:
        try:
            # تست وجود جدول
            query = f"SELECT TOP 0 * FROM {table_name}"
            df = pd.read_sql_query(query, extractor.src_engine)
            found = True
            
            print(f"\n✅ جدول: {table_name}")
            print(f"   تعداد ستون‌ها: {len(df.columns)}")
            
            # نمایش ستون‌های مهم (شامل عدد، مبلغ، تاریخ، کد)
            important_cols = [c for c in df.columns if any(
                kw in c.lower() 
                for kw in ['cc', 'date', 'tarikh', 'tedad', 'mablagh', 'mojody', 
                          'kharid', 'marjoo', 'vosol', 'etebar', 'sal', 'code']
            )]
            
            if important_cols:
                print(f"   ستون‌های مهم ({len(important_cols)}):")
                for col in important_cols[:20]:
                    print(f"      - {col}")
                if len(important_cols) > 20:
                    print(f"      ... و {len(important_cols)-20} ستون دیگر")
            else:
                print(f"   همه ستون‌ها ({len(df.columns)}):")
                for col in df.columns[:15]:
                    print(f"      - {col}")
            
            # یک رکورد نمونه
            try:
                sample = pd.read_sql_query(f"SELECT TOP 1 * FROM {table_name}", extractor.src_engine)
                print(f"\n   📝 نمونه داده:")
                for col in important_cols[:8]:
                    val = sample[col].iloc[0] if not sample.empty else 'NULL'
                    print(f"      {col}: {val}")
            except:
                pass
            
            break  # جدول پیدا شد
            
        except Exception as e:
            continue
    
    if not found:
        print(f"❌ هیچ یک از جداول یافت نشد: {', '.join(tables)}")
        print("   → نیاز به بررسی دستی نام جداول")

print("\n" + "=" * 80)
print("✅ بررسی پایان یافت. حالا می‌توانیم Fact‌ها را طراحی کنیم.")