# scripts/check_config.py
import os
import sys
from pathlib import Path
from sqlalchemy import text

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# لود .env
from dotenv import load_dotenv
load_dotenv(project_root / '.env')

print("=" * 50)
print("🔍 بررسی تنظیمات")
print("=" * 50)

# چک متغیرهای مبدأ
print("\n📦 SQL Server (مبدأ):")
src_vars = ['SRC_DB_HOST', 'SRC_DB_PORT', 'SRC_DB_DATABASE', 'SRC_DB_USER', 'SRC_DB_PASSWORD']
for var in src_vars:
    value = os.getenv(var)
    if value:
        # پسورد رو mask کن
        if 'PASSWORD' in var:
            print(f"  ✅ {var}: {value[:3]}***")
        else:
            print(f"  ✅ {var}: {value}")
    else:
        print(f"  ❌ {var}: تنظیم نشده!")

# چک متغیرهای مقصد
print("\n📦 PostgreSQL (مقصد):")
tgt_vars = ['TGT_DB_HOST', 'TGT_DB_PORT', 'TGT_DB_DATABASE', 'TGT_DB_USER', 'TGT_DB_PASSWORD']
for var in tgt_vars:
    value = os.getenv(var)
    if value:
        if 'PASSWORD' in var:
            print(f"  ✅ {var}: {value[:3]}***")
        else:
            print(f"  ✅ {var}: {value}")
    else:
        print(f"  ❌ {var}: تنظیم نشده!")

# تست لود databases.yaml
print("\n📋 تست لود databases.yaml:")
try:
    from core.engine.base_etl import BaseETL
    etl = BaseETL()
    print("  ✅ BaseETL با موفقیت لود شد")
    
    # چک کردن connection string ساخته شده
    mssql_cfg = etl.db_config['source_databases']['mssql_pharma']
    print(f"  📍 MSSQL Host: {mssql_cfg['host']}")
    print(f"  📍 MSSQL DB: {mssql_cfg['database']}")
    print(f"  📍 MSSQL User: {mssql_cfg['user']}")
    
    pg_cfg = etl.db_config['target_databases']['dw_postgres']
    print(f"  📍 PG Host: {pg_cfg['host']}")
    print(f"  📍 PG DB: {pg_cfg['database']}")
    print(f"  📍 PG User: {pg_cfg['user']}")
    
except Exception as e:
    print(f"  ❌ خطا: {e}")

# تست واقعی اتصال
print("\n🔌 تست اتصال واقعی:")

# SQL Server
try:
    from core.engine.base_etl import BaseETL
    etl = BaseETL()
    engine = etl.get_mssql_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 as test")).scalar()
        print(f"  ✅ SQL Server: متصل (نتیجه: {result})")
        
        # چک کردن جدول اصلی
        count = conn.execute(text("SELECT COUNT(*) FROM DarkhastFaktor")).scalar()
        print(f"  ✅ DarkhastFaktor: {count:,} رکورد موجود است")
except Exception as e:
    print(f"  ❌ SQL Server: {str(e)[:200]}")

# PostgreSQL
try:
    from core.engine.base_etl import BaseETL
    etl = BaseETL()
    engine = etl.get_postgres_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 as test")).scalar()
        print(f"  ✅ PostgreSQL: متصل (نتیجه: {result})")
        
        # چک کردن جداول
        for table in ['fact_sales_header', 'fact_sales_detail', 'agg_daily_sales']:
            try:
                count = conn.execute(f"SELECT COUNT(*) FROM {table}").scalar()
                print(f"  ✅ {table}: {count:,} رکورد")
            except Exception:
                print(f"  ⚠️ {table}: جدول وجود ندارد")
except Exception as e:
    print(f"  ❌ PostgreSQL: {str(e)[:200]}")

print("\n" + "=" * 50)
print("🏁 پایان بررسی")
print("=" * 50)