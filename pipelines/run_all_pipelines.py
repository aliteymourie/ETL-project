#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DW Pipeline Orchestrator
اجرای مرتب‌شده همه pipeline‌های ابعاد و فکت‌ها

ترتیب اجرا:
  1. Dimensions  (Branch → Seller → Customer)  — موازی با هم
  2. Fact Sales  (Header → Detail)             — متوالی (Header باید قبل از Detail باشد)
  3. Fact Inventory (Header → Detail)          — متوالی

Usage:
    cd ETL
    python pipelines/run_all_pipelines.py
    python pipelines/run_all_pipelines.py --workers 6 --chunk-size 200000
    python pipelines/run_all_pipelines.py --only dims
    python pipelines/run_all_pipelines.py --only facts
    python pipelines/run_all_pipelines.py --only inventory
    python pipelines/run_all_pipelines.py --test --max-rows 100000
"""

import sys
import os
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

from pipelines.load_dim_branch            import run_dim_branch_pipeline
from pipelines.load_dim_seller            import run_dim_seller_pipeline
from pipelines.load_dim_customer          import run_dim_customer_pipeline
from pipelines.load_fact_sales_header     import run_fact_sales_header_pipeline
from pipelines.load_fact_sales_detail     import run_fact_sales_detail_pipeline
from pipelines.load_fact_inventory_header import run_fact_inventory_header_pipeline
from pipelines.load_fact_inventory_detail import run_fact_inventory_detail_pipeline
from core.utils.logging import setup_logger

logger = setup_logger("dw_orchestrator")


def run_pipeline_safe(name: str, fn, **kwargs) -> dict:
    """هر pipeline را در یک try/except اجرا می‌کند و نتیجه را برمی‌گرداند."""
    start = datetime.now()
    try:
        rows = fn(**kwargs)
        elapsed = (datetime.now() - start).total_seconds()
        logger.info(f"✅ [{name}] done — {rows:,} rows | {elapsed:.1f}s")
        return {"name": name, "status": "SUCCESS", "rows": rows, "elapsed": elapsed}
    except Exception as e:
        elapsed = (datetime.now() - start).total_seconds()
        logger.error(f"❌ [{name}] FAILED after {elapsed:.1f}s — {e}")
        return {"name": name, "status": "FAILED", "rows": 0, "elapsed": elapsed, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="DW Pipeline Orchestrator")
    parser.add_argument("--workers",    type=int, default=4,       help="Parallel workers per pipeline")
    parser.add_argument("--chunk-size", type=int, default=200_000, help="Chunk size per pipeline")
    parser.add_argument("--dim-workers",type=int, default=3,       help="Parallel dim pipelines (max 3)")
    parser.add_argument("--only",       type=str, default=None,
                        choices=["dims", "facts", "sales", "inventory"],
                        help="Run only a subset of pipelines")
    parser.add_argument("--test",       action="store_true", help="Enable test mode")
    parser.add_argument("--max-rows",   type=int, default=None,    help="Row cap in test mode")
    args = parser.parse_args()

    max_rows   = args.max_rows if args.test else None
    chunk_size = args.chunk_size
    workers    = args.workers

    logger.info("=" * 70)
    logger.info("DW Pipeline Orchestrator")
    logger.info(f"  workers:    {workers}")
    logger.info(f"  chunk_size: {chunk_size:,}")
    logger.info(f"  only:       {args.only or 'all'}")
    logger.info(f"  time:       {datetime.now():%Y-%m-%d %H:%M:%S}")
    if max_rows:
        logger.info(f"  max_rows:   {max_rows:,} (Test Mode)")
    logger.info("=" * 70)

    results    = []
    start_time = datetime.now()
    run_dims   = args.only in (None, "dims")
    run_sales  = args.only in (None, "facts", "sales")
    run_inv    = args.only in (None, "facts", "inventory")

    # ─────────────────────────────────────────────────────
    # STEP 1: Dimensions — Branch, Seller, Customer موازی
    # ─────────────────────────────────────────────────────
    if run_dims:
        logger.info("─" * 40)
        logger.info("STEP 1: Loading Dimensions (parallel)")

        dim_tasks = [
            ("dim_branch",   run_dim_branch_pipeline,   {}),
            ("dim_seller",   run_dim_seller_pipeline,   {}),
            ("dim_customer", run_dim_customer_pipeline,  {"chunk_size": 50_000, "max_workers": workers}),
        ]

        with ThreadPoolExecutor(max_workers=args.dim_workers) as executor:
            futures = {
                executor.submit(run_pipeline_safe, name, fn, **kwargs): name
                for name, fn, kwargs in dim_tasks
            }
            for future in as_completed(futures):
                results.append(future.result())

    # ─────────────────────────────────────────────────────
    # STEP 2: Fact Sales — Header اول، بعد Detail
    # ─────────────────────────────────────────────────────
    if run_sales:
        logger.info("─" * 40)
        logger.info("STEP 2: Loading Fact Sales (Header → Detail)")

        r = run_pipeline_safe(
            "fact_sales_header",
            run_fact_sales_header_pipeline,
            chunk_size=chunk_size,
            max_workers=workers,
            max_rows=max_rows,
        )
        results.append(r)

        if r["status"] == "SUCCESS":
            r2 = run_pipeline_safe(
                "fact_sales_detail",
                run_fact_sales_detail_pipeline,
                chunk_size=chunk_size * 2,   # سطر فاکتور معمولاً ۲× هدر است
                max_workers=workers,
                max_rows=max_rows,
            )
            results.append(r2)
        else:
            logger.warning("fact_sales_header failed — skipping fact_sales_detail.")

    # ─────────────────────────────────────────────────────
    # STEP 3: Fact Inventory — Header اول، بعد Detail
    # ─────────────────────────────────────────────────────
    if run_inv:
        logger.info("─" * 40)
        logger.info("STEP 3: Loading Fact Inventory (Header → Detail)")

        r = run_pipeline_safe(
            "fact_inventory_header",
            run_fact_inventory_header_pipeline,
            chunk_size=chunk_size,
            max_workers=workers,
            max_rows=max_rows,
        )
        results.append(r)

        if r["status"] == "SUCCESS":
            r2 = run_pipeline_safe(
                "fact_inventory_detail",
                run_fact_inventory_detail_pipeline,
                chunk_size=chunk_size * 2,
                max_workers=workers,
                max_rows=max_rows,
            )
            results.append(r2)
        else:
            logger.warning("fact_inventory_header failed — skipping fact_inventory_detail.")

    # ─────────────────────────────────────────────────────
    # Summary
    # ─────────────────────────────────────────────────────
    elapsed_total = (datetime.now() - start_time).total_seconds() / 60
    total_rows    = sum(r["rows"] for r in results)
    failed        = [r for r in results if r["status"] == "FAILED"]

    logger.info("=" * 70)
    logger.info("ORCHESTRATOR SUMMARY")
    logger.info(f"  Total pipelines : {len(results)}")
    logger.info(f"  Total rows      : {total_rows:,}")
    logger.info(f"  Elapsed minutes : {elapsed_total:.1f}")
    for r in results:
        icon = "✅" if r["status"] == "SUCCESS" else "❌"
        err  = f" — {r.get('error','')[:80]}" if r["status"] == "FAILED" else ""
        logger.info(f"  {icon} {r['name']:<30} rows={r['rows']:>10,}  {r['elapsed']:.1f}s{err}")
    logger.info("=" * 70)

    if failed:
        logger.error(f"{len(failed)} pipeline(s) failed: {[r['name'] for r in failed]}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
