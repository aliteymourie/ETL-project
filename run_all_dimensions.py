# فایل: run_all_dimensions.py
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
    logger.info("تست Incremental Load - همه ابعاد (Dimensions)")
    logger.info(f"شروع: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)

    results = {}
    start_time = datetime.now()

    dim_configs = [
        ("dim_product",     "pipelines.dimensions.load_dim_product",     "run_dim_product_pipeline",     "کالا"),
        ("dim_customer",    "pipelines.dimensions.load_dim_customer",    "run_dim_customer_pipeline",    "مشتری"),
        ("dim_employee",    "pipelines.dimensions.load_dim_employee",    "run_dim_employee_pipeline",    "کارکنان"),
        ("dim_dist_center", "pipelines.dimensions.load_dim_dist_center", "run_dim_dist_center_pipeline", "مرکز پخش"),
        ("dim_warehouse",   "pipelines.dimensions.load_dim_warehouse",   "run_dim_warehouse_pipeline",   "انبار"),
        ("dim_supplier",    "pipelines.dimensions.load_dim_supplier",    "run_dim_supplier_pipeline",    "تأمین‌کننده"),
        ("dim_asset_group", "pipelines.dimensions.load_dim_asset_group", "run_dim_asset_group_pipeline", "گروه دارایی"),
        ("dim_branch",      "pipelines.dimensions.load_dim_branch",      "run_dim_branch_pipeline",      "مرکز پخش (قدیم)"),
        ("dim_seller",      "pipelines.dimensions.load_dim_seller",      "run_dim_seller_pipeline",      "فروشنده"),
    ]

    for dim_name, module_path, func_name, persian_name in dim_configs:
        logger.info("\n" + "█" * 60)
        logger.info(f"{dim_name} ({persian_name})")
        logger.info("█" * 60)
        try:
            import importlib
            module = importlib.import_module(module_path)
            func = getattr(module, func_name)
            logger.info(f"→ اجرای {dim_name}...")
            results[dim_name] = func()
        except Exception as e:
            logger.error(f"{dim_name}: {str(e)[:100]}")
            results[dim_name] = -1

    # dim_date - فقط بررسی وضعیت
    logger.info("\n" + "█" * 60)
    logger.info("dim_date (تاریخ) - بررسی وضعیت")
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
            logger.info(f"dim_date: {row[0]:,} رکورد از {row[1]} تا {row[2]}")
            results['dim_date'] = 0
    except Exception as e:
        logger.error(f"dim_date: {str(e)[:100]}")
        results['dim_date'] = -1

    duration = (datetime.now() - start_time).total_seconds()

    logger.info(f"""

    ╔═══════════════════════════════════════════════╗
    ║   نتیجه تست Incremental - ابعاد             ║
    ╠═══════════════════════════════════════════════╣""")

    for name, _ in dim_configs:
        logger.info(f"    ║ {name:<18}: {str(results.get(name, 'N/A')):>10} رکورد           ║")

    logger.info(f"""    ║ dim_date:        {str(results.get('dim_date', 'N/A')):>10} رکورد           ║
    ╠═══════════════════════════════════════════════╣
    ║ زمان کل:          {duration:>10.1f} ثانیه           ║
    ╚═══════════════════════════════════════════════╝
    """)

    logger.info("\nتفسیر نتایج:")
    logger.info("-" * 50)

    for name, count in results.items():
        if name == 'dim_date':
            continue
        if count == 0:
            logger.info(f"  {name}: ۰ رکورد = بدون تغییر جدید")
        elif count == -1:
            logger.info(f"  {name}: خطا - نیاز به بررسی")
        elif count < 10:
            logger.info(f"  {name}: {count} رکورد = تغییرات خیلی کم (طبیعی)")
        elif count < 100:
            logger.info(f"  {name}: {count} رکورد = تغییرات کم")
        else:
            logger.info(f"  {name}: {count} رکورد = تغییرات زیاد (اولین اجرا؟)")

    logger.info("\n" + "=" * 80)
    logger.info("ابعاد معمولاً تغییرات کمی دارند (مشتری جدید، کالای جدید و...)")
    logger.info("اگر عدد بزرگی دیدید، احتمالاً اولین اجرا پس از پاک کردن Checkpoint است.")


if __name__ == "__main__":
    main()
