# فایل: debug_sales_join.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.logging import setup_logger

logger = setup_logger("debug")

extractor = DataExtractor()
loader = DataLoader()

# 1. یک نمونه فاکتور
headers = pd.read_sql_query("""
    SELECT TOP 5 ccDarkhastFaktor, Sal, ccMoshtary, ccForoshandeh, ccMarkazPakhsh, TarikhFaktor
    FROM Sales.DarkhastFaktor
    WHERE TarikhFaktor >= '2026-05-24' AND TarikhFaktor <= '2026-05-25'
""", extractor.src_engine)

print("=" * 60)
print("نمونه هدر فاکتورها:")
print(headers[['ccDarkhastFaktor', 'ccMoshtary', 'ccForoshandeh', 'ccMarkazPakhsh']])
print()

# 2. نمونه سطر فاکتور
details = pd.read_sql_query("""
    SELECT TOP 5 d.ccDarkhastFaktor, d.ccKala, d.TedadAdadi
    FROM Sales.DarkhastFaktorSatr d
    WHERE d.ccDarkhastFaktor IN (
        SELECT TOP 5 ccDarkhastFaktor FROM Sales.DarkhastFaktor
        WHERE TarikhFaktor >= '2026-05-24' AND TarikhFaktor <= '2026-05-25'
    )
""", extractor.src_engine)

print("نمونه سطر فاکتور:")
print(details[['ccDarkhastFaktor', 'ccKala', 'TedadAdadi']])
print()

# 3. بررسی JOIN با dim_product
with loader.tgt_engine.connect() as conn:
    dim_product = pd.read_sql('SELECT product_key, cc_kala FROM dim_product', conn)
    dim_customer = pd.read_sql('SELECT customer_key, cc_moshtary FROM dim_customer', conn)
    dim_employee = pd.read_sql('SELECT employee_key, cc_afrad FROM dim_employee', conn)
    dim_center = pd.read_sql('SELECT dist_center_key, cc_markaz_pakhsh FROM dim_dist_center', conn)

# تست JOIN
df = pd.merge(headers, details, on='ccDarkhastFaktor', how='inner')
print(f"بعد از merge header+detail: {len(df)} رکورد")
print(f"ccKala های نمونه: {df['ccKala'].tolist()[:5]}")
print(f"ccMoshtary های نمونه: {df['ccMoshtary'].tolist()[:5]}")
print(f"ccForoshandeh های نمونه: {df['ccForoshandeh'].tolist()[:5]}")
print(f"ccMarkazPakhsh های نمونه: {df['ccMarkazPakhsh'].tolist()[:5]}")
print()

# تست JOIN با dim_product
df_p = pd.merge(df, dim_product, left_on='ccKala', right_on='cc_kala', how='left')
print(f"بعد از JOIN با dim_product: {len(df_p)}")
print(f"product_key ها: {df_p['product_key'].tolist()[:5]}")
print(f"NULL در product_key: {df_p['product_key'].isna().sum()}")
print()

# تست JOIN با dim_customer
df_c = pd.merge(df_p, dim_customer, left_on='ccMoshtary', right_on='cc_moshtary', how='left')
print(f"بعد از JOIN با dim_customer: {len(df_c)}")
print(f"customer_key ها: {df_c['customer_key'].tolist()[:5]}")
print(f"NULL در customer_key: {df_c['customer_key'].isna().sum()}")
print()

# تست JOIN با dim_employee
df_e = pd.merge(df_c, dim_employee, left_on='ccForoshandeh', right_on='cc_afrad', how='left')
print(f"بعد از JOIN با dim_employee: {len(df_e)}")
print(f"employee_key ها: {df_e['employee_key'].tolist()[:5]}")
print(f"NULL در employee_key: {df_e['employee_key'].isna().sum()}")
print()

# بررسی تطابق ccForoshandeh با cc_afrad
print(f"ccForoshandeh در فاکتور: {df['ccForoshandeh'].unique()[:5]}")
print(f"cc_afrad در dim_employee: {dim_employee['cc_afrad'].unique()[:5]}")
print(f"تعداد فروشنده‌های مشترک: {len(set(df['ccForoshandeh']).intersection(set(dim_employee['cc_afrad'])))}")