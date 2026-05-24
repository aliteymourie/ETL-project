CREATE TABLE IF NOT EXISTS public."Amval" (
    "ccAmval" INTEGER,
    "ShomarehAmval" INTEGER,
    "ShomarehAmvalOld" VARCHAR(20),
    "NameAmval" VARCHAR(256),
    "Tarikh" TIMESTAMP,
    "TarikhBahrehbardary" TIMESTAMP,
    "GheymatTamamShodeh" DOUBLE PRECISION,
    "ArzeshDaftary" DOUBLE PRECISION,
    "EstehlakAnbashteh" DOUBLE PRECISION,
    "ZakhirehArzesh" DOUBLE PRECISION,
    "SaghfArzeshDaftary" DOUBLE PRECISION,
    "ccJamdar" INTEGER,
    "ccGorohDaraee" INTEGER,
    "ccProject" INTEGER,
    "CodeVazeiat" INTEGER,
    "ccKalaMalzomat" INTEGER,
    "ccAfradJamdar" INTEGER,
    "TarikhKharid" TIMESTAMP,
    "ccKardexSatrR" INTEGER,
    "ccKardexSatrH" INTEGER,
    "ccGorohDaraeePM" INTEGER,
    "ArzeshEsghat" DOUBLE PRECISION,
    "EstehlakAnbashtehConvert" DOUBLE PRECISION,
    "ArzeshDaftaryConvert" DOUBLE PRECISION,
    "GheymatTamamShodehAvalDoreh" DOUBLE PRECISION,
    "ArzeshDaftaryAvalDoreh" DOUBLE PRECISION,
    "EstehlakAnbashtehAvalDoreh" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "ArzeshDaftaryEslah" DOUBLE PRECISION,
    "EstehlakAnbashtehEslah" DOUBLE PRECISION,
    "ShomarehPelak" INTEGER,
    "Tozihat" VARCHAR(-1), PRIMARY KEY ("ccAmval")
);

CREATE TABLE IF NOT EXISTS public."Amval13961026" (
    "ccAmval" INTEGER,
    "ShomarehAmval" INTEGER,
    "ShomarehAmvalOld" VARCHAR(20),
    "NameAmval" VARCHAR(256),
    "Tarikh" TIMESTAMP,
    "TarikhBahrehbardary" TIMESTAMP,
    "GheymatTamamShodeh" DOUBLE PRECISION,
    "ArzeshDaftary" DOUBLE PRECISION,
    "EstehlakAnbashteh" DOUBLE PRECISION,
    "ZakhirehArzesh" DOUBLE PRECISION,
    "SaghfArzeshDaftary" DOUBLE PRECISION,
    "ccJamdar" INTEGER,
    "ccGorohDaraee" INTEGER,
    "ccProject" INTEGER,
    "CodeVazeiat" INTEGER,
    "ccKalaMalzomat" INTEGER,
    "ccAfradJamdar" INTEGER,
    "TarikhKharid" TIMESTAMP,
    "ccKardexSatrR" INTEGER,
    "ccKardexSatrH" INTEGER,
    "ccGorohDaraeePM" INTEGER,
    "ArzeshEsghat" DOUBLE PRECISION,
    "EstehlakAnbashtehConvert" DOUBLE PRECISION,
    "ArzeshDaftaryConvert" DOUBLE PRECISION,
    "GheymatTamamShodehAvalDoreh" DOUBLE PRECISION,
    "ArzeshDaftaryAvalDoreh" DOUBLE PRECISION,
    "EstehlakAnbashtehAvalDoreh" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "ArzeshDaftaryEslah" DOUBLE PRECISION,
    "EstehlakAnbashtehEslah" DOUBLE PRECISION,
    "ShomarehPelak" INTEGER,
    "Tozihat" VARCHAR(-1)
);

