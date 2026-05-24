CREATE TABLE IF NOT EXISTS public."AdamDarkhast" (
    "ccAdamDarkhast" INTEGER,
    "ccAdamDarkhastPPC" VARCHAR(20),
    "ccMantagheh" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccForoshandeh" INTEGER,
    "NoeForoshandeh" INTEGER,
    "ccAfradForoshandeh" INTEGER,
    "ccMoshtary" INTEGER,
    "ccShahrMoshtary" INTEGER,
    "ShomarehAdamDarkhast" INTEGER,
    "TarikhAdamDarkhast" TIMESTAMP,
    "SaatMorajeehBeMoshtary" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "CodeNoeVorod" INTEGER,
    "DateVorod" TIMESTAMP,
    "ccElatAdamDarkhast" INTEGER,
    "imageName" VARCHAR(50),
    "VisitTime" VARCHAR(-1),
    "X" DOUBLE PRECISION,
    "Y" DOUBLE PRECISION,
    "Description" VARCHAR(-1),
    "DeviceChargeStatus" INTEGER,
    "insertDate" TIMESTAMP,
    "CodeDoreh" INTEGER,
    "NoOrderGuid" TEXT,
    "Tozihat" VARCHAR(200), PRIMARY KEY ("ccAdamDarkhast")
);

CREATE TABLE IF NOT EXISTS public."AdamDarkhastSatr" (
    "ccAdamDarkhast" INTEGER,
    "ccElatAdamDarkhast" INTEGER,
    "CodeVazeiat" INTEGER,
    "DateVorod" TIMESTAMP,
    "ccKala" INTEGER,
    "Description" VARCHAR(-1),
    "Tedad" DOUBLE PRECISION,
    "ccAdamDarkhastSatr" INTEGER, PRIMARY KEY ("ccAdamDarkhastSatr")
);

CREATE TABLE IF NOT EXISTS public."AeenNamehJaizehForosh03RialeDastehbandiJaizeh" (
    "ccRialeDastehbandiJaizeh" INTEGER,
    "ccDastehBandyJaizehForosh" INTEGER,
    "AzTarikh" TIMESTAMP,
    "EmtiazAz" DOUBLE PRECISION,
    "EmtiazTa" DOUBLE PRECISION,
    "RialJaizeh" INTEGER, PRIMARY KEY ("ccRialeDastehbandiJaizeh")
);

CREATE TABLE IF NOT EXISTS public."DarkhastFaktor" (
    "ccDarkhastFaktor" INTEGER,
    "Sal" INTEGER,
    "CodeNoeVorod" INTEGER,
    "ccMantaghehPakhsh" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccForoshandeh" INTEGER,
    "NoeForoshandeh" INTEGER,
    "ccAfradForoshandeh" INTEGER,
    "ccMoshtary" INTEGER,
    "ccShahrMoshtary" INTEGER,
    "ccAddressMoshtary" INTEGER,
    "EtebarJary" DOUBLE PRECISION,
    "ShomarehDarkhast" INTEGER,
    "TarikhDarkhast" TIMESTAMP,
    "ShomarehFaktor" INTEGER,
    "TarikhFaktor" TIMESTAMP,
    "TarikhPishbinyTahvil" TIMESTAMP,
    "TarikhErsal" TIMESTAMP,
    "CodeNoeVosolAzMoshtary" INTEGER,
    "ModateVosol" INTEGER,
    "CodeNoeHaml" INTEGER,
    "ccNoeMashin" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(50),
    "MablaghKolDarkhast" DOUBLE PRECISION,
    "MablaghTakhfifDarkhastTitr" DOUBLE PRECISION,
    "MablaghTakhfifDarkhastSatr" DOUBLE PRECISION,
    "MablaghKhalesDarkhast" DOUBLE PRECISION,
    "MablaghKolFaktor" DOUBLE PRECISION,
    "MablaghTakhfifFaktorTitr" DOUBLE PRECISION,
    "MablaghTakhfifFaktorSatr" DOUBLE PRECISION,
    "MablaghEzafat" DOUBLE PRECISION,
    "MablaghKhalesFaktor" DOUBLE PRECISION,
    "MablaghVajhDaryaftyFaktor" DOUBLE PRECISION,
    "DateVorod" TIMESTAMP,
    "SaatVorodBeMaghazeh" TIMESTAMP,
    "SaatKhorojAzMaghazeh" TIMESTAMP,
    "ccUser" INTEGER,
    "ccGorohForosh" INTEGER,
    "ModatRoozRaasGiri" INTEGER,
    "MablaghTakhfifFaktorTaavoni" DOUBLE PRECISION,
    "SumTedad3" INTEGER,
    "ccAfradGorohForosh" INTEGER,
    "InvCode" INTEGER,
    "Serial" INTEGER,
    "DiscntType" INTEGER,
    "DiscntSubType" INTEGER,
    "ccNoeMoshtary" INTEGER,
    "ccNoeSenf" INTEGER,
    "ShomarehFaktorIndex" INTEGER,
    "ccDorehMaly" INTEGER,
    "BeMasoliat" INTEGER,
    "SumMaliat" DOUBLE PRECISION,
    "SumAvarez" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "ccDarkhastFaktorPPC" VARCHAR(40),
    "HoghoghiShodeh" INTEGER,
    "TarikhTahvil" TIMESTAMP,
    "SaatTahvil" TIMESTAMP,
    "TarikhSarResid" TIMESTAMP,
    "ccForoshandehAsli" INTEGER,
    "ID_Sms" INTEGER,
    "TarikhErsalSms" TIMESTAMP,
    "CountPrint" INTEGER,
    "ccMasir" INTEGER,
    "DarsadTakhfifKhazaneh" DOUBLE PRECISION,
    "InvoiceType" INTEGER,
    "Type" INTEGER,
    "X" DOUBLE PRECISION,
    "Y" DOUBLE PRECISION,
    "DetailsCount" INTEGER,
    "Sharh" VARCHAR(-1),
    "NoeFaktor" INTEGER,
    "OrderGuid" TEXT,
    "IsFormal" TEXT,
    "SignatureImage" VARCHAR(250),
    "ID_WebSite" INTEGER,
    "CountPrintJayezeh" INTEGER,
    "TelephoneOrder" TEXT,
    "DeviceChargeStatus" INTEGER,
    "ReferenceNumber" VARCHAR(250),
    "MablaghMandehMoshtary" DOUBLE PRECISION,
    "ModateVosolOld" INTEGER,
    "TasviehPayeBar" INTEGER, PRIMARY KEY ("ccDarkhastFaktor", "Sal")
);

