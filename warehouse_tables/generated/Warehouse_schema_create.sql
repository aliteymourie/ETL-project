CREATE TABLE IF NOT EXISTS public."AghlamNazdik" (
    "ccAghlamNazdik" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "AzTarikh" TIMESTAMP,
    "TaTarikh" TIMESTAMP,
    "ccKalaCode" INTEGER,
    "Tedad" DOUBLE PRECISION,
    "TarikhEngheza" TIMESTAMP, PRIMARY KEY ("ccAghlamNazdik")
);

CREATE TABLE IF NOT EXISTS public."Anbar" (
    "ccAnbar" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "NameAnbar" VARCHAR(50),
    "CodeNoeAnbar" INTEGER,
    "ccAddress" INTEGER,
    "Telephone" VARCHAR(50),
    "Fax" VARCHAR(50),
    "CodeNoeSys" INTEGER,
    "CodeVazeiat" INTEGER, PRIMARY KEY ("ccAnbar")
);

CREATE TABLE IF NOT EXISTS public."Anbar14001224" (
    "ccAnbar" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "NameAnbar" VARCHAR(50),
    "CodeNoeAnbar" INTEGER,
    "ccAddress" INTEGER,
    "Telephone" VARCHAR(50),
    "Fax" VARCHAR(50),
    "CodeNoeSys" INTEGER,
    "CodeVazeiat" INTEGER
);

CREATE TABLE IF NOT EXISTS public."AnbarBeAnbar" (
    "ccAnbarAz" INTEGER,
    "ccAnbarBe" INTEGER, PRIMARY KEY ("ccAnbarAz", "ccAnbarBe")
);

CREATE TABLE IF NOT EXISTS public."AnbarGardany" (
    "ccMarkazPakhsh" INTEGER,
    "ccAnbar" INTEGER,
    "ccAnbarGardany" INTEGER,
    "Shomareh" INTEGER,
    "TarikhShoro" TIMESTAMP,
    "TarikhPaian" TIMESTAMP,
    "Sharh" VARCHAR(100),
    "CodeVazeiat" INTEGER,
    "CodeNoe" INTEGER, PRIMARY KEY ("ccAnbarGardany")
);

CREATE TABLE IF NOT EXISTS public."AnbarGardanyShomaresh" (
    "ccAnbarGardany" INTEGER,
    "ccAnbarGardanyShomaresh" INTEGER,
    "Shomaresh" INTEGER,
    "TarikhShoro" TIMESTAMP,
    "TarikhPaian" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "NoeShomaresh" INTEGER, PRIMARY KEY ("ccAnbarGardanyShomaresh")
);

CREATE TABLE IF NOT EXISTS public."AnbarGardanyShomareshKala" (
    "ccAnbarGardanyShomaresh" INTEGER,
    "ccAnbarGardanyShomareshKala" INTEGER,
    "ccKalaCode" INTEGER,
    "ccAnbarGhesmat" INTEGER,
    "ShomarehBach" VARCHAR(20),
    "TarikhTolid" TIMESTAMP,
    "TarikhEngheza" TIMESTAMP,
    "TedadComputer" INTEGER,
    "TedadGhably" INTEGER,
    "TedadJary" INTEGER,
    "ShomarehSerial" INTEGER,
    "TedadJaryTemp" DOUBLE PRECISION,
    "CodeVazeiat" INTEGER,
    "UserId" INTEGER, PRIMARY KEY ("ccAnbarGardanyShomareshKala")
);

CREATE TABLE IF NOT EXISTS public."AnbarGhesmat" (
    "ccAnbar" INTEGER,
    "ccAnbarGhesmat" INTEGER,
    "NameGhesmat" VARCHAR(50),
    "Tabagheh" INTEGER,
    "Rahro" INTEGER,
    "Ghafaseh" INTEGER,
    "Satr" INTEGER,
    "Soton" INTEGER,
    "Tol" DOUBLE PRECISION,
    "Arz" DOUBLE PRECISION,
    "Ertefa" DOUBLE PRECISION,
    "ccVahedSize" INTEGER,
    "VaznGhabeleTahamol" DOUBLE PRECISION,
    "ccVahedVazn" INTEGER, PRIMARY KEY ("ccAnbarGhesmat")
);

