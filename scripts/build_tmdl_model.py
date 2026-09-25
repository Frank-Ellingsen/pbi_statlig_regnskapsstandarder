"""
build_tmdl_model.py
-------------------
Generates the complete, production-ready TMDL semantic model definition for Power BI Desktop (.pbip).
Updated for full-scale UiA Controller package with 14 tables, 22 relationships, FactAction,
and 60+ controller DAX measures across 8 display folders.
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
\tsourceQueryCulture: en-US
\tdataAccessOptions
\t\tlegacyRedirects
\t\treturnErrorValuesAsNull

annotation __PBI_TimeIntelligenceEnabled = 0

annotation PBI_ProTooling = ["DevMode"]

annotation PBI_QueryOrder = ["_Measures","DimDate","DimOrganization","DimAccount","DimProject","DimForecastVersion","DimPositionGroup","DimStudyProgram","DimGlossary","FactGL","FactBudget","FactForecast","FactFTE","FactStudyPoints","FactAction","FactProjectBOA","FactYearlyReconciliation","DataFolder"]

ref table _Measures
ref table DimDate
ref table DimOrganization
ref table DimAccount
ref table DimProject
ref table DimForecastVersion
ref table DimPositionGroup
ref table DimStudyProgram
ref table DimGlossary
ref table FactGL
ref table FactBudget
ref table FactForecast
ref table FactFTE
ref table FactStudyPoints
ref table FactAction
ref table FactProjectBOA
ref table FactYearlyReconciliation

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

    # 3. relationships.tmdl (22 active relationships)
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
\tfromColumn: FactForecast.DatoNokkel
\ttoColumn: DimDate.DatoNokkel

relationship 00000001-0000-0000-0000-000000000010
\tfromColumn: FactForecast.Organisasjonsnokkel
\ttoColumn: DimOrganization.Organisasjonsnokkel

relationship 00000001-0000-0000-0000-000000000011
\tfromColumn: FactForecast.Konto
\ttoColumn: DimAccount.Konto

relationship 00000001-0000-0000-0000-000000000012
\tfromColumn: FactForecast.Prosjekt
\ttoColumn: DimProject.Prosjekt

relationship 00000001-0000-0000-0000-000000000013
\tfromColumn: FactForecast.Versjon
\ttoColumn: DimForecastVersion.Versjon

relationship 00000001-0000-0000-0000-000000000014
\tfromColumn: FactFTE.DatoNokkel
\ttoColumn: DimDate.DatoNokkel

relationship 00000001-0000-0000-0000-000000000015
\tfromColumn: FactFTE.Organisasjonsnokkel
\ttoColumn: DimOrganization.Organisasjonsnokkel

relationship 00000001-0000-0000-0000-000000000016
\tfromColumn: FactFTE.Stillingsgruppe
\ttoColumn: DimPositionGroup.Stillingsgruppe

relationship 00000001-0000-0000-0000-000000000017
\tfromColumn: FactStudyPoints.DatoNokkel
\ttoColumn: DimDate.DatoNokkel

relationship 00000001-0000-0000-0000-000000000018
\tfromColumn: FactStudyPoints.Organisasjonsnokkel
\ttoColumn: DimOrganization.Organisasjonsnokkel

relationship 00000001-0000-0000-0000-000000000019
\tfromColumn: FactStudyPoints.Studieprogram
\ttoColumn: DimStudyProgram.Studieprogram

relationship 00000001-0000-0000-0000-000000000020
\tfromColumn: FactAction.Organisasjonsnokkel
\ttoColumn: DimOrganization.Organisasjonsnokkel

relationship 00000001-0000-0000-0000-000000000021
\tfromColumn: FactAction.Konto
\ttoColumn: DimAccount.Konto

relationship 00000001-0000-0000-0000-000000000022
\tfromColumn: FactAction.Prosjekt
\ttoColumn: DimProject.Prosjekt

relationship 00000001-0000-0000-0000-000000000023
\tfromColumn: FactProjectBOA.Prosjekt
\ttoColumn: DimProject.Prosjekt
"""
    with open(os.path.join(sem_dir, "relationships.tmdl"), "w", encoding="utf-8") as f:
        f.write(rel_content)

    # 4. DimDate.tmdl
    dim_date_content = """table DimDate
\tlineageTag: d0000001-0000-0000-0000-000000000001
\tdataCategory: Time

\tcolumn Dato
\t\tdataType: dateTime
\t\tisKey
\t\tformatString: yyyy-MM-dd
\t\tlineageTag: d0000001-0000-0000-0000-000000000002
\t\tsummarizeBy: none
\t\tsourceColumn: Dato

\tcolumn DatoNokkel
\t\tdataType: int64
\t\tlineageTag: d0000001-0000-0000-0000-000000000003
\t\tsummarizeBy: none
\t\tsourceColumn: DatoNokkel

\tcolumn Aar
\t\tdataType: int64
\t\tlineageTag: d0000001-0000-0000-0000-000000000004
\t\tsummarizeBy: none
\t\tsourceColumn: Aar

\tcolumn Kvartal
\t\tdataType: string
\t\tlineageTag: d0000001-0000-0000-0000-000000000005
\t\tsummarizeBy: none
\t\tsourceColumn: Kvartal

\tcolumn MaanedNr
\t\tdataType: int64
\t\tlineageTag: d0000001-0000-0000-0000-000000000006
\t\tsummarizeBy: none
\t\tsourceColumn: MaanedNr

\tcolumn AarMaaned
\t\tdataType: string
\t\tlineageTag: d0000001-0000-0000-0000-000000000007
\t\tsortByColumn: MaanedStart
\t\tsummarizeBy: none
\t\tsourceColumn: AarMaaned

\tcolumn MaanedStart
\t\tdataType: dateTime
\t\tformatString: yyyy-MM-dd
\t\tlineageTag: d0000001-0000-0000-0000-000000000008
\t\tsummarizeBy: none
\t\tsourceColumn: MaanedStart

\thierarchy Tid
\t\tlineageTag: d0000001-0000-0000-0000-000000000009

\t\tlevel Aar
\t\t\tlineageTag: d0000001-0000-0000-0000-000000000010
\t\t\tcolumn: Aar

\t\tlevel Kvartal
\t\t\tlineageTag: d0000001-0000-0000-0000-000000000011
\t\t\tcolumn: Kvartal

\t\tlevel AarMaaned
\t\t\tlineageTag: d0000001-0000-0000-0000-000000000012
\t\t\tcolumn: AarMaaned

\t\tlevel Dato
\t\t\tlineageTag: d0000001-0000-0000-0000-000000000013
\t\t\tcolumn: Dato

\tpartition DimDate = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "DimDate.csv"), [Delimiter=";", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Dato", type date}, {"DatoNokkel", Int64.Type}, {"Aar", Int64.Type}, {"Kvartal", type text}, {"MaanedNr", Int64.Type}, {"AarMaaned", type text}, {"MaanedStart", type date}}, "en-US")
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    with open(os.path.join(tables_dir, "DimDate.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_date_content)

    # 5. DimOrganization.tmdl
    dim_org_content = """table DimOrganization
\tlineageTag: d0000002-0000-0000-0000-000000000001

\tcolumn Organisasjonsnokkel
\t\tdataType: string
\t\tisKey
\t\tlineageTag: d0000002-0000-0000-0000-000000000002
\t\tsummarizeBy: none
\t\tsourceColumn: Organisasjonsnokkel

\tcolumn Fakultet
\t\tdataType: string
\t\tlineageTag: d0000002-0000-0000-0000-000000000003
\t\tsummarizeBy: none
\t\tsourceColumn: Fakultet

\tcolumn Fakultetsnavn
\t\tdataType: string
\t\tlineageTag: d0000002-0000-0000-0000-000000000004
\t\tsummarizeBy: none
\t\tsourceColumn: Fakultetsnavn

\tcolumn Institutt
\t\tdataType: string
\t\tlineageTag: d0000002-0000-0000-0000-000000000005
\t\tsummarizeBy: none
\t\tsourceColumn: Institutt

\tcolumn Instituttnavn
\t\tdataType: string
\t\tlineageTag: d0000002-0000-0000-0000-000000000006
\t\tsummarizeBy: none
\t\tsourceColumn: Instituttnavn

\tcolumn Koststed
\t\tdataType: string
\t\tlineageTag: d0000002-0000-0000-0000-000000000007
\t\tsummarizeBy: none
\t\tsourceColumn: Koststed

\tcolumn Koststednavn
\t\tdataType: string
\t\tlineageTag: d0000002-0000-0000-0000-000000000008
\t\tsummarizeBy: none
\t\tsourceColumn: Koststednavn

\tcolumn Koststedtype
\t\tdataType: string
\t\tlineageTag: d0000002-0000-0000-0000-000000000009
\t\tsummarizeBy: none
\t\tsourceColumn: Koststedtype

\thierarchy 'Organisasjonshierarki'
\t\tlineageTag: d0000002-0000-0000-0000-000000000010

\t\tlevel Fakultetsnavn
\t\t\tlineageTag: d0000002-0000-0000-0000-000000000011
\t\t\tcolumn: Fakultetsnavn

