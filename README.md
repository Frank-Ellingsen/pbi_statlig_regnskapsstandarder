# UiA Controller - Økonomi & Forecast Datamodell (Power BI / PBIP)

Dette prosjektet inneholder en komplett, produksjonsklar datamodell og controller-løsning for **Universitetet i Agder (UiA)**, utviklet i henhold til beste praksis for virksomhetsstyring, prosjektcontrolling, statlig økonomistyring (SRS) og **Edward Tuftes prinsipper for datavisualisering**.

Løsningen er bygget på **Microsoft Fabric / Power BI Project-formatet (`.pbip` / TMDL)** og støtter versjonskontroll, automatisert testing og modulær DAX-arkitektur.

---

## 1. Mappestruktur & Organisering

Prosjektet er organisert i en ren, profesjonell mappestruktur:

```text
uia_powerbi_complete_forecast_model/
├── data/                               # Kildata (UTF-8, semikolon-separerte CSV-filer)
│   ├── DimAccount.csv                  # Kontoplan og SRS-regnskapslinjer (17 rader)
│   ├── DimDate.csv                     # Datotabell 2026 med kvartaler og måneder (365 rader)
│   ├── DimForecastVersion.csv          # Prognoseversjoner: BUD2026, FC1, FC2, LE (4 rader)
│   ├── DimOrganization.csv             # Organisasjonsstruktur og koststeder (63 rader)
│   ├── DimPositionGroup.csv            # Stillingsgrupper: vitenskapelig/administrativ (5 rader)
│   ├── DimProject.csv                  # Prosjekter, BOA og finansieringskilder (8 rader)
│   ├── DimStudyProgram.csv             # Studieprogrammer og studienivåer (22 rader)
│   ├── FactBudget.csv                  # Månedsbudsjett 2026 (1 306 rader)
│   ├── FactFTE.csv                     # Årsverk og faglige årsverk (1 260 rader)
│   ├── FactForecast.csv                # Rullende prognoser og tiltakseffekter (3 918 rader)
│   ├── FactGL.csv                      # Hovedbokstransaksjoner og regnskap (2 808 rader)
│   ├── FactStudyPoints.csv             # Studenttall, planlagte og avlagte studiepoeng (264 rader)
│   └── Relationships_Forecast.csv      # Definisjon av 19 relasjoner i stjernemodellen
├── dax/                                # DAX-mål og formelbiblioteker
│   ├── All_Measures_Combined.dax       # Komplett samlet DAX-bibliotek
│   ├── Base_Measures.dax               # Finansielle og aktivitetsbaserte basemål
│   └── Forecast_Measures.dax           # Spesifikke prognose- og tiltaksmål
├── docs/                               # Dokumentasjon og spesifikasjoner
│   ├── Controller - UIA.pdf            # Stillings- og casebeskrivelse for UiA
│   ├── DATA_MODEL_ARCHITECTURE.md      # Teknisk arkitektur, korn, relasjoner og ordbok
│   ├── Forecast_Model_Setup.md         # Regler for forecast- og versjonsmodellering
│   ├── PowerBI_Model_Setup.md          # Spesifikasjon av hierarkier og datatyper
│   └── skills.md                       # Faglig controller-profil og kompetanseoversikt
├── excel/                              # Excel-rapporter og ledelsesmaler
│   └── UIA-Controller-Rapport.xlsx     # Arbeidsbok for ledelsesrapportering
├── scripts/                            # Automatiserings- og valideringsskript
│   ├── build_tmdl_model.py             # Genererer TMDL semantisk modell for PBIP
│   └── validate_model.py               # DuckDB-skript for referanseintegritet og QA
├── UIA-Controller-Prosjekt.pbip        # Hovedfil for å åpne prosjektet i Power BI Desktop
├── UIA-Controller-Prosjekt.Report/     # Visuell rapportdefinisjon (Power BI Report)
├── UIA-Controller-Prosjekt.SemanticModel/ # Semantisk modell i TMDL-format (Fabric DevMode)
├── .gitignore                          # Git-konfigurasjon for Power BI, Excel og Python
└── README.md                           # Denne veiledningen
```

---

## 2. Åpne og Bruke Prosjektet i Power BI Desktop

