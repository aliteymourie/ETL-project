"""
Fact Inventory - موجودی روزانه (Incremental + Chunking)
منبع: Warehouse.MojodyRooz
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
from sqlalchemy import text
from datetime import datetime, timedelta
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.checkpoint import ETLCheckpoint
from core.utils.logging import setup_logger

logger = setup_logger("fact_inventory")

def run_fact_inventory_pipeline(from_date=None, to_date=None, chunk_size=50000, max_rows=None):
    """
    Fact Inventory - Incremental Load
    
    پارامترها:
    - from_date: تاریخ شروع (None = از checkpoint)
    - to_date: تاریخ پایان (None = امروز)
    - chunk_size: تعداد رکورد در هر چانک
    - max_rows: حداکثر رکورد برای تست (None = نامحدود)
    """
    logger.info("=" * 60)
    logger.info("🔄 Fact Inventory - موجودی روزانه")
    start_time = datetime.now()
    
    extractor = DataExtractor()
    loader = DataLoader()
    checkpoint = ETLCheckpoint(loader)
    
    pipeline_name = "fact_inventory"
    
    try:
        # 1. تعیین بازه زمانی
        if from_date is None:
            last_run = checkpoint.get_last_success(pipeline_name)
            if last_run and last_run.get('last_to_value'):
                from_date = str(last_run['last_to_value'])[:10]
                logger.info(f"📌 آخرین تاریخ: {from_date}")
            else:
                from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                logger.info(f"🆕 اولین اجرا")
        
        if to_date is None:
            to_date = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"📅 بازه: {from_date} تا {to_date}")
        
        # 2. استخراج با محدودیت اختیاری
        limit_clause = f"TOP {max_rows}" if max_rows else ""
        
        query = f"""
            SELECT {limit_clause}
                Tarikh, ccKala, ccMarkazPakhsh, Mojody
            FROM Warehouse.MojodyRooz
            WHERE Tarikh >= '{from_date}'
              AND Tarikh <= '{to_date}'
              AND ccKala IS NOT NULL
            ORDER BY Tarikh
        """
        
        logger.info(f"📥 استخراج موجودی (limit={max_rows or 'نامحدود'})...")
        df = pd.read_sql_query(query, extractor.src_engine)
        
        if df.empty:
            logger.info("✅ موجودی جدیدی یافت نشد")
            checkpoint.save_checkpoint(pipeline_name, 'SUCCESS', 0, to_value=to_date)
            return 0
        
        logger.info(f"📋 {len(df):,} رکورد استخراج شد")
        
        # 3. خواندن ابعاد یکبار
        with loader.tgt_engine.connect() as conn:
            dim_product = pd.read_sql('SELECT product_key, cc_kala FROM dim_product', conn)
            dim_center = pd.read_sql('SELECT dist_center_key, cc_markaz_pakhsh FROM dim_dist_center', conn)
        
        # 4. تبدیل
        df['Tarikh'] = pd.to_datetime(df['Tarikh'])
        df['date_key'] = df['Tarikh'].dt.strftime('%Y%m%d').astype(int)
        
        # JOIN با ابعاد - استفاده از left_on/right_on
        df = pd.merge(df, dim_product, left_on='ccKala', right_on='cc_kala', how='left')
        df['product_key'] = df['product_key'].fillna(1).astype(int)
        
        df = pd.merge(df, dim_center, left_on='ccMarkazPakhsh', right_on='cc_markaz_pakhsh', how='left')
        df['dist_center_key'] = df['dist_center_key'].fillna(1).astype(int)
        
        # 5. ساخت fact
        fact = pd.DataFrame({
            'date_key': df['date_key'],
            'product_key': df['product_key'],
            'dist_center_key': df['dist_center_key'],
            'cc_anbar': 0,
            'mojody_anbar_tedady': pd.to_numeric(df['Mojody'], errors='coerce').fillna(0),
            'mojody_anbar_kartony': 0,
            'mojody_anbar_rialy': 0,
            'faktor_tozi_nashodeh_rialy': 0,
            'tedad_aghlam_nazdik': 0
        })
        
        # 6. حذف تکراری
        fact = fact.drop_duplicates(['date_key', 'product_key', 'dist_center_key'])
        
        # 7. UPSERT چانکی
        total_inserted = 0
        chunks = [fact.iloc[i:i+chunk_size] for i in range(0, len(fact), chunk_size)]
        
        for chunk_num, chunk in enumerate(chunks, 1):
            inserted = 0
            with loader.tgt_engine.begin() as conn:
                for _, row in chunk.iterrows():
                    try:
                        conn.execute(
                            text("""
                                INSERT INTO fact_inventory (date_key, product_key, dist_center_key, cc_anbar,
                                    mojody_anbar_tedady)
                                VALUES (:d, :p, :c, 0, :m)
                                ON CONFLICT (date_key, product_key, dist_center_key, cc_anbar)
                                DO UPDATE SET mojody_anbar_tedady = EXCLUDED.mojody_anbar_tedady
                            """),
                            {"d": int(row['date_key']), "p": int(row['product_key']),
                             "c": int(row['dist_center_key']), "m": float(row['mojody_anbar_tedady'])}
                        )
                        inserted += 1
                    except:
                        pass
            
            total_inserted += inserted
            logger.info(f"⚡ چانک #{chunk_num}/{len(chunks)}: {inserted:,} رکورد (مجموع: {total_inserted:,})")
        
        # 8. Checkpoint
        checkpoint.save_checkpoint(pipeline_name, 'SUCCESS', total_inserted, to_value=to_date)
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ {total_inserted:,} رکورد در {duration:.1f}s ({total_inserted/duration:.0f} r/s)")
        return total_inserted
        
    except Exception as e:
        logger.error(f"❌ {str(e)[:200]}")
        checkpoint.save_checkpoint(pipeline_name, 'FAILED', error_message=str(e)[:500])
        raise

if __name__ == "__main__":
    # تست با ۱۰۰,۰۰۰ رکورد
    run_fact_inventory_pipeline(max_rows=100000)