CREATE TABLE IF NOT EXISTS public."AmvalAjza" (
    "ccAmval" INTEGER,
    "ccAmvalAjza" INTEGER,
    "ccGorohDaraeePM" INTEGER,
    "ccAmvalAjzaPedar" INTEGER,
    "ShomarehAmval" INTEGER,
    "Tozihat" VARCHAR(50),
    "TarikhEtmamGaranti" TIMESTAMP,
    "Hazineh" DOUBLE PRECISION,
    "IsMojod" INTEGER,
    "TarikhBahrehbardary" TIMESTAMP,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccAmvalAjza")
);

CREATE TABLE IF NOT EXISTS public."AmvalAjzaMoshakhase" (
    "ccAmvalAjzaMoshakhaseh" INTEGER,
    "ccAmvalAjza" INTEGER,
    "ccGorohDaraeeAttributes" INTEGER,
    "Meghdar" VARCHAR(100),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccAmvalAjzaMoshakhaseh")
);

CREATE TABLE IF NOT EXISTS public."AmvalBelaEstefadeh" (
    "ccAmval" INTEGER,
    "ccAmvalBelaEstefadeh" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "Tozihat" VARCHAR(200),
    "ccLocation" INTEGER,
    "ArzeshDaftary" DOUBLE PRECISION,
    "ccGoroh" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccAmvalBelaEstefadeh")
);

CREATE TABLE IF NOT EXISTS public."AmvalGuarantee" (
    "ccAmval" INTEGER,
    "TarikhEtmamGuarantee" TIMESTAMP,
    "kiloometr" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccAmval")
);

CREATE TABLE IF NOT EXISTS public."AmvalJabejaee" (
    "ccAmval" INTEGER,
    "ccAmvalJabejaee" INTEGER,
    "ccLocation" INTEGER,
    "ccGoroh" INTEGER,
    "FromDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "ccAfrad" INTEGER,
    "Elat" VARCHAR(200),
    "ArzeshDaftary" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccAmvalJabejaee")
);

