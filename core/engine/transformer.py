import pandas as pd
import numpy as np
from core.utils.jalali import JalaliCalendar


class DataTransformer:
    def __init__(self, schema_mapping: dict = None, date_columns: list = None, numeric_columns: list = None, lookups: dict = None):
        """Initializer accepts optional mappings and column lists used by transformer methods."""
        self.schema_mapping = schema_mapping or {}
        self.date_columns = date_columns or []
        self.numeric_columns = numeric_columns or []
        self.lookups = lookups or {}
        self.jalali = JalaliCalendar()

    def clean_basic_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """حذف نویزهای متداول فیلدهای متنی و یکپارچه‌سازی فضاهای خالی"""
        if df.empty:
            return df

        for col in df.select_dtypes(include=['object', 'string']).columns:
            df[col] = df[col].astype(str).str.strip()

        df = df.replace(r'^\s*$', np.nan, regex=True)
        df = df.replace(['NULL', 'null', 'None'], np.nan)
        return df

    def enforce_schema(self, df: pd.DataFrame, schema_mapping: dict) -> pd.DataFrame:
        """انطباق فیلدهای دیتابیس قدیمی با استانداردهای نوین لایه های لندینگ یا بعد انبار داده"""
        if df.empty or not schema_mapping:
            return df
        return df.rename(columns=schema_mapping)

    def handle_missing_numeric(self, df: pd.DataFrame, numeric_columns: list, default_value: float = 0.0) -> pd.DataFrame:
        """جلوگیری از خطاهای محاسباتی در فیلد مبالغ مالی پخش با کنترل مقادیر تهی عددی"""
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(default_value)
        return df

    def apply_lookups(self, df: pd.DataFrame, lookups: dict) -> pd.DataFrame:
        """اعمال نگاشت‌های کد -> مقدار (مثلاً نوع کالا، استان) با دیکشنری‌های نگاشت"""
        if df.empty or not lookups:
            return df
        for col, mapping in lookups.items():
            if col in df.columns:
                df[col] = df[col].map(mapping).fillna(df[col])
        return df

    def add_jalali_columns(self, df: pd.DataFrame, date_columns: list = None) -> pd.DataFrame:
        """برای هر ستون تاریخ مشخص شده ستون‌های کمکی شمسی را می‌سازد."""
        if df.empty:
            return df
        cols = date_columns or self.date_columns
        for col in cols:
            if col not in df.columns:
                continue
            # apply conversion row-wise but efficiently where possible
            attrs = df[col].apply(lambda v: self.jalali.get_jalali_attributes(v) if pd.notna(v) else {})
            if attrs.empty:
                continue
            # expand attributes into separate columns
            df[f"{col}_jalali_date_code"] = attrs.apply(lambda d: d.get("jalali_date_code"))
            df[f"{col}_jalali_full_date"] = attrs.apply(lambda d: d.get("jalali_full_date"))
            df[f"{col}_jalali_year"] = attrs.apply(lambda d: d.get("jalali_year"))
            df[f"{col}_jalali_month_no"] = attrs.apply(lambda d: d.get("jalali_month_no"))
            df[f"{col}_jalali_month_name"] = attrs.apply(lambda d: d.get("jalali_month_name"))
            df[f"{col}_jalali_day"] = attrs.apply(lambda d: d.get("jalali_day"))
            df[f"{col}_jalali_season"] = attrs.apply(lambda d: d.get("jalali_season"))
            df[f"{col}_is_weekend"] = attrs.apply(lambda d: d.get("is_weekend"))
        return df

    def validate_required_columns(self, df: pd.DataFrame, required_columns: list) -> bool:
        """بازگشت True اگر همه ستون‌های مورد نیاز در df وجود داشته باشند."""
        missing = [c for c in required_columns if c not in df.columns]
        return len(missing) == 0