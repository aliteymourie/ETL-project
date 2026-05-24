import pandas as pd
from core.engine.base_etl import BaseETL
from core.decorators import retry_on_failure # استفاده از دکوراتوری که زحمتش را کشیدید
from core.utils.logging import setup_logger

logger = setup_logger("extractor")

class DataExtractor(BaseETL):
    def __init__(self):
        super().__init__()
        self.src_engine = self.get_mssql_engine()
        self.tgt_engine = self.get_postgres_engine()

    def get_last_sync_timestamp(self, target_table: str, timestamp_column: str = "updated_at") -> str:
        """یافتن زمان آخرین ردیف همگام‌سازی شده در پُست‌گرس"""
        query = f"SELECT MAX({timestamp_column}) FROM {target_table}"
        try:
            with self.tgt_engine.connect() as conn:
                result = conn.execute(query).scalar()
                if result:
                    return result.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                return "1900-01-01 00:00:00.000"
        except Exception as e:
            logger.warning(f"⚠️ جدول مقصد {target_table} هنوز ساخته نشده یا فاقد فیلد زمان است. مقدار پیش‌فرض اعمال شد.")
            return "1900-01-01 00:00:00.000"

    @retry_on_failure(retries=3, delay=10)
    def extract_incremental(self, source_table: str, target_table: str, filter_column: str, chunk_size: int = 50000):
        """استخراج تکه‌تکه داده‌های جدید بر اساس رویکرد استخراج افزایشی"""
        last_sync = self.get_last_sync_timestamp(target_table)
        logger.info(f"🔍 شروع سینک افزایشی برای جدول {target_table}. بازه داده‌ها: بعد از [{last_sync}]")

        query = f"""
            SELECT * 
            FROM {source_table} 
            WHERE {filter_column} > '{last_sync}'
        """

        try:
            # پانداس در این حالت یک دیتاریدر بازگشتی تحویل می‌دهد و کل داده را به حافظه رم سرور تحمیل نمی‌کند
            chunk_container = pd.read_sql_query(query, self.src_engine, chunksize=chunk_size)
            
            has_data = False
            for chunk in chunk_container:
                if not chunk.empty:
                    has_data = True
                    yield chunk
            
            if not has_data:
                logger.info(f"✔️ تمام داده‌های جدول {source_table} به روز هستند.")
                    
        except Exception as e:
            logger.error(f"🚨 خطا در فرآیند استخراج افزایشی از دیتابیس منبع: {str(e)}")
            raise e