CREATE TABLE IF NOT EXISTS public."AmvalJabejaee13961026" (
    "ccAmval" INTEGER,
    "ccAmvalJabejaee" INTEGER,
    "ccLocation" INTEGER,
    "ccGoroh" INTEGER,
    "FromDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "ccAfrad" INTEGER,
    "Elat" VARCHAR(200),
    "ArzeshDaftary" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public."AmvalJabejaeeBK" (
    "ccAmval" INTEGER,
    "ccAmvalJabejaee" INTEGER,
    "ccLocation" INTEGER,
    "ccGoroh" INTEGER,
    "FromDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "ccAfrad" INTEGER,
    "Elat" VARCHAR(200),
    "ArzeshDaftary" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public."AmvalMoshakhaseh" (
    "ccAmvalMoshakhaseh" INTEGER,
    "ccAmval" INTEGER,
    "ccGorohDaraeeAttributes" INTEGER,
    "Meghdar" VARCHAR(100),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccAmvalMoshakhaseh")
);

CREATE TABLE IF NOT EXISTS public."AmvalTaghirArzesh" (
    "ccAmval" INTEGER,
    "ccAmvalTaghirArzesh" INTEGER,
    "Gheymat" DOUBLE PRECISION,
    "Sharh" VARCHAR(100),
    "Tarikh" TIMESTAMP,
    "CodeNoeTaghirArzesh" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccAmvalTaghirArzesh")
);

CREATE TABLE IF NOT EXISTS public."Bimeh" (
    "ccBimeh" INTEGER,
    "Sharh" VARCHAR(100),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccBimeh")
);

CREATE TABLE IF NOT EXISTS public."BimehAmval" (
    "ccBimehAmval" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "ccNoeBimeh" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccBimehNamaiandegy" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccBimehAmval")
);

CREATE TABLE IF NOT EXISTS public."BimehAmvalSatr" (
    "ccBimehAmvalSatr" INTEGER,
    "ccBimehAmval" INTEGER,
    "ccAmval" INTEGER,
    "SharhBimeh" VARCHAR(200),
    "ArzeshBimeh" DOUBLE PRECISION,
    "NerkhBimeh" DOUBLE PRECISION,
    "ShomareBimenameh" VARCHAR(100),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccBimehAmvalSatr")
);

CREATE TABLE IF NOT EXISTS public."BimehNamaiandegy" (
    "ccBimeh" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccBimehNamaiandegy" INTEGER,
    "Telephone" VARCHAR(50),
    "Fax" VARCHAR(50),
    "ccAddress" INTEGER,
    "CodeNamaiandegy" VARCHAR(10),
    "NameNamaiandegy" VARCHAR(50),
    "TeleConnection" VARCHAR(50),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccBimehNamaiandegy")
);

CREATE TABLE IF NOT EXISTS public."EhdaAmval" (
    "ccAmval" INTEGER,
    "ccEhdaAmval" INTEGER,
    "ccLocation" INTEGER,
    "ccGoroh" INTEGER,
    "ArzeshDaftary" DOUBLE PRECISION,
    "TarikhEhda" TIMESTAMP,
    "ccTafsily" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccEhdaAmval")
);

CREATE TABLE IF NOT EXISTS public."EnteghalAmvalAz" (
    "ccEnteghalAmvalAz" INTEGER,
    "ccAmval" INTEGER,
    "ccSherkat" INTEGER,
    "ccLocation" INTEGER,
    "ArzeshDaftary" DOUBLE PRECISION,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "ccGoroh" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccEnteghalAmvalAz")
);

CREATE TABLE IF NOT EXISTS public."EnteghalAmvalBe" (
    "ccEnteghalAmvalBe" INTEGER,
    "ccAmval" INTEGER,
    "ccSherkat" INTEGER,
    "ccLocation" INTEGER,
    "FromDate" TIMESTAMP,
    "EndDate" TIMESTAMP,
    "ccGoroh" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccEnteghalAmvalBe")
);

CREATE TABLE IF NOT EXISTS public."EsghatAmval" (
    "ccEsghatAmval" INTEGER,
    "ccAmval" INTEGER,
    "Tarikh" TIMESTAMP,
    "MablaghEsghat" DOUBLE PRECISION,
    "ccLocation" INTEGER,
    "ccGoroh" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccEsghatAmval")
);

CREATE TABLE IF NOT EXISTS public."EtleateTakmilyAmval" (
    "ccAmval" INTEGER,
    "Field01" VARCHAR(50),
    "Field02" VARCHAR(50),
    "Field03" VARCHAR(50),
    "Field04" VARCHAR(50),
    "Field05" VARCHAR(50),
    "ccNoeField" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccAmval")
);

CREATE TABLE IF NOT EXISTS public."ForoshAmval" (
    "ccMarkazPakhsh" INTEGER,
    "ccForoshAmval" INTEGER,
    "ShomarehForm" INTEGER,
    "TarikhForm" TIMESTAMP,
    "HazinehForosh" DOUBLE PRECISION,
    "Sepordeh" DOUBLE PRECISION,
    "ccTafsily" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccForoshAmval")
);

CREATE TABLE IF NOT EXISTS public."ForoshAmvalSatr" (
    "ccForoshAmval" INTEGER,
    "ccForoshAmvalSatr" INTEGER,
    "ccAmval" INTEGER,
    "ArzeshDaftary" DOUBLE PRECISION,
    "Gheymat" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccForoshAmvalSatr")
);

CREATE TABLE IF NOT EXISTS public."Ghavanin" (
    "ccGorohGhavanin" INTEGER,
    "ccGhavanin" INTEGER,
    "Shomareh" INTEGER,
    "Sharh" VARCHAR(100),
    "Ravesh" INTEGER,
    "Nerkh" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccGhavanin")
);

CREATE TABLE IF NOT EXISTS public."GhavaninGoroh" (
    "ccGorohGhavanin" INTEGER,
    "Code" INTEGER,
    "Sharh" VARCHAR(100),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccGorohGhavanin")
);

CREATE TABLE IF NOT EXISTS public."GorohAslyDaraee" (
    "ccGorohAslyDaraee" INTEGER,
    "NameGorohAslyDaraee" VARCHAR(50),
    "ccCodeHesabEstehlak" INTEGER,
    "ccCodeHesabZakhirehEstehlak" INTEGER,
    "ccCodeHesabDaraee" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccGorohAslyDaraee")
);

CREATE TABLE IF NOT EXISTS public."GorohAslyDaraeeAttributes" (
    "ccGorohAslyDaraeeAttributes" INTEGER,
    "Name" VARCHAR(100),
    "ccGorohAslyDaraee" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccGorohAslyDaraeeAttributes")
);

CREATE TABLE IF NOT EXISTS public."GorohDaraee" (
    "ccGorohDaraee" INTEGER,
    "Sharh" VARCHAR(50),
    "Ravesh" INTEGER,
    "Nerkh" DOUBLE PRECISION,
    "ccGorohAslyDaraee" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccGorohDaraee")
);

CREATE TABLE IF NOT EXISTS public."GorohDaraeeAttributes" (
    "ccGorohDaraeeAttributes" INTEGER,
    "Name" VARCHAR(100),
    "ccGorohDaraee" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccGorohDaraeeAttributes")
);

CREATE TABLE IF NOT EXISTS public."GorohDaraeeRaveshNerkh" (
    "ccGorohDaraeeRaveshNerkh" INTEGER,
    "ccGorohDaraee" INTEGER,
    "FromDate" TIMESTAMP,
    "Ravesh" INTEGER,
    "Nerkh" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccGorohDaraeeRaveshNerkh")
);

CREATE TABLE IF NOT EXISTS public."JamDar" (
    "ccMarkazPakhsh" INTEGER,
    "ccJamDar" INTEGER,
    "ccAfrad" INTEGER,
    "SharhJamDar" VARCHAR(20),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccJamDar")
);

CREATE TABLE IF NOT EXISTS public."Kharidaran" (
    "ccKharidaran" INTEGER,
    "FName" VARCHAR(50),
    "Lname" VARCHAR(50),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccKharidaran")
);

CREATE TABLE IF NOT EXISTS public."Location" (
    "ccMarkazPakhsh" INTEGER,
    "ccLocation" INTEGER,
    "NameLocation" VARCHAR(50),
    "ccLocationLink" INTEGER,
    "Metr" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccLocation")
);

CREATE TABLE IF NOT EXISTS public."LocationSatr" (
    "ccLocation" INTEGER,
    "ccGoroh" INTEGER,
    "Metr" DOUBLE PRECISION,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "CodeVazeiat" INTEGER,
    "Noe" INTEGER, PRIMARY KEY ("ccLocation", "ccGoroh")
);

CREATE TABLE IF NOT EXISTS public."MohasbehEstehlakTitr" (
    "ccMohasbehEstehlakTitr" INTEGER,
    "ccAmval" INTEGER,
    "Sal" INTEGER,
    "Mah" INTEGER,
    "Tarikh" TIMESTAMP,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "CodeNoeMohasebeh" INTEGER, PRIMARY KEY ("ccMohasbehEstehlakTitr", "Sal")
);

CREATE TABLE IF NOT EXISTS public."MohsebehEstehlak" (
    "ccMohsebehEstehlak" INTEGER,
    "ccAmval" INTEGER,
    "TarikhBahrehbardary" TIMESTAMP,
    "TarikhMohasebeh" TIMESTAMP,
    "Sal" INTEGER,
    "Mah" INTEGER,
    "Rooz" INTEGER,
    "ccGorohDaraee" INTEGER,
    "Ravesh" INTEGER,
    "Nerkh" DOUBLE PRECISION,
    "ccGorohAslyDaraee" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "ccLocation" INTEGER,
    "ccGoroh" INTEGER,
    "ccAfradTahvilGirandeh" INTEGER,
    "GheymatTamamShodeh" DOUBLE PRECISION,
    "ArzeshEsghat" DOUBLE PRECISION,
    "Estehlak" DOUBLE PRECISION,
    "ArzeshDaftary" DOUBLE PRECISION,
    "EstehlakAnbashteh" DOUBLE PRECISION,
    "ccJamdar" INTEGER,
    "ccAfradJamdar" INTEGER,
    "ccProject" INTEGER,
    "ccMohasbehEstehlakTitr" INTEGER,
    "AzTarikh" TIMESTAMP,
    "TaTarikh" TIMESTAMP,
    "CodeVazeiatSanadEstehlak" INTEGER,
    "ccSanad" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP,
    "CodeNoeMohasebeh" INTEGER, PRIMARY KEY ("ccMohsebehEstehlak", "Sal")
);

CREATE TABLE IF NOT EXISTS public."MohsebehEstehlakSanad" (
    "ccMohsebehEstehlakSanad" INTEGER,
    "ccMarkazPakhsh" INTEGER,
    "Sal" INTEGER,
    "Mah" INTEGER,
    "ccGoroh" INTEGER,
    "ccGorohAslyDaraee" INTEGER,
    "CodeNoeMohasebeh" INTEGER,
    "ccSanad" INTEGER,
    "tSal" INTEGER, PRIMARY KEY ("ccMohsebehEstehlakSanad")
);

CREATE TABLE IF NOT EXISTS public."NoeBimeh" (
    "ccNoeBimeh" INTEGER,
    "Sharh" VARCHAR(100),
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccNoeBimeh")
);

CREATE TABLE IF NOT EXISTS public."Project" (
    "ccProject" INTEGER,
    "NameProject" VARCHAR(50),
    "TarikhShoro" TIMESTAMP,
    "TarikhPaian" TIMESTAMP,
    "ModirProject" VARCHAR(20),
    "Faal" TEXT,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccProject")
);

CREATE TABLE IF NOT EXISTS public."TaadilAmval" (
    "ccTaadilAmval" INTEGER,
    "ccAmval" INTEGER,
    "Tarikh" TIMESTAMP,
    "MablaghTaadil" DOUBLE PRECISION,
    "ccLocation" INTEGER,
    "ccGoroh" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccTaadilAmval")
);

CREATE TABLE IF NOT EXISTS public."TabaghehBandyAmval" (
    "Tozihat" VARCHAR(200),
    "ccTabaghehBandyAmval" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccTabaghehBandyAmval")
);

CREATE TABLE IF NOT EXISTS public."TabaghehBandyAmvalSatr" (
    "ccAmval" INTEGER,
    "ccTabaghehBandyAmval" INTEGER,
    "TarikhEntry" TIMESTAMP,
    "ModifiedDate" TIMESTAMP, PRIMARY KEY ("ccTabaghehBandyAmval", "ccAmval")
);

CREATE TABLE IF NOT EXISTS public."vAmvalJabejaeeOld" (
    "ccAmval" INTEGER,
    "NameAmval" VARCHAR(256),
    "ccAmvalJabejaee" INTEGER,
    "ccLocation" INTEGER,
    "NameLocation" VARCHAR(50),
    "ccGoroh" INTEGER,
    "NameGoroh" VARCHAR(50),
    "FromDate" TIMESTAMP,
    "FromDateWithoutSlash" VARCHAR(8),
    "FromDateWithSlash" VARCHAR(10),
    "ccMarkazPakhsh" INTEGER,
    "CodeVazeiat" INTEGER,
    "NameMarkazPakhsh" VARCHAR(50),
    "FullNameTahvilGirandeh" VARCHAR(100),
    "ccAfrad" INTEGER,
    "Setad" TEXT,
    "ArzeshDaftary" DOUBLE PRECISION,
    "ShomarehAmval" INTEGER,
    "Metr" DOUBLE PRECISION,
    "ShomarehAmvalOld" VARCHAR(20),
    "Elat" VARCHAR(200),
    "ccAfradJamdar" INTEGER,
    "ccAfradTahvilGirandeh" INTEGER
);