"""
پایپ‌لاین Production فروش - استفاده از ابعاد واقعی
"""

import pandas as pd
from sqlalchemy import text
from datetime import datetime, timedelta
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.logging import setup_logger

logger = setup_logger("fact_sales_production")

def run_sales_with_real_dimensions(from_date, to_date):
    """
    بارگذاری fact_sales با JOIN به ابعاد واقعی
    دیگر از دیتای فیک استفاده نمی‌شود!
    """
    logger.info("=" * 60)
    logger.info(f"🔄 شروع پایپ‌لاین فروش با ابعاد واقعی: {from_date} تا {to_date}")
    
    extractor = DataExtractor()
    loader = DataLoader()
    
    try:
        # 1. استخراج فاکتورها
        headers_query = f"""
            SELECT ccDarkhastFaktor, Sal, ccMoshtary, ccForoshandeh, 
                   ccMarkazPakhsh, TarikhFaktor
            FROM Sales.DarkhastFaktor
            WHERE TarikhFaktor >= '{from_date}' 
              AND TarikhFaktor <= '{to_date}'
        """
        headers = pd.read_sql_query(headers_query, extractor.src_engine)
        logger.info(f"📋 {len(headers):,} فاکتور استخراج شد.")
        
        # 2. استخراج سطرها
        details_query = f"""
            SELECT d.ccDarkhastFaktor, d.ccKala, d.TedadAdadi, d.TedadKarton,
                   d.MablaghForosh, d.MablaghTakhfifFaktor, d.MablaghForoshKhalesKala
            FROM Sales.DarkhastFaktorSatr d
            INNER JOIN Sales.DarkhastFaktor h ON d.ccDarkhastFaktor = h.ccDarkhastFaktor
            WHERE h.TarikhFaktor >= '{from_date}' 
              AND h.TarikhFaktor <= '{to_date}'
        """
        
        total_rows = 0
        
        for chunk_num, details_chunk in enumerate(pd.read_sql_query(
            details_query, extractor.src_engine, chunksize=50000
        ), 1):
            
            # 3. JOIN با هدرها
            chunk_headers = headers[headers['ccDarkhastFaktor'].isin(details_chunk['ccDarkhastFaktor'])]
            df = pd.merge(details_chunk, chunk_headers, on='ccDarkhastFaktor', how='inner')
            
            # 4. محاسبه date_key
            df['TarikhFaktor'] = pd.to_datetime(df['TarikhFaktor'])
            df['date_key'] = df['TarikhFaktor'].dt.strftime('%Y%m%d').astype(int)
            
            # 5. دریافت product_key با JOIN (نه دیتای فیک!)
            with loader.tgt_engine.connect() as conn:
                # خواندن mapping کالاها
                product_map = pd.read_sql(
                    'SELECT product_key, ccKala FROM dim_product', conn
                )
                
                # خواندن mapping مشتریان
                customer_map = pd.read_sql(
                    'SELECT customer_key, ccMoshtary FROM dim_customer', conn
                )
                
                # خواندن mapping فروشندگان
                # توجه: در فاکتور از ccForoshandeh استفاده می‌شود که باید به ccAfrad نگاشت شود
                employee_map = pd.read_sql(
                    'SELECT employee_key, ccAfrad FROM dim_employee', conn
                )
                
                # خواندن mapping مراکز پخش
                center_map = pd.read_sql(
                    'SELECT dist_center_key, ccMarkazPakhsh FROM dim_dist_center', conn
                )
            
            # 6. JOIN با ابعاد واقعی
            df = pd.merge(df, product_map, on='ccKala', how='inner')
            df = pd.merge(df, customer_map, on='ccMoshtary', how='inner')
            
            # نگاشت ccForoshandeh به ccAfrad برای بعد employee
            df = df.rename(columns={'ccForoshandeh': 'ccAfrad'})
            df = pd.merge(df, employee_map, on='ccAfrad', how='inner')
            
            df = pd.merge(df, center_map, on='ccMarkazPakhsh', how='inner')
            
            # 7. گزارش رکوردهای orphan (بدون بعد)
            if len(df) < len(details_chunk):
                missing = len(details_chunk) - len(df)
                logger.warning(f"⚠️ چانک #{chunk_num}: {missing} رکورد به دلیل نبود ابعاد حذف شد.")
                logger.warning("   ➜ ابعاد مربوطه را به‌روزرسانی کنید و دوباره تلاش کنید.")
            
            # 8. ساخت fact_sales
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
            
            # 9. حذف تکراری‌ها
            fact = fact.drop_duplicates(
                subset=['cc_darkhast_faktor', 'sal_mali', 'product_key']
            )
            
            # 10. لود
            loader.bulk_copy(df=fact, target_table="fact_sales")
            total_rows += len(fact)
            logger.info(f"⚡ چانک #{chunk_num}: {len(fact):,} رکورد لود شد. مجموع: {total_rows:,}")
        
        logger.info(f"""
        ╔══════════════════════════════════════╗
        ║  ✅ فروش با ابعاد واقعی لود شد     ║
        ╠══════════════════════════════════════╣
        ║ مجموع رکوردها: {total_rows:>11,}  ║
        ╚══════════════════════════════════════╝
        """)
        
        return total_rows
        
    except Exception as e:
        logger.error(f"❌ خطا: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    run_sales_with_real_dimensions('2026-03-21', '2026-04-20')