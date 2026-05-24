CREATE TABLE IF NOT EXISTS public."AeenNamehKharid" (
    "ccAeenNamehKharid" INTEGER,
    "ccNoeKharid" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "AzMablagh" DOUBLE PRECISION,
    "TaMablagh" DOUBLE PRECISION, PRIMARY KEY ("ccAeenNamehKharid")
);

CREATE TABLE IF NOT EXISTS public."Anbardar" (
    "ccAnbarMalzomat" INTEGER,
    "ccAfrad" INTEGER, PRIMARY KEY ("ccAnbarMalzomat", "ccAfrad")
);

CREATE TABLE IF NOT EXISTS public."AnbarGorohKala" (
    "ccGoroh" INTEGER,
    "ccAnbarMalzomat" INTEGER, PRIMARY KEY ("ccGoroh", "ccAnbarMalzomat")
);

CREATE TABLE IF NOT EXISTS public."AnbarMalzomat" (
    "ccMarkazPakhsh" INTEGER,
    "ccAnbarMalzomat" INTEGER,
    "NameAnbar" VARCHAR(50),
    "CodeNoeAnbar" INTEGER,
    "ccCodeHesab" INTEGER, PRIMARY KEY ("ccAnbarMalzomat")
);

CREATE TABLE IF NOT EXISTS public."AnbarMalzomatGardany" (
    "ccMarkazPakhsh" INTEGER,
    "ccAnbarMalzomat" INTEGER,
    "ccAnbarMalzomatGardany" INTEGER,
    "Shomareh" INTEGER,
    "ccDorehMaly" INTEGER,
    "TarikhShoro" TIMESTAMP,
    "TarikhPaian" TIMESTAMP,
    "Sharh" VARCHAR(100),
    "CodeVazeiat" INTEGER, PRIMARY KEY ("ccAnbarMalzomatGardany")
);

CREATE TABLE IF NOT EXISTS public."AnbarMalzomatGardanyShomaresh" (
    "ccAnbarMalzomatGardany" INTEGER,
    "ccAnbarMalzomatGardanyShomaresh" INTEGER,
    "Shomaresh" INTEGER,
    "TarikhShoro" TIMESTAMP,
    "TarikhPaian" TIMESTAMP,
    "CodeVazeiat" INTEGER, PRIMARY KEY ("ccAnbarMalzomatGardanyShomaresh")
);

CREATE TABLE IF NOT EXISTS public."AnbarMalzomatGardanyShomareshKala" (
    "ccAnbarMalzomatGardanyShomaresh" INTEGER,
    "ccAnbarMalzomatGardanyShomareshKala" INTEGER,
    "ccKalaMalzomat" INTEGER,
    "ShomarehSerial" VARCHAR(15),
    "TarikhTolid" TIMESTAMP,
    "TarikhEngheza" TIMESTAMP,
    "TedadComputer" INTEGER,
    "TedadGhably" INTEGER,
    "TedadJary" INTEGER, PRIMARY KEY ("ccAnbarMalzomatGardanyShomareshKala")
);

CREATE TABLE IF NOT EXISTS public."Darkhast" (
    "ccMarkazPakhsh" INTEGER,
    "ccDarkhast" INTEGER,
    "ShomarehDarkhast" INTEGER,
    "TarikhDarkhast" TIMESTAMP,
    "ccAfrad" INTEGER,
    "ccPost" INTEGER,
    "CodeVazeiat" INTEGER,
    "Tozihat" VARCHAR(255),
    "ccKarbar" INTEGER,
    "ccAnbarmalzomat" INTEGER, PRIMARY KEY ("ccDarkhast")
);

