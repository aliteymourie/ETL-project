SELECT 
    f.ccForoshandeh      AS Seller_Key,
    f.SharhForoshandeh   AS Seller_Name,
    f.CodeForoshandehOld AS Seller_Code_Old,
    f.MobileNumber       AS Seller_Mobile,
    f.CodeVazeiat        AS Seller_Status_Code
FROM Pakhsh.Sales.Foroshandeh f;