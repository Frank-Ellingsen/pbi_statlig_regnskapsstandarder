# institusjonen Handelshøyskolen - Power BI Controller Rapportsuite
**Dokument-ID**: `UIA-FIN-2026-REP01`  
**Forfatter**: Frank Ellingsen (Financial Controller / Project Controller)  
**Virksomhet**: Statlig utdanningsinstitusjon / Handelshøyskolen  
**Teknisk Modell**: `UIA-Controller-Prosjekt.pbip` (Microsoft Fabric DevMode / TMDL / PBIR)  
**Standard**: Statlige regnskapsstandarder (SRS) & Edward Tufte Data-Ink Ratio

---

## 1. Kontekst & Formål for Controller-rollen ved Institusjonen

Handelshøyskolen ved Statlig utdanningsinstitusjon er AACSB-akkreditert, har om lag 2 000 studenter, 120 ansatte og er organisert i tre institutter samt fakultetsadministrasjon:
1. **Institutt for økonomi** (Samfunnsøkonomi, Finans, Regnskap)
2. **Institutt for strategi og ledelse**
3. **Institutt for rettsvitenskap**
4. **Fakultetsadministrasjonen**

Controlleren inngår i fakultetets økonomiteam, rapporterer til fakultetsdirektør, og yter løpende beslutningsstøtte til dekan, instituttledere, prosjektledere og sentral økonomiavdeling.

Rapportsuiten i Power BI er strukturert for å besvare ledelsens fem kjernebehov:
*   **Hvor står vi i dag?** (Regnskap vs. Budsjett hittil i år / YTD)
*   **Hvor ender vi ved årets slutt?** (Rullende prognoser FC1, FC2, Latest Estimate og EVM/VAC)
*   **Hvordan presterer forskningsprosjektene våre?** (BOA - Bidrags- og oppdragsaktivitet mot NFR, EU og næringsliv)
*   **Hva er sammenhengen mellom ressursbruk og studieproduksjon?** (Bemanning/årsverk, lønnskostnader og studiepoeng)
*   **Hvordan virker omstillingstiltakene?** (Portefølje av 16 innsparingstiltak, gevinster, frister og realiseringsgrad)

---

## 2. Edward Tufte Data-Ink Retningslinjer

I tråd med Edward Tuftes standarder for høy datatetthet og minimalt visuelt støy gjelder følgende prinsipper i alle sider:

1.  **Fjern "Chart Junk"**:
    *   Ingen vertikale tabellinjer i matriser og tabeller. Kun dempede horisontale linjer (`#E0E0E0`).
    *   Ingen bakgrunnsdrop shadows, tunge rammer eller dekorative ikoner på KPI-kort.
    *   Fjern standard fargelagender når linjer kan merkes direkte i grafen (*direct labeling*).
2.  **Muted Fargepalett med Signalfarger**:
    *   Bakgrunn: Nøytral hvit/lys grå (`#FFFFFF` / `#F8F9FA`).
    *   Tekst og ordinære dataserier: Mørk koksgrå (`#212529` / `#495057`).
    *   Betingede farger brukes **kun** for å signalisere avvik og risiko:
        *   **Rød (`#C00000`)**: Budsjettoverskridelse / merforbruk > 5 % eller forsinket tiltak.
        *   **Amber/Gul (`#FFC000`)**: Moderat merforbruk 2–5 % eller tiltak under observasjon.
        *   **Salviegrønn (`#70AD47`)**: I rute (+/- 2 %) eller gjennomført tiltak.
        *   **Dempet blå (`#5B9BD5`)**: Mindreforbruk / besparelse (eller høy måloppnåelse).
3.  **Typografisk Justering**:
    *   Tekst (institutt, koststed, kontonavn, prosjekt, tiltak) er alltid **venstrejustert**.
    *   Tall, valuta og prosenter er alltid **høyrejustert** med ensartet desimalplassering.

---

## 3. Side-for-side Spesifikasjon & Visuelle Oppsett

