SELECT 
    df.ccDarkhastFaktor                 AS Invoice_ID,        -- کلید اصلی جدول هدر
    df.ShomarehFaktor                   AS Invoice_Number,
    df.Sal                              AS Fiscal_Year,       -- کلید ترکیبی سال مالی

    -- کدهای اتصال به ابعاد هم‌نوا (Conformed Dimension Keys)
    df.ccMoshtary                       AS Customer_Key,      -- متصل به Dim_Customer
    df.ccMarkazPakhsh                   AS Branch_Key,        -- متصل به Dim_Branch
    df.ccForoshandeh                    AS Seller_Key,        -- متصل به Dim_Seller
    
    -- کلید زمان
    CASE 
        WHEN df.TarikhFaktor IS NOT NULL THEN CONVERT(INT, FORMAT(df.TarikhFaktor, 'yyyyMMdd')) 
        ELSE NULL 
    END                                 AS Invoice_Date_Key,  -- متصل به Dim_Date

    -- شاخص‌ها و مقادیر محاسباتی سطح هدر (Header Measures)
    ISNULL(df.MablaghKolDarkhast, 0)     AS Total_Request_Amount,
    ISNULL(df.MablaghKhalesDarkhast, 0)  AS Net_Request_Amount,
    ISNULL(df.MablaghKolFaktor, 0)       AS Total_Invoice_Amount,
    ISNULL(df.MablaghKhalesFaktor, 0)    AS Net_Invoice_Amount,
    ISNULL(df.ModateVosol, 0)            AS Collection_Term_Days ,
	df.SaatVorodBeMaghazeh AS SaatVorodBeMaghazeh,
	df.SaatKhorojAzMaghazeh AS SaatKhorojAzMaghazeh
FROM Pakhsh.Sales.DarkhastFaktor df;