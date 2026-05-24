CREATE TABLE IF NOT EXISTS public."AeenNamehElamiehBank" (
    "ccAeenNamehElamiehBank" INTEGER,
    "DastehBandy" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccBankMarkazPakhsh" INTEGER,
    "ccBankCheck" INTEGER,
    "CodeNoeCheck" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccAeenNamehElamiehBank")
);

CREATE TABLE IF NOT EXISTS public."Arz" (
    "ccArz" INTEGER,
    "NameArz" VARCHAR(50),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccArz")
);

CREATE TABLE IF NOT EXISTS public."ArzNerkh" (
    "ccArz" INTEGER,
    "ccArzNerkh" INTEGER,
    "AzTarikh" TIMESTAMP,
    "Nerkh" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccArzNerkh")
);

CREATE TABLE IF NOT EXISTS public."Bedehi" (
    "ccMarkazPakhsh" INTEGER,
    "ccBedehi" INTEGER,
    "ccMoshtary" INTEGER,
    "ccElatBedehi" INTEGER,
    "Tarikh" TIMESTAMP,
    "Mablagh" DOUBLE PRECISION,
    "Tozihat" VARCHAR(-1),
    "BedBes" INTEGER,
    "ccDariaftPardakht" INTEGER,
    "tSal" INTEGER, PRIMARY KEY ("ccBedehi")
);

CREATE TABLE IF NOT EXISTS public."BedehiBackup13971201" (
    "ccMarkazPakhsh" INTEGER,
    "ccBedehi" INTEGER,
    "ccMoshtary" INTEGER,
    "ccElatBedehi" INTEGER,
    "Tarikh" TIMESTAMP,
    "Mablagh" DOUBLE PRECISION,
    "Tozihat" VARCHAR(-1),
    "BedBes" INTEGER,
    "ccDariaftPardakht" INTEGER,
    "tSal" INTEGER
);

CREATE TABLE IF NOT EXISTS public."DariaftForPardakht" (
    "ccDariaftForPardakht" INTEGER,
    "Sal" INTEGER,
    "ccDariaftPardakht" INTEGER,
    "ccDariaftPardakhtLink" INTEGER,
    "ccMoshtary" INTEGER,
    "MablaghPardakht" DOUBLE PRECISION,
    "CodeVazeiat" INTEGER, PRIMARY KEY ("ccDariaftForPardakht", "Sal")
);

CREATE TABLE IF NOT EXISTS public."DariaftPardakht" (
    "ccDariaftPardakht" INTEGER,
    "Sal" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "CodeNoeVorod" INTEGER,
    "CodeNoeDariaftPardakht" INTEGER,
    "CodeNoeSanad" INTEGER,
    "ccSandogh" INTEGER,
    "ccShomarehHesab" INTEGER,
    "CodeNoeTafsily0" INTEGER,
    "ccvTafsily0" INTEGER,
    "CodeNoeTafsily1" INTEGER,
    "ccvTafsily1" INTEGER,
    "ZamaneSabt" TIMESTAMP,
    "ccBankSanad" INTEGER,
    "NameShobehSanad" VARCHAR(50),
    "CodeShobehSanad" VARCHAR(10),
    "ShomarehHesabSanad" VARCHAR(30),
    "ccNoeHesabSanad" INTEGER,
    "ccShahrCheck" INTEGER,
    "CodeNoeCheck" INTEGER,
    "ShomarehSanad" VARCHAR(10),
    "TarikhSanad" TIMESTAMP,
    "Mablagh" DOUBLE PRECISION,
    "CounterCheck" INTEGER,
    "ShomarehElamieh" INTEGER,
    "TarikhElamieh" TIMESTAMP,
    "ccAfradTahsildar" INTEGER,
    "ccDariaftPardakhtLink" INTEGER,
    "ccUser" INTEGER,
    "year" VARCHAR(2),
    "ccManbaDP" INTEGER,
    "ccCodeHesabMoeen" INTEGER,
    "ccKardex" INTEGER,
    "CodeNoeTafsily2" INTEGER,
    "ccvTafsily2" INTEGER,
    "CodeNoeTafsily3" INTEGER,
    "ccvTafsily3" INTEGER,
    "ccDarkhastPardakht" INTEGER,
    "ccDastehCheckBarg" INTEGER,
    "TarikhPardakht" TIMESTAMP,
    "BabatDP" VARCHAR(500),
    "ShomarehHesabVarizElamieh" VARCHAR(50),
    "BeMasoliat" INTEGER,
    "ccElatBargashtCheck" INTEGER,
    "CodeVazeiat" INTEGER,
    "ccAfradAvarandehVajh" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "SeriHarfi" VARCHAR(2),
    "SeriAdadi" VARCHAR(6),
    "TarikhVazeiat" TIMESTAMP,
    "ccDariaftPardakhtVazeiatLast" INTEGER,
    "ccSafteh" INTEGER,
    "PosTransactionNumber" VARCHAR(20),
    "PosTerrminalNumber" VARCHAR(20),
    "Maliat" DOUBLE PRECISION,
    "Avarez" DOUBLE PRECISION,
    "SoodOragh" DOUBLE PRECISION,
    "TanzilOragh" DOUBLE PRECISION,
    "ccMarkazPakhshLast" INTEGER,
    "DarVajh" VARCHAR(250),
    "CodeSayad" VARCHAR(50),
    "SamanehSayad" INTEGER, PRIMARY KEY ("ccDariaftPardakht", "Sal")
);

