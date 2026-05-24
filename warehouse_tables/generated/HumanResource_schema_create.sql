CREATE TABLE IF NOT EXISTS public."AeenNamehMabaleghMamoriat" (
    "ccAeenNamehMabaleghMamoriat" INTEGER,
    "FromDate" TIMESTAMP,
    "ZaribRoozTatil" DOUBLE PRECISION,
    "ZaribHoghoghModirAmel" DOUBLE PRECISION,
    "ZaribRoozModirAmel" DOUBLE PRECISION,
    "ZaribHoghoghAddi" DOUBLE PRECISION,
    "ZaribHoghoghAmozeshi" DOUBLE PRECISION,
    "ZaribKilometrSetad" DOUBLE PRECISION,
    "ZaribKilometrMarakez" DOUBLE PRECISION,
    "ZaribTedadMoshtaryMovazeen" DOUBLE PRECISION,
    "ZaribSabetMoshtaryMovazeen" DOUBLE PRECISION,
    "ZaribMasafatMovazeen" DOUBLE PRECISION,
    "ZaribMoshtaryMasafatMovazeen" DOUBLE PRECISION,
    "ZaribTedadMoshtaryNamaiandehForosh" DOUBLE PRECISION,
    "ZaribSabetMoshtaryNamaiandehForosh" DOUBLE PRECISION,
    "ZaribMasafatNamaiandehForosh" DOUBLE PRECISION,
    "ZaribMoshtaryMasafatNamaiandehForosh" DOUBLE PRECISION,
    "ZaribMohasebehNamaiandehForoshMovazea" DOUBLE PRECISION,
    "MablaghKhodroSetad" DOUBLE PRECISION,
    "MablaghKhodroMarakez" DOUBLE PRECISION,
    "HazinehAjans" DOUBLE PRECISION, PRIMARY KEY ("ccAeenNamehMabaleghMamoriat")
);

CREATE TABLE IF NOT EXISTS public."AeenNamehMamoriat" (
    "ccAeenNamehMamoriat" INTEGER,
    "AzTarikh" TIMESTAMP,
    "ccPost" INTEGER,
    "ZaribMabna" DOUBLE PRECISION,
    "Hadeaghal" INTEGER,
    "Hadeaksar" INTEGER, PRIMARY KEY ("ccAeenNamehMamoriat")
);

CREATE TABLE IF NOT EXISTS public."AeenNamehOlaviatMabaleghMamoriat" (
    "ccAeenNamehOlaviatMabaleghMamoriat" INTEGER,
    "ccAeenNamehOlaviatMarakezMamoriat" INTEGER,
    "FromDate" TIMESTAMP,
    "MablaghRaft" DOUBLE PRECISION,
    "MablaghBargasht" DOUBLE PRECISION, PRIMARY KEY ("ccAeenNamehOlaviatMabaleghMamoriat")
);

CREATE TABLE IF NOT EXISTS public."AeenNamehOlaviatMarakezMamoriat" (
    "ccAeenNamehOlaviatMarakezMamoriat" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "Olaviat" INTEGER, PRIMARY KEY ("ccAeenNamehOlaviatMarakezMamoriat")
);

CREATE TABLE IF NOT EXISTS public."AfradDariaftKonandeh" (
    "ccAfradDariaftKonandeh" INTEGER,
    "ccAfrad" INTEGER
);

CREATE TABLE IF NOT EXISTS public."Agahie" (
    "ccAgahie" INTEGER,
    "ccNoeAgahie" INTEGER,
    "MatneAgahie" VARCHAR(-1),
    "MablaghAgahie" DOUBLE PRECISION, PRIMARY KEY ("ccAgahie")
);

CREATE TABLE IF NOT EXISTS public."AghsateVam" (
    "ccDarkhastVam" INTEGER,
    "ccAghsatVam" INTEGER,
    "TarikhPardakht" TIMESTAMP,
    "Mablagh" DOUBLE PRECISION,
    "CodeNoePardakht" INTEGER,
    "ShomarehFish" VARCHAR(10),
    "ccMohasebehHoghoghSatr" INTEGER,
    "TarikhVorod" TIMESTAMP, PRIMARY KEY ("ccAghsatVam")
);

CREATE TABLE IF NOT EXISTS public."AiabZohab" (
    "ccAiabZohab" INTEGER,
    "Fromdate" TIMESTAMP,
    "ccMarkazPakhsh" INTEGER,
    "MablaghAiabZohab" DOUBLE PRECISION, PRIMARY KEY ("ccAiabZohab")
);

CREATE TABLE IF NOT EXISTS public."AmozeshAmozeshgah" (
    "ccAmozeshgah" INTEGER,
    "NameAmozeshgah" VARCHAR(100),
    "NameModirAmozeshgah" VARCHAR(100),
    "Address" VARCHAR(256),
    "Telephone" VARCHAR(50),
    "Fax" VARCHAR(50),
    "Email" VARCHAR(150), PRIMARY KEY ("ccAmozeshgah")
);

CREATE TABLE IF NOT EXISTS public."AmozeshAmozeshgahDoreh" (
    "ccAmozeshgah" INTEGER,
    "ccAmozeshgahDoreh" INTEGER,
    "NameDoreh" VARCHAR(150),
    "CodeDoreh" VARCHAR(10),
    "TolDoreh" INTEGER,
    "TedadJalaseh" INTEGER,
    "SaatJalaseh" INTEGER,
    "TarikhShoroDoreh" TIMESTAMP,
    "NameOstad" VARCHAR(50),
    "RozhaiehHafteh" VARCHAR(200),
    "Tozihat" VARCHAR(200), PRIMARY KEY ("ccAmozeshgahDoreh")
);

CREATE TABLE IF NOT EXISTS public."AmozeshOnvanDoreh" (
    "ccOnvanDoreh" INTEGER,
    "OnvanDoreh" VARCHAR(100),
    "CodeDoreh" VARCHAR(50),
    "ModatDoreh" DOUBLE PRECISION,
    "Mohtava" VARCHAR(250),
    "ccDastehBandyDoreha" INTEGER, PRIMARY KEY ("ccOnvanDoreh")
);

CREATE TABLE IF NOT EXISTS public."AmozeshOstad" (
    "ccOstad" INTEGER,
    "FName" VARCHAR(50),
    "LName" VARCHAR(50),
    "ccMadrakTahsily" INTEGER,
    "ccReshtehGeraiesh" INTEGER,
    "OzveHeiatElmy" TEXT,
    "RotbehElmy" INTEGER,
    "SabeghehTadris" INTEGER,
    "AddressMahalKar" VARCHAR(256),
    "TelephonMahalKar" VARCHAR(50),
    "AddressManzel" VARCHAR(256),
    "TelephoneManzel" VARCHAR(50),
    "Mobile" VARCHAR(50),
    "Email" VARCHAR(150),
    "SavabeghPazhohesh" VARCHAR(-1), PRIMARY KEY ("ccOstad")
);

CREATE TABLE IF NOT EXISTS public."AmozeshOstadDorehEraehShodeh" (
    "ccOstadDorehEraehShodeh" INTEGER,
    "ccOnvanDoreh" INTEGER,
    "ccOstad" INTEGER,
    "TarikhEjraDoreh" TIMESTAMP,
    "TedadFaragiran" INTEGER,
    "MianginArziaby" DOUBLE PRECISION,
    "Darajeh" INTEGER, PRIMARY KEY ("ccOstadDorehEraehShodeh")
);

CREATE TABLE IF NOT EXISTS public."AmozeshOstadEraehDoreh" (
    "ccOstad" INTEGER,
    "ccOstadDorehEraeh" INTEGER,
    "CodeNoeEraeh" INTEGER,
    "NameDorehEraeh" VARCHAR(100),
    "MahalEraeh" VARCHAR(100),
    "TarikhEraeh" TIMESTAMP, PRIMARY KEY ("ccOstadDorehEraeh")
);

CREATE TABLE IF NOT EXISTS public."AmozeshOstadSavabeghAmozesh" (
    "ccOstad" INTEGER,
    "ccOstadSavabeghAmozesh" INTEGER,
    "NameDars" VARCHAR(100),
    "MahalAmozesh" VARCHAR(100), PRIMARY KEY ("ccOstadSavabeghAmozesh")
);

