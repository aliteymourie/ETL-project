SELECT 
    dfs.ccDarkhastFaktorSatr            AS Sales_Fact_ID,     -- کلید اصلی سطر
    dfs.ccDarkhastFaktor                AS Invoice_ID,        -- کلید خارجی متصل به جدول هدر (Header)
    dfs.Sal                             AS Fiscal_Year,       -- کلید ترکیبی سال مالی برای اتصال به هدر

    -- کدهای اتصال به ابعاد هم‌نوا (Conformed Dimension Keys)
    dfs.ccKala                          AS Product_Key,       -- متصل به Dim_Product

    -- شاخص‌ها و مقادیر محاسباتی سطح سطر (Line Measures)
    ISNULL(dfs.Tedad1, 0)               AS Quantity_Carton,   -- تعداد کارتن
    ISNULL(dfs.Tedad2, 0)               AS Quantity_Box,      -- تعداد جعبه
    ISNULL(dfs.Tedad3, 0)               AS Quantity_Unit,     -- تعداد واحد/عددی
    ISNULL(dfs.MablaghForosh, 0)        AS Unit_Price,        -- قیمت فروش واحد
    ISNULL(dfs.MablaghTakhfifFaktor, 0) AS Row_Discount_Amount,
    ISNULL(dfs.Maliat, 0)               AS Row_Tax,
    ISNULL(dfs.Avarez, 0)               AS Row_Surcharge,
    ISNULL(dfs.MablaghForoshKhalesKala, 0) AS Row_Net_Amount  -- مبلغ خالص سطر کالا
FROM Pakhsh.Sales.DarkhastFaktorSatr dfs;
