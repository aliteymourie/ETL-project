SELECT TOP (1000) 
    ks.ccKardexSatr                     AS Kardex_Detail_Key, -- کلید اصلی سطر کاردکس
    ks.ccKardex                         AS Kardex_Header_Key, -- کلید خارجی برای اتصال به جدول هدر
    ks.Sal                              AS Fiscal_Year,

    -- کدهای اتصال به ابعاد (Dimension Keys)
    ks.ccKala                           AS Product_Key,       -- متصل به بعد هم‌نوای Dim_Product
    ks.ccTaminKonandeh                  AS Supplier_Key,      -- متصل به بعد تامین‌کنندگان
    ks.ccElat                           AS Row_Reason_Key,    -- علت سطر کاردکس
    ks.ccAfrad                          AS Person_Key,        -- شخص مرتبط با سطر

    -- ابعاد تباهیده و ویژگی‌های بچ کالا (Degenerate Dimensions / Attributes)
    ks.ShomarehBach                     AS Batch_Number,      -- شماره سری ساخت / بچ دارو
    ks.TarikhTolid                      AS Production_Date,   -- تاریخ تولید کالا
    ks.TarikhEngheza                    AS Expiry_Date,       -- تاریخ انقضا
    ks.CodeNoeKala                      AS Product_Type_Code,
    ks.GhatiAmani                       AS Is_Firm_Or_Consignment, -- فروش قطعی یا امانی
    ks.Sharh                            AS Row_Description,

    -- ⚡ کلیدهای ارتباط فرامکانی (Cross-Fact Bridges) 
    ks.ccDarkhastFaktor                 AS Linked_Invoice_ID,
    ks.ccDarkhastFaktorSatr             AS Linked_Sales_Fact_ID, -- 🌟 اتصال مستقیم به Fact_Sales_Detail برای تحلیل فاکتور در برابر خروج انبار

    -- شاخص‌ها و مقادیر عددی تراکنش کالا (Measures)
    ISNULL(ks.Tedad1, 0)                AS Quantity_Carton,   -- تعداد کارتن
    ISNULL(ks.Tedad2, 0)                AS Quantity_Box,      -- تعداد جعبه
    ISNULL(ks.Tedad3, 0)                AS Quantity_Unit,     -- تعداد عددی
    ISNULL(ks.Tedad4, 0)                AS Quantity_Alt,      -- تعداد فرعی دیگر
    ISNULL(ks.Mojody, 0)                AS Stock_Effect_Qty,  -- مقدار تاثیر بر موجودی (ورود مثبت / خروج منفی)
    
    -- لایه‌های مختلف قیمت و ارزش‌گذاری ریالی انبار
    ISNULL(ks.Gheymat, 0)               AS Price_Level_1,
    ISNULL(ks.Gheymat2, 0)              AS Price_Level_2,
    ISNULL(ks.Gheymat3, 0)              AS Price_Level_3,
    ISNULL(ks.Gheymat4, 0)              AS Price_Level_4,
    ISNULL(ks.Gheymat5, 0)              AS Price_Level_5,
    ISNULL(ks.Gheymat6, 0)              AS Price_Level_6,
    ISNULL(ks.Gheymat7, 0)              AS Price_Level_7,
    ISNULL(ks.GheymatKolM, 0)           AS Total_Row_Amount,
    ISNULL(ks.GheymatTemp, 0)           AS Temp_Price,
    ISNULL(ks.GheymatTempLast, 0)       AS Last_Temp_Price,
FROM [Pakhsh].[Warehouse].[KardexSatr] ks;