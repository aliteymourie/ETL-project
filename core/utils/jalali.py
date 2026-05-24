import jdatetime
from datetime import datetime

class JalaliCalendar:
    def __init__(self):
        # نام ماه‌های شمسی برای استفاده در داشبوردها
        self.months_farsi = [
            "فروردین", "اردیبهشت", "خرداد", 
            "تیر", "مرداد", "شهریور", 
            "مهر", "آبان", "آذر", 
            "دی", "بهمن", "اسفند"
        ]

    def get_jalali_attributes(self, date_value) -> dict:
        """
        یک تاریخ میلادی (datetime یا رشته) می‌گیرد و
        تمام ویژگی‌های شمسی مورد نیاز برای لایه مصورسازی را استخراج می‌کند.
        """
        if date_value is None:
            return {}

        # اگر ورودی رشته بود، آن را به datetime تبدیل کن
        if isinstance(date_value, str):
            try:
                # فرمت متداول دیتابیس‌ها
                date_value = datetime.strptime(date_value[:10], "%Y-%m-%d")
            except ValueError:
                return {}

        # تبدیل میلادی به شمسی
        jalali_date = jdatetime.date.fromgregorian(date=date_value)
        
        year = jalali_date.year
        month = jalali_date.month
        day = jalali_date.day
        
        # تعیین فصل
        if month <= 3:
            season = "بهار"
        elif month <= 6:
            season = "تابستان"
        elif month <= 9:
            season = "پاییز"
        else:
            season = "زمستان"

        # خروجی به صورت یک دیکشنری کامل جهت تزریق به انبار داده
        return {
            "gregorian_date": date_value.strftime("%Y-%m-%d"),
            "jalali_date_code": int(f"{year}{month:02d}{day:02d}"), # کلید عددی مثل 14050228
            "jalali_full_date": f"{year}/{month:02d}/{day:02d}",     # رشته متنی برای نمایش
            "jalali_year": year,
            "jalali_month_no": month,
            "jalali_month_name": self.months_farsi[month - 1],
            "jalali_day": day,
            "jalali_season": season,
            "is_weekend": 1 if jalali_date.weekday() == 6 else 0     # در jdatetime عدد ۶ یعنی جمعه
        }