CREATE TABLE IF NOT EXISTS public."DarkhastSatr" (
    "ccDarkhast" INTEGER,
    "ccDarkhastSatr" INTEGER,
    "Tedad" INTEGER,
    "TedadAvalyeh" INTEGER,
    "ElatOdat" VARCHAR(120),
    "CodeVazeiat" INTEGER,
    "ccKalaMalzomat" INTEGER,
    "ccUser" INTEGER,
    "ccAfradTaeedKalaTakhasosy" INTEGER,
    "CodeVazeiatTaeeid" INTEGER,
    "IsBudget" INTEGER,
    "Tozihat" VARCHAR(-1),
    "TarikhTaeed" TIMESTAMP,
    "TozihatSefaresh" VARCHAR(100),
    "TozihatKartabl" VARCHAR(-1),
    "VazeiatTakhasosi" INTEGER,
    "NoeBudget" INTEGER, PRIMARY KEY ("ccDarkhastSatr")
);

CREATE TABLE IF NOT EXISTS public."DarkhastSatrVazeiat" (
    "ccDarkhastSatr" INTEGER,
    "ccDarkhastSatrVazeiat" INTEGER,
    "CodeVazeiat" INTEGER,
    "TarikhVazeiat" TIMESTAMP,
    "ccUser" INTEGER,
    "Tozihat" VARCHAR(-1), PRIMARY KEY ("ccDarkhastSatrVazeiat")
);

CREATE TABLE IF NOT EXISTS public."DarkhastVazeiat" (
    "ccDarkhast" INTEGER,
    "ccDarkhastVazeiat" INTEGER,
    "CodeVazeiat" INTEGER,
    "TarikhVazeiat" TIMESTAMP,
    "ccUser" INTEGER,
    "Tozihat" VARCHAR(500), PRIMARY KEY ("ccDarkhastVazeiat")
);

CREATE TABLE IF NOT EXISTS public."DarsadSahmiehMarkazPakhsh" (
    "ccDarsadSahmiehMarkazPakhsh" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "DarsadSahmiehBandy" DOUBLE PRECISION, PRIMARY KEY ("ccDarsadSahmiehMarkazPakhsh")
);

CREATE TABLE IF NOT EXISTS public."DastorKharid" (
    "ccMarkazPakhsh" INTEGER,
    "ccPishFaktor" INTEGER,
    "ccDastorKharid" INTEGER,
    "ShomarehDastorKharid" INTEGER,
    "TarikhDastorKharid" TIMESTAMP,
    "Tozihat" VARCHAR(200),
    "CodeVazeiat" INTEGER,
    "ccUserTaeed" INTEGER, PRIMARY KEY ("ccDastorKharid")
);

CREATE TABLE IF NOT EXISTS public."DastorKharidsatr" (
    "ccDastorKharid" INTEGER,
    "ccDastorKharidsatr" INTEGER,
    "ccKalaMalzomat" INTEGER,
    "TedadPishFaktor" INTEGER,
    "GheymatPishFaktor" DOUBLE PRECISION,
    "TedadDastorKharid" INTEGER,
    "GheymatDastorKharid" DOUBLE PRECISION, PRIMARY KEY ("ccDastorKharidsatr")
);

CREATE TABLE IF NOT EXISTS public."FaktorKala" (
    "ccMarkazPakhsh" INTEGER,
    "ccFaktorKala" INTEGER,
    "ShomarehFaktorKala" INTEGER,
    "TarikhFaktorKala" TIMESTAMP,
    "CodeNoeKharid" INTEGER,
    "ccTaminKonandehMalzomat" INTEGER,
    "Tozihat" VARCHAR(200),
    "ccTankhah" INTEGER,
    "ccAfradTankhah" INTEGER,
    "ccKarpardaz" INTEGER,
    "ccAfradKarpardaz" INTEGER,
    "CodeVazeiat" INTEGER,
    "ccRefrence" INTEGER,
    "ccDastorKharid" INTEGER,
    "MablaghMaliat" DOUBLE PRECISION,
    "MablaghAvarez" DOUBLE PRECISION,
    "ccUserTaeed" INTEGER, PRIMARY KEY ("ccFaktorKala")
);

CREATE TABLE IF NOT EXISTS public."FaktorKalaPhoto" (
    "ccFaktorKala" INTEGER,
    "ccPhoto" INTEGER,
    "ccNoePhoto" INTEGER, PRIMARY KEY ("ccFaktorKala", "ccPhoto")
);

