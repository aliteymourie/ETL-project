"""
بارگذاری بعد انبار (dim_warehouse) از Warehouse.Anbar
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
from sqlalchemy import text
from datetime import datetime
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.logging import setup_logger

logger = setup_logger("dim_warehouse")

def run_dim_warehouse_pipeline():
    logger.info("=" * 60)
    logger.info("🔄 شروع پایپ‌لاین بعد انبار (dim_warehouse)...")
    start_time = datetime.now()
    
    extractor = DataExtractor()
    loader = DataLoader()
    
    try:
        query = """
            SELECT ccAnbar, NameAnbar, ccMarkazPakhsh, CodeNoeAnbar, 
                   ccAddress, CodeVazeiat
            FROM Warehouse.Anbar
            WHERE ccAnbar IS NOT NULL
            ORDER BY ccAnbar
        """
        
        logger.info("📥 استخراج انبارها...")
        df = pd.read_sql_query(query, extractor.src_engine)
        
        if df.empty:
            logger.warning("⚠️ هیچ انباری یافت نشد")
            return 0
        
        logger.info(f"📋 {len(df):,} انبار استخراج شد")
        
        # خواندن موجودی
        with loader.tgt_engine.connect() as conn:
            existing = pd.read_sql('SELECT cc_anbar FROM dim_warehouse', conn)
        
        new_warehouses = df[~df['ccAnbar'].isin(existing['cc_anbar'])]
        
        inserted = 0
        with loader.tgt_engine.begin() as conn:
            for _, row in new_warehouses.iterrows():
                conn.execute(
                    text("""
                        INSERT INTO dim_warehouse (cc_anbar, name_anbar, cc_markaz_pakhsh, 
                            code_noe_anbar, cc_address, is_active)
                        VALUES (:cc, :name, :markaz, :noe, :address, :active)
                        ON CONFLICT (cc_anbar) DO NOTHING
                    """),
                    {
                        "cc": int(row['ccAnbar']),
                        "name": str(row['NameAnbar'])[:200] if pd.notna(row['NameAnbar']) else 'نامشخص',
                        "markaz": int(row['ccMarkazPakhsh']) if pd.notna(row['ccMarkazPakhsh']) else None,
                        "noe": int(row['CodeNoeAnbar']) if pd.notna(row['CodeNoeAnbar']) else None,
                        "address": int(row['ccAddress']) if pd.notna(row['ccAddress']) else None,
                        "active": row['CodeVazeiat'] == 3 if pd.notna(row['CodeVazeiat']) else True
                    }
                )
                inserted += 1
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ {inserted:,} انبار جدید در {duration:.1f}s")
        return inserted
        
    except Exception as e:
        logger.error(f"❌ خطا: {str(e)[:200]}")
        raise

if __name__ == "__main__":
    run_dim_warehouse_pipeline()