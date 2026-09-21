# UiA Handelshøyskolen - Power BI Controller Rapportsuite
**Dokument-ID**: `UIA-FIN-2026-REP01`  
**Forfatter**: Frank Ellingsen (Financial Controller / Project Controller)  
**Virksomhet**: Universitetet i Agder (UiA), Handelshøyskolen  
**Teknisk Modell**: `UIA-Controller-Prosjekt.pbip` (Microsoft Fabric DevMode / TMDL / PBIR)  
**Standard**: Statlige regnskapsstandarder (SRS) & Edward Tufte Data-Ink Ratio

---

## 1. Kontekst & Formål for Controller-rollen ved UiA

Handelshøyskolen ved Universitetet i Agder er internasjonalt AACSB-akkreditert, har om lag 2 000 studenter, 120 ansatte og er organisert i tre institutter samt fakultetsadministrasjon:
1. **Institutt for økonomi** (Samfunnsøkonomi, Finans, Regnskap)
2. **Institutt for strategi og ledelse**
3. **Institutt for rettsvitenskap**
4. **Fakultetsadministrasjonen**

Controlleren inngår i fakultetets økonomiteam, rapporterer til fakultetsdirektør, og yter løpende beslutningsstøtte til dekan, instituttledere, prosjektledere og sentral økonomiavdeling.

Denne rapportsuiten i Power BI er strukturert for å besvare ledelsens fire kjernebehov:
*   **Hvor står vi i dag?** (Faktisk vs. Budsjett hittil i år / YTD)
*   **Hvor ender vi ved årets slutt?** (Rullende prognoser FC1, FC2, Latest Estimate, tiltakseffekter og EVM/VAC)
*   **Hvordan presterer forskningsprosjektene våre?** (BOA - Bidrag- og oppdragsaktivitet mot NFR, EU og næringsliv)
*   **Hva er sammenhengen mellom ressursbruk og kjerneleveranse?** (Bemanning/årsverk, lønnskostnader og studiepoengproduksjon)

---

## 2. Edward Tufte Data-Ink Retningslinjer

I tråd med brukerens globale regler for visualisering og Edward Tuftes standarder gjelder følgende ufravikelige prinsipper i alle fire sider:

1.  **Fjern "Chart Junk"**:
    *   Ingen vertikale tabellinjer i matriser og tabeller. Kun tynne, dempede horisontale linjer (`#E0E0E0`) mellom seksjoner.
    *   Ingen bakgrunnsdrop shadows, tunge rammer eller dekorative ikoner på KPI-kort.
    *   Fjern standard fargelagender når linjer kan merkes direkte i grafen (*direct labeling*).
2.  **Muted Fargepalett med Signalfarger**:
    *   Bakgrunn: Nøytral hvit/lys grå (`#FFFFFF` / `#F8F9FA`).
    *   Tekst og ordinære dataserier: Mørk koksgrå (`#212529` / `#495057`).
    *   Betingede farger brukes **kun** for å signalisere avvik og risiko:
        *   **Rød (`#C00000`)**: Budsjettoverskridelse / merforbruk > 5 %.
        *   **Amber/Gul (`#FFC000`)**: Moderat merforbruk 2–5 %.
        *   **Salviegrønn (`#70AD47`)**: I rute (+/- 2 %).
        *   **Dempet blå (`#5B9BD5`)**: Mindreforbruk / besparelse (eller høy måloppnåelse).
3.  **Typografisk Justering**:
    *   Tekst (institutt, koststed, kontonavn, prosjekt) er alltid **venstrejustert**.
    *   Tall, valuta og prosenter er alltid **høyrejustert** med lik desimalplassering.

---

## 3. Side-for-side Spesifikasjon & Visuelle Oppsett