CREATE TABLE IF NOT EXISTS public."BarNameh" (
    "ccMarkazPakhsh" INTEGER,
    "ccBarNameh" INTEGER,
    "ShomarehBarnameh" VARCHAR(15),
    "TarikhBarnameh" TIMESTAMP,
    "ShomarehBimeh" VARCHAR(15),
    "TarikhBimeh" TIMESTAMP,
    "RialBimeh" DOUBLE PRECISION,
    "SherkatBimeh" VARCHAR(50),
    "NameBarbary" VARCHAR(50),
    "ShomarehMashin" VARCHAR(10),
    "NameRanandeh" VARCHAR(50),
    "CodeVazeiat" INTEGER, PRIMARY KEY ("ccBarNameh")
);

CREATE TABLE IF NOT EXISTS public."BarNamehSatr" (
    "ccRefrence" INTEGER,
    "ccBarnameh" INTEGER, PRIMARY KEY ("ccRefrence", "ccBarnameh")
);

CREATE TABLE IF NOT EXISTS public."Brand" (
    "ccBrand" INTEGER,
    "NameBrand" VARCHAR(50), PRIMARY KEY ("ccBrand")
);

CREATE TABLE IF NOT EXISTS public."DastehBandiNezaraty" (
    "ccNoeDastehBandiNezaraty" INTEGER,
    "ccDastehBandiNezaraty" INTEGER,
    "NameDastehBandiNezaraty" VARCHAR(50),
    "Code" VARCHAR(50), PRIMARY KEY ("ccDastehBandiNezaraty")
);

CREATE TABLE IF NOT EXISTS public."ElatMarjoeeKala" (
    "ccElatMarjoeeKala" INTEGER,
    "Sharh" VARCHAR(250),
    "CodeNoeElat" INTEGER,
    "MasoleiatElat" INTEGER,
    "CodeNoeAnbar" INTEGER, PRIMARY KEY ("ccElatMarjoeeKala")
);

CREATE TABLE IF NOT EXISTS public."FaktorKharid" (
    "ccMarkazPakhsh" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "ccFaktorKharid" INTEGER,
    "ShomarehFaktorKharid" INTEGER,
    "TarikhFaktorKharid" TIMESTAMP,
    "MablaghKol" DOUBLE PRECISION,
    "Takhfif" DOUBLE PRECISION,
    "CodeVazeiat" INTEGER, PRIMARY KEY ("ccFaktorKharid")
);

CREATE TABLE IF NOT EXISTS public."FaktorKharidSatr" (
    "ccFaktorKharid" INTEGER,
    "ccFaktorKharidSatr" INTEGER,
    "Tedad" DOUBLE PRECISION,
    "Gheymat" DOUBLE PRECISION,
    "ccKalaCode" INTEGER, PRIMARY KEY ("ccFaktorKharidSatr")
);

CREATE TABLE IF NOT EXISTS public."FaktorKharidSatrAnbar" (
    "ccFaktorKharidSatr" INTEGER,
    "ccFaktorKharidSatrAnbar" INTEGER,
    "ccKardexSatr" INTEGER, PRIMARY KEY ("ccFaktorKharidSatrAnbar")
);

CREATE TABLE IF NOT EXISTS public."GheymatMianginKala" (
    "ccMarkazPakhsh" INTEGER,
    "CodeNoeAnbar" INTEGER,
    "ccKalaCode" INTEGER,
    "GheymatMiangin" DOUBLE PRECISION,
    "ccKardexEffect" INTEGER,
    "TarikhEffect" TIMESTAMP, PRIMARY KEY ("ccMarkazPakhsh", "CodeNoeAnbar", "ccKalaCode")
);

CREATE TABLE IF NOT EXISTS public."GheymatMianginKalaLog" (
    "ccGheymatMianginKalaLog" INTEGER,
    "CodeNoeAnbar" INTEGER,
    "ccKalaCode" INTEGER,
    "GheymatMiangin" DOUBLE PRECISION,
    "Tarikh" TIMESTAMP, PRIMARY KEY ("ccGheymatMianginKalaLog")
);

CREATE TABLE IF NOT EXISTS public."GheymatMianginKalaTaminKonandeh" (
    "CodeNoeAnbar" INTEGER,
    "ccKalaCode" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "GheymatMiangin" DOUBLE PRECISION, PRIMARY KEY ("CodeNoeAnbar", "ccKalaCode", "ccTaminKonandeh")
);

