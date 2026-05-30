"""
پایپ‌لاین بارگذاری بعد کالا (dim_product) - مطابق با ساختار واقعی SQL Server
"""

import pandas as pd
from sqlalchemy import text
from datetime import datetime
from io import StringIO
import csv
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.logging import setup_logger

logger = setup_logger("dim_product")

def clean_text(text, max_length=None):
    """پاکسازی متن از کاراکترهای مخرب"""
    if pd.isna(text) or text is None:
        return ''
    cleaned = str(text).replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
    if max_length and len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    return cleaned

def run_dim_product_pipeline():
    """
    بارگذاری بعد کالا با ستون‌های واقعی:
    ccKala, NameKala, CodeJenerik, BarCode, CodeRasmiDaroo,
    ccTaminkonandeh, ccTolidkonandeh
    """
    logger.info("=" * 60)
    logger.info("🔄 شروع پایپ‌لاین بعد کالا (dim_product)...")
    start_time = datetime.now()
    
    extractor = DataExtractor()
    loader = DataLoader()
    
    try:
        # 1. استخراج از SQL Server با نام ستون‌های واقعی
        query = """
            SELECT 
                ccKala,
                NameKala,
                CodeJenerik,
                BarCode,
                CodeRasmiDaroo,
                ccTaminkonandeh,
                ccTolidkonandeh,
                CodeVazeiat
            FROM Warehouse.Kala
            WHERE ccKala IS NOT NULL
            ORDER BY ccKala
        """
        
        logger.info("📥 در حال استخراج کالاها از SQL Server...")
        df_src = pd.read_sql_query(query, extractor.src_engine)
        
        if df_src.empty:
            logger.warning("⚠️ هیچ کالایی در منبع یافت نشد.")
            return 0
        
        logger.info(f"📋 {len(df_src):,} کالا استخراج شد.")
        
        # 2. پاکسازی و تبدیل داده‌ها
        df_dim = pd.DataFrame()
        df_dim['cc_kala'] = df_src['ccKala'].astype(int)
        df_dim['name_kala'] = df_src['NameKala'].apply(lambda x: clean_text(x, 256))
        df_dim['generic_code'] = df_src['CodeJenerik'].apply(
            lambda x: str(int(x)) if pd.notna(x) and x != 0 else None
        )
        df_dim['barcode'] = df_src['BarCode'].apply(lambda x: clean_text(x, 100))
        df_dim['code_rasmi_daroo'] = df_src['CodeRasmiDaroo'].apply(lambda x: clean_text(x, 100))
        df_dim['cc_tamin_konandeh'] = pd.to_numeric(df_src['ccTaminkonandeh'], errors='coerce')
        df_dim['cc_tolid_konandeh'] = pd.to_numeric(df_src['ccTolidkonandeh'], errors='coerce')
        
        # وضعیت کالا (3 = فعال)
        df_dim['is_active'] = df_src['CodeVazeiat'].apply(
            lambda x: True if x == 3 else False
        )
        
        # فیلدهایی که NULL هستند را آماده می‌کنیم
        df_dim['group_daraee_name'] = None
        df_dim['name_tamin_konandeh'] = None
        df_dim['name_tolid_konandeh'] = None
        
        # 3. خواندن داده‌های موجود در PostgreSQL
        with loader.tgt_engine.connect() as conn:
            existing = pd.read_sql(
                'SELECT product_key, cc_kala FROM dim_product', 
                conn
            )
            logger.info(f"📊 {len(existing):,} کالا در انبار داده موجود است.")
        
        # 4. شناسایی کالاهای جدید و موجود
        new_products = df_dim[~df_dim['cc_kala'].isin(existing['cc_kala'])]
        existing_products = df_dim[df_dim['cc_kala'].isin(existing['cc_kala'])]
        
        logger.info(f"🆕 کالاهای جدید: {len(new_products):,}")
        logger.info(f"🔄 کالاهای موجود: {len(existing_products):,}")
        
        total_new = 0
        total_updated = 0
        
        with loader.tgt_engine.begin() as conn:
            # 5. درج کالاهای جدید با COPY
            if not new_products.empty:
                output = StringIO()
                writer = csv.writer(output, delimiter='\t', quoting=csv.QUOTE_MINIMAL, 
                                  quotechar='"', escapechar='\\')
                
                for _, row in new_products.iterrows():
                    writer.writerow([
                        int(row['cc_kala']),
                        row['name_kala'],
                        row['generic_code'] if pd.notna(row['generic_code']) else None,
                        row['group_daraee_name'],
                        int(row['cc_tamin_konandeh']) if pd.notna(row['cc_tamin_konandeh']) else None,
                        row['name_tamin_konandeh'],
                        row['name_tolid_konandeh'],
                        bool(row['is_active']),
                        datetime.now(),
                        datetime.now()
                    ])
                
                output.seek(0)
                
                try:
                    with conn.connection.cursor() as cursor:
                        cursor.copy_from(
                            output,
                            'dim_product',
                            columns=('cc_kala', 'name_kala', 'generic_code', 'group_daraee_name',
                                    'cc_tamin_konandeh', 'name_tamin_konandeh', 'name_tolid_konandeh',
                                    'is_active', 'created_at', 'updated_at'),
                            null=''
                        )
                    total_new = len(new_products)
                    logger.info(f"✨ {total_new:,} کالای جدید با COPY اضافه شد.")
                except Exception as copy_error:
                    logger.warning(f"⚠️ خطا در COPY، استفاده از INSERT: {str(copy_error)[:100]}")
                    
                    # Fallback به INSERT
                    insert_count = 0
                    for _, row in new_products.iterrows():
                        try:
                            conn.execute(
                                text("""
                                    INSERT INTO dim_product (cc_kala, name_kala, generic_code, 
                                        cc_tamin_konandeh, is_active)
                                    VALUES (:cc_kala, :name_kala, :generic_code, 
                                        :cc_tamin_konandeh, :is_active)
                                    ON CONFLICT (cc_kala) DO NOTHING
                                """),
                                {
                                    "cc_kala": int(row['cc_kala']),
                                    "name_kala": row['name_kala'],
                                    "generic_code": row['generic_code'],
                                    "cc_tamin_konandeh": int(row['cc_tamin_konandeh']) if pd.notna(row['cc_tamin_konandeh']) else None,
                                    "is_active": bool(row['is_active'])
                                }
                            )
                            insert_count += 1
                        except Exception as insert_error:
                            logger.debug(f"⚠️ خطا در درج cc_kala={row['cc_kala']}: {str(insert_error)[:80]}")
                    
                    total_new = insert_count
                    logger.info(f"✨ {insert_count:,} کالای جدید با INSERT اضافه شد.")
            
            # 6. به‌روزرسانی کالاهای موجود
            if not existing_products.empty:
                update_count = 0
                for _, row in existing_products.iterrows():
                    try:
                        result = conn.execute(
                            text("""
                                UPDATE dim_product 
                                SET name_kala = :name_kala,
                                    generic_code = :generic_code,
                                    cc_tamin_konandeh = :cc_tamin_konandeh,
                                    is_active = :is_active,
                                    updated_at = NOW()
                                WHERE cc_kala = :cc_kala
                            """),
                            {
                                "cc_kala": int(row['cc_kala']),
                                "name_kala": row['name_kala'],
                                "generic_code": row['generic_code'],
                                "cc_tamin_konandeh": int(row['cc_tamin_konandeh']) if pd.notna(row['cc_tamin_konandeh']) else None,
                                "is_active": bool(row['is_active'])
                            }
                        )
                        if result.rowcount > 0:
                            update_count += 1
                    except Exception as update_error:
                        logger.debug(f"⚠️ خطا در به‌روزرسانی cc_kala={row['cc_kala']}: {str(update_error)[:80]}")
                
                total_updated = update_count
                if update_count > 0:
                    logger.info(f"🔄 {update_count:,} کالا به‌روزرسانی شد.")
        
        # 7. گزارش نهایی
        duration = (datetime.now() - start_time).total_seconds()
        total_processed = total_new + total_updated
        
        logger.info(f"""
        ╔══════════════════════════════════════╗
        ║     ✅ بعد کالا با موفقیت لود شد    ║
        ╠══════════════════════════════════════╣
        ║ کالاهای جدید: {total_new:>13,}  ║
        ║ به‌روزرسانی‌ها: {total_updated:>11,}  ║
        ║ کل پردازش: {total_processed:>15,}  ║
        ║ زمان: {duration:>17.1f} ثانیه ║
        ╚══════════════════════════════════════╝
        """)
        
        return total_processed
        
    except Exception as e:
        logger.error(f"❌ خطا در پایپ‌لاین کالا: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    run_dim_product_pipeline()