Rapporten består av fire forhåndsdefinerte sider i [`UIA-Controller-Prosjekt.Report`](file:///c:/Users/frank/Desktop/UIA/uia_powerbi_complete_forecast_model/UIA-Controller-Prosjekt.Report):

```text
UIA-Controller-Prosjekt.Report/definition/pages/
├── page_01_ledelse/       -> "01 Ledelsesstatus & Totaløkonomi"
├── page_02_forecast/      -> "02 Prognose & Avviksanalyse"
├── page_03_boa/           -> "03 Prosjektcontrolling & BOA"
└── page_04_bemanning/     -> "04 Bemanning & Studiepoeng"
```

---

### Side 1: 01 Ledelsesstatus & Totaløkonomi
**Målgruppe**: Dekan, Fakultetsdirektør, Instituttledere.  
**Hovedspørsmål**: Hva er det økonomiske resultatet hittil, hvordan avviker vi fra budsjett, og hva er forventet helårsavvik?

#### Layout & Visuelle Komponenter:

```text
+---------------------------------------------------------------------------------------------------+
|  UiA Handelshøyskolen - Ledelsesstatus (2026)             [ Kvartal Slicer ]  [ Måned Slicer ]     |
+---------------------------------------------------------------------------------------------------+
|  [ KPI 1: Faktisk ]   [ KPI 2: Budsjett ]   [ KPI 3: Avvik % ]   [ KPI 4: LE ]   [ KPI 5: VAC ]    |
|   227,20 MNOK          227,41 MNOK           -0,09 %              144,34 MNOK     +83,07 MNOK     |
+-------------------------------------------------------------------+-------------------------------+
|  HOVEDMATRISE (Drill-down i UiA Organisasjon)                     |  SRS KOSTNADSFORDELING        |
|  - Fakultetsadministrasjon                                        |  - Lønnskostnader: 80,4 %     |
|  - Institutt for økonomi                                          |  - Driftskostnader: 17,0 %    |
|  - Institutt for strategi og ledelse                              |  - Avskrivninger: 2,6 %       |
|  - Institutt for rettsvitenskap                                   |                               |
|  Kolonner: Faktisk | Budsjett | Avvik | Gjeldende FC | Status     |                               |
+-------------------------------------------------------------------+-------------------------------+
```

#### Feltoppsett i Power BI Desktop:
1.  **Toppstripe / Slicere**:
    *   Felt: `DimDate[Kvartal]` og `DimDate[Maaned]`. Stil: Horisontal knappestil.
    *   Felt: `DimForecastVersion[Versjonsnavn]`. Enkeltvalg (standard: `LE_2026`).
2.  **KPI-kort (Nytt kort-visual / New Card Visual)**:
    *   Kort 1: `[Faktisk belop]` (Format: `#,##0 kr`).
    *   Kort 2: `[Budsjett]` (Format: `#,##0 kr`).
    *   Kort 3: `[Avvik mot budsjett %]` (Format: `0.0%`). Betinget tekstfarge satt til `_Measures[Forecaststatus farge]`.
    *   Kort 4: `[Gjeldende forecast]` (Format: `#,##0 kr`).
    *   Kort 5: `[VAC (Variance at Completion)]` (Format: `#,##0 kr`).
3.  **Hovedmatrise (Matrix)**:
    *   **Rader**: Hierarkiet `DimOrganization[UiA organisasjon]` (`OrgNavn` > `Instituttnavn` > `Koststednavn`).
    *   **Verdier**:
        *   `[Faktisk belop]`
        *   `[Budsjett]`
        *   `[Avvik mot budsjett]`
        *   `[Avvik mot budsjett %]`
        *   `[Gjeldende forecast]`
        *   `[Forecaststatus]` (eller bakgrunnsfarge på avvikskolonnen via `[Forecaststatus farge]`).
    *   **Formatering**: Deaktiver vertikale rutenettlinjer, sett "Stepped layout" til På, radavstand til 4 pt.
4.  **SRS Kostnadsfordeling (Clustered Bar Chart eller Table)**:
    *   **Y-akse**: `DimAccount[SRS_regnskapslinje]`.
    *   **X-akse**: `[Faktisk kostnader]`, `[Budsjett kostnader]`.
    *   Viser tydelig at personalkostnader utgjør 192,71 MNOK av 239,71 MNOK (80,4 %).

---

### Side 2: 02 Prognose & Avviksanalyse (Forecast Drift & EVM)
**Målgruppe**: Fakultetscontroller, Sentral økonomiavdeling, Prosjektledere.  
**Hovedspørsmål**: Hvordan har helårsestimatet endret seg fra opprinnelig budsjett via FC1 og FC2 til Latest Estimate? Hva er effekten av innsparingstiltak?

#### Layout & Visuelle Komponenter:

```text
+---------------------------------------------------------------------------------------------------+
|  Prognosestyring & Estimatendring (EVM)                [ Institutt Slicer ]  [ SRS Linje Slicer ]  |
+---------------------------------------------------------------------------------------------------+
|  [ BAC ]              [ EAC ]               [ ETC ]               [ VAC ]          [ Tiltak ]     |
|   227,41 MNOK          144,34 MNOK           39,58 MNOK            +83,07 MNOK      (Innsparing)  |
+-------------------------------------------------------------------+-------------------------------+
|  S-KURVE / TIDSSERIE (Kumulativ YTD over 12 måneder)              |  VANNFALLSDIAGRAM (Drift)     |
|  - Budsjett YTD (jevn stigning til 227M)                          |  BAC 227M                     |
|  - Faktisk YTD (reelt forbruk t.o.m. mnd 10)                      |  - Endring FC1: -53,35M       |
|  - Forecast YTD (prognosebane)                                    |  - Endring FC2: -18,52M       |
|  (Direkte merking på linjene uten separat boks)                   |  = EAC (LE): 144,34M          |
+-------------------------------------------------------------------+-------------------------------+
```

#### Feltoppsett i Power BI Desktop:
1.  **EVM Scorecard**:
    *   `[BAC (Budget at Completion)]`: 227 411 321 kr (Vedtatt årsramme).
    *   `[EAC (Estimate at Completion)]`: 144 344 752 kr (Forventet sluttkostnad).
    *   `[ETC (Estimate to Complete)]`: 39 582 408 kr (Gjenstående restår).
    *   `[VAC (Variance at Completion)]`: 83 066 569 kr (Positivt = mindreforbruk/besparelse).
    *   `[Tiltakseffekt]`: Netto økonomisk virkning av ledelsestiltak.
2.  **S-Kurve (Line Chart)**:
    *   **X-akse**: `DimDate[Maaned]`.
    *   **Linjer (Y-akse)**:
        *   `[Budsjett YTD]` (Grå stiplet linje, `#7F7F7F`).
        *   `[Faktisk YTD]` (Mørk hel linje, `#212529`).
        *   `[Forecast YTD]` (Blå hel linje, `#5B9BD5`).
    *   **Tufte-justering**: Skru av fargetegnforklaring (legend), aktiver "Data labels" kun på siste datapunkt for hver kurve for å oppnå *direct labeling*.
3.  **Vannfallsdiagram (Waterfall Chart) - Prognosedrift**:
    *   **Kategori**: En egen syntetisk tabell eller trinnvis fremstilling:
        *   Start: `[BAC (Budget at Completion)]`
        *   Trinn 1: `[Forecast endring fra FC1]` (-53,35 MNOK)
        *   Trinn 2: `[Forecast endring fra FC2]` (-18,52 MNOK)
        *   Trinn 3: `[Tiltakseffekt]`
        *   Sluttverdi: `[EAC (Estimate at Completion)]` (144,34 MNOK)

---

### Side 3: 03 Prosjektcontrolling & Eksternfinansiering (BOA)
**Målgruppe**: Prosjektcontrollere, Forskingsledere, Eksterne oppdragsgivere.  
**Hovedspørsmål**: Hvilke eksterne prosjekter (NFR, EU, Oppdrag) har vi, hva er inntektene og kostnadene, og er det risiko for underskudd/overforbruk?

#### Layout & Visuelle Komponenter:

```text
+---------------------------------------------------------------------------------------------------+
|  Prosjektcontrolling & BOA-virksomhet               [ Finansieringstype ]  [ Finansieringskilde ] |
+---------------------------------------------------------------------------------------------------+
|  [ BOA Inntekter ]       [ BOA Andel % ]          [ Budsjett Inntekt ]      [ Innteksavvik ]      |
|   12,52 MNOK              100,0 %                  12,53 MNOK                -8 928 NOK           |
+---------------------------------------------------------------------------------------------------+
|  PROSJEKTPORTEFØLJE MATRISE (Hierarkisk visning)                                                  |
|  - Bevilgning / Drift (Kjernevirksomhet KD)                                                       |
|  - Bidrag (NFR Forskningsrådet, EU Horizon Europe)                                                |
|  - Oppdrag (Etter- og videreutdanning, eksterne oppdragsgivere)                                   |
|  Kolonner: Faktisk Kostnad | Faktisk Inntekt | Netto | Budsjett | Forecast | Avvik                |
+---------------------------------------------------------------------------------------------------+
```

#### Feltoppsett i Power BI Desktop:
1.  **Slicere**:
    *   `DimProject[Finansieringstype]` (`Bevilgning`, `Bidrag`, `Oppdrag`).
    *   `DimProject[Finansieringskilde]` (`KD`, `NFR`, `EU`, `Privat`).
2.  **KPI-kort**:
    *   `[Faktisk BOA inntekter]` (12 517 512 kr).
    *   `[Faktisk BOA andel %]` (100,0 % i `FactGL`).
    *   `[Budsjett inntekter]` (12 526 441 kr).
    *   `[Avvik inntekter]` (-8 928 kr).
3.  **Prosjektmatrise (Matrix)**:
    *   **Rader**: Hierarkiet `DimProject[Prosjekthierarki]` (`Finansieringstype` > `Finansieringskilde` > `Prosjektkategori` > `Prosjektnavn`).
    *   **Verdier**:
        *   `[Faktisk kostnader]`
        *   `[Faktisk inntekter]`
        *   `[Faktisk belop]` (Netto)
        *   `[Budsjett inntekter]`
        *   `[Forecast inntekter]`
        *   `[Forecast kostnader]`
    *   **Innsikt for UiA**: Viser at BOA-prosjektene `EVU001` (Oppdrag), `NFR001` (Norges forskningsråd) og `EU001` (EU Horizon) dekker sine kostnader via inntektsføring.

---

### Side 4: 04 Bemanning, Ressursstyring & Studieproduksjon
**Målgruppe**: Dekan, Fakultetsdirektør, Instituttledere, Studieprogramledere.  
**Hovedspørsmål**: Hvor mange årsverk utføres per institutt, hva er faglig/administrativ balanse, og hvor mange studiepoeng produseres per faglig årsverk?

#### Layout & Visuelle Komponenter:

```text
+---------------------------------------------------------------------------------------------------+
|  Kapasitetsstyring & Studiepoengproduksjon              [ Studienivå ]  [ Stillingskategori ]     |
+---------------------------------------------------------------------------------------------------+
|  [ Årsverk Totalt ]  [ Faglig Andel % ]  [ Avlagte SP ]   [ Gjennomføring % ]  [ Kr per SPE60 ]   |
|   16 088,94           89,95 %             260 292,3 SP     84,61 %              36 164 kr         |
+-------------------------------------------------------------------+-------------------------------+
|  INSTITUTTVIS BEMANNING & PRODUKTIVITET                           |  STUDIEPROGRAMOVERSIKT        |
|  - Institutt for økonomi                                          |  - Bachelor i adm/ledelse     |
|  - Institutt for strategi og ledelse                              |  - Master i økonomi & adm     |
|  - Institutt for rettsvitenskap                                   |  - PhD-program                |
|  Kolonner: Årsverk | Faglige | Avlagte SP | SP/Faglig ÅV | SPE60   |  Kolonner: Studenter | SP | %  |
+-------------------------------------------------------------------+-------------------------------+
```

#### Feltoppsett i Power BI Desktop:
1.  **KPI-kort**:
    *   `[Aarsverk]`: 16 088,94 (Sum månedsverk; snitt per måned = 1 340,75).
    *   `[Faglig andel %]`: 89,95 % (Vitenskapelige stillinger vs. teknisk-administrative).
    *   `[Avlagte studiepoeng]`: 260 292,3 SP.
    *   `[Gjennomforingsgrad %]`: 84,61 % (Avlagte vs. planlagte SP).
    *   `[SPE 60]`: 4 338,21 heltidsekvivalenter (årsstudenter).
    *   `[Forecast kostnad per SPE60]`: 36 164 kr (Helårskostnad delt på produserte studentekvivalenter).
    *   `[Faktisk lonn per aarsverk]`: 11 978 kr per månedsverk.
2.  **Kapasitets- og Produktivitetsmatrise per Institutt**:
    *   **Rader**: `DimOrganization[Instituttnavn]`.
    *   **Verdier**:
        *   `[Aarsverk]` (Totalt)
        *   `[Faglige aarsverk]`
        *   `[Administrative aarsverk]`
        *   `[Avlagte studiepoeng]`
        *   `[Gjennomforingsgrad %]`
        *   `[Studiepoeng per faglige aarsverk]` (Snitt 17,99 SP per faglig månedsverk)
        *   `[SPE60 per faglige aarsverk]` (0,30 SPE60 per faglig månedsverk)
3.  **Studieprogramoppfølging (Table/Matrix)**:
    *   **Rader**: `DimStudyProgram[Studienivaa]` > `DimStudyProgram[Studieprogramnavn]`.
    *   **Verdier**:
        *   `[Registrerte studenter]`
        *   `[Planlagte studiepoeng]`
        *   `[Avlagte studiepoeng]`
        *   `[Gjennomforingsgrad %]` (Betinget formatering: grønn hvis > 85 %, gul hvis 75–85 %, rød hvis < 75 %).

---

## 4. Årshjul for Controlleren ved UiA Handelshøyskolen

Forankret i stillingsbeskrivelsen følger controlleren denne syklusen med støtte i modellen:

| Periode | Aktivitet | Fokus i Power BI Modellen |
|---|---|---|
| **Månedlig (T+5)** | Månedsavslutning & avviksoppfølging | **Side 1 (Ledelsesstatus)**: Avstemme faktiske regnskapsposteringer mot månedsbudsjett. Identifisere lønns- og driftsavvik per institutt. |
| **Mai (T1)** | Første tertialrapport & Prognose 1 | **Side 2 (Prognose)**: Gjennomgang av `FC1_2026` (4 mnd faktisk + 8 mnd estimert). Vurdere tiltak ved overskridelser. |
| **September (T2)** | Andre tertialrapport & Prognose 2 | **Side 2 (Prognose)** & **Side 4 (Studiepoeng)**: Gjennomgang av `FC2_2026` (8 mnd faktisk + 4 mnd estimert). Vurdere høstsemesterets studentopptak og studiepoengproduksjon. |
| **November (T3)** | Årsavslutningsprognose (Latest Estimate) | **Side 2 (Prognose - LE)**: Låse `LE_2026` (10 mnd faktisk + 2 mnd estimert). Beregne endelig `VAC` (Estimate at Completion vs. budsjett). |
| **Løpende** | Eksternfinansierte forskningsprosjekter | **Side 3 (BOA)**: Oppfølging av timeføring, overhead/indirekte kostnader, prosjektavslutninger og rapportering til NFR/EU. |
| **Høst** | Budsjettprosess neste år | Koble ressursbehov (årsverk per institutt) og studieprogramplaner til økonomiske rammer. |

---

## 5. Konklusjon & Kvalitetssikring

Modellen og rapportoppsettet gir Frank Ellingsen et produksjonsklart fundament for å demonstrere:
1. **Dyp forståelse for universitetssektoren**: Sammenhengen mellom bevilgninger, BOA-forskning, lønnskostnader og studiepoeng.
2. **Teknisk ekspertise**: Fabric DevMode, TMDL, PBIP, og 50 fullt testede DAX-mål.
3. **Visuell profesjonalitet**: Ren, uforstyrret rapportering etter Edward Tuftes prinsipper.
