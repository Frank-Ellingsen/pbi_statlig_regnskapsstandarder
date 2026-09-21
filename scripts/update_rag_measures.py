import os

measures_code = """\tmeasure 'BAC (Budget at Completion)' = [Aarsbudsjett]
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

\tmeasure 'Avvik YTD %' = DIVIDE ( [Avvik YTD], ABS ( [Budsjett YTD] ) )
\t\tformatString: 0.0%
\t\tdisplayFolder: 01 Okonomi

\tmeasure 'Forecast lonnsavvik' = [Forecast lonn] - CALCULATE ( [Aarsbudsjett], DimAccount[SRS_regnskapslinje] = "Lonnskostnader" )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 02 Forecast

\tmeasure 'Absolutt forecastavvik' = ABS ( [Forecastavvik] )
\t\tformatString: #,##0.00
\t\tdisplayFolder: 02 Forecast

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

with open("scripts/build_tmdl_model.py", "r", encoding="utf-8") as f:
    code = f.read()

bac_marker = "\tmeasure 'BAC (Budget at Completion)' = [Aarsbudsjett]"
bac_idx = code.find(bac_marker)

if bac_idx != -1:
    end_marker = '"""\n    with open(os.path.join(tables_dir, "_Measures.tmdl")'
    closing_idx = code.find(end_marker, bac_idx)
    new_code = code[:bac_idx] + measures_code + code[closing_idx:]
    with open("scripts/build_tmdl_model.py", "w", encoding="utf-8") as f:
        f.write(new_code)
    print("Updated scripts/build_tmdl_model.py successfully!")
else:
    print("Could not find BAC marker!")