CREATE TABLE IF NOT EXISTS public."FaktorKalaSatr" (
    "ccFaktorKala" INTEGER,
    "ccFaktorKalaSatr" INTEGER,
    "ccKalaMalzomat" INTEGER,
    "Tedad1" INTEGER,
    "Tedad2" INTEGER,
    "GheymatKhales" DOUBLE PRECISION,
    "GheymatNaKhales" DOUBLE PRECISION, PRIMARY KEY ("ccFaktorKalaSatr")
);

CREATE TABLE IF NOT EXISTS public."FaktorKalaSatrParameterKharid" (
    "ccFaktorKalaSatr" INTEGER,
    "ccParameterKharid" INTEGER, PRIMARY KEY ("ccFaktorKalaSatr", "ccParameterKharid")
);

CREATE TABLE IF NOT EXISTS public."Gharardad" (
    "ccGharardad" INTEGER,
    "ShomarehGharardad" VARCHAR(20),
    "TarikhGharardad" TIMESTAMP,
    "ccGoroh" INTEGER,
    "MozoeGharardad" VARCHAR(350),
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "ccPeymankar" INTEGER,
    "Mablagh" DOUBLE PRECISION,
    "ccNoeGharardad" INTEGER,
    "DarsadPishpardakht" DOUBLE PRECISION,
    "DarsadMalyat" DOUBLE PRECISION,
    "DarsadBimeh" DOUBLE PRECISION,
    "DarsadHosnehAnjamKar" DOUBLE PRECISION,
    "CodeVazeiat" INTEGER,
    "ccMarkazPakhsh" INTEGER, PRIMARY KEY ("ccGharardad")
);

CREATE TABLE IF NOT EXISTS public."GorohSahmiehBandy" (
    "ccGorohSahmiehBandy" INTEGER,
    "cckalaCode" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "ccAnbar" INTEGER,
    "CodeGorohSahmiehBandy" INTEGER, PRIMARY KEY ("ccGorohSahmiehBandy")
);

CREATE TABLE IF NOT EXISTS public."KalaMalzomat" (
    "ccKalaMalzomat" INTEGER,
    "NameKala" VARCHAR(100),
    "CodeNoeKalaMalzomat" INTEGER,
    "ccVahedShomaresh" INTEGER,
    "AkharinGheimat" DOUBLE PRECISION,
    "ccAfradTaeedKalaTakhasosy" INTEGER,
    "IsTakhasosy" TEXT,
    "ccGorohDaraee" INTEGER,
    "ccCodeHesab" INTEGER, PRIMARY KEY ("ccKalaMalzomat")
);

CREATE TABLE IF NOT EXISTS public."KalaMalzomatGoroh" (
    "ccKalaMalzomat" INTEGER,
    "ccGoroh" INTEGER, PRIMARY KEY ("ccKalaMalzomat", "ccGoroh")
);

CREATE TABLE IF NOT EXISTS public."KalaMalzomatTakhasosiAfrad" (
    "ccKalaMalzomatTakhasosiAfrad" INTEGER,
    "ccKalaMalzomat" INTEGER,
    "ccAfradTaeedKonandeh" INTEGER,
    "AzTarikh" TIMESTAMP,
    "TaTarikh" TIMESTAMP, PRIMARY KEY ("ccKalaMalzomatTakhasosiAfrad")
);

CREATE TABLE IF NOT EXISTS public."KalaMalzomatTaminKonandehMalzomat" (
    "ccKalaMalzomat" INTEGER,
    "ccTaminKonandehMalzomat" INTEGER,
    "IsEnhesary" TEXT, PRIMARY KEY ("ccKalaMalzomat", "ccTaminKonandehMalzomat")
);

