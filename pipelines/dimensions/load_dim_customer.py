"""
پایپ‌لاین افزایشی بعد مشتری (dim_customer) - نسخه Incremental
فقط مشتریان جدید/تغییر کرده را پردازش می‌کند
"""

import pandas as pd
from sqlalchemy import text
from datetime import datetime, timedelta
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.checkpoint import ETLCheckpoint
from core.utils.logging import setup_logger

logger = setup_logger("dim_customer_inc")

def clean_text(text, max_length=None):
    if pd.isna(text) or text is None:
        return ''
    cleaned = str(text).replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
    if max_length and len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    return cleaned

def format_date_sql(date_val):
    if date_val is None:
        return (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(date_val, datetime):
        return date_val.strftime('%Y-%m-%d %H:%M:%S')
    return str(date_val)[:19].replace('T', ' ')

def run_dim_customer_pipeline():
    """
    بارگذاری افزایشی بعد مشتری
    فقط مشتریانی که ModifiedDate آنها جدیدتر است
    """
    logger.info("=" * 60)
    logger.info("🔄 شروع پایپ‌لاین افزایشی بعد مشتری (dim_customer)...")
    start_time = datetime.now()
    
    extractor = DataExtractor()
    loader = DataLoader()
    checkpoint = ETLCheckpoint(loader)
    
    pipeline_name = "dim_customer"
    
    try:
        # 1. خواندن آخرین ModifiedDate
        last_run = checkpoint.get_last_success(pipeline_name)
        
        if last_run and last_run.get('last_from_value'):
            last_modified = format_date_sql(last_run['last_from_value'])
            logger.info(f"📌 آخرین ModifiedDate: {last_modified}")
        else:
            last_modified = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d %H:%M:%S')
            logger.info("🆕 اولین اجرا - پردازش کل داده‌ها")
        
        # 2. استخراج فقط مشتریان تغییر کرده
        # چک می‌کنیم آیا ModifiedDate در Sales.Moshtary وجود دارد
        query = f"""
            SELECT 
                ccMoshtary,
                NameMoshtary,
                CodePosty,
                CodeEghtesady,
                CodeNoeShakhsiat,
                CodeNoeVosolAzMoshtary,
                ccMahaleh,
                CodeVazeiat,
                CodeMoshtaryOld,
                ModifiedDate
            FROM Sales.Moshtary
            WHERE ccMoshtary IS NOT NULL
              AND ModifiedDate >= CONVERT(DATETIME, '{last_modified}', 120)
            ORDER BY ModifiedDate
        """
        
        logger.info("📥 در حال استخراج مشتریان تغییر کرده...")
        
        try:
            df_src = pd.read_sql_query(query, extractor.src_engine)
        except Exception as e:
            # اگر ModifiedDate وجود نداشت، از روش جایگزین استفاده کن
            logger.warning(f"⚠️ ستون ModifiedDate یافت نشد: {str(e)[:80]}")
            logger.info("🔄 استفاده از روش جایگزین: مقایسه با موجودی")
            
            # همه را بخوان
            query_all = """
                SELECT 
                    ccMoshtary, NameMoshtary, CodePosty, CodeEghtesady,
                    CodeNoeShakhsiat, CodeNoeVosolAzMoshtary, ccMahaleh,
                    CodeVazeiat, CodeMoshtaryOld
                FROM Sales.Moshtary
                WHERE ccMoshtary IS NOT NULL
                ORDER BY ccMoshtary
            """
            df_src = pd.read_sql_query(query_all, extractor.src_engine)
        
        if df_src.empty:
            logger.info("✅ هیچ مشتری جدید/تغییر کرده‌ای یافت نشد")
            checkpoint.save_checkpoint(pipeline_name, 'SUCCESS', 0)
            return 0
        
        logger.info(f"📋 {len(df_src):,} مشتری تغییر کرده")
        
        # ذخیره آخرین ModifiedDate
        if 'ModifiedDate' in df_src.columns:
            max_modified = format_date_sql(df_src['ModifiedDate'].max())
        else:
            max_modified = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 3. پاکسازی و تبدیل
        df_dim = pd.DataFrame()
        df_dim['cc_moshtary'] = df_src['ccMoshtary'].astype(int)
        df_dim['name_moshtary'] = df_src['NameMoshtary'].apply(lambda x: clean_text(x, 256))
        df_dim['cc_mantagheh'] = pd.to_numeric(df_src['ccMahaleh'], errors='coerce')
        df_dim['cc_shahr_moshtary'] = pd.to_numeric(df_src['CodePosty'], errors='coerce')
        df_dim['shomareh_hesab_new'] = df_src['CodeEghtesady'].apply(lambda x: clean_text(x, 30))
        df_dim['mablagh_etebar'] = 0.0
        df_dim['is_active'] = df_src['CodeVazeiat'].apply(lambda x: True if x == 3 else False)
        
        # 4. UPSERT (درج یا به‌روزرسانی فقط برای تغییر کرده‌ها)
        total_processed = 0
        
        with loader.tgt_engine.begin() as conn:
            for _, row in df_dim.iterrows():
                try:
                    conn.execute(
                        text("""
                            INSERT INTO dim_customer (cc_moshtary, name_moshtary, 
                                cc_mantagheh, cc_shahr_moshtary, shomareh_hesab_new,
                                mablagh_etebar, is_active, updated_at)
                            VALUES (:cc, :name, :mantagheh, :shahr, :hesab, :etebar, :active, NOW())
                            ON CONFLICT (cc_moshtary) DO UPDATE SET
                                name_moshtary = EXCLUDED.name_moshtary,
                                cc_mantagheh = EXCLUDED.cc_mantagheh,
                                cc_shahr_moshtary = EXCLUDED.cc_shahr_moshtary,
                                shomareh_hesab_new = EXCLUDED.shomareh_hesab_new,
                                is_active = EXCLUDED.is_active,
                                updated_at = NOW()
                        """),
                        {
                            "cc": int(row['cc_moshtary']),
                            "name": row['name_moshtary'],
                            "mantagheh": int(row['cc_mantagheh']) if pd.notna(row['cc_mantagheh']) else None,
                            "shahr": int(row['cc_shahr_moshtary']) if pd.notna(row['cc_shahr_moshtary']) else None,
                            "hesab": row['shomareh_hesab_new'] if row['shomareh_hesab_new'] else None,
                            "etebar": float(row['mablagh_etebar']),
                            "active": bool(row['is_active'])
                        }
                    )
                    total_processed += 1
                except Exception as e:
                    logger.debug(f"⚠️ خطا در مشتری {row['cc_moshtary']}: {str(e)[:80]}")
        
        # 5. Checkpoint
        checkpoint.save_checkpoint(pipeline_name, 'SUCCESS', total_processed, from_value=max_modified)
        
        # 6. گزارش
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"""
        ╔══════════════════════════════════════╗
        ║  ✅ بعد مشتری (افزایشی) لود شد     ║
        ╠══════════════════════════════════════╣
        ║ پردازش شده: {total_processed:>14,}  ║
        ║ زمان: {duration:>17.1f} ثانیه ║
        ╚══════════════════════════════════════╝
        """)
        
        return total_processed
        
    except Exception as e:
        logger.error(f"❌ خطا: {str(e)[:200]}")
        checkpoint.save_checkpoint(pipeline_name, 'FAILED', error_message=str(e)[:500])
        raise


if __name__ == "__main__":
    run_dim_customer_pipeline()