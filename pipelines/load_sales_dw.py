"""
بارگذاری داده‌های فروش در Data Warehouse
نسخه نهایی با query های تست شده و جواب داده
"""

import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from typing import Optional, Dict
from core.engine.extractor import DataExtractor
from core.engine.transformer import DataTransformer
from core.engine.loader import DataLoader
from core.utils.jalali import JalaliCalendar
from core.utils.logging import setup_logger
from sqlalchemy import text

logger = setup_logger("load_sales_dw")

# ============================================================
# نگاشت دقیق ستون‌ها - بر اساس schema واقعی
# ============================================================

HEADER_COLUMN_MAPPING = {
    'ccDarkhastFaktor': 'sales_header_id',
    'Sal': 'year',
    'ccMoshtary': 'customer_id',
    'ccForoshandeh': 'salesman_id',
    'ccMarkazPakhsh': 'distribution_center_id',
    'ccGorohForosh': 'sales_group_id',
    'ShomarehFaktor': 'invoice_number',
    'TarikhFaktor': 'invoice_date',
    'MablaghKolFaktor': 'gross_amount',
    'MablaghTakhfifFaktorTitr': 'header_discount_amount',
    'MablaghTakhfifFaktorSatr': 'line_discount_amount',
    'MablaghEzafat': 'additional_amount',
    'MablaghKhalesFaktor': 'net_amount',
    'SumMaliat': 'tax_amount',
    'SumAvarez': 'duty_amount',
    'CodeVazeiat': 'status_code',
    'DateVorod': 'modified_date',
    'NoeFaktor': 'invoice_type',
    'ccDorehMaly': 'fiscal_period_id',
}

DETAIL_COLUMN_MAPPING = {
    'ccDarkhastFaktorSatr': 'sales_detail_id',
    'ccDarkhastFaktor': 'sales_header_id',
    'Sal': 'year',
    'ccKala': 'product_id',
    'ccKalaCode': 'product_code_id',
    'ShomarehBach': 'batch_number',
    'TarikhTolid': 'production_date',
    'TarikhEngheza': 'expiry_date',
    'Tedad1': 'quantity_pack',
    'Tedad2': 'quantity_box',
    'Tedad3': 'quantity_unit',
    'MablaghForosh': 'unit_price',
    'MablaghTakhfifFaktor': 'discount_amount',
    'Maliat': 'tax_amount',
    'Avarez': 'duty_amount',
    'MablaghForoshKhalesKala': 'net_line_amount',
    'DateVorod': 'modified_date',
    'CodeVazeiat': 'status_code',
}

NUMERIC_COLUMNS_HEADER = [
    'gross_amount', 'header_discount_amount', 'line_discount_amount',
    'additional_amount', 'net_amount', 'tax_amount', 'duty_amount'
]

NUMERIC_COLUMNS_DETAIL = [
    'quantity_pack', 'quantity_box', 'quantity_unit',
    'unit_price', 'discount_amount', 'tax_amount',
    'duty_amount', 'net_line_amount'
]


# ============================================================
# توابع نگاشت و تبدیل
# ============================================================

def map_header_to_fact(chunk: pd.DataFrame) -> pd.DataFrame:
    """تبدیل هدر فاکتور از schema منبع به schema مقصد"""
    df = chunk.copy()
    
    available_source_cols = [c for c in HEADER_COLUMN_MAPPING.keys() if c in df.columns]
    
    if not available_source_cols:
        logger.warning("⚠️ هیچ ستون قابل نگاشتی در هدر فاکتور پیدا نشد")
        return pd.DataFrame()
    
    mapping_subset = {k: v for k, v in HEADER_COLUMN_MAPPING.items() if k in df.columns}
    df = df[list(mapping_subset.keys())].rename(columns=mapping_subset)
    df['etl_loaded_at'] = pd.Timestamp.utcnow()
    
    return df


