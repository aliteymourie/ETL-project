# فایل: fix_all_facts.py
# اجرای سریع برای دیدن نتایج
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.engine.extractor import DataExtractor
import pandas as pd

e = DataExtractor()

print("=" * 60)
print("🔍 تست FaktorKharid - چرا JOIN خالی است؟")
print("=" * 60)

# تست بدون JOIN
try:
    h = pd.read_sql_query("SELECT TOP 3 ccFaktorKharid, TarikhFaktorKharid FROM Warehouse.FaktorKharid ORDER BY TarikhFaktorKharid DESC", e.src_engine)
    print(f"FaktorKharid: {len(h)} رکورد")
    print(h)
    
    s = pd.read_sql_query("SELECT TOP 3 * FROM Warehouse.FaktorKharidSatr", e.src_engine)
    print(f"\nFaktorKharidSatr: {len(s)} رکورد")
    print(s)
    
    # آیا اصلاً دیتا دارند؟
    count_h = pd.read_sql_query("SELECT COUNT(*) as cnt FROM Warehouse.FaktorKharid", e.src_engine).iloc[0,0]
    count_s = pd.read_sql_query("SELECT COUNT(*) as cnt FROM Warehouse.FaktorKharidSatr", e.src_engine).iloc[0,0]
    print(f"\nکل FaktorKharid: {count_h:,}")
    print(f"کل FaktorKharidSatr: {count_s:,}")
except Exception as ex:
    print(f"❌ {ex}")