\t\tlevel Instituttnavn
\t\t\tlineageTag: d0000002-0000-0000-0000-000000000012
\t\t\tcolumn: Instituttnavn

\t\tlevel Koststednavn
\t\t\tlineageTag: d0000002-0000-0000-0000-000000000013
\t\t\tcolumn: Koststednavn

\tpartition DimOrganization = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "DimOrganization.csv"), [Delimiter=";", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Organisasjonsnokkel", type text}, {"Fakultet", type text}, {"Fakultetsnavn", type text}, {"Institutt", type text}, {"Instituttnavn", type text}, {"Koststed", type text}, {"Koststednavn", type text}, {"Koststedtype", type text}}, "en-US")
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    with open(os.path.join(tables_dir, "DimOrganization.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_org_content)

    # 6. DimAccount.tmdl
    dim_acc_content = """table DimAccount
\tlineageTag: d0000003-0000-0000-0000-000000000001

\tcolumn Konto
\t\tdataType: int64
\t\tisKey
\t\tlineageTag: d0000003-0000-0000-0000-000000000002
\t\tsummarizeBy: none
\t\tsourceColumn: Konto

\tcolumn StandardKonto3
\t\tdataType: int64
\t\tlineageTag: d0000003-0000-0000-0000-000000000003
\t\tsummarizeBy: none
\t\tsourceColumn: StandardKonto3

\tcolumn Kontonavn
\t\tdataType: string
\t\tlineageTag: d0000003-0000-0000-0000-000000000004
\t\tsummarizeBy: none
\t\tsourceColumn: Kontonavn

\tcolumn Kontoklasse
\t\tdataType: int64
\t\tlineageTag: d0000003-0000-0000-0000-000000000005
\t\tsummarizeBy: none
\t\tsourceColumn: Kontoklasse

\tcolumn Kontogruppe
\t\tdataType: int64
\t\tlineageTag: d0000003-0000-0000-0000-000000000006
\t\tsummarizeBy: none
\t\tsourceColumn: Kontogruppe

\tcolumn Kontotype
\t\tdataType: string
\t\tlineageTag: d0000003-0000-0000-0000-000000000007
\t\tsummarizeBy: none
\t\tsourceColumn: Kontotype

\tcolumn SRS_regnskapslinje
\t\tdataType: string
\t\tlineageTag: d0000003-0000-0000-0000-000000000008
\t\tsummarizeBy: none
\t\tsourceColumn: SRS_regnskapslinje

\tcolumn AktuellFor
\t\tdataType: string
\t\tlineageTag: d0000003-0000-0000-0000-000000000009
\t\tsummarizeBy: none
\t\tsourceColumn: AktuellFor

\thierarchy Kontohierarki
\t\tlineageTag: d0000003-0000-0000-0000-000000000010

\t\tlevel SRS_regnskapslinje
\t\t\tlineageTag: d0000003-0000-0000-0000-000000000011
\t\t\tcolumn: SRS_regnskapslinje

\t\tlevel Kontotype
\t\t\tlineageTag: d0000003-0000-0000-0000-000000000012
\t\t\tcolumn: Kontotype

\t\tlevel Kontonavn
\t\t\tlineageTag: d0000003-0000-0000-0000-000000000013
\t\t\tcolumn: Kontonavn

\t\tlevel Konto
\t\t\tlineageTag: d0000003-0000-0000-0000-000000000014
\t\t\tcolumn: Konto

\tpartition DimAccount = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "DimAccount.csv"), [Delimiter=";", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Konto", Int64.Type}, {"StandardKonto3", Int64.Type}, {"Kontonavn", type text}, {"Kontoklasse", Int64.Type}, {"Kontogruppe", Int64.Type}, {"Kontotype", type text}, {"SRS_regnskapslinje", type text}, {"AktuellFor", type text}}, "en-US")
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    with open(os.path.join(tables_dir, "DimAccount.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_acc_content)

    # 7. DimProject.tmdl
    dim_proj_content = """table DimProject
\tlineageTag: d0000004-0000-0000-0000-000000000001

\tcolumn Prosjekt
\t\tdataType: string
\t\tisKey
\t\tlineageTag: d0000004-0000-0000-0000-000000000002
\t\tsummarizeBy: none
\t\tsourceColumn: Prosjekt

\tcolumn Prosjektnavn
\t\tdataType: string
\t\tlineageTag: d0000004-0000-0000-0000-000000000003
\t\tsummarizeBy: none
\t\tsourceColumn: Prosjektnavn

\tcolumn Finansieringstype
\t\tdataType: string
\t\tlineageTag: d0000004-0000-0000-0000-000000000004
\t\tsummarizeBy: none
\t\tsourceColumn: Finansieringstype

\tcolumn Finansieringskilde
\t\tdataType: string
\t\tlineageTag: d0000004-0000-0000-0000-000000000005
\t\tsummarizeBy: none
\t\tsourceColumn: Finansieringskilde

\tcolumn Prosjektkategori
\t\tdataType: string
\t\tlineageTag: d0000004-0000-0000-0000-000000000006
\t\tsummarizeBy: none
\t\tsourceColumn: Prosjektkategori

\thierarchy Prosjekthierarki
\t\tlineageTag: d0000004-0000-0000-0000-000000000007

\t\tlevel Finansieringstype
\t\t\tlineageTag: d0000004-0000-0000-0000-000000000008
\t\t\tcolumn: Finansieringstype

\t\tlevel Finansieringskilde
\t\t\tlineageTag: d0000004-0000-0000-0000-000000000009
\t\t\tcolumn: Finansieringskilde

\t\tlevel Prosjektkategori
\t\t\tlineageTag: d0000004-0000-0000-0000-000000000010
\t\t\tcolumn: Prosjektkategori

\t\tlevel Prosjektnavn
\t\t\tlineageTag: d0000004-0000-0000-0000-000000000011
\t\t\tcolumn: Prosjektnavn

\tpartition DimProject = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "DimProject.csv"), [Delimiter=";", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Prosjekt", type text}, {"Prosjektnavn", type text}, {"Finansieringstype", type text}, {"Finansieringskilde", type text}, {"Prosjektkategori", type text}}, "en-US")
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    with open(os.path.join(tables_dir, "DimProject.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_proj_content)

    # 8. DimForecastVersion.tmdl
    dim_fc_content = """table DimForecastVersion
\tlineageTag: d0000005-0000-0000-0000-000000000001

\tcolumn Versjon
\t\tdataType: string
\t\tisKey
\t\tlineageTag: d0000005-0000-0000-0000-000000000002
\t\tsummarizeBy: none
\t\tsourceColumn: Versjon

\tcolumn Versjonsnavn
\t\tdataType: string
\t\tlineageTag: d0000005-0000-0000-0000-000000000003
\t\tsortByColumn: Sortering
\t\tsummarizeBy: none
\t\tsourceColumn: Versjonsnavn

\tcolumn Sortering
\t\tdataType: int64
\t\tlineageTag: d0000005-0000-0000-0000-000000000004
\t\tsummarizeBy: none
\t\tsourceColumn: Sortering

\tpartition DimForecastVersion = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "DimForecastVersion.csv"), [Delimiter=";", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Versjon", type text}, {"Versjonsnavn", type text}, {"Sortering", Int64.Type}}, "en-US")
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    with open(os.path.join(tables_dir, "DimForecastVersion.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_fc_content)

    # 9. DimPositionGroup.tmdl
    dim_pos_content = """table DimPositionGroup
\tlineageTag: d0000006-0000-0000-0000-000000000001

\tcolumn Stillingsgruppe
\t\tdataType: string
\t\tisKey
\t\tlineageTag: d0000006-0000-0000-0000-000000000002
\t\tsummarizeBy: none
\t\tsourceColumn: Stillingsgruppe

\tcolumn Stillingsgruppenavn
\t\tdataType: string
\t\tlineageTag: d0000006-0000-0000-0000-000000000003
\t\tsummarizeBy: none
\t\tsourceColumn: Stillingsgruppenavn

\tcolumn Stillingskategori
\t\tdataType: string
\t\tlineageTag: d0000006-0000-0000-0000-000000000004
\t\tsummarizeBy: none
\t\tsourceColumn: Stillingskategori

\tpartition DimPositionGroup = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "DimPositionGroup.csv"), [Delimiter=";", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Stillingsgruppe", type text}, {"Stillingsgruppenavn", type text}, {"Stillingskategori", type text}}, "en-US")
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    with open(os.path.join(tables_dir, "DimPositionGroup.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_pos_content)

    # 10. DimStudyProgram.tmdl
    dim_sp_content = """table DimStudyProgram
\tlineageTag: d0000007-0000-0000-0000-000000000001

\tcolumn Studieprogram
\t\tdataType: string
\t\tisKey
\t\tlineageTag: d0000007-0000-0000-0000-000000000002
\t\tsummarizeBy: none
\t\tsourceColumn: Studieprogram

\tcolumn Studieprogramnavn
\t\tdataType: string
\t\tlineageTag: d0000007-0000-0000-0000-000000000003
\t\tsummarizeBy: none
\t\tsourceColumn: Studieprogramnavn

\tcolumn Studienivaa
\t\tdataType: string
\t\tlineageTag: d0000007-0000-0000-0000-000000000004
\t\tsummarizeBy: none
\t\tsourceColumn: Studienivaa

\tcolumn NormerteStudiepoeng
\t\tdataType: int64
\t\tlineageTag: d0000007-0000-0000-0000-000000000005
\t\tsummarizeBy: none
\t\tsourceColumn: NormerteStudiepoeng

\tcolumn Institutt
\t\tdataType: string
\t\tlineageTag: d0000007-0000-0000-0000-000000000006
\t\tsummarizeBy: none
\t\tsourceColumn: Institutt

\tcolumn Fakultet
\t\tdataType: string
\t\tlineageTag: d0000007-0000-0000-0000-000000000007
\t\tsummarizeBy: none
\t\tsourceColumn: Fakultet

\thierarchy Studie
\t\tlineageTag: d0000007-0000-0000-0000-000000000008

\t\tlevel Studienivaa
\t\t\tlineageTag: d0000007-0000-0000-0000-000000000009
\t\t\tcolumn: Studienivaa

\t\tlevel Studieprogramnavn
\t\t\tlineageTag: d0000007-0000-0000-0000-000000000010
\t\t\tcolumn: Studieprogramnavn

\tpartition DimStudyProgram = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "DimStudyProgram.csv"), [Delimiter=";", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Studieprogram", type text}, {"Studieprogramnavn", type text}, {"Studienivaa", type text}, {"NormerteStudiepoeng", Int64.Type}, {"Institutt", type text}, {"Fakultet", type text}}, "en-US")
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    with open(os.path.join(tables_dir, "DimStudyProgram.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_sp_content)

    # 10b. DimGlossary.tmdl
    dim_glossary_content = """table DimGlossary
\tlineageTag: d0000008-0000-0000-0000-000000000001

\tcolumn BegrepID
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: d0000008-0000-0000-0000-000000000002
\t\tsummarizeBy: count
\t\tsourceColumn: BegrepID

\t\tannotation SummarizationSetBy = Automatic

\tcolumn Begrep
\t\tdataType: string
\t\tisKey
\t\tlineageTag: d0000008-0000-0000-0000-000000000003
\t\tsummarizeBy: none
\t\tsourceColumn: Begrep

\tcolumn FulltNavn
\t\tdataType: string
\t\tlineageTag: d0000008-0000-0000-0000-000000000004
\t\tsummarizeBy: none
\t\tsourceColumn: FulltNavn

\tcolumn Kategori
\t\tdataType: string
\t\tlineageTag: d0000008-0000-0000-0000-000000000005
\t\tsummarizeBy: none
\t\tsourceColumn: Kategori

\tcolumn Definisjon
\t\tdataType: string
\t\tlineageTag: d0000008-0000-0000-0000-000000000006
\t\tsummarizeBy: none
\t\tsourceColumn: Definisjon

\tcolumn PraktiskTolkning
\t\tdataType: string
\t\tlineageTag: d0000008-0000-0000-0000-000000000007
\t\tsummarizeBy: none
\t\tsourceColumn: PraktiskTolkning

\tcolumn FormelDAX
\t\tdataType: string
\t\tlineageTag: d0000008-0000-0000-0000-000000000008
\t\tsummarizeBy: none
\t\tsourceColumn: FormelDAX

\tcolumn RolleKontekst
\t\tdataType: string
\t\tlineageTag: d0000008-0000-0000-0000-000000000009
\t\tsummarizeBy: none
\t\tsourceColumn: RolleKontekst

\tcolumn RelevantRapport
\t\tdataType: string
\t\tlineageTag: d0000008-0000-0000-0000-000000000010
\t\tsummarizeBy: none
\t\tsourceColumn: RelevantRapport

\tpartition DimGlossary = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "DimGlossary.csv"), [Delimiter=";", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"BegrepID", Int64.Type}, {"Begrep", type text}, {"FulltNavn", type text}, {"Kategori", type text}, {"Definisjon", type text}, {"PraktiskTolkning", type text}, {"FormelDAX", type text}, {"RolleKontekst", type text}, {"RelevantRapport", type text}}, "en-US")
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    with open(os.path.join(tables_dir, "DimGlossary.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_glossary_content)

    # 11. FactGL.tmdl
    fact_gl_content = """table FactGL
\tlineageTag: f0000001-0000-0000-0000-000000000001

\tcolumn Bilag
\t\tdataType: string
\t\tlineageTag: f0000001-0000-0000-0000-000000000002
\t\tsummarizeBy: none
\t\tsourceColumn: Bilag

\tcolumn DatoNokkel
\t\tdataType: int64
\t\tlineageTag: f0000001-0000-0000-0000-000000000003
\t\tsummarizeBy: none
\t\tsourceColumn: DatoNokkel

\tcolumn Organisasjonsnokkel
\t\tdataType: string
\t\tlineageTag: f0000001-0000-0000-0000-000000000004
\t\tsummarizeBy: none
\t\tsourceColumn: Organisasjonsnokkel

\tcolumn Konto
\t\tdataType: int64
\t\tlineageTag: f0000001-0000-0000-0000-000000000005
\t\tsummarizeBy: none
\t\tsourceColumn: Konto

\tcolumn Prosjekt
\t\tdataType: string
\t\tlineageTag: f0000001-0000-0000-0000-000000000006
\t\tsummarizeBy: none
\t\tsourceColumn: Prosjekt

\tcolumn Belop_signert
\t\tdataType: decimal
\t\tformatString: #,##0.00
\t\tlineageTag: f0000001-0000-0000-0000-000000000007
\t\tsummarizeBy: sum
\t\tsourceColumn: Belop_signert

\tcolumn Tekst
\t\tdataType: string
\t\tlineageTag: f0000001-0000-0000-0000-000000000008
\t\tsummarizeBy: none
\t\tsourceColumn: Tekst

\tcolumn Datakilde
\t\tdataType: string
\t\tlineageTag: f0000001-0000-0000-0000-000000000009
\t\tsummarizeBy: none
\t\tsourceColumn: Datakilde

\tpartition FactGL = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "FactGL.csv"), [Delimiter=";", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Bilag", type text}, {"DatoNokkel", Int64.Type}, {"Organisasjonsnokkel", type text}, {"Konto", Int64.Type}, {"Prosjekt", type text}, {"Belop_signert", Currency.Type}, {"Tekst", type text}, {"Datakilde", type text}}, "en-US")
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    with open(os.path.join(tables_dir, "FactGL.tmdl"), "w", encoding="utf-8") as f:
        f.write(fact_gl_content)

    # 12. FactBudget.tmdl
    fact_budget_content = """table FactBudget
\tlineageTag: f0000002-0000-0000-0000-000000000001

\tcolumn DatoNokkel
\t\tdataType: int64
\t\tlineageTag: f0000002-0000-0000-0000-000000000002
\t\tsummarizeBy: none
\t\tsourceColumn: DatoNokkel

\tcolumn Organisasjonsnokkel
\t\tdataType: string
\t\tlineageTag: f0000002-0000-0000-0000-000000000003
\t\tsummarizeBy: none
\t\tsourceColumn: Organisasjonsnokkel

\tcolumn Konto
\t\tdataType: int64
\t\tlineageTag: f0000002-0000-0000-0000-000000000004
\t\tsummarizeBy: none
\t\tsourceColumn: Konto

\tcolumn Prosjekt
\t\tdataType: string
\t\tlineageTag: f0000002-0000-0000-0000-000000000005
\t\tsummarizeBy: none
\t\tsourceColumn: Prosjekt

\tcolumn BudsjettBelop
\t\tdataType: decimal
\t\tformatString: #,##0.00
\t\tlineageTag: f0000002-0000-0000-0000-000000000006
\t\tsummarizeBy: sum
\t\tsourceColumn: BudsjettBelop

\tcolumn Scenario
\t\tdataType: string
\t\tlineageTag: f0000002-0000-0000-0000-000000000007
\t\tsummarizeBy: none
\t\tsourceColumn: Scenario

\tpartition FactBudget = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "FactBudget.csv"), [Delimiter=";", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"DatoNokkel", Int64.Type}, {"Organisasjonsnokkel", type text}, {"Konto", Int64.Type}, {"Prosjekt", type text}, {"BudsjettBelop", Currency.Type}, {"Scenario", type text}}, "en-US")
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    with open(os.path.join(tables_dir, "FactBudget.tmdl"), "w", encoding="utf-8") as f:
        f.write(fact_budget_content)

    # 13. FactForecast.tmdl
    fact_forecast_content = """table FactForecast
\tlineageTag: f0000003-0000-0000-0000-000000000001

\tcolumn DatoNokkel
\t\tdataType: int64
\t\tlineageTag: f0000003-0000-0000-0000-000000000002
\t\tsummarizeBy: none
\t\tsourceColumn: DatoNokkel

\tcolumn Organisasjonsnokkel
\t\tdataType: string
\t\tlineageTag: f0000003-0000-0000-0000-000000000003
\t\tsummarizeBy: none
\t\tsourceColumn: Organisasjonsnokkel

\tcolumn Konto
\t\tdataType: int64
\t\tlineageTag: f0000003-0000-0000-0000-000000000004
\t\tsummarizeBy: none
\t\tsourceColumn: Konto

\tcolumn Prosjekt
\t\tdataType: string
\t\tlineageTag: f0000003-0000-0000-0000-000000000005
\t\tsummarizeBy: none
\t\tsourceColumn: Prosjekt

\tcolumn Versjon
\t\tdataType: string
\t\tlineageTag: f0000003-0000-0000-0000-000000000006
\t\tsummarizeBy: none
\t\tsourceColumn: Versjon

\tcolumn ForecastBelop
\t\tdataType: decimal
\t\tformatString: #,##0.00
\t\tlineageTag: f0000003-0000-0000-0000-000000000007
\t\tsummarizeBy: sum
\t\tsourceColumn: ForecastBelop

\tcolumn Datastatus
\t\tdataType: string
\t\tlineageTag: f0000003-0000-0000-0000-000000000008
\t\tsummarizeBy: none
\t\tsourceColumn: Datastatus

\tcolumn Sannsynlighet
\t\tdataType: double
\t\tformatString: 0.0%
\t\tlineageTag: f0000003-0000-0000-0000-000000000009
\t\tsummarizeBy: average
\t\tsourceColumn: Sannsynlighet

\tcolumn Kommentar
\t\tdataType: string
\t\tlineageTag: f0000003-0000-0000-0000-000000000010
\t\tsummarizeBy: none
\t\tsourceColumn: Kommentar

\tpartition FactForecast = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "FactForecast.csv"), [Delimiter=";", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"DatoNokkel", Int64.Type}, {"Organisasjonsnokkel", type text}, {"Konto", Int64.Type}, {"Prosjekt", type text}, {"Versjon", type text}, {"ForecastBelop", Currency.Type}, {"Datastatus", type text}, {"Sannsynlighet", type number}, {"Kommentar", type text}}, "en-US")
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    with open(os.path.join(tables_dir, "FactForecast.tmdl"), "w", encoding="utf-8") as f:
        f.write(fact_forecast_content)

    # 14. FactFTE.tmdl
    fact_fte_content = """table FactFTE
\tlineageTag: f0000004-0000-0000-0000-000000000001

\tcolumn DatoNokkel
\t\tdataType: int64
\t\tlineageTag: f0000004-0000-0000-0000-000000000002
\t\tsummarizeBy: none
\t\tsourceColumn: DatoNokkel

\tcolumn Organisasjonsnokkel
\t\tdataType: string
\t\tlineageTag: f0000004-0000-0000-0000-000000000003
\t\tsummarizeBy: none
\t\tsourceColumn: Organisasjonsnokkel

\tcolumn Stillingsgruppe
\t\tdataType: string
\t\tlineageTag: f0000004-0000-0000-0000-000000000004
\t\tsummarizeBy: none
\t\tsourceColumn: Stillingsgruppe

\tcolumn Aarsverk
\t\tdataType: decimal
\t\tformatString: #,##0.00
\t\tlineageTag: f0000004-0000-0000-0000-000000000005
\t\tsummarizeBy: sum
\t\tsourceColumn: Aarsverk

\tcolumn FagligeAarsverk
\t\tdataType: decimal
\t\tformatString: #,##0.00
\t\tlineageTag: f0000004-0000-0000-0000-000000000006
\t\tsummarizeBy: sum
\t\tsourceColumn: FagligeAarsverk

\tcolumn Scenario
\t\tdataType: string
\t\tlineageTag: f0000004-0000-0000-0000-000000000007
\t\tsummarizeBy: none
\t\tsourceColumn: Scenario

\tpartition FactFTE = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "FactFTE.csv"), [Delimiter=";", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"DatoNokkel", Int64.Type}, {"Organisasjonsnokkel", type text}, {"Stillingsgruppe", type text}, {"Aarsverk", type number}, {"FagligeAarsverk", type number}, {"Scenario", type text}}, "en-US")
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    with open(os.path.join(tables_dir, "FactFTE.tmdl"), "w", encoding="utf-8") as f:
        f.write(fact_fte_content)

    # 15. FactStudyPoints.tmdl
    fact_sp_content = """table FactStudyPoints
\tlineageTag: f0000005-0000-0000-0000-000000000001

\tcolumn DatoNokkel
\t\tdataType: int64
\t\tlineageTag: f0000005-0000-0000-0000-000000000002
\t\tsummarizeBy: none
\t\tsourceColumn: DatoNokkel

\tcolumn Organisasjonsnokkel
\t\tdataType: string
\t\tlineageTag: f0000005-0000-0000-0000-000000000003
\t\tsummarizeBy: none
\t\tsourceColumn: Organisasjonsnokkel

\tcolumn Studieprogram
\t\tdataType: string
\t\tlineageTag: f0000005-0000-0000-0000-000000000004
\t\tsummarizeBy: none
\t\tsourceColumn: Studieprogram

\tcolumn RegistrerteStudenter
\t\tdataType: int64
\t\tlineageTag: f0000005-0000-0000-0000-000000000005
\t\tsummarizeBy: sum
\t\tsourceColumn: RegistrerteStudenter

\tcolumn PlanlagteStudiepoeng
\t\tdataType: int64
\t\tlineageTag: f0000005-0000-0000-0000-000000000006
\t\tsummarizeBy: sum
\t\tsourceColumn: PlanlagteStudiepoeng

\tcolumn AvlagteStudiepoeng
\t\tdataType: decimal
\t\tformatString: #,##0.0
\t\tlineageTag: f0000005-0000-0000-0000-000000000007
\t\tsummarizeBy: sum
\t\tsourceColumn: AvlagteStudiepoeng

\tcolumn SPE60
\t\tdataType: decimal
\t\tformatString: #,##0.00
\t\tlineageTag: f0000005-0000-0000-0000-000000000008
\t\tsummarizeBy: sum
\t\tsourceColumn: SPE60

\tcolumn BestattAndel
\t\tdataType: double
\t\tformatString: 0.0%
\t\tlineageTag: f0000005-0000-0000-0000-000000000009
\t\tsummarizeBy: average
\t\tsourceColumn: BestattAndel

\tpartition FactStudyPoints = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "FactStudyPoints.csv"), [Delimiter=";", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"DatoNokkel", Int64.Type}, {"Organisasjonsnokkel", type text}, {"Studieprogram", type text}, {"RegistrerteStudenter", Int64.Type}, {"PlanlagteStudiepoeng", Int64.Type}, {"AvlagteStudiepoeng", type number}, {"SPE60", type number}, {"BestattAndel", type number}}, "en-US")
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    with open(os.path.join(tables_dir, "FactStudyPoints.tmdl"), "w", encoding="utf-8") as f:
        f.write(fact_sp_content)

    # 16. FactAction.tmdl (NEW TABLE)
    fact_action_content = """table FactAction
