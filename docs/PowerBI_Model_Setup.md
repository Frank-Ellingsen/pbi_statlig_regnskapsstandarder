# Power BI Stjernemodell & DAX Målbibliotek

## 1. Import & Datatyper
Alle CSV-filer er definert med semikolon (`;`) som skilletegn og UTF-8 tegnsett.
*   **Datatyper**: `DatoNokkel` er heltall (Int64) i samtlige tabeller. Beløp (`Belop_signert`, `BudsjettBelop`, `ForecastBelop`, `Tiltakseffekt`, `Debet`, `Kredit`) er desimaltall (valuta). `Aarsverk` og `Studiepoeng` er desimaltall.
*   **M-spørringer**: Samtlige tabeller bruker parameteren `#"DataFolder"` som peker på den lokale data-mappen (`data/`).

---

## 2. Stjernemodell & Relasjoner
Det er etablert 19 aktive en-til-mange (`1:*`) relasjoner med enkel filtreringsretning (`single direction`) fra dimensjoner til faktatabeller:
*   Ingen toveis filtrering (`crossFilterDirection: both`) benyttes for å unngå tvetydighet og ytelsestap.
*   Alle faktatabeller (`FactGL`, `FactBudget`, `FactForecast`, `FactFTE`, `FactStudyPoints`) filtreres rent av felles dimensjoner (`DimDate`, `DimOrganization`, `DimAccount`, `DimProject`, `DimPositionGroup`, `DimStudyProgram`, `DimForecastVersion`).

---

## 3. Hierarkier
Følgende 5 drill-down hierarkier er etablert i TMDL-modellen:
1.  **`UiA organisasjon`** (`DimOrganization`): `OrgNavn` > `Instituttnavn` > `Koststednavn`
2.  **`Kontohierarki`** (`DimAccount`): `SRS_regnskapslinje` > `Kontotype` > `Kontonavn` > `Konto`
3.  **`Prosjekthierarki`** (`DimProject`): `Finansieringstype` > `Finansieringskilde` > `Prosjektkategori` > `Prosjektnavn`
4.  **`Studie`** (`DimStudyProgram`): `Studienivaa` > `Studieprogramnavn`
5.  **`Tid`** (`DimDate`): `Aar` > `Kvartal` > `Maaned` > `Dato`

---

## 4. DAX Målbibliotek (50 Mål i 8 Mapper)

Målene er plassert i den dedikerte måltabellen `_Measures` og strukturert i 8 nummererte mapper:

### 01 Faktisk (Actuals / FactGL)
*   `Faktisk belop`: `SUM(FactGL[Belop_signert])` - Netto bokført beløp (Debet - Kredit).
*   `Faktisk debet`: `SUM(FactGL[Debet])` - Samlet debet (kostnader).
*   `Faktisk kredit`: `SUM(FactGL[Kredit])` - Samlet kredit (inntekter).
*   `Faktisk inntekter`: `CALCULATE(-[Faktisk belop], DimAccount[Kontotype] = "Inntekt")` - Inntekter vendt til positivt fortegn.
*   `Faktisk kostnader`: `CALCULATE([Faktisk belop], DimAccount[Kontotype] = "Kostnad")` - Kostnader med positivt fortegn.
*   `Faktisk lonnskostnader`: `CALCULATE([Faktisk belop], DimAccount[SRS_regnskapslinje] = "Lonnskostnader")`.
*   `Faktisk driftskostnader`: `CALCULATE([Faktisk belop], DimAccount[SRS_regnskapslinje] = "Andre driftskostnader")`.
*   `Faktisk avskrivninger`: `CALCULATE([Faktisk belop], DimAccount[SRS_regnskapslinje] = "Avskrivninger")`.
*   `Faktisk BOA inntekter`: `CALCULATE([Faktisk inntekter], DimProject[Finansieringstype] IN { "Bidrag", "Oppdrag" })`.
*   `Faktisk BOA andel %`: `DIVIDE([Faktisk BOA inntekter], [Faktisk inntekter])`.
*   `Faktisk lonn per aarsverk`: `DIVIDE([Faktisk lonnskostnader], [Aarsverk])`.
*   `Faktisk kostnad per SPE60`: `DIVIDE([Faktisk kostnader], [SPE 60])`.
*   `Faktisk YTD`: `TOTALYTD([Faktisk belop], DimDate[Dato])`.
*   `Faktisk inntekter YTD`: `TOTALYTD([Faktisk inntekter], DimDate[Dato])`.
*   `Faktisk kostnader YTD`: `TOTALYTD([Faktisk kostnader], DimDate[Dato])`.

### 02 Budsjett (Budget / FactBudget & BAC)
*   `Budsjett`: `SUM(FactBudget[BudsjettBelop])`.
*   `Budsjett inntekter`: Budsjetterte inntekter snudd til positivt fortegn.
*   `Budsjett kostnader`: Budsjetterte kostnader (Debet).
*   `Budsjett lonnskostnader`: Budsjetterte personalkostnader.
*   `Budsjett lonn per aarsverk`: `DIVIDE([Budsjett lonnskostnader], [Aarsverk])`.
*   `Budsjett YTD`: `TOTALYTD([Budsjett], DimDate[Dato])`.
*   `Aarsbudsjett`: Budsjett fjernet for månedskontekst via `REMOVEFILTERS(DimDate)`.
*   `BAC (Budget at Completion)`: Prosjektledelses- og EVM-mål: `[Aarsbudsjett]`.

