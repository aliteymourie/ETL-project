"""
مدیریت خطا و تلاش مجدد - سازگار با Airflow
"""

import time
import functools
from sqlalchemy.exc import OperationalError, TimeoutError
from core.utils.logging import setup_logger

logger = setup_logger("retry_handler")

# خطاهایی که قابل تلاش مجدد هستند
RETRYABLE_ERRORS = (
    OperationalError,      # اتصال به دیتابیس
    TimeoutError,          # timeout
    ConnectionError,       # شبکه
    TimeoutError,          # timeout عمومی
)


def retry_on_failure(
    max_retries=3,
    initial_delay=5,
    backoff_factor=2,
    max_delay=300,
    retryable_errors=RETRYABLE_ERRORS
):
    """
    دکوراتور تلاش مجدد با Exponential Backoff
    
    پارامترها:
    - max_retries: حداکثر تعداد تلاش
    - initial_delay: تاخیر اولیه (ثانیه)
    - backoff_factor: ضریب افزایش تاخیر
    - max_delay: حداکثر تاخیر (ثانیه)
    - retryable_errors: خطاهای قابل تلاش مجدد
    
    نحوه استفاده:
    @retry_on_failure(max_retries=3, initial_delay=5)
    def my_function():
        ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            last_exception = None
            
            for attempt in range(1, max_retries + 1):
                try:
                    logger.debug(f"🔄 تلاش {attempt}/{max_retries} برای [{func_name}]")
                    result = func(*args, **kwargs)
                    
                    if attempt > 1:
                        logger.info(f"✅ [{func_name}] در تلاش {attempt} موفق شد")
                    
                    return result
                    
                except retryable_errors as e:
                    last_exception = e
                    
                    if attempt < max_retries:
                        delay = min(initial_delay * (backoff_factor ** (attempt - 1)), max_delay)
                        logger.warning(
                            f"⚠️ [{func_name}] تلاش {attempt}/{max_retries} ناموفق. "
                            f"خطا: {str(e)[:100]}. تلاش مجدد در {delay:.0f} ثانیه..."
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"🚨 [{func_name}] پس از {max_retries} تلاش کاملاً شکست خورد. "
                            f"آخرین خطا: {str(e)[:200]}"
                        )
                        raise
                        
                except Exception as e:
                    # خطاهای غیرقابل تلاش - فوراً raise کن
                    logger.error(f"❌ [{func_name}] خطای غیرقابل تلاش: {str(e)[:200]}")
                    raise
            
            # اگر به اینجا برسیم یعنی همه تلاش‌ها ناموفق بوده
            raise last_exception
            
        return wrapper
    return decorator


def safe_execute(func, *args, default_return=None, **kwargs):
    """
    اجرای ایمن یک تابع - اگر خطا داد، مقدار پیش‌فرض برگردان
    
    برای پردازش رکورد به رکورد که یک رکورد خراب نباید کل کار را متوقف کند
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.debug(f"⚠️ خطا در safe_execute: {str(e)[:80]}")
        return default_return


class ErrorCollector:
    """
    جمع‌آوری خطاها بدون توقف پردازش
    مناسب برای Batch Processing
    """
    
    def __init__(self, max_errors=100):
        self.errors = []
        self.max_errors = max_errors
        self.total_processed = 0
        self.total_errors = 0
    
    def execute(self, func, *args, **kwargs):
        """
        اجرای یک تابع و جمع‌آوری خطاها
        """
        self.total_processed += 1
        
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            self.total_errors += 1
            error_info = {
                'function': func.__name__ if hasattr(func, '__name__') else str(func),
                'args': str(args)[:100],
                'error': str(e)[:200],
                'error_type': type(e).__name__
            }
            
            if len(self.errors) < self.max_errors:
                self.errors.append(error_info)
            
            return None
    
    def get_summary(self):
        """گزارش خلاصه خطاها"""
        return {
            'total_processed': self.total_processed,
            'total_errors': self.total_errors,
            'error_rate': round(self.total_errors / self.total_processed * 100, 2) if self.total_processed > 0 else 0,
            'first_errors': self.errors[:5]
        }
    
    def has_errors(self):
        return self.total_errors > 0
    
    def log_summary(self):
        """لاگ خلاصه خطاها"""
        summary = self.get_summary()
        
        if self.has_errors():
            logger.warning(f"""
            ╔══════════════════════════════════════╗
            ║     📊 خلاصه خطاهای پردازش          ║
            ╠══════════════════════════════════════╣
            ║ کل پردازش: {summary['total_processed']:>14,}  ║
            ║ خطاها: {summary['total_errors']:>18,}  ║
            ║ نرخ خطا: {summary['error_rate']:>15}٪  ║
            ╚══════════════════════════════════════╝
            """)
            
            if summary['first_errors']:
                logger.warning("   اولین خطاها:")
                for i, err in enumerate(summary['first_errors'][:3], 1):
                    logger.warning(f"   {i}. {err['error_type']}: {err['error'][:100]}")
        else:
            logger.info(f"✅ {summary['total_processed']:,} رکورد بدون خطا پردازش شد")