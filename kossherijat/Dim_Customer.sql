SELECT 
    m.ccMoshtary                 AS Customer_Key, -- کلید هم‌نوا برای اتصال به فروش و حسابداری
    m.NameMoshtary               AS Customer_Name,
    m.CodeVazeiat                AS Customer_Status_Code,
    m.TarikhMoarefiMoshtary      AS Customer_Intro_Date,
	m.NameTablo					 AS Customer_Name_summary,
    city.NameMahal               AS Customer_City_Name,
    mnm.NameNoeMalekiatMoshtary  AS Customer_Ownership_Type
FROM Pakhsh.Sales.Moshtary m
LEFT JOIN Pakhsh.Sales.NoeMalekiatMoshtary mnm 
    ON m.ccNoeMalekiatMoshtary = mnm.ccNoeMalekiatMoshtary
LEFT JOIN Pakhsh.Global.Mahal city 
    ON m.ccMahaleh = city.ccMahal;