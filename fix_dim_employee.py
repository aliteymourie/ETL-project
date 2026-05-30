# فایل: fix_dim_employee.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from sqlalchemy import text
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.logging import setup_logger

logger = setup_logger("fix_employee")

def fix_missing_employees():
    """اضافه کردن فروشنده‌هایی که ccAfrad ندارند"""
    
    extractor = DataExtractor()
    loader = DataLoader()
    
    # 1. خواندن فروشنده‌های بدون ccAfrad از SQL Server
    query = """
        SELECT ccForoshandeh
        FROM Sales.Foroshandeh
        WHERE ccAfrad IS NULL AND ccForoshandeh IS NOT NULL
    """
    
    logger.info("📥 خواندن فروشنده‌های بدون ccAfrad از SQL Server...")
    df = pd.read_sql_query(query, extractor.src_engine)
    
    if df.empty:
        logger.info("✅ همه فروشنده‌ها ccAfrad دارند - مشکلی نیست")
        return 0
    
    logger.info(f"📋 {len(df):,} فروشنده بدون ccAfrad یافت شد")
    
    # 2. خواندن موجودی فعلی dim_employee
    with loader.tgt_engine.connect() as conn:
        existing = pd.read_sql('SELECT cc_afrad FROM dim_employee', conn)
    
    # 3. فیلتر فروشنده‌های جدید
    new_employees = df[~df['ccForoshandeh'].isin(existing['cc_afrad'])]
    
    if new_employees.empty:
        logger.info("✅ همه فروشنده‌های بدون ccAfrad قبلاً اضافه شده‌اند")
        return 0
    
    logger.info(f"🆕 {len(new_employees):,} فروشنده جدید باید اضافه شود")
    
    # 4. اضافه کردن به dim_employee
    inserted = 0
    with loader.tgt_engine.begin() as conn:
        for _, row in new_employees.iterrows():
            try:
                conn.execute(
                    text("""
                        INSERT INTO dim_employee (cc_afrad, full_name, is_active)
                        VALUES (:cc_afrad, :name, TRUE)
                        ON CONFLICT (cc_afrad) DO UPDATE SET
                            full_name = :name,
                            is_active = TRUE,
                            updated_at = NOW()
                    """),
                    {
                        "cc_afrad": int(row['ccForoshandeh']),
                        "name": f"{int(row['ccForoshandeh'])} - فروشنده"
                    }
                )
                inserted += 1
            except Exception as e:
                logger.warning(f"⚠️ خطا در ccForoshandeh={row['ccForoshandeh']}: {str(e)[:80]}")
    
    logger.info(f"✅ {inserted:,} فروشنده جدید اضافه شد")
    return inserted


if __name__ == "__main__":
    fix_missing_employees()