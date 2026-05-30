"""
Fact Asset - اموال (Incremental + Chunking)
منبع: AssetAccounting.Amval
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

logger = setup_logger("fact_asset")

def format_date_sql(date_val):
    if date_val is None:
        return (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(date_val, datetime):
        return date_val.strftime('%Y-%m-%d %H:%M:%S')
    return str(date_val)[:19].replace('T', ' ')

def run_fact_asset_pipeline(chunk_size=50000, max_rows=None):
    """
    Fact Asset - Incremental Load
    
    پارامترها:
    - chunk_size: تعداد رکورد در هر چانک
    - max_rows: حداکثر رکورد برای تست
    """
    logger.info("=" * 60)
    logger.info("🔄 Fact Asset - اموال")
    start_time = datetime.now()
    
    extractor = DataExtractor()
    loader = DataLoader()
    checkpoint = ETLCheckpoint(loader)
    
    pipeline_name = "fact_asset"
    
    try:
        # 1. خواندن آخرین ModifiedDate
        last_run = checkpoint.get_last_success(pipeline_name)
        
        if last_run and last_run.get('last_from_value'):
            last_modified = format_date_sql(last_run['last_from_value'])
            logger.info(f"📌 آخرین ModifiedDate: {last_modified}")
        else:
            last_modified = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d %H:%M:%S')
            logger.info("🆕 اولین اجرا")
        
        # 2. استخراج
        limit_clause = f"TOP {max_rows}" if max_rows else ""
        
        query = f"""
            SELECT {limit_clause}
                ccAmval, ccJamdar, TarikhBahrehbardary,
                GheymatTamamShodeh, ArzeshDaftary, EstehlakAnbashteh,
                ModifiedDate
            FROM AssetAccounting.Amval
            WHERE ccAmval IS NOT NULL
              AND ModifiedDate >= CONVERT(DATETIME, '{last_modified}', 120)
            ORDER BY ModifiedDate
        """
        
        logger.info(f"📥 استخراج اموال (limit={max_rows or 'نامحدود'})...")
        df = pd.read_sql_query(query, extractor.src_engine)
        
        if df.empty:
            logger.info("✅ تغییر جدیدی یافت نشد")
            checkpoint.save_checkpoint(pipeline_name, 'SUCCESS', 0)
            return 0
        
        logger.info(f"📋 {len(df):,} قلم اموال")
        max_modified = format_date_sql(df['ModifiedDate'].max())
        
        # 3. تبدیل
        df['TarikhBahrehbardary'] = pd.to_datetime(df['TarikhBahrehbardary'], errors='coerce')
        df['date_key'] = df['TarikhBahrehbardary'].apply(
            lambda x: int(x.strftime('%Y%m%d')) if pd.notna(x) else 20200101
        )
        
        fact = pd.DataFrame({
            'date_key': df['date_key'],
            'dist_center_key': 1,
            'employee_key': df['ccJamdar'].fillna(1).astype(int),
            'cc_amval': df['ccAmval'],
            'gheymat_tamam_shodeh': pd.to_numeric(df['GheymatTamamShodeh'], errors='coerce').fillna(0),
            'arzesh_daftary': pd.to_numeric(df['ArzeshDaftary'], errors='coerce').fillna(0),
            'estehlak_anbashteh': pd.to_numeric(df['EstehlakAnbashteh'], errors='coerce').fillna(0),
            'depreciation_rate': 0
        })
        
        fact = fact.drop_duplicates(['date_key', 'cc_amval'])
        
        # 4. UPSERT چانکی
        total_inserted = 0
        chunks = [fact.iloc[i:i+chunk_size] for i in range(0, len(fact), chunk_size)]
        
        for chunk_num, chunk in enumerate(chunks, 1):
            inserted = 0
            with loader.tgt_engine.begin() as conn:
                for _, row in chunk.iterrows():
                    try:
                        conn.execute(
                            text("""
                                INSERT INTO fact_asset (date_key, dist_center_key, employee_key, cc_amval,
                                    gheymat_tamam_shodeh, arzesh_daftary, estehlak_anbashteh, depreciation_rate)
                                VALUES (:d, 1, :e, :a, :g, :ar, :es, 0)
                                ON CONFLICT (date_key, cc_amval) DO UPDATE SET
                                    arzesh_daftary = EXCLUDED.arzesh_daftary,
                                    estehlak_anbashteh = EXCLUDED.estehlak_anbashteh
                            """),
                            {"d": int(row['date_key']), "e": int(row['employee_key']),
                             "a": int(row['cc_amval']), "g": float(row['gheymat_tamam_shodeh']),
                             "ar": float(row['arzesh_daftary']), "es": float(row['estehlak_anbashteh'])}
                        )
                        inserted += 1
                    except:
                        pass
            
            total_inserted += inserted
            logger.info(f"⚡ چانک #{chunk_num}/{len(chunks)}: {inserted:,} (مجموع: {total_inserted:,})")
        
        # 5. Checkpoint
        checkpoint.save_checkpoint(pipeline_name, 'SUCCESS', total_inserted, from_value=max_modified)
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ {total_inserted:,} رکورد در {duration:.1f}s")
        return total_inserted
        
    except Exception as e:
        logger.error(f"❌ {str(e)[:200]}")
        checkpoint.save_checkpoint(pipeline_name, 'FAILED', error_message=str(e)[:500])
        raise

if __name__ == "__main__":
    run_fact_asset_pipeline(max_rows=100000)