CREATE TABLE IF NOT EXISTS public."Kala" (
    "ccKala" INTEGER,
    "ccKalaCode" INTEGER,
    "ccKalaLink" INTEGER,
    "CodeKalaT" VARCHAR(12),
    "NameKala" VARCHAR(150),
    "NameKalaFaktor" VARCHAR(150),
    "NamePocketPC" VARCHAR(150),
    "NameKalaPrint" VARCHAR(150),
    "NameLatin" VARCHAR(150),
    "ccBrand" INTEGER,
    "CodeNoeGheymat" INTEGER,
    "Tol" DOUBLE PRECISION,
    "Arz" DOUBLE PRECISION,
    "Ertefa" DOUBLE PRECISION,
    "ccVahedSize" INTEGER,
    "ccVahedVazn" INTEGER,
    "Tedad1" INTEGER,
    "Tedad2" INTEGER,
    "Tedad3" INTEGER,
    "Tedad4" INTEGER,
    "Olaviat" INTEGER,
    "ccVahedShomaresh" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(50),
    "VaznKhales" DOUBLE PRECISION,
    "VaznNaKhales" DOUBLE PRECISION,
    "VaznKarton" DOUBLE PRECISION,
    "CodeNoeKalaMalzomat" INTEGER,
    "CodeKalaOld" VARCHAR(15),
    "CodeNoeSys" INTEGER,
    "CodeSort" VARCHAR(300),
    "MashmolMaliat" TEXT,
    "MashmolAvarez" TEXT,
    "MashmolSobsid" TEXT,
    "CodeJenerik" INTEGER,
    "CodeGS1" VARCHAR(20),
    "IranCode" VARCHAR(20),
    "CodeMelli" VARCHAR(20),
    "BarCode" VARCHAR(20),
    "BarCodeAmaliati" VARCHAR(20),
    "CodeMoeen" VARCHAR(20),
    "ccTaminkonandeh" INTEGER,
    "ccTolidkonandeh" INTEGER,
    "NahvehTamin" INTEGER,
    "TaeedFani" TEXT,
    "CodeRasmiDaroo" VARCHAR(20),
    "GhatiAmani" INTEGER,
    "flagTarikhMilady" INTEGER,
    "codegtin" VARCHAR(-1),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "ShenasehKala" VARCHAR(50), PRIMARY KEY ("ccKala")
);

CREATE TABLE IF NOT EXISTS public."KalaAdamElat" (
    "SharhElat" VARCHAR(100),
    "CodeNoeAdam" INTEGER,
    "ccKalaAdamElat" INTEGER, PRIMARY KEY ("ccKalaAdamElat")
);

CREATE TABLE IF NOT EXISTS public."KalaAdamMarjoee" (
    "ccKalaCode" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccKalaAdamMarjoee" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "ccElat" INTEGER,
    "Elat" VARCHAR(255),
    "Sharh" VARCHAR(-1), PRIMARY KEY ("ccKalaAdamMarjoee")
);

CREATE TABLE IF NOT EXISTS public."KalaAdamSefaresh" (
    "ccKalaCode" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccKalaAdamSefaresh" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "ccElat" INTEGER,
    "Elat" VARCHAR(255),
    "Sharh" VARCHAR(-1), PRIMARY KEY ("ccKalaAdamSefaresh")
);

CREATE TABLE IF NOT EXISTS public."KalaAnbar" (
    "ccAnbar" INTEGER,
    "ccKalaCode" INTEGER,
    "MinMojodi" DOUBLE PRECISION,
    "MaxMojodi" DOUBLE PRECISION,
    "NoghtehSefaresh" DOUBLE PRECISION,
    "Mojody" INTEGER, PRIMARY KEY ("ccAnbar", "ccKalaCode")
);

CREATE TABLE IF NOT EXISTS public."KalaAnbarBK" (
    "ccAnbar" INTEGER,
    "ccKalaCode" INTEGER,
    "MinMojodi" DOUBLE PRECISION,
    "MaxMojodi" DOUBLE PRECISION,
    "NoghtehSefaresh" DOUBLE PRECISION,
    "Mojody" INTEGER
);

CREATE TABLE IF NOT EXISTS public."KalaAnbarGhesmat" (
    "ccKalaCode" INTEGER,
    "ccAnbarGhesmat" INTEGER, PRIMARY KEY ("ccKalaCode", "ccAnbarGhesmat")
);

CREATE TABLE IF NOT EXISTS public."KalaBachAdamForosh" (
    "ccKalaCode" INTEGER,
    "ShomarehBach" VARCHAR(50),
    "ccKalaBachAdamForosh" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "ccElat" INTEGER, PRIMARY KEY ("ccKalaBachAdamForosh")
);

