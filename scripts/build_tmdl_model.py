"""
build_tmdl_model.py
-------------------
Generates the complete TMDL semantic model definition for Power BI Desktop (.pbip).
Builds tables, M partitions, hierarchies, relationships, and DAX measures.
"""

import os

def build_model():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sem_dir = os.path.join(base_dir, "UIA-Controller-Prosjekt.SemanticModel", "definition")
    tables_dir = os.path.join(sem_dir, "tables")
    os.makedirs(tables_dir, exist_ok=True)
    
    print(f"Building TMDL definition in: {sem_dir}")

    # 1. model.tmdl
    model_content = """model Model
\tculture: en-US
\tdefaultPowerBIDataSourceVersion: powerBI_V3
\tsourceQueryCulture: nb-NO
\tdataAccessOptions
\t\tlegacyRedirects
\t\treturnErrorValuesAsNull

annotation __PBI_TimeIntelligenceEnabled = 0

annotation PBI_ProTooling = ["DevMode"]

ref table _Measures
ref table DimDate
ref table DimOrganization
ref table DimAccount
ref table DimProject
ref table DimForecastVersion
ref table DimPositionGroup
ref table DimStudyProgram
ref table FactGL
ref table FactBudget
ref table FactForecast
ref table FactFTE
ref table FactStudyPoints

ref cultureInfo en-US
"""
    with open(os.path.join(sem_dir, "model.tmdl"), "w", encoding="utf-8") as f:
        f.write(model_content)

    # 2. expressions.tmdl
    expr_content = """expression DataFolder = "C:\\\\Users\\\\frank\\\\Desktop\\\\UIA\\\\uia_powerbi_complete_forecast_model\\\\data\\\\" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
\tlineageTag: e0000000-0000-0000-0000-000000000001

\tannotation PBI_NavigationStepName = Navigation

\tannotation PBI_ResultType = Text
"""
    with open(os.path.join(sem_dir, "expressions.tmdl"), "w", encoding="utf-8") as f:
        f.write(expr_content)

    # 3. relationships.tmdl
    rel_content = """relationship 00000001-0000-0000-0000-000000000001
\tfromColumn: FactGL.DatoNokkel
\ttoColumn: DimDate.DatoNokkel

relationship 00000001-0000-0000-0000-000000000002
\tfromColumn: FactGL.Organisasjonsnokkel
\ttoColumn: DimOrganization.Organisasjonsnokkel

relationship 00000001-0000-0000-0000-000000000003
\tfromColumn: FactGL.Konto
\ttoColumn: DimAccount.Konto

relationship 00000001-0000-0000-0000-000000000004
\tfromColumn: FactGL.Prosjekt
\ttoColumn: DimProject.Prosjekt

relationship 00000001-0000-0000-0000-000000000005
\tfromColumn: FactBudget.DatoNokkel
\ttoColumn: DimDate.DatoNokkel

relationship 00000001-0000-0000-0000-000000000006
\tfromColumn: FactBudget.Organisasjonsnokkel
\ttoColumn: DimOrganization.Organisasjonsnokkel

relationship 00000001-0000-0000-0000-000000000007
\tfromColumn: FactBudget.Konto
\ttoColumn: DimAccount.Konto

relationship 00000001-0000-0000-0000-000000000008
\tfromColumn: FactBudget.Prosjekt
\ttoColumn: DimProject.Prosjekt

relationship 00000001-0000-0000-0000-000000000009
\tfromColumn: FactFTE.DatoNokkel
\ttoColumn: DimDate.DatoNokkel

relationship 00000001-0000-0000-0000-000000000010
\tfromColumn: FactFTE.Organisasjonsnokkel
\ttoColumn: DimOrganization.Organisasjonsnokkel

relationship 00000001-0000-0000-0000-000000000011
\tfromColumn: FactFTE.Stillingsgruppe
\ttoColumn: DimPositionGroup.Stillingsgruppe

relationship 00000001-0000-0000-0000-000000000012
\tfromColumn: FactStudyPoints.DatoNokkel
\ttoColumn: DimDate.DatoNokkel

relationship 00000001-0000-0000-0000-000000000013
\tfromColumn: FactStudyPoints.Organisasjonsnokkel
\ttoColumn: DimOrganization.Organisasjonsnokkel

relationship 00000001-0000-0000-0000-000000000014
\tfromColumn: FactStudyPoints.Studieprogram
\ttoColumn: DimStudyProgram.Studieprogram

relationship 00000001-0000-0000-0000-000000000015
\tfromColumn: FactForecast.DatoNokkel
\ttoColumn: DimDate.DatoNokkel

relationship 00000001-0000-0000-0000-000000000016
\tfromColumn: FactForecast.Organisasjonsnokkel
\ttoColumn: DimOrganization.Organisasjonsnokkel

relationship 00000001-0000-0000-0000-000000000017
\tfromColumn: FactForecast.Konto
\ttoColumn: DimAccount.Konto

relationship 00000001-0000-0000-0000-000000000018
\tfromColumn: FactForecast.Prosjekt
\ttoColumn: DimProject.Prosjekt

relationship 00000001-0000-0000-0000-000000000019
\tfromColumn: FactForecast.Versjon
\ttoColumn: DimForecastVersion.Versjon
"""
    with open(os.path.join(sem_dir, "relationships.tmdl"), "w", encoding="utf-8") as f:
        f.write(rel_content)

    # 4. _Measures.tmdl
    measures_content = """table _Measures
\tlineageTag: m0000000-0000-0000-0000-000000000001

\tmeasure 'Faktisk belop' = SUM ( FactGL[Belop_signert] )
\t\tformatString: #,##0
\t\tdisplayFolder: 01 Faktisk

\tmeasure 'Faktisk debet' = SUM ( FactGL[Debet] )
\t\tformatString: #,##0
\t\tdisplayFolder: 01 Faktisk

\tmeasure 'Faktisk kredit' = SUM ( FactGL[Kredit] )
\t\tformatString: #,##0
\t\tdisplayFolder: 01 Faktisk

\tmeasure 'Faktisk inntekter' = ```
\t\tCALCULATE (
\t\t    -[Faktisk belop],
\t\t    DimAccount[Kontotype] = "Inntekt"
\t\t)
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 01 Faktisk

\tmeasure 'Faktisk kostnader' = ```
\t\tCALCULATE (
\t\t    [Faktisk belop],
\t\t    DimAccount[Kontotype] = "Kostnad"
\t\t)
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 01 Faktisk

\tmeasure 'Faktisk lonnskostnader' = ```
\t\tCALCULATE (
\t\t    [Faktisk belop],
\t\t    DimAccount[SRS_regnskapslinje] = "Lonnskostnader"
\t\t)
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 01 Faktisk

\tmeasure 'Faktisk driftskostnader' = ```
\t\tCALCULATE (
\t\t    [Faktisk belop],
\t\t    DimAccount[SRS_regnskapslinje] IN { "Andre driftskostnader", "Husleie og lokaler" }
\t\t)
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 01 Faktisk

\tmeasure 'Faktisk YTD' = TOTALYTD ( [Faktisk belop], DimDate[Dato] )
\t\tformatString: #,##0
\t\tdisplayFolder: 01 Faktisk

\tmeasure 'Faktisk inntekter YTD' = TOTALYTD ( [Faktisk inntekter], DimDate[Dato] )
\t\tformatString: #,##0
\t\tdisplayFolder: 01 Faktisk

\tmeasure 'Faktisk kostnader YTD' = TOTALYTD ( [Faktisk kostnader], DimDate[Dato] )
\t\tformatString: #,##0
\t\tdisplayFolder: 01 Faktisk

\tmeasure Budsjett = SUM ( FactBudget[BudsjettBelop] )
\t\tformatString: #,##0
\t\tdisplayFolder: 02 Budsjett

\tmeasure 'Budsjett inntekter' = ```
\t\tCALCULATE (
\t\t    -[Budsjett],
\t\t    DimAccount[Kontotype] = "Inntekt"
\t\t)
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 02 Budsjett

\tmeasure 'Budsjett kostnader' = ```
\t\tCALCULATE (
\t\t    [Budsjett],
\t\t    DimAccount[Kontotype] = "Kostnad"
\t\t)
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 02 Budsjett

\tmeasure 'Budsjett lonnskostnader' = ```
\t\tCALCULATE (
\t\t    [Budsjett],
\t\t    DimAccount[SRS_regnskapslinje] = "Lonnskostnader"
\t\t)
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 02 Budsjett

\tmeasure 'Budsjett YTD' = TOTALYTD ( [Budsjett], DimDate[Dato] )
\t\tformatString: #,##0
\t\tdisplayFolder: 02 Budsjett

\tmeasure Aarsbudsjett = ```
\t\tCALCULATE (
\t\t    [Budsjett],
\t\t    REMOVEFILTERS ( DimDate[MaanedNr], DimDate[Maaned], DimDate[AarMaaned], DimDate[Dato], DimDate[DatoNokkel] )
\t\t)
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 02 Budsjett

\tmeasure 'Forecast belop' = SUM ( FactForecast[ForecastBelop] )
\t\tformatString: #,##0
\t\tdisplayFolder: 03 Forecast & LE

\tmeasure Tiltakseffekt = SUM ( FactForecast[Tiltakseffekt] )
\t\tformatString: #,##0
\t\tdisplayFolder: 03 Forecast & LE

\tmeasure 'Forecast etter tiltak' = [Forecast belop] + [Tiltakseffekt]
\t\tformatString: #,##0
\t\tdisplayFolder: 03 Forecast & LE

\tmeasure 'Valgt forecastversjon' = SELECTEDVALUE ( DimForecastVersion[Versjon], "LE_2026" )
\t\tdisplayFolder: 03 Forecast & LE

\tmeasure 'Gjeldende forecast' = ```
\t\tVAR ValgtVersjon = [Valgt forecastversjon]
\t\tRETURN
\t\t    CALCULATE (
\t\t        [Forecast belop],
\t\t        KEEPFILTERS ( DimForecastVersion[Versjon] = ValgtVersjon )
\t\t    )
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 03 Forecast & LE

\tmeasure 'Gjeldende forecast etter tiltak' = ```
\t\tVAR ValgtVersjon = [Valgt forecastversjon]
\t\tRETURN
\t\t    CALCULATE (
\t\t        [Forecast etter tiltak],
\t\t        KEEPFILTERS ( DimForecastVersion[Versjon] = ValgtVersjon )
\t\t    )
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 03 Forecast & LE

\tmeasure 'Forecast aarsbelop' = ```
\t\tCALCULATE (
\t\t    [Gjeldende forecast],
\t\t    REMOVEFILTERS ( DimDate[MaanedNr], DimDate[Maaned], DimDate[AarMaaned], DimDate[Dato], DimDate[DatoNokkel] )
\t\t)
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 03 Forecast & LE

\tmeasure 'Forecast YTD' = TOTALYTD ( [Gjeldende forecast], DimDate[Dato] )
\t\tformatString: #,##0
\t\tdisplayFolder: 03 Forecast & LE

\tmeasure 'Forecast restaar' = [Forecast aarsbelop] - [Forecast YTD]
\t\tformatString: #,##0
\t\tdisplayFolder: 03 Forecast & LE

\tmeasure 'Latest Estimate' = ```
\t\tCALCULATE (
\t\t    [Forecast belop],
\t\t    DimForecastVersion[Versjon] = "LE_2026"
\t\t)
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 03 Forecast & LE

\tmeasure 'Latest Estimate aarsbelop' = CALCULATE ( [Latest Estimate], REMOVEFILTERS ( DimDate ) )
\t\tformatString: #,##0
\t\tdisplayFolder: 03 Forecast & LE

\tmeasure 'Forecast inntekter' = ```
\t\tCALCULATE (
\t\t    -[Gjeldende forecast],
\t\t    DimAccount[Kontotype] = "Inntekt"
\t\t)
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 03 Forecast & LE

\tmeasure 'Forecast kostnader' = ```
\t\tCALCULATE (
\t\t    [Gjeldende forecast],
\t\t    DimAccount[Kontotype] = "Kostnad"
\t\t)
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 03 Forecast & LE

\tmeasure 'Forecast lonnskostnader' = ```
\t\tCALCULATE (
\t\t    [Gjeldende forecast],
\t\t    DimAccount[SRS_regnskapslinje] = "Lonnskostnader"
\t\t)
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 03 Forecast & LE

\tmeasure 'Forecast BOA inntekter' = ```
\t\tCALCULATE (
\t\t    [Forecast inntekter],
\t\t    DimProject[Finansieringstype] IN { "Bidrag", "Oppdrag" }
\t\t)
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 03 Forecast & LE

\tmeasure 'Forecast BOA andel %' = DIVIDE ( [Forecast BOA inntekter], [Forecast inntekter] )
\t\tformatString: 0.0%
\t\tdisplayFolder: 03 Forecast & LE

\tmeasure 'Avvik mot budsjett' = [Faktisk belop] - [Budsjett]
\t\tformatString: #,##0
\t\tdisplayFolder: 04 Avvik & Analyse

\tmeasure 'Avvik mot budsjett %' = DIVIDE ( [Avvik mot budsjett], ABS ( [Budsjett] ) )
\t\tformatString: 0.0%
\t\tdisplayFolder: 04 Avvik & Analyse

\tmeasure 'Forecast mot budsjett' = [Forecast aarsbelop] - [Aarsbudsjett]
\t\tformatString: #,##0
\t\tdisplayFolder: 04 Avvik & Analyse

\tmeasure 'Forecast mot budsjett %' = DIVIDE ( [Forecast mot budsjett], ABS ( [Aarsbudsjett] ) )
\t\tformatString: 0.0%
\t\tdisplayFolder: 04 Avvik & Analyse

\tmeasure 'Forecast etter tiltak mot budsjett' = ```
\t\tCALCULATE (
\t\t    [Gjeldende forecast etter tiltak],
\t\t    REMOVEFILTERS ( DimDate[MaanedNr], DimDate[Maaned], DimDate[AarMaaned], DimDate[Dato], DimDate[DatoNokkel] )
\t\t) - [Aarsbudsjett]
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 04 Avvik & Analyse

\tmeasure 'Forecast endring fra FC1' = ```
\t\t[Forecast aarsbelop]
\t\t    - CALCULATE (
\t\t        [Forecast belop],
\t\t        DimForecastVersion[Versjon] = "FC1_2026",
\t\t        REMOVEFILTERS ( DimDate )
\t\t    )
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 04 Avvik & Analyse

\tmeasure 'Forecast endring fra FC2' = ```
\t\t[Forecast aarsbelop]
\t\t    - CALCULATE (
\t\t        [Forecast belop],
\t\t        DimForecastVersion[Versjon] = "FC2_2026",
\t\t        REMOVEFILTERS ( DimDate )
\t\t    )
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 04 Avvik & Analyse

\tmeasure 'LE mot budsjett' = [Latest Estimate aarsbelop] - [Aarsbudsjett]
\t\tformatString: #,##0
\t\tdisplayFolder: 04 Avvik & Analyse

\tmeasure 'LE mot budsjett %' = DIVIDE ( [LE mot budsjett], ABS ( [Aarsbudsjett] ) )
\t\tformatString: 0.0%
\t\tdisplayFolder: 04 Avvik & Analyse

\tmeasure Aarsverk = SUM ( FactFTE[Aarsverk] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 05 Bemanning

\tmeasure 'Faglige aarsverk' = SUM ( FactFTE[FagligeAarsverk] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 05 Bemanning

\tmeasure 'Administrative aarsverk' = ```
\t\tCALCULATE (
\t\t    [Aarsverk],
\t\t    DimPositionGroup[Stillingskategori] = "Administrativ"
\t\t)
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 05 Bemanning

\tmeasure 'Aarsverk snitt' = ```
\t\tAVERAGEX (
\t\t    VALUES ( DimDate[AarMaaned] ),
\t\t    [Aarsverk]
\t\t)
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 05 Bemanning

\tmeasure 'Forecast lonn per aarsverk' = DIVIDE ( [Forecast lonnskostnader], [Aarsverk] )
\t\tformatString: #,##0
\t\tdisplayFolder: 05 Bemanning

\tmeasure 'Avlagte studiepoeng' = SUM ( FactStudyPoints[AvlagteStudiepoeng] )
\t\tformatString: #,##0.0
\t\tdisplayFolder: 06 Studiepoeng

\tmeasure 'Planlagte studiepoeng' = SUM ( FactStudyPoints[PlanlagteStudiepoeng] )
\t\tformatString: #,##0.0
\t\tdisplayFolder: 06 Studiepoeng

\tmeasure 'SPE 60' = SUM ( FactStudyPoints[SPE60] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 06 Studiepoeng

\tmeasure 'Registrerte studenter' = SUM ( FactStudyPoints[RegistrerteStudenter] )
\t\tformatString: #,##0
\t\tdisplayFolder: 06 Studiepoeng

\tmeasure 'Gjennomforingsgrad %' = DIVIDE ( [Avlagte studiepoeng], [Planlagte studiepoeng] )
\t\tformatString: 0.0%
\t\tdisplayFolder: 06 Studiepoeng

\tmeasure 'Forecast kostnad per SPE60' = DIVIDE ( [Forecast kostnader], [SPE 60] )
\t\tformatString: #,##0
\t\tdisplayFolder: 06 Studiepoeng

\tmeasure 'Forecast datakvalitet %' = AVERAGE ( FactForecast[Sannsynlighet] )
\t\tformatString: 0.0%
\t\tdisplayFolder: 07 Datakvalitet

\tmeasure 'Forecast faktisk andel %' = ```
\t\tDIVIDE (
\t\t    CALCULATE ( [Forecast belop], FactForecast[Datastatus] = "Faktisk hittil" ),
\t\t    [Forecast belop]
\t\t)
\t\t```
\t\tformatString: 0.0%
\t\tdisplayFolder: 07 Datakvalitet

\tmeasure 'Forecast estimert andel %' = ```
\t\tDIVIDE (
\t\t    CALCULATE ( [Forecast belop], FactForecast[Datastatus] = "Estimert restaar" ),
\t\t    [Forecast belop]
\t\t)
\t\t```
\t\tformatString: 0.0%
\t\tdisplayFolder: 07 Datakvalitet

\tmeasure Forecaststatus = ```
\t\tVAR AvvikPct = [Forecast mot budsjett %]
\t\tRETURN
\t\t    SWITCH (
\t\t        TRUE (),
\t\t        ISBLANK ( AvvikPct ), BLANK (),
\t\t        AvvikPct > 0.05, "Rod",
\t\t        AvvikPct > 0.02, "Gul",
\t\t        AvvikPct < -0.05, "Bla",
\t\t        "Gronn"
\t\t    )
\t\t```
\t\tdisplayFolder: 08 Status & Farger

\tmeasure 'Forecaststatus farge' = ```
\t\tSWITCH (
\t\t    [Forecaststatus],
\t\t    "Rod", "#C00000",
\t\t    "Gul", "#FFC000",
\t\t    "Bla", "#5B9BD5",
\t\t    "Gronn", "#70AD47",
\t\t    "#A6A6A6"
\t\t)
\t\t```
\t\tdisplayFolder: 08 Status & Farger

\tcolumn Placeholder
\t\tdataType: string
\t\tisHidden
\t\tsourceColumn: Placeholder
\t\tsummarizeBy: none

\tpartition _Measures = m
\t\tmode: import
\t\tsource = ```
\t\t\tlet
\t\t\t    Source = #table(type table [Placeholder = text], {{"Placeholder"}})
\t\t\tin
\t\t\t    Source
\t\t\t```
"""
    with open(os.path.join(tables_dir, "_Measures.tmdl"), "w", encoding="utf-8") as f:
        f.write(measures_content)

    # 5. DimDate.tmdl
    dim_date_content = """table DimDate
\tlineageTag: d0000001-0000-0000-0000-000000000001
\tdataCategory: Time

\tcolumn Dato
\t\tdataType: dateTime
\t\tisKey
\t\tformatString: yyyy-MM-dd
\t\tsourceColumn: Dato
\t\tsummarizeBy: none

\tcolumn DatoNokkel
\t\tdataType: int64
\t\tsourceColumn: DatoNokkel
\t\tsummarizeBy: none

\tcolumn Aar
\t\tdataType: int64
\t\tsourceColumn: Aar
\t\tsummarizeBy: none

\tcolumn Kvartal
\t\tdataType: string
\t\tsourceColumn: Kvartal
\t\tsummarizeBy: none

\tcolumn MaanedNr
\t\tdataType: int64
\t\tsourceColumn: MaanedNr
\t\tsummarizeBy: none

\tcolumn Maaned
\t\tdataType: string
\t\tsourceColumn: Maaned
\t\tsortByColumn: MaanedNr
\t\tsummarizeBy: none

\tcolumn AarMaaned
\t\tdataType: string
\t\tsourceColumn: AarMaaned
\t\tsortByColumn: MaanedStart
\t\tsummarizeBy: none

\tcolumn MaanedStart
\t\tdataType: dateTime
\t\tformatString: yyyy-MM-dd
\t\tsourceColumn: MaanedStart
\t\tsummarizeBy: none

\thierarchy Tid
\t\tlineageTag: d0000001-0000-0000-0000-000000000002

\t\tlevel Aar
\t\t\tlineageTag: d0000001-0000-0000-0000-000000000003
\t\t\tcolumn: Aar

\t\tlevel Kvartal
\t\t\tlineageTag: d0000001-0000-0000-0000-000000000004
\t\t\tcolumn: Kvartal

\t\tlevel Maaned
\t\t\tlineageTag: d0000001-0000-0000-0000-000000000005
\t\t\tcolumn: Maaned

\t\tlevel Dato
\t\t\tlineageTag: d0000001-0000-0000-0000-000000000006
\t\t\tcolumn: Dato

\tpartition DimDate = m
\t\tmode: import
\t\tsource = ```
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "DimDate.csv"), [Delimiter=";", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Dato", type date}, {"DatoNokkel", Int64.Type}, {"Aar", Int64.Type}, {"Kvartal", type text}, {"MaanedNr", Int64.Type}, {"Maaned", type text}, {"AarMaaned", type text}, {"MaanedStart", type date}})
\t\t\tin
\t\t\t    #"Changed Type"
\t\t\t```
"""
    with open(os.path.join(tables_dir, "DimDate.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_date_content)

    # 6. DimOrganization.tmdl
    dim_org_content = """table DimOrganization
\tlineageTag: d0000002-0000-0000-0000-000000000001

\tcolumn Organisasjonsnokkel
\t\tdataType: int64
\t\tisKey
\t\tsourceColumn: Organisasjonsnokkel
\t\tsummarizeBy: none

\tcolumn OrgEnhet
\t\tdataType: int64
\t\tsourceColumn: OrgEnhet
\t\tsummarizeBy: none

\tcolumn OrgNavn
\t\tdataType: string
\t\tsourceColumn: OrgNavn
\t\tsummarizeBy: none

\tcolumn Institutt
\t\tdataType: int64
\t\tsourceColumn: Institutt
\t\tsummarizeBy: none

\tcolumn Instituttnavn
\t\tdataType: string
\t\tsourceColumn: Instituttnavn
\t\tsummarizeBy: none

\tcolumn Koststed
\t\tdataType: int64
\t\tsourceColumn: Koststed
\t\tsummarizeBy: none

\tcolumn Koststednavn
\t\tdataType: string
\t\tsourceColumn: Koststednavn
\t\tsummarizeBy: none

\tcolumn Koststedtype
\t\tdataType: string
\t\tsourceColumn: Koststedtype
\t\tsummarizeBy: none

\tcolumn Organisasjonsnivaa
\t\tdataType: string
\t\tsourceColumn: Organisasjonsnivaa
\t\tsummarizeBy: none

\thierarchy 'UiA organisasjon'
\t\tlineageTag: d0000002-0000-0000-0000-000000000002

\t\tlevel OrgNavn
\t\t\tlineageTag: d0000002-0000-0000-0000-000000000003
\t\t\tcolumn: OrgNavn

\t\tlevel Instituttnavn
\t\t\tlineageTag: d0000002-0000-0000-0000-000000000004
\t\t\tcolumn: Instituttnavn

\t\tlevel Koststednavn
\t\t\tlineageTag: d0000002-0000-0000-0000-000000000005
\t\t\tcolumn: Koststednavn

\tpartition DimOrganization = m
\t\tmode: import
\t\tsource = ```
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "DimOrganization.csv"), [Delimiter=";", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Organisasjonsnokkel", Int64.Type}, {"OrgEnhet", Int64.Type}, {"OrgNavn", type text}, {"Institutt", Int64.Type}, {"Instituttnavn", type text}, {"Koststed", Int64.Type}, {"Koststednavn", type text}, {"Koststedtype", type text}, {"Organisasjonsnivaa", type text}})
\t\t\tin
\t\t\t    #"Changed Type"
\t\t\t```
"""
    with open(os.path.join(tables_dir, "DimOrganization.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_org_content)

    # 7. DimAccount.tmdl
    dim_acc_content = """table DimAccount
\tlineageTag: d0000003-0000-0000-0000-000000000001

\tcolumn Konto
\t\tdataType: int64
\t\tisKey
\t\tsourceColumn: Konto
\t\tsummarizeBy: none

\tcolumn Kontonavn
\t\tdataType: string
\t\tsourceColumn: Kontonavn
\t\tsummarizeBy: none

\tcolumn Kontotype
\t\tdataType: string
\t\tsourceColumn: Kontotype
\t\tsummarizeBy: none

\tcolumn SRS_regnskapslinje
\t\tdataType: string
\t\tsourceColumn: SRS_regnskapslinje
\t\tsummarizeBy: none

\thierarchy Konto
\t\tlineageTag: d0000003-0000-0000-0000-000000000002

\t\tlevel SRS_regnskapslinje
\t\t\tlineageTag: d0000003-0000-0000-0000-000000000003
\t\t\tcolumn: SRS_regnskapslinje

\t\tlevel Kontotype
\t\t\tlineageTag: d0000003-0000-0000-0000-000000000004
\t\t\tcolumn: Kontotype

\t\tlevel Kontonavn
\t\t\tlineageTag: d0000003-0000-0000-0000-000000000005
\t\t\tcolumn: Kontonavn

\t\tlevel Konto
\t\t\tlineageTag: d0000003-0000-0000-0000-000000000006
\t\t\tcolumn: Konto

\tpartition DimAccount = m
\t\tmode: import
\t\tsource = ```
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "DimAccount.csv"), [Delimiter=";", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Konto", Int64.Type}, {"Kontonavn", type text}, {"Kontotype", type text}, {"SRS_regnskapslinje", type text}})
\t\t\tin
\t\t\t    #"Changed Type"
\t\t\t```
"""
    with open(os.path.join(tables_dir, "DimAccount.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_acc_content)

    # 8. DimProject.tmdl
    dim_proj_content = """table DimProject
\tlineageTag: d0000004-0000-0000-0000-000000000001

\tcolumn Prosjekt
\t\tdataType: string
\t\tisKey
\t\tsourceColumn: Prosjekt
\t\tsummarizeBy: none

\tcolumn Prosjektnavn
\t\tdataType: string
\t\tsourceColumn: Prosjektnavn
\t\tsummarizeBy: none

\tcolumn Finansieringstype
\t\tdataType: string
\t\tsourceColumn: Finansieringstype
\t\tsummarizeBy: none

\tcolumn Finansieringskilde
\t\tdataType: string
\t\tsourceColumn: Finansieringskilde
\t\tsummarizeBy: none

\tcolumn Prosjektkategori
\t\tdataType: string
\t\tsourceColumn: Prosjektkategori
\t\tsummarizeBy: none

\tcolumn Startaar
\t\tdataType: int64
\t\tsourceColumn: Startaar
\t\tsummarizeBy: none

\tcolumn Sluttaar
\t\tdataType: int64
\t\tsourceColumn: Sluttaar
\t\tsummarizeBy: none

\thierarchy Prosjekt
\t\tlineageTag: d0000004-0000-0000-0000-000000000002

\t\tlevel Finansieringstype
\t\t\tlineageTag: d0000004-0000-0000-0000-000000000003
\t\t\tcolumn: Finansieringstype

\t\tlevel Finansieringskilde
\t\t\tlineageTag: d0000004-0000-0000-0000-000000000004
\t\t\tcolumn: Finansieringskilde

\t\tlevel Prosjektkategori
\t\t\tlineageTag: d0000004-0000-0000-0000-000000000005
\t\t\tcolumn: Prosjektkategori

\t\tlevel Prosjektnavn
\t\t\tlineageTag: d0000004-0000-0000-0000-000000000006
\t\t\tcolumn: Prosjektnavn

\tpartition DimProject = m
\t\tmode: import
\t\tsource = ```
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "DimProject.csv"), [Delimiter=";", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Prosjekt", type text}, {"Prosjektnavn", type text}, {"Finansieringstype", type text}, {"Finansieringskilde", type text}, {"Prosjektkategori", type text}, {"Startaar", Int64.Type}, {"Sluttaar", Int64.Type}})
\t\t\tin
\t\t\t    #"Changed Type"
\t\t\t```
"""
    with open(os.path.join(tables_dir, "DimProject.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_proj_content)

    # 9. DimForecastVersion.tmdl
    dim_fc_content = """table DimForecastVersion
\tlineageTag: d0000005-0000-0000-0000-000000000001

\tcolumn Versjon
\t\tdataType: string
\t\tisKey
\t\tsourceColumn: Versjon
\t\tsummarizeBy: none

\tcolumn Versjonsnavn
\t\tdataType: string
\t\tsourceColumn: Versjonsnavn
\t\tsortByColumn: Sortering
\t\tsummarizeBy: none

\tcolumn Versjonstype
\t\tdataType: string
\t\tsourceColumn: Versjonstype
\t\tsummarizeBy: none

\tcolumn Sortering
\t\tdataType: int64
\t\tsourceColumn: Sortering
\t\tsummarizeBy: none

\tcolumn CutoffDatoNokkel
\t\tdataType: int64
\t\tsourceColumn: CutoffDatoNokkel
\t\tsummarizeBy: none

\tcolumn ErGjeldende
\t\tdataType: int64
\t\tsourceColumn: ErGjeldende
\t\tsummarizeBy: none

\tpartition DimForecastVersion = m
\t\tmode: import
\t\tsource = ```
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "DimForecastVersion.csv"), [Delimiter=";", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Versjon", type text}, {"Versjonsnavn", type text}, {"Versjonstype", type text}, {"Sortering", Int64.Type}, {"CutoffDatoNokkel", Int64.Type}, {"ErGjeldende", Int64.Type}})
\t\t\tin
\t\t\t    #"Changed Type"
\t\t\t```
"""
    with open(os.path.join(tables_dir, "DimForecastVersion.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_fc_content)

    # 10. DimPositionGroup.tmdl
    dim_pos_content = """table DimPositionGroup
\tlineageTag: d0000006-0000-0000-0000-000000000001

\tcolumn Stillingsgruppe
\t\tdataType: string
\t\tisKey
\t\tsourceColumn: Stillingsgruppe
\t\tsummarizeBy: none

\tcolumn Stillingsgruppenavn
\t\tdataType: string
\t\tsourceColumn: Stillingsgruppenavn
\t\tsummarizeBy: none

\tcolumn Stillingskategori
\t\tdataType: string
\t\tsourceColumn: Stillingskategori
\t\tsummarizeBy: none

\tpartition DimPositionGroup = m
\t\tmode: import
\t\tsource = ```
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "DimPositionGroup.csv"), [Delimiter=";", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Stillingsgruppe", type text}, {"Stillingsgruppenavn", type text}, {"Stillingskategori", type text}})
\t\t\tin
\t\t\t    #"Changed Type"
\t\t\t```
"""
    with open(os.path.join(tables_dir, "DimPositionGroup.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_pos_content)

    # 11. DimStudyProgram.tmdl
    dim_sp_content = """table DimStudyProgram
\tlineageTag: d0000007-0000-0000-0000-000000000001

\tcolumn Studieprogram
\t\tdataType: string
\t\tisKey
\t\tsourceColumn: Studieprogram
\t\tsummarizeBy: none

\tcolumn Studieprogramnavn
\t\tdataType: string
\t\tsourceColumn: Studieprogramnavn
\t\tsummarizeBy: none

\tcolumn Studienivaa
\t\tdataType: string
\t\tsourceColumn: Studienivaa
\t\tsummarizeBy: none

\tcolumn NormerteStudiepoeng
\t\tdataType: int64
\t\tsourceColumn: NormerteStudiepoeng
\t\tsummarizeBy: none

\tcolumn Institutt
\t\tdataType: int64
\t\tsourceColumn: Institutt
\t\tsummarizeBy: none

\tcolumn OrgEnhet
\t\tdataType: int64
\t\tsourceColumn: OrgEnhet
\t\tsummarizeBy: none

\tcolumn Status
\t\tdataType: string
\t\tsourceColumn: Status
\t\tsummarizeBy: none

\tcolumn Rapporteringsaar
\t\tdataType: int64
\t\tsourceColumn: Rapporteringsaar
\t\tsummarizeBy: none

\thierarchy Studie
\t\tlineageTag: d0000007-0000-0000-0000-000000000002

\t\tlevel Studienivaa
\t\t\tlineageTag: d0000007-0000-0000-0000-000000000003
\t\t\tcolumn: Studienivaa

\t\tlevel Studieprogramnavn
\t\t\tlineageTag: d0000007-0000-0000-0000-000000000004
\t\t\tcolumn: Studieprogramnavn

\tpartition DimStudyProgram = m
\t\tmode: import
\t\tsource = ```
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "DimStudyProgram.csv"), [Delimiter=";", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Studieprogram", type text}, {"Studieprogramnavn", type text}, {"Studienivaa", type text}, {"NormerteStudiepoeng", Int64.Type}, {"Institutt", Int64.Type}, {"OrgEnhet", Int64.Type}, {"Status", type text}, {"Rapporteringsaar", Int64.Type}})
\t\t\tin
\t\t\t    #"Changed Type"
\t\t\t```
"""
    with open(os.path.join(tables_dir, "DimStudyProgram.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_sp_content)

    # 12. FactGL.tmdl
    fact_gl_content = """table FactGL
\tlineageTag: f0000001-0000-0000-0000-000000000001

\tcolumn Bilag
\t\tdataType: string
\t\tsourceColumn: Bilag
\t\tsummarizeBy: none

\tcolumn DatoNokkel
\t\tdataType: int64
\t\tsourceColumn: DatoNokkel
\t\tsummarizeBy: none

\tcolumn Organisasjonsnokkel
\t\tdataType: int64
\t\tsourceColumn: Organisasjonsnokkel
\t\tsummarizeBy: none

\tcolumn Konto
\t\tdataType: int64
\t\tsourceColumn: Konto
\t\tsummarizeBy: none

\tcolumn Prosjekt
\t\tdataType: string
\t\tsourceColumn: Prosjekt
\t\tsummarizeBy: none

\tcolumn Finansieringskilde
\t\tdataType: string
\t\tsourceColumn: Finansieringskilde
\t\tsummarizeBy: none

\tcolumn Tekst
\t\tdataType: string
\t\tsourceColumn: Tekst
\t\tsummarizeBy: none

\tcolumn Belop_signert
\t\tdataType: double
\t\tformatString: #,##0.00
\t\tsourceColumn: Belop_signert
\t\tsummarizeBy: sum

\tcolumn Debet
\t\tdataType: double
\t\tformatString: #,##0.00
\t\tsourceColumn: Debet
\t\tsummarizeBy: sum

\tcolumn Kredit
\t\tdataType: double
\t\tformatString: #,##0.00
\t\tsourceColumn: Kredit
\t\tsummarizeBy: sum

\tcolumn Valuta
\t\tdataType: string
\t\tsourceColumn: Valuta
\t\tsummarizeBy: none

\tcolumn Datakilde
\t\tdataType: string
\t\tsourceColumn: Datakilde
\t\tsummarizeBy: none

\tpartition FactGL = m
\t\tmode: import
\t\tsource = ```
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "FactGL.csv"), [Delimiter=";", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Bilag", type text}, {"DatoNokkel", Int64.Type}, {"Organisasjonsnokkel", Int64.Type}, {"Konto", Int64.Type}, {"Prosjekt", type text}, {"Finansieringskilde", type text}, {"Tekst", type text}, {"Belop_signert", type number}, {"Debet", type number}, {"Kredit", type number}, {"Valuta", type text}, {"Datakilde", type text}})
\t\t\tin
\t\t\t    #"Changed Type"
\t\t\t```
"""
    with open(os.path.join(tables_dir, "FactGL.tmdl"), "w", encoding="utf-8") as f:
        f.write(fact_gl_content)

    # 13. FactBudget.tmdl
    fact_bgt_content = """table FactBudget
\tlineageTag: f0000002-0000-0000-0000-000000000001

\tcolumn DatoNokkel
\t\tdataType: int64
\t\tsourceColumn: DatoNokkel
\t\tsummarizeBy: none

\tcolumn Organisasjonsnokkel
\t\tdataType: int64
\t\tsourceColumn: Organisasjonsnokkel
\t\tsummarizeBy: none

\tcolumn Konto
\t\tdataType: int64
\t\tsourceColumn: Konto
\t\tsummarizeBy: none

\tcolumn Prosjekt
\t\tdataType: string
\t\tsourceColumn: Prosjekt
\t\tsummarizeBy: none

\tcolumn BudsjettBelop
\t\tdataType: double
\t\tformatString: #,##0.00
\t\tsourceColumn: BudsjettBelop
\t\tsummarizeBy: sum

\tcolumn Scenario
\t\tdataType: string
\t\tsourceColumn: Scenario
\t\tsummarizeBy: none

\tpartition FactBudget = m
\t\tmode: import
\t\tsource = ```
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "FactBudget.csv"), [Delimiter=";", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"DatoNokkel", Int64.Type}, {"Organisasjonsnokkel", Int64.Type}, {"Konto", Int64.Type}, {"Prosjekt", type text}, {"BudsjettBelop", type number}, {"Scenario", type text}})
\t\t\tin
\t\t\t    #"Changed Type"
\t\t\t```
"""
    with open(os.path.join(tables_dir, "FactBudget.tmdl"), "w", encoding="utf-8") as f:
        f.write(fact_bgt_content)

    # 14. FactForecast.tmdl
    fact_fc_content = """table FactForecast
\tlineageTag: f0000003-0000-0000-0000-000000000001

\tcolumn DatoNokkel
\t\tdataType: int64
\t\tsourceColumn: DatoNokkel
\t\tsummarizeBy: none

\tcolumn Organisasjonsnokkel
\t\tdataType: int64
\t\tsourceColumn: Organisasjonsnokkel
\t\tsummarizeBy: none

\tcolumn Konto
\t\tdataType: int64
\t\tsourceColumn: Konto
\t\tsummarizeBy: none

\tcolumn Prosjekt
\t\tdataType: string
\t\tsourceColumn: Prosjekt
\t\tsummarizeBy: none

\tcolumn Versjon
\t\tdataType: string
\t\tsourceColumn: Versjon
\t\tsummarizeBy: none

\tcolumn ForecastBelop
\t\tdataType: double
\t\tformatString: #,##0.00
\t\tsourceColumn: ForecastBelop
\t\tsummarizeBy: sum

\tcolumn Datastatus
\t\tdataType: string
\t\tsourceColumn: Datastatus
\t\tsummarizeBy: none

\tcolumn Sannsynlighet
\t\tdataType: double
\t\tformatString: 0.0%
\t\tsourceColumn: Sannsynlighet
\t\tsummarizeBy: average

\tcolumn Kommentar
\t\tdataType: string
\t\tsourceColumn: Kommentar
\t\tsummarizeBy: none

\tcolumn Tiltakseffekt
\t\tdataType: double
\t\tformatString: #,##0.00
\t\tsourceColumn: Tiltakseffekt
\t\tsummarizeBy: sum

\tpartition FactForecast = m
\t\tmode: import
\t\tsource = ```
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "FactForecast.csv"), [Delimiter=";", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"DatoNokkel", Int64.Type}, {"Organisasjonsnokkel", Int64.Type}, {"Konto", Int64.Type}, {"Prosjekt", type text}, {"Versjon", type text}, {"ForecastBelop", type number}, {"Datastatus", type text}, {"Sannsynlighet", type number}, {"Kommentar", type text}, {"Tiltakseffekt", type number}})
\t\t\tin
\t\t\t    #"Changed Type"
\t\t\t```
"""
    with open(os.path.join(tables_dir, "FactForecast.tmdl"), "w", encoding="utf-8") as f:
        f.write(fact_fc_content)

    # 15. FactFTE.tmdl
    fact_fte_content = """table FactFTE
\tlineageTag: f0000004-0000-0000-0000-000000000001

\tcolumn DatoNokkel
\t\tdataType: int64
\t\tsourceColumn: DatoNokkel
\t\tsummarizeBy: none

\tcolumn Organisasjonsnokkel
\t\tdataType: int64
\t\tsourceColumn: Organisasjonsnokkel
\t\tsummarizeBy: none

\tcolumn Stillingsgruppe
\t\tdataType: string
\t\tsourceColumn: Stillingsgruppe
\t\tsummarizeBy: none

\tcolumn Aarsverk
\t\tdataType: double
\t\tformatString: #,##0.00
\t\tsourceColumn: Aarsverk
\t\tsummarizeBy: sum

\tcolumn FagligeAarsverk
\t\tdataType: double
\t\tformatString: #,##0.00
\t\tsourceColumn: FagligeAarsverk
\t\tsummarizeBy: sum

\tcolumn Scenario
\t\tdataType: string
\t\tsourceColumn: Scenario
\t\tsummarizeBy: none

\tpartition FactFTE = m
\t\tmode: import
\t\tsource = ```
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "FactFTE.csv"), [Delimiter=";", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"DatoNokkel", Int64.Type}, {"Organisasjonsnokkel", Int64.Type}, {"Stillingsgruppe", type text}, {"Aarsverk", type number}, {"FagligeAarsverk", type number}, {"Scenario", type text}})
\t\t\tin
\t\t\t    #"Changed Type"
\t\t\t```
"""
    with open(os.path.join(tables_dir, "FactFTE.tmdl"), "w", encoding="utf-8") as f:
        f.write(fact_fte_content)

    # 16. FactStudyPoints.tmdl
    fact_sp_content = """table FactStudyPoints
\tlineageTag: f0000005-0000-0000-0000-000000000001

\tcolumn DatoNokkel
\t\tdataType: int64
\t\tsourceColumn: DatoNokkel
\t\tsummarizeBy: none

\tcolumn Organisasjonsnokkel
\t\tdataType: int64
\t\tsourceColumn: Organisasjonsnokkel
\t\tsummarizeBy: none

\tcolumn Studieprogram
\t\tdataType: string
\t\tsourceColumn: Studieprogram
\t\tsummarizeBy: none

\tcolumn RegistrerteStudenter
\t\tdataType: int64
\t\tformatString: #,##0
\t\tsourceColumn: RegistrerteStudenter
\t\tsummarizeBy: sum

\tcolumn PlanlagteStudiepoeng
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tsourceColumn: PlanlagteStudiepoeng
\t\tsummarizeBy: sum

\tcolumn AvlagteStudiepoeng
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tsourceColumn: AvlagteStudiepoeng
\t\tsummarizeBy: sum

\tcolumn SPE60
\t\tdataType: double
\t\tformatString: #,##0.00
\t\tsourceColumn: SPE60
\t\tsummarizeBy: sum

\tcolumn BestattAndel
\t\tdataType: double
\t\tformatString: 0.0%
\t\tsourceColumn: BestattAndel
\t\tsummarizeBy: average

\tpartition FactStudyPoints = m
\t\tmode: import
\t\tsource = ```
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "FactStudyPoints.csv"), [Delimiter=";", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"DatoNokkel", Int64.Type}, {"Organisasjonsnokkel", Int64.Type}, {"Studieprogram", type text}, {"RegistrerteStudenter", Int64.Type}, {"PlanlagteStudiepoeng", type number}, {"AvlagteStudiepoeng", type number}, {"SPE60", type number}, {"BestattAndel", type number}})
\t\t\tin
\t\t\t    #"Changed Type"
\t\t\t```
"""
    with open(os.path.join(tables_dir, "FactStudyPoints.tmdl"), "w", encoding="utf-8") as f:
        f.write(fact_sp_content)

    print("Successfully built all TMDL model definitions!")

if __name__ == "__main__":
    build_model()
