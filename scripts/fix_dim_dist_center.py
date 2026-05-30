"""
رفع مشکل orphan در fact_treasury
به‌روزرسانی dim_dist_center با مراکز پخش جدید از Treasury
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sqlalchemy import text
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.logging import setup_logger

logger = setup_logger("fix_dist_center")

def fix_dim_dist_center():
    """
    اضافه کردن مراکز پخشی که در Treasury.DariaftPardakht هستند
    ولی در dim_dist_center وجود ندارند
    """
    logger.info("=" * 60)
    logger.info("🔧 رفع مشکل orphan در fact_treasury")
    
    extractor = DataExtractor()
    loader = DataLoader()
    
    try:
        # 1. خواندن مراکز پخش یکتا از SQL Server
        query = """
            SELECT DISTINCT ccMarkazPakhsh
            FROM Treasury.DariaftPardakht
            WHERE ccMarkazPakhsh IS NOT NULL
            ORDER BY ccMarkazPakhsh
        """
        
        logger.info("📥 خواندن مراکز پخش از Treasury...")
        df_src = pd.read_sql_query(query, extractor.src_engine)
        
        if df_src.empty:
            logger.info("✅ مرکز پخشی در Treasury نیست")
            return 0
        
        logger.info(f"📋 {len(df_src):,} مرکز پخش یکتا در Treasury")
        
        # 2. خواندن موجودی فعلی dim_dist_center از PostgreSQL
        with loader.tgt_engine.connect() as conn:
            existing = pd.read_sql('SELECT cc_markaz_pakhsh FROM dim_dist_center', conn)
        
        logger.info(f"📊 {len(existing):,} مرکز پخش در dim_dist_center موجود است")
        
        # 3. پیدا کردن مراکز جدید
        new_centers = df_src[~df_src['ccMarkazPakhsh'].isin(existing['cc_markaz_pakhsh'])]
        
        if new_centers.empty:
            logger.info("✅ همه مراکز پخش در dim_dist_center هستند")
            return 0
        
        logger.info(f"🆕 {len(new_centers):,} مرکز پخش جدید باید اضافه شود")
        
        # 4. اضافه کردن به dim_dist_center
        inserted = 0
        with loader.tgt_engine.begin() as conn:
            for _, row in new_centers.iterrows():
                try:
                    conn.execute(
                        text("""
                            INSERT INTO dim_dist_center (cc_markaz_pakhsh, name_markaz_pakhsh, is_active)
                            VALUES (:code, :name, TRUE)
                            ON CONFLICT (cc_markaz_pakhsh) DO UPDATE SET
                                name_markaz_pakhsh = :name,
                                is_active = TRUE,
                                updated_at = NOW()
                        """),
                        {
                            "code": int(row['ccMarkazPakhsh']),
                            "name": f"مرکز پخش {int(row['ccMarkazPakhsh'])}"
                        }
                    )
                    inserted += 1
                except Exception as e:
                    logger.debug(f"⚠️ خطا در {row['ccMarkazPakhsh']}: {str(e)[:80]}")
        
        logger.info(f"✅ {inserted:,} مرکز پخش جدید اضافه شد")
        
        # 5. حالا fact_treasury را با dist_center_key درست آپدیت کن
        logger.info("\n🔄 به‌روزرسانی fact_treasury با dist_center_key صحیح...")
        
        # خواندن مپینگ جدید
        with loader.tgt_engine.connect() as conn:
            dim_center = pd.read_sql('SELECT dist_center_key, cc_markaz_pakhsh FROM dim_dist_center', conn)
        
        # خواندن fact_treasury که dist_center_key=1 دارند
        with loader.tgt_engine.connect() as conn:
            orphan_facts = pd.read_sql("""
                SELECT cc_sanad_dariaft, dist_center_key 
                FROM fact_treasury 
                WHERE dist_center_key = 1
            """, conn)
        
        if len(orphan_facts) > 0:
            logger.info(f"   {len(orphan_facts):,} رکورد orphan در fact_treasury")
            
            # باید از SQL Server دوباره ccMarkazPakhsh را بخوانیم
            # اما چون کلید اصلی cc_sanad_dariaft است، نمی‌توانیم مستقیماً آپدیت کنیم
            # راه‌حل: دوباره fact_treasury را با dist_center_key درست لود کن
            
            logger.info("   💡 پیشنهاد: fact_treasury را دوباره اجرا کن:")
            logger.info("   python -m pipelines.facts.load_fact_treasury")
        
        return inserted
        
    except Exception as e:
        logger.error(f"❌ خطا: {str(e)[:200]}")
        raise

if __name__ == "__main__":
    fix_dim_dist_center()