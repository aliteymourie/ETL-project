#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ETL/pipelines/test_20_rows.py
تست سریع: فقط ۲۰ ردیف از SQL Server → PostgreSQL
"""

import sys
import os
import pandas as pd
import jdatetime
import csv
from io import StringIO
from datetime import datetime
from sqlalchemy import text

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

from core.engine.extractor import DataExtractor
from core.engine.loader import DataLoader
from core.utils.logging import setup_logger

logger = setup_logger("test_20")

from pipelines.load_obt_sales_v5 import (
    FINAL_COLS, INT_COLS, BOOL_COLS,
    build_upsert_sql, add_jalali_columns,
    DDL_WIDE_SALES, DDL_CHUNK_LOG, DDL_DEAD_LETTER,
)

JALALI_1403_START = "2024-03-20 00:00:00"


def test_20():
    logger.info("=" * 50)
    logger.info("تست ۲۰ ردیف")
    logger.info("=" * 50)

    extractor = DataExtractor()
    loader    = DataLoader()

    # ── ۱. DDL ────────────────────────────────────────────
    loader.create_table(DDL_WIDE_SALES)
    loader.create_table(DDL_CHUNK_LOG)
    loader.create_table(DDL_DEAD_LETTER)
    logger.info("جداول آماده.")

    # ── ۲. پاکسازی wide_sales ────────────────────────────
    with loader.tgt_engine.begin() as conn:
        conn.execute(text("DELETE FROM wide_sales"))
    logger.info("wide_sales پاک شد.")

    # ── ۳. پیدا کردن ۲۰ ID معتبر ─────────────────────────
    find_sql = """
        SELECT TOP 20
            dfs.ccDarkhastFaktorSatr AS rid
        FROM Pakhsh.Sales.DarkhastFaktorSatr dfs
        INNER JOIN Pakhsh.Sales.DarkhastFaktor df
            ON  df.ccDarkhastFaktor = dfs.ccDarkhastFaktor
            AND df.Sal              = dfs.Sal
        WHERE df.TarikhFaktor IS NOT NULL
          AND df.ModifiedDate >= CONVERT(DATETIME, '{lm}', 120)
        ORDER BY dfs.ccDarkhastFaktorSatr
    """.format(lm=JALALI_1403_START)

    ids_df = pd.read_sql(find_sql, extractor.src_engine)
    if ids_df.empty:
        logger.error("هیچ داده‌ای پیدا نشد!")
        return

    id_list = ids_df['rid'].tolist()
    ids_str = ",".join(str(int(x)) for x in id_list)
    logger.info(f"IDs: {id_list}")

    # ── ۴. Extract با IN ──────────────────────────────────
    sql = """
        SELECT
            dfs.ccDarkhastFaktorSatr            AS faktorsatr_id,
            dfs.ccDarkhastFaktor                AS faktor_id,
            df.Sal                              AS fiscal_year,
            df.ShomarehFaktorIndex              AS invoice_index,
            df.ShomarehFaktor                   AS invoice_number,
            df.ShomarehDarkhast                 AS request_number,
            df.TarikhFaktor                     AS invoice_datetime,
            CAST(df.TarikhFaktor   AS DATE)     AS invoice_date,
            df.TarikhDarkhast                   AS order_datetime,
            CAST(df.TarikhDarkhast AS DATE)     AS order_date,
            df.TarikhErsal                      AS ship_datetime,
            CAST(df.TarikhErsal    AS DATE)     AS ship_date,
            df.TarikhTahvil                     AS delivery_datetime,
            CAST(df.TarikhTahvil   AS DATE)     AS delivery_date,
            df.TarikhPishbinyTahvil             AS estimated_delivery_datetime,
            df.TarikhSarResid                   AS expiry_datetime,
            df.TarikhEntry                      AS entry_datetime,
            df.ModifiedDate                     AS header_modified_date,
            df.CodeVazeiat                      AS invoice_status_code,
            CASE df.CodeVazeiat
                WHEN 0  THEN N'ثبت اولیه'
                WHEN 1  THEN N'بستن درخواست'
                WHEN 4  THEN N'فاکتور توزیع نشده'
                WHEN 5  THEN N'پیش بینی ارسال'
                WHEN 6  THEN N'ارسال به مسیر'
                WHEN 7  THEN N'تسویه'
                WHEN 8  THEN N'تسویه ناقص'
                WHEN 9  THEN N'رسید از پخش'
                WHEN 10 THEN N'رسید از مشتری'
                ELSE        N'سایر'
            END                                 AS invoice_status_text,
            df.NoeFaktor                        AS invoice_type_code,
            df.InvoiceType                      AS invoice_subtype,
            df.CodeNoeVorod                     AS entry_type_code,
            df.CodeNoeVosolAzMoshtary           AS collection_type_code,
            df.CodeNoeHaml                      AS transport_type_code,
            df.DiscntType                       AS discount_type,
            df.DiscntSubType                    AS discount_subtype,
            df.IsFormal                         AS is_formal,
            df.TelephoneOrder                   AS is_telephone_order,
            df.BeMasoliat                       AS is_cooperative,
            df.HoghoghiShodeh                   AS is_legalized,
            df.TasviehPayeBar                   AS settlement_base,
            df.InvCode                          AS inventory_code,
            df.Serial                           AS serial_number,
            df.Elat                             AS cancel_reason,
            df.Sharh                            AS invoice_note,
            df.ReferenceNumber                  AS reference_number,
            df.DeviceChargeStatus               AS device_charge_status,
            df.CountPrint                       AS print_count,
            df.X                                AS gps_longitude,
            df.Y                                AS gps_latitude,
            df.SaatVorodBeMaghazeh              AS store_entry_time,
            df.SaatKhorojAzMaghazeh             AS store_exit_time,
            df.ModateVosol                      AS collection_days,
            df.ModatRoozRaasGiri                AS tracking_days,
            df.EtebarJary                       AS current_credit,
            df.MablaghMandehMoshtary            AS customer_balance,
            df.DarsadTakhfifKhazaneh            AS treasury_discount_pct,
            df.SumTedad3                        AS total_box_count,
            df.DetailsCount                     AS row_count,
            ISNULL(df.MablaghKolDarkhast,           0) AS request_gross_amount,
            ISNULL(df.MablaghTakhfifDarkhastTitr,   0) AS request_header_discount,
            ISNULL(df.MablaghTakhfifDarkhastSatr,   0) AS request_row_discount,
            ISNULL(df.MablaghKhalesDarkhast,        0) AS request_net_amount,
            ISNULL(df.MablaghKolFaktor,             0) AS invoice_gross_total,
            ISNULL(df.MablaghTakhfifFaktorTitr,     0) AS invoice_header_discount,
            ISNULL(df.MablaghTakhfifFaktorSatr,     0) AS invoice_row_discount,
            ISNULL(df.MablaghTakhfifFaktorTaavoni,  0) AS invoice_cooperative_discount,
            ISNULL(df.MablaghEzafat,                0) AS invoice_extra_charges,
            ISNULL(df.MablaghKhalesFaktor,          0) AS invoice_net_total,
            ISNULL(df.MablaghVajhDaryaftyFaktor,    0) AS invoice_payment_received,
            ISNULL(df.SumMaliat,                    0) AS invoice_tax_total,
            ISNULL(df.SumAvarez,                    0) AS invoice_surcharge_total,
            m.ccMoshtary                        AS customer_id,
            m.NameMoshtary                      AS customer_name,
            m.NameTablo                         AS customer_signboard_name,
            m.CodeEghtesady                     AS customer_economic_code,
            m.ShenasehMeli                      AS customer_national_id,
            m.CodePosty                         AS customer_postal_code,
            m.Telephone                         AS customer_phone,
            m.Fax                               AS customer_fax,
            m.NoeMoshtary                       AS customer_type_code,
            m.Rank                              AS customer_rank,
            ISNULL(m.EtebarKol,              0) AS customer_credit_limit,
            ISNULL(m.EtebarPishnahady,       0) AS customer_suggested_credit,
            ISNULL(m.ForoshTaghribiRoozaneh, 0) AS customer_daily_sale_estimate,
            m.CodeVazeiat                       AS customer_status_code,
            m.TarikhMoarefiMoshtary             AS customer_intro_date,
            m.X                                 AS customer_gps_longitude,
            m.Y                                 AS customer_gps_latitude,
            city.NameMahal                      AS customer_city_name,
            mnm.NameNoeMalekiatMoshtary         AS customer_ownership_type,
            df.ccForoshandeh                    AS seller_id,
            f.SharhForoshandeh                  AS seller_name,
            f.CodeForoshandehOld                AS seller_code_old,
            f.MobileNumber                      AS seller_mobile,
            f.CodeVazeiat                       AS seller_status_code,
            df.ccGorohForosh                    AS sales_group_id,
            gf.CodeGorohForosh                  AS sales_group_code,
            gf.SharhGorohForosh                 AS sales_group_name,
            df.ccMarkazPakhsh                   AS branch_id,
            mp.NameMarkazPakhsh                 AS branch_name,
            df.ccMantaghehPakhsh                AS region_id,
            mtp.NameMantaghehPakhsh             AS region_name,
            df.ccMasir                          AS route_id,
            dfs.ShomarehBach                    AS batch_number,
            dfs.ShomarehBachMulti               AS batch_number_multi,
            dfs.TarikhTolid                     AS production_date,
            dfs.TarikhEngheza                   AS expiry_date_row,
            dfs.Tedad1                          AS quantity,
            dfs.Tedad2                          AS quantity2,
            dfs.Tedad3                          AS quantity3,
            dfs.TedadAdadi                      AS quantity_piece,
            dfs.TedadBasteh                     AS quantity_box,
            dfs.TedadKarton                     AS quantity_carton,
            dfs.MablaghForosh                   AS unit_price,
            dfs.MablaghDarkhasti                AS requested_unit_price,
            dfs.MablaghForosh * dfs.Tedad1      AS gross_amount,
            ISNULL(dfs.MablaghTakhfifDarkhast,  0) AS request_row_discount_amt,
            ISNULL(dfs.MablaghTakhfifFaktor,    0) AS row_discount,
            ISNULL(dfs.MablaghTakhfifDasti,     0) AS manual_discount,
            ISNULL(dfs.DarsadTakhfifTaavoni,    0) AS cooperative_discount_pct,
            ISNULL(dfs.MablaghTakhfifNaghdiVahed, 0) AS cash_discount_per_unit,
            ISNULL(dfs.Maliat,                  0) AS row_tax,
            ISNULL(dfs.Avarez,                  0) AS row_surcharge,
            dfs.MablaghForoshKhalesKala         AS row_net_amount,
            dfs.GheymatMiangin                  AS avg_cost_price,
            dfs.GheymatKharid                   AS purchase_price,
            dfs.MojodyGhabelForosh              AS available_stock_at_sale,
            dfs.CodeVazeiat                     AS row_status_code,
            dfs.AdamJayezehKala                 AS no_prize_flag,
            dfs.ModifiedDate                    AS row_modified_date,
            k.ccKala                            AS product_id,
            k.ccKalaCode                        AS product_code_id,
            k.NameKala                          AS product_name,
            k.NameKalaFaktor                    AS product_invoice_name,
            k.NameLatin                         AS product_latin_name,
            k.CodeKalaT                         AS product_code,
            k.CodeKalaOld                       AS product_code_old,
            k.CodeJenerik                       AS product_generic_code,
            k.IranCode                          AS product_iran_code,
            k.CodeGS1                           AS product_gs1_code,
            k.BarCode                           AS product_barcode,
            k.CodeRasmiDaroo                    AS product_official_drug_code,
            k.ShenasehKala                      AS product_identifier,
            k.CodeNoeKalaMalzomat               AS product_type_code,
            k.MashmolMaliat                     AS product_tax_eligible,
            k.MashmolAvarez                     AS product_surcharge_eligible,
            k.MashmolSobsid                     AS product_subsidy_eligible,
            k.VaznKhales                        AS product_net_weight,
            k.VaznNaKhales                      AS product_gross_weight,
            k.VaznKarton                        AS product_carton_weight,
            k.Tedad1                            AS units_per_carton,
            k.Tedad2                            AS units_per_box,
            br.ccBrand                          AS brand_id,
            br.NameBrand                        AS brand_name,
            dfs.ccTaminKonandeh                 AS supplier_id
        FROM Pakhsh.Sales.DarkhastFaktorSatr dfs
        INNER JOIN Pakhsh.Sales.DarkhastFaktor df
            ON  df.ccDarkhastFaktor = dfs.ccDarkhastFaktor
            AND df.Sal              = dfs.Sal
        LEFT JOIN Pakhsh.Sales.Moshtary m
            ON df.ccMoshtary = m.ccMoshtary
        LEFT JOIN Pakhsh.Sales.NoeMalekiatMoshtary mnm
            ON m.ccNoeMalekiatMoshtary = mnm.ccNoeMalekiatMoshtary
        LEFT JOIN Pakhsh.Global.Mahal city
            ON m.ccMahaleh = city.ccMahal
        LEFT JOIN Pakhsh.Sales.Foroshandeh f
            ON df.ccForoshandeh = f.ccForoshandeh
        LEFT JOIN Pakhsh.Sales.GorohForosh gf
            ON df.ccGorohForosh = gf.ccGorohForosh
        LEFT JOIN Pakhsh.Global.MarkazPakhsh mp
            ON df.ccMarkazPakhsh = mp.ccMarkazPakhsh
        LEFT JOIN Pakhsh.Global.MantaghehPakhsh mtp
            ON df.ccMantaghehPakhsh = mtp.ccMantaghehPakhsh
        LEFT JOIN Pakhsh.Warehouse.Kala k
            ON dfs.ccKala = k.ccKala
        LEFT JOIN Pakhsh.Warehouse.Brand br
            ON k.ccBrand = br.ccBrand
        WHERE dfs.ccDarkhastFaktorSatr IN ({ids})
        ORDER BY dfs.ccDarkhastFaktorSatr
    """.format(ids=ids_str)

    logger.info("Extract...")
    chunk = pd.read_sql(sql, extractor.src_engine)
    logger.info(f"  extracted: {len(chunk)} ردیف")

    if chunk.empty:
        logger.error("هیچ ردیفی extract نشد!")
        return

    # ── ۵. Transform ──────────────────────────────────────
    logger.info("Transform...")
    chunk = add_jalali_columns(chunk, "invoice_datetime",  "invoice")
    chunk = add_jalali_columns(chunk, "order_datetime",    "order")
    chunk = add_jalali_columns(chunk, "ship_datetime",     "ship")
    chunk = add_jalali_columns(chunk, "delivery_datetime", "delivery")

    for col in chunk.select_dtypes(include="object").columns:
        chunk[col] = (
            chunk[col].astype(str)
            .str.replace("\n", " ").str.replace("\r", " ")
            .str.replace("\t", " ").str.strip()
            .replace("nan", None).replace("None", None).replace("", None)
        )

    chunk["etl_updated_at"] = pd.Timestamp.now()
    chunk = chunk[[c for c in FINAL_COLS if c in chunk.columns]]

    for col in INT_COLS:
        if col in chunk.columns:
            chunk[col] = pd.to_numeric(chunk[col], errors='coerce').astype('Int64')

    for col in BOOL_COLS:
        if col in chunk.columns:
            chunk[col] = chunk[col].map(
                lambda x: True if x in (1, True, '1', 'True') else
                          (False if x in (0, False, '0', 'False') else None)
            )

    logger.info(f"  transformed: {len(chunk)} ردیف, {len(chunk.columns)} ستون")

    # ── ۶. نمایش نمونه ────────────────────────────────────
    sample_cols = [
        "faktorsatr_id", "faktor_id", "fiscal_year",
        "invoice_number", "customer_id", "customer_name",
        "product_id", "product_name", "quantity", "unit_price",
        "invoice_jalali", "invoice_jalali_key",
        "is_cooperative", "is_legalized",
    ]
    existing = [c for c in sample_cols if c in chunk.columns]
    logger.info(f"نمونه:\n{chunk[existing].head(5).to_string()}")

    # ── ۷. Load ────────────────────────────────────────────
    logger.info("Load...")
    upsert_sql = build_upsert_sql(FINAL_COLS)
    filled_cols = [c for c in FINAL_COLS if c in chunk.columns]
    cols_str = ", ".join(filled_cols)

    output = StringIO()
    chunk.to_csv(output, sep='|', header=False, index=False,
                 na_rep='\\N', quoting=csv.QUOTE_MINIMAL)
    output.seek(0)

    raw_conn = loader.tgt_engine.raw_connection()
    try:
        with raw_conn.cursor() as cur:
            cur.execute("""
                CREATE TEMP TABLE IF NOT EXISTS tmp_staging (
                    LIKE wide_sales INCLUDING DEFAULTS EXCLUDING CONSTRAINTS
                ) ON COMMIT DROP
            """)
            cur.execute("TRUNCATE tmp_staging")

            copy_sql = (
                f"COPY tmp_staging ({cols_str}) "
                f"FROM STDIN WITH (FORMAT csv, DELIMITER '|', NULL '\\N')"
            )
            cur.copy_expert(copy_sql, output)
            cur.execute(upsert_sql)

        raw_conn.commit()
        logger.info(f"  loaded: {len(chunk)} ردیف")

    except Exception as e:
        raw_conn.rollback()
        logger.error(f"  LOAD FAILED: {e}")
        raise
    finally:
        raw_conn.close()

    # ── ۸. تأیید ──────────────────────────────────────────
    verify = pd.read_sql("SELECT COUNT(*) AS cnt FROM wide_sales",
                         loader.tgt_engine)
    cnt = int(verify['cnt'].iloc[0])
    logger.info(f"  PostgreSQL: {cnt} ردیف")

    if cnt == len(chunk):
        logger.info("=" * 50)
        logger.info(f"TEST PASSED - {cnt} ردیف")
        logger.info("=" * 50)
    else:
        logger.error(f"TEST FAILED - انتظار {len(chunk)} ولی {cnt}")

    # ── ۹. نمایش نتیجه ────────────────────────────────────
    result = pd.read_sql(
        "SELECT faktorsatr_id, customer_name, product_name, "
        "quantity, unit_price, invoice_jalali, invoice_jalali_key "
        "FROM wide_sales ORDER BY faktorsatr_id LIMIT 5",
        loader.tgt_engine,
    )
    logger.info(f"\nنتیجه در PostgreSQL:\n{result.to_string()}")


if __name__ == "__main__":
    test_20()
