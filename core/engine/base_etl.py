import os
import re
import yaml
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from core.utils.logging import setup_logger
from dotenv import load_dotenv

logger = setup_logger("base_etl")

class BaseETL:
    def __init__(self, settings_path="config/settings.yaml", db_config_path="config/databases.yaml"):
        load_dotenv()
        self.settings_path = settings_path
        self.db_config_path = db_config_path
        
        # ۱. لود کردن تنظیمات عمومی و دیتابیس‌ها
        self.settings = self._load_yaml(self.settings_path)
        self.db_config = self._load_yaml(self.db_config_path)
        
        # ۲. جایگذاری متغیرهای محیطی امنیتی (مثل پسوردها)
        self.db_config = self._replace_env_vars(self.db_config)

    def _load_yaml(self, path):
        """خواندن فایل‌های تنظیمات YAML"""
        if not os.path.exists(path):
            logger.error(f"❌ تنظیماتی در مسیر {path} پیدا نشد!")
            raise FileNotFoundError(f"تنظیماتی در مسیر {path} پیدا نشد!")
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _replace_env_vars(self, config_dict):
        """
        پیمایش هوشمند و جایگزینی مقادیر ${VAR} با Environment Variables واقعی سرور
        """
        pattern = re.compile(r"\$\{(.+?)\}")
        
        def replace(value):
            if isinstance(value, str):
                match = pattern.match(value)
                if match:
                    env_var = match.group(1)
                    return os.getenv(env_var, "")
            return value

        if isinstance(config_dict, dict):
            return {k: self._replace_env_vars(replace(v)) for k, v in config_dict.items()}
        elif isinstance(config_dict, list):
            return [self._replace_env_vars(replace(v)) for v in config_dict]
        
        return replace(config_dict)

    def get_mssql_engine(self):
        """ساخت کانکشن استرینگ و موتور اتصال به دیتابیس مادر (SQL Server)"""
        try:
            cfg = self.db_config["source_databases"]["mssql_pharma"]
            connection_url = (
                f"mssql+pyodbc://{cfg['user']}:{quote_plus(cfg['password'])}@{cfg['host']}:{cfg['port']}/{cfg['database']}"
                f"?driver={cfg['driver'].replace(' ', '+')}"
            )
            # ترکیب pool_pre_ping و fast_executemany پایداری و سرعت لود از منبع را تضمین می‌کند
            return create_engine(connection_url, fast_executemany=True, pool_pre_ping=True)
        except Exception as e:
            logger.error(f"❌ خطا در ایجاد موتور اتصال SQL Server: {str(e)}")
            raise e

    def get_postgres_engine(self):
        """ساخت موتور اتصال به انبار داده (PostgreSQL)"""
        try:
            cfg = self.db_config["target_databases"]["dw_postgres"]
            connection_url = f"postgresql://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}"
            return create_engine(connection_url, pool_pre_ping=True)
        except Exception as e:
            logger.error(f"❌ خطا در ایجاد موتور اتصال PostgreSQL: {str(e)}")
            raise e