CREATE TABLE IF NOT EXISTS public."DariaftPardakhtBargashty" (
    "ccDariaftPardakhtBargashty" INTEGER,
    "Sal" INTEGER,
    "ccDariaftPardakhtJaigozin" INTEGER,
    "ccDariaftPardakht" INTEGER,
    "Mablagh" DOUBLE PRECISION,
    "CodeVazeiat" INTEGER,
    "ZamaneTakhsiseCheck" TIMESTAMP,
    "ccUser" INTEGER,
    "ccDariaftPardakhtBargashtyLink" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccDariaftPardakhtBargashty", "Sal")
);

CREATE TABLE IF NOT EXISTS public."DariaftPardakhtBedehi" (
    "ccDariaftPardakhtBedehi" INTEGER,
    "ccBedehi" INTEGER,
    "ccDariaftPardakht" INTEGER,
    "Mablagh" DOUBLE PRECISION,
    "CodeVazeiat" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "CodeNoeBedehi" INTEGER,
    "ccUser" INTEGER,
    "State" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccDariaftPardakhtBedehi")
);

CREATE TABLE IF NOT EXISTS public."DariaftPardakhtDarkhastFaktor" (
    "ccDariaftPardakhtDarkhastFaktor" INTEGER,
    "Sal" INTEGER,
    "ccDarkhastFaktor" INTEGER,
    "ccDariaftPardakht" INTEGER,
    "Mablagh" DOUBLE PRECISION,
    "CodeVazeiat" INTEGER,
    "ccAfradMamorVosol" INTEGER,
    "ZamaneTakhsiseFaktor" TIMESTAMP,
    "ShomarehFaktor" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "SalFaktor" INTEGER,
    "ccUser" INTEGER,
    "ccDariaftPardakhtElamiehMarkazPakhsh" INTEGER,
    "ccMoshtary" INTEGER,
    "MablaghFaktor" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccDariaftPardakhtDarkhastFaktor", "Sal")
);

