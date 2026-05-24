import os
import logging
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    """تنظیم لاگر استاندارد پروژه برای ثبت وقایع در فایل و ترمینال"""
    logger = logging.getLogger(name)
    
    # اگر لاگر قبلاً تنظیم شده، دوباره تنظیمش نکن
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(logging.INFO)
    
    # ساخت فرمت نمایش لاگ‌ها (زمان - نام ماژول - سطح خطا - متن پیام)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # ۱. هندلر برای چاپ در ترمینال (Console)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # ۲. هندلر برای ذخیره در فایل (با تفکیک روزانه)
    log_dir = "logs/etl"
    os.makedirs(log_dir, exist_ok=True)
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_handler = logging.FileHandler(f"{log_dir}/etl_{current_date}.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger