"""
پایپ‌لاین بارگذاری بعد فروشنده (dim_employee) - مطابق با ساختار واقعی Sales.Foroshandeh
"""

import pandas as pd
from sqlalchemy import text
from datetime import datetime
from io import StringIO
import csv
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.logging import setup_logger

logger = setup_logger("dim_employee")

def clean_text(text, max_length=None):
    if pd.isna(text) or text is None:
        return ''
    cleaned = str(text).replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
    if max_length and len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    return cleaned

def run_dim_employee_pipeline():
    """
    بارگذاری بعد فروشنده از Sales.Foroshandeh
    ستون‌های مهم: ccForoshandeh, ccAfrad, ccMarkazPakhsh
    نکته: باید به جدول Afrad هم JOIN بزنیم برای نام فروشنده
    """
    logger.info("=" * 60)
    logger.info("🔄 شروع پایپ‌لاین بعد فروشنده (dim_employee)...")
    start_time = datetime.now()
    
    extractor = DataExtractor()
    loader = DataLoader()
    
    try:
        # 1. استخراج از SQL Server
        # ابتدا سعی می‌کنیم به Afrad JOIN بزنیم برای نام
        query = """
            SELECT 
                f.ccForoshandeh,
                f.ccAfrad,
                f.ccMarkazPakhsh,
                f.ccGorohForosh,
                f.CodeVazeiat,
                f.CodeForoshandehOld,
                ISNULL(a.FullName, CAST(f.ccForoshandeh AS VARCHAR) + ' - فروشنده') AS FullName,
                ISNULL(a.Meliat, '') AS Meliat,
                ISNULL(a.JamdarName, '') AS JamdarName,
                ISNULL(a.IsInListBank, 0) AS IsInListBank
            FROM Sales.Foroshandeh f
            LEFT JOIN HR.Afrad a ON f.ccAfrad = a.ccAfrad
            WHERE f.ccForoshandeh IS NOT NULL
            ORDER BY f.ccForoshandeh
        """
        
        logger.info("📥 در حال استخراج فروشندگان از SQL Server...")
        
        try:
            df_src = pd.read_sql_query(query, extractor.src_engine)
        except Exception as e:
            logger.warning(f"⚠️ JOIN با Afrad ناموفق: {str(e)[:100]}")
            # کوئری بدون JOIN
            query = """
                SELECT 
                    ccForoshandeh,
                    ccAfrad,
                    ccMarkazPakhsh,
                    CodeVazeiat,
                    CAST(ccForoshandeh AS VARCHAR) + ' - فروشنده' AS FullName,
                    '' AS Meliat,
                    '' AS JamdarName,
                    0 AS IsInListBank
                FROM Sales.Foroshandeh
                WHERE ccForoshandeh IS NOT NULL
                ORDER BY ccForoshandeh
            """
            df_src = pd.read_sql_query(query, extractor.src_engine)
        
        if df_src.empty:
            logger.warning("⚠️ هیچ فروشنده‌ای در منبع یافت نشد.")
            return 0
        
        logger.info(f"📋 {len(df_src):,} فروشنده استخراج شد.")
        
        # 2. پاکسازی و تبدیل
        df_dim = pd.DataFrame()
        df_dim['cc_afrad'] = df_src['ccAfrad'].fillna(df_src['ccForoshandeh']).astype(int)
        df_dim['full_name'] = df_src['FullName'].apply(lambda x: clean_text(x, 150))
        df_dim['is_in_list_bank'] = df_src['IsInListBank'].astype(bool)
        df_dim['meliat'] = df_src['Meliat'].apply(lambda x: clean_text(x, 50))
        df_dim['jamdar_name'] = df_src['JamdarName'].apply(lambda x: clean_text(x, 100))
        df_dim['is_active'] = df_src['CodeVazeiat'].apply(
            lambda x: True if x == 3 else False
        )
        
        # 3. خواندن داده‌های موجود
        with loader.tgt_engine.connect() as conn:
            existing = pd.read_sql(
                'SELECT employee_key, cc_afrad FROM dim_employee', 
                conn
            )
            logger.info(f"📊 {len(existing):,} فروشنده در انبار داده موجود است.")
        
        # 4. شناسایی جدید vs موجود
        new_employees = df_dim[~df_dim['cc_afrad'].isin(existing['cc_afrad'])]
        existing_employees = df_dim[df_dim['cc_afrad'].isin(existing['cc_afrad'])]
        
        logger.info(f"🆕 فروشندگان جدید: {len(new_employees):,}")
        
        total_new = 0
        total_updated = 0
        
        with loader.tgt_engine.begin() as conn:
            # 5. درج فروشندگان جدید
            if not new_employees.empty:
                insert_count = 0
                for _, row in new_employees.iterrows():
                    try:
                        conn.execute(
                            text("""
                                INSERT INTO dim_employee (cc_afrad, full_name, is_in_list_bank, 
                                    meliat, jamdar_name, is_active)
                                VALUES (:cc_afrad, :name, :bank, :meliat, :jamdar, :active)
                                ON CONFLICT (cc_afrad) DO NOTHING
                            """),
                            {
                                "cc_afrad": int(row['cc_afrad']),
                                "name": row['full_name'],
                                "bank": bool(row['is_in_list_bank']),
                                "meliat": row['meliat'] if row['meliat'] else None,
                                "jamdar": row['jamdar_name'] if row['jamdar_name'] else None,
                                "active": bool(row['is_active'])
                            }
                        )
                        insert_count += 1
                    except Exception:
                        pass
                
                total_new = insert_count
                logger.info(f"✨ {total_new:,} فروشنده جدید اضافه شد.")
            
            # 6. به‌روزرسانی
            if not existing_employees.empty:
                update_count = 0
                for _, row in existing_employees.iterrows():
                    try:
                        result = conn.execute(
                            text("""
                                UPDATE dim_employee 
                                SET full_name = :name,
                                    is_active = :active,
                                    updated_at = NOW()
                                WHERE cc_afrad = :code
                            """),
                            {
                                "code": int(row['cc_afrad']),
                                "name": row['full_name'],
                                "active": bool(row['is_active'])
                            }
                        )
                        if result.rowcount > 0:
                            update_count += 1
                    except Exception:
                        pass
                
                total_updated = update_count
                if update_count > 0:
                    logger.info(f"🔄 {update_count:,} فروشنده به‌روزرسانی شد.")
        
        # 7. گزارش
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"""
        ╔══════════════════════════════════════╗
        ║   ✅ بعد فروشنده با موفقیت لود شد   ║
        ╠══════════════════════════════════════╣
        ║ جدید: {total_new:>20,}  ║
        ║ زمان: {duration:>17.1f} ثانیه ║
        ╚══════════════════════════════════════╝
        """)
        
        return total_new + total_updated
        
    except Exception as e:
        logger.error(f"❌ خطا در پایپ‌لاین فروشنده: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    run_dim_employee_pipeline()