CREATE TABLE IF NOT EXISTS public."DariaftPardakhtDarkhastFaktorTemp" (
    "ccDariaftPardakhtDarkhastFaktor" INTEGER,
    "Sal" INTEGER,
    "ccDarkhastFaktor" INTEGER,
    "ccDariaftPardakht" INTEGER,
    "Mablagh" DOUBLE PRECISION,
    "CodeVazeiat" INTEGER,
    "ccAfradMamorVosol" INTEGER,
    "ZamaneTakhsiseFaktor" TIMESTAMP,
    "ShomarehFaktor" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "SalFaktor" INTEGER,
    "ccUser" INTEGER,
    "ccDariaftPardakhtElamiehMarkazPakhsh" INTEGER,
    "ccMoshtary" INTEGER,
    "MablaghFaktor" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public."DariaftPardakhtPhoto" (
    "ccDariaftPardakht" INTEGER,
    "Sal" INTEGER,
    "ccPhoto" INTEGER,
    "ccNoePhoto" INTEGER, PRIMARY KEY ("ccDariaftPardakht", "Sal", "ccPhoto")
);

CREATE TABLE IF NOT EXISTS public."DariaftPardakhtTafsily" (
    "ccDariaftPardakht" INTEGER,
    "ccDariaftPardakhtTafsily" INTEGER,
    "Sal" INTEGER,
    "ccCodeHesab" INTEGER,
    "ccTafsily1" INTEGER,
    "ccTafsily2" INTEGER,
    "ccTafsily3" INTEGER,
    "Mablagh" DOUBLE PRECISION,
    "ccUser" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "Codevazeiat" INTEGER,
    "sharh" VARCHAR(200), PRIMARY KEY ("ccDariaftPardakhtTafsily", "Sal")
);

CREATE TABLE IF NOT EXISTS public."DariaftPardakhtTakhirTadieh" (
    "ccDariaftPardakhtTakhirTadieh" INTEGER,
    "ccTakhirTadieh" INTEGER,
    "ccDariaftPardakht" INTEGER,
    "Mablagh" DOUBLE PRECISION,
    "CodeVazeiat" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "CodeNoeBedehi" INTEGER,
    "ccUser" INTEGER,
    "State" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "ZamaneSabt" TIMESTAMP, PRIMARY KEY ("ccDariaftPardakhtTakhirTadieh")
);

CREATE TABLE IF NOT EXISTS public."DariaftPardakhtVazeiat" (
    "ccDariaftPardakht" INTEGER,
    "ccDariaftPardakhtVazeiat" INTEGER,
    "Sal" INTEGER,
    "CodeVazeiat" INTEGER,
    "ZamanVazeiat" TIMESTAMP,
    "Mablagh" DOUBLE PRECISION,
    "TarikhSanad" TIMESTAMP,
    "ccUser" INTEGER,
    "TarikhVazeiat" TIMESTAMP,
    "ccElatBargashtCheck" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "ccAfrad" INTEGER,
    "ccTafsily" INTEGER,
    "ccShomarehHesab" INTEGER, PRIMARY KEY ("ccDariaftPardakhtVazeiat", "Sal")
);

CREATE TABLE IF NOT EXISTS public."DarkhastPardakht" (
    "ccDarkhastPardakht" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "TarikhDarkhast" TIMESTAMP,
    "ShomarehDarkhast" INTEGER,
    "TarikhNiaz" TIMESTAMP,
    "MablaghDarkhast" DOUBLE PRECISION,
    "Babat" VARCHAR(500),
    "ccAfradDarkhast" INTEGER,
    "CodeNoeTafsily0" INTEGER,
    "ccvTafsily0" INTEGER,
    "CodeNoeTafsily1" INTEGER,
    "ccvTafsily1" INTEGER,
    "CodeNoeTafsily2" INTEGER,
    "ccvTafsily2" INTEGER,
    "CodeNoeTafsily3" INTEGER,
    "ccvTafsily3" INTEGER,
    "ccManbaDP" INTEGER,
    "ccCodeHesabMoeen" INTEGER,
    "CodeNoePardakht" INTEGER,
    "ccSandogh" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccDarkhastPardakht")
);

CREATE TABLE IF NOT EXISTS public."DarkhastPardakhVazeiat" (
    "ccDarkhastPardakhtVazeiat" INTEGER,
    "ccDarkhastPardakht" INTEGER,
    "ZamanVazeiatDarkhastPardakht" TIMESTAMP,
    "CodeVazeiatDarkhastPardakht" INTEGER,
    "ccUser" INTEGER,
    "Elat" VARCHAR(50),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccDarkhastPardakhtVazeiat")
);

CREATE TABLE IF NOT EXISTS public."DastehCheck" (
    "ccDastehCheck" INTEGER,
    "ccShomarehHesab" INTEGER,
    "TarikhDarkhast" TIMESTAMP,
    "TarikhDariaft" TIMESTAMP,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccDastehCheck")
);

CREATE TABLE IF NOT EXISTS public."DastehCheckBarg" (
    "ccDastehCheck" INTEGER,
    "ccDastehCheckBarg" INTEGER,
    "Serial" INTEGER,
    "Sery" VARCHAR(10),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccDastehCheckBarg")
);

CREATE TABLE IF NOT EXISTS public."Elamieh" (
    "ccElamieh" INTEGER,
    "CodeNoeElamieh" INTEGER,
    "ccMarkazPakhshAz" INTEGER,
    "ccMarkazPakhshBe" INTEGER,
    "TarikhElamieh" TIMESTAMP,
    "ccCodeHesabTaraf1" INTEGER,
    "ccTafsily1Taraf1" INTEGER,
    "ccTafsily2Taraf1" INTEGER,
    "ccTafsily3Taraf1" INTEGER,
    "ccCodeHesabTaraf2" INTEGER,
    "ccTafsily1Taraf2" INTEGER,
    "ccTafsily2Taraf2" INTEGER,
    "ccTafsily3Taraf2" INTEGER,
    "Elat" VARCHAR(-1),
    "Mablagh" DOUBLE PRECISION,
    "Tozihat" VARCHAR(250),
    "CodeVazeiat" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccElamieh")
);

CREATE TABLE IF NOT EXISTS public."ElamiehDetail" (
    "ccElamiehSatr" INTEGER,
    "ccElamieh" INTEGER,
    "ccCodeHesabTaraf1" INTEGER,
    "ccTafsily1Taraf1" INTEGER,
    "ccTafsily2Taraf1" INTEGER,
    "ccTafsily3Taraf1" INTEGER,
    "NoeMahal" INTEGER,
    "Mablagh" DOUBLE PRECISION, PRIMARY KEY ("ccElamiehSatr")
);

CREATE TABLE IF NOT EXISTS public."ElamiehMaster" (
    "ccElamieh" INTEGER,
    "CodeNoeElamieh" INTEGER,
    "ccMarkazPakhshAz" INTEGER,
    "ccMarkazPakhshBe" INTEGER,
    "Tozihat" VARCHAR(-1),
    "TarikhElamieh" TIMESTAMP,
    "Elat" VARCHAR(-1),
    "SumMablagh" DOUBLE PRECISION,
    "CodeVazeiat" INTEGER,
    "ModifiedDate" TIMESTAMP,
    "ccAfrad" INTEGER, PRIMARY KEY ("ccElamieh")
);

CREATE TABLE IF NOT EXISTS public."ElatBargashtCheck" (
    "ccElatBargashtCheck" INTEGER,
    "SharhElat" VARCHAR(50),
    "CodeVazeiatBargashty" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccElatBargashtCheck")
);

CREATE TABLE IF NOT EXISTS public."ElatBedehi" (
    "ccElatBedehi" INTEGER,
    "ElatBedehi" VARCHAR(50),
    "ccCodeHesab" INTEGER, PRIMARY KEY ("ccElatBedehi")
);

CREATE TABLE IF NOT EXISTS public."ElatTakhirTadieh" (
    "ccElatTakhirTadieh" INTEGER,
    "ElatTakhirTadieh" VARCHAR(50),
    "ccCodeHesab" INTEGER, PRIMARY KEY ("ccElatTakhirTadieh")
);

CREATE TABLE IF NOT EXISTS public."HazinehTankhah" (
    "ccHazinehTankhah" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccTankhah" INTEGER,
    "ccAfradTankhah" INTEGER,
    "Tarikh" TIMESTAMP,
    "Shomareh" INTEGER,
    "Tozihat" VARCHAR(100),
    "CodeVazeiat" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccHazinehTankhah")
);

CREATE TABLE IF NOT EXISTS public."HazinehTankhahSatr" (
    "ccHazinehTankhah" INTEGER,
    "ccHazinehTankhahSatr" INTEGER,
    "ccHazineh" INTEGER,
    "ccTafsily" INTEGER,
    "ccTafsily2" INTEGER,
    "ccTafsily3" INTEGER,
    "Tarikh" TIMESTAMP,
    "Mablagh" DOUBLE PRECISION,
    "Tozihat" VARCHAR(100),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccHazinehTankhahSatr")
);

CREATE TABLE IF NOT EXISTS public."KartBank" (
    "ccKartBank" INTEGER,
    "ccKartBankNoeAmalKard" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccShomarehHesab1" INTEGER,
    "CodeNoeTafsily1" INTEGER,
    "ccvTafsily1" INTEGER,
    "ShomarehSanad" VARCHAR(10),
    "TarikhSanad" TIMESTAMP,
    "BedBes" INTEGER,
    "Mablagh" DOUBLE PRECISION,
    "BabatDP" VARCHAR(500),
    "ZamaneSabt" TIMESTAMP,
    "ccShomarehHesab2" INTEGER,
    "CodeVazeiat" INTEGER,
    "ShomarehResid" VARCHAR(100),
    "ccUser" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccKartBank")
);

CREATE TABLE IF NOT EXISTS public."KartBankNoeAmalKard" (
    "ccKartBankNoeAmalKard" INTEGER,
    "Sharh" VARCHAR(50),
    "BedBes" INTEGER,
    "Faal" TEXT,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccKartBankNoeAmalKard")
);

CREATE TABLE IF NOT EXISTS public."KartBankVazeiat" (
    "ccKartBank" INTEGER,
    "ccKartBankVazeiat" INTEGER,
    "ZamaneVazeiat" TIMESTAMP,
    "TarikhVazeiat" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "ccUser" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccKartBankVazeiat")
);

CREATE TABLE IF NOT EXISTS public."ManbaDP" (
    "ccManbaDP" INTEGER,
    "CodeNoeDariaftPardakht" INTEGER,
    "ccCodeHesabMoeen" INTEGER,
    "NameManbaDP" VARCHAR(50),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "Faal" TEXT, PRIMARY KEY ("ccManbaDP")
);

CREATE TABLE IF NOT EXISTS public."PardakhtBank" (
    "ccPardakhtBank" INTEGER,
    "ccAfrad" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "Mablagh" INTEGER,
    "TarikhPardakht" TIMESTAMP,
    "CodeNoePardakht" INTEGER,
    "ccUser" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccPardakhtBank")
);

CREATE TABLE IF NOT EXISTS public."RasGiri" (
    "ccRasGiri" INTEGER,
    "ShomarehRasGiri" INTEGER,
    "TarikhRasGiri" TIMESTAMP,
    "ccDarkhastFaktor" INTEGER,
    "EkhtelafRoozFaktor" INTEGER,
    "TarikhRaseFaktor" TIMESTAMP,
    "RoozTakhir" INTEGER,
    "TarikhMohlatePardakhtFaktor" TIMESTAMP,
    "ShomarehCheck" VARCHAR(50),
    "MablaghCheck" DOUBLE PRECISION,
    "TarikhCheck" TIMESTAMP,
    "EkhtelafRoozCheck" INTEGER,
    "TarikhRaseCheck" TIMESTAMP,
    "EkhtelafMohlatPardakhtVaRaseCheck" INTEGER,
    "CodevazeiatRasGiri" INTEGER, PRIMARY KEY ("ccRasGiri")
);

CREATE TABLE IF NOT EXISTS public."RasGiriEstemhal" (
    "ccRasGiri" INTEGER,
    "ShomarehRasGiri" INTEGER,
    "TarikhRasGiri" TIMESTAMP,
    "ccDarkhastFaktor" INTEGER,
    "EkhtelafRoozFaktor" INTEGER,
    "TarikhRaseFaktor" TIMESTAMP,
    "RoozTakhir" INTEGER,
    "TarikhMohlatePardakhtFaktor" TIMESTAMP,
    "ShomarehCheck" VARCHAR(50),
    "MablaghCheck" DOUBLE PRECISION,
    "TarikhCheck" TIMESTAMP,
    "EkhtelafRoozCheck" INTEGER,
    "TarikhRaseCheck" TIMESTAMP,
    "EkhtelafMohlatPardakhtVaRaseCheck" INTEGER, PRIMARY KEY ("ccRasGiri")
);

CREATE TABLE IF NOT EXISTS public."Safteh" (
    "ccMarkazPakhsh" INTEGER,
    "ccSandogh" INTEGER,
    "ccSafteh" INTEGER,
    "TarikhKharid" TIMESTAMP,
    "Serial" INTEGER,
    "Sery" VARCHAR(10),
    "Mablagh" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccSafteh")
);

CREATE TABLE IF NOT EXISTS public."Sandogh" (
    "ccSandogh" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "NameSandogh" VARCHAR(50),
    "CodeArzyRialy" TEXT,
    "ccAfradSandoghdar" INTEGER,
    "IsForVosol" TEXT,
    "SaghfeSandogh" DOUBLE PRECISION,
    "KasreSandogh" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "MablaghEbteda" INTEGER, PRIMARY KEY ("ccSandogh")
);

CREATE TABLE IF NOT EXISTS public."SoratHesabBank" (
    "ccSoratHesabBank" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccShomarehHesab" INTEGER,
    "Tarikh" TIMESTAMP,
    "CodeNoeVorod" INTEGER,
    "MablaghMandehAvalDoreh" DOUBLE PRECISION,
    "CodeVazeiat" INTEGER,
    "MablaghMandehPayanDoreh" DOUBLE PRECISION, PRIMARY KEY ("ccSoratHesabBank")
);

CREATE TABLE IF NOT EXISTS public."SoratHesabBankSatr" (
    "ccSoratHesabBank" INTEGER,
    "ccSoratHesabBankSatr" INTEGER,
    "CodeNoeSanad" INTEGER,
    "ShomarehSanad" VARCHAR(20),
    "SeriHarfi" VARCHAR(2),
    "SeriAdadi" VARCHAR(6),
    "MablaghBed" DOUBLE PRECISION,
    "MablaghBes" DOUBLE PRECISION,
    "ccRefrence" INTEGER, PRIMARY KEY ("ccSoratHesabBankSatr")
);

CREATE TABLE IF NOT EXISTS public."SystemConfig" (
    "ccMarkazPakhsh" INTEGER,
    "CodeNoeDariaftAzMoshtary" INTEGER,
    "ManbaDariaftPishfarz" INTEGER,
    "ManbaPardakhtPishfarz" INTEGER,
    "NoeHesabPishFarz" INTEGER,
    "ShomarehHesabMarkazPakhshPishFarz" INTEGER, PRIMARY KEY ("ccMarkazPakhsh")
);

CREATE TABLE IF NOT EXISTS public."Taahod" (
    "ccTaahod" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "CodeNoeDPTaahod" INTEGER,
    "ccTafsily" INTEGER,
    "Tarikh" TIMESTAMP,
    "Tedad" INTEGER,
    "Mablagh" DOUBLE PRECISION,
    "CodeNoeTaahod" INTEGER,
    "TaTarikh" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "ccTaahodLink" INTEGER,
    "ccManba" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccTaahod")
);

CREATE TABLE IF NOT EXISTS public."Tahsildar" (
    "ccMarkazPakhsh" INTEGER,
    "ccTahsildar" INTEGER,
    "ccAfradTahsildar" INTEGER,
    "SharhTahsildar" VARCHAR(100),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccTahsildar")
);

CREATE TABLE IF NOT EXISTS public."TakhirTadieh" (
    "ccMarkazPakhsh" INTEGER,
    "ccTakhirTadieh" INTEGER,
    "ccMoshtary" INTEGER,
    "ccElatTakhirTadieh" INTEGER,
    "Tarikh" TIMESTAMP,
    "Mablagh" DOUBLE PRECISION,
    "Tozihat" VARCHAR(-1), PRIMARY KEY ("ccTakhirTadieh")
);

CREATE TABLE IF NOT EXISTS public."Tankhah" (
    "ccMarkazPakhsh" INTEGER,
    "ccTankhah" INTEGER,
    "ccAfrad" INTEGER,
    "SharhTankhah" VARCHAR(50),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccTankhah")
);

CREATE TABLE IF NOT EXISTS public."tmpReportAmalKardSandogh" (
    "ccRpt" INTEGER,
    "SessionID" VARCHAR(50),
    "ccMarkazPakhsh" INTEGER,
    "NameMarkazPakhsh" VARCHAR(50),
    "ccMoshtary" INTEGER,
    "CodeMoshtaryOld" VARCHAR(15),
    "NameMoshtary" VARCHAR(100),
    "ccForoshandeh" INTEGER,
    "NameForoshandeh" VARCHAR(100),
    "ccAfradMamorPakhsh" INTEGER,
    "NameMamorPakhsh" VARCHAR(100),
    "ShomarehFaktor" VARCHAR(20),
    "TarikhFaktor" VARCHAR(10),
    "TarikhErsal" VARCHAR(10),
    "MablaghKhalesFaktor" DOUBLE PRECISION,
    "MablaghDPF" DOUBLE PRECISION,
    "MablaghDP" DOUBLE PRECISION,
    "TarikhF" VARCHAR(10),
    "TarikhL" TIMESTAMP,
    "Naghd1" DOUBLE PRECISION,
    "Chek2" DOUBLE PRECISION,
    "FishHavaleh3_4" DOUBLE PRECISION,
    "Marjoee6" DOUBLE PRECISION,
    "EkhtelafTakhfif7" DOUBLE PRECISION,
    "MoghaieratPakhsh8" DOUBLE PRECISION,
    "ElamiehDariaft9" DOUBLE PRECISION,
    "ElamiehPardakht10" DOUBLE PRECISION,
    "TakhfifNaghdi20" DOUBLE PRECISION,
    "KarmozdHavalehVojoh21" DOUBLE PRECISION,
    "TakhfifMoredi22" DOUBLE PRECISION,
    "ElamiehSetad25" DOUBLE PRECISION,
    "ChekBargashty" DOUBLE PRECISION,
    "NaghsChek" DOUBLE PRECISION,
    "CodeNoe" INTEGER, PRIMARY KEY ("ccRpt")
);