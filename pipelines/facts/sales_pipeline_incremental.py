"""
پایپ‌لاین افزایشی fact_sales - نسخه Production
فقط فاکتورهای جدید را پردازش می‌کند
با مپینگ صحیح ccForoshandeh -> ccAfrad
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sqlalchemy import text
from datetime import datetime, timedelta
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.checkpoint import ETLCheckpoint
from core.utils.logging import setup_logger

logger = setup_logger("fact_sales_inc")

def run_fact_sales_incremental(from_date=None, to_date=None, chunk_size=50000):
    """
    بارگذاری افزایشی fact_sales
    
    پارامترها:
    - from_date: تاریخ شروع (اگر None باشد، از checkpoint خوانده می‌شود)
    - to_date: تاریخ پایان (اگر None باشد، امروز)
    - chunk_size: تعداد رکورد در هر چانک
    """
    logger.info("=" * 60)
    logger.info("🔄 شروع پایپ‌لاین افزایشی فروش...")
    start_time = datetime.now()
    
    extractor = DataExtractor()
    loader = DataLoader()
    checkpoint = ETLCheckpoint(loader)
    
    pipeline_name = "fact_sales_incremental"
    
    try:
        # ================================================================
        # 1. تعیین بازه زمانی
        # ================================================================
        if from_date is None:
            last_run = checkpoint.get_last_success(pipeline_name)
            
            if last_run and last_run.get('last_to_value'):
                last_date = str(last_run['last_to_value'])[:10]
                logger.info(f"📌 آخرین تاریخ پردازش شده: {last_date}")
                from_dt = datetime.strptime(last_date, '%Y-%m-%d') - timedelta(days=1)
                from_date = from_dt.strftime('%Y-%m-%d')
            else:
                from_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
                logger.info(f"🆕 اولین اجرا - از {from_date}")
        
        if to_date is None:
            to_date = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"📅 بازه پردازش: {from_date} تا {to_date}")
        
        # ================================================================
        # 2. استخراج هدر فاکتورهای جدید
        # ================================================================
        headers_query = f"""
            SELECT 
                ccDarkhastFaktor, 
                Sal, 
                ccMoshtary, 
                ccForoshandeh, 
                ccMarkazPakhsh, 
                TarikhFaktor
            FROM Sales.DarkhastFaktor
            WHERE TarikhFaktor >= '{from_date}'
              AND TarikhFaktor <= '{to_date}'
            ORDER BY TarikhFaktor
        """
        
        logger.info("📥 استخراج هدر فاکتورها...")
        headers = pd.read_sql_query(headers_query, extractor.src_engine)
        
        if headers.empty:
            logger.info("✅ هیچ فاکتور جدیدی یافت نشد.")
            checkpoint.save_checkpoint(pipeline_name, 'SUCCESS', 0, to_value=to_date)
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"⏱️ زمان اجرا: {duration:.1f} ثانیه")
            return 0
        
        logger.info(f"📋 {len(headers):,} فاکتور جدید یافت شد.")
        
        # ================================================================
        # 3. استخراج سطرهای فاکتور
        # ================================================================
        details_query = f"""
            SELECT 
                d.ccDarkhastFaktor, 
                d.ccKala, 
                d.TedadAdadi, 
                d.TedadKarton,
                d.MablaghForosh, 
                d.MablaghTakhfifFaktor, 
                d.MablaghForoshKhalesKala
            FROM Sales.DarkhastFaktorSatr d
            WHERE d.ccDarkhastFaktor IN (
                SELECT ccDarkhastFaktor 
                FROM Sales.DarkhastFaktor
                WHERE TarikhFaktor >= '{from_date}'
                  AND TarikhFaktor <= '{to_date}'
            )
        """
        
        # ================================================================
        # 4. خواندن ابعاد از PostgreSQL
        # ================================================================
        logger.info("📚 خواندن ابعاد از PostgreSQL...")
        with loader.tgt_engine.connect() as conn:
            dim_product = pd.read_sql(
                'SELECT product_key, cc_kala FROM dim_product WHERE is_active = TRUE', 
                conn
            )
            dim_customer = pd.read_sql(
                'SELECT customer_key, cc_moshtary FROM dim_customer WHERE is_active = TRUE', 
                conn
            )
            dim_employee = pd.read_sql(
                'SELECT employee_key, cc_afrad FROM dim_employee WHERE is_active = TRUE', 
                conn
            )
            dim_center = pd.read_sql(
                'SELECT dist_center_key, cc_markaz_pakhsh FROM dim_dist_center WHERE is_active = TRUE', 
                conn
            )
        
        # ================================================================
        # 5. خواندن مپینگ ccForoshandeh -> ccAfrad از SQL Server
        # ================================================================
        logger.info("📚 خواندن مپینگ فروشنده (ccForoshandeh -> ccAfrad)...")
        mapping_query = """
            SELECT ccForoshandeh, ccAfrad 
            FROM Sales.Foroshandeh
            WHERE ccForoshandeh IS NOT NULL AND ccAfrad IS NOT NULL
        """
        mapping = pd.read_sql_query(mapping_query, extractor.src_engine)
        
        # اصلاح نام ستون‌ها برای هماهنگی با PostgreSQL
        mapping = mapping.rename(columns={'ccAfrad': 'cc_afrad'})
        
        # JOIN مپینگ با dim_employee برای بدست آوردن employee_key
        dim_employee_mapped = pd.merge(
            mapping, 
            dim_employee, 
            on='cc_afrad', 
            how='inner'
        )[['employee_key', 'ccForoshandeh']].drop_duplicates()
        
        logger.info(f"   محصول: {len(dim_product):,} | مشتری: {len(dim_customer):,} | "
                   f"فروشنده: {len(dim_employee_mapped):,} | مرکز: {len(dim_center):,}")
        
        # ================================================================
        # 6. پردازش چانکی سطرهای فاکتور
        # ================================================================
        total_rows = 0
        total_orphan = 0
        total_errors = 0
        chunk_counter = 0
        
        for chunk_details in pd.read_sql_query(details_query, extractor.src_engine, chunksize=chunk_size):
            chunk_counter += 1
            chunk_start = datetime.now()
            
            # 6.1. JOIN سطرها با هدرها
            chunk_headers = headers[headers['ccDarkhastFaktor'].isin(chunk_details['ccDarkhastFaktor'])]
            df = pd.merge(chunk_details, chunk_headers, on='ccDarkhastFaktor', how='inner')
            
            if df.empty:
                logger.debug(f"چانک #{chunk_counter}: خالی پس از JOIN با هدر")
                continue
            
            # 6.2. محاسبه date_key از TarikhFaktor
            df['TarikhFaktor'] = pd.to_datetime(df['TarikhFaktor'])
            df['date_key'] = df['TarikhFaktor'].dt.strftime('%Y%m%d').astype(int)
            
            # 6.3. JOIN با ابعاد (LEFT JOIN برای حفظ orphan ها)
            df = pd.merge(df, dim_product, left_on='ccKala', right_on='cc_kala', how='left')
            df['product_key'] = df['product_key'].fillna(1).astype(int)
            
            df = pd.merge(df, dim_customer, left_on='ccMoshtary', right_on='cc_moshtary', how='left')
            df['customer_key'] = df['customer_key'].fillna(1).astype(int)
            
            df = pd.merge(df, dim_employee_mapped, on='ccForoshandeh', how='left')
            df['employee_key'] = df['employee_key'].fillna(1).astype(int)
            
            df = pd.merge(df, dim_center, left_on='ccMarkazPakhsh', right_on='cc_markaz_pakhsh', how='left')
            df['dist_center_key'] = df['dist_center_key'].fillna(1).astype(int)
            
            # 6.4. محاسبه تعداد orphan
            orphan_in_chunk = len(df[
                (df['product_key'] == 1) | 
                (df['customer_key'] == 1) | 
                (df['employee_key'] == 1) | 
                (df['dist_center_key'] == 1)
            ])
            total_orphan += orphan_in_chunk
            
            if df.empty:
                logger.warning(f"⚠️ چانک #{chunk_counter}: همه رکوردها خالی شدند!")
                continue
            
            # 6.5. ساخت DataFrame نهایی fact_sales
            fact = pd.DataFrame({
                'date_key': df['date_key'],
                'product_key': df['product_key'],
                'customer_key': df['customer_key'],
                'employee_key': df['employee_key'],
                'dist_center_key': df['dist_center_key'],
                'cc_darkhast_faktor': df['ccDarkhastFaktor'],
                'sal_mali': df['Sal'],
                'tedad_faktor': df['TedadAdadi'],
                'tedad_faktor_kartony': df['TedadKarton'],
                'fi_forosh': df['MablaghForosh'],
                'mablagh_takhfif': df['MablaghTakhfifFaktor'],
                'mablagh_khales_satr': df['MablaghForoshKhalesKala']
            })
            
            # 6.6. حذف رکوردهای کاملاً تکراری
            fact = fact.drop_duplicates(['cc_darkhast_faktor', 'sal_mali', 'product_key'])
            
            # 6.7. UPSERT در PostgreSQL
            insert_count = 0
            error_count = 0
            first_error = None
            
            for _, row in fact.iterrows():
                try:
                    with loader.tgt_engine.begin() as conn:
                        conn.execute(
                            text("""
                                INSERT INTO fact_sales (
                                    date_key, product_key, customer_key, employee_key, dist_center_key,
                                    cc_darkhast_faktor, sal_mali, tedad_faktor, tedad_faktor_kartony,
                                    fi_forosh, mablagh_takhfif, mablagh_khales_satr, etl_updated_at
                                ) VALUES (
                                    :date_key, :product_key, :customer_key, :employee_key, :dist_center_key,
                                    :cc_darkhast_faktor, :sal_mali, :tedad_faktor, :tedad_faktor_kartony,
                                    :fi_forosh, :mablagh_takhfif, :mablagh_khales_satr, NOW()
                                )
                                ON CONFLICT (cc_darkhast_faktor, sal_mali, product_key) 
                                DO UPDATE SET
                                    tedad_faktor = EXCLUDED.tedad_faktor,
                                    tedad_faktor_kartony = EXCLUDED.tedad_faktor_kartony,
                                    fi_forosh = EXCLUDED.fi_forosh,
                                    mablagh_takhfif = EXCLUDED.mablagh_takhfif,
                                    mablagh_khales_satr = EXCLUDED.mablagh_khales_satr,
                                    etl_updated_at = NOW()
                            """),
                            {
                                "date_key": int(row['date_key']),
                                "product_key": int(row['product_key']),
                                "customer_key": int(row['customer_key']),
                                "employee_key": int(row['employee_key']),
                                "dist_center_key": int(row['dist_center_key']),
                                "cc_darkhast_faktor": int(row['cc_darkhast_faktor']),
                                "sal_mali": int(row['sal_mali']),
                                "tedad_faktor": float(row['tedad_faktor']),
                                "tedad_faktor_kartony": float(row['tedad_faktor_kartony']),
                                "fi_forosh": float(row['fi_forosh']),
                                "mablagh_takhfif": float(row['mablagh_takhfif']),
                                "mablagh_khales_satr": float(row['mablagh_khales_satr'])
                            }
                        )
                    insert_count += 1
                except Exception as e:
                    error_count += 1
                    if error_count == 1:
                        first_error = str(e)[:300]
                    if error_count <= 3:
                        logger.error(f"❌ خطای UPSERT: {str(e)[:200]}")
            
            total_rows += insert_count
            total_errors += error_count
            
            # 6.8. گزارش پیشرفت چانک
            chunk_duration = (datetime.now() - chunk_start).total_seconds()
            logger.info(f"⚡ چانک #{chunk_counter}: درج={insert_count:,}, خطا={error_count}, "
                       f"orphan={orphan_in_chunk} (زمان: {chunk_duration:.1f}s)")
            
            if error_count > 0 and first_error:
                logger.error(f"   ↳ اولین خطا: {first_error}")
        
        # ================================================================
        # 7. ذخیره checkpoint برای اجرای بعدی
        # ================================================================
        checkpoint.save_checkpoint(pipeline_name, 'SUCCESS', total_rows, to_value=to_date)
        
        # ================================================================
        # 8. گزارش نهایی
        # ================================================================
        duration = (datetime.now() - start_time).total_seconds()
        rows_per_sec = total_rows / duration if duration > 0 else 0
        
        logger.info(f"""
        ╔═══════════════════════════════════════════╗
        ║       ✅ فروش افزایشی لود شد            ║
        ╠═══════════════════════════════════════════╣
        ║ رکوردهای درج شده:    {total_rows:>8,}  ║
        ║ خطاهای UPSERT:       {total_errors:>8,}  ║
        ║ رکوردهای Orphan:     {total_orphan:>8,}  ║
        ║ چانک‌ها:             {chunk_counter:>8}  ║
        ║ زمان کل:          {duration:>8.1f} ثانیه ║
        ║ سرعت:        {rows_per_sec:>10.0f} رکورد/ثانیه ║
        ╚═══════════════════════════════════════════╝
        """)
        
        if total_errors > 0:
            logger.error(f"🚨 {total_errors} خطا در UPSERT! اولین خطا: {first_error}")
        
        return total_rows
        
    except Exception as e:
        logger.error(f"❌ خطا در پایپ‌لاین فروش: {str(e)}", exc_info=True)
        checkpoint.save_checkpoint(pipeline_name, 'FAILED', error_message=str(e)[:500])
        raise


if __name__ == "__main__":
    run_fact_sales_incremental()