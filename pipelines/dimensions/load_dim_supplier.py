"""
بارگذاری بعد تأمین‌کننده (dim_supplier)
از Warehouse.KalaTaminKonandeh + جستجوی نام
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
from sqlalchemy import text
from datetime import datetime
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.logging import setup_logger

logger = setup_logger("dim_supplier")

def run_dim_supplier_pipeline():
    logger.info("=" * 60)
    logger.info("🔄 شروع پایپ‌لاین بعد تأمین‌کننده (dim_supplier)...")
    start_time = datetime.now()
    
    extractor = DataExtractor()
    loader = DataLoader()
    
    try:
        # استخراج تأمین‌کننده‌های یکتا از KalaTaminKonandeh
        query = """
            SELECT DISTINCT ccTaminKonandeh
            FROM Warehouse.KalaTaminKonandeh
            WHERE ccTaminKonandeh IS NOT NULL
            UNION
            SELECT DISTINCT ccTaminKonandeh
            FROM Warehouse.FaktorKharid
            WHERE ccTaminKonandeh IS NOT NULL
            ORDER BY ccTaminKonandeh
        """
        
        logger.info("📥 استخراج تأمین‌کننده‌ها...")
        df = pd.read_sql_query(query, extractor.src_engine)
        
        if df.empty:
            logger.warning("⚠️ هیچ تأمین‌کننده‌ای یافت نشد")
            return 0
        
        # نام‌گذاری پیش‌فرض
        df['NameTaminKonandeh'] = df['ccTaminKonandeh'].apply(
            lambda x: f"تأمین‌کننده {int(x)}"
        )
        
        logger.info(f"📋 {len(df):,} تأمین‌کننده استخراج شد")
        
        # خواندن موجودی
        with loader.tgt_engine.connect() as conn:
            existing = pd.read_sql('SELECT cc_tamin_konandeh FROM dim_supplier', conn)
        
        new_suppliers = df[~df['ccTaminKonandeh'].isin(existing['cc_tamin_konandeh'])]
        
        inserted = 0
        with loader.tgt_engine.begin() as conn:
            for _, row in new_suppliers.iterrows():
                conn.execute(
                    text("""
                        INSERT INTO dim_supplier (cc_tamin_konandeh, name_tamin_konandeh, is_active)
                        VALUES (:cc, :name, TRUE)
                        ON CONFLICT (cc_tamin_konandeh) DO NOTHING
                    """),
                    {
                        "cc": int(row['ccTaminKonandeh']),
                        "name": str(row['NameTaminKonandeh'])[:200]
                    }
                )
                inserted += 1
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ {inserted:,} تأمین‌کننده جدید در {duration:.1f}s")
        return inserted
        
    except Exception as e:
        logger.error(f"❌ خطا: {str(e)[:200]}")
        raise

if __name__ == "__main__":
    run_dim_supplier_pipeline()