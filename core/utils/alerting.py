"""
سیستم هشدار - تلگرام، ایمیل، لاگ
سازگار با Airflow (Airflow خودش Callback دارد)
"""

import requests
from datetime import datetime
from core.utils.logging import setup_logger

logger = setup_logger("alerting")


class AlertManager:
    """
    مدیریت هشدارها
    در Airflow می‌تواند با on_failure_callback ترکیب شود
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        self.telegram_token = self.config.get('telegram_token')
        self.telegram_chat_id = self.config.get('telegram_chat_id')
    
    def send_telegram(self, message, parse_mode='HTML'):
        """ارسال پیام به تلگرام"""
        if not self.telegram_token or not self.telegram_chat_id:
            logger.debug("⚠️ تنظیمات تلگرام کامل نیست")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"⚠️ خطا در ارسال تلگرام: {e}")
            return False
    
    def alert_error(self, pipeline_name, error_message, rows_processed=0):
        """هشدار خطا"""
        message = f"""
🚨 <b>خطا در پایپ‌لاین</b>

📋 نام: <code>{pipeline_name}</code>
⏰ زمان: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 رکوردهای پردازش شده: {rows_processed:,}

❌ خطا:
<pre>{str(error_message)[:300]}</pre>
        """
        
        logger.error(message)
        self.send_telegram(message)
    
    def alert_success(self, pipeline_name, rows_processed, duration):
        """هشدار موفقیت (فقط برای پایپ‌لاین‌های مهم)"""
        message = f"""
✅ <b>پایپ‌لاین با موفقیت پایان یافت</b>

📋 نام: <code>{pipeline_name}</code>
📊 رکوردها: {rows_processed:,}
⏱️ زمان: {duration:.1f} ثانیه
🚀 سرعت: {rows_processed/duration:.0f} رکورد/ثانیه
        """
        
        logger.info(message)
        # فقط برای خطاها تلگرام بفرست، موفقیت‌ها را لاگ کن
    
    def alert_quality_failure(self, check_name, details):
        """هشدار کاهش کیفیت داده"""
        message = f"""
⚠️ <b>هشدار کیفیت داده</b>

🔍 بررسی: {check_name}
📊 جزئیات: {str(details)[:200]}
⏰ زمان: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        logger.warning(message)
        self.send_telegram(message)
    