"""
ماژول کنترل کیفیت داده (Data Quality) - نسخه کامل
بررسی صحت، یکپارچگی و کامل بودن همه Fact ها و ابعاد
"""

import pandas as pd
from sqlalchemy import text
from datetime import datetime, timedelta
from core.utils.logging import setup_logger

logger = setup_logger("data_quality")


class DataQualityChecker:
    """
    بررسی کیفیت داده در مراحل مختلف ETL
    """
    
    def __init__(self, extractor, loader):
        self.extractor = extractor
        self.loader = loader
        self.results = []
    
    def check_row_count(self, source_query, target_table, tolerance_pct=5):
        """مقایسه تعداد رکوردهای منبع و مقصد"""
        logger.info(f"🔢 بررسی تعداد رکورد: {target_table}")
        
        try:
            df_src = pd.read_sql_query(source_query, self.extractor.src_engine)
            src_count = len(df_src)
            
            with self.loader.tgt_engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {target_table}"))
                tgt_count = result.scalar()
            
            diff = abs(src_count - tgt_count)
            diff_pct = (diff / src_count * 100) if src_count > 0 else 0
            passed = diff_pct <= tolerance_pct
            
            status = "✅" if passed else "❌"
            logger.info(f"   {status} منبع: {src_count:,} | مقصد: {tgt_count:,} | اختلاف: {diff_pct:.1f}%")
            
            return {
                'check': 'row_count',
                'table': target_table,
                'source_count': src_count,
                'target_count': tgt_count,
                'difference_pct': round(diff_pct, 2),
                'passed': passed,
                'status': 'PASS' if passed else 'FAIL'
            }
        except Exception as e:
            logger.error(f"   ❌ خطا: {str(e)[:100]}")
            return {'check': 'row_count', 'table': target_table, 'passed': False, 'status': 'ERROR', 'error': str(e)[:200]}
    
    def check_orphan_fk(self, fact_table, dim_table, fk_column, pk_column):
        """بررسی رکوردهای orphan"""
        logger.info(f"🔗 بررسی orphan: {fact_table}.{fk_column} -> {dim_table}.{pk_column}")
        
        try:
            with self.loader.tgt_engine.connect() as conn:
                query = f"""
                    SELECT COUNT(*) as orphan_count
                    FROM {fact_table} f
                    LEFT JOIN {dim_table} d ON f.{fk_column} = d.{pk_column}
                    WHERE f.{fk_column} != 1 
                      AND d.{pk_column} IS NULL
                """
                result = conn.execute(text(query))
                orphan_count = result.scalar()
                
                total_query = f"SELECT COUNT(*) FROM {fact_table} WHERE {fk_column} != 1"
                total_result = conn.execute(text(total_query))
                total_count = total_result.scalar()
                
                orphan_pct = (orphan_count / total_count * 100) if total_count > 0 else 0
                passed = orphan_count == 0
                
                status = "✅" if passed else "⚠️"
                logger.info(f"   {status} Orphan: {orphan_count:,} از {total_count:,} ({orphan_pct:.2f}%)")
                
                return {
                    'check': 'orphan_fk',
                    'fact_table': fact_table,
                    'dim_table': dim_table,
                    'orphan_count': orphan_count,
                    'total_count': total_count,
                    'orphan_pct': round(orphan_pct, 2),
                    'passed': passed,
                    'status': 'PASS' if passed else 'WARN'
                }
        except Exception as e:
            logger.error(f"   ❌ خطا: {str(e)[:100]}")
            return {'check': 'orphan_fk', 'passed': False, 'status': 'ERROR', 'error': str(e)[:200]}
    
    def check_null_values(self, table, required_columns):
        """بررسی مقادیر NULL"""
        logger.info(f"🔍 بررسی NULL: {table}")
        
        try:
            with self.loader.tgt_engine.connect() as conn:
                results = []
                all_passed = True
                
                for col in required_columns:
                    query = f"SELECT COUNT(*) as null_count FROM {table} WHERE {col} IS NULL"
                    result = conn.execute(text(query))
                    null_count = result.scalar()
                    
                    total_query = f"SELECT COUNT(*) FROM {table}"
                    total_result = conn.execute(text(total_query))
                    total_count = total_result.scalar()
                    
                    null_pct = (null_count / total_count * 100) if total_count > 0 else 0
                    passed = null_count == 0
                    
                    if not passed:
                        all_passed = False
                    
                    status = "✅" if passed else "⚠️"
                    logger.info(f"   {status} {col}: {null_count:,} NULL از {total_count:,} ({null_pct:.2f}%)")
                    
                    results.append({'column': col, 'null_count': null_count, 'null_pct': round(null_pct, 2), 'passed': passed})
                
                return {
                    'check': 'null_values',
                    'table': table,
                    'columns': results,
                    'passed': all_passed,
                    'status': 'PASS' if all_passed else 'WARN'
                }
        except Exception as e:
            logger.error(f"   ❌ خطا: {str(e)[:100]}")
            return {'check': 'null_values', 'table': table, 'passed': False, 'status': 'ERROR', 'error': str(e)[:200]}
    
    def check_duplicates(self, table, key_columns):
        """بررسی رکوردهای تکراری"""
        logger.info(f"🔍 بررسی تکراری: {table}")
        
        try:
            with self.loader.tgt_engine.connect() as conn:
                key_cols_str = ", ".join(key_columns)
                query = f"""
                    SELECT {key_cols_str}, COUNT(*) as cnt
                    FROM {table}
                    GROUP BY {key_cols_str}
                    HAVING COUNT(*) > 1
                """
                result = conn.execute(text(query))
                duplicates = result.fetchall()
                dup_count = len(duplicates)
                
                total_query = f"SELECT COUNT(*) FROM {table}"
                total_result = conn.execute(text(total_query))
                total_count = total_result.scalar()
                
                passed = dup_count == 0
                status = "✅" if passed else "❌"
                logger.info(f"   {status} تکراری: {dup_count:,} گروه از {total_count:,} رکورد")
                
                return {
                    'check': 'duplicates',
                    'table': table,
                    'duplicate_groups': dup_count,
                    'total_rows': total_count,
                    'passed': passed,
                    'status': 'PASS' if passed else 'FAIL'
                }
        except Exception as e:
            logger.error(f"   ❌ خطا: {str(e)[:100]}")
            return {'check': 'duplicates', 'table': table, 'passed': False, 'status': 'ERROR', 'error': str(e)[:200]}
    
    def check_value_ranges(self, table, column, min_value=None, max_value=None):
        """بررسی محدوده مقادیر عددی"""
        logger.info(f"📏 بررسی محدوده: {table}.{column}")
        
        try:
            with self.loader.tgt_engine.connect() as conn:
                conditions = []
                if min_value is not None:
                    conditions.append(f"{column} < {min_value}")
                if max_value is not None:
                    conditions.append(f"{column} > {max_value}")
                
                if not conditions:
                    return {'passed': True, 'status': 'SKIP'}
                
                where_clause = " OR ".join(conditions)
                query = f"SELECT COUNT(*) as out_of_range FROM {table} WHERE {where_clause}"
                result = conn.execute(text(query))
                out_of_range = result.scalar()
                
                stats_query = f"SELECT MIN({column}), MAX({column}), AVG({column}) FROM {table}"
                stats = conn.execute(text(stats_query)).fetchone()
                
                passed = out_of_range == 0
                status = "✅" if passed else "⚠️"
                logger.info(f"   {status} خارج از محدوده: {out_of_range:,} | Min={stats[0]:,.2f}, Max={stats[1]:,.2f}, Avg={stats[2]:,.2f}")
                
                return {
                    'check': 'value_ranges',
                    'table': table, 'column': column,
                    'min_value': float(stats[0]) if stats[0] else None,
                    'max_value': float(stats[1]) if stats[1] else None,
                    'avg_value': float(stats[2]) if stats[2] else None,
                    'out_of_range': out_of_range,
                    'passed': passed,
                    'status': 'PASS' if passed else 'WARN'
                }
        except Exception as e:
            logger.error(f"   ❌ خطا: {str(e)[:100]}")
            return {'check': 'value_ranges', 'passed': False, 'status': 'ERROR', 'error': str(e)[:200]}
    
    def check_freshness(self, table, date_column, max_hours_old=24):
        """بررسی به‌روز بودن داده‌ها"""
        logger.info(f"🕐 بررسی freshness: {table}.{date_column}")
        
        try:
            with self.loader.tgt_engine.connect() as conn:
                query = f"SELECT MAX({date_column}) as last_update FROM {table}"
                result = conn.execute(text(query))
                last_update = result.scalar()
                
                if last_update is None:
                    return {'check': 'freshness', 'table': table, 'passed': False, 'status': 'FAIL', 'message': 'هیچ داده‌ای وجود ندارد'}
                
                hours_old = (datetime.now() - last_update).total_seconds() / 3600
                passed = hours_old <= max_hours_old
                
                status = "✅" if passed else "⚠️"
                logger.info(f"   {status} آخرین به‌روزرسانی: {last_update} ({hours_old:.1f} ساعت قبل)")
                
                return {
                    'check': 'freshness',
                    'table': table,
                    'last_update': str(last_update),
                    'hours_old': round(hours_old, 1),
                    'passed': passed,
                    'status': 'PASS' if passed else 'WARN'
                }
        except Exception as e:
            logger.error(f"   ❌ خطا: {str(e)[:100]}")
            return {'check': 'freshness', 'passed': False, 'status': 'ERROR', 'error': str(e)[:200]}
    
    def run_all_checks(self):
        """اجرای تمام بررسی‌های کیفیت داده برای همه Fact ها"""
        logger.info("=" * 70)
        logger.info("🔬 شروع بررسی کیفیت داده (Data Quality Check) - همه Fact ها")
        logger.info("=" * 70)
        
        all_results = []
        
        # ================================================================
        # 1. بررسی تعداد رکوردها
        # ================================================================
        logger.info("\n📋 1. بررسی تعداد رکوردها (منبع vs مقصد):")
        
        all_results.append(self.check_row_count(
            "SELECT ccKala FROM Warehouse.Kala WHERE ccKala IS NOT NULL",
            "dim_product"
        ))
        all_results.append(self.check_row_count(
            "SELECT ccMoshtary FROM Sales.Moshtary WHERE ccMoshtary IS NOT NULL",
            "dim_customer"
        ))
        all_results.append(self.check_row_count(
            "SELECT ccForoshandeh FROM Sales.Foroshandeh WHERE ccForoshandeh IS NOT NULL",
            "dim_employee"
        ))
        all_results.append(self.check_row_count(
            "SELECT ccAnbar FROM Warehouse.Anbar WHERE ccAnbar IS NOT NULL",
            "dim_warehouse"
        ))
        all_results.append(self.check_row_count(
            "SELECT DISTINCT ccTaminKonandeh FROM Warehouse.KalaTaminKonandeh WHERE ccTaminKonandeh IS NOT NULL",
            "dim_supplier"
        ))
        all_results.append(self.check_row_count(
            "SELECT ccGorohDaraee FROM AssetAccounting.GorohDaraee WHERE ccGorohDaraee IS NOT NULL",
            "dim_asset_group"
        ))
        
        # ================================================================
        # 2. بررسی Orphan FK
        # ================================================================
        logger.info("\n📋 2. بررسی یکپارچگی کلیدهای خارجی (Orphan FK):")
        
        # fact_sales
        all_results.append(self.check_orphan_fk("fact_sales", "dim_product", "product_key", "product_key"))
        all_results.append(self.check_orphan_fk("fact_sales", "dim_customer", "customer_key", "customer_key"))
        all_results.append(self.check_orphan_fk("fact_sales", "dim_employee", "employee_key", "employee_key"))
        all_results.append(self.check_orphan_fk("fact_sales", "dim_dist_center", "dist_center_key", "dist_center_key"))
        all_results.append(self.check_orphan_fk("fact_sales", "dim_date", "date_key", "date_key"))
        
        # fact_inventory
        all_results.append(self.check_orphan_fk("fact_inventory", "dim_product", "product_key", "product_key"))
        all_results.append(self.check_orphan_fk("fact_inventory", "dim_dist_center", "dist_center_key", "dist_center_key"))
        all_results.append(self.check_orphan_fk("fact_inventory", "dim_date", "date_key", "date_key"))
        
        # fact_asset
        all_results.append(self.check_orphan_fk("fact_asset", "dim_employee", "employee_key", "employee_key"))
        all_results.append(self.check_orphan_fk("fact_asset", "dim_date", "date_key", "date_key"))
        
        # fact_treasury
        all_results.append(self.check_orphan_fk("fact_treasury", "dim_customer", "customer_key", "customer_key"))
        all_results.append(self.check_orphan_fk("fact_treasury", "dim_date", "date_key", "date_key"))
        all_results.append(self.check_orphan_fk("fact_treasury", "dim_dist_center", "dist_center_key", "dist_center_key"))
        
        # ================================================================
        # 3. بررسی NULL
        # ================================================================
        logger.info("\n📋 3. بررسی مقادیر NULL:")
        
        all_results.append(self.check_null_values("fact_sales", [
            'date_key', 'product_key', 'customer_key', 'employee_key', 'dist_center_key',
            'cc_darkhast_faktor', 'sal_mali'
        ]))
        all_results.append(self.check_null_values("fact_inventory", [
            'date_key', 'product_key', 'dist_center_key'
        ]))
        all_results.append(self.check_null_values("fact_asset", [
            'date_key', 'cc_amval'
        ]))
        all_results.append(self.check_null_values("fact_treasury", [
            'date_key', 'cc_sanad_dariaft', 'customer_key'
        ]))
        all_results.append(self.check_null_values("dim_product", ['cc_kala', 'name_kala']))
        all_results.append(self.check_null_values("dim_customer", ['cc_moshtary', 'name_moshtary']))
        all_results.append(self.check_null_values("dim_employee", ['cc_afrad', 'full_name']))
        all_results.append(self.check_null_values("dim_warehouse", ['cc_anbar', 'name_anbar']))
        all_results.append(self.check_null_values("dim_supplier", ['cc_tamin_konandeh']))
        all_results.append(self.check_null_values("dim_asset_group", ['cc_goroh_daraee']))
        
        # ================================================================
        # 4. بررسی تکراری
        # ================================================================
        logger.info("\n📋 4. بررسی رکوردهای تکراری:")
        
        all_results.append(self.check_duplicates("fact_sales", ['cc_darkhast_faktor', 'sal_mali', 'product_key']))
        all_results.append(self.check_duplicates("fact_inventory", ['date_key', 'product_key', 'dist_center_key', 'cc_anbar']))
        all_results.append(self.check_duplicates("fact_asset", ['date_key', 'cc_amval']))
        all_results.append(self.check_duplicates("fact_treasury", ['cc_sanad_dariaft']))
        all_results.append(self.check_duplicates("dim_product", ['cc_kala']))
        all_results.append(self.check_duplicates("dim_customer", ['cc_moshtary']))
        all_results.append(self.check_duplicates("dim_employee", ['cc_afrad']))
        all_results.append(self.check_duplicates("dim_warehouse", ['cc_anbar']))
        all_results.append(self.check_duplicates("dim_supplier", ['cc_tamin_konandeh']))
        all_results.append(self.check_duplicates("dim_asset_group", ['cc_goroh_daraee']))
        
        # ================================================================
        # 5. بررسی محدوده مقادیر
        # ================================================================
        logger.info("\n📋 5. بررسی محدوده مقادیر:")
        
        # fact_sales
        all_results.append(self.check_value_ranges("fact_sales", "fi_forosh", min_value=0))
        all_results.append(self.check_value_ranges("fact_sales", "tedad_faktor", min_value=0))
        all_results.append(self.check_value_ranges("fact_sales", "mablagh_takhfif", max_value=1000000000))
        
        # fact_inventory
        all_results.append(self.check_value_ranges("fact_inventory", "mojody_anbar_tedady", min_value=0))
        
        # fact_asset
        all_results.append(self.check_value_ranges("fact_asset", "gheymat_tamam_shodeh", min_value=0))
        all_results.append(self.check_value_ranges("fact_asset", "estehlak_anbashteh", max_value=100000000000))
        
        # fact_treasury
        all_results.append(self.check_value_ranges("fact_treasury", "mablagh_sanad", min_value=0))
        
        # ================================================================
        # 6. بررسی Freshness
        # ================================================================
        logger.info("\n📋 6. بررسی به‌روز بودن داده‌ها:")
        
        all_results.append(self.check_freshness("fact_sales", "etl_updated_at", max_hours_old=24))
        all_results.append(self.check_freshness("fact_inventory", "etl_created_at", max_hours_old=48))
        all_results.append(self.check_freshness("fact_asset", "etl_created_at", max_hours_old=168))
        all_results.append(self.check_freshness("fact_treasury", "etl_created_at", max_hours_old=168))
        all_results.append(self.check_freshness("dim_product", "updated_at", max_hours_old=168))
        all_results.append(self.check_freshness("dim_customer", "updated_at", max_hours_old=168))
        
        # ================================================================
        # 7. گزارش نهایی
        # ================================================================
        logger.info("\n" + "=" * 70)
        logger.info("📊 گزارش نهایی کیفیت داده:")
        logger.info("=" * 70)
        
        passed_count = sum(1 for r in all_results if r.get('passed', False))
        failed_count = sum(1 for r in all_results if not r.get('passed', False))
        total_checks = len(all_results)
        score = passed_count / total_checks * 100 if total_checks > 0 else 0
        
        for i, result in enumerate(all_results, 1):
            status_icon = "✅" if result.get('passed') else "❌"
            check_name = result.get('check', 'unknown')
            table = result.get('table', result.get('fact_table', 'N/A'))
            status = result.get('status', '?')
            logger.info(f"   {i:2d}. {status_icon} {check_name:<20} | {table:<25} | {status}")
        
        logger.info(f"""
        ╔══════════════════════════════════════╗
        ║     📊 خلاصه کیفیت داده            ║
        ╠══════════════════════════════════════╣
        ║ کل بررسی‌ها: {total_checks:>11}  ║
        ║ موفق: {passed_count:>17}  ║
        ║ ناموفق: {failed_count:>15}  ║
        ║ نمره: {score:>18.0f}٪  ║
        ╚══════════════════════════════════════╝
        """)
        
        return all_results


if __name__ == "__main__":
    from core.engine.extractor import DataExtractor
    from core.engine.loader import DataLoader
    
    extractor = DataExtractor()
    loader = DataLoader()
    
    checker = DataQualityChecker(extractor, loader)
    results = checker.run_all_checks()