def map_detail_to_fact(chunk: pd.DataFrame) -> pd.DataFrame:
    """تبدیل ردیف فاکتور از schema منبع به schema مقصد"""
    df = chunk.copy()
    
    available_source_cols = [c for c in DETAIL_COLUMN_MAPPING.keys() if c in df.columns]
    
    if not available_source_cols:
        logger.warning("⚠️ هیچ ستون قابل نگاشتی در ردیف فاکتور پیدا نشد")
        return pd.DataFrame()
    
    mapping_subset = {k: v for k, v in DETAIL_COLUMN_MAPPING.items() if k in df.columns}
    df = df[list(mapping_subset.keys())].rename(columns=mapping_subset)
    
    if 'quantity_unit' in df.columns:
        df['total_quantity'] = df['quantity_unit'].fillna(0)
    elif 'quantity_pack' in df.columns:
        df['total_quantity'] = df['quantity_pack'].fillna(0)
    else:
        df['total_quantity'] = 0
    
    if 'net_line_amount' not in df.columns or df['net_line_amount'].isna().all():
        df['net_line_amount'] = (
            df.get('unit_price', 0).fillna(0) * df['total_quantity'].fillna(0)
            - df.get('discount_amount', 0).fillna(0)
            + df.get('tax_amount', 0).fillna(0)
            + df.get('duty_amount', 0).fillna(0)
        )
    
    df['etl_loaded_at'] = pd.Timestamp.utcnow()
    
    return df


def validate_header_data(df: pd.DataFrame) -> pd.DataFrame:
    """اعتبارسنجی داده‌های هدر فاکتور"""
    if df.empty:
        return df
    
    null_customer = df['customer_id'].isna() if 'customer_id' in df.columns else pd.Series(False)
    null_salesman = df['salesman_id'].isna() if 'salesman_id' in df.columns else pd.Series(False)
    
    invalid_mask = null_customer | null_salesman
    if invalid_mask.any():
        logger.warning(f"⚠️ {invalid_mask.sum()} رکورد بدون مشتری/فروشنده حذف شد")
        df = df[~invalid_mask]
    
    if 'net_amount' in df.columns:
        neg_mask = df['net_amount'] < 0
        if neg_mask.any():
            logger.warning(f"⚠️ {neg_mask.sum()} فاکتور با مبلغ خالص منفی - صفر شد")
            df.loc[neg_mask, 'net_amount'] = 0
    
    return df


def validate_detail_data(df: pd.DataFrame) -> pd.DataFrame:
    """اعتبارسنجی داده‌های ردیف فاکتور"""
    if df.empty:
        return df
    
    if 'product_id' in df.columns:
        null_product = df['product_id'].isna()
        if null_product.any():
            logger.warning(f"⚠️ {null_product.sum()} ردیف بدون محصول حذف شد")
            df = df[~null_product]
    
    if 'total_quantity' in df.columns:
        zero_qty = df['total_quantity'] <= 0
        if zero_qty.any():
            logger.warning(f"⚠️ {zero_qty.sum()} ردیف با مقدار صفر حذف شد")
            df = df[~zero_qty]
    
    if 'unit_price' in df.columns:
        neg_price = df['unit_price'] < 0
        if neg_price.any():
            logger.warning(f"⚠️ {neg_price.sum()} ردیف با قیمت منفی - صفر شد")
            df.loc[neg_price, 'unit_price'] = 0
    
    return df


# ============================================================
# بارگذاری با Query های تست شده
# ============================================================

