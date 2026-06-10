"""
اجرای تستی OBT Sales Pipeline
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import importlib.util
from datetime import datetime
from core.utils.logging import setup_logger

logger = setup_logger("obt_test_runner")

def main():
    logger.info("=" * 80)
    logger.info("🧪 تست OBT Sales Pipeline - wide_sales")
    logger.info(f"⏰ شروع: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)
    
    start_time = datetime.now()
    
    try:
        # لود ماژول OBT Sales از مسیر pipelines/load_obt_sales.py
        spec = importlib.util.spec_from_file_location(
            "load_obt_sales",
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                        "pipelines", "load_obt_sales.py")
        )
        obt_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(obt_module)
        
        logger.info("✅ ماژول load_obt_sales بارگذاری شد")
        
        # اجرای پایپلاین
        logger.info("\n▶️ شروع اجرای OBT Sales...")
        total = obt_module.run_obt_sales_pipeline(chunk_size=50000)
        
        # گزارش
        duration = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"""
        
        ╔═══════════════════════════════════════════╗
        ║   🎉 تست OBT Sales پایان یافت          ║
        ╠═══════════════════════════════════════════╣
        ║ کل رکوردها:      {total:>10,}           ║
        ║ زمان کل:         {duration:>8.1f} ثانیه  ║
        ║ سرعت:            {total/duration if duration > 0 else 0:>10.0f} r/s     ║
        ╚═══════════════════════════════════════════╝
        """)
        
        # بررسی جدول
        from core.engine.loader import DataLoader
        import pandas as pd
        
        loader = DataLoader()
        with loader.tgt_engine.connect() as conn:
            df = pd.read_sql("""
                SELECT 
                    COUNT(*) as total_rows,
                    COUNT(DISTINCT faktor_id) as unique_invoices,
                    COUNT(DISTINCT customer_id) as unique_customers,
                    COUNT(DISTINCT product_id) as unique_products,
                    MIN(invoice_date) as min_date,
                    MAX(invoice_date) as max_date
                FROM wide_sales
            """, conn)
            
            logger.info(f"""
        📊 آمار جدول wide_sales:
        ─────────────────────────────────
        کل ردیف‌ها:    {df['total_rows'].iloc[0]:>10,}
        فاکتورهای یکتا: {df['unique_invoices'].iloc[0]:>10,}
        مشتریان یکتا:   {df['unique_customers'].iloc[0]:>10,}
        کالاهای یکتا:   {df['unique_products'].iloc[0]:>10,}
        بازه تاریخ:     {str(df['min_date'].iloc[0])[:10]} تا {str(df['max_date'].iloc[0])[:10]}
            """)
            
            # نمونه ۳ ردیف
            sample = pd.read_sql("""
                SELECT faktorsatr_id, fiscal_year, customer_name, 
                       product_name, quantity, row_net_amount,
                       invoice_jalali
                FROM wide_sales
                LIMIT 3
            """, conn)
            
            if not sample.empty:
                logger.info("📝 نمونه داده:")
                for _, row in sample.iterrows():
                    logger.info(f"   {str(row['customer_name'])[:20]:<20} | "
                               f"{str(row['product_name'])[:25]:<25} | "
                               f"{row['quantity']:>6} | "
                               f"{row['row_net_amount']:>12,} | "
                               f"{row['invoice_jalali']}")
        
    except Exception as e:
        logger.error(f"❌ خطا: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()