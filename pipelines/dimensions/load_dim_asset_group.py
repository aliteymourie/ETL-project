"""
بارگذاری بعد گروه دارایی (dim_asset_group) از AssetAccounting.GorohDaraee
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
from sqlalchemy import text
from datetime import datetime
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.logging import setup_logger

logger = setup_logger("dim_asset_group")

def run_dim_asset_group_pipeline():
    logger.info("=" * 60)
    logger.info("🔄 شروع پایپ‌لاین بعد گروه دارایی (dim_asset_group)...")
    start_time = datetime.now()
    
    extractor = DataExtractor()
    loader = DataLoader()
    
    try:
        query = """
            SELECT ccGorohDaraee, ccGorohAslyDaraee
            FROM AssetAccounting.GorohDaraee
            WHERE ccGorohDaraee IS NOT NULL
            ORDER BY ccGorohDaraee
        """
        
        logger.info("📥 استخراج گروه‌های دارایی...")
        df = pd.read_sql_query(query, extractor.src_engine)
        
        if df.empty:
            logger.warning("⚠️ هیچ گروه دارایی یافت نشد")
            return 0
        
        df['NameGorohDaraee'] = df['ccGorohDaraee'].apply(
            lambda x: f"گروه دارایی {int(x)}"
        )
        
        logger.info(f"📋 {len(df):,} گروه دارایی استخراج شد")
        
        with loader.tgt_engine.connect() as conn:
            existing = pd.read_sql('SELECT cc_goroh_daraee FROM dim_asset_group', conn)
        
        new_groups = df[~df['ccGorohDaraee'].isin(existing['cc_goroh_daraee'])]
        
        inserted = 0
        with loader.tgt_engine.begin() as conn:
            for _, row in new_groups.iterrows():
                conn.execute(
                    text("""
                        INSERT INTO dim_asset_group (cc_goroh_daraee, name_goroh_daraee, 
                            cc_goroh_asly_daraee, is_active)
                        VALUES (:cc, :name, :parent, TRUE)
                        ON CONFLICT (cc_goroh_daraee) DO NOTHING
                    """),
                    {
                        "cc": int(row['ccGorohDaraee']),
                        "name": str(row['NameGorohDaraee'])[:200],
                        "parent": int(row['ccGorohAslyDaraee']) if pd.notna(row['ccGorohAslyDaraee']) else None
                    }
                )
                inserted += 1
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ {inserted:,} گروه دارایی جدید در {duration:.1f}s")
        return inserted
        
    except Exception as e:
        logger.error(f"❌ خطا: {str(e)[:200]}")
        raise

if __name__ == "__main__":
    run_dim_asset_group_pipeline()