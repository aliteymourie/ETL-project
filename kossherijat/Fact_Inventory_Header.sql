SELECT TOP (1000) 
    k.ccKardex                          AS Kardex_Header_Key, -- کلید اصلی سطح هدر کاردکس
    k.Sal                               AS Fiscal_Year,       -- سال مالی
    k.ShomarehForm                      AS Document_Number,   -- شماره سند انبار
    k.ShomarehFaktor                    AS Invoice_Number,    -- شماره فاکتور مرتبط
    k.CodeNoeForm                       AS Form_Type_Code,    -- نوع فرم (رسید/حواله/...)
    k.CodeNoeAmalyat                    AS Operation_Type_Code,
    k.CodeNoeAnbar                      AS Warehouse_Type_Code,
    k.CodeVazeiat                       AS Status_Code,
    k.Elat                              AS Header_Reason,     -- علت سند
    k.MarjoeeKamel                      AS Is_Fully_Returned, -- وضعیت مرجوعی کامل (بیت)

    -- کدهای اتصال به ابعاد هم‌نوا (Conformed Dimension Foreign Keys)
    k.ccMarkazPakhsh                    AS Branch_Key,        -- متصل به Dim_Branch
    k.ccAnbar                           AS Warehouse_Key,     -- متصل به بعد انبارها
    k.ccMoshtary                        AS Customer_Key,      -- متصل به Dim_Customer
    k.ccForoshandeh                     AS Seller_Key,        -- متصل به Dim_Seller
    k.ccMarkazPakhshBe                  AS Target_Branch_Key, -- مرکز پخش مقصد (در صورت انتقال بین مراکز)
    
    -- کلیدهای زمان هم‌نوا (Conformed Date Keys)
    CASE WHEN k.TarikhForm IS NOT NULL THEN CONVERT(INT, FORMAT(k.TarikhForm, 'yyyyMMdd')) ELSE NULL END AS Form_Date_Key,
    CASE WHEN k.TarikhFaktor IS NOT NULL THEN CONVERT(INT, FORMAT(k.TarikhFaktor, 'yyyyMMdd')) ELSE NULL END AS Invoice_Date_Key,

    -- شاخص‌ها و مقادیر محاسباتی سطح هدر (Header Measures)
    ISNULL(k.SumGheymatMarjoee, 0)      AS Total_Return_Amount,
    ISNULL(k.SumTedadMarjoee, 0)        AS Total_Return_Quantity,
    ISNULL(k.SumMaliat, 0)              AS Total_Tax_Amount,
    ISNULL(k.SumAvarez, 0)              AS Total_Surcharge_Amount,
    ISNULL(k.TakhfifFaktor, 0)          AS Header_Discount_Amount_1,
    ISNULL(k.MablaghTakhfif, 0)         AS Header_Discount_Amount_2
FROM [Pakhsh].[Warehouse].[Kardex] k;