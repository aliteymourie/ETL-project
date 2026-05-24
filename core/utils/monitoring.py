import pandas as pd
from datetime import datetime
from core.engine.base_etl import BaseETL

class PipelineMonitor(BaseETL):
    def __init__(self):
        super().__init__()
        self.engine = self.get_postgres_engine()
        self._create_monitoring_table()

    def _create_monitoring_table(self):
        """ساخت جدول لاگ‌های عملکردی در خود پُست‌گرس در صورت عدم وجود"""
        query = """
        CREATE TABLE IF NOT EXISTS etl_pipeline_logs (
            id SERIAL PRIMARY KEY,
            pipeline_name VARCHAR(100),
            status VARCHAR(20),
            rows_processed INT,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            execution_time_seconds REAL,
            error_message TEXT
        );
        """
        with self.engine.connect() as conn:
            with conn.begin():
                conn.execute(query)

    def log_success(self, pipeline_name: str, rows_processed: int, start_time: datetime):
        """ثبت وضعیت موفقیت پایپ‌لاین"""
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        df = pd.DataFrame([{
            "pipeline_name": pipeline_name,
            "status": "SUCCESS",
            "rows_processed": rows_processed,
            "start_time": start_time,
            "end_time": end_time,
            "execution_time_seconds": duration,
            "error_message": None
        }])
        df.to_sql("etl_pipeline_logs", self.engine, if_exists="append", index=False)

    def log_failure(self, pipeline_name: str, start_time: datetime, error_message: str):
        """ثبت وضعیت شکست پایپ‌لاین"""
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        df = pd.DataFrame([{
            "pipeline_name": pipeline_name,
            "status": "FAILED",
            "rows_processed": 0,
            "start_time": start_time,
            "end_time": end_time,
            "execution_time_seconds": duration,
            "error_message": str(error_message)
        }])
        df.to_sql("etl_pipeline_logs", self.engine, if_exists="append", index=False)