CREATE TABLE IF NOT EXISTS public."KalaBachAdamMarjoee" (
    "ccKalaCode" INTEGER,
    "ShomarehBach" VARCHAR(50),
    "ccKalaBachAdamMarjoee" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "ccElat" INTEGER, PRIMARY KEY ("ccKalaBachAdamMarjoee")
);

CREATE TABLE IF NOT EXISTS public."KalaDastehBandiNezaraty" (
    "ccKalaCode" INTEGER,
    "ccDastehBandiNezaraty" INTEGER,
    "ccKalaDastehBandiNezaraty" INTEGER, PRIMARY KEY ("ccKalaDastehBandiNezaraty")
);

CREATE TABLE IF NOT EXISTS public."KalaGheymatKharid" (
    "ccKalaCode" INTEGER,
    "ccTaminkonandeh" INTEGER,
    "ccKalaGheymatKharid" INTEGER,
    "MablaghKharid" DOUBLE PRECISION,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(50), PRIMARY KEY ("ccKalaGheymatKharid")
);

CREATE TABLE IF NOT EXISTS public."KalaGheymatMasrafKonandeh" (
    "ccKalaCode" INTEGER,
    "ccKalaGheymatMasrafKonandeh" INTEGER,
    "MablaghMasrafKonandeh" DOUBLE PRECISION,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(50), PRIMARY KEY ("ccKalaGheymatMasrafKonandeh")
);

CREATE TABLE IF NOT EXISTS public."KalaGheymatPhoto" (
    "ccKalaGheymat" INTEGER,
    "CodeNoeGheymat" INTEGER,
    "ccPhoto" INTEGER,
    "ccNoePhoto" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ccUser" INTEGER, PRIMARY KEY ("ccKalaGheymat", "CodeNoeGheymat", "ccPhoto")
);

CREATE TABLE IF NOT EXISTS public."KalaGoroh" (
    "ccKalaGoroh" INTEGER,
    "ccKalaCode" INTEGER,
    "ccGoroh" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccKalaCode", "ccGoroh")
);