\tlineageTag: f0000006-0000-0000-0000-000000000001

\tcolumn TiltakID
\t\tdataType: string
\t\tisKey
\t\tlineageTag: f0000006-0000-0000-0000-000000000002
\t\tsummarizeBy: none
\t\tsourceColumn: TiltakID

\tcolumn Organisasjonsnokkel
\t\tdataType: string
\t\tlineageTag: f0000006-0000-0000-0000-000000000003
\t\tsummarizeBy: none
\t\tsourceColumn: Organisasjonsnokkel

\tcolumn Prosjekt
\t\tdataType: string
\t\tlineageTag: f0000006-0000-0000-0000-000000000004
\t\tsummarizeBy: none
\t\tsourceColumn: Prosjekt

\tcolumn Konto
\t\tdataType: int64
\t\tlineageTag: f0000006-0000-0000-0000-000000000005
\t\tsummarizeBy: none
\t\tsourceColumn: Konto

\tcolumn Avviksarsak
\t\tdataType: string
\t\tlineageTag: f0000006-0000-0000-0000-000000000006
\t\tsummarizeBy: none
\t\tsourceColumn: Avviksarsak

\tcolumn Tiltaksbeskrivelse
\t\tdataType: string
\t\tlineageTag: f0000006-0000-0000-0000-000000000007
\t\tsummarizeBy: none
\t\tsourceColumn: Tiltaksbeskrivelse

