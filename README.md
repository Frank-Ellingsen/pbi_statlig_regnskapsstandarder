# UiA Controller - Økonomi & Forecast Datamodell (Power BI / PBIP)

Dette prosjektet inneholder en komplett, produksjonsklar datamodell og controller-løsning for **Universitetet i Agder (UiA)**, oppdatert med den fullskala styringspakken (`uia_complete_controller_powerbi_excel_package`). Modellen er utviklet i henhold til beste praksis for virksomhetsstyring, prosjektcontrolling, DFØs statlige regnskapsstandarder (SRS), BOA-retningslinjer (Bidrag & Oppdrag) og **Edward Tuftes prinsipper for datavisualisering (Data-Ink Ratio)**.

Løsningen er bygget på **Microsoft Fabric / Power BI Project-formatet (`.pbip` / TMDL)** og støtter versjonskontroll i Git, automatisert testing via DuckDB og Python, samt modulær DAX-arkitektur.

---

## 1. Mappestruktur & Organisering

```text
uia_powerbi_complete_forecast_model/
├── data/                               # Kildata (UTF-8, semikolon-separerte CSV-filer)
│   ├── DimAccount.csv                  # Kontoplan iht. DFØ R-102/2025 (46 kontoer)
│   ├── DimDate.csv                     # Kalender 2026-2027 (730 dager)
│   ├── DimForecastVersion.csv          # Prognoseversjoner: BUD2026, FC1, FC2, LE (4 rader)
│   ├── DimOrganization.csv             # Organisasjonsstruktur for hele UiA (74 koststeder)
│   ├── DimPositionGroup.csv            # Stillingsgrupper: vitenskapelig/administrativ (5 rader)
│   ├── DimProject.csv                  # Prosjekter, BOA-typer og finansieringskilder (8 rader)
│   ├── DimStudyProgram.csv             # Studieprogrammer og studienivåer (22 rader)
│   ├── FactAction.csv                  # Omstillingstiltak og gevinstrealisering (16 tiltak)
│   ├── FactBudget.csv                  # Periodisert månedsbudsjett (17 760 rader)
│   ├── FactFTE.csv                     # Årsverk og faglige årsverk (1 440 rader)
│   ├── FactForecast.csv                # Rullende prognoser FC1, FC2, LE (53 280 rader)
│   ├── FactGL.csv                      # Hovedboksposteringer og regnskap (35 760 rader)
│   ├── FactStudyPoints.csv             # Studenttall og studiepoengproduksjon (264 rader)
│   └── Relationships.csv               # Definisjon av 22 relasjoner i stjernemodellen
├── dax/                                # DAX-mål og formelbiblioteker
│   ├── Complete_Measures.dax           # Master DAX-bibliotek med formatering og beskrivelser
│   └── All_Measures_Combined.dax       # Komplett samlet DAX-katalog for Excel og verktøy
├── docs/                               # Dokumentasjon og spesifikasjoner
│   ├── Controller - UIA.pdf            # Stillings- og casebeskrivelse for UiA
│   ├── DATA_MODEL_ARCHITECTURE.md      # Teknisk arkitektur, korn, relasjoner og ordbok
│   ├── Forecast_Model_Setup.md         # Regler for forecast- og versjonsmodellering
│   ├── PowerBI_Model_Setup.md          # Spesifikasjon av hierarkier og datatyper
│   ├── UIA_Controller_Reporting_Suite.md # Detaljert rapport- og visualspesifikasjon
│   └── skills.md                       # Faglig controller-profil og kompetanseoversikt
├── excel/                              # Excel-arbeidsbøker og ledelsesmaler
│   ├── uia_controller_excel_pack.xlsx  # Fullskala integrert controller-arbeidsbok (2.47 MB)
│   └── UIA-Controller-Rapport.xlsx     # Arbeidsbok for ledelsesrapportering
├── scripts/                            # Automatiserings- og QA-skript
│   ├── build_tmdl_model.py             # Genererer TMDL semantisk modell for PBIP
│   ├── validate_model.py               # Validerer referanseintegritet og 0 PK-duplikater
│   └── test_dax_measures.py            # 43 automatiserte tester for DAX og forretningslogikk
├── UIA-Controller-Prosjekt.pbip        # Hovedfil for å åpne prosjektet i Power BI Desktop
├── UIA-Controller-Prosjekt.Report/     # Visuell rapportdefinisjon (PBIR)
├── UIA-Controller-Prosjekt.SemanticModel/ # Semantisk modell i TMDL-format (Fabric DevMode)
├── .gitignore                          # Git-konfigurasjon for Power BI, Excel og Python
└── README.md                           # Denne veiledningen
```

---

## 2. Åpne og Bruke Prosjektet i Power BI Desktop