CREATE TABLE IF NOT EXISTS public."AmozeshOstadSavabeghTahsily" (
    "ccOstad" INTEGER,
    "ccOstadSavabeghTahsily" INTEGER,
    "ccReshtehGeraiesh" INTEGER,
    "MahalTahsil" VARCHAR(150),
    "ccMadrakTahsily" INTEGER,
    "ccMaghtaeTahsily" INTEGER, PRIMARY KEY ("ccOstadSavabeghTahsily")
);

CREATE TABLE IF NOT EXISTS public."AmozeshOstadTavanmandy" (
    "ccOstad" INTEGER,
    "ccOstadTavanmandy" INTEGER,
    "CodeNoeEraeh" INTEGER,
    "Onvan" VARCHAR(100),
    "AlaghehBishtar" TEXT, PRIMARY KEY ("ccOstadTavanmandy")
);

CREATE TABLE IF NOT EXISTS public."AmozeshOstadZaban" (
    "ccOstad" INTEGER,
    "ccNoeZaban" INTEGER,
    "CodeSathMokalemeh" INTEGER,
    "CodeSathKhandan" INTEGER,
    "CodeSathNeveshtan" INTEGER, PRIMARY KEY ("ccOstad", "ccNoeZaban")
);

CREATE TABLE IF NOT EXISTS public."AmozeshTaghvim" (
    "ccTaghvimAmozesh" INTEGER,
    "ccOnvanDoreh" INTEGER,
    "TedadSaat" INTEGER,
    "CodeNoeDoreh" INTEGER,
    "CodeNoeKar" INTEGER,
    "TarikhPishnahady" TIMESTAMP,
    "CodeMahalEjra" INTEGER, PRIMARY KEY ("ccTaghvimAmozesh")
);

CREATE TABLE IF NOT EXISTS public."AmozeshTaghvimAfrad" (
    "ccTaghvimAmozesh" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccAfrad" INTEGER, PRIMARY KEY ("ccTaghvimAmozesh", "ccAfrad")
);

CREATE TABLE IF NOT EXISTS public."DarkhastJazbNiro" (
    "ccDarkhastJazbNiro" INTEGER,
    "ccShoghl" INTEGER,
    "EtelaateAgahi" VARCHAR(255),
    "Tedad1" INTEGER,
    "ElateDarkhast" VARCHAR(100),
    "ccAfradDarkhastKonandeh" INTEGER,
    "CodeVazeiat" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccPost" INTEGER,
    "Elat" VARCHAR(255),
    "TarikhDarkhast" TIMESTAMP,
    "ccUser" INTEGER,
    "ccKarbar" INTEGER, PRIMARY KEY ("ccDarkhastJazbNiro")
);

CREATE TABLE IF NOT EXISTS public."DarkhastJazbNiroAgahie" (
    "ccAgahie" INTEGER,
    "ccDarkhastJazbNiro" INTEGER, PRIMARY KEY ("ccAgahie", "ccDarkhastJazbNiro")
);

CREATE TABLE IF NOT EXISTS public."DarkhastJazbNiroPhoto" (
    "ccDarkhastJazbNiro" INTEGER,
    "ccPhoto" INTEGER, PRIMARY KEY ("ccDarkhastJazbNiro", "ccPhoto")
);

CREATE TABLE IF NOT EXISTS public."DarkhastJazbNiroVazeiat" (
    "ccDarkhastJazbNiro" INTEGER,
    "ccDarkhastJazbNiroVazeiat" INTEGER,
    "CodeVazeiat" INTEGER,
    "TarikhVazeiat" TIMESTAMP,
    "ccUser" INTEGER, PRIMARY KEY ("ccDarkhastJazbNiroVazeiat")
);

CREATE TABLE IF NOT EXISTS public."DarkhastMorkhasi" (
    "ccMarkazPakhsh" INTEGER,
    "ccDarkhastMorkhasi" INTEGER,
    "CodeNoe" INTEGER,
    "ccAfrad" INTEGER,
    "ccAfradJaigozin" INTEGER,
    "AzTarikh" TIMESTAMP,
    "TaTarikh" TIMESTAMP,
    "CodeNoeMorkhasi" INTEGER,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(100),
    "ccUser" INTEGER,
    "ccKarbar" INTEGER, PRIMARY KEY ("ccDarkhastMorkhasi")
);

CREATE TABLE IF NOT EXISTS public."DarkhastMorkhasiVazeiat" (
    "ccDarkhastMorkhasi" INTEGER,
    "ccDarkhastMorkhasiVazeiat" INTEGER,
    "CodeVazeiat" INTEGER,
    "TarikhVazeiat" TIMESTAMP,
    "ccUser" INTEGER, PRIMARY KEY ("ccDarkhastMorkhasiVazeiat")
);

CREATE TABLE IF NOT EXISTS public."DarkhastVam" (
    "ccDarkhastVam" INTEGER,
    "ccNoeVam" INTEGER,
    "ccAfradDarkhastKonandeh" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "TarikhDarkhast" TIMESTAMP,
    "MablaghDarkhast" DOUBLE PRECISION,
    "TedadAghsat" INTEGER,
    "MablaghAghsat" DOUBLE PRECISION,
    "CodeVazeiat" INTEGER,
    "ccUser" INTEGER,
    "ccKarbar" INTEGER,
    "TarikhDariaft" TIMESTAMP,
    "CodeNoeZemanat" INTEGER,
    "TarikhAvalinGhest" TIMESTAMP,
    "Elat" VARCHAR(255),
    "ccDariaftPardakht" INTEGER,
    "Sal" INTEGER,
    "TarikhVorod" TIMESTAMP, PRIMARY KEY ("ccDarkhastVam")
);

CREATE TABLE IF NOT EXISTS public."DarkhastVamKatalog" (
    "ccDarkhastVamKatalog" INTEGER,
    "ccDarkhastVam" INTEGER,
    "ShomarehGhest" INTEGER,
    "MablaghGhest" DOUBLE PRECISION, PRIMARY KEY ("ccDarkhastVamKatalog")
);

CREATE TABLE IF NOT EXISTS public."DarkhastVamVazeiat" (
    "ccDarkhastVam" INTEGER,
    "ccDarkhastVamVazeiat" INTEGER,
    "CodeVazeiat" INTEGER,
    "TarikhVazeiat" TIMESTAMP,
    "ccUser" INTEGER, PRIMARY KEY ("ccDarkhastVamVazeiat")
);

CREATE TABLE IF NOT EXISTS public."DastehBandyDoreha" (
    "ccDastehBandyDoreha" INTEGER,
    "DastehBandyDoreha" VARCHAR(50), PRIMARY KEY ("ccDastehBandyDoreha")
);

CREATE TABLE IF NOT EXISTS public."DinMazhab" (
    "ccDinMazhab" INTEGER,
    "CodeNoeDinMazhab" INTEGER,
    "NameDinMazhab" VARCHAR(50),
    "ccDinMazhabLink" INTEGER, PRIMARY KEY ("ccDinMazhab")
);

CREATE TABLE IF NOT EXISTS public."Ghaza" (
    "ccMarkazPakhsh" INTEGER,
    "ccGhaza" INTEGER,
    "PersonelGhaza" VARCHAR(50), PRIMARY KEY ("ccGhaza")
);

CREATE TABLE IF NOT EXISTS public."GhazaSatr" (
    "ccGhaza" INTEGER,
    "ccGhazasatr" INTEGER,
    "AzTarikh" TIMESTAMP,
    "Mablagh" DOUBLE PRECISION, PRIMARY KEY ("ccGhazasatr")
);

CREATE TABLE IF NOT EXISTS public."GorohHoghoghy" (
    "ccGorohHoghoghy" INTEGER,
    "NameGorohHoghoghy" VARCHAR(50), PRIMARY KEY ("ccGorohHoghoghy")
);

CREATE TABLE IF NOT EXISTS public."GorohShoghl" (
    "ccGorohShoghl" INTEGER,
    "NameGorohShoghl" VARCHAR(50), PRIMARY KEY ("ccGorohShoghl")
);

