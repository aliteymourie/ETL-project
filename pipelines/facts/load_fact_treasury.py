"""
Fact Treasury - خزانه‌داری (Incremental + Chunking)
منبع: Treasury.DariaftPardakhtDarkhastFaktor
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

logger = setup_logger("fact_treasury")

def format_date_sql(date_val):
    if date_val is None:
        return (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(date_val, datetime):
        return date_val.strftime('%Y-%m-%d %H:%M:%S')
    return str(date_val)[:19].replace('T', ' ')

def run_fact_treasury_pipeline(chunk_size=50000, max_rows=None):
    """
    Fact Treasury - Incremental Load
    
    پارامترها:
    - chunk_size: تعداد رکورد در هر چانک
    - max_rows: حداکثر رکورد برای تست
    """
    logger.info("=" * 60)
    logger.info("🔄 Fact Treasury - خزانه‌داری")
    start_time = datetime.now()
    
    extractor = DataExtractor()
    loader = DataLoader()
    checkpoint = ETLCheckpoint(loader)
    
    pipeline_name = "fact_treasury"
    
    try:
        # 1. خواندن آخرین TarikhEntry
        last_run = checkpoint.get_last_success(pipeline_name)
        
        if last_run and last_run.get('last_from_value'):
            last_entry = format_date_sql(last_run['last_from_value'])
            logger.info(f"📌 آخرین TarikhEntry: {last_entry}")
        else:
            last_entry = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d %H:%M:%S')
            logger.info("🆕 اولین اجرا")
        
        # 2. استخراج
        limit_clause = f"TOP {max_rows}" if max_rows else ""
        
        query = f"""
            SELECT {limit_clause}
                dpf.ccDariaftPardakhtDarkhastFaktor,
                dpf.ccMoshtary,
                dpf.ccMarkazPakhsh,
                dpf.Mablagh AS MablaghFaktor,
                dpf.TarikhEntry,
                dp.TarikhSanad
            FROM Treasury.DariaftPardakhtDarkhastFaktor dpf
            LEFT JOIN Treasury.DariaftPardakht dp 
                ON dpf.ccDariaftPardakht = dp.ccDariaftPardakht
            WHERE dpf.TarikhEntry >= CONVERT(DATETIME, '{last_entry}', 120)
            ORDER BY dpf.TarikhEntry
        """
        
        logger.info(f"📥 استخراج اسناد (limit={max_rows or 'نامحدود'})...")
        df = pd.read_sql_query(query, extractor.src_engine)
        
        if df.empty:
            logger.info("✅ سند جدیدی یافت نشد")
            checkpoint.save_checkpoint(pipeline_name, 'SUCCESS', 0)
            return 0
        
        logger.info(f"📋 {len(df):,} سند")
        max_entry = format_date_sql(df['TarikhEntry'].max())
        
        # 3. تبدیل
        df['TarikhSanad'] = pd.to_datetime(df['TarikhSanad'], errors='coerce')
        df['date_key'] = df['TarikhSanad'].apply(
            lambda x: int(x.strftime('%Y%m%d')) if pd.notna(x) else 20200101
        )
        
        with loader.tgt_engine.connect() as conn:
            dim_customer = pd.read_sql('SELECT customer_key, cc_moshtary FROM dim_customer', conn)
        
        df = pd.merge(df, dim_customer, left_on='ccMoshtary', right_on='cc_moshtary', how='left')
        df['customer_key'] = df['customer_key'].fillna(1).astype(int)
        
        # 4. ساخت fact
        fact = pd.DataFrame({
            'date_key': df['date_key'],
            'customer_key': df['customer_key'],
            'employee_key': 1,
            'dist_center_key': df['ccMarkazPakhsh'].fillna(1).astype(int),
            'cc_sanad_dariaft': df['ccDariaftPardakhtDarkhastFaktor'],
            'mablagh_sanad': pd.to_numeric(df['MablaghFaktor'], errors='coerce').fillna(0),
            'chek_bargashty': 0,
            'takhfif_naghdi_20': 0,
            'naghs_chek': 0
        })
        
        fact = fact.drop_duplicates(['cc_sanad_dariaft'])
        
        # 5. UPSERT چانکی
        total_inserted = 0
        chunks = [fact.iloc[i:i+chunk_size] for i in range(0, len(fact), chunk_size)]
        
        for chunk_num, chunk in enumerate(chunks, 1):
            inserted = 0
            with loader.tgt_engine.begin() as conn:
                for _, row in chunk.iterrows():
                    try:
                        conn.execute(
                            text("""
                                INSERT INTO fact_treasury (date_key, customer_key, employee_key, 
                                    dist_center_key, cc_sanad_dariaft, mablagh_sanad)
                                VALUES (:d, :c, 1, :ct, :s, :m)
                                ON CONFLICT (cc_sanad_dariaft) DO UPDATE SET
                                    mablagh_sanad = EXCLUDED.mablagh_sanad
                            """),
                            {"d": int(row['date_key']), "c": int(row['customer_key']),
                             "ct": int(row['dist_center_key']), "s": int(row['cc_sanad_dariaft']),
                             "m": float(row['mablagh_sanad'])}
                        )
                        inserted += 1
                    except:
                        pass
            
            total_inserted += inserted
            logger.info(f"⚡ چانک #{chunk_num}/{len(chunks)}: {inserted:,} (مجموع: {total_inserted:,})")
        
        # 6. Checkpoint
        checkpoint.save_checkpoint(pipeline_name, 'SUCCESS', total_inserted, from_value=max_entry)
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ {total_inserted:,} رکورد در {duration:.1f}s")
        return total_inserted
        
    except Exception as e:
        logger.error(f"❌ {str(e)[:200]}")
        checkpoint.save_checkpoint(pipeline_name, 'FAILED', error_message=str(e)[:500])
        raise

if __name__ == "__main__":
    run_fact_treasury_pipeline(max_rows=100000)