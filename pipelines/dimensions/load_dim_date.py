"""
پایپ‌لاین تولید بعد تاریخ - نسخه استاندارد و کامل
date_key = میلادی YYYYMMDD + اطلاعات شمسی
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import jdatetime
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import text
from core.engine.loader import DataLoader
from core.utils.logging import setup_logger

logger = setup_logger("dim_date")

# نگاشت‌های شمسی
JALALI_MONTH_NAMES = {
    1: 'فروردین', 2: 'اردیبهشت', 3: 'خرداد',
    4: 'تیر', 5: 'مرداد', 6: 'شهریور',
    7: 'مهر', 8: 'آبان', 9: 'آذر',
    10: 'دی', 11: 'بهمن', 12: 'اسفند'
}

JALALI_SEASONS = {
    1: 'بهار', 2: 'بهار', 3: 'بهار',
    4: 'تابستان', 5: 'تابستان', 6: 'تابستان',
    7: 'پاییز', 8: 'پاییز', 9: 'پاییز',
    10: 'زمستان', 11: 'زمستان', 12: 'زمستان'
}

GREGORIAN_MONTH_NAMES = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}

DAY_NAMES = {
    0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
    4: 'Friday', 5: 'Saturday', 6: 'Sunday'
}

# کوئری INSERT یکبار تعریف می‌شود
INSERT_SQL = """
    INSERT INTO dim_date (
        date_key, full_date, gregorian_year, gregorian_month,
        gregorian_month_name, gregorian_day, day_of_week,
        day_of_week_name, is_weekend, jalali_year, jalali_month,
        jalali_month_name, jalali_day, jalali_date_str,
        jalali_season, is_holiday
    ) VALUES (
        :date_key, :full_date, :gregorian_year, :gregorian_month,
        :gregorian_month_name, :gregorian_day, :day_of_week,
        :day_of_week_name, :is_weekend, :jalali_year, :jalali_month,
        :jalali_month_name, :jalali_day, :jalali_date_str,
        :jalali_season, :is_holiday
    )
"""


def run_dim_date_pipeline(start_year=2016, end_year=2036):
    """
    تولید بعد تاریخ با date_key میلادی + اطلاعات شمسی
    
    پارامترها:
    - start_year: سال میلادی شروع (پیش‌فرض: 2016)
    - end_year: سال میلادی پایان (پیش‌فرض: 2036)
    """
    logger.info("=" * 60)
    logger.info(f"🔄 تولید بعد تاریخ میلادی-شمسی: {start_year} تا {end_year}")
    start_time = datetime.now()
    
    loader = DataLoader()
    
    try:
        # 1. محاسبه بازه
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)
        
        total_days = (end_date - start_date).days + 1
        logger.info(f"📅 تولید {total_days:,} روز...")
        
        # 2. تولید تمام روزها در حافظه
        dates = []
        current_date = start_date
        
        logger.info("🔄 در حال تولید تاریخ‌ها...")
        while current_date <= end_date:
            # تبدیل به شمسی
            try:
                jd = jdatetime.date.fromgregorian(date=current_date)
                jalali_year = jd.year
                jalali_month = jd.month
                jalali_day = jd.day
                jalali_month_name = JALALI_MONTH_NAMES.get(jalali_month, '')
                jalali_season = JALALI_SEASONS.get(jalali_month, '')
                jalali_date_str = f"{jalali_year}-{jalali_month:02d}-{jalali_day:02d}"
            except Exception:
                jalali_year = None
                jalali_month = None
                jalali_day = None
                jalali_month_name = None
                jalali_season = None
                jalali_date_str = None
            
            # اطلاعات میلادی
            date_key = int(current_date.strftime('%Y%m%d'))
            gregorian_year = current_date.year
            gregorian_month = current_date.month
            gregorian_day = current_date.day
            gregorian_month_name = GREGORIAN_MONTH_NAMES.get(gregorian_month, '')
            day_of_week = current_date.weekday()  # 0=Monday
            day_of_week_name = DAY_NAMES.get(day_of_week, '')
            is_weekend = (current_date.weekday() == 4)  # Friday
            
            dates.append({
                'date_key': date_key,
                'full_date': current_date,
                'gregorian_year': gregorian_year,
                'gregorian_month': gregorian_month,
                'gregorian_month_name': gregorian_month_name,
                'gregorian_day': gregorian_day,
                'day_of_week': day_of_week,
                'day_of_week_name': day_of_week_name,
                'is_weekend': is_weekend,
                'jalali_year': jalali_year,
                'jalali_month': jalali_month,
                'jalali_month_name': jalali_month_name,
                'jalali_day': jalali_day,
                'jalali_date_str': jalali_date_str,
                'jalali_season': jalali_season,
                'is_holiday': False
            })
            
            current_date += timedelta(days=1)
        
        logger.info(f"✅ {len(dates):,} روز در حافظه تولید شد.")
        
        # 3. ذخیره در PostgreSQL
        logger.info("💾 در حال ذخیره در PostgreSQL...")
        
        with loader.tgt_engine.begin() as conn:
            # پاک کردن رکوردهای قبلی
            conn.execute(text("DELETE FROM dim_date"))
            
            inserted = 0
            errors = 0
            batch_size = 500
            
            for i in range(0, len(dates), batch_size):
                batch = dates[i:i+batch_size]
                
                for record in batch:
                    try:
                        conn.execute(text(INSERT_SQL), record)
                        inserted += 1
                    except Exception as e:
                        errors += 1
                        if errors <= 3:
                            logger.warning(f"⚠️ خطا در date_key={record['date_key']}: {str(e)[:100]}")
                
                # گزارش پیشرفت
                progress = min(i + batch_size, len(dates))
                if progress % 5000 == 0 or progress == len(dates):
                    logger.info(f"  ➜ {progress:,}/{len(dates):,} ({progress*100/len(dates):.0f}%)")
        
        # 4. گزارش نهایی
        duration = (datetime.now() - start_time).total_seconds()
        
        if errors > 0:
            logger.warning(f"⚠️ {errors} خطا در ذخیره‌سازی")
        
        logger.info(f"""
        ╔══════════════════════════════════════╗
        ║   ✅ بعد تاریخ (استاندارد) تولید شد ║
        ╠══════════════════════════════════════╣
        ║ کل روزها: {len(dates):>16,}  ║
        ║ ذخیره شده: {inserted:>15,}  ║
        ║ خطا: {errors:>20,}  ║
        ║ زمان: {duration:>17.1f} ثانیه ║
        ╚══════════════════════════════════════╝
        """)
        
        # 5. بررسی صحت
        with loader.tgt_engine.connect() as conn:
            result = conn.execute(text("""
                SELECT COUNT(*) as cnt, MIN(full_date) as min_date, MAX(full_date) as max_date
                FROM dim_date
            """))
            row = result.fetchone()
            logger.info(f"📊 بررسی نهایی: {row[0]:,} رکورد از {row[1]} تا {row[2]}")
        
        return inserted
        
    except Exception as e:
        logger.error(f"❌ خطا: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    run_dim_date_pipeline(2011, 2036)