Rapporten består av fem sider i [`UIA-Controller-Prosjekt.Report`](file:///c:/Users/frank/Desktop/UIA/uia_powerbi_complete_forecast_model/UIA-Controller-Prosjekt.Report):

```text
UIA-Controller-Prosjekt.Report/definition/pages/
├── page_01_ledelse/       -> "01 Ledelsesstatus & Totaløkonomi"
├── page_02_forecast/      -> "02 Prognose & Avviksanalyse"
├── page_03_boa/           -> "03 Prosjektcontrolling & BOA"
├── page_04_bemanning/     -> "04 Bemanning & Studiepoeng"
└── page_05_tiltak/        -> "05 Tiltak & Omstillingsportefølje"
```

---

### Side 1: 01 Ledelsesstatus & Totaløkonomi
**Målgruppe**: Dekan, Fakultetsdirektør, Instituttledere.  
**Hovedspørsmål**: Hva er det økonomiske resultatet hittil, hvordan avviker vi fra budsjett, og hva er forventet helårsavvik?

#### Layout & Visuelle Komponenter:

```text
+---------------------------------------------------------------------------------------------------+
|  institusjonen Handelshøyskolen - Ledelsesstatus (2026)             [ Kvartal Slicer ]  [ Måned Slicer ]     |
+---------------------------------------------------------------------------------------------------+
|  [ KPI 1: Regnskap ]   [ KPI 2: Budsjett ]   [ KPI 3: Avvik % ]   [ KPI 4: LE ]   [ KPI 5: VAC ]  |
|    10,62 MNOK            10,75 MNOK            -1,22 %              36,79 MNOK     -26,05 MNOK    |
+-------------------------------------------------------------------+-------------------------------+
|  HOVEDMATRISE (Drill-down i institusjonen Organisasjon)                     |  SRS KOSTNADSFORDELING        |
|  - Fakultetsadministrasjon                                        |  - Lønnskostnader: 69,0 %     |
|  - Institutt for økonomi                                          |  - Driftskostnader: 26,0 %    |
|  - Institutt for strategi og ledelse                              |  - Avskrivninger: 5,0 %       |
|  - Institutt for rettsvitenskap                                   |                               |
|  Kolonner: Regnskap | Budsjett | Avvik | Gjeldende FC | Status    |  Kolonner: Regnskap | Budsjett|
+-------------------------------------------------------------------+-------------------------------+
```

#### Feltoppsett i Power BI Desktop:
1.  **Toppstripe / Slicere**:
    *   `DimDate[Kvartal]` og `DimDate[Maaned]`. Stil: Horisontal knappestil.
    *   `DimForecastVersion[Versjon]`. Enkeltvalg (standard: `LE_2026`).
2.  **KPI-kort (Nytt kort-visual / New Card Visual)**:
    *   Kort 1: `[Regnskap]` (10 617 128,19 kr).
    *   Kort 2: `[Budsjett]` (10 747 732,82 kr).
    *   Kort 3: `[Avvik %]` (-1,22 %). Betinget farge via `[Forecaststatus farge]`.
    *   Kort 4: `[Gjeldende forecast]` (36 793 524,31 kr).
    *   Kort 5: `[VAC (Variance at Completion)]` (-26 045 791,49 kr).
3.  **Hovedmatrise (Matrix)**:
    *   **Rader**: `DimOrganization[Fakultetsnavn]` > `DimOrganization[Instituttnavn]` > `DimOrganization[Koststednavn]`.
    *   **Verdier**: `[Regnskap]`, `[Budsjett]`, `[Avvik]`, `[Avvik %]`, `[Gjeldende forecast]`, `[Forecaststatus]`.
    *   **Formatering**: Ingen vertikale linjer, radavstand 4 pt.
4.  **SRS Kostnadsfordeling (Clustered Bar Chart)**:
    *   **Y-akse**: `DimAccount[SRS_regnskapslinje]`.
    *   **X-akse**: `[Kostnader]`, `[Budsjett]`.

---

### Side 2: 02 Prognose & Avviksanalyse (Forecast Drift & EVM)
**Målgruppe**: Fakultetscontroller, Sentral økonomiavdeling, Prosjektledere.  
**Hovedspørsmål**: Hvordan har helårsestimatet endret seg fra BAC via FC1 og FC2 til LE? Hva er tiltaksjustert prognose?

#### Layout & Visuelle Komponenter:

```text
+---------------------------------------------------------------------------------------------------+
|  Prognosestyring & Estimatendring (EVM)                [ Institutt Slicer ]  [ SRS Linje Slicer ]  |
+---------------------------------------------------------------------------------------------------+
|  [ BAC ]              [ EAC ]               [ ETC ]               [ VAC ]          [ Tiltak ]     |
|   10,75 MNOK           36,79 MNOK            (Gjenstående)         -26,05 MNOK      -10,01 MNOK   |
+-------------------------------------------------------------------+-------------------------------+
|  S-KURVE / TIDSSERIE (Kumulativ YTD over 12 måneder)              |  PROGNOSEVANDRING (FC1-FC2-LE)|
|  - Budsjett YTD (BAC-bane)                                        |  BAC: 10,75 M                 |
|  - Regnskap YTD (reelt forbruk)                                   |  FC1: 35,47 M                 |
|  - Gjeldende forecast (prognosebane)                              |  FC2: 35,96 M                 |
|  (Direkte merking på linjene uten separat boks)                   |  LE:  36,79 M                 |
+-------------------------------------------------------------------+-------------------------------+
```

#### Feltoppsett i Power BI Desktop:
1.  **EVM Scorecard**:
    *   `[BAC (Budget at Completion)]`: 10 747 733 kr.
    *   `[EAC (Estimate at Completion)]`: 36 793 524 kr.
    *   `[ETC (Estimate to Complete)]`: Gjenstående ressursbruk.
    *   `[VAC (Variance at Completion)]`: -26 045 791 kr (Merforbruk mot budsjett).
    *   `[Forventet tiltakseffekt]`: -10 005 000 kr (Porteføljebesparelse).
2.  **S-Kurve (Line Chart)**:
    *   **X-akse**: `DimDate[Maaned]`.
    *   **Y-akse**: `[Budsjett YTD]` (Grå stiplet `#7F7F7F`), `[Regnskap YTD]` (Mørk hel `#212529`), `[Forecast aarsbelop]`.
3.  **Vannfallsdiagram / Prognosevandring**:
    *   Trinnvis visning fra `BAC` -> `FC1` -> `FC2` -> `LE` -> `[Forecast etter tiltak]` (26,79 MNOK).

---

### Side 3: 03 Prosjektcontrolling & Eksternfinansiering (BOA)
**Målgruppe**: Prosjektcontrollere, Forskningsledere, Eksterne oppdragsgivere.  
**Hovedspørsmål**: Hvilke BOA-prosjekter har vi (NFR, EU, Oppdrag), og dekker inntektene de faktiske prosjektkostnadene?

#### Layout & Visuelle Komponenter:

```text
+---------------------------------------------------------------------------------------------------+
|  Prosjektcontrolling & BOA-virksomhet               [ Finansieringstype ]  [ Finansieringskilde ] |
+---------------------------------------------------------------------------------------------------+
|  [ BOA Inntekter ]       [ NFR Inntekter ]        [ EU Inntekter ]          [ BOA Andel % ]       |
|    25,68 MNOK              12,90 MNOK               7,43 MNOK                 1,20 %              |
+---------------------------------------------------------------------------------------------------+
|  PROSJEKTPORTEFØLJE MATRISE (Hierarkisk visning)                                                  |
|  - Bevilgning / Drift (KD)                                                                        |
|  - Bidrag (NFR, EU)                                                                               |
|  - Oppdrag (Ekstern etter- og videreutdanning / rådgivning)                                       |
|  Kolonner: Kostnader | Inntekter | Regnskap (Netto) | Budsjett | Gjeldende FC | Avvik            |
+---------------------------------------------------------------------------------------------------+
```

#### Feltoppsett i Power BI Desktop:
1.  **Slicere**: `DimProject[Finansieringstype]` og `DimProject[Finansieringskilde]`.
2.  **KPI-kort**:
    *   `[BOA inntekter]` (25 678 288,24 kr).
    *   `[NFR inntekter]` (12 901 569,82 kr).
    *   `[EU inntekter]` (7 430 967,28 kr).
    *   `[BOA andel %]` (1,20 % av institusjonens totale inntekter).
3.  **Prosjektmatrise (Matrix)**:
    *   **Rader**: `DimProject[Prosjekthierarki]` (`Finansieringstype` > `Finansieringskilde` > `Prosjektkategori` > `Prosjektnavn`).
    *   **Verdier**: `[Kostnader]`, `[Inntekter]`, `[Regnskap]`, `[Budsjett]`, `[Gjeldende forecast]`, `[Avvik]`.

---

### Side 4: 04 Bemanning, Ressursstyring & Studieproduksjon
**Målgruppe**: Dekan, Fakultetsdirektør, Instituttledere, Studieprogramledere.  
**Hovedspørsmål**: Hvor mange årsverk utføres per institutt, hva er faglig balanse, og hvor mange studiepoeng produseres?

#### Layout & Visuelle Komponenter:

```text
+---------------------------------------------------------------------------------------------------+
|  Kapasitetsstyring & Studiepoengproduksjon              [ Studienivå ]  [ Stillingskategori ]     |
+---------------------------------------------------------------------------------------------------+
|  [ Årsverk Siste Mnd ] [ Faglige Årsverk ] [ Reg. Studenter ] [ Avlagte SP ]   [ Måloppnåelse % ] |
|    1 285,93              661,77              6 490             336 945,4 SP      86,38 %          |
+-------------------------------------------------------------------+-------------------------------+
|  INSTITUTTVIS BEMANNING & PRODUKTIVITET                           |  STUDIEPROGRAMOVERSIKT        |
|  - Institutt for økonomi                                          |  - Bachelor i adm/ledelse     |
|  - Institutt for strategi og ledelse                              |  - Master i økonomi & adm     |
|  - Institutt for rettsvitenskap                                   |  - PhD-program                |
|  Kolonner: Årsverk | Faglige ÅV | Studenter/Faglig ÅV | SPE60     |  Kolonner: Studenter | SP | %  |
+-------------------------------------------------------------------+-------------------------------+
```

#### Feltoppsett i Power BI Desktop:
1.  **KPI-kort**:
    *   `[Aarsverk]`: 1 285,93 årsverk (snapshot ved siste måned).
    *   `[Faglige aarsverk]`: 661,77 vitenskapelige årsverk.
    *   `[Registrerte studenter]`: 6 490 studenter.
    *   `[Avlagte studiepoeng]`: 336 945,4 SP.
    *   `[Studiepoeng maaloppnaelse %]`: 86,38 % (Avlagte vs. planlagte SP).
    *   `[Studenter per faglig aarsverk]`: 9,8 studenter per vitenskapelig årsverk.
2.  **Instituttmatrise**:
    *   **Rader**: `DimOrganization[Instituttnavn]`.
    *   **Verdier**: `[Aarsverk]`, `[Faglige aarsverk]`, `[Studenter per faglig aarsverk]`, `[Avlagte studiepoeng]`, `[SPE60]`, `[Lonn per aarsverk]`.
3.  **Studieprogramtabell**:
    *   **Rader**: `DimStudyProgram[Studienivaa]` > `DimStudyProgram[Studieprogramnavn]`.
    *   **Verdier**: `[Registrerte studenter]`, `[Avlagte studiepoeng]`, `[SPE60]`, `[Studiepoeng maaloppnaelse %]`.

---

### Side 5: 05 Tiltak & Omstillingsportefølje (FactAction)
**Målgruppe**: Dekan, Fakultetsdirektør, Økonomiledelse, Omstillingsutvalg.  
**Hovedspørsmål**: Hvilke innsparingstiltak er igangsatt, hvem er ansvarlig, hva er realisert gevinst mot mål, og hvilke tiltak er forsinket?

#### Layout & Visuelle Komponenter:

```text
+---------------------------------------------------------------------------------------------------+
|  Omstilling & Tiltaksoppfølging (2026)                    [ Status Slicer ]  [ Kategori Slicer ]  |
+---------------------------------------------------------------------------------------------------+
|  [ Antall Tiltak ]    [ Forventet Effekt ]  [ Realisert Effekt ]  [ Realiseringsgrad ] [ Forsinket] |
|    16 tiltak            -10,01 MNOK           -5,56 MNOK            55,59 %              4 tiltak |
+-------------------------------------------------------------------+-------------------------------+
|  TILTAKSPORTEFØLJE (Tabell med trafikklys)                        |  TILTAKSEFFEKT MOT RESTAVVIK  |
|  - T001: Reduksjon timeundervisning (ISL)                         |  Forecastavvik:  +26,05 M     |
|  - T002: Digitalisering emneevaluering (ADM)                      |  Tiltakseffekt:  -10,01 M     |
|  - T003: Sammenslåing masteremner (ØKO)                           |  Restavvik:      +16,04 M     |
|  Kolonner: ID | Navn | Ansvarlig | Frist | Forventet | Realisert  |  Dekningsgrad:    38,4 %      |
+-------------------------------------------------------------------+-------------------------------+
```

#### Feltoppsett i Power BI Desktop:
1.  **Slicere**:
    *   `FactAction[Status]` (`Gjennomfort`, `Pagar`, `Forsinket`, `Planlagt`).
    *   `FactAction[Tiltakskategori]`.
2.  **KPI-kort**:
    *   `[Antall tiltak]`: 16 tiltak.
    *   `[Forventet tiltakseffekt]`: -10 005 000 kr.
    *   `[Realisert tiltakseffekt]`: -5 562 082 kr.
    *   `[Tiltak realiseringsgrad %]`: 55,59 %.
    *   `[Forsinkede tiltak]`: 4 tiltak (Fremhevet med rød farge `#C00000`).
3.  **Tiltakstabell**:
    *   **Kolonner**: `FactAction[TiltakID]`, `FactAction[Tiltaksnavn]`, `FactAction[Ansvarlig]`, `FactAction[FristDatoNokkel]`, `FactAction[Status]`, `[Forventet tiltakseffekt]`, `[Realisert tiltakseffekt]`.
    *   **Betinget formatering på Status**:
        *   `Gjennomfort` -> Grønn (`#70AD47`)
        *   `Pagar` -> Blå (`#5B9BD5`)
        *   `Planlagt` -> Grå (`#A6A6A6`)
        *   `Forsinket` -> Rød (`#C00000`)
4.  **Bro / Dekningskort**:
    *   `[Forecastavvik]`: 26 045 791 kr.
    *   `[Forventet tiltakseffekt]`: -10 005 000 kr.
    *   `[Restavvik etter tiltak]`: 16 040 791 kr.
    *   `[Tiltaksdekning av avvik %]`: 38,4 %.

---

## 4. Årshjul for Controlleren ved institusjonen Handelshøyskolen

| Periode | Aktivitet | Fokus i Power BI Modellen |
|---|---|---|
| **Månedlig (T+5)** | Månedsavslutning & avviksoppfølging | **Side 1 (Ledelse)** & **Side 5 (Tiltak)**: Avstemme faktiske regnskapsposteringer mot månedsbudsjett. Følge opp åpne tiltak og forsinkelser. |
| **Mai (T1)** | Første tertialrapport & Prognose 1 | **Side 2 (Prognose)**: Gjennomgang av `FC1_2026` (4 mnd faktisk + 8 mnd estimert). Vurdere tiltak ved overskridelser. |
| **September (T2)** | Andre tertialrapport & Prognose 2 | **Side 2 (Prognose)** & **Side 4 (Studier)**: Gjennomgang av `FC2_2026` (8 mnd faktisk + 4 mnd estimert). Vurdere høstens studentopptak og studiepoeng. |
| **November (T3)** | Årsavslutningsprognose (Latest Estimate) | **Side 2 (Prognose - LE)**: Låse `LE_2026` (10 mnd faktisk + 2 mnd estimert). Beregne endelig `VAC` (Estimate at Completion vs. budsjett). |
| **Løpende** | Eksternfinansierte forskningsprosjekter | **Side 3 (BOA)**: Timeføring, overhead/indirekte kostnader, prosjektavslutninger og rapportering til NFR/EU. |
| **Høst** | Budsjettprosess neste år | Koble ressursbehov (årsverk per institutt) og studieprogramplaner til økonomiske rammer (BAC). |

---

## 5. Kvalitetssikring & Integritet

*   **14 tabeller** og **22 aktive relasjoner** validert med DuckDB ([`scripts/validate_model.py`](file:///c:/Users/frank/Desktop/UIA/uia_powerbi_complete_forecast_model/scripts/validate_model.py)).
*   **43 automatiserte tester** bestått i DAX testsuiten ([`scripts/test_dax_measures.py`](file:///c:/Users/frank/Desktop/UIA/uia_powerbi_complete_forecast_model/scripts/test_dax_measures.py)).
*   100 % overensstemmelse med Edward Tuftes Data-Ink Ratio og Frank Ellingsens standarder.