def run_load_sales_headers(chunk_size: int = 50000, from_date: str = None, to_date: str = None) -> int:
    """
    استخراج و بارگذاری هدر فاکتورهای فروش با query تست شده
    
    Args:
        chunk_size: اندازه هر chunk
        from_date: تاریخ شروع (پیش‌فرض: همه داده‌ها)
        to_date: تاریخ پایان (پیش‌فرض: همه داده‌ها)
    
    Returns:
        تعداد کل رکوردهای بارگذاری شده
    """
    logger.info("=" * 60)
    logger.info("🔄 شروع بارگذاری هدر فاکتورهای فروش")
    logger.info("=" * 60)
    
    extractor = DataExtractor()
    transformer = DataTransformer(
        numeric_columns=['MablaghKolFaktor', 'MablaghKhalesFaktor',
                        'MablaghTakhfifFaktorTitr', 'MablaghTakhfifFaktorSatr',
                        'SumMaliat', 'SumAvarez'],
        date_columns=['TarikhFaktor', 'DateVorod']
    )
    loader = DataLoader()
    
    # ⭐ Query تست شده و جواب داده
    if from_date and to_date:
        query = f"""
        SELECT * FROM Sales.DarkhastFaktor
        WHERE TarikhFaktor >= '{from_date}' AND TarikhFaktor <= '{to_date}'
        ORDER BY TarikhFaktor
        """
        logger.info(f"📅 بازه: {from_date} تا {to_date}")
    else:
        query = """
        SELECT * FROM Sales.DarkhastFaktor
        ORDER BY TarikhFaktor
        """
        logger.info("📅 بازه: همه داده‌ها")
    
    total_rows = 0
    chunk_count = 0
    
    try:
        for chunk in pd.read_sql_query(query, extractor.src_engine, chunksize=chunk_size):
            if chunk.empty:
                continue
            
            chunk_count += 1
            
            # تبدیل و پاکسازی
            chunk = transformer.clean_basic_data(chunk)
            chunk = transformer.handle_missing_numeric(
                chunk,
                ['MablaghKolFaktor', 'MablaghKhalesFaktor',
                 'MablaghTakhfifFaktorTitr', 'MablaghTakhfifFaktorSatr',
                 'SumMaliat', 'SumAvarez'],
                default_value=0.0
            )
            
            # نگاشت به schema مقصد
            fact_df = map_header_to_fact(chunk)
            
            if fact_df.empty:
                continue
            
            # اعتبارسنجی
            fact_df = validate_header_data(fact_df)
            
            # مدیریت مقادیر عددی
            for col in NUMERIC_COLUMNS_HEADER:
                if col in fact_df.columns:
                    fact_df[col] = pd.to_numeric(fact_df[col], errors='coerce').fillna(0)
            
            # بارگذاری
            loader.bulk_copy(df=fact_df, target_table='fact_sales_header')
            
            chunk_rows = len(fact_df)
            total_rows += chunk_rows
            logger.info(f"  📦 Chunk #{chunk_count}: {chunk_rows:,} هدر فاکتور بارگذاری شد")
        
        logger.info(f"✅ مجموع: {total_rows:,} هدر فاکتور بارگذاری شد")
        return total_rows
        
    except Exception as e:
        logger.error(f"❌ خطا در بارگذاری هدر فاکتورها: {e}")
        raise