\tcolumn AnsvarligRolle
\t\tdataType: string
\t\tlineageTag: f0000006-0000-0000-0000-000000000008
\t\tsummarizeBy: none
\t\tsourceColumn: AnsvarligRolle

\tcolumn StartDatoNokkel
\t\tdataType: int64
\t\tlineageTag: f0000006-0000-0000-0000-000000000009
\t\tsummarizeBy: none
\t\tsourceColumn: StartDatoNokkel

\tcolumn FristDatoNokkel
\t\tdataType: int64
\t\tlineageTag: f0000006-0000-0000-0000-000000000010
\t\tsummarizeBy: none
\t\tsourceColumn: FristDatoNokkel

\tcolumn ForventetEffekt
\t\tdataType: decimal
\t\tformatString: #,##0.00
\t\tlineageTag: f0000006-0000-0000-0000-000000000011
\t\tsummarizeBy: sum
\t\tsourceColumn: ForventetEffekt

\tcolumn RealisertEffekt
\t\tdataType: decimal
\t\tformatString: #,##0.00
\t\tlineageTag: f0000006-0000-0000-0000-000000000012
\t\tsummarizeBy: sum
\t\tsourceColumn: RealisertEffekt

\tcolumn Status
\t\tdataType: string
\t\tlineageTag: f0000006-0000-0000-0000-000000000013
\t\tsummarizeBy: none
\t\tsourceColumn: Status