CREATE TABLE IF NOT EXISTS public."KalaGoroh13980320" (
    "ccKalaGoroh" INTEGER,
    "ccKalaCode" INTEGER,
    "ccGoroh" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public."KalaHistory" (
    "ccKalaHistory" INTEGER,
    "ccKala" INTEGER,
    "ccKalaCode" INTEGER,
    "ccKalaLink" INTEGER,
    "CodeKalaT" VARCHAR(12),
    "NameKala" VARCHAR(50),
    "NameKalaFaktor" VARCHAR(50),
    "NamePocketPC" VARCHAR(50),
    "NameKalaPrint" VARCHAR(50),
    "NameLatin" VARCHAR(50),
    "ccBrand" INTEGER,
    "CodeNoeGheymat" INTEGER,
    "Tol" DOUBLE PRECISION,
    "Arz" DOUBLE PRECISION,
    "Ertefa" DOUBLE PRECISION,
    "ccVahedSize" INTEGER,
    "ccVahedVazn" INTEGER,
    "Tedad1" INTEGER,
    "Tedad2" INTEGER,
    "Tedad3" INTEGER,
    "Tedad4" INTEGER,
    "Olaviat" INTEGER,
    "ccVahedShomaresh" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(50),
    "VaznKhales" DOUBLE PRECISION,
    "VaznNaKhales" DOUBLE PRECISION,
    "VaznKarton" DOUBLE PRECISION,
    "CodeNoeKalaMalzomat" INTEGER,
    "CodeKalaOld" VARCHAR(15),
    "CodeNoeSys" INTEGER,
    "CodeSort" VARCHAR(300),
    "MashmolMaliat" TEXT,
    "MashmolAvarez" TEXT,
    "MashmolSobsid" TEXT,
    "CodeJenerik" INTEGER,
    "Tarikh" TIMESTAMP,
    "ccUser" INTEGER,
    "CodeNoeCRUD" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "ccTolidKonandeh" INTEGER,
    "NahvehTamin" INTEGER,
    "TaeedFani" TEXT,
    "GhatiAmani" TEXT, PRIMARY KEY ("ccKalaHistory")
);

CREATE TABLE IF NOT EXISTS public."KalaMoshabeh" (
    "ccKalaCode" INTEGER,
    "ccKalaCodeMoshabeh" INTEGER, PRIMARY KEY ("ccKalaCode", "ccKalaCodeMoshabeh")
);

CREATE TABLE IF NOT EXISTS public."KalaPhoto" (
    "ccKalaCode" INTEGER,
    "ccPhoto" INTEGER,
    "ccNoePhoto" INTEGER, PRIMARY KEY ("ccKalaCode", "ccPhoto")
);

CREATE TABLE IF NOT EXISTS public."KalaSahmiehBandy" (
    "ShomarehBakhshnameh" VARCHAR(50),
    "TarikhBakhshNameh" TIMESTAMP,
    "ccKalaCode" INTEGER,
    "ccKalaSahmieh" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(50), PRIMARY KEY ("ccKalaSahmieh")
);

CREATE TABLE IF NOT EXISTS public."KalaShomarehBach" (
    "ccShomarehBach" INTEGER,
    "ccKalaCode" INTEGER,
    "ShomarehBach" VARCHAR(50),
    "ccTaminKonandeh" INTEGER,
    "TarikhTolid" TIMESTAMP,
    "TarikhEngheza" TIMESTAMP,
    "ccTolidKonandeh" INTEGER,
    "CodeNoeTarikh" TEXT,
    "IranCode" VARCHAR(20),
    "Codegtin" VARCHAR(25),
    "TarikhEntery" TIMESTAMP,
    "TarikhEnghezaTemp" TIMESTAMP,
    "UID" VARCHAR(25), PRIMARY KEY ("ccShomarehBach")
);

CREATE TABLE IF NOT EXISTS public."KalaTaminKonandeh" (
    "ccKalaCode" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "CodeKalaTaminKonandeh" VARCHAR(15),
    "CodeVazeiat" INTEGER, PRIMARY KEY ("ccKalaCode")
);

CREATE TABLE IF NOT EXISTS public."KalaTedadBlokeh" (
    "ccKalaTedadBlokeh" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccKalaCode" INTEGER,
    "ccKala" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "Tedad" DOUBLE PRECISION,
    "ccRefrence" INTEGER,
    "CodeNoeAnbar" INTEGER, PRIMARY KEY ("ccKalaTedadBlokeh")
);

CREATE TABLE IF NOT EXISTS public."KalaTolidKonandeh" (
    "ccKalaCode" INTEGER,
    "ccTolidKonandeh" INTEGER, PRIMARY KEY ("ccKalaCode")
);

CREATE TABLE IF NOT EXISTS public."KalaZaribBazariaby" (
    "ccKalaCode" INTEGER,
    "ccKalaZaribBazariaby" INTEGER,
    "ZaribBazariaby" DOUBLE PRECISION,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(255), PRIMARY KEY ("ccKalaZaribBazariaby")
);

CREATE TABLE IF NOT EXISTS public."Kardex" (
    "ccMarkazPakhsh" INTEGER,
    "ccAnbar" INTEGER,
    "CodeNoeAnbar" INTEGER,
    "ccKardex" INTEGER,
    "Sal" INTEGER,
    "CodeNoeForm" INTEGER,
    "CodeNoeAmalyat" INTEGER,
    "ShomarehForm" INTEGER,
    "TarikhForm" TIMESTAMP,
    "ccMarkazPakhshBe" INTEGER,
    "ccRefrence" INTEGER,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(50),
    "ShomarehFaktor" VARCHAR(12),
    "TarikhFaktor" TIMESTAMP,
    "ccUser" INTEGER,
    "ccMoshtary" INTEGER,
    "SumGheymatMarjoee" DOUBLE PRECISION,
    "SumTedadMarjoee" DOUBLE PRECISION,
    "MarjoeeKamel" TEXT,
    "SumMaliat" DOUBLE PRECISION,
    "SumAvarez" DOUBLE PRECISION,
    "TakhfifFaktor" DOUBLE PRECISION,
    "CodeNoeVorod" INTEGER,
    "ccForoshandeh" INTEGER,
    "MablaghTakhfif" DOUBLE PRECISION,
    "ccMashin" INTEGER,
    "ccAfradRanandeh" INTEGER, PRIMARY KEY ("ccKardex", "Sal")
);

CREATE TABLE IF NOT EXISTS public."KardexAmarNameh" (
    "ccKardexAmarNameh" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "CodeNoeAnbar" INTEGER,
    "ccAnbar" INTEGER,
    "TarikhForm" TIMESTAMP,
    "CodeNoeForm" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "ccKalacode" INTEGER,
    "ShomarehBach" VARCHAR(50),
    "TarikhTolid" TIMESTAMP,
    "TarikhEngheza" TIMESTAMP,
    "Tedad" INTEGER,
    "ccRefrence" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "Codevazeiat" INTEGER,
    "UUID" VARCHAR(50),
    "Olaviat" INTEGER,
    "Comment" VARCHAR(100),
    "GLN" VARCHAR(20),
    "IRC" VARCHAR(20),
    "Gtin" VARCHAR(20),
    "TedadDarBasteh" INTEGER, PRIMARY KEY ("ccKardexAmarNameh")
);

CREATE TABLE IF NOT EXISTS public."KardexAmarNamehBK13990208" (
    "ccKardexAmarNameh" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "CodeNoeAnbar" INTEGER,
    "ccAnbar" INTEGER,
    "TarikhForm" TIMESTAMP,
    "CodeNoeForm" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "ccKalacode" INTEGER,
    "ShomarehBach" VARCHAR(50),
    "TarikhTolid" TIMESTAMP,
    "TarikhEngheza" TIMESTAMP,
    "Tedad" INTEGER,
    "ccRefrence" INTEGER,
    "TarikhEntry" TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public."KardexFlat" (
    "ccKardexFlat" INTEGER,
    "Sal" INTEGER,
    "ccKardex" INTEGER,
    "ccKardexSatr" INTEGER,
    "ccKardexSatrGhesmat" INTEGER,
    "ccAnbarGhesmat" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccAnbar" INTEGER,
    "CodeNoeAnbar" INTEGER,
    "CodeNoeForm" INTEGER,
    "CodeNoeAmalyat" INTEGER,
    "ShomarehForm" INTEGER,
    "TarikhForm" TIMESTAMP,
    "ccRefrence" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "ccKala" INTEGER,
    "ccKalaCode" INTEGER,
    "CodeNoeKala" INTEGER,
    "ShomarehBach" VARCHAR(20),
    "TarikhTolid" TIMESTAMP,
    "TarikhEngheza" TIMESTAMP,
    "Tedad3" DOUBLE PRECISION,
    "Tedad4" DOUBLE PRECISION,
    "GheymatMiangin" DOUBLE PRECISION,
    "GheymatMoaserMiangin" DOUBLE PRECISION,
    "GheymatKharid" DOUBLE PRECISION,
    "GheymatForosh" DOUBLE PRECISION,
    "GheymatMianginTaminKonandeh" DOUBLE PRECISION,
    "GheymatForoshKhalesKala" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "Maliat" DOUBLE PRECISION,
    "Avarez" DOUBLE PRECISION,
    "NoeKharid" INTEGER,
    "ccDarkhastFaktorSatr" INTEGER,
    "TakhfifFaktor" DOUBLE PRECISION,
    "GheymatMianginTemp" DOUBLE PRECISION,
    "ccMarkazPakhshBe" INTEGER,
    "GheymatMasrafKonandeh" DOUBLE PRECISION,
    "GheymatTempLast" DOUBLE PRECISION,
    "GhatiAmani" INTEGER, PRIMARY KEY ("ccKardexFlat", "Sal")
);

CREATE TABLE IF NOT EXISTS public."KardexSatr" (
    "ccKardex" INTEGER,
    "ccKardexSatr" INTEGER,
    "Sal" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "ccKala" INTEGER,
    "ccKalaCode" INTEGER,
    "ShomarehBach" VARCHAR(20),
    "TarikhTolid" TIMESTAMP,
    "TarikhEngheza" TIMESTAMP,
    "Tedad1" DOUBLE PRECISION,
    "Tedad2" DOUBLE PRECISION,
    "Tedad3" DOUBLE PRECISION,
    "Mojody" DOUBLE PRECISION,
    "Gheymat" DOUBLE PRECISION,
    "ccElat" INTEGER,
    "Gheymat2" DOUBLE PRECISION,
    "GheymatKolM" DOUBLE PRECISION,
    "ccDarkhastFaktor" INTEGER,
    "Gheymat3" DOUBLE PRECISION,
    "CodeNoeKala" INTEGER,
    "ccAfrad" INTEGER,
    "Gheymat4" DOUBLE PRECISION,
    "Gheymat5" DOUBLE PRECISION,
    "TarikhForm" TIMESTAMP,
    "Tedad4" DOUBLE PRECISION,
    "TakhfifFaktor" DOUBLE PRECISION,
    "Maliat" DOUBLE PRECISION,
    "Avarez" DOUBLE PRECISION,
    "Gheymat7" DOUBLE PRECISION,
    "Gheymat6" DOUBLE PRECISION,
    "NoeKharid" INTEGER,
    "Sharh" VARCHAR(200),
    "ccDarkhastFaktorSatr" INTEGER,
    "GheymatTemp" DOUBLE PRECISION,
    "GheymatTempLast" DOUBLE PRECISION,
    "GhatiAmani" INTEGER, PRIMARY KEY ("ccKardexSatr", "Sal")
);

CREATE TABLE IF NOT EXISTS public."KardexSatrGhesmat" (
    "ccKardexSatr" INTEGER,
    "ccAnbarGhesmat" INTEGER,
    "Tedad" DOUBLE PRECISION,
    "Mojody" DOUBLE PRECISION,
    "TarikhForm" TIMESTAMP,
    "Tedad4" DOUBLE PRECISION,
    "ccKardexSatrGhesmat" INTEGER,
    "Sal" INTEGER, PRIMARY KEY ("ccKardexSatrGhesmat", "Sal")
);

CREATE TABLE IF NOT EXISTS public."KardexTafkikHavaleh" (
    "ccKardexTafkikHavaleh" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "Shomareh" INTEGER,
    "Tarikh" TIMESTAMP,
    "Sharh" VARCHAR(200),
    "CodeVazeiat" INTEGER,
    "CodeNoeHaml" INTEGER,
    "CodeNoeHavaleh" INTEGER, PRIMARY KEY ("ccKardexTafkikHavaleh")
);

CREATE TABLE IF NOT EXISTS public."KardexTafkikHavalehSatr" (
    "ccKardexTafkikHavaleh" INTEGER,
    "ccKardex" INTEGER, PRIMARY KEY ("ccKardexTafkikHavaleh", "ccKardex")
);

CREATE TABLE IF NOT EXISTS public."KardexTarikh" (
    "ccKardexTarikh" INTEGER,
    "ccKardex" INTEGER,
    "TarikhErsalMoadian" TIMESTAMP,
    "CodeNoeForm" INTEGER, PRIMARY KEY ("ccKardexTarikh")
);

CREATE TABLE IF NOT EXISTS public."KardexVazeiat" (
    "ccKardex" INTEGER,
    "ccKardexVazeiat" INTEGER,
    "CodeVazeiat" INTEGER,
    "ZamanVazeiat" TIMESTAMP, PRIMARY KEY ("ccKardexVazeiat")
);

CREATE TABLE IF NOT EXISTS public."MarjoeeJavayez" (
    "ccMarjoeeJavayez" INTEGER,
    "ccDarkhastFaktor" INTEGER,
    "ccJayezeh" INTEGER,
    "ccKalaCode" INTEGER,
    "Tedad" INTEGER, PRIMARY KEY ("ccMarjoeeJavayez")
);

CREATE TABLE IF NOT EXISTS public."MohasebehMianginGhatee" (
    "ccMohasebehMianginGhatee" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeNoeMohasebeh" INTEGER,
    "ccUser" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccMohasebehMianginGhatee")
);

CREATE TABLE IF NOT EXISTS public."MohasebehMianginGhateeBK" (
    "ccMohasebehMianginGhatee" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeNoeMohasebeh" INTEGER,
    "ccUser" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public."MohasebehMianginGhateebk2" (
    "ccMohasebehMianginGhatee" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeNoeMohasebeh" INTEGER,
    "ccUser" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public."Mojody" (
    "ccKala" INTEGER,
    "ccKalaCode" INTEGER,
    "ShomarehBach" VARCHAR(20),
    "TarikhTolid" TIMESTAMP,
    "TarikhEngheza" TIMESTAMP,
    "ccAnbar" INTEGER,
    "ccAnbarghesmat" INTEGER,
    "Mojody" DOUBLE PRECISION,
    "ccKardexEffect" INTEGER
);

CREATE TABLE IF NOT EXISTS public."MojodyRooz" (
    "ccMojodyRooz" INTEGER,
    "Tarikh" TIMESTAMP,
    "ccKala" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "Mojody" INTEGER, PRIMARY KEY ("ccMojodyRooz")
);

CREATE TABLE IF NOT EXISTS public."NoeDastehBandiNezaraty" (
    "ccNoeDastehBandiNezaraty" INTEGER,
    "Sharh" VARCHAR(50), PRIMARY KEY ("ccNoeDastehBandiNezaraty")
);

CREATE TABLE IF NOT EXISTS public."NoeForm" (
    "CodeNoeForm" INTEGER,
    "NameNoeform" VARCHAR(50), PRIMARY KEY ("CodeNoeForm")
);

CREATE TABLE IF NOT EXISTS public."Sefaresh" (
    "ccMarkazPakhsh" INTEGER,
    "ccSefaresh" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "CodeNoeSefaresh" INTEGER,
    "ShomarehSefaresh" INTEGER,
    "TarikhSefaresh" TIMESTAMP,
    "TarikhNiaz" TIMESTAMP,
    "ccDarkhastFaktor" INTEGER,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(100),
    "TarikhErsal" TIMESTAMP,
    "Tozihat" VARCHAR(100), PRIMARY KEY ("ccSefaresh")
);

CREATE TABLE IF NOT EXISTS public."SefareshSatr" (
    "ccSefaresh" INTEGER,
    "ccSefareshSatr" INTEGER,
    "ccKala" INTEGER,
    "Tedad1" DOUBLE PRECISION,
    "Tedad2" DOUBLE PRECISION,
    "AzTarikh" TIMESTAMP,
    "TaTarikh" TIMESTAMP,
    "SefareshPishnahady" INTEGER,
    "CodeNoeKala" INTEGER,
    "Tozihat" VARCHAR(100), PRIMARY KEY ("ccSefareshSatr")
);

CREATE TABLE IF NOT EXISTS public."SystemConfig" (
    "EjbaryKalaGoroh" TEXT,
    "EjbaryKalaTaminkonandeh" TEXT,
    "EjbaryKalaGheimat" TEXT,
    "HaveModatVosolCheckKartabl" TEXT,
    "TedadroozGozashtehSefaresh" INTEGER,
    "ZaribForoshForTaeedKala" TEXT
);

CREATE TABLE IF NOT EXISTS public."TafkikAnbar" (
    "ccMarkazPakhsh" INTEGER,
    "ccTafkikAnbar" INTEGER,
    "ShomarehTafkikAnbar" INTEGER,
    "TarikhTafkikAnbar" TIMESTAMP,
    "TarikhPishBiniErsal" TIMESTAMP,
    "TarikhErsal" TIMESTAMP,
    "SaatErsal" TIMESTAMP,
    "ccNoeMashin" INTEGER,
    "ccMashin" INTEGER,
    "ccAfradRanandeh" INTEGER,
    "ccAfradMamorPakhsh" INTEGER,
    "TarikhDariaft" TIMESTAMP,
    "SaatDariaft" TIMESTAMP,
    "MasirTedad" INTEGER,
    "CodeVazeiat" INTEGER,
    "ccUser" INTEGER,
    "TarikhBargasht" TIMESTAMP,
    "SaatBargasht" TIMESTAMP,
    "Sharh" VARCHAR(200),
    "ViewTaghvimPakhsh" INTEGER, PRIMARY KEY ("ccTafkikAnbar")
);

CREATE TABLE IF NOT EXISTS public."TafkikAnbarSatr" (
    "ccTafkikAnbar" INTEGER,
    "ccTafkikAnbarSatr" INTEGER,
    "ccKardex" INTEGER, PRIMARY KEY ("ccTafkikAnbarSatr")
);

CREATE TABLE IF NOT EXISTS public."Vahed" (
    "ccVahed" INTEGER,
    "NameVahed" VARCHAR(50),
    "CodeNoeVahed" INTEGER, PRIMARY KEY ("ccVahed")
);

CREATE TABLE IF NOT EXISTS public."VahedTabdil" (
    "ccVahedAz" INTEGER,
    "ccVahedBe" INTEGER,
    "Zarib" NUMERIC, PRIMARY KEY ("ccVahedAz", "ccVahedBe")
);

CREATE TABLE IF NOT EXISTS public."VazeiatMarjoeeFaktor" (
    "ccVazeiatMarjoeeFaktor" INTEGER,
    "ccDarkhastFaktor" INTEGER,
    "Tarikh" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "ccAnbar" INTEGER,
    "ccElat" INTEGER, PRIMARY KEY ("ccVazeiatMarjoeeFaktor")
);

CREATE TABLE IF NOT EXISTS public."VazeiatSefaresh" (
    "ccVazeiatSefaresh" INTEGER,
    "ccSefaresh" INTEGER,
    "CodeVazeiat" INTEGER,
    "Tarikh" TIMESTAMP, PRIMARY KEY ("ccVazeiatSefaresh")
);