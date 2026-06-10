#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DW Test Runner — فقط ۱۰۰ سطر اول از هر pipeline

Usage:
    cd ETL
    python pipelines/run_test_100.py
    python pipelines/run_test_100.py --only dims
    python pipelines/run_test_100.py --only facts
    python pipelines/run_test_100.py --only inventory
    python pipelines/run_test_100.py --pipeline dim_customer
"""

import sys
import os
import argparse
from datetime import datetime

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

from pipelines.dimensions.load_dim_branch            import run_dim_branch_pipeline
from pipelines.dimensions.load_dim_seller            import run_dim_seller_pipeline
from pipelines.dimensions.load_dim_customer          import run_dim_customer_pipeline
from pipelines.facts.load_fact_sales_header     import run_fact_sales_header_pipeline
from pipelines.facts.load_fact_sales_detail     import run_fact_sales_detail_pipeline
from pipelines.facts.load_fact_inventory_header import run_fact_inventory_header_pipeline
from pipelines.facts.load_fact_inventory_detail import run_fact_inventory_detail_pipeline
from core.utils.logging import setup_logger

logger = setup_logger("test_runner_100")

TEST_ROWS = 20

# همه pipeline‌ها با پارامترهای تست
ALL_PIPELINES = [
    {
        "name":  "dim_branch",
        "group": "dims",
        "fn":    run_dim_branch_pipeline,
        "kwargs": {},                       # Full-Refresh: row limit اعمال نمی‌شود
    },
    {
        "name":  "dim_seller",
        "group": "dims",
        "fn":    run_dim_seller_pipeline,
        "kwargs": {},                       # Full-Refresh
    },
    {
        "name":  "dim_customer",
        "group": "dims",
        "fn":    run_dim_customer_pipeline,
        "kwargs": {"chunk_size": TEST_ROWS, "max_workers": 1, "max_rows": TEST_ROWS},
    },
    {
        "name":  "fact_sales_header",
        "group": "facts",
        "fn":    run_fact_sales_header_pipeline,
        "kwargs": {"chunk_size": TEST_ROWS, "max_workers": 1, "max_rows": TEST_ROWS},
    },
    {
        "name":  "fact_sales_detail",
        "group": "facts",
        "fn":    run_fact_sales_detail_pipeline,
        "kwargs": {"chunk_size": TEST_ROWS, "max_workers": 1, "max_rows": TEST_ROWS},
    },
    {
        "name":  "fact_inventory_header",
        "group": "inventory",
        "fn":    run_fact_inventory_header_pipeline,
        "kwargs": {"chunk_size": TEST_ROWS, "max_workers": 1, "max_rows": TEST_ROWS},
    },
    {
        "name":  "fact_inventory_detail",
        "group": "inventory",
        "fn":    run_fact_inventory_detail_pipeline,
        "kwargs": {"chunk_size": TEST_ROWS, "max_workers": 1, "max_rows": TEST_ROWS},
    },
]


def run_one(pipeline: dict) -> dict:
    name = pipeline["name"]
    logger.info(f"▶ [{name}] starting test (limit={TEST_ROWS} rows) ...")
    start = datetime.now()
    try:
        rows = pipeline["fn"](**pipeline["kwargs"])
        elapsed = (datetime.now() - start).total_seconds()
        logger.info(f"✅ [{name}] OK — {rows:,} rows | {elapsed:.1f}s")
        return {"name": name, "status": "SUCCESS", "rows": rows, "elapsed": elapsed}
    except Exception as e:
        elapsed = (datetime.now() - start).total_seconds()
        logger.error(f"❌ [{name}] FAILED — {e}", exc_info=True)
        return {"name": name, "status": "FAILED", "rows": 0, "elapsed": elapsed, "error": str(e)}


def print_summary(results: list, total_elapsed: float):
    logger.info("=" * 60)
    logger.info(f"TEST SUMMARY  (limit={TEST_ROWS} rows each)")
    logger.info(f"  Total pipelines : {len(results)}")
    logger.info(f"  Total elapsed   : {total_elapsed:.1f}s")
    logger.info("-" * 60)
    for r in results:
        icon = "✅" if r["status"] == "SUCCESS" else "❌"
        err  = f"  → {r.get('error','')[:70]}" if r["status"] == "FAILED" else ""
        logger.info(f"  {icon} {r['name']:<30} rows={r['rows']:>5}  {r['elapsed']:.1f}s{err}")
    logger.info("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="DW Test Runner — 100 rows per pipeline")
    parser.add_argument(
        "--only",
        choices=["dims", "facts", "inventory"],
        default=None,
        help="فقط یک گروه از pipeline‌ها را اجرا کن",
    )
    parser.add_argument(
        "--pipeline",
        default=None,
        help="نام دقیق یک pipeline برای اجرا (مثلاً: dim_customer)",
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info(f"DW Test Runner  (TEST_ROWS={TEST_ROWS})")
    logger.info(f"  time: {datetime.now():%Y-%m-%d %H:%M:%S}")
    if args.pipeline:
        logger.info(f"  pipeline: {args.pipeline}")
    elif args.only:
        logger.info(f"  group:    {args.only}")
    else:
        logger.info("  running: ALL pipelines")
    logger.info("=" * 60)

    # فیلتر کردن pipeline‌ها
    if args.pipeline:
        targets = [p for p in ALL_PIPELINES if p["name"] == args.pipeline]
        if not targets:
            valid = ", ".join(p["name"] for p in ALL_PIPELINES)
            logger.error(f"Pipeline '{args.pipeline}' not found. Valid names: {valid}")
            sys.exit(1)
    elif args.only:
        targets = [p for p in ALL_PIPELINES if p["group"] == args.only]
    else:
        targets = ALL_PIPELINES

    start_time = datetime.now()
    results    = [run_one(p) for p in targets]
    total_elapsed = (datetime.now() - start_time).total_seconds()

    print_summary(results, total_elapsed)

    failed = [r for r in results if r["status"] == "FAILED"]
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