\tcolumn Prioritet
\t\tdataType: string
\t\tlineageTag: f0000006-0000-0000-0000-000000000014
\t\tsummarizeBy: none
\t\tsourceColumn: Prioritet

\tcolumn Sannsynlighet
\t\tdataType: double
\t\tformatString: 0.0%
\t\tlineageTag: f0000006-0000-0000-0000-000000000015
\t\tsummarizeBy: average
\t\tsourceColumn: Sannsynlighet

\tpartition FactAction = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "FactAction.csv"), [Delimiter=";", Columns=14, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"TiltakID", type text}, {"Organisasjonsnokkel", type text}, {"Prosjekt", type text}, {"Konto", Int64.Type}, {"Avviksarsak", type text}, {"Tiltaksbeskrivelse", type text}, {"AnsvarligRolle", type text}, {"StartDatoNokkel", Int64.Type}, {"FristDatoNokkel", Int64.Type}, {"ForventetEffekt", Currency.Type}, {"RealisertEffekt", Currency.Type}, {"Status", type text}, {"Prioritet", type text}, {"Sannsynlighet", type number}}, "en-US")
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    with open(os.path.join(tables_dir, "FactAction.tmdl"), "w", encoding="utf-8") as f:
        f.write(fact_action_content)

    # 17. FactProjectBOA.tmdl
    fact_boa_content = """table FactProjectBOA
\tlineageTag: f0000010-0000-0000-0000-000000000001

\tcolumn Prosjekt
\t\tdataType: string
\t\tisKey
\t\tlineageTag: f0000010-0000-0000-0000-000000000002
\t\tsummarizeBy: none
\t\tsourceColumn: Prosjekt

\tcolumn Prosjektnavn
\t\tdataType: string
\t\tlineageTag: f0000010-0000-0000-0000-000000000003
\t\tsummarizeBy: none
\t\tsourceColumn: Prosjektnavn

\tcolumn Finansieringstype
\t\tdataType: string
\t\tlineageTag: f0000010-0000-0000-0000-000000000004
\t\tsummarizeBy: none
\t\tsourceColumn: Finansieringstype

\tcolumn Finansieringskilde
\t\tdataType: string
\t\tlineageTag: f0000010-0000-0000-0000-000000000005
\t\tsummarizeBy: none
\t\tsourceColumn: Finansieringskilde

\tcolumn Kontraktsbelop
\t\tdataType: decimal
\t\tformatString: #,##0.00
\t\tlineageTag: f0000010-0000-0000-0000-000000000006
\t\tsummarizeBy: sum
\t\tsourceColumn: Kontraktsbelop

\tcolumn Budsjett
\t\tdataType: decimal
\t\tformatString: #,##0.00
\t\tlineageTag: f0000010-0000-0000-0000-000000000007
\t\tsummarizeBy: sum
\t\tsourceColumn: Budsjett

\tcolumn Frikjop
\t\tdataType: decimal
\t\tformatString: #,##0.00
\t\tlineageTag: f0000010-0000-0000-0000-000000000008
\t\tsummarizeBy: sum
\t\tsourceColumn: Frikjop

\tcolumn DirekteDrift
\t\tdataType: decimal
\t\tformatString: #,##0.00
\t\tlineageTag: f0000010-0000-0000-0000-000000000009
\t\tsummarizeBy: sum
\t\tsourceColumn: DirekteDrift

\tcolumn Overhead
\t\tdataType: decimal
\t\tformatString: #,##0.00
\t\tlineageTag: f0000010-0000-0000-0000-000000000010
\t\tsummarizeBy: sum
\t\tsourceColumn: Overhead

\tcolumn Leiested
\t\tdataType: decimal
\t\tformatString: #,##0.00
\t\tlineageTag: f0000010-0000-0000-0000-000000000011
\t\tsummarizeBy: sum
\t\tsourceColumn: Leiested

\tcolumn PåløptKostnad
\t\tdataType: decimal
\t\tformatString: #,##0.00
\t\tlineageTag: f0000010-0000-0000-0000-000000000012
\t\tsummarizeBy: sum
\t\tsourceColumn: PåløptKostnad

\tcolumn Inntektsført
\t\tdataType: decimal
\t\tformatString: #,##0.00
\t\tlineageTag: f0000010-0000-0000-0000-000000000013
\t\tsummarizeBy: sum
\t\tsourceColumn: Inntektsført

\tcolumn Dekningsgrad
\t\tdataType: double
\t\tformatString: 0.0%
\t\tlineageTag: f0000010-0000-0000-0000-000000000014
\t\tsummarizeBy: average
\t\tsourceColumn: Dekningsgrad

\tcolumn '%TidGått'
\t\tdataType: double
\t\tformatString: 0.0%
\t\tlineageTag: f0000010-0000-0000-0000-000000000015
\t\tsummarizeBy: average
\t\tsourceColumn: '%TidGått'

\tcolumn '%BudsjettForbrukt'
\t\tdataType: double
\t\tformatString: 0.0%
\t\tlineageTag: f0000010-0000-0000-0000-000000000016
\t\tsummarizeBy: average
\t\tsourceColumn: '%BudsjettForbrukt'

\tcolumn Forbruksavvik
\t\tdataType: double
\t\tformatString: 0.0%
\t\tlineageTag: f0000010-0000-0000-0000-000000000017
\t\tsummarizeBy: average
\t\tsourceColumn: Forbruksavvik

\tcolumn RAG_Status
\t\tdataType: string
\t\tlineageTag: f0000010-0000-0000-0000-000000000018
\t\tsummarizeBy: none
\t\tsourceColumn: RAG_Status

\tcolumn StatusMerknad
\t\tdataType: string
\t\tlineageTag: f0000010-0000-0000-0000-000000000019
\t\tsummarizeBy: none
\t\tsourceColumn: StatusMerknad

\tpartition FactProjectBOA = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "FactProjectBOA.csv"), [Delimiter=";", Columns=18, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Prosjekt", type text}, {"Prosjektnavn", type text}, {"Finansieringstype", type text}, {"Finansieringskilde", type text}, {"Kontraktsbelop", Currency.Type}, {"Budsjett", Currency.Type}, {"Frikjop", Currency.Type}, {"DirekteDrift", Currency.Type}, {"Overhead", Currency.Type}, {"Leiested", Currency.Type}, {"PåløptKostnad", Currency.Type}, {"Inntektsført", Currency.Type}, {"Dekningsgrad", type number}, {"%TidGått", type number}, {"%BudsjettForbrukt", type number}, {"Forbruksavvik", type number}, {"RAG_Status", type text}, {"StatusMerknad", type text}}, "en-US")
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    with open(os.path.join(tables_dir, "FactProjectBOA.tmdl"), "w", encoding="utf-8") as f:
        f.write(fact_boa_content)

    # 18. FactYearlyReconciliation.tmdl
    fact_recon_content = """table FactYearlyReconciliation
\tlineageTag: f0000008-0000-0000-0000-000000000001

\tcolumn MndNr
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: f0000008-0000-0000-0000-000000000002
\t\tsummarizeBy: none
\t\tsourceColumn: MndNr

\tcolumn Maaned
\t\tdataType: string
\t\tlineageTag: f0000008-0000-0000-0000-000000000003
\t\tsummarizeBy: none
\t\tsourceColumn: Maaned

\tcolumn StatligBevilgning
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000004
\t\tsummarizeBy: sum
\t\tsourceColumn: StatligBevilgning

\tcolumn Forskningsinntekter
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000005
\t\tsummarizeBy: sum
\t\tsourceColumn: Forskningsinntekter

\tcolumn AndreInntekter
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000006
\t\tsummarizeBy: sum
\t\tsourceColumn: AndreInntekter

\tcolumn Lonnskostnader
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000007
\t\tsummarizeBy: sum
\t\tsourceColumn: Lonnskostnader

\tcolumn Driftskostnader
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000008
\t\tsummarizeBy: sum
\t\tsourceColumn: Driftskostnader

\tcolumn InvesteringerCapex
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000009
\t\tsummarizeBy: sum
\t\tsourceColumn: InvesteringerCapex

\tcolumn PlanlagtVerdi_PV
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000010
\t\tsummarizeBy: sum
\t\tsourceColumn: PlanlagtVerdi_PV

\tcolumn OpptjentVerdi_EV
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000011
\t\tsummarizeBy: sum
\t\tsourceColumn: OpptjentVerdi_EV

\tcolumn FaktiskKostnad_AC
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000012
\t\tsummarizeBy: sum
\t\tsourceColumn: FaktiskKostnad_AC

\tcolumn TotalInntekt
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000013
\t\tsummarizeBy: sum
\t\tsourceColumn: TotalInntekt

\tcolumn TotalKostnad
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000014
\t\tsummarizeBy: sum
\t\tsourceColumn: TotalKostnad

\tcolumn NettoResultat
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000015
\t\tsummarizeBy: sum
\t\tsourceColumn: NettoResultat

\tcolumn Kumulativ_Inntekt
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000016
\t\tsummarizeBy: sum
\t\tsourceColumn: Kumulativ_Inntekt

