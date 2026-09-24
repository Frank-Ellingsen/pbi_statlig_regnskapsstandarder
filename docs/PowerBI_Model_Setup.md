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
1.  **`Organisasjonshierarki`** (`DimOrganization`): `OrgNavn` > `Instituttnavn` > `Koststednavn`
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

### 07 Status & Farger (Tufte Data-Ink & RAG)
Fargestyring og statusindikatorer er utformet iht. Edward Tuftes prinsipper: nøytrale tabellbakgrunner uten tunge fargefyll, med presise Unicode-ikoner (`🔴`, `🟡`, `🟢`, `⚪`) og dempede semantiske hex-farger for betinget formatering i Power BI (bakgrunnsfarge eller skriftfarge).

| Domene | RAG Målnavn | Fargemål | Terskelverdier / Logikk | RAG Tekst | Hex-farge |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Helårsprognose** | `Forecast RAG Status` | `Forecaststatus farge` | `[Forecastavvik %] > 0.05`<br>`[Forecastavvik %] >= 0.02`<br>Ellers | `🔴 Rød (>5%)`<br>`🟡 Gul (2-5%)`<br>`🟢 Grønn (<=2%)` | `#ef4444`<br>`#f59e0b`<br>`#10b981` |
| **YTD Regnskap** | `Avvik YTD RAG Status` | `Avvik RAG farge` | `[Avvik YTD %] > 0.05`<br>`[Avvik YTD %] >= 0.02`<br>Ellers | `🔴 Rød (>5%)`<br>`🟡 Gul (2-5%)`<br>`🟢 Grønn (<=2%)` | `#ef4444`<br>`#f59e0b`<br>`#10b981` |
| **Omstillingstiltak** | `Tiltak RAG Status` | `Tiltak RAG farge` | `Status = "Gjennomført"`<br>`Status = "Pågår"`<br>`Status = "Forsinket"`<br>`Status = "Planlagt"` | `🟢 Gjennomført`<br>`🟡 Pågår`<br>`🔴 Forsinket`<br>`⚪ Planlagt` | `#10b981`<br>`#f59e0b`<br>`#ef4444`<br>`#94a3b8` |
| **Studiepoeng** | `Studiepoeng RAG Status` | `Studiepoeng RAG farge` | `[Måloppnåelse] >= 0.90`<br>`[Måloppnåelse] >= 0.80`<br>Ellers | `🟢 Mål nådd (>=90%)`<br>`🟡 Moderat (80-90%)`<br>`🔴 Lav (<80%)` | `#10b981`<br>`#f59e0b`<br>`#ef4444` |
| **EVM Sluttavvik** | `EVM Sluttavvik RAG Status` | `EVM Sluttavvik RAG farge` | `[VAC] >= 0`<br>`[VAC %] >= -0.05`<br>Ellers | `🟢 Under budsjett`<br>`🟡 Moderat overskridelse`<br>`🔴 Kritisk overskridelse` | `#10b981`<br>`#f59e0b`<br>`#ef4444` |
| **Porteføljerisiko** | `Antall rode institutter` | — | `[Forecastavvik %] > 0.05` | Heltall (Antall enheter i rød sone) | Format: `#,0` |

### 09 Begrepskatalog (DimGlossary)
*   `Antall begreper`: `COUNTROWS(DimGlossary)` (60 definerte styringsbegreper).
*   `Antall begrepskategorier`: `DISTINCTCOUNT(DimGlossary[Kategori])` (8 faglige styringsakser).

---

## 5. Kjøring av Automatisert Testsuite
Alle 60+ målene er verifisert med en automatisert Python/DuckDB testsuite som tester formlene mot de underliggende CSV-filene:
```bash
python scripts/test_dax_measures.py
```
Testsuiten omfatter **61 automatiserte tester (61/61 bestått)** og sjekker:
1. Additivitet og fortegnsintegritet for inntekter og kostnader iht. SRS.
2. Filterkontekst og tidssammenhenger (YTD, ETC, EAC, BAC, VAC).
3. Bemannings-snapshots og stillingskategorier.
4. RAG-grenser (5% og 2% terskler for prognose og YTD-avvik).
5. Studiepoeng-terskler (90% og 80% måloppnåelse).
6. EVM-sluttavvikskategorisering for BOA-prosjekter.
7. Aggregerte risikoindikatorer (`Antall rode institutter`).
8. Begrepskatalogens integritet og kategorier (`DimGlossary`).
