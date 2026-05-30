"""
تست Incremental Load همه پایپلاین‌ها
بررسی می‌کند که فقط داده‌های جدید استخراج می‌شوند
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import importlib.util
from datetime import datetime
from core.utils.logging import setup_logger

logger = setup_logger("incremental_test")

def main():
    logger.info("=" * 80)
    logger.info("🧪 تست Incremental Load - همه پایپلاین‌ها")
    logger.info(f"⏰ شروع: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)
    
    results = {}
    start_time = datetime.now()
    
    # ================================================================
    # 1. ابعاد (Dimensions)
    # ================================================================
    logger.info("\n" + "█" * 60)
    logger.info("📁 تست ابعاد (باید ۰ یا خیلی کم باشند)")
    logger.info("█" * 60)
    
    try:
        from pipelines.dimensions.load_dim_product_incremental import run_dim_product_pipeline_incremental
        logger.info("→ اجرای dim_product...")
        results['dim_product'] = run_dim_product_pipeline_incremental()
    except Exception as e:
        logger.error(f"❌ dim_product: {str(e)[:100]}")
        results['dim_product'] = -1
    
    # ================================================================
    # 2. Fact ها
    # ================================================================
    logger.info("\n" + "█" * 60)
    logger.info("📊 تست Fact ها")
    logger.info("█" * 60)
    
    # 2.1 Fact Sales (فایل در pipelines/facts/)
    try:
        logger.info("→ اجرای fact_sales...")
        spec = importlib.util.spec_from_file_location(
            "sales_pipeline_incremental",
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                        "pipelines", "facts", "sales_pipeline_incremental.py")
        )
        sales_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sales_module)
        results['fact_sales'] = sales_module.run_fact_sales_incremental()
    except Exception as e:
        logger.error(f"❌ fact_sales: {str(e)[:100]}")
        results['fact_sales'] = -1
    
    # 2.2 Fact Inventory
    try:
        from pipelines.facts.load_fact_inventory import run_fact_inventory_pipeline
        logger.info("→ اجرای fact_inventory...")
        results['fact_inventory'] = run_fact_inventory_pipeline()
    except Exception as e:
        logger.error(f"❌ fact_inventory: {str(e)[:100]}")
        results['fact_inventory'] = -1
    
    # 2.3 Fact Asset
    try:
        from pipelines.facts.load_fact_asset import run_fact_asset_pipeline
        logger.info("→ اجرای fact_asset...")
        results['fact_asset'] = run_fact_asset_pipeline()
    except Exception as e:
        logger.error(f"❌ fact_asset: {str(e)[:100]}")
        results['fact_asset'] = -1
    
    # 2.4 Fact Treasury
    try:
        from pipelines.facts.load_fact_treasury import run_fact_treasury_pipeline
        logger.info("→ اجرای fact_treasury...")
        results['fact_treasury'] = run_fact_treasury_pipeline()
    except Exception as e:
        logger.error(f"❌ fact_treasury: {str(e)[:100]}")
        results['fact_treasury'] = -1
    
    # ================================================================
    # 3. گزارش نهایی
    # ================================================================
    duration = (datetime.now() - start_time).total_seconds()
    
    logger.info(f"""
    
    ╔═══════════════════════════════════════════════╗
    ║     🧪 نتیجه تست Incremental Load           ║
    ╠═══════════════════════════════════════════════╣
    ║ dim_product:     {results.get('dim_product', 'N/A'):>10} رکورد           ║
    ║ fact_sales:      {results.get('fact_sales', 'N/A'):>10} رکورد           ║
    ║ fact_inventory:  {results.get('fact_inventory', 'N/A'):>10} رکورد           ║
    ║ fact_asset:      {results.get('fact_asset', 'N/A'):>10} رکورد           ║
    ║ fact_treasury:   {results.get('fact_treasury', 'N/A'):>10} رکورد           ║
    ╠═══════════════════════════════════════════════╣
    ║ زمان کل:         {duration:>10.1f} ثانیه           ║
    ╚═══════════════════════════════════════════════╝
    """)
    
    # تفسیر نتایج
    logger.info("\n📋 تفسیر نتایج:")
    logger.info("-" * 50)
    
    for name, count in results.items():
        if count == 0:
            logger.info(f"  ✅ {name}: ۰ رکورد = عالی! Incremental کار می‌کند")
        elif count == -1:
            logger.info(f"  ❌ {name}: خطا - نیاز به بررسی")
        elif count < 100:
            logger.info(f"  ✅ {name}: {count} رکورد = داده جدید کم (طبیعی)")
        elif count < 1000:
            logger.info(f"  ℹ️ {name}: {count} رکورد = داده جدید متوسط")
        else:
            logger.info(f"  ⚠️ {name}: {count} رکورد = داده جدید زیاد (بررسی کن)")
    
    logger.info("\n" + "=" * 80)
    logger.info("💡 نکته: اگر همه ۰ باشند، یعنی Checkpoint درست کار می‌کند!")
    logger.info("💡 اگر عدد بزرگی دیدید، Checkpoint پاک شده و Full Load شده است.")


if __name__ == "__main__":
    main()