\tcolumn Kumulativ_Kostnad
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000017
\t\tsummarizeBy: sum
\t\tsourceColumn: Kumulativ_Kostnad

\tcolumn Kumulativ_PV
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000018
\t\tsummarizeBy: none
\t\tsourceColumn: Kumulativ_PV

\tcolumn Kumulativ_EV
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000019
\t\tsummarizeBy: none
\t\tsourceColumn: Kumulativ_EV

\tcolumn Kumulativ_AC
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000020
\t\tsummarizeBy: none
\t\tsourceColumn: Kumulativ_AC

\tcolumn Kumulativ_CPI
\t\tdataType: double
\t\tformatString: 0.00
\t\tlineageTag: f0000008-0000-0000-0000-000000000021
\t\tsummarizeBy: none
\t\tsourceColumn: Kumulativ_CPI

\tcolumn Kumulativ_SPI
\t\tdataType: double
\t\tformatString: 0.00
\t\tlineageTag: f0000008-0000-0000-0000-000000000022
\t\tsummarizeBy: none
\t\tsourceColumn: Kumulativ_SPI

\tcolumn Kumulativ_CV
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000023
\t\tsummarizeBy: none
\t\tsourceColumn: Kumulativ_CV

\tcolumn Kumulativ_SV
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000024
\t\tsummarizeBy: none
\t\tsourceColumn: Kumulativ_SV