CREATE TABLE IF NOT EXISTS public."KardexMalzomat" (
    "ccMarkazPakhsh" INTEGER,
    "ccTaminKonandehMalzomat" INTEGER,
    "ccAnbarMalzomat" INTEGER,
    "ccKardexMalzomat" INTEGER,
    "CodeNoeAmalyat" INTEGER,
    "CodeNoeForm" INTEGER,
    "ShomarehForm" INTEGER,
    "TarikhForm" TIMESTAMP,
    "ccRefrence" INTEGER,
    "CodeVazeiat" INTEGER,
    "ccGoroh" INTEGER,
    "Tozihat" VARCHAR(255),
    "ccAfrad" INTEGER,
    "CodeNoeHavaleh" INTEGER,
    "ccDastorKharid" INTEGER,
    "ccGorohAslyDaraee" INTEGER,
    "MablaghMaliat" DOUBLE PRECISION,
    "MablaghAvarez" DOUBLE PRECISION,
    "ccTankhah" INTEGER,
    "ccUserTaeed" INTEGER, PRIMARY KEY ("ccKardexMalzomat")
);

CREATE TABLE IF NOT EXISTS public."KardexMalzomatSatr" (
    "ccKardexMalzomat" INTEGER,
    "ccKardexMalzomatSatr" INTEGER,
    "ccKalaMalzomat" INTEGER,
    "TarikhEngheza" TIMESTAMP,
    "Tedad" DOUBLE PRECISION,
    "Mojody" DOUBLE PRECISION,
    "Gheymat" DOUBLE PRECISION,
    "GheymatMiangin" DOUBLE PRECISION,
    "GheymatMoaserMiangin" DOUBLE PRECISION,
    "Sort" INTEGER, PRIMARY KEY ("ccKardexMalzomatSatr")
);

CREATE TABLE IF NOT EXISTS public."Karpardaz" (
    "ccMarkazPakhsh" INTEGER,
    "ccKarpardaz" INTEGER,
    "ccAfrad" INTEGER,
    "SharhKarpardaz" VARCHAR(100),
    "ccTankhah" INTEGER, PRIMARY KEY ("ccKarpardaz")
);

CREATE TABLE IF NOT EXISTS public."Khadamat" (
    "ccKhadamat" INTEGER,
    "SharhKhadamat" VARCHAR(100),
    "AkharinGheimat" DOUBLE PRECISION, PRIMARY KEY ("ccKhadamat")
);

CREATE TABLE IF NOT EXISTS public."KhadamatGoroh" (
    "ccKhadamat" INTEGER,
    "ccGoroh" INTEGER, PRIMARY KEY ("ccKhadamat", "ccGoroh")
);

CREATE TABLE IF NOT EXISTS public."MoeenKalaMarkazHazineh" (
    "ccMoeenKalaMarkazHazineh" INTEGER,
    "ccGorohKalaMalzomat" INTEGER,
    "ccGorohMarkazHazineh" INTEGER,
    "ccCodeHesab" INTEGER, PRIMARY KEY ("ccMoeenKalaMarkazHazineh")
);

CREATE TABLE IF NOT EXISTS public."MohasebehMianginMalzomatGhatee" (
    "ccMohasebehMianginMalzomatGhatee" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeNoeMohasebeh" INTEGER,
    "ccUser" INTEGER,
    "TarikhEntry" TIMESTAMP, PRIMARY KEY ("ccMohasebehMianginMalzomatGhatee")
);

CREATE TABLE IF NOT EXISTS public."NoeGharardad" (
    "ccNoeGharardad" INTEGER,
    "NameNoeGharardad" VARCHAR(50), PRIMARY KEY ("ccNoeGharardad")
);

CREATE TABLE IF NOT EXISTS public."NoeKharid" (
    "ccNoeKharid" INTEGER,
    "NameNoeKharid" VARCHAR(50), PRIMARY KEY ("ccNoeKharid")
);

CREATE TABLE IF NOT EXISTS public."ParameterKharid" (
    "ccParameterKharid" INTEGER,
    "Sharh" VARCHAR(100),
    "NoeParameter" INTEGER,
    "Mizan" DOUBLE PRECISION, PRIMARY KEY ("ccParameterKharid")
);

