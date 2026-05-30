"""
Backfill کل تاریخچه فروش - برای اجرا روی سرور اصلی
۱۸ میلیون رکورد را به صورت پارتیشن‌بندی شده منتقل می‌کند

استفاده:
  python scripts/backfill_sales.py --start 2021-03-21 --end 2026-05-25 --workers 4
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import pandas as pd
from sqlalchemy import text
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.checkpoint import ETLCheckpoint
from core.utils.logging import setup_logger

logger = setup_logger("backfill_sales")


def generate_monthly_ranges(start_date, end_date):
    """
    تولید بازه‌های ماهانه برای پردازش موازی
    مثال: [
        ('2021-03-21', '2021-04-20'),
        ('2021-04-21', '2021-05-21'),
        ...
    ]
    """
    ranges = []
    current = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    while current < end:
        # ماه بعد (تقریبی - ۳۰ روز)
        next_month = current + timedelta(days=30)
        if next_month > end:
            next_month = end
        
        ranges.append((
            current.strftime('%Y-%m-%d'),
            next_month.strftime('%Y-%m-%d')
        ))
        current = next_month + timedelta(days=1)
    
    return ranges


def backfill_month(month_range):
    """
    بارگذاری یک ماه از داده‌ها
    مناسب برای اجرای موازی
    """
    from_date, to_date = month_range
    
    logger.info(f"📅 شروع بازه: {from_date} تا {to_date}")
    
    extractor = DataExtractor()
    loader = DataLoader()
    
    try:
        # 1. استخراج هدرها
        headers_query = f"""
            SELECT ccDarkhastFaktor, Sal, ccMoshtary, ccForoshandeh, 
                   ccMarkazPakhsh, TarikhFaktor
            FROM Sales.DarkhastFaktor
            WHERE TarikhFaktor >= '{from_date}'
              AND TarikhFaktor <= '{to_date}'
        """
        headers = pd.read_sql_query(headers_query, extractor.src_engine)
        
        if headers.empty:
            logger.info(f"   ⏭️ بازه {from_date} تا {to_date}: بدون داده")
            return 0
        
        # 2. استخراج سطرها
        details_query = f"""
            SELECT d.ccDarkhastFaktor, d.ccKala, d.TedadAdadi, d.TedadKarton,
                   d.MablaghForosh, d.MablaghTakhfifFaktor, d.MablaghForoshKhalesKala
            FROM Sales.DarkhastFaktorSatr d
            WHERE d.ccDarkhastFaktor IN (
                SELECT ccDarkhastFaktor FROM Sales.DarkhastFaktor
                WHERE TarikhFaktor >= '{from_date}'
                  AND TarikhFaktor <= '{to_date}'
            )
        """
        
        # 3. خواندن ابعاد
        with loader.tgt_engine.connect() as conn:
            dim_product = pd.read_sql('SELECT product_key, cc_kala FROM dim_product', conn)
            dim_customer = pd.read_sql('SELECT customer_key, cc_moshtary FROM dim_customer', conn)
            dim_employee = pd.read_sql('SELECT employee_key, cc_afrad FROM dim_employee', conn)
            dim_center = pd.read_sql('SELECT dist_center_key, cc_markaz_pakhsh FROM dim_dist_center', conn)
        
        # 4. مپینگ فروشنده
        mapping_query = """
            SELECT ccForoshandeh, ccAfrad FROM Sales.Foroshandeh
            WHERE ccForoshandeh IS NOT NULL AND ccAfrad IS NOT NULL
        """
        mapping = pd.read_sql_query(mapping_query, extractor.src_engine)
        mapping = mapping.rename(columns={'ccAfrad': 'cc_afrad'})
        dim_employee_mapped = pd.merge(mapping, dim_employee, on='cc_afrad', how='inner')[
            ['employee_key', 'ccForoshandeh']
        ].drop_duplicates()
        
        # 5. پردازش چانکی
        total_rows = 0
        chunk_size = 50000
        
        for chunk_details in pd.read_sql_query(details_query, extractor.src_engine, chunksize=chunk_size):
            # JOIN با هدرها
            chunk_headers = headers[headers['ccDarkhastFaktor'].isin(chunk_details['ccDarkhastFaktor'])]
            df = pd.merge(chunk_details, chunk_headers, on='ccDarkhastFaktor', how='inner')
            
            if df.empty:
                continue
            
            # date_key میلادی
            df['TarikhFaktor'] = pd.to_datetime(df['TarikhFaktor'])
            df['date_key'] = df['TarikhFaktor'].dt.strftime('%Y%m%d').astype(int)
            
            # JOIN با ابعاد
            df = pd.merge(df, dim_product, left_on='ccKala', right_on='cc_kala', how='left')
            df['product_key'] = df['product_key'].fillna(1).astype(int)
            
            df = pd.merge(df, dim_customer, left_on='ccMoshtary', right_on='cc_moshtary', how='left')
            df['customer_key'] = df['customer_key'].fillna(1).astype(int)
            
            df = pd.merge(df, dim_employee_mapped, on='ccForoshandeh', how='left')
            df['employee_key'] = df['employee_key'].fillna(1).astype(int)
            
            df = pd.merge(df, dim_center, left_on='ccMarkazPakhsh', right_on='cc_markaz_pakhsh', how='left')
            df['dist_center_key'] = df['dist_center_key'].fillna(1).astype(int)
            
            # ساخت fact
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
            
            # حذف تکراری
            fact = fact.drop_duplicates(['cc_darkhast_faktor', 'sal_mali', 'product_key'])
            
            # بارگذاری با COPY
            loader.bulk_copy(df=fact, target_table="fact_sales")
            total_rows += len(fact)
        
        logger.info(f"   ✅ بازه {from_date}: {total_rows:,} رکورد")
        return total_rows
        
    except Exception as e:
        logger.error(f"   ❌ خطا در بازه {from_date}: {str(e)[:200]}")
        raise


def run_backfill_serial(start_date, end_date):
    """
    اجرای پشت سر هم (بدون موازی)
    برای سرورهای با RAM محدود
    """
    ranges = generate_monthly_ranges(start_date, end_date)
    total = 0
    
    logger.info(f"📋 {len(ranges)} بازه ماهانه برای پردازش")
    
    for i, month_range in enumerate(ranges, 1):
        logger.info(f"\n🔄 بازه {i}/{len(ranges)}")
        try:
            rows = backfill_month(month_range)
            total += rows
            logger.info(f"   📊 مجموع تا اینجا: {total:,} رکورد")
        except Exception as e:
            logger.error(f"🚨 توقف در بازه {i}: {e}")
            break
    
    return total


def run_backfill_parallel(start_date, end_date, workers=2):
    """
    اجرای موازی با ThreadPool
    برای سرورهای قوی (CPU/RAM بالا)
    """
    ranges = generate_monthly_ranges(start_date, end_date)
    total = 0
    
    logger.info(f"📋 {len(ranges)} بازه ماهانه با {workers} worker")
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(backfill_month, r): r for r in ranges}
        
        for i, future in enumerate(as_completed(futures), 1):
            month_range = futures[future]
            try:
                rows = future.result()
                total += rows
                logger.info(f"✅ بازه {i}/{len(ranges)}: {rows:,} رکورد (مجموع: {total:,})")
            except Exception as e:
                logger.error(f"❌ بازه {month_range}: {e}")
    
    return total


def main():
    parser = argparse.ArgumentParser(description='Backfill داده‌های تاریخی فروش')
    parser.add_argument('--start', required=True, help='تاریخ شروع (YYYY-MM-DD)')
    parser.add_argument('--end', required=True, help='تاریخ پایان (YYYY-MM-DD)')
    parser.add_argument('--workers', type=int, default=1, help='تعداد worker موازی')
    
    args = parser.parse_args()
    
    logger.info("=" * 70)
    logger.info("🚀 BACKFILL تاریخی فروش")
    logger.info(f"   بازه: {args.start} تا {args.end}")
    logger.info(f"   حالت: {'موازی (' + str(args.workers) + ' worker)' if args.workers > 1 else 'سریال'}")
    logger.info("=" * 70)
    
    start_time = datetime.now()
    
    if args.workers > 1:
        total = run_backfill_parallel(args.start, args.end, args.workers)
    else:
        total = run_backfill_serial(args.start, args.end)
    
    duration = (datetime.now() - start_time).total_seconds()
    hours = duration / 3600
    
    logger.info(f"""
    ╔══════════════════════════════════════╗
    ║     ✅ BACKFILL پایان یافت          ║
    ╠══════════════════════════════════════╣
    ║ کل رکوردها: {total:>15,}  ║
    ║ زمان کل: {hours:>15.1f} ساعت   ║
    ║ سرعت: {total/duration:>15.0f} رکورد/ثانیه ║
    ╚══════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()