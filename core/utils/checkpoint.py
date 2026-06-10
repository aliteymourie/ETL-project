"""
مدیریت Checkpoint - اصلاح فرمت تاریخ
"""

from sqlalchemy import text
from datetime import datetime
from core.utils.logging import setup_logger

logger = setup_logger("checkpoint")

class ETLCheckpoint:
    def __init__(self, loader):
        self.loader = loader
        self._ensure_table_exists()
    
    def _ensure_table_exists(self):
        try:
            with self.loader.tgt_engine.connect() as conn:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS etl_metadata.etl_checkpoint (
                        pipeline_name VARCHAR(100) PRIMARY KEY,
                        last_run_at TIMESTAMP,
                        last_success_at TIMESTAMP,
                        last_from_value VARCHAR(100),
                        last_to_value VARCHAR(100),
                        rows_processed INTEGER DEFAULT 0,
                        status VARCHAR(20),
                        error_message TEXT,
                        updated_at TIMESTAMP DEFAULT NOW()
                    )
                """))
                for ddl in (
                    "ALTER TABLE etl_metadata.etl_checkpoint ADD COLUMN IF NOT EXISTS last_run_at TIMESTAMP",
                    "ALTER TABLE etl_metadata.etl_checkpoint ADD COLUMN IF NOT EXISTS last_success_at TIMESTAMP",
                    "ALTER TABLE etl_metadata.etl_checkpoint ADD COLUMN IF NOT EXISTS last_from_value VARCHAR(100)",
                    "ALTER TABLE etl_metadata.etl_checkpoint ADD COLUMN IF NOT EXISTS last_to_value VARCHAR(100)",
                    "ALTER TABLE etl_metadata.etl_checkpoint ADD COLUMN IF NOT EXISTS rows_processed INTEGER DEFAULT 0",
                    "ALTER TABLE etl_metadata.etl_checkpoint ADD COLUMN IF NOT EXISTS status VARCHAR(20)",
                    "ALTER TABLE etl_metadata.etl_checkpoint ADD COLUMN IF NOT EXISTS error_message TEXT",
                    "ALTER TABLE etl_metadata.etl_checkpoint ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW()",
                ):
                    conn.execute(text(ddl))
                conn.execute(text("""
                    DO $$
                    BEGIN
                        -- Try PRIMARY KEY on pipeline_name if no PK exists
                        IF NOT EXISTS (
                            SELECT 1 FROM pg_constraint
                            WHERE conrelid = 'etl_metadata.etl_checkpoint'::regclass
                              AND contype  = 'p'
                        ) THEN
                            ALTER TABLE etl_metadata.etl_checkpoint
                                ADD CONSTRAINT etl_checkpoint_pkey PRIMARY KEY (pipeline_name);
                        END IF;
                        -- Fallback: unique index on pipeline_name (table may already have PK on id)
                        IF NOT EXISTS (
                            SELECT 1 FROM pg_indexes
                            WHERE schemaname = 'etl_metadata'
                              AND tablename   = 'etl_checkpoint'
                              AND indexname   = 'idx_checkpoint_unique_pipeline'
                        ) THEN
                            CREATE UNIQUE INDEX idx_checkpoint_unique_pipeline
                                ON etl_metadata.etl_checkpoint (pipeline_name);
                        END IF;
                    END;
                    $$;
                """))
                conn.commit()
        except Exception as e:
            logger.error(f"خطا در ایجاد جدول checkpoint: {e}")
    
    def get_last_success(self, pipeline_name):
        try:
            with self.loader.tgt_engine.connect() as conn:
                result = conn.execute(
                    text("""
                        SELECT last_success_at, last_from_value, last_to_value, rows_processed
                        FROM etl_metadata.etl_checkpoint
                        WHERE pipeline_name = :name AND status = 'SUCCESS'
                    """),
                    {"name": pipeline_name}
                )
                row = result.fetchone()
                
                if row:
                    return {
                        'last_success_at': row[0],
                        'last_from_value': row[1],
                        'last_to_value': row[2],
                        'rows_processed': row[3]
                    }
                return None
        except Exception as e:
            logger.warning(f"⚠️ خطا در خواندن checkpoint {pipeline_name}: {e}")
            return None
    
    def save_checkpoint(self, pipeline_name, status, rows_processed=0, 
                       from_value=None, to_value=None, error_message=None):
        """
        ذخیره وضعیت اجرا
        تاریخ‌ها با فرمت مناسب SQL Server ذخیره می‌شوند
        """
        try:
            # تبدیل تاریخ به فرمت SQL Server (YYYY-MM-DD HH:MM:SS)
            if from_value:
                if isinstance(from_value, datetime):
                    from_value = from_value.strftime('%Y-%m-%d %H:%M:%S')
                elif 'T' in str(from_value):
                    from_value = str(from_value).replace('T', ' ')[:19]
                elif '.' in str(from_value):
                    from_value = str(from_value).split('.')[0]
            
            if to_value and isinstance(to_value, datetime):
                to_value = to_value.strftime('%Y-%m-%d')
            
            with self.loader.tgt_engine.begin() as conn:
                conn.execute(
                    text("""
                        INSERT INTO etl_metadata.etl_checkpoint 
                            (pipeline_name, last_run_at, last_success_at, 
                             last_from_value, last_to_value, rows_processed, status, error_message)
                        VALUES 
                            (:name, NOW(), CASE WHEN :status = 'SUCCESS' THEN NOW() ELSE NULL END,
                             :from_val, :to_val, :rows, :status, :error)
                        ON CONFLICT (pipeline_name) DO UPDATE SET
                            last_run_at = NOW(),
                            last_success_at = CASE WHEN :status = 'SUCCESS' THEN NOW() 
                                                   ELSE etl_metadata.etl_checkpoint.last_success_at END,
                            last_from_value = :from_val,
                            last_to_value = :to_val,
                            rows_processed = :rows,
                            status = :status,
                            error_message = :error,
                            updated_at = NOW()
                    """),
                    {
                        "name": pipeline_name,
                        "status": status,
                        "rows": rows_processed,
                        "from_val": str(from_value) if from_value else None,
                        "to_val": str(to_value) if to_value else None,
                        "error": error_message[:500] if error_message else None
                    }
                )
            logger.debug(f"✅ Checkpoint ذخیره شد: {pipeline_name} = {status}")
        except Exception as e:
            logger.warning(f"⚠️ خطا در ذخیره checkpoint: {e}")