CREATE TABLE IF NOT EXISTS public."Peymankar" (
    "ccPeymankar" INTEGER,
    "NamePeymankar" VARCHAR(50),
    "CodeNoeShakhsiat" INTEGER,
    "Telephone" VARCHAR(50),
    "Fax" VARCHAR(50),
    "ccAddress" INTEGER,
    "CodeVazeiat" INTEGER, PRIMARY KEY ("ccPeymankar")
);

CREATE TABLE IF NOT EXISTS public."PeymankarAfrad" (
    "ccPeymankar" INTEGER,
    "ccAfrad" INTEGER,
    "Semat" VARCHAR(15), PRIMARY KEY ("ccPeymankar", "ccAfrad")
);

CREATE TABLE IF NOT EXISTS public."PeymankarGoroh" (
    "ccPeymankar" INTEGER,
    "ccGoroh" INTEGER, PRIMARY KEY ("ccPeymankar", "ccGoroh")
);

CREATE TABLE IF NOT EXISTS public."PeymankarKhadamat" (
    "ccKhadamat" INTEGER,
    "ccPeymankar" INTEGER, PRIMARY KEY ("ccKhadamat", "ccPeymankar")
);

CREATE TABLE IF NOT EXISTS public."PeymankarMarkazPakhsh" (
    "ccMarkazPakhsh" INTEGER,
    "ccPeymankar" INTEGER, PRIMARY KEY ("ccMarkazPakhsh", "ccPeymankar")
);

CREATE TABLE IF NOT EXISTS public."Pishfaktor" (
    "ccMarkazPakhsh" INTEGER,
    "ccPishfaktor" INTEGER,
    "ShomarehPishfaktor" INTEGER,
    "TarikhPishfaktor" TIMESTAMP,
    "TarikhVosol" TIMESTAMP,
    "TarikhEtebar" TIMESTAMP,
    "GheymatKol" DOUBLE PRECISION,
    "CodeVazeiat" INTEGER,
    "ccTaminKonandehMalzomat" INTEGER,
    "ccSefareshMalzomat" INTEGER,
    "ccUser" INTEGER,
    "ccUserEntry" INTEGER,
    "ElatOdat" VARCHAR(255), PRIMARY KEY ("ccPishfaktor")
);

CREATE TABLE IF NOT EXISTS public."PishfaktorPhoto" (
    "ccPishfaktor" INTEGER,
    "ccPhoto" INTEGER,
    "ccNoePhoto" INTEGER, PRIMARY KEY ("ccPhoto", "ccPishfaktor")
);

CREATE TABLE IF NOT EXISTS public."PishfaktorSatr" (
    "ccPishfaktor" INTEGER,
    "ccPishfaktorSatr" INTEGER,
    "ccKalaMalzomat" INTEGER,
    "ccKalaMalzomatPishnahady" INTEGER,
    "Tedad" INTEGER,
    "Gheymat" DOUBLE PRECISION, PRIMARY KEY ("ccPishfaktorSatr")
);