CREATE TABLE IF NOT EXISTS public."DarkhastFaktorbkbeforupvaz" (
    "ccDarkhastFaktor" INTEGER,
    "Sal" INTEGER,
    "CodeNoeVorod" INTEGER,
    "ccMantaghehPakhsh" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccForoshandeh" INTEGER,
    "NoeForoshandeh" INTEGER,
    "ccAfradForoshandeh" INTEGER,
    "ccMoshtary" INTEGER,
    "ccShahrMoshtary" INTEGER,
    "ccAddressMoshtary" INTEGER,
    "EtebarJary" DOUBLE PRECISION,
    "ShomarehDarkhast" INTEGER,
    "TarikhDarkhast" TIMESTAMP,
    "ShomarehFaktor" INTEGER,
    "TarikhFaktor" TIMESTAMP,
    "TarikhPishbinyTahvil" TIMESTAMP,
    "TarikhErsal" TIMESTAMP,
    "CodeNoeVosolAzMoshtary" INTEGER,
    "ModateVosol" INTEGER,
    "CodeNoeHaml" INTEGER,
    "ccNoeMashin" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(50),
    "MablaghKolDarkhast" DOUBLE PRECISION,
    "MablaghTakhfifDarkhastTitr" DOUBLE PRECISION,
    "MablaghTakhfifDarkhastSatr" DOUBLE PRECISION,
    "MablaghKhalesDarkhast" DOUBLE PRECISION,
    "MablaghKolFaktor" DOUBLE PRECISION,
    "MablaghTakhfifFaktorTitr" DOUBLE PRECISION,
    "MablaghTakhfifFaktorSatr" DOUBLE PRECISION,
    "MablaghEzafat" DOUBLE PRECISION,
    "MablaghKhalesFaktor" DOUBLE PRECISION,
    "MablaghVajhDaryaftyFaktor" DOUBLE PRECISION,
    "DateVorod" TIMESTAMP,
    "SaatVorodBeMaghazeh" TIMESTAMP,
    "SaatKhorojAzMaghazeh" TIMESTAMP,
    "ccUser" INTEGER,
    "ccGorohForosh" INTEGER,
    "ModatRoozRaasGiri" INTEGER,
    "MablaghTakhfifFaktorTaavoni" DOUBLE PRECISION,
    "SumTedad3" INTEGER,
    "ccAfradGorohForosh" INTEGER,
    "InvCode" INTEGER,
    "Serial" INTEGER,
    "DiscntType" INTEGER,
    "DiscntSubType" INTEGER,
    "ccNoeMoshtary" INTEGER,
    "ccNoeSenf" INTEGER,
    "ShomarehFaktorIndex" INTEGER,
    "ccDorehMaly" INTEGER,
    "BeMasoliat" INTEGER,
    "SumMaliat" DOUBLE PRECISION,
    "SumAvarez" DOUBLE PRECISION,
    "MablaghMandehMoshtary" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "ccDarkhastFaktorPPC" VARCHAR(40),
    "HoghoghiShodeh" INTEGER,
    "TarikhTahvil" TIMESTAMP,
    "SaatTahvil" TIMESTAMP,
    "TarikhSarResid" TIMESTAMP,
    "ccForoshandehAsli" INTEGER,
    "ID_Sms" INTEGER,
    "TarikhErsalSms" TIMESTAMP,
    "CountPrint" INTEGER,
    "ccMasir" INTEGER,
    "DarsadTakhfifKhazaneh" DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS public."DarkhastFaktorBKFAKTOR" (
    "ccDarkhastFaktor" INTEGER,
    "Sal" INTEGER,
    "CodeNoeVorod" INTEGER,
    "ccMantaghehPakhsh" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccForoshandeh" INTEGER,
    "NoeForoshandeh" INTEGER,
    "ccAfradForoshandeh" INTEGER,
    "ccMoshtary" INTEGER,
    "ccShahrMoshtary" INTEGER,
    "ccAddressMoshtary" INTEGER,
    "EtebarJary" DOUBLE PRECISION,
    "ShomarehDarkhast" INTEGER,
    "TarikhDarkhast" TIMESTAMP,
    "ShomarehFaktor" INTEGER,
    "TarikhFaktor" TIMESTAMP,
    "TarikhPishbinyTahvil" TIMESTAMP,
    "TarikhErsal" TIMESTAMP,
    "CodeNoeVosolAzMoshtary" INTEGER,
    "ModateVosol" INTEGER,
    "CodeNoeHaml" INTEGER,
    "ccNoeMashin" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(50),
    "MablaghKolDarkhast" DOUBLE PRECISION,
    "MablaghTakhfifDarkhastTitr" DOUBLE PRECISION,
    "MablaghTakhfifDarkhastSatr" DOUBLE PRECISION,
    "MablaghKhalesDarkhast" DOUBLE PRECISION,
    "MablaghKolFaktor" DOUBLE PRECISION,
    "MablaghTakhfifFaktorTitr" DOUBLE PRECISION,
    "MablaghTakhfifFaktorSatr" DOUBLE PRECISION,
    "MablaghEzafat" DOUBLE PRECISION,
    "MablaghKhalesFaktor" DOUBLE PRECISION,
    "MablaghVajhDaryaftyFaktor" DOUBLE PRECISION,
    "DateVorod" TIMESTAMP,
    "SaatVorodBeMaghazeh" TIMESTAMP,
    "SaatKhorojAzMaghazeh" TIMESTAMP,
    "ccUser" INTEGER,
    "ccGorohForosh" INTEGER,
    "ModatRoozRaasGiri" INTEGER,
    "MablaghTakhfifFaktorTaavoni" DOUBLE PRECISION,
    "SumTedad3" INTEGER,
    "ccAfradGorohForosh" INTEGER,
    "InvCode" INTEGER,
    "Serial" INTEGER,
    "DiscntType" INTEGER,
    "DiscntSubType" INTEGER,
    "ccNoeMoshtary" INTEGER,
    "ccNoeSenf" INTEGER,
    "ShomarehFaktorIndex" INTEGER,
    "ccDorehMaly" INTEGER,
    "BeMasoliat" INTEGER,
    "SumMaliat" DOUBLE PRECISION,
    "SumAvarez" DOUBLE PRECISION,
    "MablaghMandehMoshtary" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "ccDarkhastFaktorPPC" VARCHAR(40),
    "HoghoghiShodeh" INTEGER,
    "TarikhTahvil" TIMESTAMP,
    "SaatTahvil" TIMESTAMP,
    "TarikhSarResid" TIMESTAMP,
    "ccForoshandehAsli" INTEGER,
    "ID_Sms" INTEGER,
    "TarikhErsalSms" TIMESTAMP,
    "CountPrint" INTEGER,
    "ccMasir" INTEGER
);

CREATE TABLE IF NOT EXISTS public."DarkhastFaktorEstemhal" (
    "ccDarkhastFaktorEstemhal" INTEGER,
    "TarikhSabt" TIMESTAMP,
    "ccDarkhastFaktor" INTEGER,
    "RoozTakhir" INTEGER,
    "CodeMojavez" VARCHAR(10),
    "TarikhMojavez" TIMESTAMP,
    "MojavezDahandeh" VARCHAR(50),
    "CodeBeOhdeh" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "Tozihat" VARCHAR(250),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "ccGoroh" INTEGER,
    "Sharh" VARCHAR(-1), PRIMARY KEY ("ccDarkhastFaktorEstemhal")
);

CREATE TABLE IF NOT EXISTS public."DarkhastFaktorModatVosol_Log" (
    "ccDarkhastFaktor" INTEGER,
    "ModateVosol" INTEGER,
    "ModateVosolOld" INTEGER,
    "ModatRoozRaasGiri" INTEGER,
    "TarikhFaktor" TIMESTAMP,
    "TarikhSarResid" TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public."DarkhastFaktorSatr" (
    "ccDarkhastFaktor" INTEGER,
    "ccDarkhastFaktorSatr" INTEGER,
    "Sal" INTEGER,
    "ccKala" INTEGER,
    "ccKalaCode" INTEGER,
    "ShomarehBach" VARCHAR(100),
    "TarikhTolid" TIMESTAMP,
    "TarikhEngheza" TIMESTAMP,
    "Tedad1" DOUBLE PRECISION,
    "Tedad2" DOUBLE PRECISION,
    "Tedad3" DOUBLE PRECISION,
    "MablaghForosh" DOUBLE PRECISION,
    "MablaghTakhfifDarkhast" DOUBLE PRECISION,
    "MablaghTakhfifFaktor" DOUBLE PRECISION,
    "ccTafkikJoze" INTEGER,
    "MojodyGhabelForosh" DOUBLE PRECISION,
    "DateVorod" TIMESTAMP,
    "CodeNoeKala" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "GheymatMiangin" DOUBLE PRECISION,
    "ccDarkhastFaktorSatrTaavoni" INTEGER,
    "ccAfrad" INTEGER,
    "CodeVazeiat" INTEGER,
    "DarsadTakhfifTaavoni" DOUBLE PRECISION,
    "ccUser" INTEGER,
    "MablaghTakhfifNaghdiVahed" DOUBLE PRECISION,
    "GheymatKharid" DOUBLE PRECISION,
    "DiscntType" INTEGER,
    "DiscntSubType" INTEGER,
    "TarikhFaktor" TIMESTAMP,
    "Maliat" DOUBLE PRECISION,
    "Avarez" DOUBLE PRECISION,
    "MablaghForoshKhalesKala" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "ccDarkhastFaktorSatrPPC" VARCHAR(50),
    "ShomarehBachMulti" VARCHAR(-1),
    "MablaghDarkhasti" DOUBLE PRECISION,
    "MablaghTakhfifDasti" DOUBLE PRECISION,
    "ModatVosol" INTEGER,
    "TedadAdadi" DOUBLE PRECISION,
    "TedadBasteh" DOUBLE PRECISION,
    "TedadKarton" DOUBLE PRECISION,
    "AdamJayezehKala" TEXT, PRIMARY KEY ("ccDarkhastFaktorSatr", "Sal")
);

CREATE TABLE IF NOT EXISTS public."DarkhastFaktorSatrTakhfif" (
    "ccDarkhastFaktorSatr" INTEGER,
    "ccDarkhastFaktorSatrTakhfif" INTEGER,
    "Sal" INTEGER,
    "CodeNoeTakhfif" INTEGER,
    "ccTakhfif" INTEGER,
    "DarsadTakhfif" DOUBLE PRECISION,
    "MablaghTakhfif" DOUBLE PRECISION,
    "TarikhFaktor" TIMESTAMP,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "ShomarehBach" VARCHAR(20), PRIMARY KEY ("ccDarkhastFaktorSatrTakhfif", "Sal")
);

CREATE TABLE IF NOT EXISTS public."DarkhastFaktorTakhfif" (
    "ccDarkhastFaktor" INTEGER,
    "ccDarkhastFaktorTakhfif" INTEGER,
    "Sal" INTEGER,
    "CodeNoeTakhfif" INTEGER,
    "ccTakhfif" INTEGER,
    "DarsadTakhfif" DOUBLE PRECISION,
    "MablaghTakhfif" DOUBLE PRECISION,
    "TarikhFaktor" TIMESTAMP,
    "ccSabadKala" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "ccJayezehSatrKala" INTEGER, PRIMARY KEY ("ccDarkhastFaktorTakhfif", "Sal")
);

CREATE TABLE IF NOT EXISTS public."DarkhastFaktorVazeiat" (
    "ccDarkhastFaktor" INTEGER,
    "ccDarkhastFaktorVazeiat" INTEGER,
    "Sal" INTEGER,
    "CodeVazeiat" INTEGER,
    "ZamanVazeiat" TIMESTAMP,
    "ccUser" INTEGER, PRIMARY KEY ("ccDarkhastFaktorVazeiat", "Sal")
);

CREATE TABLE IF NOT EXISTS public."DarkhastFaktorVazeiat20" (
    "ccDarkhastFaktor" INTEGER
);

CREATE TABLE IF NOT EXISTS public."DarkhastFaktorVazeiatHoghoghi" (
    "ccDarkhastFaktor" INTEGER,
    "ccDarkhastFaktorVazeiat" INTEGER,
    "Sal" INTEGER,
    "CodeVazeiat" INTEGER,
    "ZamanVazeiat" TIMESTAMP,
    "ccUser" INTEGER
);

CREATE TABLE IF NOT EXISTS public."DastehBandyJaizehForosh" (
    "ccDastehBandyJaizehForosh" INTEGER,
    "SharhDastehBandyJaizehForosh" VARCHAR(50), PRIMARY KEY ("ccDastehBandyJaizehForosh")
);

CREATE TABLE IF NOT EXISTS public."ElamMarjoee" (
    "ccElamMarjoee" INTEGER,
    "ccElamMarjoeePPC" VARCHAR(20),
    "CodeNoeVorod" INTEGER,
    "ccMantagheh" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccForoshandeh" INTEGER,
    "NoeForoshandeh" INTEGER,
    "ccAfradForoshandeh" INTEGER,
    "ccMoshtary" INTEGER,
    "ccShahrMoshtary" INTEGER,
    "ShomarehElamMarjoee" INTEGER,
    "TarikhElamMarjoee" TIMESTAMP,
    "ccDarkhastFaktor" INTEGER,
    "NextFaktor" INTEGER,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(50),
    "DateVorod" TIMESTAMP, PRIMARY KEY ("ccElamMarjoee")
);

CREATE TABLE IF NOT EXISTS public."ElamMarjoeeSatr" (
    "ccElamMarjoee" INTEGER,
    "ccElamMarjoeeSatr" INTEGER,
    "ccDarkhastFaktor" INTEGER,
    "ccKala" INTEGER,
    "ccKalaCode" INTEGER,
    "ShomarehBach" VARCHAR(10),
    "TarikhTolid" TIMESTAMP,
    "TarikhEngheza" TIMESTAMP,
    "Tedad1" INTEGER,
    "Tedad2" INTEGER,
    "Tedad3" INTEGER,
    "Fee" INTEGER,
    "ccElatMarjoee" INTEGER,
    "CodeNoeMarjoee" INTEGER,
    "DateVorod" TIMESTAMP, PRIMARY KEY ("ccElamMarjoeeSatr")
);

CREATE TABLE IF NOT EXISTS public."ElatAdamDarkhast" (
    "ccElatAdamDarkhast" INTEGER,
    "NameElatAdamDarkhast" VARCHAR(50), PRIMARY KEY ("ccElatAdamDarkhast")
);

CREATE TABLE IF NOT EXISTS public."ElatAdamFaalMoshtary" (
    "ccElatAdamFaalMoshtary" INTEGER,
    "NameElatAdamFaalMoshtary" VARCHAR(50), PRIMARY KEY ("ccElatAdamFaalMoshtary")
);

CREATE TABLE IF NOT EXISTS public."ElatAdamForoshMarkazPakhsh" (
    "ccElatAdamForoshMarkazPakhsh" INTEGER,
    "CodeVahed" INTEGER,
    "NameElatAdamForoshMarkazPakhsh" VARCHAR(50), PRIMARY KEY ("ccElatAdamForoshMarkazPakhsh")
);

CREATE TABLE IF NOT EXISTS public."ElatMarjoee" (
    "ccElatMarjoee" INTEGER,
    "NameElatMarjoee" VARCHAR(50), PRIMARY KEY ("ccElatMarjoee")
);

CREATE TABLE IF NOT EXISTS public."EshantionDarkhast" (
    "ccEshantionDarkhast" INTEGER,
    "ccDarkhastFaktor" INTEGER,
    "ccKala" INTEGER,
    "Tedad" INTEGER,
    "TedadAdadi" DOUBLE PRECISION,
    "TedadBasteh" DOUBLE PRECISION,
    "TedadKarton" DOUBLE PRECISION,
    "ShomarehBach" VARCHAR(100), PRIMARY KEY ("ccEshantionDarkhast")
);

CREATE TABLE IF NOT EXISTS public."Estemhal" (
    "ccEstemhal" INTEGER,
    "ccDarkhastFaktor" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ShomarehFaktor" INTEGER,
    "TarikhVorodEstemhal" TIMESTAMP,
    "Estemhal" INTEGER,
    "MasoulEstemhal" INTEGER,
    "ShomarehMojavez" VARCHAR(20),
    "TarikhMojavez" TIMESTAMP,
    "MalekeMojavez" VARCHAR(100),
    "Description" VARCHAR(200),
    "Attachment" VARCHAR(-1),
    "Control" TEXT, PRIMARY KEY ("ccEstemhal")
);

CREATE TABLE IF NOT EXISTS public."EtebarDastehBandy" (
    "ccEtebarDastehBandy" INTEGER,
    "ccGoroh" INTEGER,
    "EtebarRialy" DOUBLE PRECISION,
    "EtebarTedady" DOUBLE PRECISION,
    "RoozMotalebat" INTEGER,
    "SaghfFaktor" DOUBLE PRECISION,
    "SaghfRoozSayadi" DOUBLE PRECISION, PRIMARY KEY ("ccEtebarDastehBandy")
);

CREATE TABLE IF NOT EXISTS public."EtebarMojazAeenNameh" (
    "ccEMojaz" INTEGER,
    "CodeNoeLevelEtebar" INTEGER,
    "MaxEtebarRialy" DOUBLE PRECISION,
    "MaxEtebarTedady" DOUBLE PRECISION,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(255),
    "ccGoroh" INTEGER,
    "RoozMotalebat" INTEGER,
    "SaghfFaktor" DOUBLE PRECISION,
    "SaghfRoozSayadi" DOUBLE PRECISION, PRIMARY KEY ("ccEMojaz")
);

CREATE TABLE IF NOT EXISTS public."Foroshandeh" (
    "ccMarkazPakhsh" INTEGER,
    "ccForoshandeh" INTEGER,
    "NoeForoshandeh" INTEGER,
    "RoozMojaz" INTEGER,
    "MaxTedadCheckBargashty" INTEGER,
    "MaxMablaghCheckBargashty" DOUBLE PRECISION,
    "MaxModatCheckBargashty" INTEGER,
    "MaxTedadFaktorBaz" INTEGER,
    "MaxMablaghFaktorBaz" DOUBLE PRECISION,
    "CodeVazeiat" INTEGER,
    "CodeForoshandehOld" VARCHAR(10),
    "SharhForoshandeh" VARCHAR(50),
    "ccAfrad" INTEGER,
    "ccGorohForosh" INTEGER,
    "MobileNumber" VARCHAR(50),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "DeviceIMEI" VARCHAR(-1),
    "MaxTedadChekSayad" INTEGER,
    "MaxMablaghChekSayad" DOUBLE PRECISION,
    "MaxModatChekSayad" INTEGER, PRIMARY KEY ("ccForoshandeh")
);

CREATE TABLE IF NOT EXISTS public."ForoshandehBeForoshandeh" (
    "ccForoshandehBeForoshandeh" INTEGER,
    "ccForoshandeh" INTEGER,
    "ccForoshandehLink" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP, PRIMARY KEY ("ccForoshandehBeForoshandeh")
);

CREATE TABLE IF NOT EXISTS public."ForoshandehKalaSahmiehBandy" (
    "ccKalaCode" INTEGER,
    "ccForoshandeh" INTEGER,
    "ccKalaSahmiehBandy" INTEGER,
    "NesbatSahmieh" DOUBLE PRECISION,
    "TedadMojody" DOUBLE PRECISION,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(50),
    "TedadSahmieh" INTEGER, PRIMARY KEY ("ccKalaSahmiehBandy")
);

CREATE TABLE IF NOT EXISTS public."ForoshandehMoshtary" (
    "ccForoshandeh" INTEGER,
    "ccMoshtary" INTEGER,
    "ccMasir" INTEGER,
    "ccForoshandehMoshtary" INTEGER,
    "RoozVizit" INTEGER,
    "Olaviat" INTEGER,
    "CodeVazeiat" INTEGER,
    "ElatGheirFaalMoshtary" VARCHAR(200),
    "CodeNoeUpdate" INTEGER,
    "CodeNoeVorod" INTEGER, PRIMARY KEY ("ccForoshandehMoshtary")
);

CREATE TABLE IF NOT EXISTS public."ForoshandehNoeMoshtary" (
    "ccForoshandeh" INTEGER,
    "ccGoroh" INTEGER,
    "ccForoshandehNoeMoshtary" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(50), PRIMARY KEY ("ccForoshandehNoeMoshtary")
);

CREATE TABLE IF NOT EXISTS public."GorohForosh" (
    "ccMarkazPakhsh" INTEGER,
    "ccGorohForosh" INTEGER,
    "CodeGorohForosh" VARCHAR(10),
    "SharhGorohForosh" VARCHAR(50),
    "ccAfrad" INTEGER,
    "CodeVazeiat" INTEGER, PRIMARY KEY ("ccGorohForosh")
);

CREATE TABLE IF NOT EXISTS public."GorohOlaviatTozih" (
    "ccGorohOlaviatTozih" INTEGER,
    "ccGoroh" INTEGER,
    "OlaviatTozih" INTEGER, PRIMARY KEY ("ccGorohOlaviatTozih")
);

CREATE TABLE IF NOT EXISTS public."GorohTahtehNazar" (
    "ccMarkazPakhsh" INTEGER,
    "ccGoroh" INTEGER
);

CREATE TABLE IF NOT EXISTS public."hadaf" (
    "ccHadaf" INTEGER,
    "Version" INTEGER,
    "Sal" INTEGER,
    "Mah" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccGorohForosh" INTEGER,
    "ccForoshandeh" INTEGER,
    "ccKalaCode" INTEGER,
    "Tedad" DOUBLE PRECISION,
    "Rial" DOUBLE PRECISION,
    "ccGoroh" INTEGER,
    "Padash" DOUBLE PRECISION, PRIMARY KEY ("ccHadaf")
);

CREATE TABLE IF NOT EXISTS public."Hadaf_DP" (
    "ccHadaf" INTEGER,
    "Sal" INTEGER,
    "Version" INTEGER,
    "MablaghHadafSal" DOUBLE PRECISION, PRIMARY KEY ("ccHadaf")
);

CREATE TABLE IF NOT EXISTS public."Hadaf_PG" (
    "ccHadaf" INTEGER,
    "sal" INTEGER,
    "mah" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccKalaCode" INTEGER,
    "ccKala" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "Tedad" DOUBLE PRECISION, PRIMARY KEY ("ccHadaf")
);

CREATE TABLE IF NOT EXISTS public."HadafForoshandeh_DP" (
    "ccHadafForoshandeh" INTEGER,
    "ccHadafMarkazPakhsh" INTEGER,
    "ccForoshandeh" INTEGER,
    "Darsad" DOUBLE PRECISION, PRIMARY KEY ("ccHadafForoshandeh")
);

CREATE TABLE IF NOT EXISTS public."HadafForoshandeh_PG" (
    "ccHadafForoshandeh_PG" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "ccKala" INTEGER,
    "ccKalaCode" INTEGER,
    "AzTarikh" TIMESTAMP,
    "TaTarikh" TIMESTAMP,
    "Sal" INTEGER,
    "Mah" INTEGER,
    "ccForoshandeh" INTEGER,
    "Zarib1" DOUBLE PRECISION,
    "Zarib2" DOUBLE PRECISION,
    "Tarikh" TIMESTAMP, PRIMARY KEY ("ccHadafForoshandeh_PG")
);

CREATE TABLE IF NOT EXISTS public."HadafMah_DP" (
    "ccHadafMah" INTEGER,
    "ccHadaf" INTEGER,
    "Sal" INTEGER,
    "Mah" INTEGER,
    "Darsad" DOUBLE PRECISION,
    "MablaghHadafMah" DOUBLE PRECISION, PRIMARY KEY ("ccHadafMah")
);

CREATE TABLE IF NOT EXISTS public."HadafMoshtary_DP" (
    "ccHadafMoshtary" INTEGER,
    "ccHadafMarkazPakhsh" INTEGER,
    "ccMoshtary" INTEGER,
    "Darsad" DOUBLE PRECISION, PRIMARY KEY ("ccHadafMoshtary")
);

CREATE TABLE IF NOT EXISTS public."HadafSal" (
    "ccHadafSal" INTEGER,
    "Sal" INTEGER,
    "MablaghHadafSal" DOUBLE PRECISION,
    "Version" INTEGER,
    "CodeNoeHadaf" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "MablaghHadafVosoulSal" DOUBLE PRECISION, PRIMARY KEY ("ccHadafSal")
);

CREATE TABLE IF NOT EXISTS public."HadafSalMah" (
    "ccHadafSal" INTEGER,
    "ccHadafSalMah" INTEGER,
    "Mah" INTEGER,
    "DarsadHadafMah" DOUBLE PRECISION,
    "MablaghHadafMah" DOUBLE PRECISION,
    "TedadRoozKari" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "DarsadHadafVosoulMah" DOUBLE PRECISION,
    "MablaghHadafVosoulMah" DOUBLE PRECISION, PRIMARY KEY ("ccHadafSalMah")
);

CREATE TABLE IF NOT EXISTS public."HadafSalMah_M" (
    "ccHadafSalMah" INTEGER,
    "ccHadafSalMah_M" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "DarsadHadafMarkazPakhsh" DOUBLE PRECISION,
    "MablaghHadafMarkazPakhsh" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "MablaghHadafVosoulMarkazPakhsh" DOUBLE PRECISION,
    "DarsadHadafVosoulMarkazPakhsh" DOUBLE PRECISION, PRIMARY KEY ("ccHadafSalMah_M")
);

CREATE TABLE IF NOT EXISTS public."HadafSalMah_MG" (
    "ccHadafSalMah_M" INTEGER,
    "ccHadafSalMah_MG" INTEGER,
    "ccGorohForosh" INTEGER,
    "DarsadHadafGorohForosh" DOUBLE PRECISION,
    "MablaghHadafGorohForosh" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "DarsadHadafVosoulGorohForosh" DOUBLE PRECISION,
    "MablaghHadafVosoulGorohForosh" DOUBLE PRECISION, PRIMARY KEY ("ccHadafSalMah_MG")
);

CREATE TABLE IF NOT EXISTS public."HadafSalMah_MGF" (
    "ccHadafSalMah_MG" INTEGER,
    "ccHadafSalMah_MGF" INTEGER,
    "ccForoshandeh" INTEGER,
    "DarsadHadafForoshandeh" DOUBLE PRECISION,
    "MablaghHadafForoshandeh" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "DarsadHadafVosoulForoshandeh" DOUBLE PRECISION,
    "MablaghHadafVosoulForoshandeh" DOUBLE PRECISION, PRIMARY KEY ("ccHadafSalMah_MGF")
);

CREATE TABLE IF NOT EXISTS public."HadafSalMah_MGFG" (
    "ccHadafSalMah_MGF" INTEGER,
    "ccHadafSalMah_MGFG" INTEGER,
    "ccGorohKala" INTEGER,
    "DarsadHadafGorohKala" DOUBLE PRECISION,
    "MablaghHadafGorohKala" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccHadafSalMah_MGFG")
);

CREATE TABLE IF NOT EXISTS public."HadafSalMah_MGFK" (
    "ccHadafSalMah_MGF" INTEGER,
    "ccHadafSalMah_MGFK" INTEGER,
    "ccKala" INTEGER,
    "DarsadHadafKala" DOUBLE PRECISION,
    "MablaghHadafKala" DOUBLE PRECISION,
    "TedadHadafKala" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccHadafSalMah_MGFK")
);

CREATE TABLE IF NOT EXISTS public."HadafSalMah_MGFM" (
    "ccHadafSalMah_MGF" INTEGER,
    "ccHadafSalMah_MGFM" INTEGER,
    "ccMasir" INTEGER,
    "DarsadHadafMasir" DOUBLE PRECISION,
    "MablaghHadafMasir" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccHadafSalMah_MGFM")
);

CREATE TABLE IF NOT EXISTS public."HadafSalMah_MGFT" (
    "ccHadafSalMah_MGF" INTEGER,
    "ccHadafSalMah_MGFT" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "DarsadHadafTaminKonandeh" DOUBLE PRECISION,
    "MablaghHadafTaminKonandeh" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccHadafSalMah_MGFT")
);

CREATE TABLE IF NOT EXISTS public."HadafSalMarkazPakhsh_DP" (
    "ccHadafMarkazPakhsh" INTEGER,
    "ccHadafMah" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "Darsad" DOUBLE PRECISION, PRIMARY KEY ("ccHadafMarkazPakhsh")
);

CREATE TABLE IF NOT EXISTS public."Jayezeh" (
    "ccJayezeh" INTEGER,
    "CodeNoe" INTEGER,
    "SharhJayezeh" VARCHAR(50),
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "NoeTedadRial" INTEGER,
    "NameNoeFieldMoshtary" INTEGER,
    "ccNoeFieldMoshtary" INTEGER,
    "NoeVosol" INTEGER,
    "CodeVazeiat" INTEGER,
    "ElatAdamTaeedJayzeh" VARCHAR(-1),
    "CodeNoeVorod" INTEGER,
    "OnBach" INTEGER, PRIMARY KEY ("ccJayezeh")
);

CREATE TABLE IF NOT EXISTS public."Jayezehbk" (
    "ccJayezeh" INTEGER,
    "CodeNoe" INTEGER,
    "SharhJayezeh" VARCHAR(50),
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "NoeTedadRial" INTEGER,
    "NameNoeFieldMoshtary" INTEGER,
    "ccNoeFieldMoshtary" INTEGER,
    "NoeVosol" INTEGER,
    "CodeVazeiat" INTEGER,
    "ElatAdamTaeedJayzeh" VARCHAR(-1)
);

CREATE TABLE IF NOT EXISTS public."JayezehPhoto" (
    "ccJayezeh" INTEGER,
    "ccPhoto" INTEGER,
    "ccNoePhoto" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ccUser" INTEGER, PRIMARY KEY ("ccJayezeh", "ccPhoto")
);

CREATE TABLE IF NOT EXISTS public."JayezehSatr" (
    "ccJayezeh" INTEGER,
    "ccJayezehSatr" INTEGER,
    "NameNoeField" INTEGER,
    "ccNoeField" INTEGER,
    "Az" DOUBLE PRECISION,
    "Ta" DOUBLE PRECISION,
    "CodeNoeBastehBandy" INTEGER,
    "BeEza" DOUBLE PRECISION,
    "CodeNoeBastehBandyBeEza" INTEGER,
    "TedadJayezeh" INTEGER,
    "RialJayezeh" DOUBLE PRECISION,
    "ccKalaCodeJayezeh" INTEGER,
    "NoeRialJayezeh" INTEGER,
    "MohasebehAzMazad" TEXT,
    "Darsad" INTEGER,
    "ccJayezehSatrInsert" INTEGER,
    "ShomarehBach" VARCHAR(50), PRIMARY KEY ("ccJayezehSatr")
);

CREATE TABLE IF NOT EXISTS public."JayezehSatrbk" (
    "ccJayezeh" INTEGER,
    "ccJayezehSatr" INTEGER,
    "NameNoeField" INTEGER,
    "ccNoeField" INTEGER,
    "Az" DOUBLE PRECISION,
    "Ta" DOUBLE PRECISION,
    "CodeNoeBastehBandy" INTEGER,
    "BeEza" DOUBLE PRECISION,
    "CodeNoeBastehBandyBeEza" INTEGER,
    "TedadJayezeh" INTEGER,
    "RialJayezeh" DOUBLE PRECISION,
    "ccKalaCodeJayezeh" INTEGER,
    "NoeRialJayezeh" INTEGER,
    "MohasebehAzMazad" TEXT,
    "Darsad" INTEGER,
    "ccJayezehSatrInsert" INTEGER
);

CREATE TABLE IF NOT EXISTS public."JayezehSatrKala" (
    "ccJayezehSatr" INTEGER,
    "ccJayezehSatrKala" INTEGER,
    "DarsadJayezeh" INTEGER,
    "TedadJayezeh" INTEGER,
    "ccKalaCodeJayezeh" INTEGER,
    "NoeRialJayezeh" INTEGER,
    "RialJayezeh" DOUBLE PRECISION,
    "ShomarehBach" VARCHAR(50), PRIMARY KEY ("ccJayezehSatrKala")
);

CREATE TABLE IF NOT EXISTS public."JayezehTaminkonandeh" (
    "ccJayezehTaminkonandeh" INTEGER,
    "CodeNoe" INTEGER,
    "SharhJayezeh" VARCHAR(50),
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "NoeTedadRial" INTEGER,
    "NameNoeFieldMoshtary" INTEGER,
    "ccNoeFieldMoshtary" INTEGER
);

CREATE TABLE IF NOT EXISTS public."JayezehTaminkonandehSatr" (
    "ccJayezehTaminkonandeh" INTEGER,
    "ccJayezehTaminkonandehSatr" INTEGER,
    "NameNoeField" INTEGER,
    "ccNoeField" INTEGER,
    "Az" DOUBLE PRECISION,
    "Ta" DOUBLE PRECISION,
    "CodeNoeBastehBandy" INTEGER,
    "BeEza" DOUBLE PRECISION,
    "CodeNoeBastehBandyBeEza" INTEGER,
    "TedadJayezeh" INTEGER,
    "RialJayezeh" DOUBLE PRECISION,
    "ccKalaCodeJayezeh" INTEGER,
    "NoeRialJayezeh" INTEGER,
    "MohasebehAzMazad" TEXT,
    "Darsad" INTEGER,
    "ccJayezehTaminkonandehSatrInsert" INTEGER
);

CREATE TABLE IF NOT EXISTS public."JayezehTaminkonandehSatrKala" (
    "ccJayezehTaminkonandehSatr" INTEGER,
    "ccJayezehTaminkonandehSatrKala" INTEGER,
    "DarsadJayezeh" INTEGER,
    "TedadJayezeh" INTEGER,
    "ccKalaCodeJayezeh" INTEGER,
    "NoeRialJayezeh" INTEGER,
    "RialJayezeh" DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS public."KalaAdamForoshForoshandeh" (
    "ShomarehBakhshnameh" VARCHAR(50),
    "TarikhBakhshNameh" TIMESTAMP,
    "ccKalaCode" INTEGER,
    "ccForoshandeh" INTEGER,
    "ccKalaAdamForoshForoshandeh" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(50), PRIMARY KEY ("ccKalaAdamForoshForoshandeh")
);

CREATE TABLE IF NOT EXISTS public."KalaAdamForoshInMarkazPakhsh" (
    "ccKalaCode" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccKalaAdamForoshInmarkazPakhsh" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "ccElat" INTEGER, PRIMARY KEY ("ccKalaAdamForoshInmarkazPakhsh")
);

CREATE TABLE IF NOT EXISTS public."KalaAdamForoshMarkazPakhsh" (
    "ccKalaCode" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccKalaAdamForoshMarkazPakhsh" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "ccElat" INTEGER,
    "ccGoroh" INTEGER,
    "ccMoshtary" INTEGER,
    "Sharh" VARCHAR(-1), PRIMARY KEY ("ccKalaAdamForoshMarkazPakhsh")
);

CREATE TABLE IF NOT EXISTS public."KalaAdamForoshMarkazPakhshOstan" (
    "ccKalaAdamForoshMarkazPakhsh" INTEGER,
    "ccKalaAdamForoshMarkazPakhshOstan" INTEGER,
    "ccOstan" INTEGER,
    "ccShahr" INTEGER, PRIMARY KEY ("ccKalaAdamForoshMarkazPakhshOstan")
);

CREATE TABLE IF NOT EXISTS public."KalaAdamForoshShahr" (
    "ccKalaCode" INTEGER,
    "ccShahr" INTEGER,
    "ccKalaAdamForoshShahr" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(50), PRIMARY KEY ("ccKalaAdamForoshShahr")
);

CREATE TABLE IF NOT EXISTS public."KalaGheymatForosh" (
    "ccKalaCode" INTEGER,
    "ccKalaGheymatForosh" INTEGER,
    "MablaghForosh" DOUBLE PRECISION,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(50), PRIMARY KEY ("ccKalaGheymatForosh")
);

CREATE TABLE IF NOT EXISTS public."KalaGheymatForoshNew" (
    "ccKalaCode" INTEGER,
    "ccKalaGheymatForoshNew" INTEGER,
    "MablaghForshNew" DOUBLE PRECISION,
    "ccMoshtary" INTEGER,
    "ccGoroh" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(50),
    "ccKalaGheymatLink" INTEGER,
    "ccMarkazPakhsh" INTEGER, PRIMARY KEY ("ccKalaGheymatForoshNew")
);

CREATE TABLE IF NOT EXISTS public."KalaModatVosolCheck" (
    "ccMarkazPakhsh" INTEGER,
    "ccKalaModatVosolCheck" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "ccKala" INTEGER,
    "ccKalaCode" INTEGER,
    "ModatVosoul" INTEGER,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(255),
    "ccGoroh" INTEGER,
    "ModatVosoulEtebarat" INTEGER,
    "Az" INTEGER,
    "Ta" INTEGER,
    "CodeNo" INTEGER,
    "CodeHamsan" INTEGER,
    "ModatBazPardakht" INTEGER,
    "ShomarehBach" VARCHAR(50), PRIMARY KEY ("ccKalaModatVosolCheck")
);

CREATE TABLE IF NOT EXISTS public."KalaModatVosolCheck13970802" (
    "ccMarkazPakhsh" INTEGER,
    "ccKalaModatVosolCheck" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "ccKala" INTEGER,
    "ccKalaCode" INTEGER,
    "ModatVosoul" INTEGER,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(255),
    "ccGoroh" INTEGER,
    "ModatVosoulEtebarat" INTEGER,
    "Az" INTEGER,
    "Ta" INTEGER,
    "CodeNo" INTEGER,
    "CodeHamsan" INTEGER,
    "ModatBazPardakht" INTEGER
);

CREATE TABLE IF NOT EXISTS public."KalaModatVosolCheckbk" (
    "ccMarkazPakhsh" INTEGER,
    "ccKalaModatVosolCheck" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "ccKala" INTEGER,
    "ccKalaCode" INTEGER,
    "ModatVosoul" INTEGER,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(255),
    "ccGoroh" INTEGER,
    "ModatVosoulEtebarat" INTEGER,
    "Az" INTEGER,
    "Ta" INTEGER,
    "CodeNo" INTEGER,
    "CodeHamsan" INTEGER,
    "ModatBazPardakht" INTEGER
);

CREATE TABLE IF NOT EXISTS public."KalaModatVosolCheckEnghezaNazdik" (
    "ccMarkazPakhsh" INTEGER,
    "ccKalaModatVosolCheckEnghezaNazdik" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "ccKala" INTEGER,
    "ccKalaCode" INTEGER,
    "ModatVosoul" INTEGER,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(255),
    "ccGoroh" INTEGER,
    "ModatVosoulEtebarat" INTEGER,
    "Az" INTEGER,
    "Ta" INTEGER,
    "CodeNo" INTEGER,
    "CodeHamsan" INTEGER,
    "ISUpdate" TEXT,
    "ModatBazPardakht" DOUBLE PRECISION, PRIMARY KEY ("ccKalaModatVosolCheckEnghezaNazdik")
);

CREATE TABLE IF NOT EXISTS public."KalaModatVosolPhoto" (
    "ccKalaModatVosolCheck" INTEGER,
    "ccPhoto" INTEGER,
    "ccNoePhoto" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ccUser" INTEGER, PRIMARY KEY ("ccKalaModatVosolCheck", "ccPhoto")
);

CREATE TABLE IF NOT EXISTS public."KalaMojodyForoshandeh" (
    "ccForoshandeh" INTEGER,
    "ccKala" INTEGER,
    "ccKalaCode" INTEGER,
    "TedadMojody" DOUBLE PRECISION, PRIMARY KEY ("ccForoshandeh", "ccKala", "ccKalaCode")
);

CREATE TABLE IF NOT EXISTS public."KalaMojodyGhabelForosh" (
    "ccMarkazPakhsh" INTEGER,
    "ccKala" INTEGER,
    "MojodyGhabelForosh" DOUBLE PRECISION,
    "MojodyGhabelForoshDarkhast" DOUBLE PRECISION, PRIMARY KEY ("ccMarkazPakhsh", "ccKala")
);

CREATE TABLE IF NOT EXISTS public."KalaZaribForosh" (
    "ccKalaCode" INTEGER,
    "ccKalaZaribForosh" INTEGER,
    "ZaribForosh" INTEGER,
    "CodeNoeBastehBandy" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "ccGoroh" INTEGER,
    "Elat" VARCHAR(255),
    "NoeVorod" INTEGER, PRIMARY KEY ("ccKalaZaribForosh")
);

CREATE TABLE IF NOT EXISTS public."KardexUUID" (
    "ccKardexUUID" INTEGER,
    "ccKardex" INTEGER,
    "Time" TIMESTAMP,
    "UUID" VARCHAR(36),
    "CodeNoeAction" INTEGER,
    "Status" TEXT,
    "Comment" VARCHAR(-1),
    "CodeNoeForm" INTEGER,
    "ccKardexSatrUUID" INTEGER,
    "Status_concurrency" INTEGER,
    "ModifyDate" TIMESTAMP, PRIMARY KEY ("ccKardexUUID")
);

CREATE TABLE IF NOT EXISTS public."KardexUUIDLog" (
    "ccKardexUUIDLog" INTEGER,
    "ccKardexUUID" INTEGER,
    "ccKardex" INTEGER,
    "Time" TIMESTAMP,
    "UUID" VARCHAR(36),
    "CodeNoeAction" INTEGER,
    "Status" INTEGER,
    "Comment" VARCHAR(-1), PRIMARY KEY ("ccKardexUUIDLog")
);

CREATE TABLE IF NOT EXISTS public."MamorPakhsh" (
    "ccMarkazPakhsh" INTEGER,
    "ccMamorPakhsh" INTEGER,
    "MaxTedadCheckBargashty" INTEGER,
    "MaxMablaghCheckBargashty" DOUBLE PRECISION,
    "MaxModatCheckBargashty" INTEGER,
    "MaxTedadFaktorBaz" INTEGER,
    "MaxMablaghFaktorBaz" DOUBLE PRECISION,
    "CodeVazeiat" INTEGER,
    "CodeMamorPakhshOld" VARCHAR(10),
    "SharhMamorPakhsh" VARCHAR(50),
    "ccAfrad" INTEGER,
    "MobileNumber" VARCHAR(50), PRIMARY KEY ("ccMamorPakhsh")
);

CREATE TABLE IF NOT EXISTS public."MarjoeeAmany" (
    "ccDarkhastFaktor" INTEGER,
    "ccTafkikJoze" INTEGER,
    "Tarikh" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "ccMarjoeeAmany" INTEGER, PRIMARY KEY ("ccMarjoeeAmany")
);

CREATE TABLE IF NOT EXISTS public."Mashin" (
    "ccMarkazPakhsh" INTEGER,
    "ccMashin" INTEGER,
    "ccNoeMashin" INTEGER,
    "CodeNoeMalekiat" INTEGER,
    "ShomarehMashin" VARCHAR(10),
    "ccAfradRanadeh" INTEGER,
    "ArmTarhTerafik" TEXT,
    "DeviceIMEI" VARCHAR(50), PRIMARY KEY ("ccMashin")
);

CREATE TABLE IF NOT EXISTS public."Masir" (
    "ccForoshandeh" INTEGER,
    "ccMasir" INTEGER,
    "NameMasir" VARCHAR(20),
    "ToolDoreh" INTEGER,
    "ToorVisit" INTEGER,
    "TarikhShoro" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "CodeMasirOld" VARCHAR(100),
    "RoozMojaz" INTEGER,
    "Depo" INTEGER,
    "CodeNoeUpdate" INTEGER,
    "CodeNoeVorod" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "Bound" VARCHAR(-1),
    "ccMantaghe" INTEGER,
    "MasirBound" VARCHAR(-1),
    "NoeMasir" INTEGER, PRIMARY KEY ("ccMasir")
);

CREATE TABLE IF NOT EXISTS public."MasirHamsan" (
    "ccMarkazPakhsh" INTEGER,
    "ccMasirHamsan" INTEGER,
    "CodeMasirHamsan" VARCHAR(10),
    "ccMahaleh" INTEGER,
    "OlaviatHamsan" INTEGER,
    "CodeNoeMasir" INTEGER,
    "FaselehTaMasir" DOUBLE PRECISION,
    "ZamanTaradod" DOUBLE PRECISION, PRIMARY KEY ("ccMasirHamsan")
);

CREATE TABLE IF NOT EXISTS public."MasirHamsanSatr" (
    "ccMasirHamsan" INTEGER,
    "ccMahaleh" INTEGER,
    "ccMasirHamsanSatr" INTEGER,
    "Olaviat" INTEGER, PRIMARY KEY ("ccMasirHamsanSatr")
);

CREATE TABLE IF NOT EXISTS public."MasirRooz" (
    "ccMasirRooz" INTEGER,
    "ccMasir" INTEGER,
    "Rooz" INTEGER,
    "ModatVisit" TEXT,
    "TarikhShoro" TIMESTAMP, PRIMARY KEY ("ccMasirRooz")
);

CREATE TABLE IF NOT EXISTS public."MasirSatr" (
    "ccMasirSatr" INTEGER,
    "ccMasir" INTEGER,
    "ccMahaleh" INTEGER, PRIMARY KEY ("ccMasirSatr")
);

CREATE TABLE IF NOT EXISTS public."MasirTarikh" (
    "ccMasirTarikh" INTEGER,
    "ccMasir" INTEGER,
    "Tarikh" TIMESTAMP, PRIMARY KEY ("ccMasirTarikh")
);

CREATE TABLE IF NOT EXISTS public."Moavagh" (
    "ccMoavagh" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "ccMarkazPakhsh" INTEGER,
    "ccDarkhastFaktor" INTEGER,
    "ccDariaftPardakht" INTEGER,
    "ccMoshtary" INTEGER,
    "ccForoshandeh" INTEGER, PRIMARY KEY ("ccMoavagh")
);

CREATE TABLE IF NOT EXISTS public."ModatVosolGorohMoshtarian" (
    "ccModatVosolGorohMoshtarian" INTEGER,
    "ccGoroh" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "ModateVosol" INTEGER,
    "CodeVazeiat" INTEGER,
    "NameAeenName" VARCHAR(300),
    "ElatOdat" VARCHAR(100), PRIMARY KEY ("ccModatVosolGorohMoshtarian")
);

CREATE TABLE IF NOT EXISTS public."Moshtary" (
    "ccMoshtary" INTEGER,
    "ccMoshtaryJadid" INTEGER,
    "MoshtaryAsli" TEXT,
    "ccMoshtary_Link" INTEGER,
    "TarikhMoarefiMoshtary" TIMESTAMP,
    "NameMoshtary" VARCHAR(60),
    "NameTablo" VARCHAR(60),
    "CodePosty" VARCHAR(20),
    "CodeEghtesady" VARCHAR(23),
    "CodeNoeVosolAzMoshtary" INTEGER,
    "ModateVosol" INTEGER,
    "CodeNoeShakhsiat" INTEGER,
    "ccMahaleh" INTEGER,
    "ccNoeMalekiatMoshtary" INTEGER,
    "ModateParvanehKasb" INTEGER,
    "ModateHozor" INTEGER,
    "Telephone" VARCHAR(50),
    "Fax" VARCHAR(50),
    "Kart" TEXT,
    "Javaz" TEXT,
    "NoeJavaz" VARCHAR(15),
    "ShomarehJavaz" VARCHAR(15),
    "TarikhEnghezaJavaz" TIMESTAMP,
    "Darajeh" VARCHAR(1),
    "Namaiandeh" TEXT,
    "NoeMashin" VARCHAR(50),
    "Sanad" TEXT,
    "GhafasehBandy" TEXT,
    "TedadYakhchal" INTEGER,
    "TedadFraizer" INTEGER,
    "TedadSandogh" INTEGER,
    "HosneShohrat" TEXT,
    "ForoshTaghribiRoozaneh" DOUBLE PRECISION,
    "MojoudiTaghriby" DOUBLE PRECISION,
    "EtebarPishnahady" DOUBLE PRECISION,
    "EtebarKol" DOUBLE PRECISION,
    "Tozihat" VARCHAR(200),
    "CodeVazeiat" INTEGER,
    "ccElatAdamFaalMoshtary" INTEGER,
    "ccUser" INTEGER,
    "CodeMoshtaryOld" INTEGER,
    "TarikhEjareh" TIMESTAMP,
    "KharidPishnahady" DOUBLE PRECISION,
    "CodeNahvehTahiehKala" INTEGER,
    "EtebarPishnahadySystem" DOUBLE PRECISION,
    "CodeMoshtaryOldDos" VARCHAR(15),
    "FlagCodeVazeiat" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "ElatOdat" VARCHAR(500),
    "Etebar" TEXT,
    "X" DOUBLE PRECISION,
    "Y" DOUBLE PRECISION,
    "TarikhUpDatePosition_Tablet" TIMESTAMP,
    "TarikhUpDatePosition_Map" TIMESTAMP,
    "ShenasehMeli" VARCHAR(20),
    "ccMantaghe" INTEGER,
    "Rank" VARCHAR(10),
    "NoeMoshtary" INTEGER,
    "CheckBargashty" INTEGER,
    "CustomerLocationGuid" TEXT, PRIMARY KEY ("ccMoshtary")
);

CREATE TABLE IF NOT EXISTS public."MoshtaryAddress" (
    "ccMoshtaryAddress" INTEGER,
    "ccMoshtary" INTEGER,
    "ccAddress" INTEGER,
    "ccNoeAddress" INTEGER,
    "ccMahaleh" INTEGER,
    "CodeNoeMasir" INTEGER,
    "CodeVazeiat" INTEGER,
    "CodeMoshtaryOld" VARCHAR(10),
    "ccUser" INTEGER,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccMoshtaryAddress")
);

CREATE TABLE IF NOT EXISTS public."MoshtaryAddressSaatTahvil" (
    "ccMoshtaryAddressSaatTahvil" INTEGER,
    "ccMoshtaryAddress" INTEGER,
    "SaatTahvilAz" TIMESTAMP,
    "SaatTahvilTa" TIMESTAMP, PRIMARY KEY ("ccMoshtaryAddressSaatTahvil")
);

CREATE TABLE IF NOT EXISTS public."MoshtaryAfrad" (
    "ccMoshtary" INTEGER,
    "ccAfrad" INTEGER,
    "Semat" VARCHAR(50),
    "MojazEmza" TEXT,
    "CodeMoshtaryOld" VARCHAR(10),
    "TarafHesab" TEXT, PRIMARY KEY ("ccMoshtary", "ccAfrad")
);

CREATE TABLE IF NOT EXISTS public."MoshtaryBK" (
    "ccMoshtary" INTEGER,
    "ccMoshtaryJadid" INTEGER,
    "MoshtaryAsli" TEXT,
    "ccMoshtary_Link" INTEGER,
    "TarikhMoarefiMoshtary" TIMESTAMP,
    "NameMoshtary" VARCHAR(50),
    "NameTablo" VARCHAR(50),
    "CodePosty" VARCHAR(20),
    "CodeEghtesady" VARCHAR(15),
    "CodeNoeVosolAzMoshtary" INTEGER,
    "ModateVosol" INTEGER,
    "CodeNoeShakhsiat" INTEGER,
    "ccMahaleh" INTEGER,
    "ccNoeMalekiatMoshtary" INTEGER,
    "ModateParvanehKasb" INTEGER,
    "ModateHozor" INTEGER,
    "Telephone" VARCHAR(50),
    "Fax" VARCHAR(50),
    "Kart" TEXT,
    "Javaz" TEXT,
    "NoeJavaz" VARCHAR(15),
    "ShomarehJavaz" VARCHAR(15),
    "TarikhEnghezaJavaz" TIMESTAMP,
    "Darajeh" VARCHAR(1),
    "Namaiandeh" TEXT,
    "NoeMashin" VARCHAR(50),
    "Sanad" TEXT,
    "GhafasehBandy" TEXT,
    "TedadYakhchal" INTEGER,
    "TedadFraizer" INTEGER,
    "TedadSandogh" INTEGER,
    "HosneShohrat" TEXT,
    "ForoshTaghribiRoozaneh" DOUBLE PRECISION,
    "MojoudiTaghriby" DOUBLE PRECISION,
    "EtebarPishnahady" DOUBLE PRECISION,
    "EtebarKol" DOUBLE PRECISION,
    "Tozihat" VARCHAR(200),
    "CodeVazeiat" INTEGER,
    "ccElatAdamFaalMoshtary" INTEGER,
    "ccUser" INTEGER,
    "CodeMoshtaryOld" INTEGER,
    "TarikhEjareh" TIMESTAMP,
    "KharidPishnahady" DOUBLE PRECISION,
    "CodeNahvehTahiehKala" INTEGER,
    "EtebarPishnahadySystem" DOUBLE PRECISION,
    "CodeMoshtaryOldDos" VARCHAR(15),
    "FlagCodeVazeiat" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "ElatOdat" VARCHAR(500),
    "Etebar" TEXT,
    "X" DOUBLE PRECISION,
    "Y" DOUBLE PRECISION,
    "TarikhUpDatePosition_Tablet" TIMESTAMP,
    "TarikhUpDatePosition_Map" TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public."MoshtaryEtebar" (
    "ccEtebar" INTEGER,
    "ccMoshtary" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "EtebarJary" DOUBLE PRECISION,
    "Etebar_Min" DOUBLE PRECISION,
    "Etebar_Max" DOUBLE PRECISION,
    "EtebarTedady" DOUBLE PRECISION,
    "CodeNoeLevelEtebar" INTEGER,
    "MablaghEtebarDarkhasty" DOUBLE PRECISION,
    "EtebarTedadyDarkhasty" DOUBLE PRECISION,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(100),
    "RoozMotalebat" INTEGER,
    "SaghfFaktor" DOUBLE PRECISION,
    "SaghfRoozSayadi" DOUBLE PRECISION,
    "CheckMoavaghFaktor" TEXT,
    "CheckCheckBargashti" TEXT,
    "TedadCheckBargashti" DOUBLE PRECISION,
    "MablaghCheckBargashti" DOUBLE PRECISION,
    "MablaghMoavaghMoshtary" DOUBLE PRECISION,
    "ccPhoto" INTEGER, PRIMARY KEY ("ccEtebar")
);

CREATE TABLE IF NOT EXISTS public."MoshtaryEtebarPhoto" (
    "ccEtebar" INTEGER,
    "ccPhoto" INTEGER,
    "ccUser" INTEGER, PRIMARY KEY ("ccEtebar", "ccPhoto")
);

CREATE TABLE IF NOT EXISTS public."MoshtaryEtebarVazeiat" (
    "ccEtebarVazeiat" INTEGER,
    "ccEtebar" INTEGER,
    "NoeAmaliat" INTEGER,
    "CodeNoeLevelEtebar" INTEGER,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(100),
    "ccUser" INTEGER,
    "TarikhEntry" TIMESTAMP, PRIMARY KEY ("ccEtebarVazeiat")
);

CREATE TABLE IF NOT EXISTS public."MoshtaryEtelaatMoadian" (
    "ccMoshtaryMoadian" INTEGER,
    "CodeShobeh" VARCHAR(50),
    "ShomarehEghtesadi" VARCHAR(50),
    "ccMoshtary" INTEGER,
    "NoeErsal" INTEGER, PRIMARY KEY ("ccMoshtaryMoadian")
);

CREATE TABLE IF NOT EXISTS public."MoshtaryGoroh" (
    "ccMoshtaryGoroh" INTEGER,
    "ccMoshtary" INTEGER,
    "ccGoroh" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccMoshtary", "ccGoroh")
);

CREATE TABLE IF NOT EXISTS public."MoshtaryJadid" (
    "ccMoshtaryJadid" INTEGER,
    "ccMoshtaryJadidPPC" VARCHAR(20),
    "NameMoshtary" VARCHAR(200),
    "NameTablo" VARCHAR(50),
    "EtebarPishnahady" DOUBLE PRECISION,
    "AddressAvaliehMoshtary" VARCHAR(256),
    "Telephone" VARCHAR(50),
    "ccNoeMalekiatMoshtary" INTEGER,
    "ModateParvanehKasb" INTEGER,
    "ModateHozor" INTEGER,
    "ccAfrad" INTEGER,
    "ccForoshandeh" INTEGER,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(50),
    "CodeNoeVorod" INTEGER,
    "DateVorod" TIMESTAMP,
    "ccGoroh" INTEGER,
    "ccMahaleh" INTEGER,
    "Mobile" VARCHAR(20),
    "Tozihat" VARCHAR(254),
    "ccNoeMoshtary" INTEGER,
    "ccMasir" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "X" DOUBLE PRECISION,
    "Y" DOUBLE PRECISION,
    "CodeMeli" VARCHAR(20),
    "ShenasehMeli" VARCHAR(20),
    "ShomarehHesab" VARCHAR(50),
    "CodeEghtesady" VARCHAR(20),
    "CodePosty" VARCHAR(50),
    "ShomarehSabt" VARCHAR(50),
    "Type" TEXT,
    "Gln" VARCHAR(50),
    "NewCustomerGuid" TEXT,
    "ImageName" VARCHAR(250),
    "IsReal" TEXT,
    "DateLocal" TIMESTAMP,
    "ccSenf" INTEGER, PRIMARY KEY ("ccMoshtaryJadid")
);

CREATE TABLE IF NOT EXISTS public."MoshtaryJadidDarkhast" (
    "ccMarkazPakhsh" INTEGER,
    "ccMoshtaryJadidDarkhast" INTEGER,
    "TarikhDarkhast" TIMESTAMP,
    "ccForoshandeh" INTEGER,
    "ccAfrad" INTEGER,
    "ccMoshtaryJadid" INTEGER,
    "ccKala" INTEGER,
    "Tedad" DOUBLE PRECISION,
    "MablaghForosh" DOUBLE PRECISION,
    "CodeNoeVorod" INTEGER,
    "DateVorod" TIMESTAMP,
    "CodeVazeiat" INTEGER, PRIMARY KEY ("ccMoshtaryJadidDarkhast")
);

CREATE TABLE IF NOT EXISTS public."MoshtaryPhoto" (
    "ccMoshtary" INTEGER,
    "ccPhoto" INTEGER,
    "ccNoePhoto" INTEGER, PRIMARY KEY ("ccMoshtary", "ccPhoto")
);

CREATE TABLE IF NOT EXISTS public."MoshtaryShomarehHesab" (
    "ccMoshtary" INTEGER,
    "ccShomarehHesab" INTEGER,
    "CodeMoshtaryOld" VARCHAR(10),
    "ccBank" INTEGER,
    "NameShobeh" VARCHAR(50),
    "CodeShobeh" VARCHAR(10),
    "ccShahr" INTEGER,
    "CodeNoeCheck" INTEGER,
    "Faal" TEXT, PRIMARY KEY ("ccMoshtary", "ccShomarehHesab")
);

CREATE TABLE IF NOT EXISTS public."NoeMalekiatMoshtary" (
    "ccNoeMalekiatMoshtary" INTEGER,
    "NameNoeMalekiatMoshtary" VARCHAR(50), PRIMARY KEY ("ccNoeMalekiatMoshtary")
);

CREATE TABLE IF NOT EXISTS public."NoeMashin" (
    "ccNoeMashin" INTEGER,
    "NameNoeMashin" VARCHAR(20),
    "Tol" DOUBLE PRECISION,
    "Arz" DOUBLE PRECISION,
    "Ertefa" DOUBLE PRECISION,
    "ccVahedSize" INTEGER,
    "Vazn" DOUBLE PRECISION,
    "ccVahedVazn" INTEGER, PRIMARY KEY ("ccNoeMashin")
);

CREATE TABLE IF NOT EXISTS public."NoeMoshtaryRialKharid" (
    "ccNoeMoshtaryRialKharid" INTEGER,
    "ccGoroh" INTEGER,
    "HadeAghalMablaghKharid" DOUBLE PRECISION, PRIMARY KEY ("ccNoeMoshtaryRialKharid")
);

CREATE TABLE IF NOT EXISTS public."NoeVosolAzMoshtary" (
    "ccNoeVosolAzMoshtary" INTEGER,
    "NameNoeVosolAzMoshtary" VARCHAR(50),
    "OlaviatNoeVosolAzMoshtary" INTEGER,
    "NamaieshModatVosol" TEXT, PRIMARY KEY ("ccNoeVosolAzMoshtary")
);

CREATE TABLE IF NOT EXISTS public."Point" (
    "ccpoint" INTEGER,
    "ccMoshtary" INTEGER,
    "X" DOUBLE PRECISION,
    "Y" DOUBLE PRECISION,
    "DateTime" TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public."SabadGorohKala" (
    "ccSabadGorohKala" INTEGER,
    "NameSabadGorohKala" VARCHAR(50),
    "Faal" TEXT, PRIMARY KEY ("ccSabadGorohKala")
);

CREATE TABLE IF NOT EXISTS public."SabadGorohKalaSatr" (
    "ccSabadGorohKalaSatr" INTEGER,
    "ccSabadGorohKala" INTEGER,
    "ccGorohKala" INTEGER,
    "Tedad" DOUBLE PRECISION,
    "HadeAghlKharidDarFaktor" DOUBLE PRECISION, PRIMARY KEY ("ccSabadGorohKalaSatr")
);

CREATE TABLE IF NOT EXISTS public."SabadKala" (
    "ccSabadKala" INTEGER,
    "NameSabadKala" VARCHAR(50),
    "Faal" TEXT, PRIMARY KEY ("ccSabadKala")
);

CREATE TABLE IF NOT EXISTS public."SabadKalaSatr" (
    "ccSabadKalaSatr" INTEGER,
    "ccSabadKala" INTEGER,
    "ccKala" INTEGER,
    "Tedad" DOUBLE PRECISION,
    "HadeAghlKharidDarFaktor" DOUBLE PRECISION, PRIMARY KEY ("ccSabadKalaSatr")
);

CREATE TABLE IF NOT EXISTS public."SahmiehBandyMoshtary" (
    "ccSahmiehBandyMoshtary" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "ccMoshtary" INTEGER,
    "ccGoroh" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "Tozihat" VARCHAR(200), PRIMARY KEY ("ccSahmiehBandyMoshtary")
);

CREATE TABLE IF NOT EXISTS public."SahmiehBandyMoshtaryOstan" (
    "ccSahmiehBandyMoshtary" INTEGER,
    "ccSahmiehBandyMoshtaryOstan" INTEGER,
    "ccOstan" INTEGER,
    "ccShahr" INTEGER, PRIMARY KEY ("ccSahmiehBandyMoshtaryOstan")
);

CREATE TABLE IF NOT EXISTS public."SahmiehBandyMoshtarySatr" (
    "ccSahmiehBandyMoshtary" INTEGER,
    "ccSahmiehBandyMoshtarySatr" INTEGER,
    "ccKalaCode" INTEGER,
    "TedadSahmieh" INTEGER,
    "ModifiedDate" TIMESTAMP,
    "TedadGhabli" INTEGER,
    "Tozihat" VARCHAR(100), PRIMARY KEY ("ccSahmiehBandyMoshtarySatr")
);

CREATE TABLE IF NOT EXISTS public."SazmaneGhazaDarooGLN" (
    "ccSazmaneGhazaDarooGLN" INTEGER,
    "CodeNoeRefrence" INTEGER,
    "ccRefrence" INTEGER,
    "GLN" VARCHAR(50),
    "HIX" VARCHAR(50), PRIMARY KEY ("ccSazmaneGhazaDarooGLN")
);

CREATE TABLE IF NOT EXISTS public."SghfeEstemhal" (
    "ccSghfeEstemhal" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "Mablagh" DOUBLE PRECISION,
    "MianginRoozaneh" DOUBLE PRECISION,
    "ccGoroh" INTEGER,
    "NoeAeenNameh" INTEGER,
    "Rooz" INTEGER,
    "SaghfRooz" INTEGER,
    "ccMoshtary" INTEGER,
    "ccUser" INTEGER, PRIMARY KEY ("ccSghfeEstemhal")
);

CREATE TABLE IF NOT EXISTS public."SharhFaktor" (
    "ccSharhFaktor" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccGoroh" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "Sharh" VARCHAR(500),
    "Tozihat" VARCHAR(100), PRIMARY KEY ("ccSharhFaktor")
);

CREATE TABLE IF NOT EXISTS public."Sms" (
    "ID" INTEGER,
    "SmsDate" VARCHAR(50),
    "MobileNum" VARCHAR(50),
    "SmsText" VARCHAR(500),
    "Status" INTEGER, PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public."TafkikJoze" (
    "ccMarkazPakhsh" INTEGER,
    "ccTafkikJoze" INTEGER,
    "ShomarehTafkikJoze" INTEGER,
    "TarikhTafkikJoze" TIMESTAMP,
    "TarikhPishBiniErsal" TIMESTAMP,
    "TarikhErsal" TIMESTAMP,
    "ccNoeMashin" INTEGER,
    "ccMashin" INTEGER,
    "ccAfradRanandeh" INTEGER,
    "SaatKhorooj" TIMESTAMP,
    "SaatVorood" TIMESTAMP,
    "ccAfradMamorPakhsh" INTEGER,
    "MasirTedad" INTEGER,
    "CodeVazeiat" INTEGER,
    "ccUser" INTEGER,
    "TarikhBargasht" TIMESTAMP,
    "SaatBargasht" TIMESTAMP,
    "Sharh" VARCHAR(200), PRIMARY KEY ("ccTafkikJoze")
);

CREATE TABLE IF NOT EXISTS public."TafkikJozeSatr" (
    "ccTafkikJoze" INTEGER,
    "ccTafkikJozeSatr" INTEGER,
    "ccDarkhastFaktor" INTEGER, PRIMARY KEY ("ccTafkikJozeSatr")
);

CREATE TABLE IF NOT EXISTS public."TafkikJozeTasfieh" (
    "ccMarkazPakhsh" INTEGER,
    "ccTafkikJoze" INTEGER,
    "TarikhTasvieh" TIMESTAMP,
    "TedadKalaTafkik" DOUBLE PRECISION,
    "MablaghKolTafkik" DOUBLE PRECISION,
    "MablaghNaghd" INTEGER,
    "MablaghChek" INTEGER,
    "MablaghKartKhan" INTEGER,
    "MablaghTakhfif" INTEGER,
    "MablaghMarjoee" INTEGER,
    "MablaghResid" INTEGER,
    "CodeVazeiat" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccTafkikJoze")
);

CREATE TABLE IF NOT EXISTS public."TafkikJozeTasfiehSatr" (
    "ccTafkikJoze" INTEGER,
    "ccDarkhastFaktor" INTEGER,
    "MablaghKolTafkik" DOUBLE PRECISION,
    "MablaghNaghd" INTEGER,
    "MablaghChek" INTEGER,
    "MablaghKartKhan" INTEGER,
    "MablaghTakhfif" INTEGER,
    "MablaghMarjoee" INTEGER,
    "MablaghResid" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccTafkikJoze", "ccDarkhastFaktor")
);

CREATE TABLE IF NOT EXISTS public."TafkikKol" (
    "ccMarkazPakhsh" INTEGER,
    "ccTafkikKol" INTEGER,
    "ShomarehTafkikKol" INTEGER,
    "TarikhTafkikKol" TIMESTAMP, PRIMARY KEY ("ccTafkikKol")
);

CREATE TABLE IF NOT EXISTS public."TafkikKolSatr" (
    "ccTafkikKol" INTEGER,
    "ccTafkikJoze" INTEGER, PRIMARY KEY ("ccTafkikKol", "ccTafkikJoze")
);

CREATE TABLE IF NOT EXISTS public."TakhfifHajmi" (
    "ccTakhfifHajmi" INTEGER,
    "CodeNoe" INTEGER,
    "SharhTakhfif" VARCHAR(50),
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "NoeTedadRial" INTEGER,
    "NameNoeFieldMoshtary" INTEGER,
    "ccNoeFieldMoshtary" INTEGER,
    "NoeVosol" INTEGER,
    "CodeNoeVorod" INTEGER,
    "OnBach" INTEGER,
    "CodeVazeiat" INTEGER, PRIMARY KEY ("ccTakhfifHajmi")
);

CREATE TABLE IF NOT EXISTS public."TakhfifHajmiSatr" (
    "ccTakhfifHajmi" INTEGER,
    "ccTakhfifHajmiSatr" INTEGER,
    "NameNoeField" INTEGER,
    "ccNoeField" INTEGER,
    "Az" DOUBLE PRECISION,
    "Ta" DOUBLE PRECISION,
    "CodeNoeBastehBandy" INTEGER,
    "BeEza" DOUBLE PRECISION,
    "CodeNoeBastehBandyBeEza" INTEGER,
    "DarsadTakhfif" DOUBLE PRECISION,
    "RialTakhfif" DOUBLE PRECISION,
    "ShomarehBach" VARCHAR(50), PRIMARY KEY ("ccTakhfifHajmiSatr")
);

CREATE TABLE IF NOT EXISTS public."TakhfifHamlMostaghim" (
    "ccTakhfifHamlMostaghim" INTEGER,
    "CodeNoe" INTEGER,
    "SharhTakhfif" VARCHAR(50),
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "ccTaminKonandeh" INTEGER,
    "ccNoeMashin" INTEGER,
    "MablaghMashin" DOUBLE PRECISION,
    "HajmMashin" DOUBLE PRECISION,
    "VaznMashin" DOUBLE PRECISION,
    "DarsadTakhfif" DOUBLE PRECISION, PRIMARY KEY ("ccTakhfifHamlMostaghim")
);

CREATE TABLE IF NOT EXISTS public."TakhfifHamlMostaghimSatr" (
    "ccTakhfifHamlMostaghim" INTEGER,
    "ccTakhfifHamlMostaghimSatr" INTEGER,
    "ccKalaCode" INTEGER, PRIMARY KEY ("ccTakhfifHamlMostaghimSatr")
);

CREATE TABLE IF NOT EXISTS public."TakhfifJayezeh" (
    "ccTakhfifJayezeh" INTEGER,
    "CodeNoe" INTEGER,
    "NoeForm" INTEGER,
    "SharhTakhfifJayezeh" VARCHAR(50),
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "NoeTedadRial" INTEGER,
    "ccNoeMashin" INTEGER,
    "MablaghMashin" DOUBLE PRECISION,
    "NameNoeFieldMoshtary" INTEGER,
    "ccNoeFieldMoshtary" INTEGER,
    "Olaviat" INTEGER, PRIMARY KEY ("ccTakhfifJayezeh")
);

CREATE TABLE IF NOT EXISTS public."TakhfifJayezehAdam" (
    "ccTakhfifJayezeh" INTEGER,
    "ccTakhfifJayezehAdam" INTEGER,
    "CodeNoeTakhfif" INTEGER,
    "CodeNoeTakhfifAdam" INTEGER, PRIMARY KEY ("ccTakhfifJayezeh", "CodeNoeTakhfif", "ccTakhfifJayezehAdam", "CodeNoeTakhfifAdam")
);

CREATE TABLE IF NOT EXISTS public."TakhfifJayezehMarkazPakhsh" (
    "ccMarkazPakhsh" INTEGER,
    "ccTakhfifJayezeh" INTEGER,
    "CodeNoeTakhfif" INTEGER, PRIMARY KEY ("ccMarkazPakhsh", "ccTakhfifJayezeh", "CodeNoeTakhfif")
);

CREATE TABLE IF NOT EXISTS public."TakhfifJayezehPhoto" (
    "ccTakhfifJayezeh" INTEGER,
    "CodeNoeTakhfif" INTEGER,
    "ccPhoto" INTEGER,
    "ccNoePhoto" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ccUser" INTEGER, PRIMARY KEY ("ccTakhfifJayezeh", "CodeNoeTakhfif", "ccPhoto")
);

CREATE TABLE IF NOT EXISTS public."TakhfifJayezehSatr" (
    "ccTakhfifJayezeh" INTEGER,
    "ccTakhfifJayezehSatr" INTEGER,
    "NameNoeField" INTEGER,
    "ccNoeField" INTEGER,
    "Az" DOUBLE PRECISION,
    "Ta" DOUBLE PRECISION,
    "BeEza" DOUBLE PRECISION,
    "TedadJayezeh" INTEGER,
    "ccKalaCodeJayezeh" INTEGER,
    "DarsadTakhfif" DOUBLE PRECISION,
    "CodeNoeBastehBandy" INTEGER,
    "CodeNoeBastehBandyBeEza" INTEGER,
    "RialJayezeh" DOUBLE PRECISION, PRIMARY KEY ("ccTakhfifJayezehSatr")
);

CREATE TABLE IF NOT EXISTS public."TakhfifNaghdy" (
    "ccTakhfifNaghdy" INTEGER,
    "CodeNoe" INTEGER,
    "SharhTakhfif" VARCHAR(50),
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "NameNoeFieldMoshtary" INTEGER,
    "ccNoeFieldMoshtary" INTEGER,
    "SaghfeMablaghTakhfif" DOUBLE PRECISION,
    "Az" DOUBLE PRECISION,
    "Ta" DOUBLE PRECISION,
    "CodeNoeVorod" INTEGER,
    "OnBach" INTEGER,
    "CodeNoeVosolAzMoshtary" INTEGER, PRIMARY KEY ("ccTakhfifNaghdy")
);

CREATE TABLE IF NOT EXISTS public."TakhfifNaghdySatr" (
    "ccTakhfifNaghdySatr" INTEGER,
    "ccTakhfifNaghdy" INTEGER,
    "ccKala" INTEGER,
    "DarsadTakhfif" DOUBLE PRECISION,
    "CodeNoeMohasebeh" INTEGER,
    "HadeAghalKharid" DOUBLE PRECISION,
    "AzMablagh" DOUBLE PRECISION,
    "TaMablagh" DOUBLE PRECISION,
    "RialTakhfif" DOUBLE PRECISION, PRIMARY KEY ("ccTakhfifNaghdySatr")
);

CREATE TABLE IF NOT EXISTS public."TakhfifSenfi" (
    "ccTakhfifSenfi" INTEGER,
    "CodeNoe" INTEGER,
    "SharhTakhfif" VARCHAR(50),
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "NoeTedadRial" INTEGER,
    "NameNoeFieldMoshtary" INTEGER,
    "ccNoeFieldMoshtary" INTEGER,
    "DiscntType" INTEGER,
    "DiscntSubType" INTEGER,
    "CodeNoeVorod" INTEGER,
    "OnBach" INTEGER, PRIMARY KEY ("ccTakhfifSenfi")
);

CREATE TABLE IF NOT EXISTS public."TakhfifSenfiSatr" (
    "ccTakhfifSenfi" INTEGER,
    "ccTakhfifSenfiSatr" INTEGER,
    "NameNoeField" INTEGER,
    "ccNoeField" INTEGER,
    "Az" DOUBLE PRECISION,
    "Ta" DOUBLE PRECISION,
    "CodeNoeBastehBandy" INTEGER,
    "BeEza" DOUBLE PRECISION,
    "CodeNoeBastehBandyBeEza" INTEGER,
    "DarsadTakhfif" DOUBLE PRECISION,
    "DiscntType" INTEGER,
    "DiscntSubType" INTEGER, PRIMARY KEY ("ccTakhfifSenfiSatr")
);

CREATE TABLE IF NOT EXISTS public."test" (
    "id" INTEGER
);

CREATE TABLE IF NOT EXISTS public."tmpReportEtebarMoshtary" (
    "ccEtebar" INTEGER,
    "SessionID" VARCHAR(100),
    "ccMoshtary" INTEGER,
    "EtebarPishnahadyMoshtary" DOUBLE PRECISION,
    "TedadFaktor" INTEGER,
    "MablaghForosh" DOUBLE PRECISION,
    "TedadDoreh" INTEGER,
    "ToorVisit" INTEGER,
    "ModatVosol" INTEGER,
    "GorohMoshtary" INTEGER,
    "MaxEtebar" DOUBLE PRECISION,
    "MinEtebar" DOUBLE PRECISION,
    "NameMoshtary" VARCHAR(250),
    "CodeMoshtaryOld" VARCHAR(50),
    "TarikhMoarefi" VARCHAR(50),
    "NameGoroh" VARCHAR(100),
    "NoeVosolAzMoshtary" VARCHAR(50),
    "EtebarJary" DOUBLE PRECISION,
    "Asnad" DOUBLE PRECISION,
    "Moavagh" DOUBLE PRECISION,
    "ccMarkazPakhsh" INTEGER,
    "NameMarkazPakhsh" VARCHAR(100), PRIMARY KEY ("ccEtebar")
);

CREATE TABLE IF NOT EXISTS public."tmpReportHadaf" (
    "ccRpt" INTEGER,
    "SessionID" VARCHAR(50),
    "ccMantaghehPakhsh" INTEGER,
    "NameMantaghehPakhsh" VARCHAR(50),
    "ccMarkazPakhsh" INTEGER,
    "NameMarkazPakhsh" VARCHAR(50),
    "ccGorohForosh" INTEGER,
    "NameGoroshforosh" VARCHAR(50),
    "ccForoshandeh" INTEGER,
    "SharhForoshandeh" VARCHAR(50),
    "ccTaminKonandeh" INTEGER,
    "NameTaminkonandeh" VARCHAR(50),
    "ccGorohKala" INTEGER,
    "NameGorohKala" VARCHAR(50),
    "ccKalaCode" INTEGER,
    "NameKala" VARCHAR(50),
    "ForoshRoozRial" DOUBLE PRECISION,
    "HadafRoozRial" DOUBLE PRECISION,
    "ForoshTaRoozMahRial" DOUBLE PRECISION,
    "HadafTaRoozMahRial" DOUBLE PRECISION,
    "ForoshMahRial" DOUBLE PRECISION,
    "HadafMahRial" DOUBLE PRECISION,
    "ForoshDorehRial" DOUBLE PRECISION,
    "HadafDorehRial" DOUBLE PRECISION,
    "ForoshRoozTedad" DOUBLE PRECISION,
    "HadafRoozTedad" DOUBLE PRECISION,
    "ForoshTaRoozMahTedad" DOUBLE PRECISION,
    "HadafTaRoozMahTedad" DOUBLE PRECISION,
    "ForoshMahTedad" DOUBLE PRECISION,
    "HadafMahTedad" DOUBLE PRECISION,
    "ForoshDorehTedad" DOUBLE PRECISION,
    "HadafDorehTedad" DOUBLE PRECISION,
    "ForoshRoozVazn" DOUBLE PRECISION,
    "HadafRoozVazn" DOUBLE PRECISION,
    "ForoshTaRoozMahVazn" DOUBLE PRECISION,
    "HadafTaRoozMahVazn" DOUBLE PRECISION,
    "ForoshMahVazn" DOUBLE PRECISION,
    "HadafMahVazn" DOUBLE PRECISION,
    "ForoshDorehVazn" DOUBLE PRECISION,
    "HadafDorehVazn" DOUBLE PRECISION, PRIMARY KEY ("ccRpt")
);

CREATE TABLE IF NOT EXISTS public."tmpReportJaizehForosh" (
    "ccReport" INTEGER,
    "SessionID" VARCHAR(50),
    "cc" INTEGER,
    "ccA" INTEGER,
    "ccLink" INTEGER,
    "lvl" INTEGER,
    "Sharh" VARCHAR(100),
    "FLName" VARCHAR(100),
    "ShomarehPersonely" INTEGER,
    "Forosh" DOUBLE PRECISION,
    "Hadaf" DOUBLE PRECISION,
    "RialMashmolJaizeh" DOUBLE PRECISION,
    "JamEmtiaz" DOUBLE PRECISION,
    "RialJaizeh" DOUBLE PRECISION,
    "JaizehHogohogh" DOUBLE PRECISION,
    "ccMarkazPakhsh" INTEGER, PRIMARY KEY ("ccReport")
);

CREATE TABLE IF NOT EXISTS public."tmpReportJaizehForoshEmtiaz" (
    "ccRpt" INTEGER,
    "SessionID" VARCHAR(50),
    "cc" INTEGER,
    "lvl" INTEGER,
    "OnvanAmel" VARCHAR(150),
    "Meghdar" DOUBLE PRECISION,
    "Operator" VARCHAR(50),
    "Mabna" DOUBLE PRECISION,
    "Emtiaz" DOUBLE PRECISION,
    "Noe" INTEGER, PRIMARY KEY ("ccRpt")
);

CREATE TABLE IF NOT EXISTS public."tmpReportJaizehForoshKala" (
    "ccRpt" INTEGER,
    "SessionID" VARCHAR(50),
    "cc" INTEGER,
    "lvl" INTEGER,
    "ccKalaCode" INTEGER,
    "ccTaminKonandeh" INTEGER,
    "Forosh" DOUBLE PRECISION,
    "Hadaf" DOUBLE PRECISION,
    "Darsad" DOUBLE PRECISION,
    "RialMashmol" DOUBLE PRECISION, PRIMARY KEY ("ccRpt")
);

CREATE TABLE IF NOT EXISTS public."w" (
    "ccKholaseh" INTEGER,
    "ccMarkazpakhsh" INTEGER,
    "Tarikh" TIMESTAMP,
    "MojodyAnbarKartony" DOUBLE PRECISION,
    "MojodyAnbarTedady" DOUBLE PRECISION,
    "FaktorToziNashodehRialy" DOUBLE PRECISION,
    "FaktorToziNashodehTedad" INTEGER,
    "Forosh15Rialy" DOUBLE PRECISION,
    "MojodyAnbarRialy" DOUBLE PRECISION,
    "Forosh15Kartony" DOUBLE PRECISION,
    "Forosh15Tedady" DOUBLE PRECISION, PRIMARY KEY ("ccKholaseh")
);