1.  **Åpne prosjektet**:
    *   Dobbeltklikk på [`UIA-Controller-Prosjekt.pbip`](file:///c:/Users/frank/Desktop/UIA/uia_powerbi_complete_forecast_model/UIA-Controller-Prosjekt.pbip).
    *   Power BI Desktop leser automatisk `UIA-Controller-Prosjekt.SemanticModel` og laster alle 13 tabeller, 19 relasjoner, hierarkier og DAX-mål.
2.  **Oppdatering av data**:
    *   Klikk **Hjem** -> **Oppdater** (**Refresh**) i Power BI Desktop.
3.  **Endre databane (Parameter)**:
    *   Dersom mappen flyttes til en annen datamaskin eller filbane, klikk **Transformer data** -> **Rediger parametere** (**Edit Parameters**), og oppdater parameteren `DataFolder`.

---

## 3. Datamodellens Nøkkeltall & Avstemming (2026)

Automatisk avstemt med DuckDB ([`scripts/validate_model.py`](file:///c:/Users/frank/Desktop/UIA/uia_powerbi_complete_forecast_model/scripts/validate_model.py)):

| Område | Måltall | Beløp / Mengde | Kommentar |
|---|---|---|---|
| **Regnskap (FactGL)** | Total debet | 239 714 929,30 NOK | Kostnader |
| | Total kredit | 12 517 512,28 NOK | Inntekter (snudd fortegn) |
| | Netto regnskap | 227 197 417,02 NOK | 2 808 bilag |
| **Budsjett (FactBudget)** | Budsjett inntekter | 12 526 440,83 NOK | |
| | Budsjett kostnader | 239 937 762,19 NOK | |
| | Netto budsjett | 227 411 321,36 NOK | 1 306 budsjettlinjer |
| **Prognose (FactForecast)** | FC1_2026 (etter april) | 197 699 399,78 NOK | 4 mnd faktisk + 8 mnd estimert |
| | FC2_2026 (etter august) | 162 863 721,23 NOK | 8 mnd faktisk + 4 mnd estimert |
| | LE_2026 (etter oktober) | 144 344 752,39 NOK | 10 mnd faktisk + 2 mnd estimert |
| **Bemanning (FactFTE)** | Sum årsverk | 16 088,94 årsverk | Månedssum (snitt 1 340,75) |
| | Faglige årsverk | 14 471,81 årsverk | 89,9% faglig andel |
| **Utdanning (FactStudyPoints)** | Avlagte studiepoeng | 260 292,3 SP | 84,61% gjennomføring |
| | Planlagte studiepoeng | 307 645,0 SP | |
| | SPE 60 enheter | 4 338,21 SPE | Årsstudentekvivalenter |

---

## 4. Pre-konfigurert Rapportsuite i Power BI (PBIR)

Rapportdefinisjonen i [`UIA-Controller-Prosjekt.Report`](file:///c:/Users/frank/Desktop/UIA/uia_powerbi_complete_forecast_model/UIA-Controller-Prosjekt.Report) er forhåndskonfigurert med de 4 typiske controllersidene for UiA Handelshøyskolen:

1.  **`01 Ledelsesstatus & Totaløkonomi`** (`page_01_ledelse`): Faktisk vs. Budsjett vs. Latest Estimate, organisasjonsdrilldown og SRS-fordeling (Lønn, Drift, Avskrivninger).
2.  **`02 Prognose & Avviksanalyse`** (`page_02_forecast`): Rullende prognoser (FC1, FC2, LE), tiltakseffekter, EVM (BAC, EAC, ETC, VAC) og S-kurve over 12 måneder.
3.  **`03 Prosjektcontrolling & BOA`** (`page_03_boa`): Bidrag- og oppdragsforskning (NFR, EU, Oppdrag), finansieringskilder, indirekte kostnader og prosjektresultater.
4.  **`04 Bemanning & Studiepoeng`** (`page_04_bemanning`): Årsverk (faglige UF vs. teknisk-adm), lønn per årsverk, avlagte studiepoeng, gjennomføringsgrad og kostnad per studentekvivalent (`SPE 60`).

*For fullstendig layout, visuelle feltoppsett og Edward Tufte Data-Ink retningslinjer, se den detaljerte manualen:*  
👉 [**`docs/UIA_Controller_Reporting_Suite.md`**](file:///c:/Users/frank/Desktop/UIA/uia_powerbi_complete_forecast_model/docs/UIA_Controller_Reporting_Suite.md)