1.  **Åpne prosjektet**:
    *   Dobbeltklikk på [`UIA-Controller-Prosjekt.pbip`](file:///c:/Users/frank/Desktop/UIA/uia_powerbi_complete_forecast_model/UIA-Controller-Prosjekt.pbip).
    *   Power BI Desktop leser automatisk `UIA-Controller-Prosjekt.SemanticModel` og laster alle 14 tabeller, 22 relasjoner, hierarkier og DAX-mål.
2.  **Oppdatering av data**:
    *   Klikk **Hjem** -> **Oppdater** (**Refresh**) i Power BI Desktop.
3.  **Endre databane (Parameter)**:
    *   Dersom mappen flyttes til en annen datamaskin eller filbane, klikk **Transformer data** -> **Rediger parametere** (**Edit Parameters**), og oppdater parameteren `DataFolder`.

---

## 3. Datamodellens Nøkkeltall & Avstemming (Fullskala Pakke)

Automatisk avstemt og validert med DuckDB ([`scripts/validate_model.py`](file:///c:/Users/frank/Desktop/UIA/uia_powerbi_complete_forecast_model/scripts/validate_model.py) og [`scripts/test_dax_measures.py`](file:///c:/Users/frank/Desktop/UIA/uia_powerbi_complete_forecast_model/scripts/test_dax_measures.py)):

| Område | Måltall | Beløp / Mengde | Kommentar / Integritet |
|---|---|---|---|
| **Regnskap (FactGL)** | Total inntekt | 2 138 486 811,09 NOK | Bevilgning + BOA (35 760 rader) |
| | Totale kostnader | 2 149 103 939,28 NOK | Drifts- og personalkostnader |
| | Netto regnskap | 10 617 128,19 NOK | Netto driftsunderskudd / rammebruk |
| | Lønnskostnader | 1 482 268 875,90 NOK | 68,97 % lønnsandel |
| **Budsjett (FactBudget)** | Netto budsjett (BAC) | 10 747 732,82 NOK | 17 760 budsjettlinjer |
| | Budsjettavvik | -130 604,63 NOK | -1,22 % (mindreforbruk mot budsjett) |
| **Prognoser (FactForecast)**| FC1_2026 (T1) | 35 472 635,98 NOK | 53 280 prognoserader |
| | FC2_2026 (T2) | 35 956 159,17 NOK | Rullende oppdatering |
| | Latest Estimate (LE) | 36 793 524,31 NOK | Gjeldende helårsestimat (EAC) |
| | Forecastavvik mot budsjett| 26 045 791,49 NOK | Forventet merforbruk før tiltak |
| **Tiltak (FactAction)** | Porteføljeomfang | 16 tiltak | 12 åpne, 4 forsinkede |
| | Forventet effekt | -10 005 000,00 NOK | Fullt innsparingspotensial |
| | Realisert effekt | -5 562 081,66 NOK | 55,59 % realiseringsgrad |
| | Forecast etter tiltak | 26 788 524,31 NOK | Netto estimat inkl. tiltak |
| **BOA Prosjekter** | BOA inntekter | 25 678 288,24 NOK | NFR (12,90M), EU (7,43M), Ekstern (5,35M) |
| | BOA andel av inntekter | 1,20 % | Eksternfinansiert andel |
| **Bemanning (FactFTE)** | Årsverk siste mnd | 1 285,93 årsverk | 1 440 rader |
| | Faglige årsverk | 661,77 årsverk | 51,5 % vitenskapelig andel |
| **Utdanning (FactStudyPoints)**| Registrerte studenter | 6 490 studenter | Siste måneds snapshot |
| | Avlagte studiepoeng | 336 945,4 SP | 86,38 % måloppnåelse |
| | SPE60 enheter | 5 615,74 SPE | 9,8 studenter per faglig årsverk |

---

## 4. Kvalitetssikring & Automatisert Testing

Prosjektet inkluderer to automatiserte QA-skript som kjøres lokalt mot DuckDB:

```powershell
# 1. Validering av referanseintegritet, 0 PK-duplikater og 0 fremmednøkkel-orfe:
python scripts/validate_model.py

# 2. Kjøring av 43 automatiserte DAX-tester:
python scripts/test_dax_measures.py
```

Resultat: **43/43 tester består (0 feil)**.

---

## 5. Edward Tufte Visuelle Standarder

Dashbordene følger Edward Tuftes **Data-Ink Ratio**:
*   Ingen vertikale tabellinjer eller unødvendige rutenett i tabeller.
*   Ingen tunge skygger (drop shadows), unødvendige rammer eller pynteikoner på KPI-kort.
*   Direkte merking (direct labeling) på kurver og grafer i stedet for store fargeforklaringer.
*   Fargestyring via heksadesimale DAX-mål: Rød (`#C00000`) for risiko og forsinkelser, Grønn (`#70AD47`) for måloppnåelse, Gul (`#FFC000`) for varsel.
*   Venstrejustert tekst, høyrejusterte tall og beløp med vertikal justering av desimaler.
