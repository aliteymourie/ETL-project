import io
import pandas as pd
from core.engine.base_etl import BaseETL
from core.decorators import retry_on_failure
from core.utils.logging import setup_logger
from sqlalchemy import text

logger = setup_logger("loader")

class DataLoader(BaseETL):
    def __init__(self):
        super().__init__()
        self.tgt_engine = self.get_postgres_engine()

    def ensure_tracking_column(self, table_name: str):
        """
        اطمینان از وجود ستون updated_at برای ردگیری همگام‌سازی افزایشی.
        این متد ستون را در صورت عدم وجود می‌سازد و با داده‌های موجود پر می‌کند.
        """
        try:
            with self.tgt_engine.connect() as conn:
                # بررسی وجود ستون
                result = conn.execute(text(f"""
                    SELECT EXISTS (
                        SELECT 1 FROM information_schema.columns 
                        WHERE table_name = '{table_name}' AND column_name = 'updated_at'
                    )
                """)).scalar()
                
                if not result:
                    # افزودن ستون
                    conn.execute(text(f"""
                        ALTER TABLE {table_name} 
                        ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    """))
                    conn.commit()
                    logger.info(f"✅ ستون updated_at به {table_name} اضافه شد.")
                    
                    # پر کردن مقادیر اولیه از روی ستون‌های موجود
                    conn.execute(text(f"""
                        UPDATE {table_name} 
                        SET updated_at = COALESCE(modified_date, invoice_date, created_date, CURRENT_TIMESTAMP)
                    """))
                    conn.commit()
                    logger.info(f"✅ مقادیر اولیه updated_at در {table_name} مقداردهی شد.")
                else:
                    logger.debug(f"ℹ️ ستون updated_at از قبل در {table_name} وجود دارد.")
                    
        except Exception as e:
            logger.warning(f"⚠️ خطا در مدیریت ستون updated_at برای {table_name}: {str(e)}")

    @retry_on_failure(retries=3, delay=5)
    def bulk_copy(self, df: pd.DataFrame, target_table: str):
        """بارگذاری حجمی و فوق سریع با پروتکل بومی COPY در دیتابیس مقصد"""
        if df.empty:
            logger.warning(f"⚠️ دیتایی برای بارگذاری در جدول {target_table} یافت نشد.")
            return

        # اطمینان از وجود ستون ردیابی (بدون ایجاد خطا در صورت شکست)
        try:
            self.ensure_tracking_column(target_table)
        except Exception:
            pass

        # حل مشکل مقادیر تهی با تعریف شناسه یکتا پیش‌فرض برای دیتابیس پستگرس
        output = io.StringIO()
        df.to_csv(output, sep='\t', header=False, index=False, na_rep='\\N')
        output.seek(0)

        raw_conn = self.tgt_engine.raw_connection()
        try:
            with raw_conn.cursor() as cursor:
                cursor.copy_from(
                    output, 
                    target_table, 
                    null='\\N', # تطابق دقیق پانداس ناپیدا با دیتابیس پُست‌گرس
                    columns=list(df.columns)
                )
            raw_conn.commit()
            logger.info(f"✨ تعداد {len(df)} ردیف با موفقیت در جدول انبار داده ({target_table}) لود شد.")
            
        except Exception as e:
            raw_conn.rollback()
            logger.error(f"❌ شکست عملیات جابه‌جایی انبوه در جدول {target_table}: {str(e)}")
            raise e
        finally:
            raw_conn.close()

    def create_table(self, ddl_sql: str):
        """اجرای دستور DDL برای ایجاد یا اصلاح جدول در دیتابیس مقصد."""
        try:
            with self.tgt_engine.connect() as conn:
                conn.execute(text(ddl_sql))
            logger.info("✅ اجرای DDL با موفقیت انجام شد.")
        except Exception as e:
            logger.error(f"❌ خطا در اجرای DDL: {str(e)}")
            raise e