"""
پایپ‌لاین بارگذاری بعد مرکز پخش - استخراج از فاکتورها چون جدول مجزا ندارد
"""

import pandas as pd
from sqlalchemy import text
from datetime import datetime
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.logging import setup_logger

logger = setup_logger("dim_dist_center")

def run_dim_dist_center_pipeline():
    """
    استخراج مراکز پخش منحصر به فرد از جدول فاکتورها
    """
    logger.info("=" * 60)
    logger.info("🔄 شروع پایپ‌لاین بعد مرکز پخش...")
    start_time = datetime.now()
    
    extractor = DataExtractor()
    loader = DataLoader()
    
    try:
        # استخراج مراکز پخش یکتا از فاکتورها
        query = """
            SELECT DISTINCT 
                ccMarkazPakhsh,
                CAST(ccMarkazPakhsh AS VARCHAR) + N' - مرکز پخش' AS NameMarkazPakhsh
            FROM Sales.DarkhastFaktor
            WHERE ccMarkazPakhsh IS NOT NULL
            ORDER BY ccMarkazPakhsh
        """
        
        logger.info("📥 در حال استخراج مراکز پخش از فاکتورها...")
        df_src = pd.read_sql_query(query, extractor.src_engine)
        
        if df_src.empty:
            logger.warning("⚠️ هیچ مرکز پخشی یافت نشد.")
            return 0
        
        logger.info(f"📋 {len(df_src):,} مرکز پخش یکتا استخراج شد.")
        
        # پاکسازی
        df_dim = pd.DataFrame()
        df_dim['cc_markaz_pakhsh'] = df_src['ccMarkazPakhsh'].astype(int)
        df_dim['name_markaz_pakhsh'] = df_src['NameMarkazPakhsh'].astype(str).str.strip()
        df_dim['is_active'] = True
        
        # خواندن موجود
        with loader.tgt_engine.connect() as conn:
            existing = pd.read_sql(
                'SELECT dist_center_key, cc_markaz_pakhsh FROM dim_dist_center', 
                conn
            )
        
        new_centers = df_dim[~df_dim['cc_markaz_pakhsh'].isin(existing['cc_markaz_pakhsh'])]
        
        total_new = 0
        with loader.tgt_engine.begin() as conn:
            for _, row in new_centers.iterrows():
                try:
                    conn.execute(
                        text("""
                            INSERT INTO dim_dist_center (cc_markaz_pakhsh, name_markaz_pakhsh, is_active)
                            VALUES (:code, :name, TRUE)
                            ON CONFLICT (cc_markaz_pakhsh) DO NOTHING
                        """),
                        {"code": int(row['cc_markaz_pakhsh']), "name": row['name_markaz_pakhsh']}
                    )
                    total_new += 1
                except Exception:
                    pass
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"""
        ╔══════════════════════════════════════╗
        ║  ✅ بعد مرکز پخش با موفقیت لود شد  ║
        ╠══════════════════════════════════════╣
        ║ جدید: {total_new:>20,}  ║
        ║ زمان: {duration:>17.1f} ثانیه ║
        ╚══════════════════════════════════════╝
        """)
        
        return total_new
        
    except Exception as e:
        logger.error(f"❌ خطا: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    run_dim_dist_center_pipeline()