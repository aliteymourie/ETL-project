# فایل: run_all_facts_test.py (اصلاح import)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from core.utils.logging import setup_logger

logger = setup_logger("facts_test_runner")

def main():
    logger.info("=" * 80)
    logger.info("🚀 اجرای تستی تمام Fact ها (محدودیت ۱۰۰,۰۰۰ رکورد)")
    logger.info(f"⏰ شروع: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)
    
    results = {}
    start_time = datetime.now()
    
    # 1. Fact Inventory
    logger.info("\n" + "█" * 60)
    logger.info("1/4: Fact Inventory (موجودی)")
    from pipelines.facts.load_fact_inventory import run_fact_inventory_pipeline
    results['fact_inventory'] = run_fact_inventory_pipeline(max_rows=100000)
    
    # 2. Fact Asset
    logger.info("\n" + "█" * 60)
    logger.info("2/4: Fact Asset (اموال)")
    from pipelines.facts.load_fact_asset import run_fact_asset_pipeline
    results['fact_asset'] = run_fact_asset_pipeline(max_rows=100000)
    
    # 3. Fact Treasury
    logger.info("\n" + "█" * 60)
    logger.info("3/4: Fact Treasury (خزانه)")
    from pipelines.facts.load_fact_treasury import run_fact_treasury_pipeline
    results['fact_treasury'] = run_fact_treasury_pipeline(max_rows=100000)
    
    # 4. Fact Sales
    logger.info("\n" + "█" * 60)
    logger.info("4/4: Fact Sales (فروش)")
    # اصلاح import - فایل sales_pipeline_incremental مستقیماً در pipelines است
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "sales_pipeline_incremental",
        os.path.join(os.path.dirname(__file__), "pipelines", "sales_pipeline_incremental.py")
    )
    sales_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sales_module)
    results['fact_sales'] = sales_module.run_fact_sales_incremental()
    
    # گزارش نهایی
    duration = (datetime.now() - start_time).total_seconds()
    total = sum(results.values())
    
    logger.info(f"""
    
    ╔═══════════════════════════════════════════════╗
    ║     🎉 تست تمام Fact ها پایان یافت          ║
    ╠═══════════════════════════════════════════════╣
    ║ fact_inventory:  {results['fact_inventory']:>10,} رکورد           ║
    ║ fact_asset:      {results['fact_asset']:>10,} رکورد           ║
    ║ fact_treasury:   {results['fact_treasury']:>10,} رکورد           ║
    ║ fact_sales:      {results['fact_sales']:>10,} رکورد           ║
    ╠═══════════════════════════════════════════════╣
    ║ مجموع:           {total:>10,} رکورد           ║
    ║ زمان کل:         {duration:>10.1f} ثانیه           ║
    ╚═══════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()