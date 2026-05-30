"""
مانیتورینگ و ثبت متادیتای اجرا - سازگار با Airflow
"""

import time
import functools
from datetime import datetime
from sqlalchemy import text
from core.utils.logging import setup_logger

logger = setup_logger("monitoring")


class PipelineMonitor:
    """
    مانیتورینگ پایپ‌لاین‌ها
    ثبت زمان اجرا، تعداد رکورد، وضعیت و خطاها
    
    سازگار با Airflow: می‌تواند به عنوان callback یا context manager استفاده شود
    """
    
    def __init__(self, loader, pipeline_name):
        self.loader = loader
        self.pipeline_name = pipeline_name
        self.start_time = None
        self.metrics = {}
    
    def start(self, metadata=None):
        """شروع مانیتورینگ"""
        self.start_time = datetime.now()
        self.metrics = {
            'pipeline_name': self.pipeline_name,
            'status': 'RUNNING',
            'start_time': self.start_time,
            'metadata': metadata or {}
        }
        
        logger.info(f"🚀 [{self.pipeline_name}] شروع اجرا در {self.start_time}")
        
        # ثبت در دیتابیس
        self._log_to_db('STARTED')
        
        return self
    
    def success(self, rows_processed=0, extra_metrics=None):
        """ثبت موفقیت"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        self.metrics.update({
            'status': 'SUCCESS',
            'end_time': end_time,
            'duration_seconds': duration,
            'rows_processed': rows_processed,
            'rows_per_second': rows_processed / duration if duration > 0 else 0
        })
        
        if extra_metrics:
            self.metrics.update(extra_metrics)
        
        logger.info(f"""
        ╔══════════════════════════════════════╗
        ║     ✅ [{self.pipeline_name}]       ║
        ╠══════════════════════════════════════╣
        ║ رکوردها: {rows_processed:>16,}  ║
        ║ زمان: {duration:>18.1f} ثانیه ║
        ╚══════════════════════════════════════╝
        """)
        
        self._log_to_db('SUCCESS', rows_processed, str(end_time))
        
        return self.metrics
    
    def failure(self, error_message):
        """ثبت شکست"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        self.metrics.update({
            'status': 'FAILED',
            'end_time': end_time,
            'duration_seconds': duration,
            'error_message': str(error_message)[:500]
        })
        
        logger.error(f"❌ [{self.pipeline_name}] شکست: {str(error_message)[:200]}")
        
        self._log_to_db('FAILED', error_message=str(error_message)[:500])
        
        return self.metrics
    
    def _log_to_db(self, status, rows=0, end_time=None):
        """ثبت در جدول مانیتورینگ"""
        try:
            with self.loader.tgt_engine.begin() as conn:
                conn.execute(
                    text("""
                        INSERT INTO etl_metadata.monitoring_log 
                            (pipeline_name, run_id, status, rows_processed, 
                             start_time, end_time, duration_seconds, error_message)
                        VALUES 
                            (:pipeline, :run_id, :status, :rows,
                             :start_time, :end_time, :duration, :error)
                    """),
                    {
                        "pipeline": self.pipeline_name,
                        "run_id": self.start_time.strftime('%Y%m%d%H%M%S') if self.start_time else datetime.now().strftime('%Y%m%d%H%M%S'),
                        "status": status,
                        "rows": rows,
                        "start_time": self.start_time if self.start_time else datetime.now(),
                        "end_time": datetime.now() if end_time is None else end_time,
                        "duration": (datetime.now() - self.start_time).total_seconds() if self.start_time else 0,
                        "error": str(end_time) if status == 'FAILED' else None
                    }
                )
        except Exception as e:
            logger.debug(f"⚠️ خطا در ثبت مانیتورینگ: {e}")
    
    def __enter__(self):
        """Context Manager: with PipelineMonitor(...) as monitor:"""
        return self.start()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """خودکار success/failure بر اساس خطا"""
        if exc_type is None:
            self.success()
        else:
            self.failure(str(exc_val))
        return False  # خطا را propagate کن


def monitor_pipeline(pipeline_name):
    """
    دکوراتور برای مانیتورینگ خودکار پایپ‌لاین
    
    @monitor_pipeline("dim_product")
    def run_dim_product():
        ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            from core.engine.loader import DataLoader
            loader = DataLoader()
            
            monitor = PipelineMonitor(loader, pipeline_name)
            monitor.start()
            
            try:
                result = func(*args, **kwargs)
                rows = result if isinstance(result, (int, float)) else 0
                monitor.success(rows)
                return result
            except Exception as e:
                monitor.failure(str(e))
                raise
        
        return wrapper
    return decorator


def log_execution_time(func):
    """
    دکوراتور ساده برای لاگ زمان اجرا
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        logger.info(f"⏱️ [{func.__name__}] زمان اجرا: {duration:.2f} ثانیه")
        return result
    return wrapper