def run_load_sales_details(chunk_size: int = 50000, from_date: str = None, to_date: str = None) -> int:
    """
    استخراج و بارگذاری ردیف فاکتورهای فروش با query تست شده
    
    Args:
        chunk_size: اندازه هر chunk
        from_date: تاریخ شروع
        to_date: تاریخ پایان
    
    Returns:
        تعداد کل رکوردهای بارگذاری شده
    """
    logger.info("=" * 60)
    logger.info("🔄 شروع بارگذاری ردیف فاکتورهای فروش")
    logger.info("=" * 60)
    
    extractor = DataExtractor()
    transformer = DataTransformer(
        numeric_columns=['MablaghForosh', 'MablaghTakhfifFaktor',
                        'Maliat', 'Avarez', 'Tedad1', 'Tedad2', 'Tedad3',
                        'MablaghForoshKhalesKala'],
        date_columns=['TarikhFaktor', 'TarikhTolid', 'TarikhEngheza', 'DateVorod']
    )
    loader = DataLoader()
    
    # ⭐ Query تست شده
    if from_date and to_date:
        query = f"""
        SELECT * FROM Sales.DarkhastFaktorSatr
        WHERE TarikhFaktor >= '{from_date}' AND TarikhFaktor <= '{to_date}'
        ORDER BY TarikhFaktor
        """
        logger.info(f"📅 بازه: {from_date} تا {to_date}")
    else:
        query = """
        SELECT * FROM Sales.DarkhastFaktorSatr
        ORDER BY TarikhFaktor
        """
        logger.info("📅 بازه: همه داده‌ها")
    
    total_rows = 0
    chunk_count = 0
    
    try:
        for chunk in pd.read_sql_query(query, extractor.src_engine, chunksize=chunk_size):
            if chunk.empty:
                continue
            
            chunk_count += 1
            
            # تبدیل و پاکسازی
            chunk = transformer.clean_basic_data(chunk)
            chunk = transformer.handle_missing_numeric(
                chunk,
                ['MablaghForosh', 'MablaghTakhfifFaktor', 'Maliat', 'Avarez',
                 'Tedad1', 'Tedad2', 'Tedad3', 'MablaghForoshKhalesKala'],
                default_value=0.0
            )
            
            # نگاشت
            fact_df = map_detail_to_fact(chunk)
            
            if fact_df.empty:
                continue
            
            # اعتبارسنجی
            fact_df = validate_detail_data(fact_df)
            
            # مدیریت مقادیر عددی
            for col in NUMERIC_COLUMNS_DETAIL:
                if col in fact_df.columns:
                    fact_df[col] = pd.to_numeric(fact_df[col], errors='coerce').fillna(0)
            
            # بارگذاری
            loader.bulk_copy(df=fact_df, target_table='fact_sales_detail')
            
            chunk_rows = len(fact_df)
            total_rows += chunk_rows
            logger.info(f"  📦 Chunk #{chunk_count}: {chunk_rows:,} ردیف فاکتور بارگذاری شد")
        
        logger.info(f"✅ مجموع: {total_rows:,} ردیف فاکتور بارگذاری شد")
        return total_rows
        
    except Exception as e:
        logger.error(f"❌ خطا در بارگذاری ردیف فاکتورها: {e}")
        raise


def run_load_sales_incremental(chunk_size: int = 50000, from_date: str = None, to_date: str = None) -> Dict:
    """
    اجرای کامل بارگذاری فروش
    
    Args:
        chunk_size: اندازه chunk
        from_date: تاریخ شروع (مثلاً '2026-04-21' برای ۱ اردیبهشت ۱۴۰۵)
        to_date: تاریخ پایان (مثلاً '2026-05-20' برای ۳۰ اردیبهشت ۱۴۰۵)
        
    Returns:
        گزارش اجرا
    """
    start_time = datetime.now()
    report = {
        'start_time': start_time.isoformat(),
        'headers': {'status': 'not_run', 'rows': 0, 'error': None},
        'details': {'status': 'not_run', 'rows': 0, 'error': None},
        'total_rows': 0,
        'status': 'unknown'
    }
    
    try:
        # فاز ۱: هدر فاکتورها
        try:
            header_rows = run_load_sales_headers(chunk_size, from_date, to_date)
            report['headers'] = {'status': 'success', 'rows': header_rows, 'error': None}
            report['total_rows'] += header_rows
        except Exception as e:
            report['headers'] = {'status': 'failed', 'rows': 0, 'error': str(e)}
            report['status'] = 'partial'
            logger.error(f"فاز ۱ (هدر) با خطا مواجه شد: {e}")
        
        # فاز ۲: ردیف فاکتورها
        try:
            detail_rows = run_load_sales_details(chunk_size, from_date, to_date)
            report['details'] = {'status': 'success', 'rows': detail_rows, 'error': None}
            report['total_rows'] += detail_rows
        except Exception as e:
            report['details'] = {'status': 'failed', 'rows': 0, 'error': str(e)}
            report['status'] = 'partial'
            logger.error(f"فاز ۲ (ردیف) با خطا مواجه شد: {e}")
        
        if report['status'] != 'partial':
            report['status'] = 'success'
        
        end_time = datetime.now()
        report['end_time'] = end_time.isoformat()
        report['duration_seconds'] = (end_time - start_time).total_seconds()
        
        logger.info("=" * 60)
        logger.info(f"📊 گزارش نهایی بارگذاری فروش:")
        logger.info(f"   هدر: {report['headers']['status']} - {report['headers']['rows']:,} رکورد")
        logger.info(f"   ردیف: {report['details']['status']} - {report['details']['rows']:,} رکورد")
        logger.info(f"   مجموع: {report['total_rows']:,} رکورد")
        logger.info(f"   زمان: {report['duration_seconds']:.2f} ثانیه")
        logger.info("=" * 60)
        
        return report
        
    except Exception as e:
        logger.error(f"🚨 خطای بحرانی: {e}")
        report['status'] = 'failed'
        report['error'] = str(e)
        raise