### 03 Forecast & LE (Prognoser, EAC & ETC)
*   `Forecast belop`: `SUM(FactForecast[ForecastBelop])`.
*   `Tiltakseffekt`: `SUM(FactForecast[Tiltakseffekt])`.
*   `Forecast etter tiltak`: `[Forecast belop] + [Tiltakseffekt]`.
*   `Valgt forecastversjon`: `SELECTEDVALUE(DimForecastVersion[Versjon], "LE_2026")`.
*   `Gjeldende forecast`: Dynamisk forecast filtrert på aktiv versjon (standard `LE_2026`).
*   `Gjeldende forecast etter tiltak`: Dynamisk forecast inkludert innsparingstiltak.
*   `Forecast aarsbelop`: Helårsprognose via `REMOVEFILTERS(DimDate)`.
*   `EAC (Estimate at Completion)`: Prosjektledelses- og EVM-mål: `[Forecast aarsbelop]`.
*   `Forecast YTD`: `TOTALYTD([Gjeldende forecast], DimDate[Dato])`.
*   `Forecast restaar`: `[Forecast aarsbelop] - [Forecast YTD]`.
*   `ETC (Estimate to Complete)`: Prosjektledelses- og EVM-mål: `[Forecast restaar]`.
*   `Latest Estimate`: Låst referanse til `LE_2026`.
*   `Latest Estimate aarsbelop`: Helårs Latest Estimate.
*   `Forecast inntekter`: Prognostiserte inntekter (positivt fortegn).
*   `Forecast kostnader`: Prognostiserte drifts- og personalkostnader.
*   `Forecast lonnskostnader`: Prognostiserte personalkostnader.
*   `Forecast BOA inntekter`: Prognostisert eksternfinansiering.
*   `Forecast BOA andel %`: `DIVIDE([Forecast BOA inntekter], [Forecast inntekter])`.
*   `Forecast lonn per aarsverk`: `DIVIDE([Forecast lonnskostnader], [Aarsverk])`.
*   `Forecast kostnad per SPE60`: `DIVIDE([Forecast kostnader], [SPE 60])`.

### 04 Avvik & Analyse (Variance, Drift & VAC)
*   `Avvik mot budsjett`: `[Faktisk belop] - [Budsjett]`.
*   `Avvik mot budsjett %`: Relativt periodisk avvik.
*   `Avvik inntekter`: Mer-/mindreinntekter.
*   `Avvik kostnader`: Mer-/mindreforbruk.
*   `Avvik lonnskostnader`: Lønnsavvik.
*   `Forecast mot budsjett`: `[Forecast aarsbelop] - [Aarsbudsjett]`.
*   `Forecast mot budsjett %`: Helårsavvik i prosent.
*   `VAC (Variance at Completion)`: EVM-mål: `[BAC] - [EAC]` (positivt = besparelse / mindreforbruk).
*   `VAC %`: `DIVIDE([VAC], [BAC])`.
*   `Forecast etter tiltak mot budsjett`: Helårsavvik hensyntatt ledelsestiltak.
*   `Forecast endring fra FC1`: Estimatendring (drift) mot tidlig prognose FC1.
*   `Forecast endring fra FC2`: Estimatendring (drift) mot mellomprognose FC2.
*   `LE mot budsjett`: Helårsavvik for Latest Estimate mot opprinnelig budsjett.
*   `LE mot budsjett %`: Relativt avvik for LE mot budsjett.

### 05 Bemanning (FactFTE)
*   `Aarsverk`: `SUM(FactFTE[Aarsverk])`.
*   `Faglige aarsverk`: `SUM(FactFTE[FagligeAarsverk])`.
*   `Administrative aarsverk`: Årsverk der `DimPositionGroup[Stillingskategori] = "Teknisk-administrativ"`.
*   `Faglig andel %`: `DIVIDE([Faglige aarsverk], [Aarsverk])`.
*   `Aarsverk snitt`: `AVERAGEX(VALUES(DimDate[AarMaaned]), [Aarsverk])`.

### 06 Studiepoeng (FactStudyPoints)
*   `Avlagte studiepoeng`: `SUM(FactStudyPoints[AvlagteStudiepoeng])`.
*   `Planlagte studiepoeng`: `SUM(FactStudyPoints[PlanlagteStudiepoeng])`.
*   `SPE 60`: `SUM(FactStudyPoints[SPE60])`.
*   `Registrerte studenter`: `SUM(FactStudyPoints[RegistrerteStudenter])`.
*   `Gjennomforingsgrad %`: `DIVIDE([Avlagte studiepoeng], [Planlagte studiepoeng])`.
*   `Studiepoeng per faglige aarsverk`: `DIVIDE([Avlagte studiepoeng], [Faglige aarsverk])`.
*   `SPE60 per faglige aarsverk`: `DIVIDE([SPE 60], [Faglige aarsverk])`.

### 07 Datakvalitet & Modenhet
*   `Forecast datakvalitet %`: `AVERAGE(FactForecast[Sannsynlighet])`.
*   `Forecast faktisk andel %`: Andel av prognosen som er basert på realisert regnskap.
*   `Forecast estimert andel %`: Andel av prognosen som er gjenstående estimat.

### 08 Status & Farger (Tufte Data-Ink)
*   `Forecaststatus`: Risikovurdering via `SWITCH`: Rød (>5% overskridelse), Gul (2-5%), Grønn (+/-2%), Blå (<-5% mindreforbruk).
*   `Forecaststatus farge`: Hex-koder for betinget formatering: `#C00000` (Rød), `#FFC000` (Amber), `#70AD47` (Salviegrønn), `#5B9BD5` (Dempet blå), `#A6A6A6` (Grå).

---

## 5. Kjøring av Automatisert Testsuite
Alle 50 målene er verifisert med en automatisert Python/DuckDB testsuite som tester formlene mot de underliggende CSV-filene:
```bash
python scripts/test_dax_measures.py
```
Testsuiten sjekker additivitet, fortegn, filterkontekst, tidssammenhenger (YTD/ETC/EAC), stillingskategorier og betinget formatering.
