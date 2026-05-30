"""
پایپ‌لاین افزایشی بعد کالا - نسخه Production
فقط تغییرات جدید را پردازش می‌کند
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
from sqlalchemy import text
from datetime import datetime, timedelta
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.checkpoint import ETLCheckpoint
from core.utils.logging import setup_logger

logger = setup_logger("dim_product_inc")

def clean_text(text, max_length=None):
    """پاکسازی متن از کاراکترهای مخرب"""
    if pd.isna(text) or text is None:
        return ''
    cleaned = str(text).replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
    if max_length and len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    return cleaned

def format_date_for_sql_server(date_value):
    """
    تبدیل تاریخ به فرمت قابل قبول SQL Server
    ورودی: datetime یا str
    خروجی: str با فرمت YYYY-MM-DD HH:MM:SS
    """
    if date_value is None:
        return None
    
    if isinstance(date_value, datetime):
        return date_value.strftime('%Y-%m-%d %H:%M:%S')
    
    # اگر string است، میکروثانیه را حذف کن
    date_str = str(date_value)
    if '.' in date_str:
        date_str = date_str.split('.')[0]
    if 'T' in date_str:
        date_str = date_str.replace('T', ' ')
    
    return date_str[:19]  # حداکثر 19 کاراکتر: YYYY-MM-DD HH:MM:SS

def run_dim_product_pipeline_incremental():
    """
    بارگذاری افزایشی بعد کالا
    - اجرای اول: کل داده را می‌خواند
    - اجراهای بعدی: فقط کالاهایی که ModifiedDate آن‌ها از آخرین اجرا جدیدتر است
    """
    logger.info("=" * 60)
    logger.info("🔄 شروع پایپ‌لاین افزایشی بعد کالا...")
    start_time = datetime.now()
    
    extractor = DataExtractor()
    loader = DataLoader()
    checkpoint = ETLCheckpoint(loader)
    
    pipeline_name = "dim_product_incremental"
    
    try:
        # 1. خواندن آخرین وضعیت اجرا
        last_run = checkpoint.get_last_success(pipeline_name)
        
        if last_run and last_run.get('last_from_value'):
            last_modified = format_date_for_sql_server(last_run['last_from_value'])
            logger.info(f"📌 آخرین اجرای موفق: {last_run['last_success_at']}")
            logger.info(f"📌 آخرین ModifiedDate پردازش شده: {last_modified}")
        else:
            # اولین اجرا: از ۱۰ سال پیش شروع کن
            last_modified = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d %H:%M:%S')
            logger.info(f"🆕 اولین اجرا - پردازش کل داده‌ها از {last_modified}")
        
        # 2. استخراج فقط کالاهای تغییر کرده از SQL Server
        query = f"""
            SELECT 
                ccKala,
                NameKala,
                CodeJenerik,
                BarCode,
                CodeRasmiDaroo,
                ccTaminkonandeh,
                ccTolidkonandeh,
                CodeVazeiat,
                ModifiedDate
            FROM Warehouse.Kala
            WHERE ccKala IS NOT NULL
              AND ModifiedDate >= CONVERT(DATETIME, '{last_modified}', 120)
            ORDER BY ModifiedDate
        """
        
        logger.info("📥 در حال استخراج کالاهای تغییر کرده...")
        df_src = pd.read_sql_query(query, extractor.src_engine)
        
        if df_src.empty:
            logger.info("✅ هیچ کالای جدید/تغییر کرده‌ای یافت نشد.")
            checkpoint.save_checkpoint(
                pipeline_name, 'SUCCESS', 0,
                from_value=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                to_value=datetime.now().strftime('%Y-%m-%d')
            )
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"⏱️ زمان اجرا: {duration:.1f} ثانیه")
            return 0
        
        # ذخیره آخرین ModifiedDate برای اجرای بعدی
        max_modified = df_src['ModifiedDate'].max()
        logger.info(f"📋 {len(df_src):,} کالا تغییر کرده (از {last_modified} تا {max_modified})")
        
        # 3. پاکسازی و تبدیل
        df_dim = pd.DataFrame()
        df_dim['cc_kala'] = df_src['ccKala'].astype(int)
        df_dim['name_kala'] = df_src['NameKala'].apply(lambda x: clean_text(x, 256))
        df_dim['generic_code'] = df_src['CodeJenerik'].apply(
            lambda x: str(int(x)) if pd.notna(x) and x != 0 else None
        )
        df_dim['cc_tamin_konandeh'] = pd.to_numeric(df_src['ccTaminkonandeh'], errors='coerce')
        df_dim['is_active'] = df_src['CodeVazeiat'].apply(lambda x: True if x == 3 else False)
        
        # 4. پردازش با UPSERT (درج یا به‌روزرسانی)
        total_processed = 0
        batch_size = 500
        errors = 0
        
        with loader.tgt_engine.begin() as conn:
            for i in range(0, len(df_dim), batch_size):
                batch = df_dim.iloc[i:i+batch_size]
                
                for _, row in batch.iterrows():
                    try:
                        conn.execute(
                            text("""
                                INSERT INTO dim_product (cc_kala, name_kala, generic_code, 
                                    cc_tamin_konandeh, is_active, updated_at)
                                VALUES (:cc_kala, :name, :generic, :tamin, :active, NOW())
                                ON CONFLICT (cc_kala) DO UPDATE SET
                                    name_kala = EXCLUDED.name_kala,
                                    generic_code = EXCLUDED.generic_code,
                                    cc_tamin_konandeh = EXCLUDED.cc_tamin_konandeh,
                                    is_active = EXCLUDED.is_active,
                                    updated_at = NOW()
                            """),
                            {
                                "cc_kala": int(row['cc_kala']),
                                "name": row['name_kala'],
                                "generic": row['generic_code'],
                                "tamin": int(row['cc_tamin_konandeh']) if pd.notna(row['cc_tamin_konandeh']) else None,
                                "active": bool(row['is_active'])
                            }
                        )
                        total_processed += 1
                    except Exception as e:
                        errors += 1
                        if errors <= 5:
                            logger.debug(f"⚠️ خطا در رکورد {row['cc_kala']}: {str(e)[:80]}")
                
                if (i // batch_size) % 10 == 0:
                    logger.debug(f"  ➜ {total_processed:,}/{len(df_dim):,} پردازش شد...")
        
        if errors > 0:
            logger.warning(f"⚠️ {errors} خطا در پردازش رکوردها (از {len(df_dim):,})")
        
        # 5. ذخیره checkpoint با فرمت تاریخ مناسب
        formatted_max_modified = format_date_for_sql_server(max_modified)
        checkpoint.save_checkpoint(
            pipeline_name, 'SUCCESS', total_processed,
            from_value=formatted_max_modified,
            to_value=datetime.now().strftime('%Y-%m-%d')
        )
        
        # 6. گزارش نهایی
        duration = (datetime.now() - start_time).total_seconds()
        rows_per_sec = total_processed / duration if duration > 0 else 0
        
        logger.info(f"""
        ╔══════════════════════════════════════╗
        ║  ✅ بعد کالا (افزایشی) لود شد      ║
        ╠══════════════════════════════════════╣
        ║ رکوردهای پردازش شده: {total_processed:>5}  ║
        ║ خطاها: {errors:>17}  ║
        ║ زمان: {duration:>15.1f} ثانیه ║
        ║ سرعت: {rows_per_sec:>15.0f} رکورد/ثانیه ║
        ╚══════════════════════════════════════╝
        """)
        
        return total_processed
        
    except Exception as e:
        logger.error(f"❌ خطا در پایپ‌لاین: {str(e)}", exc_info=True)
        checkpoint.save_checkpoint(
            pipeline_name, 'FAILED', 
            error_message=str(e)[:500]
        )
        raise


if __name__ == "__main__":
    run_dim_product_pipeline_incremental()