def aggregate_daily_sales(target_date: date = None) -> Dict:
    """
    تجمیع فروش روزانه - همون KPI که تست شده
    
    Args:
        target_date: تاریخ مورد نظر (پیش‌فرض: دیروز)
    
    Returns:
        نتیجه تجمیع
    """
    loader = DataLoader()
    
    if target_date is None:
        target_date = date.today() - timedelta(days=1)
    
    date_id = int(target_date.strftime('%Y%m%d'))
    
    logger.info(f"📊 تجمیع فروش برای تاریخ {date_id}")
    
    agg_sql = """
    INSERT INTO agg_daily_sales (date_id, total_net, total_units, orders_count)
    SELECT 
        :date_id as date_id,
        COALESCE(SUM(h.net_amount), 0) as total_net,
        COALESCE(SUM(d.total_quantity), 0) as total_units,
        COUNT(DISTINCT h.sales_header_id) as orders_count
    FROM fact_sales_header h
    LEFT JOIN fact_sales_detail d ON h.sales_header_id = d.sales_header_id 
        AND h.year = d.year
    WHERE DATE(h.invoice_date) = :target_date
    ON CONFLICT (date_id) 
    DO UPDATE SET
        total_net = EXCLUDED.total_net,
        total_units = EXCLUDED.total_units,
        orders_count = EXCLUDED.orders_count,
        updated_at = CURRENT_TIMESTAMP
    RETURNING total_net, total_units, orders_count;
    """
    
    try:
        with loader.tgt_engine.connect() as conn:
            result = conn.execute(
                text(agg_sql), 
                {'date_id': date_id, 'target_date': target_date.isoformat()}
            ).fetchone()
            conn.commit()
        
        if result:
            logger.info(f"✅ تجمیع روز {date_id}: "
                       f"فروش={result[0]:,.0f}, "
                       f"تعداد={result[1]:,.0f}, "
                       f"فاکتور={result[2]}")
            return {
                'date_id': date_id,
                'total_net': float(result[0]),
                'total_units': float(result[1]),
                'orders_count': int(result[2])
            }
    except Exception as e:
        logger.error(f"❌ خطا در تجمیع فروش: {e}")
        raise


# ============================================================
# KPI های تست شده (همون query هایی که جواب دادن)
# ============================================================

