#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OBT Sales Pipeline v6 Runner (wide_sales)

Usage:
    cd ETL
    python pipelines/run_obt_sales_v6.py
    python pipelines/run_obt_sales_v6.py --workers 6 --chunk-size 150000
    python pipelines/run_obt_sales_v6.py --test --max-rows 500000
"""

import sys
import os
import argparse
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

# Import v6 loader explicitly so v5 remains available.
from pipelines.load_obt_sales_v6 import run_obt_sales_pipeline
from core.utils.logging import setup_logger

logger = setup_logger("obt_sales_runner")


def main():
    parser = argparse.ArgumentParser(description="OBT Sales Pipeline v6 (wide_sales)")
    parser.add_argument("--workers",    type=int, default=4, help="Number of parallel workers")
    parser.add_argument("--chunk-size", type=int, default=100_000, help="ID range size per chunk")
    parser.add_argument("--test",       action="store_true", help="Enable test mode")
    parser.add_argument("--max-rows",   type=int, default=None, help="Maximum rows in test mode")
    args = parser.parse_args()

    max_rows = args.max_rows if args.test else None

    logger.info("=" * 60)
    logger.info("OBT Sales Pipeline v6 (wide_sales)")
    logger.info(f"  workers:    {args.workers}")
    logger.info(f"  chunk_size: {args.chunk_size:,}")
    logger.info(f"  time:       {datetime.now():%Y-%m-%d %H:%M:%S}")
    if max_rows:
        logger.info(f"  max_rows:   {max_rows:,} (Test Mode)")
    logger.info("=" * 60)

    try:
        total = run_obt_sales_pipeline(
            chunk_size=args.chunk_size,
            max_workers=args.workers,
            max_rows=max_rows,
        )
        logger.info(f"Done - {total:,} rows processed successfully.")
        sys.exit(0)

    except KeyboardInterrupt:
        logger.warning("Stopped by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Fatal Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