CREATE TABLE IF NOT EXISTS public."KhadamatRefahi" (
    "ccKhadamatRefahi" INTEGER,
    "NameKhadamatRefahi" VARCHAR(100),
    "ccNoeKhadamatRefahi" INTEGER,
    "NamaieshDarFish" TEXT,
    "Faal" TEXT,
    "CodeNoeRefahi" INTEGER,
    "ccSherkat" INTEGER,
    "CodeItem" INTEGER, PRIMARY KEY ("ccKhadamatRefahi")
);

CREATE TABLE IF NOT EXISTS public."KhadamatRefahiAfrad" (
    "ccKhadamatRefahiAfrad" INTEGER,
    "ccKhadamatRefahi" INTEGER,
    "ccAfrad" INTEGER,
    "Shomareh" VARCHAR(20),
    "MablaghSahmeKarmand" DOUBLE PRECISION,
    "MablaghSahmeKarfarma" DOUBLE PRECISION,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP, PRIMARY KEY ("ccKhadamatRefahiAfrad")
);

CREATE TABLE IF NOT EXISTS public."KhadamatRefahiAfrad14041028" (
    "ccKhadamatRefahiAfrad" INTEGER,
    "ccKhadamatRefahi" INTEGER,
    "ccAfrad" INTEGER,
    "Shomareh" VARCHAR(20),
    "MablaghSahmeKarmand" DOUBLE PRECISION,
    "MablaghSahmeKarfarma" DOUBLE PRECISION,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public."KhadamatRefahiAfradParsian" (
    "ccKhadamatRefahiAfradParsian" INTEGER,
    "ccKhadamatRefahiAfrad" INTEGER,
    "Mablagh" DOUBLE PRECISION,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "Sharh" VARCHAR(255),
    "Mah" INTEGER,
    "ccDariaftPardakht" INTEGER, PRIMARY KEY ("ccKhadamatRefahiAfradParsian")
);

CREATE TABLE IF NOT EXISTS public."KhadamatRefahiAfradTakafol" (
    "ccKhadamatRefahiAfradTakafol" INTEGER,
    "ccKhadamatRefahiAfrad" INTEGER,
    "ccPersonelAfradTakafol" INTEGER,
    "Shomareh" VARCHAR(20),
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP, PRIMARY KEY ("ccKhadamatRefahiAfradTakafol")
);

CREATE TABLE IF NOT EXISTS public."KhadamatRefahiHistory" (
    "ccKhadamatRefahiHistory" INTEGER,
    "ccKhadamatRefahi" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "TedadAfradTahtePoshesh" INTEGER,
    "Mablagh" DOUBLE PRECISION,
    "NamaieshDarFish" TEXT,
    "Sharh" VARCHAR(255), PRIMARY KEY ("ccKhadamatRefahiHistory")
);

CREATE TABLE IF NOT EXISTS public."KhadamatRefahiHistorySatr" (
    "ccKhadamatRefahiHistory" INTEGER,
    "ccKhadamatRefahiHistorySatr" INTEGER,
    "SahmeKarfarma" DOUBLE PRECISION,
    "SahmeFard" DOUBLE PRECISION,
    "TaSen" INTEGER, PRIMARY KEY ("ccKhadamatRefahiHistorySatr")
);

CREATE TABLE IF NOT EXISTS public."KhadamatRefahiMablaghAfrad" (
    "ccKhadamatRefahiMablaghAfrad" INTEGER,
    "ccKhadamatRefahiAfrad" INTEGER,
    "MablaghSahmeKarmand" DOUBLE PRECISION,
    "MablaghSahmeKarfarma" DOUBLE PRECISION,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP, PRIMARY KEY ("ccKhadamatRefahiMablaghAfrad")
);

CREATE TABLE IF NOT EXISTS public."MadrakTahsily" (
    "ccMadrakTahsily" INTEGER,
    "NameMadrakTahsily" VARCHAR(50),
    "Olaviat" INTEGER,
    "CodeDisketDaraeeMadrak" INTEGER, PRIMARY KEY ("ccMadrakTahsily")
);

CREATE TABLE IF NOT EXISTS public."MaghtaeTahsily" (
    "ccMaghtaeTahsily" INTEGER,
    "NameMaghtaeTahsily" VARCHAR(50),
    "Olaviat" INTEGER,
    "CodeMaghtaeDaraee" INTEGER, PRIMARY KEY ("ccMaghtaeTahsily")
);

CREATE TABLE IF NOT EXISTS public."Mamoriat" (
    "ccMamoriat" INTEGER,
    "ccMarkazPakhshAz" INTEGER,
    "ccMarkazPakhshTa" INTEGER,
    "Sal" INTEGER,
    "Mah" INTEGER,
    "ccAfrad" INTEGER,
    "AzTarikh" TIMESTAMP,
    "TaTarikh" TIMESTAMP,
    "TedadRoozAddi" INTEGER,
    "TedadRoozTatil" INTEGER,
    "CodeVazeiat" INTEGER,
    "TarikhSabt" TIMESTAMP,
    "ccUser" INTEGER,
    "Elat" VARCHAR(255),
    "ccHokmeKarPMAfradErsal" INTEGER,
    "SharhMamoriat" VARCHAR(400),
    "ccMarkazPakhsh" INTEGER,
    "CodeNoe" INTEGER,
    "MahalMamoriat" VARCHAR(255),
    "NoeVasilehNaghlieh" VARCHAR(100),
    "ShomarehShahrbani" VARCHAR(20),
    "Masafat" INTEGER,
    "CodeVazeiatAnjam" INTEGER, PRIMARY KEY ("ccMamoriat")
);

CREATE TABLE IF NOT EXISTS public."MamoriatAfradTaeedKonandeh" (
    "ccMamoriatAfradTaeedKonandeh" INTEGER,
    "ccAfradModir" INTEGER,
    "ccAfradPersonel" INTEGER,
    "ccAfradModir1" INTEGER, PRIMARY KEY ("ccMamoriatAfradTaeedKonandeh")
);

CREATE TABLE IF NOT EXISTS public."MamoriatGozaresh" (
    "ccMamoriat" INTEGER,
    "ccMamoriatGozaresh" INTEGER,
    "MatneGozaresh" VARCHAR(-1), PRIMARY KEY ("ccMamoriatGozaresh")
);

CREATE TABLE IF NOT EXISTS public."MamoriatHazineh" (
    "ccMamoriat" INTEGER,
    "ccMamoriatHazineh" INTEGER,
    "ccHazineh" INTEGER,
    "ccArz" INTEGER,
    "Nerkh" DOUBLE PRECISION,
    "Meghdar" DOUBLE PRECISION,
    "Mablagh" DOUBLE PRECISION, PRIMARY KEY ("ccMamoriatHazineh")
);

CREATE TABLE IF NOT EXISTS public."MamoriatReport" (
    "ccMamoriat" INTEGER,
    "ccMamoriatReport" INTEGER,
    "AddressFile" VARCHAR(-1),
    "SharhFile" VARCHAR(100),
    "WebAddress" VARCHAR(-1),
    "ccAfrad" INTEGER,
    "AzTarikh" TIMESTAMP,
    "TaTarikh" TIMESTAMP, PRIMARY KEY ("ccMamoriatReport")
);

CREATE TABLE IF NOT EXISTS public."MamoriatVazeiat" (
    "ccMamoriat" INTEGER,
    "ccMamoriatVazeiat" INTEGER,
    "CodeVazeiat" INTEGER,
    "TarikhVazeiat" TIMESTAMP,
    "ccUser" INTEGER, PRIMARY KEY ("ccMamoriatVazeiat")
);

CREATE TABLE IF NOT EXISTS public."MandehMorkhasi" (
    "ccMandehMorkhasi" INTEGER,
    "ccAfrad" INTEGER,
    "TaTarikh" TIMESTAMP,
    "MandehRooz" INTEGER,
    "MandehSaat" INTEGER, PRIMARY KEY ("ccMandehMorkhasi")
);

CREATE TABLE IF NOT EXISTS public."Masir" (
    "ccMarkazPakhsh" INTEGER,
    "ccMasir" INTEGER,
    "NameMasir" VARCHAR(50), PRIMARY KEY ("ccMasir")
);

CREATE TABLE IF NOT EXISTS public."MasirSatr" (
    "ccMasir" INTEGER,
    "ccMasirSatr" INTEGER,
    "AzTarikh" TIMESTAMP,
    "Mablagh" DOUBLE PRECISION, PRIMARY KEY ("ccMasirSatr")
);

CREATE TABLE IF NOT EXISTS public."MohasebehMamoriat" (
    "ccMohasebehMamoriat" INTEGER,
    "ccMamoriat" INTEGER,
    "ccAfrad" INTEGER,
    "Sal" INTEGER,
    "Mah" INTEGER,
    "ccPost" INTEGER,
    "ccShoghl" INTEGER,
    "ccVahed" INTEGER,
    "NoeMamoriat" INTEGER,
    "NoePersonel" INTEGER,
    "NoeVasileh" INTEGER,
    "MajmooeDariafti" DOUBLE PRECISION,
    "Kilometer" INTEGER,
    "Masafat" INTEGER,
    "TedadMoshtary" INTEGER,
    "MablaghHoghogh" DOUBLE PRECISION,
    "MablaghMasir" DOUBLE PRECISION,
    "RaftBePaianeh" INTEGER,
    "BargashtBePaianeh" INTEGER,
    "RaftAzPaianeh" INTEGER,
    "BargashtAzPaianeh" INTEGER,
    "MablaghAiabZohabRaft" DOUBLE PRECISION,
    "MablaghAiabZohabBargasht" DOUBLE PRECISION,
    "MablaghMamoriat" DOUBLE PRECISION,
    "DarsadPardakhti" INTEGER,
    "SabtDarHoghoogh" TEXT, PRIMARY KEY ("ccMohasebehMamoriat")
);

CREATE TABLE IF NOT EXISTS public."Nahar" (
    "ccNahar" INTEGER,
    "FromDate" TIMESTAMP,
    "ccMarkazPakhsh" INTEGER,
    "MablaghNahar" DOUBLE PRECISION, PRIMARY KEY ("ccNahar")
);

CREATE TABLE IF NOT EXISTS public."NoeAgahie" (
    "ccNoeAgahie" INTEGER,
    "NameNoeAgahie" VARCHAR(50), PRIMARY KEY ("ccNoeAgahie")
);

CREATE TABLE IF NOT EXISTS public."NoeEnfesal" (
    "ccNoeEnfesal" INTEGER,
    "NameEnfesal" VARCHAR(50), PRIMARY KEY ("ccNoeEnfesal")
);

CREATE TABLE IF NOT EXISTS public."NoeEstekhdam" (
    "ccNoeEstekhdam" INTEGER,
    "NameNoeEstekhdam" VARCHAR(50), PRIMARY KEY ("ccNoeEstekhdam")
);

CREATE TABLE IF NOT EXISTS public."NoeHokm" (
    "ccNoeHokm" INTEGER,
    "OnvanHokm" VARCHAR(100),
    "CodeNoeHokm" INTEGER,
    "CodeNoeZamanHokm" INTEGER,
    "CodeVazeiatPersonel" INTEGER,
    "NoeHokm" INTEGER, PRIMARY KEY ("ccNoeHokm")
);

CREATE TABLE IF NOT EXISTS public."NoeKarmandYabi" (
    "ccNoeKarmandYabi" INTEGER,
    "NameNoeKarmandYabi" VARCHAR(50), PRIMARY KEY ("ccNoeKarmandYabi")
);

CREATE TABLE IF NOT EXISTS public."NoeKhadamatRefahi" (
    "ccNoeKhadamatRefahi" INTEGER,
    "NameNoeKhadamatRefahi" VARCHAR(50), PRIMARY KEY ("ccNoeKhadamatRefahi")
);

CREATE TABLE IF NOT EXISTS public."NoeMoafiat" (
    "ccNoeMoafiat" INTEGER,
    "NameNoeMoafiat" VARCHAR(50), PRIMARY KEY ("ccNoeMoafiat")
);

CREATE TABLE IF NOT EXISTS public."NoeVam" (
    "ccNoeVam" INTEGER,
    "NameVam" VARCHAR(50),
    "SaghfeMablagh" DOUBLE PRECISION,
    "Faal" TEXT,
    "NamaieshDarFishHoghogh" TEXT,
    "CodeItem" INTEGER,
    "CodeNoeSodorSanad" INTEGER,
    "ccCodeHesab" INTEGER,
    "ccCodeHesabBedehi" INTEGER,
    "CodeNoeSanadTafsily" INTEGER,
    "ccTafsily" INTEGER, PRIMARY KEY ("ccNoeVam")
);

CREATE TABLE IF NOT EXISTS public."NoeVamBazPardakht" (
    "ccNoeVam" INTEGER,
    "ccNoeVamBazPardakht" INTEGER,
    "TaHoghogh" DOUBLE PRECISION,
    "Tedad" INTEGER, PRIMARY KEY ("ccNoeVamBazPardakht")
);

CREATE TABLE IF NOT EXISTS public."NoeZaban" (
    "ccNoeZaban" INTEGER,
    "NameNoeZaban" VARCHAR(50), PRIMARY KEY ("ccNoeZaban")
);

CREATE TABLE IF NOT EXISTS public."Personel" (
    "ShomarehKart" INTEGER,
    "ccAfrad" INTEGER,
    "ccAfradModir" INTEGER,
    "CodeNoeModir" INTEGER,
    "TarikhEstekhdam" TIMESTAMP,
    "ShomarehBimeh" VARCHAR(20),
    "CodeVazeiatSarbazy" INTEGER,
    "TarikhShoroeSarbazy" TIMESTAMP,
    "TarikhPaianSarbazy" TIMESTAMP,
    "ModatZamanKhedmatSal" INTEGER,
    "ModatZamanKhedmat" INTEGER,
    "ccNoeMoafiat" INTEGER,
    "CodeVazeiatTaahol" INTEGER,
    "CodeNoeGovahinameh" INTEGER,
    "TarikhAkhzGovahinameh" TIMESTAMP,
    "ElateAdamAnjamMamoriat" VARCHAR(50),
    "NoeEtiad" VARCHAR(50),
    "ElateNaghsehOzv" VARCHAR(50),
    "HoghoghDarkhasty" DOUBLE PRECISION,
    "CodeVazeiat" INTEGER,
    "ccShobehBimeh" INTEGER,
    "ccShobehDaraee" INTEGER,
    "ShomarehPersonely" INTEGER,
    "ShomarehPersonelyOld" VARCHAR(15),
    "ccDinMazhab" INTEGER,
    "TarikhEbtalGovahinameh" TIMESTAMP,
    "TarikhEnfesal" TIMESTAMP,
    "TarikhKhatemeh" TIMESTAMP,
    "TarikhEtebarBimeh" TIMESTAMP,
    "TarikhPorseshNameh" TIMESTAMP,
    "TarikhDataEntry" TIMESTAMP,
    "ccNoeEnfesal" INTEGER,
    "ccDarkhastJazbNiro" INTEGER,
    "TarikhShoroBimeh" TIMESTAMP,
    "SabeghehBimeh" INTEGER,
    "MashmolGhanon" TEXT,
    "Janbaz" TEXT,
    "DarsadMoafiatBime" DOUBLE PRECISION,
    "DarsadMoafiatBimeKarfarma" DOUBLE PRECISION,
    "ShomarehHesab" VARCHAR(30),
    "ShomarehHesabNew" VARCHAR(30),
    "IsInListBank" TEXT,
    "ccMasir" INTEGER,
    "ccBank" INTEGER,
    "ccNoeHesab" INTEGER,
    "CodeShobeh" VARCHAR(20),
    "NameShobeh" VARCHAR(30),
    "TarikhEzdevaj" TIMESTAMP,
    "Meliat" VARCHAR(50),
    "ccGhaza" INTEGER,
    "Faal" INTEGER, PRIMARY KEY ("ccAfrad")
);

CREATE TABLE IF NOT EXISTS public."PersonelAddress" (
    "ccPersonelAddress" INTEGER,
    "ccAfrad" INTEGER,
    "ccAddress" INTEGER,
    "ccNoeAddress" INTEGER, PRIMARY KEY ("ccPersonelAddress")
);

CREATE TABLE IF NOT EXISTS public."PersonelAfradTakafol" (
    "ccPersonelAfradTakafol" INTEGER,
    "NameFamily" VARCHAR(50),
    "CodeNesbat" INTEGER,
    "Shoghl" VARCHAR(50),
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "ccAfrad" INTEGER,
    "TarikhTavalod" TIMESTAMP,
    "ShomarehBimeh" VARCHAR(20),
    "TarikhEtebarBimeh" TIMESTAMP,
    "ShomarehShenasnameh" VARCHAR(15), PRIMARY KEY ("ccPersonelAfradTakafol")
);

CREATE TABLE IF NOT EXISTS public."PersonelAmozesh" (
    "ccPersonelAmozesh" INTEGER,
    "ccAfrad" INTEGER,
    "ccOnvanDoreh" INTEGER,
    "TarikhEjra" TIMESTAMP,
    "JamSaat" DOUBLE PRECISION,
    "TedadVahed" INTEGER,
    "ccAmozeshgah" INTEGER,
    "MianginArziaby" DOUBLE PRECISION,
    "Govahi" TEXT,
    "Hazineh" DOUBLE PRECISION,
    "Mohtava" VARCHAR(250),
    "OlaviatDoreha" INTEGER,
    "EstandardGhereEstandard" INTEGER, PRIMARY KEY ("ccPersonelAmozesh")
);

CREATE TABLE IF NOT EXISTS public."PersonelAnbar" (
    "ccPersonelAnbar" INTEGER,
    "ccAfrad" INTEGER,
    "ccPost" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccGoroh" INTEGER,
    "ccShoghl" INTEGER, PRIMARY KEY ("ccPersonelAnbar")
);

CREATE TABLE IF NOT EXISTS public."PersoneleKelidi" (
    "ccPersoneleKelidi" INTEGER,
    "ccAfrad" INTEGER, PRIMARY KEY ("ccPersoneleKelidi")
);

CREATE TABLE IF NOT EXISTS public."PersonelEmtiazKeify" (
    "ccPersonelEmtiazKeify" INTEGER,
    "ccAfrad" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "Sal" INTEGER,
    "Mah" INTEGER,
    "EmtiazKeify" DOUBLE PRECISION, PRIMARY KEY ("ccPersonelEmtiazKeify")
);

CREATE TABLE IF NOT EXISTS public."PersonelEnfesalShobehBimeh" (
    "ccAfrad" INTEGER,
    "ccShobehBimeh" INTEGER,
    "TarikhEnfesal" TIMESTAMP,
    "ccPersonelHokmKargoziny" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccPost" INTEGER,
    "ccShoghl" INTEGER,
    "ShomarehPersonely" INTEGER,
    "ccUser" INTEGER,
    "Sal" INTEGER,
    "Mah" INTEGER, PRIMARY KEY ("ccAfrad", "ccShobehBimeh", "Sal", "Mah")
);

CREATE TABLE IF NOT EXISTS public."PersonelGharardadiBeRasmi" (
    "ccAfradGharardadiRasmi" INTEGER,
    "ccAfrad" INTEGER,
    "TedadDafaateTaghaza" INTEGER,
    "Taeed" TEXT,
    "TarikhAkharinTaghazaWithoutSlash" VARCHAR(8),
    "TarikhAkharinTaghaza" TIMESTAMP, PRIMARY KEY ("ccAfradGharardadiRasmi")
);

CREATE TABLE IF NOT EXISTS public."PersonelHokmKargoziny" (
    "ccAfrad" INTEGER,
    "ccPersonelHokmKargoziny" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccPost" INTEGER,
    "ccShoghl" INTEGER,
    "TarikhSodor" TIMESTAMP,
    "ShomarehHokm" VARCHAR(20),
    "SharhHokm" VARCHAR(600),
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(255),
    "CodeNoeEstekhdam" INTEGER,
    "ShHokm" INTEGER,
    "Paieh" INTEGER,
    "Rotbeh" INTEGER,
    "MablaghMozdeShoghl" DOUBLE PRECISION,
    "MablaghKhareBar" DOUBLE PRECISION,
    "MablaghMaskan" DOUBLE PRECISION,
    "MablaghHaghOlad" DOUBLE PRECISION,
    "MablaghHaghJazb" DOUBLE PRECISION,
    "MablaghHaghMasooliat" DOUBLE PRECISION,
    "MablaghSaierMazaia" DOUBLE PRECISION,
    "MablaghMozdeSanavat" DOUBLE PRECISION,
    "MablaghMozdeRotbeh" DOUBLE PRECISION,
    "MablaghHaghSarparasty" DOUBLE PRECISION,
    "MablaghHaghSharaietKar" DOUBLE PRECISION,
    "MablaghMandegaryHaghPost" DOUBLE PRECISION,
    "MablaghTaedilGhablAzTarh" DOUBLE PRECISION,
    "MablaghTafavotTatbigh" DOUBLE PRECISION,
    "MablaghBon" DOUBLE PRECISION,
    "CodeNoeVorod" INTEGER,
    "ccUser" INTEGER,
    "ccKarbar" INTEGER,
    "ccShobehBimeh" INTEGER,
    "ccShobehDaraee" INTEGER,
    "PayeHokm" INTEGER,
    "Hok_Date" VARCHAR(8),
    "Hok_Date_From" VARCHAR(8),
    "Hok_date_To" VARCHAR(8),
    "ccNoeHokm" VARCHAR(50),
    "ShamsiSodor" VARCHAR(10),
    "ShamsiDate" VARCHAR(10),
    "sematOld" VARCHAR(50), PRIMARY KEY ("ccPersonelHokmKargoziny")
);

CREATE TABLE IF NOT EXISTS public."PersonelHokmKargozinyBKBeforeDeletehokmgorohi" (
    "ccAfrad" INTEGER,
    "ccPersonelHokmKargoziny" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccPost" INTEGER,
    "ccShoghl" INTEGER,
    "TarikhSodor" TIMESTAMP,
    "ShomarehHokm" VARCHAR(20),
    "SharhHokm" VARCHAR(600),
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(255),
    "CodeNoeEstekhdam" INTEGER,
    "ShHokm" INTEGER,
    "Paieh" INTEGER,
    "Rotbeh" INTEGER,
    "MablaghMozdeShoghl" DOUBLE PRECISION,
    "MablaghKhareBar" DOUBLE PRECISION,
    "MablaghMaskan" DOUBLE PRECISION,
    "MablaghHaghOlad" DOUBLE PRECISION,
    "MablaghHaghJazb" DOUBLE PRECISION,
    "MablaghHaghMasooliat" DOUBLE PRECISION,
    "MablaghSaierMazaia" DOUBLE PRECISION,
    "MablaghMozdeSanavat" DOUBLE PRECISION,
    "MablaghMozdeRotbeh" DOUBLE PRECISION,
    "MablaghHaghSarparasty" DOUBLE PRECISION,
    "MablaghHaghSharaietKar" DOUBLE PRECISION,
    "MablaghMandegaryHaghPost" DOUBLE PRECISION,
    "MablaghTaedilGhablAzTarh" DOUBLE PRECISION,
    "MablaghTafavotTatbigh" DOUBLE PRECISION,
    "MablaghBon" DOUBLE PRECISION,
    "CodeNoeVorod" INTEGER,
    "ccUser" INTEGER,
    "ccKarbar" INTEGER,
    "ccShobehBimeh" INTEGER,
    "ccShobehDaraee" INTEGER,
    "PayeHokm" INTEGER,
    "Hok_Date" VARCHAR(8),
    "Hok_Date_From" VARCHAR(8),
    "Hok_date_To" VARCHAR(8),
    "ccNoeHokm" VARCHAR(50),
    "ShamsiSodor" VARCHAR(10),
    "ShamsiDate" VARCHAR(10),
    "sematOld" VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS public."PersonelHokmKargozinyNoe" (
    "ccPersonelHokmKargozinyNoe" INTEGER,
    "ccPersonelHokmKargoziny" INTEGER,
    "ccNoeHokm" INTEGER,
    "NoeHokm" INTEGER, PRIMARY KEY ("ccPersonelHokmKargozinyNoe")
);

CREATE TABLE IF NOT EXISTS public."PersonelHokmKargozinyNoeTest" (
    "ccPersonelHokmKargozinyNoe" INTEGER,
    "ccPersonelHokmKargoziny" INTEGER,
    "ccNoeHokm" INTEGER,
    "NoeHokm" INTEGER
);

CREATE TABLE IF NOT EXISTS public."PersonelHokmKargozinyTest" (
    "ccAfrad" INTEGER,
    "ccPersonelHokmKargoziny" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccPost" INTEGER,
    "ccShoghl" INTEGER,
    "TarikhSodor" TIMESTAMP,
    "ShomarehHokm" VARCHAR(20),
    "SharhHokm" VARCHAR(600),
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(255),
    "CodeNoeEstekhdam" INTEGER,
    "ShHokm" INTEGER,
    "Paieh" INTEGER,
    "Rotbeh" INTEGER,
    "MablaghMozdeShoghl" DOUBLE PRECISION,
    "MablaghKhareBar" DOUBLE PRECISION,
    "MablaghMaskan" DOUBLE PRECISION,
    "MablaghHaghOlad" DOUBLE PRECISION,
    "MablaghHaghJazb" DOUBLE PRECISION,
    "MablaghHaghMasooliat" DOUBLE PRECISION,
    "MablaghSaierMazaia" DOUBLE PRECISION,
    "MablaghMozdeSanavat" DOUBLE PRECISION,
    "MablaghMozdeRotbeh" DOUBLE PRECISION,
    "MablaghHaghSarparasty" DOUBLE PRECISION,
    "MablaghHaghSharaietKar" DOUBLE PRECISION,
    "MablaghMandegaryHaghPost" DOUBLE PRECISION,
    "MablaghTaedilGhablAzTarh" DOUBLE PRECISION,
    "MablaghTafavotTatbigh" DOUBLE PRECISION,
    "MablaghBon" DOUBLE PRECISION,
    "CodeNoeVorod" INTEGER,
    "ccUser" INTEGER,
    "ccKarbar" INTEGER,
    "ccShobehBimeh" INTEGER,
    "ccShobehDaraee" INTEGER,
    "PayeHokm" INTEGER,
    "Hok_Date" VARCHAR(8),
    "Hok_Date_From" VARCHAR(8),
    "Hok_date_To" VARCHAR(8),
    "ccNoeHokm" VARCHAR(50),
    "ShamsiSodor" VARCHAR(10),
    "ShamsiDate" VARCHAR(10),
    "sematOld" VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS public."PersonelHokmKargozinyTest70995" (
    "ccAfrad" INTEGER,
    "ccPersonelHokmKargoziny" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccPost" INTEGER,
    "ccShoghl" INTEGER,
    "TarikhSodor" TIMESTAMP,
    "ShomarehHokm" VARCHAR(20),
    "SharhHokm" VARCHAR(600),
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "Elat" VARCHAR(255),
    "CodeNoeEstekhdam" INTEGER,
    "ShHokm" INTEGER,
    "Paieh" INTEGER,
    "Rotbeh" INTEGER,
    "MablaghMozdeShoghl" DOUBLE PRECISION,
    "MablaghKhareBar" DOUBLE PRECISION,
    "MablaghMaskan" DOUBLE PRECISION,
    "MablaghHaghOlad" DOUBLE PRECISION,
    "MablaghHaghJazb" DOUBLE PRECISION,
    "MablaghHaghMasooliat" DOUBLE PRECISION,
    "MablaghSaierMazaia" DOUBLE PRECISION,
    "MablaghMozdeSanavat" DOUBLE PRECISION,
    "MablaghMozdeRotbeh" DOUBLE PRECISION,
    "MablaghHaghSarparasty" DOUBLE PRECISION,
    "MablaghHaghSharaietKar" DOUBLE PRECISION,
    "MablaghMandegaryHaghPost" DOUBLE PRECISION,
    "MablaghTaedilGhablAzTarh" DOUBLE PRECISION,
    "MablaghTafavotTatbigh" DOUBLE PRECISION,
    "MablaghBon" DOUBLE PRECISION,
    "CodeNoeVorod" INTEGER,
    "ccUser" INTEGER,
    "ccKarbar" INTEGER,
    "ccShobehBimeh" INTEGER,
    "ccShobehDaraee" INTEGER,
    "PayeHokm" INTEGER,
    "Hok_Date" VARCHAR(8),
    "Hok_Date_From" VARCHAR(8),
    "Hok_date_To" VARCHAR(8),
    "ccNoeHokm" VARCHAR(50),
    "ShamsiSodor" VARCHAR(10),
    "ShamsiDate" VARCHAR(10),
    "sematOld" VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS public."PersonelHokmKargozinyVazeiat" (
    "ccPersonelHokmKargoziny" INTEGER,
    "ccPersonelHokmKargozinyVazeiat" INTEGER,
    "CodeVazeiat" INTEGER,
    "TarikhVazeiat" TIMESTAMP,
    "ccUser" INTEGER, PRIMARY KEY ("ccPersonelHokmKargozinyVazeiat")
);

CREATE TABLE IF NOT EXISTS public."PersonelHokmKargozinyVazeiatTest" (
    "ccPersonelHokmKargoziny" INTEGER,
    "ccPersonelHokmKargozinyVazeiat" INTEGER,
    "CodeVazeiat" INTEGER,
    "TarikhVazeiat" TIMESTAMP,
    "ccUser" INTEGER
);

CREATE TABLE IF NOT EXISTS public."PersonelMadarekTahsily" (
    "ccAfrad" INTEGER,
    "ccAfradMadrakTahsily" INTEGER,
    "NameMoaseseh" VARCHAR(100),
    "ccMadrakTahsily" INTEGER,
    "ccMaghtaeTahsily" INTEGER,
    "ccReshtehGeraiesh" INTEGER,
    "TarikhAkhzMadrak" TIMESTAMP,
    "Moadel" DOUBLE PRECISION,
    "ccAddress" INTEGER, PRIMARY KEY ("ccAfradMadrakTahsily")
);

CREATE TABLE IF NOT EXISTS public."PersonelMadrak" (
    "ccAfrad" INTEGER,
    "ccPhoto" INTEGER,
    "ccNoePhoto" INTEGER, PRIMARY KEY ("ccAfrad", "ccPhoto")
);

CREATE TABLE IF NOT EXISTS public."PersonelMoaref" (
    "ccPersonelMoaref" INTEGER,
    "ccAfrad" INTEGER,
    "NameFamily" VARCHAR(50),
    "Telephone" VARCHAR(50),
    "Shoghl" VARCHAR(50),
    "ccAddress" INTEGER, PRIMARY KEY ("ccPersonelMoaref")
);

CREATE TABLE IF NOT EXISTS public."PersonelOzviatAnjoman" (
    "ccPersonelOzviatAnjoman" INTEGER,
    "NameAnjoman" VARCHAR(50),
    "NoeOzviat" VARCHAR(50),
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "ccAfrad" INTEGER, PRIMARY KEY ("ccPersonelOzviatAnjoman")
);

CREATE TABLE IF NOT EXISTS public."PersonelSanavat" (
    "ccAfrad" INTEGER,
    "ccPersonelSanavat" INTEGER,
    "TarikhTasvieh" TIMESTAMP,
    "Sal" INTEGER,
    "Mah" INTEGER,
    "Rooz" INTEGER,
    "MablaghTasvieh" DOUBLE PRECISION,
    "TedadRoozMohasebeh" INTEGER, PRIMARY KEY ("ccPersonelSanavat")
);

CREATE TABLE IF NOT EXISTS public."PersonelSanavatMorkhasi" (
    "ccPersonelSanavatMorkhasi" INTEGER,
    "ccAfrad" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "MablaghAvalDorehBeSaat" DOUBLE PRECISION,
    "MablaghAvalDorehBeDaghigheh" DOUBLE PRECISION,
    "MablaghSanavatBeSaat" DOUBLE PRECISION,
    "MablaghSanavatBeDaghigheh" DOUBLE PRECISION,
    "TaTarikh" TIMESTAMP,
    "ccPersonelHokmKargoziny" INTEGER, PRIMARY KEY ("ccPersonelSanavatMorkhasi")
);

CREATE TABLE IF NOT EXISTS public."PersonelSanavatZakhireh" (
    "ccPersonelSanavatZakhireh" INTEGER,
    "ccAfrad" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "Mablagh" DOUBLE PRECISION,
    "MablaghZakhireh" DOUBLE PRECISION,
    "TaTarikh" TIMESTAMP,
    "TedadRoozMohasebeh" INTEGER,
    "CodeNoeSanavat" INTEGER,
    "RoozKarkard" INTEGER,
    "RoozKarkardPersonelSanavat" INTEGER,
    "RoozKarkardTalabSanavat" INTEGER,
    "ccPersonelHokmKargoziny" INTEGER, PRIMARY KEY ("ccPersonelSanavatZakhireh")
);

CREATE TABLE IF NOT EXISTS public."PersonelSanavatZakhireh13961208" (
    "ccPersonelSanavatZakhireh" INTEGER,
    "ccAfrad" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "Mablagh" DOUBLE PRECISION,
    "MablaghZakhireh" DOUBLE PRECISION,
    "TaTarikh" TIMESTAMP,
    "TedadRoozMohasebeh" INTEGER,
    "CodeNoeSanavat" INTEGER,
    "RoozKarkard" INTEGER,
    "RoozKarkardPersonelSanavat" INTEGER,
    "RoozKarkardTalabSanavat" INTEGER,
    "ccPersonelHokmKargoziny" INTEGER
);

CREATE TABLE IF NOT EXISTS public."PersonelSavabeghKary" (
    "ccPersonelSavabeghKary" INTEGER,
    "NameMoasseseh" VARCHAR(50),
    "Telephone" VARCHAR(50),
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "Semat" VARCHAR(50),
    "Hoghogh" DOUBLE PRECISION,
    "ElatTarkKar" VARCHAR(50),
    "ccAfrad" INTEGER,
    "ccAddress" INTEGER, PRIMARY KEY ("ccPersonelSavabeghKary")
);

CREATE TABLE IF NOT EXISTS public."PersonelTamasZarory" (
    "ccPersonelTamasZarory" INTEGER,
    "NameFamily" VARCHAR(50),
    "Telephone" VARCHAR(50),
    "ccAfrad" INTEGER, PRIMARY KEY ("ccPersonelTamasZarory")
);

CREATE TABLE IF NOT EXISTS public."PersonelTashvighTanbih" (
    "ccPersonelTashvighTanbih" INTEGER,
    "ccAfrad" INTEGER,
    "CodeNoeNameh" INTEGER,
    "ShomarehNameh" VARCHAR(15),
    "TarikhNameh" TIMESTAMP,
    "Tozihat" VARCHAR(-1), PRIMARY KEY ("ccPersonelTashvighTanbih")
);

CREATE TABLE IF NOT EXISTS public."PersonelVabasteh" (
    "ccPersonelVabasteh" INTEGER,
    "NesbatPersonelVabasteh" VARCHAR(35),
    "ccAfrad" INTEGER,
    "NameFamily" VARCHAR(50), PRIMARY KEY ("ccPersonelVabasteh")
);

CREATE TABLE IF NOT EXISTS public."PersonelZaban" (
    "ccNoeZaban" INTEGER,
    "ccAfrad" INTEGER,
    "CodeSathMokalemeh" INTEGER,
    "CodeSathKhandan" INTEGER,
    "CodeSathNeveshtan" INTEGER, PRIMARY KEY ("ccAfrad", "ccNoeZaban")
);

CREATE TABLE IF NOT EXISTS public."Post" (
    "ccPost" INTEGER,
    "NamePost" VARCHAR(50),
    "Faal" TEXT,
    "ccGoroh" INTEGER,
    "ccPostLink" INTEGER,
    "Tedad" INTEGER,
    "EtelaatTakmily" VARCHAR(255),
    "ZamanehRasmi" INTEGER,
    "CodeTaminEjtemaee" VARCHAR(6),
    "SharhTaminEjtemaee" VARCHAR(50),
    "CodePost" INTEGER,
    "CodeDisketDaraee" INTEGER, PRIMARY KEY ("ccPost")
);

CREATE TABLE IF NOT EXISTS public."PostAfradDariaftKonandeh" (
    "ccPostAfradDariaftKonandeh" INTEGER,
    "ccPost" INTEGER, PRIMARY KEY ("ccPostAfradDariaftKonandeh")
);

CREATE TABLE IF NOT EXISTS public."PostDorehAmozesh" (
    "ccPost" INTEGER,
    "ccOnvanDoreh" INTEGER,
    "OlaviatDoreha" INTEGER, PRIMARY KEY ("ccPost", "ccOnvanDoreh")
);

CREATE TABLE IF NOT EXISTS public."PostShoghl" (
    "ccPost" INTEGER,
    "ccShoghl" INTEGER, PRIMARY KEY ("ccPost", "ccShoghl")
);

CREATE TABLE IF NOT EXISTS public."ReshtehGeraiesh" (
    "ccReshtehGeraiesh" INTEGER,
    "CodeNoeReshtehGeraiesh" INTEGER,
    "NameReshtehGeraiesh" VARCHAR(50),
    "ccReshtehGeraieshLink" INTEGER, PRIMARY KEY ("ccReshtehGeraiesh")
);

CREATE TABLE IF NOT EXISTS public."SharheMotammam" (
    "ccSharheMotammam" INTEGER,
    "OnvaneMotammam" VARCHAR(150),
    "NameSharheMotammam" VARCHAR(-1),
    "Olaviat" INTEGER,
    "Visible" TEXT, PRIMARY KEY ("ccSharheMotammam")
);

CREATE TABLE IF NOT EXISTS public."ShobehBimeh" (
    "ccShobehBimeh" INTEGER,
    "NameShobehBimeh" VARCHAR(50),
    "Faal" TEXT,
    "ShomarehKargah" VARCHAR(-1),
    "ccAddress" INTEGER,
    "ccMarkazPakhsh" INTEGER, PRIMARY KEY ("ccShobehBimeh")
);

CREATE TABLE IF NOT EXISTS public."ShobehDaraee" (
    "ccShobehDaraee" INTEGER,
    "NameShobehDaraee" VARCHAR(50), PRIMARY KEY ("ccShobehDaraee")
);

CREATE TABLE IF NOT EXISTS public."Shoghl" (
    "ccShoghl" INTEGER,
    "NameShoghl" VARCHAR(50),
    "ccGorohShoghl" INTEGER,
    "TarifeShoghl" VARCHAR(-1),
    "TedadNiaz" INTEGER,
    "HadeAghalEmtiaz" INTEGER,
    "Faal" TEXT,
    "ccGorohHoghoghy" INTEGER,
    "CodeShoghl" INTEGER, PRIMARY KEY ("ccShoghl")
);

CREATE TABLE IF NOT EXISTS public."Shoghl_Tamin" (
    "OPNO" VARCHAR(4),
    "JOB_UPDATE" VARCHAR(6),
    "JOB_CODE" VARCHAR(12),
    "JOB_DESC" VARCHAR(200),
    "JOB_TYPE1" VARCHAR(2),
    "JOB_TYPE2" VARCHAR(4)
);

CREATE TABLE IF NOT EXISTS public."ShoghlEhraz" (
    "ccShoghl" INTEGER,
    "ccShoghlEhrazNoe" INTEGER,
    "ccShoghlEhraz" INTEGER,
    "ShoghlEhraz" VARCHAR(350),
    "Emtiaz" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP, PRIMARY KEY ("ccShoghlEhraz")
);

CREATE TABLE IF NOT EXISTS public."ShoghlEhrazJensiat" (
    "ccShoghl" INTEGER,
    "ccShoghlEhrazJensiat" INTEGER,
    "CodeJensiat" INTEGER,
    "Emtiaz" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP, PRIMARY KEY ("ccShoghlEhrazJensiat")
);

CREATE TABLE IF NOT EXISTS public."ShoghlEhrazNoe" (
    "ccShoghlEhrazNoe" INTEGER,
    "ShoghlEhrazNoe" VARCHAR(50), PRIMARY KEY ("ccShoghlEhrazNoe")
);

CREATE TABLE IF NOT EXISTS public."ShoghlEhrazReshtehGeraiesh" (
    "ccShoghl" INTEGER,
    "ccShoghlEhrazReshtehGeraiesh" INTEGER,
    "ccMadrakTahsily" INTEGER,
    "ccMaghtaeTahsily" INTEGER,
    "ccReshtehGeraiesh" INTEGER,
    "Emtiaz" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP, PRIMARY KEY ("ccShoghlEhrazReshtehGeraiesh")
);

CREATE TABLE IF NOT EXISTS public."ShoghlEhrazSabegheh" (
    "ccShoghl" INTEGER,
    "ccShoghlEhrazSabegheh" INTEGER,
    "TaMah" INTEGER,
    "Emtiaz" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP, PRIMARY KEY ("ccShoghlEhrazSabegheh")
);

CREATE TABLE IF NOT EXISTS public."ShoghlEhrazSarparasty" (
    "ccShoghl" INTEGER,
    "ccShoghlEhrazSarparasty" INTEGER,
    "EmtiazMostaghim" INTEGER,
    "SaghfeEmtiazMostaghim" INTEGER,
    "EmtiazGheireMostaghim" INTEGER,
    "SaghfeGheireMostaghimEmtiaz" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP, PRIMARY KEY ("ccShoghlEhrazSarparasty")
);

CREATE TABLE IF NOT EXISTS public."ShoghlEhrazSen" (
    "ccShoghl" INTEGER,
    "ccShoghlEhrazSen" INTEGER,
    "TaSen" INTEGER,
    "Emtiaz" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP, PRIMARY KEY ("ccShoghlEhrazSen")
);

CREATE TABLE IF NOT EXISTS public."ShoghlSharh" (
    "ccShoghl" INTEGER,
    "ccShoghlSharhNoe" INTEGER,
    "ccShoghlSharh" INTEGER,
    "ShoghlSharh" VARCHAR(-1), PRIMARY KEY ("ccShoghlSharh")
);

CREATE TABLE IF NOT EXISTS public."ShoghlSharhNoe" (
    "ccShoghlSharhNoe" INTEGER,
    "ShoghlSharhNoe" VARCHAR(50), PRIMARY KEY ("ccShoghlSharhNoe")
);

CREATE TABLE IF NOT EXISTS public."ShoghlSoalatMosahebeh" (
    "ccShoghlSoalatMosahebeh" INTEGER,
    "ccShoghl" INTEGER,
    "SharhSoal" VARCHAR(350),
    "CodeNoeSoal" INTEGER,
    "Emtiaz" INTEGER, PRIMARY KEY ("ccShoghlSoalatMosahebeh")
);

CREATE TABLE IF NOT EXISTS public."SystemConfig" (
    "ccNoeEnfesalFot" INTEGER,
    "MohasebeHagheOlad_FS" INTEGER
);

CREATE TABLE IF NOT EXISTS public."vPersonelEnfesal" (
    "ccAfrad" INTEGER,
    "FNamePersonel" VARCHAR(50),
    "LNamePersonel" VARCHAR(50),
    "FullNamePersonel" VARCHAR(101),
    "ccAfradModir" INTEGER,
    "FName" VARCHAR(50),
    "LName" VARCHAR(50),
    "FullNameModir" VARCHAR(101),
    "ShomarehKart" INTEGER,
    "ShomarehBimeh" VARCHAR(20),
    "CodeJensiat" INTEGER,
    "txtJensiat" VARCHAR(3),
    "Email" VARCHAR(50),
    "Title" VARCHAR(50),
    "Telephone" VARCHAR(50),
    "Fax" VARCHAR(50),
    "Mobile" VARCHAR(50),
    "Dakhely" VARCHAR(5),
    "CodeMely" VARCHAR(15),
    "ShomarehShenasnameh" VARCHAR(15),
    "ccShahrTavalod" INTEGER,
    "ccShahrSodor" INTEGER,
    "TarikhTavalodWithoutSlash" VARCHAR(8),
    "TarikhTavalodWithSlash" VARCHAR(10),
    "NamePedar" VARCHAR(50),
    "TarikhFotWithoutSlash" VARCHAR(8),
    "TarikhSodorWithoutSlash" VARCHAR(8),
    "ccShobehBimeh" INTEGER,
    "CodeVazeiatSarbazy" INTEGER,
    "txtVazeiatSarbazy" VARCHAR(20),
    "TarikhPaianSarbazyWithoutSlash" VARCHAR(8),
    "ccNoeMoafiat" INTEGER,
    "CodeVazeiatTaahol" INTEGER,
    "txtVazeiatTaahol" VARCHAR(15),
    "CodeNoeGovahinameh" INTEGER,
    "TarikhAkhzGovahiNamehWithoutSlash" VARCHAR(8),
    "ElateAdamAnjamMamoriat" VARCHAR(50),
    "NoeEtiad" VARCHAR(50),
    "ElateNaghsehOzv" VARCHAR(50),
    "HoghoghDarkhasty" DOUBLE PRECISION,
    "CodeVazeiat" INTEGER,
    "txtVazeiat" VARCHAR(20),
    "ShomarehPersonely" INTEGER,
    "TarikhEstekhdamWithoutSlash" VARCHAR(8),
    "TarikhEstekhdamWithSlash" VARCHAR(10),
    "TarikhEstekhdam" TIMESTAMP,
    "TarikhPaianSarbazy" TIMESTAMP,
    "TarikhAkhzGovahinameh" TIMESTAMP,
    "TarikhTavalod" TIMESTAMP,
    "TarikhSodor" TIMESTAMP,
    "TarikhFot" TIMESTAMP,
    "ShomarehPersonelyOld" VARCHAR(15),
    "ccShahrestanTavalod" INTEGER,
    "ccOstanTavalod" INTEGER,
    "ccShahrestanSodor" INTEGER,
    "ccOstanSodor" INTEGER,
    "ccDinMazhab" INTEGER,
    "TarikhEbtalGovahiNamehWithoutSlash" VARCHAR(8),
    "TarikhEbtalGovahinameh" TIMESTAMP,
    "TarikhEnfesalWithoutSlash" VARCHAR(8),
    "TarikhEnfesal" TIMESTAMP,
    "TarikhEtebarBimeh" TIMESTAMP,
    "TarikhEtebarBimehWithoutSlash" VARCHAR(8),
    "TarikhPorseshNameh" TIMESTAMP,
    "TarikhPorseshNamehWithoutSlash" VARCHAR(8),
    "TarikhDataEntry" TIMESTAMP,
    "TarikhDataEntryWithoutSlash" VARCHAR(8),
    "ccNoeEnfesal" INTEGER,
    "NameEnfesal" VARCHAR(50),
    "ccDarkhastJazbNiro" INTEGER,
    "ccAfradDarkhastKonandeh" INTEGER,
    "TarikhShoroBimeh" TIMESTAMP,
    "TarikhShoroBimehWithoutSlash" VARCHAR(8),
    "SabeghehBimeh" INTEGER,
    "MashmolGhanon" TEXT,
    "Janbaz" TEXT,
    "ShomarehHesab" VARCHAR(30),
    "ccMasir" INTEGER,
    "ccShobehDaraee" INTEGER,
    "ccMarkazPakhshMasir" INTEGER,
    "ccBank" INTEGER,
    "NameBank" VARCHAR(50),
    "ccNoeHesab" INTEGER,
    "NameNoeHesab" VARCHAR(50),
    "CodeShobeh" VARCHAR(20),
    "Faal" TEXT,
    "TarikhEzdevaj" TIMESTAMP,
    "TarikhEzdevajWithoutSlash" VARCHAR(8),
    "MahalTavalod" VARCHAR(50),
    "MahalSodor" VARCHAR(50),
    "NameShobeh" VARCHAR(30),
    "TarikhAkhzMadrak" TIMESTAMP,
    "DarsadMoafiatBime" DOUBLE PRECISION,
    "DarsadMoafiatBimeKarfarma" DOUBLE PRECISION,
    "TarikhShoroeSarbazyWithoutSlash" VARCHAR(8),
    "TarikhShoroeSarbazy" TIMESTAMP,
    "ModatZamanKhedmat" INTEGER,
    "ModatZamanKhedmatSal" INTEGER,
    "IsInListBank" TEXT,
    "TarikhKhatemehWithoutSlash" VARCHAR(8),
    "TarikhKhatemeh" TIMESTAMP,
    "ShomarehHesabNew" VARCHAR(30),
    "Meliat" VARCHAR(50),
    "ccGhaza" INTEGER,
    "Expr1" INTEGER
);