def get_sales_kpi(from_date: str = '2026-04-21', to_date: str = '2026-05-20') -> Dict:
    """
    دریافت KPI های اصلی فروش - همون query تست شده
    
    Args:
        from_date: تاریخ شروع (پیش‌فرض: ۱ اردیبهشت ۱۴۰۵)
        to_date: تاریخ پایان (پیش‌فرض: ۳۰ اردیبهشت ۱۴۰۵)
    
    Returns:
        دیکشنری KPI ها
    """
    loader = DataLoader()
    
    query = f"""
    SELECT 
        COUNT(DISTINCT sales_header_id) AS tedad_faktor,
        COUNT(DISTINCT customer_id) AS tedad_moshtary,
        COALESCE(SUM(net_amount), 0) AS forosh_khales,
        COALESCE(SUM(gross_amount), 0) AS forosh_nakhales,
        COALESCE(SUM(header_discount_amount) + SUM(line_discount_amount), 0) AS takhfif,
        COALESCE(AVG(net_amount), 0) AS miangin_faktor
    FROM fact_sales_header
    WHERE invoice_date >= '{from_date}'
        AND invoice_date <= '{to_date}'
    """
    
    try:
        with loader.tgt_engine.connect() as conn:
            result = conn.execute(text(query)).fetchone()
            conn.commit()
        
        kpi = {
            'tedad_faktor': int(result[0]),
            'tedad_moshtary': int(result[1]),
            'forosh_khales': float(result[2]),
            'forosh_nakhales': float(result[3]),
            'takhfif': float(result[4]),
            'miangin_faktor': float(result[5]),
            'darsad_takhfif': (float(result[4]) / float(result[3]) * 100) if float(result[3]) > 0 else 0
        }
        
        logger.info(f"📊 KPI فروش:")
        logger.info(f"   فاکتور: {kpi['tedad_faktor']:,}")
        logger.info(f"   فروش خالص: {kpi['forosh_khales']/1e9:,.2f} میلیارد تومان")
        logger.info(f"   تخفیف: {kpi['darsad_takhfif']:.1f}%")
        
        return kpi
        
    except Exception as e:
        logger.error(f"❌ خطا در محاسبه KPI: {e}")
        raise


def get_sales_by_status(from_date: str = '2026-04-21', to_date: str = '2026-05-20') -> pd.DataFrame:
    """
    فروش بر اساس وضعیت فاکتور - همون query تست شده
    
    Args:
        from_date: تاریخ شروع
        to_date: تاریخ پایان
    
    Returns:
        DataFrame وضعیت‌ها
    """
    loader = DataLoader()
    
    query = f"""
    SELECT 
        status_code,
        COUNT(DISTINCT sales_header_id) AS tedad,
        COALESCE(SUM(net_amount), 0) AS forosh
    FROM fact_sales_header
    WHERE invoice_date >= '{from_date}'
        AND invoice_date <= '{to_date}'
    GROUP BY status_code
    ORDER BY forosh DESC
    """
    
    try:
        with loader.tgt_engine.connect() as conn:
            df = pd.read_sql(text(query), conn)
            conn.commit()
        return df
    except Exception as e:
        logger.error(f"❌ خطا: {e}")
        return pd.DataFrame()


def get_sales_by_group(from_date: str = '2026-04-21', to_date: str = '2026-05-20') -> pd.DataFrame:
    """
    فروش بر اساس گروه فروش (Top 5) - همون query تست شده
    
    Args:
        from_date: تاریخ شروع
        to_date: تاریخ پایان
    
    Returns:
        DataFrame گروه‌ها
    """
    loader = DataLoader()
    
    query = f"""
    SELECT 
        sales_group_id,
        COUNT(DISTINCT sales_header_id) AS tedad,
        COALESCE(SUM(net_amount), 0) AS forosh
    FROM fact_sales_header
    WHERE invoice_date >= '{from_date}'
        AND invoice_date <= '{to_date}'
        AND sales_group_id IS NOT NULL
    GROUP BY sales_group_id
    ORDER BY forosh DESC
    LIMIT 5
    """
    
    try:
        with loader.tgt_engine.connect() as conn:
            df = pd.read_sql(text(query), conn)
            conn.commit()
        return df
    except Exception as e:
        logger.error(f"❌ خطا: {e}")
        return pd.DataFrame()