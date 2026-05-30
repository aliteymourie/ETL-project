# فایل: run_all_dimensions_incremental_test.py
"""
تست Incremental Load برای همه ابعاد
بررسی می‌کند که فقط داده‌های جدید استخراج می‌شوند
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from core.utils.logging import setup_logger

logger = setup_logger("dimensions_incremental_test")


def main():
    logger.info("=" * 80)
    logger.info("🧪 تست Incremental Load - همه ابعاد (Dimensions)")
    logger.info(f"⏰ شروع: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)
    
    results = {}
    start_time = datetime.now()
    
    # ================================================================
    # 1. dim_product (کالا - با ModifiedDate)
    # ================================================================
    logger.info("\n" + "█" * 60)
    logger.info("1/9: dim_product (کالا)")
    logger.info("█" * 60)
    try:
        from pipelines.dimensions.load_dim_product_incremental import run_dim_product_pipeline_incremental
        logger.info("→ اجرای dim_product...")
        results['dim_product'] = run_dim_product_pipeline_incremental()
    except Exception as e:
        logger.error(f"❌ dim_product: {str(e)[:100]}")
        results['dim_product'] = -1
    
    # ================================================================
    # 2. dim_customer (مشتری)
    # ================================================================
    logger.info("\n" + "█" * 60)
    logger.info("2/9: dim_customer (مشتری)")
    logger.info("█" * 60)
    try:
        from pipelines.dimensions.load_dim_customer import run_dim_customer_pipeline
        logger.info("→ اجرای dim_customer...")
        results['dim_customer'] = run_dim_customer_pipeline()
    except Exception as e:
        logger.error(f"❌ dim_customer: {str(e)[:100]}")
        results['dim_customer'] = -1
    
    # ================================================================
    # 3. dim_employee (فروشنده)
    # ================================================================
    logger.info("\n" + "█" * 60)
    logger.info("3/9: dim_employee (فروشنده)")
    logger.info("█" * 60)
    try:
        from pipelines.dimensions.load_dim_employee import run_dim_employee_pipeline
        logger.info("→ اجرای dim_employee...")
        results['dim_employee'] = run_dim_employee_pipeline()
    except Exception as e:
        logger.error(f"❌ dim_employee: {str(e)[:100]}")
        results['dim_employee'] = -1
    
    # ================================================================
    # 4. dim_dist_center (مرکز پخش)
    # ================================================================
    logger.info("\n" + "█" * 60)
    logger.info("4/9: dim_dist_center (مرکز پخش)")
    logger.info("█" * 60)
    try:
        from pipelines.dimensions.load_dim_dist_center import run_dim_dist_center_pipeline
        logger.info("→ اجرای dim_dist_center...")
        results['dim_dist_center'] = run_dim_dist_center_pipeline()
    except Exception as e:
        logger.error(f"❌ dim_dist_center: {str(e)[:100]}")
        results['dim_dist_center'] = -1
    
    # ================================================================
    # 5. dim_warehouse (انبار)
    # ================================================================
    logger.info("\n" + "█" * 60)
    logger.info("5/9: dim_warehouse (انبار)")
    logger.info("█" * 60)
    try:
        from pipelines.dimensions.load_dim_warehouse import run_dim_warehouse_pipeline
        logger.info("→ اجرای dim_warehouse...")
        results['dim_warehouse'] = run_dim_warehouse_pipeline()
    except Exception as e:
        logger.error(f"❌ dim_warehouse: {str(e)[:100]}")
        results['dim_warehouse'] = -1
    
    # ================================================================
    # 6. dim_supplier (تأمین‌کننده)
    # ================================================================
    logger.info("\n" + "█" * 60)
    logger.info("6/9: dim_supplier (تأمین‌کننده)")
    logger.info("█" * 60)
    try:
        from pipelines.dimensions.load_dim_supplier import run_dim_supplier_pipeline
        logger.info("→ اجرای dim_supplier...")
        results['dim_supplier'] = run_dim_supplier_pipeline()
    except Exception as e:
        logger.error(f"❌ dim_supplier: {str(e)[:100]}")
        results['dim_supplier'] = -1
    
    # ================================================================
    # 7. dim_asset_group (گروه دارایی)
    # ================================================================
    logger.info("\n" + "█" * 60)
    logger.info("7/9: dim_asset_group (گروه دارایی)")
    logger.info("█" * 60)
    try:
        from pipelines.dimensions.load_dim_asset_group import run_dim_asset_group_pipeline
        logger.info("→ اجرای dim_asset_group...")
        results['dim_asset_group'] = run_dim_asset_group_pipeline()
    except Exception as e:
        logger.error(f"❌ dim_asset_group: {str(e)[:100]}")
        results['dim_asset_group'] = -1
    
    # ================================================================
    # 8. dim_date (تاریخ - فقط در صورت نیاز بازسازی)
    # ================================================================
    logger.info("\n" + "█" * 60)
    logger.info("8/9: dim_date (تاریخ) - بررسی وضعیت")
    logger.info("█" * 60)
    try:
        from core.engine.loader import DataLoader
        from sqlalchemy import text
        
        loader = DataLoader()
        with loader.tgt_engine.connect() as conn:
            result = conn.execute(text(
                "SELECT COUNT(*), MIN(full_date), MAX(full_date) FROM dim_date"
            ))
            row = result.fetchone()
            logger.info(f"   📅 dim_date: {row[0]:,} رکورد از {row[1]} تا {row[2]}")
            results['dim_date'] = 0  # بدون تغییر
    except Exception as e:
        logger.error(f"❌ dim_date: {str(e)[:100]}")
        results['dim_date'] = -1
    
    # ================================================================
    # 9. dim_tafsily و dim_moien (حسابداری - هنوز پیاده‌سازی نشده)
    # ================================================================
    logger.info("\n" + "█" * 60)
    logger.info("9/9: dim_tafsily و dim_moien - ⏭️ رد شد (هنوز پیاده‌سازی نشده)")
    logger.info("█" * 60)
    results['dim_tafsily'] = 0
    results['dim_moien'] = 0
    
    # ================================================================
    # گزارش نهایی
    # ================================================================
    duration = (datetime.now() - start_time).total_seconds()
    
    logger.info(f"""
    
    ╔═══════════════════════════════════════════════╗
    ║   🧪 نتیجه تست Incremental - ابعاد          ║
    ╠═══════════════════════════════════════════════╣
    ║ dim_product:      {results.get('dim_product', 'N/A'):>10} رکورد           ║
    ║ dim_customer:     {results.get('dim_customer', 'N/A'):>10} رکورد           ║
    ║ dim_employee:     {results.get('dim_employee', 'N/A'):>10} رکورد           ║
    ║ dim_dist_center:  {results.get('dim_dist_center', 'N/A'):>10} رکورد           ║
    ║ dim_warehouse:    {results.get('dim_warehouse', 'N/A'):>10} رکورد           ║
    ║ dim_supplier:     {results.get('dim_supplier', 'N/A'):>10} رکورد           ║
    ║ dim_asset_group:  {results.get('dim_asset_group', 'N/A'):>10} رکورد           ║
    ║ dim_date:         {results.get('dim_date', 'N/A'):>10} رکورد           ║
    ╠═══════════════════════════════════════════════╣
    ║ زمان کل:          {duration:>10.1f} ثانیه           ║
    ╚═══════════════════════════════════════════════╝
    """)
    
    # تفسیر نتایج
    logger.info("\n📋 تفسیر نتایج:")
    logger.info("-" * 50)
    
    for name, count in results.items():
        if name in ['dim_date', 'dim_tafsily', 'dim_moien']:
            continue
        if count == 0:
            logger.info(f"  ✅ {name}: ۰ رکورد = بدون تغییر جدید")
        elif count == -1:
            logger.info(f"  ❌ {name}: خطا - نیاز به بررسی")
        elif count < 10:
            logger.info(f"  ✅ {name}: {count} رکورد = تغییرات خیلی کم (طبیعی)")
        elif count < 100:
            logger.info(f"  ℹ️ {name}: {count} رکورد = تغییرات کم")
        else:
            logger.info(f"  ⚠️ {name}: {count} رکورد = تغییرات زیاد (اولین اجرا؟)")
    
    logger.info("\n" + "=" * 80)
    logger.info("💡 ابعاد معمولاً تغییرات کمی دارند (مشتری جدید، کالای جدید و...)")
    logger.info("💡 اگر عدد بزرگی دیدید، احتمالاً اولین اجرا پس از پاک کردن Checkpoint است.")


if __name__ == "__main__":
    main()