\tpartition FactYearlyReconciliation = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "FactYearlyReconciliation.csv"), [Delimiter=";", Columns=23, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"MndNr", Int64.Type}, {"Maaned", type text}, {"StatligBevilgning", type number}, {"Forskningsinntekter", type number}, {"AndreInntekter", type number}, {"Lonnskostnader", type number}, {"Driftskostnader", type number}, {"InvesteringerCapex", type number}, {"PlanlagtVerdi_PV", type number}, {"OpptjentVerdi_EV", type number}, {"FaktiskKostnad_AC", type number}, {"TotalInntekt", type number}, {"TotalKostnad", type number}, {"NettoResultat", type number}, {"Kumulativ_Inntekt", type number}, {"Kumulativ_Kostnad", type number}, {"Kumulativ_PV", type number}, {"Kumulativ_EV", type number}, {"Kumulativ_AC", type number}, {"Kumulativ_CPI", type number}, {"Kumulativ_SPI", type number}, {"Kumulativ_CV", type number}, {"Kumulativ_SV", type number}}, "no-NO")
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    with open(os.path.join(tables_dir, "FactYearlyReconciliation.tmdl"), "w", encoding="utf-8") as f:
        f.write(fact_recon_content)

    # 19. _Measures.tmdl (Full Controller DAX Library)
    measures_content = """table _Measures
\tlineageTag: m0000000-0000-0000-0000-000000000001

\tmeasure Regnskap = SUM ( FactGL[Belop_signert] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 01 Okonomi

\tmeasure Budsjett = SUM ( FactBudget[BudsjettBelop] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 01 Okonomi

\tmeasure Avvik = [Regnskap] - [Budsjett]
\t\tformatString: #,##0.00
\t\tdisplayFolder: 01 Okonomi

\tmeasure 'Avvik %' = DIVIDE ( [Avvik], ABS ( [Budsjett] ) )
\t\tformatString: 0.0%
\t\tdisplayFolder: 01 Okonomi

\tmeasure 'Regnskap YTD' = TOTALYTD ( [Regnskap], DimDate[Dato] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 01 Okonomi

\tmeasure 'Budsjett YTD' = TOTALYTD ( [Budsjett], DimDate[Dato] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 01 Okonomi

\tmeasure 'Avvik YTD' = [Regnskap YTD] - [Budsjett YTD]
\t\tformatString: #,##0.00
\t\tdisplayFolder: 01 Okonomi

\tmeasure Inntekter = ```
\t\tCALCULATE (
\t\t    -[Regnskap],
\t\t    DimAccount[Kontotype] = "Inntekt"
\t\t)
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 01 Okonomi

\tmeasure Kostnader = ```
\t\tCALCULATE (
\t\t    [Regnskap],
\t\t    DimAccount[Kontotype] = "Kostnad"
\t\t)
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 01 Okonomi

\tmeasure Lonnskostnader = ```
\t\tCALCULATE (
\t\t    [Regnskap],
\t\t    DimAccount[SRS_regnskapslinje] = "Lonnskostnader"
\t\t)
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 01 Okonomi

\tmeasure 'Lonnandel %' = DIVIDE ( [Lonnskostnader], [Kostnader] )
\t\tformatString: 0.0%
\t\tdisplayFolder: 01 Okonomi

\tmeasure Forecast = SUM ( FactForecast[ForecastBelop] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 02 Forecast

\tmeasure 'Valgt forecastversjon' = SELECTEDVALUE ( DimForecastVersion[Versjon], "LE_2026" )
\t\tdisplayFolder: 02 Forecast

\tmeasure 'Gjeldende forecast' = ```
\t\tVAR V = [Valgt forecastversjon]
\t\tRETURN
\t\t    CALCULATE (
\t\t        [Forecast],
\t\t        KEEPFILTERS ( DimForecastVersion[Versjon] = V )
\t\t    )
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 02 Forecast

\tmeasure Aarsbudsjett = CALCULATE ( [Budsjett], REMOVEFILTERS ( DimDate ) )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 02 Forecast

\tmeasure 'Forecast aarsbelop' = CALCULATE ( [Gjeldende forecast], REMOVEFILTERS ( DimDate ) )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 02 Forecast

\tmeasure Forecastavvik = [Forecast aarsbelop] - [Aarsbudsjett]
\t\tformatString: #,##0.00
\t\tdisplayFolder: 02 Forecast

\tmeasure 'Forecastavvik %' = DIVIDE ( [Forecastavvik], ABS ( [Aarsbudsjett] ) )
\t\tformatString: 0.0%
\t\tdisplayFolder: 02 Forecast

\tmeasure 'Forecast confidence %' = AVERAGE ( FactForecast[Sannsynlighet] )
\t\tformatString: 0.0%
\t\tdisplayFolder: 02 Forecast

\tmeasure FC1 = ```
\t\tCALCULATE (
\t\t    [Forecast],
\t\t    REMOVEFILTERS ( DimForecastVersion ),
\t\t    DimForecastVersion[Versjon] = "FC1_2026",
\t\t    REMOVEFILTERS ( DimDate )
\t\t)
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 02 Forecast

\tmeasure FC2 = ```
\t\tCALCULATE (
\t\t    [Forecast],
\t\t    REMOVEFILTERS ( DimForecastVersion ),
\t\t    DimForecastVersion[Versjon] = "FC2_2026",
\t\t    REMOVEFILTERS ( DimDate )
\t\t)
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 02 Forecast

\tmeasure 'Latest Estimate' = ```
\t\tCALCULATE (
\t\t    [Forecast],
\t\t    REMOVEFILTERS ( DimForecastVersion ),
\t\t    DimForecastVersion[Versjon] = "LE_2026",
\t\t    REMOVEFILTERS ( DimDate )
\t\t)
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 02 Forecast

\tmeasure 'Endring FC2 til LE' = [Latest Estimate] - [FC2]
\t\tformatString: #,##0.00
\t\tdisplayFolder: 02 Forecast

\tmeasure 'Forecast lonn' = ```
\t\tCALCULATE (
\t\t    [Gjeldende forecast],
\t\t    DimAccount[SRS_regnskapslinje] = "Lonnskostnader"
\t\t)
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 02 Forecast

\tmeasure Aarsverk = ```
\t\tVAR D =
\t\t    MAXX (
\t\t        FILTER ( ALLSELECTED ( DimDate ), CALCULATE ( COUNTROWS ( FactFTE ) ) > 0 ),
\t\t        DimDate[DatoNokkel]
\t\t    )
\t\tRETURN
\t\t    CALCULATE ( SUM ( FactFTE[Aarsverk] ), DimDate[DatoNokkel] = D )
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 03 Bemanning & Studier

\tmeasure 'Faglige aarsverk' = ```
\t\tVAR D =
\t\t    MAXX (
\t\t        FILTER ( ALLSELECTED ( DimDate ), CALCULATE ( COUNTROWS ( FactFTE ) ) > 0 ),
\t\t        DimDate[DatoNokkel]
\t\t    )
\t\tRETURN
\t\t    CALCULATE ( SUM ( FactFTE[FagligeAarsverk] ), DimDate[DatoNokkel] = D )
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 03 Bemanning & Studier

\tmeasure 'Registrerte studenter' = ```
\t\tVAR D =
\t\t    MAXX (
\t\t        FILTER ( ALLSELECTED ( DimDate ), CALCULATE ( COUNTROWS ( FactStudyPoints ) ) > 0 ),
\t\t        DimDate[DatoNokkel]
\t\t    )
\t\tRETURN
\t\t    CALCULATE ( SUM ( FactStudyPoints[RegistrerteStudenter] ), DimDate[DatoNokkel] = D )
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 03 Bemanning & Studier

\tmeasure 'Avlagte studiepoeng' = SUM ( FactStudyPoints[AvlagteStudiepoeng] )
\t\tformatString: #,##0.0
\t\tdisplayFolder: 03 Bemanning & Studier

\tmeasure SPE60 = SUM ( FactStudyPoints[SPE60] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 03 Bemanning & Studier

\tmeasure 'Studiepoeng maaloppnaelse %' = DIVIDE ( [Avlagte studiepoeng], SUM ( FactStudyPoints[PlanlagteStudiepoeng] ) )
\t\tformatString: 0.0%
\t\tdisplayFolder: 03 Bemanning & Studier

\tmeasure 'Studenter per faglig aarsverk' = DIVIDE ( [Registrerte studenter], [Faglige aarsverk] )
\t\tformatString: #,##0.0
\t\tdisplayFolder: 03 Bemanning & Studier

\tmeasure 'SPE60 per faglig aarsverk' = DIVIDE ( [SPE60], [Faglige aarsverk] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 03 Bemanning & Studier

\tmeasure 'Kostnad per student' = DIVIDE ( [Kostnader], [Registrerte studenter] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 03 Bemanning & Studier

\tmeasure 'Kostnad per SPE60' = DIVIDE ( [Kostnader], [SPE60] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 03 Bemanning & Studier

\tmeasure 'Lonn per aarsverk' = DIVIDE ( [Lonnskostnader], [Aarsverk] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 03 Bemanning & Studier

\tmeasure 'BOA inntekter' = ```
\t\tCALCULATE (
\t\t    [Inntekter],
\t\t    DimProject[Finansieringstype] IN { "Bidrag", "Oppdrag" }
\t\t)
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 04 BOA

\tmeasure 'NFR inntekter' = ```
\t\tCALCULATE (
\t\t    [Inntekter],
\t\t    DimProject[Finansieringskilde] = "NFR"
\t\t)
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 04 BOA

\tmeasure 'EU inntekter' = ```
\t\tCALCULATE (
\t\t    [Inntekter],
\t\t    DimProject[Finansieringskilde] = "EU"
\t\t)
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 04 BOA

\tmeasure 'BOA andel %' = DIVIDE ( [BOA inntekter], [Inntekter] )
\t\tformatString: 0.0%
\t\tdisplayFolder: 04 BOA

\tmeasure 'BOA per faglig aarsverk' = DIVIDE ( [BOA inntekter], [Faglige aarsverk] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 04 BOA

\tmeasure 'Antall tiltak' = DISTINCTCOUNT ( FactAction[TiltakID] )
\t\tformatString: #,##0
\t\tdisplayFolder: 05 Tiltak

\tmeasure 'Forventet tiltakseffekt' = SUM ( FactAction[ForventetEffekt] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 05 Tiltak

\tmeasure 'Realisert tiltakseffekt' = SUM ( FactAction[RealisertEffekt] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 05 Tiltak

\tmeasure 'Tiltak realiseringsgrad %' = DIVIDE ( [Realisert tiltakseffekt], [Forventet tiltakseffekt] )
\t\tformatString: 0.0%
\t\tdisplayFolder: 05 Tiltak

\tmeasure 'Aapne tiltak' = ```
\t\tCALCULATE (
\t\t    [Antall tiltak],
\t\t    FactAction[Status] <> "Gjennomfort"
\t\t)
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 05 Tiltak

\tmeasure 'Forsinkede tiltak' = ```
\t\tCALCULATE (
\t\t    [Antall tiltak],
\t\t    FactAction[Status] = "Forsinket"
\t\t)
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 05 Tiltak

\tmeasure 'Forecast etter tiltak' = [Forecast aarsbelop] + [Forventet tiltakseffekt]
\t\tformatString: #,##0.00
\t\tdisplayFolder: 05 Tiltak

\tmeasure 'Restavvik etter tiltak' = [Forecast etter tiltak] - [Aarsbudsjett]
\t\tformatString: #,##0.00
\t\tdisplayFolder: 05 Tiltak

\tmeasure 'Tiltaksdekning av avvik %' = DIVIDE ( ABS ( [Forventet tiltakseffekt] ), ABS ( [Forecastavvik] ) )
\t\tformatString: 0.0%
\t\tdisplayFolder: 05 Tiltak

\tmeasure 'BAC (Budget at Completion)' = [Aarsbudsjett]
\t\tformatString: #,##0.00
\t\tdisplayFolder: 06 EVM Prosjekt

\tmeasure 'EAC (Estimate at Completion)' = [Forecast aarsbelop]
\t\tformatString: #,##0.00
\t\tdisplayFolder: 06 EVM Prosjekt

\tmeasure 'ETC (Estimate to Complete)' = [Forecast aarsbelop] - TOTALYTD ( [Gjeldende forecast], DimDate[Dato] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 06 EVM Prosjekt

\tmeasure 'VAC (Variance at Completion)' = [BAC (Budget at Completion)] - [EAC (Estimate at Completion)]
\t\tformatString: #,##0.00
\t\tdisplayFolder: 06 EVM Prosjekt

\tmeasure 'VAC %' = DIVIDE ( [VAC (Variance at Completion)], [BAC (Budget at Completion)] )
\t\tformatString: 0.0%
\t\tdisplayFolder: 06 EVM Prosjekt

\tmeasure Forecaststatus = ```
\t\tVAR AvvikPct = [Forecastavvik %]
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
\t\tdisplayFolder: 07 Status & Farger

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
\t\tdisplayFolder: 07 Status & Farger

\tmeasure 'Forecast RAG Status' = ```
\t\tVAR AvvikPct = [Forecastavvik %]
\t\tRETURN
\t\t    SWITCH (
\t\t        TRUE (),
\t\t        ISBLANK ( AvvikPct ), BLANK (),
\t\t        AvvikPct > 0.05, "🔴 Rød (>5%)",
\t\t        AvvikPct > 0.02, "🟡 Gul (2-5%)",
\t\t        "🟢 Grønn (<=2%)"
\t\t    )
\t\t```
\t\tdisplayFolder: 07 Status & Farger

\tmeasure 'Avvik YTD RAG Status' = ```
\t\tVAR AvvikPct = [Avvik YTD %]
\t\tRETURN
\t\t    SWITCH (
\t\t        TRUE (),
\t\t        ISBLANK ( AvvikPct ), BLANK (),
\t\t        AvvikPct > 0.05, "🔴 Rød (>5%)",
\t\t        AvvikPct > 0.02, "🟡 Gul (2-5%)",
\t\t        "🟢 Grønn (<=2%)"
\t\t    )
\t\t```
\t\tdisplayFolder: 07 Status & Farger

\tmeasure 'Tiltak RAG Status' = ```
\t\tVAR S = SELECTEDVALUE ( FactAction[Status] )
\t\tRETURN
\t\t    SWITCH (
\t\t        S,
\t\t        "Gjennomfort", "🟢 Gjennomført",
\t\t        "Pagar", "🟡 Pågår",
\t\t        "Forsinket", "🔴 Forsinket",
\t\t        "⚪ Planlagt"
\t\t    )
\t\t```
\t\tdisplayFolder: 07 Status & Farger

\tmeasure 'Studiepoeng RAG Status' = ```
\t\tVAR M = [Studiepoeng maaloppnaelse %]
\t\tRETURN
\t\t    SWITCH (
\t\t        TRUE (),
\t\t        ISBLANK ( M ), BLANK (),
\t\t        M >= 0.90, "🟢 Mål nådd (>=90%)",
\t\t        M >= 0.80, "🟡 Moderat (80-90%)",
\t\t        "🔴 Lav (<80%)"
\t\t    )
\t\t```
\t\tdisplayFolder: 07 Status & Farger

\tmeasure 'EVM Sluttavvik RAG Status' = ```
\t\tVAR V = [VAC %]
\t\tRETURN
\t\t    SWITCH (
\t\t        TRUE (),
\t\t        ISBLANK ( V ), BLANK (),
\t\t        V >= 0, "🟢 Under budsjett",
\t\t        V >= -0.05, "🟡 Moderat overskridelse",
\t\t        "🔴 Kritisk overskridelse"
\t\t    )
\t\t```
\t\tdisplayFolder: 07 Status & Farger

\tmeasure 'Antall rode institutter' = ```
\t\tCALCULATE (
\t\t    DISTINCTCOUNT ( DimOrganization[Instituttnavn] ),
\t\t    FILTER (
\t\t        VALUES ( DimOrganization[Instituttnavn] ),
\t\t        [Forecastavvik %] > 0.05
\t\t    )
\t\t)
\t\t```
\t\tformatString: #,##0
\t\tdisplayFolder: 07 Status & Farger

\tmeasure 'Avvik RAG farge' = ```
\t\tVAR AvvikPct = [Avvik YTD %]
\t\tRETURN
\t\t    SWITCH (
\t\t        TRUE (),
\t\t        ISBLANK ( AvvikPct ), "#A6A6A6",
\t\t        AvvikPct > 0.05, "#C00000",
\t\t        AvvikPct > 0.02, "#FFC000",
\t\t        "#70AD47"
\t\t    )
\t\t```
\t\tdisplayFolder: 07 Status & Farger

\tmeasure 'Tiltak RAG farge' = ```
\t\tVAR S = SELECTEDVALUE ( FactAction[Status] )
\t\tRETURN
\t\t    SWITCH (
\t\t        S,
\t\t        "Gjennomfort", "#70AD47",
\t\t        "Pagar", "#FFC000",
\t\t        "Forsinket", "#C00000",
\t\t        "#A6A6A6"
\t\t    )
\t\t```
\t\tdisplayFolder: 07 Status & Farger

\tmeasure 'Studiepoeng RAG farge' = ```
\t\tVAR M = [Studiepoeng maaloppnaelse %]
\t\tRETURN
\t\t    SWITCH (
\t\t        TRUE (),
\t\t        ISBLANK ( M ), "#A6A6A6",
\t\t        M >= 0.90, "#70AD47",
\t\t        M >= 0.80, "#FFC000",
\t\t        "#C00000"
\t\t    )
\t\t```
\t\tdisplayFolder: 07 Status & Farger

\tmeasure 'EVM Sluttavvik RAG farge' = ```
\t\tVAR V = [VAC %]
\t\tRETURN
\t\t    SWITCH (
\t\t        TRUE (),
\t\t        ISBLANK ( V ), "#A6A6A6",
\t\t        V >= 0, "#70AD47",
\t\t        V >= -0.05, "#FFC000",
\t\t        "#C00000"
\t\t    )
\t\t```
\t\tdisplayFolder: 07 Status & Farger

\tmeasure 'Avvik YTD %' = DIVIDE ( [Avvik YTD], ABS ( [Budsjett YTD] ) )
\t\tformatString: 0.0%
\t\tdisplayFolder: 01 Okonomi

\tmeasure 'Forecast lonnsavvik' = [Forecast lonn] - CALCULATE ( [Aarsbudsjett], DimAccount[SRS_regnskapslinje] = "Lonnskostnader" )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 02 Forecast

\tmeasure 'Absolutt forecastavvik' = ABS ( [Forecastavvik] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 02 Forecast

\tmeasure 'Antall begreper' = COUNTROWS ( DimGlossary )
\t\tformatString: #,##0
\t\tdisplayFolder: 09 Begrepskatalog

\tmeasure 'Antall begrepskategorier' = DISTINCTCOUNT ( DimGlossary[Kategori] )
\t\tformatString: #,##0
\t\tdisplayFolder: 09 Begrepskatalog

\tmeasure 'Statsbevilgning basis' = ```
\t\tCALCULATE (
\t\t    -[Budsjett],
\t\t    REMOVEFILTERS ( DimDate ),
\t\t    DimAccount[Konto] = 3900
\t\t)
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 10 Regulatorisk & Veileder

\tmeasure 'Maks tillatt reserve 5%' = [Statsbevilgning basis] * 0.05
\t\tformatString: #,##0.00
\t\tdisplayFolder: 10 Regulatorisk & Veileder

\tmeasure 'Beregnet avsetningsandel %' = DIVIDE ( ABS ( [Avvik YTD] ), [Statsbevilgning basis] )
\t\tformatString: 0.000%
\t\tdisplayFolder: 10 Regulatorisk & Veileder

\tmeasure '5 %-regel Status' = ```
\t\tIF (
\t\t    [Beregnet avsetningsandel %] <= 0.05,
\t\t    "🟢 Overholdt (<=5%)",
\t\t    "🔴 Overskredet (>5%)"
\t\t)
\t\t```
\t\tdisplayFolder: 10 Regulatorisk & Veileder

\tmeasure 'KD 2025 SPE Kat 1 Sats' = 54550.0
\t\tformatString: #,##0
\t\tdisplayFolder: 10 Regulatorisk & Veileder

\tmeasure 'KD 2025 SPE Kat 2 Sats' = 81800.0
\t\tformatString: #,##0
\t\tdisplayFolder: 10 Regulatorisk & Veileder

\tmeasure 'KD 2025 SPE Kat 3 Sats' = 190900.0
\t\tformatString: #,##0
\t\tdisplayFolder: 10 Regulatorisk & Veileder

\tmeasure 'SRS 1 Driftsinntekter' = [Inntekter]
\t\tformatString: #,##0.00
\t\tdisplayFolder: 10 Regulatorisk & Veileder

\tmeasure 'SRS 1 Driftskostnader' = [Kostnader]
\t\tformatString: #,##0.00
\t\tdisplayFolder: 10 Regulatorisk & Veileder

\tmeasure 'SRS 1 Netto driftsresultat' = [Kostnader] - [Inntekter]
\t\tformatString: #,##0.00
\t\tdisplayFolder: 10 Regulatorisk & Veileder

\tmeasure 'SRS 10 Bidragsinntekter' = ```
\t\tCALCULATE (
\t\t    [Inntekter],
\t\t    DimProject[Finansieringstype] = "Bidrag"
\t\t)
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 10 Regulatorisk & Veileder

\tmeasure 'SRS 9 Oppdragsinntekter' = ```
\t\tCALCULATE (
\t\t    [Inntekter],
\t\t    DimProject[Finansieringstype] = "Oppdrag"
\t\t)
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 10 Regulatorisk & Veileder

\tmeasure 'SRS 17 Avskrivninger' = ```
\t\tCALCULATE (
\t\t    [Regnskap],
\t\t    DimAccount[SRS_regnskapslinje] = "Av- og nedskrivninger"
\t\t)
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 10 Regulatorisk & Veileder

\tmeasure 'Total Inntekt BAC' = 1433.0
\t\tformatString: #,##0.0 "MNOK"
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Total Kostnad EAC' = 1444.0
\t\tformatString: #,##0.0 "MNOK"
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Helårs Nettoresultat VAC' = -11.0
\t\tformatString: #,##0.0 "MNOK"
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Helårs Earned Value EV' = 1344.0
\t\tformatString: #,##0.0 "MNOK"
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Helårs CPI' = 0.95
\t\tformatString: 0.00
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Helårs SPI' = 0.92
\t\tformatString: 0.00
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Helårs ETC' = 100.0
\t\tformatString: #,##0.0 "MNOK"
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Helårs Capex Andel' = 0.11165
\t\tformatString: 0.0%
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Helårs Lønnsandel' = 0.65876
\t\tformatString: 0.0%
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Helårs Driftsandel' = 0.23726
\t\tformatString: 0.0%
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Kumulativ PV' = AVERAGE ( FactYearlyReconciliation[Kumulativ_PV] )
\t\tformatString: #,##0.0 "MNOK"
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Kumulativ EV' = AVERAGE ( FactYearlyReconciliation[Kumulativ_EV] )
\t\tformatString: #,##0.0 "MNOK"
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Kumulativ AC' = AVERAGE ( FactYearlyReconciliation[Kumulativ_AC] )
\t\tformatString: #,##0.0 "MNOK"
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Månedlig Inntekt' = SUM ( FactYearlyReconciliation[TotalInntekt] )
\t\tformatString: #,##0.0 "MNOK"
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Månedlig Kostnad' = SUM ( FactYearlyReconciliation[TotalKostnad] )
\t\tformatString: #,##0.0 "MNOK"
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Månedlig Nettoresultat' = SUM ( FactYearlyReconciliation[NettoResultat] )
\t\tformatString: #,##0.0 "MNOK"
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure EAC = [EAC (Estimate at Completion)]
\t\tformatString: #,##0.00
\t\tdisplayFolder: 06 EVM

\tmeasure 'BOA Inntekt YTD SRS 10' = ```
\t\tCALCULATE (
\t\t    -[Regnskap],
\t\t    DimAccount[Konto] IN { 3400, 3420 }
\t\t)
\t\t```
\t\tformatString: #,##0.00
\t\tdisplayFolder: 07 BOA Prosjekter

\tmeasure 'TDI Kontraktsbeløp' = SUM ( FactProjectBOA[Kontraktsbelop] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 07 BOA Prosjekter

\tmeasure 'TDI Budsjett' = SUM ( FactProjectBOA[Budsjett] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 07 BOA Prosjekter

\tmeasure 'TDI Frikjøp Beløp' = SUM ( FactProjectBOA[Frikjop] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 07 BOA Prosjekter

\tmeasure 'TDI Direkte Drift Beløp' = SUM ( FactProjectBOA[DirekteDrift] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 07 BOA Prosjekter

\tmeasure 'TDI Overhead Beløp' = SUM ( FactProjectBOA[Overhead] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 07 BOA Prosjekter

\tmeasure 'TDI Leiested Beløp' = SUM ( FactProjectBOA[Leiested] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 07 BOA Prosjekter

\tmeasure 'TDI Forbruksavvik %' = AVERAGE ( FactProjectBOA[Forbruksavvik] )
\t\tformatString: 0.0%
\t\tdisplayFolder: 07 BOA Prosjekter

\tcolumn Placeholder
\t\tdataType: string
\t\tisHidden
\t\tlineageTag: m0000000-0000-0000-0000-000000000099
\t\tsummarizeBy: none
\t\tsourceColumn: Placeholder

\tpartition _Measures = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = #table(type table [Placeholder = text], {{"Placeholder"}})
\t\t\t\tin
\t\t\t\t    Source
"""
    with open(os.path.join(tables_dir, "_Measures.tmdl"), "w", encoding="utf-8") as f:
        f.write(measures_content)

    print("All TMDL tables and relationships successfully built.")

if __name__ == "__main__":
    build_model()
