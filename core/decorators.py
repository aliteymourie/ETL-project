# core/decorators.py
import time
import threading
from functools import wraps
from datetime import datetime, timedelta
from enum import Enum
from core.utils.logging import setup_logger

logger = setup_logger("decorators")

class CircuitState(Enum):
    """وضعیت‌های مدارشکن"""
    CLOSED = "closed"        # عادی - درخواست‌ها عبور می‌کنند
    OPEN = "open"            # قطع - درخواست‌ها reject می‌شوند
    HALF_OPEN = "half_open"  # نیمه‌باز - تست سلامت

class CircuitBreaker:
    """
    مدارشکن برای محافظت از سیستم در برابر خطاهای آبشاری
    
    استفاده:
        circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60)
        
        @circuit_breaker
        def risky_operation():
            ...
    """
    
    def __init__(self, failure_threshold: int = 5, timeout_seconds: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout_seconds
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self.lock = threading.RLock()
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self.lock:
                # اگر مدار باز است
                if self.state == CircuitState.OPEN:
                    # چک timeout برای ورود به حالت نیمه‌باز
                    if datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout):
                        logger.info(f"🔄 مدار نیمه‌باز شد برای {func.__name__}")
                        self.state = CircuitState.HALF_OPEN
                    else:
                        raise CircuitBreakerOpenError(
                            f"مدار برای {func.__name__} باز است. "
                            f"{self.timeout - (datetime.now() - self.last_failure_time).seconds} ثانیه صبر کنید"
                        )
                
                try:
                    result = func(*args, **kwargs)
                    
                    # موفقیت - بازنشانی شمارنده
                    if self.state == CircuitState.HALF_OPEN:
                        logger.info(f"✅ مدار بسته شد برای {func.__name__}")
                        self.state = CircuitState.CLOSED
                    self.failure_count = 0
                    return result
                    
                except Exception as e:
                    self.failure_count += 1
                    self.last_failure_time = datetime.now()
                    
                    if self.failure_count >= self.failure_threshold:
                        logger.error(
                            f"🚨 مدار باز شد برای {func.__name__} "
                            f"(شکست {self.failure_count} از {self.failure_threshold})"
                        )
                        self.state = CircuitState.OPEN
                    
                    raise e
        
        return wrapper


class CircuitBreakerOpenError(Exception):
    """خطای اختصاصی برای مدار باز"""
    pass


def retry_on_failure(retries: int = 3, delay: int = 5, 
                    backoff_factor: int = 2, 
                    exceptions: tuple = (Exception,)):
    """
    دکوریتور تلاش مجدد با قابلیت‌های:
    - Exponential backoff
    - لیست exceptions قابل تنظیم
    - لاگ جزئیات هر تلاش
    
    Args:
        retries: تعداد تلاش‌های مجدد
        delay: تاخیر اولیه (ثانیه)
        backoff_factor: ضریب افزایش تاخیر
        exceptions: tuple خطاهایی که باید retry شوند
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                    
                except exceptions as e:
                    last_exception = e
                    
                    if attempt < retries:
                        wait_time = delay * (backoff_factor ** (attempt - 1))
                        logger.warning(
                            f"⚠️ تلاش {attempt}/{retries} برای [{func.__name__}] ناموفق. "
                            f"خطا: {str(e)[:200]}. "
                            f"تلاش مجدد در {wait_time} ثانیه..."
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(
                            f"🚨 [{func.__name__}] پس از {retries} تلاش کاملاً شکست خورد. "
                            f"آخرین خطا: {str(e)}"
                        )
            
            raise last_exception
        
        return wrapper
    return decorator


def log_execution_time(func):
    """دکوریتور محاسبه و لاگ زمان اجرا"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            
            if elapsed > 60:
                logger.warning(f"⏰ [{func.__name__}] زمان اجرا: {elapsed:.1f} ثانیه (بیش از حد)")
            else:
                logger.info(f"⏱️ [{func.__name__}] زمان اجرا: {elapsed:.2f} ثانیه")
            
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"❌ [{func.__name__}] پس از {elapsed:.2f} ثانیه با خطا متوقف شد: {e}")
            raise
    return wrapper


def validate_dataframe(required_columns: list = None):
    """دکوریتور اعتبارسنجی DataFrame ورودی"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # پیدا کردن DataFrame در args یا kwargs
            df = None
            for arg in args:
                if isinstance(arg, pd.DataFrame):
                    df = arg
                    break
            
            if df is None:
                df = kwargs.get('df')
            
            if df is not None and df.empty:
                logger.warning(f"⚠️ [{func.__name__}] DataFrame خالی است. عملیات انجام نشد.")
                return df
            
            if required_columns and df is not None:
                missing = [col for col in required_columns if col not in df.columns]
                if missing:
                    raise ValueError(
                        f"ستون‌های ضروری در [{func.__name__}] وجود ندارند: {missing}"
                    )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


# نمونه استفاده از مدارشکن
db_circuit_breaker = CircuitBreaker(failure_threshold=3, timeout_seconds=30)
extract_circuit_breaker = CircuitBreaker(failure_threshold=5, timeout_seconds=60)