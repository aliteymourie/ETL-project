"""
Fact Purchase - خرید
منبع: Warehouse.FaktorKharid + FaktorKharidSatr
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
from sqlalchemy import text
from datetime import datetime
from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.logging import setup_logger

logger = setup_logger("fact_purchase")

def run_fact_purchase_pipeline():
    logger.info("=" * 60)
    logger.info("🔄 Fact Purchase - خرید")
    start_time = datetime.now()
    
    extractor = DataExtractor()
    loader = DataLoader()
    
    try:
        # 1. استخراج با JOIN
        query = """
            SELECT 
                h.ccFaktorKharid,
                h.ccMarkazPakhsh,
                h.ccTaminKonandeh,
                h.TarikhFaktorKharid,
                h.MablaghKol,
                s.ccFaktorKharidSatr,
                s.Tedad,
                s.Gheymat,
                s.ccKalaCode
            FROM Warehouse.FaktorKharid h
            INNER JOIN Warehouse.FaktorKharidSatr s 
                ON h.ccFaktorKharid = s.ccFaktorKharid
            WHERE h.TarikhFaktorKharid IS NOT NULL
            ORDER BY h.TarikhFaktorKharid
        """
        
        logger.info("📥 استخراج خریدها...")
        df = pd.read_sql_query(query, extractor.src_engine)
        
        if df.empty:
            logger.warning("⚠️ خریدی یافت نشد")
            return 0
        
        logger.info(f"📋 {len(df):,} سطر خرید")
        
        # 2. ابعاد
        with loader.tgt_engine.connect() as conn:
            dim_product = pd.read_sql('SELECT product_key, cc_kala FROM dim_product', conn)
            dim_supplier = pd.read_sql('SELECT supplier_key, cc_tamin_konandeh FROM dim_supplier', conn)
        
        # 3. date_key
        df['TarikhFaktorKharid'] = pd.to_datetime(df['TarikhFaktorKharid'])
        df['date_key'] = df['TarikhFaktorKharid'].dt.strftime('%Y%m%d').astype(int)
        
        # 4. JOIN ابعاد (کالا با ccKalaCode)
        df = pd.merge(df, dim_product, left_on='ccKalaCode', right_on='cc_kala', how='left')
        df['product_key'] = df['product_key'].fillna(1).astype(int)
        
        df = pd.merge(df, dim_supplier, on='ccTaminKonandeh', how='left')
        df['supplier_key'] = df['supplier_key'].fillna(1).astype(int)
        
        # 5. ساخت fact
        fact = pd.DataFrame({
            'date_key': df['date_key'],
            'product_key': df['product_key'],
            'dist_center_key': 1,
            'cc_tamin_konandeh': df['ccTaminKonandeh'].fillna(1).astype(int),
            'cc_faktor_kharid': df['ccFaktorKharid'],
            'cc_faktor_kharid_satr': df['ccFaktorKharidSatr'],
            'az_mablagh': 0,
            'ta_mablagh': df['MablaghKol'],
            'tedad_kharid': pd.to_numeric(df['Tedad'], errors='coerce').fillna(0),
            'fi_kharid': pd.to_numeric(df['Gheymat'], errors='coerce').fillna(0)
        })
        
        fact = fact.drop_duplicates(['cc_faktor_kharid', 'cc_faktor_kharid_satr'])
        
        inserted = 0
        with loader.tgt_engine.begin() as conn:
            for _, row in fact.iterrows():
                try:
                    conn.execute(
                        text("""
                            INSERT INTO fact_purchase (date_key, product_key, dist_center_key,
                                cc_tamin_konandeh, cc_faktor_kharid, cc_faktor_kharid_satr,
                                az_mablagh, ta_mablagh, tedad_kharid, fi_kharid)
                            VALUES (:date_key, :product_key, 1,
                                :cc_tamin, :cc_faktor, :cc_satr,
                                :az, :ta, :tedad, :fi)
                            ON CONFLICT (cc_faktor_kharid, cc_faktor_kharid_satr)
                            DO UPDATE SET
                                tedad_kharid = EXCLUDED.tedad_kharid,
                                fi_kharid = EXCLUDED.fi_kharid
                        """),
                        {
                            "date_key": int(row['date_key']),
                            "product_key": int(row['product_key']),
                            "cc_tamin": int(row['cc_tamin_konandeh']),
                            "cc_faktor": int(row['cc_faktor_kharid']),
                            "cc_satr": int(row['cc_faktor_kharid_satr']),
                            "az": float(row['az_mablagh']),
                            "ta": float(row['ta_mablagh']),
                            "tedad": float(row['tedad_kharid']),
                            "fi": float(row['fi_kharid'])
                        }
                    )
                    inserted += 1
                except Exception as e:
                    logger.debug(f"⚠️ خطا: {str(e)[:80]}")
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ {inserted:,} رکورد در {duration:.1f}s")
        return inserted
        
    except Exception as e:
        logger.error(f"❌ خطا: {str(e)[:200]}")
        raise

if __name__ == "__main__":
    run_fact_purchase_pipeline()