CREATE TABLE IF NOT EXISTS public."rptPardakhTaminKonandeh" (
    "ccTaminkonandehPardakht" INTEGER,
    "ccKalaCode" INTEGER,
    "Tedad" DOUBLE PRECISION,
    "TarikhForm" TIMESTAMP,
    "ShomarehForm" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "TarikhAghsat" TIMESTAMP,
    "MablaghAghsat" DOUBLE PRECISION,
    "MablaghPorsant" DOUBLE PRECISION,
    "MablaghHazinehHaml" VARCHAR(10),
    "SessionID" VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS public."SahmiehBandy" (
    "ccSahmiehBandy" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccAnbar" INTEGER,
    "ShomarehForm" INTEGER,
    "TarikhForm" TIMESTAMP,
    "CodeNoeSahmiehBandy" INTEGER,
    "CodeVazeiat" INTEGER,
    "CodeNoeHamlSahmiehBandy" INTEGER,
    "CodeNoeHavalehSahmiehBandy" INTEGER,
    "Sharh" VARCHAR(-1),
    "ccUser" INTEGER, PRIMARY KEY ("ccSahmiehBandy")
);

CREATE TABLE IF NOT EXISTS public."SahmiehBandySatr" (
    "ccSahmiehBandy" INTEGER,
    "ccSahmiehBandySatr" INTEGER,
    "CodeGorohSahmiehBandy" INTEGER,
    "ccKalaCode" INTEGER,
    "TedadToziee" INTEGER,
    "Mojody" INTEGER,
    "TaTarikh" TIMESTAMP,
    "MianginRooz" INTEGER, PRIMARY KEY ("ccSahmiehBandySatr")
);

CREATE TABLE IF NOT EXISTS public."SahmiehBandySatrMarkazPakhsh" (
    "ccSahmiehBandySatr" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccSahmiehBandySatrMarkazPakhsh" INTEGER,
    "Tedad" INTEGER,
    "Mojody" INTEGER,
    "Forosh" INTEGER, PRIMARY KEY ("ccSahmiehBandySatrMarkazPakhsh")
);

CREATE TABLE IF NOT EXISTS public."SahmiehBandyTarget" (
    "ccSahmiehBandyTarget" INTEGER,
    "Sal" INTEGER,
    "Mah" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccKalaCode" INTEGER,
    "Revision" INTEGER,
    "Tedad" INTEGER, PRIMARY KEY ("ccSahmiehBandyTarget")
);

CREATE TABLE IF NOT EXISTS public."SefareshMalzomat" (
    "ccMarkazPakhsh" INTEGER,
    "ccSefareshMalzomat" INTEGER,
    "ShomarehSefareshMalzomat" INTEGER,
    "TarikhSefareshMalzomat" TIMESTAMP,
    "ccNoeKharid" INTEGER,
    "ccAeenNamehKharid" INTEGER,
    "ccTankhah" INTEGER,
    "ccAfradTankhah" INTEGER,
    "ccKarpardaz" INTEGER,
    "ccAfradKarpardaz" INTEGER,
    "CodeVazeiat" INTEGER,
    "ccUser" INTEGER,
    "IsEnhesary" TEXT,
    "AddressFile" VARCHAR(-1),
    "WebAddress" VARCHAR(-1),
    "SharhFile" VARCHAR(-1), PRIMARY KEY ("ccSefareshMalzomat")
);

CREATE TABLE IF NOT EXISTS public."SefareshMalzomatSatr" (
    "ccSefareshMalzomat" INTEGER,
    "ccDarkhastSatr" INTEGER,
    "TedadSefaresh" INTEGER, PRIMARY KEY ("ccSefareshMalzomat", "ccDarkhastSatr")
);

CREATE TABLE IF NOT EXISTS public."SefareshMalzomatTaminKonandeh" (
    "ccSefareshMalzomat" INTEGER,
    "ccTaminKonandehMalzomat" INTEGER,
    "TarikhEstelam" TIMESTAMP,
    "ShomarehEstelam" INTEGER, PRIMARY KEY ("ccSefareshMalzomat", "ccTaminKonandehMalzomat")
);

CREATE TABLE IF NOT EXISTS public."SefareshMalzomatVazeiat" (
    "ccSefareshMalzomat" INTEGER,
    "ccSefareshMalzomatVazeiat" INTEGER,
    "CodeVazeiat" INTEGER,
    "TarikhVazeiat" TIMESTAMP,
    "ccUser" INTEGER, PRIMARY KEY ("ccSefareshMalzomatVazeiat")
);

CREATE TABLE IF NOT EXISTS public."TaminKonandeh" (
    "ccTaminKonandeh" INTEGER,
    "CodeNoeTaminKonandeh" INTEGER,
    "NameEkhtesary" VARCHAR(5),
    "NameTaminKonandeh" VARCHAR(50),
    "NameLatinTaminKonandeh" VARCHAR(50),
    "NameSabtShodeh" VARCHAR(50),
    "ShomarehSabt" VARCHAR(10),
    "Olaviat" INTEGER,
    "Telephone" VARCHAR(50),
    "Fax" VARCHAR(50),
    "URL" VARCHAR(100),
    "ccAddress" INTEGER,
    "CodeVazeiat" INTEGER,
    "CodeNoeSys" INTEGER,
    "CodeTaminKonandehOld" VARCHAR(15),
    "OzveGoroh" TEXT,
    "ccAfrad" INTEGER,
    "CodeNoeShakhsiat" INTEGER,
    "CodeEghtesadi" VARCHAR(15),
    "GhatiAmani" TEXT,
    "ccHesabMoeen" INTEGER,
    "CodeSortTaminkonandeh" INTEGER,
    "ShenasehMeli" VARCHAR(20), PRIMARY KEY ("ccTaminKonandeh")
);

CREATE TABLE IF NOT EXISTS public."TaminKonandehAfrad" (
    "ccTaminKonandeh" INTEGER,
    "ccAfrad" INTEGER,
    "Semat" VARCHAR(50), PRIMARY KEY ("ccTaminKonandeh", "ccAfrad")
);

CREATE TABLE IF NOT EXISTS public."TaminKonandehMadrak" (
    "ccTaminKonandeh" INTEGER,
    "ccPhoto" INTEGER,
    "ccNoePhoto" INTEGER, PRIMARY KEY ("ccTaminKonandeh", "ccPhoto")
);

CREATE TABLE IF NOT EXISTS public."TaminKonandehMalzomat" (
    "ccTaminKonandehMalzomat" INTEGER,
    "NameTaminKonandeh" VARCHAR(50),
    "Telephone" VARCHAR(50),
    "Fax" VARCHAR(50),
    "CodeVazeiat" INTEGER,
    "ccAddress" INTEGER,
    "CodeNoeShakhsiat" INTEGER,
    "ccTaminkonandehTejari" INTEGER, PRIMARY KEY ("ccTaminKonandehMalzomat")
);

CREATE TABLE IF NOT EXISTS public."TaminKonandehMalzomatGoroh" (
    "ccTaminKonandehMalzomat" INTEGER,
    "ccGoroh" INTEGER, PRIMARY KEY ("ccTaminKonandehMalzomat", "ccGoroh")
);

CREATE TABLE IF NOT EXISTS public."TaminKonandehMalzomatMarkazPakhsh" (
    "ccMarkazPakhsh" INTEGER,
    "ccTaminKonandehMalzomat" INTEGER, PRIMARY KEY ("ccMarkazPakhsh", "ccTaminKonandehMalzomat")
);

CREATE TABLE IF NOT EXISTS public."TaminKonandehModatBazPardakhtKala" (
    "ccTaminKonandehModatBazPardakhtKala" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "ccKala" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "CodeVazeiat" INTEGER,
    "ModatBazPardakht" INTEGER,
    "ccUser" INTEGER
);

CREATE TABLE IF NOT EXISTS public."TaminkonandehPardakht" (
    "ccTaminkonandehPardakht" INTEGER,
    "ccKalaCode" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "CodeNoePardakht" INTEGER,
    "ShoroPardakhtRooz" INTEGER,
    "FaselehAghsat" VARCHAR(255),
    "CodeHazinehHaml" INTEGER,
    "CodePorsantAzMahal" INTEGER,
    "DarsadPorsant" DOUBLE PRECISION,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "DarsadHazinehHaml" DOUBLE PRECISION,
    "TedadAghsat" INTEGER, PRIMARY KEY ("ccTaminkonandehPardakht")
);

CREATE TABLE IF NOT EXISTS public."TaminKonandehShomarehHesab" (
    "ccTaminKonandeh" INTEGER,
    "ccShomarehHesab" INTEGER,
    "ccBank" INTEGER,
    "NameShobeh" VARCHAR(50),
    "CodeShobeh" VARCHAR(10), PRIMARY KEY ("ccTaminKonandeh", "ccShomarehHesab")
);

CREATE TABLE IF NOT EXISTS public."TolidKonandeh" (
    "ccTolidKonandeh" INTEGER,
    "NameTolidKonandeh" VARCHAR(150),
    "ccKeshvar" INTEGER, PRIMARY KEY ("ccTolidKonandeh")
);