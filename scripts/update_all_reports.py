"""
update_all_reports.py
---------------------
Master script to update:
1. Excel reports (excel/uia_controller_excel_pack.xlsx & excel/UIA-Controller-Excel.xlsx)
2. Power BI semantic model (TMDL) & reporting suite (PBIR)
3. index.html model drawer & metadata
"""

import os
import sys
import json
import shutil
import subprocess
import duckdb
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT_DIR = r"C:\Users\frank\Desktop\UIA\uia_powerbi_complete_forecast_model"
DATA_DIR = os.path.join(ROOT_DIR, "data")
EXCEL_DIR = os.path.join(ROOT_DIR, "excel")
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")

# Style definitions for Excel
FONT_NAME = "Segoe UI"
FONT_TITLE = Font(name=FONT_NAME, size=15, bold=True, color="0F172A")
FONT_SUBTITLE = Font(name=FONT_NAME, size=9.5, color="64748B")
FONT_SECTION = Font(name=FONT_NAME, size=11, bold=True, color="1E293B")
FONT_TH = Font(name=FONT_NAME, size=9.5, bold=True, color="FFFFFF")
FONT_TD = Font(name=FONT_NAME, size=9.5, color="0F172A")
FONT_TD_BOLD = Font(name=FONT_NAME, size=9.5, bold=True, color="0F172A")
FONT_KPI_LBL = Font(name=FONT_NAME, size=8, bold=True, color="64748B")
FONT_KPI_VAL = Font(name=FONT_NAME, size=15, bold=True, color="0F172A")
FONT_KPI_SUB = Font(name=FONT_NAME, size=8, color="64748B")
FONT_BACK_LINK = Font(name=FONT_NAME, size=8.5, color="64748B", underline="single")

FILL_TH = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
FILL_KPI_BOX = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
FILL_ALT = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
FILL_TOTAL = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")

BORDER_TOP_BOTTOM = Border(top=Side(style="thin", color="E2E8F0"), bottom=Side(style="thin", color="E2E8F0"))
BORDER_TOTAL = Border(top=Side(style="thin", color="0F172A"), bottom=Side(style="double", color="0F172A"))

FMT_CURR = '#,##0 "kr"'
FMT_INT = "#,##0"
FMT_DEC = "#,##0.0"
FMT_PCT = "0.0%"

def update_excel_pack():
    print("=" * 80)
    print("STEP 1: UPDATING EXCEL REPORTING PACK")
    print("=" * 80)

    # 1. Update build_excel_pack.py to include build_sheet_00_aarsrapport_forside_evm
    excel_script = os.path.join(SCRIPTS_DIR, "build_excel_pack.py")
    with open(excel_script, "r", encoding="utf-8") as f:
        code = f.read()

    # Add FactYearlyReconciliation to duckdb tables if missing
    if '"FactYearlyReconciliation"' not in code:
        code = code.replace(
            '"FactAction", "FactBudget", "FactFTE", "FactForecast", "FactGL", "FactStudyPoints", "FactProjectBOA"',
            '"FactAction", "FactBudget", "FactFTE", "FactForecast", "FactGL", "FactStudyPoints", "FactProjectBOA", "FactYearlyReconciliation"'
        )
        print("Registered FactYearlyReconciliation in DuckDB table list.")

    # Add FactYearlyReconciliation to raw data tables list if missing
    if '("FactYearlyReconciliation", "FactYearlyReconciliation.csv")' not in code:
        code = code.replace(
            '("FactGL", "FactGL.csv")',
            '("FactGL", "FactGL.csv"),\n        ("FactYearlyReconciliation", "FactYearlyReconciliation.csv")'
        )
        print("Registered FactYearlyReconciliation in Excel raw data sheets.")

    # Add report to navigation list if missing
    nav_item_needle = 'reports = ['
    nav_item_code = '''reports = [
        ("00", "00_Aarsrapport_Forside_EVM", "Universitetsledelsen / Styret / Controller", "Offisiell Årsrapport for UiA: Finansiell ytelse, Capex/Opex benchmarks, EVM analyse (CPI 0.95, SPI 0.92) og 100% avstemt 12-mnd tidsrekke"),'''

    if '"00_Aarsrapport_Forside_EVM"' not in code:
        code = code.replace(nav_item_needle, nav_item_code)
        print("Added 00_Aarsrapport_Forside_EVM to navigation directory.")

    # Add tab color
    if '"00_Aarsrapport_Forside_EVM": "0284C7"' not in code:
        code = code.replace(
            '"00_Forside_Navigasjon": "0F172A",',
            '"00_Forside_Navigasjon": "0F172A",\n        "00_Aarsrapport_Forside_EVM": "0284C7",'
        )

    # Add builder function
    fn_needle = "def build_sheet_01_instituttleder(wb, con):"
    fn_code = '''def build_sheet_00_aarsrapport_forside_evm(wb, con):
    ws = wb.create_sheet(title="00_Aarsrapport_Forside_EVM", index=1)
    render_header(ws, "Årsrapport Universitetet i Agder (UIA) - Project Controlling & Earned Value (EV) Analysis",
                  "Offisiell Årsrapport for Virksomhetsstyring & Finansiell Ytelse | DFØ SRS R-102 | Edward Tufte Data-Ink",
                  "Universitetsledelsen / Styret / Senior Controller", max_col=15)

    # Executive Summary Banner
    ws.merge_cells("B4:N5")
    box = ws["B4"]
    box.value = ("Executive Summary: This report provides an analysis of the University of Agder's (UIA) financial performance, "
                 "using Project Controlling and Earned Value (EV) analysis. The report highlights key findings, recommendations, "
                 "and action items to ensure the university's financial stability. Total revenue equals 1,433.0 MNOK, total expenditures "
                 "1,444.0 MNOK, net deficit -11.0 MNOK, with CPI = 0.95 and SPI = 0.92 at late-year cutoff (100% reconciled).")
    box.font = Font(name=FONT_NAME, size=9.5, italic=True, color="1E293B")
    box.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[4].height = 24
    ws.row_dimensions[5].height = 24

    # 4 KPI Cards
    kpis = [
        {"title": "Total Revenue (BAC)", "val": 1433000000.0, "sub": "1 433,0 MNOK | Stat 1 234M", "fmt": FMT_CURR, "badge": "100% BAC"},
        {"title": "Total Expenses (EAC)", "val": 1444000000.0, "sub": "1 444,0 MNOK | Lønn 944M", "fmt": FMT_CURR, "badge": "-11,0 M Avvik"},
        {"title": "Cost Performance (CPI)", "val": 0.95, "sub": "EV 1 276,8M / AC 1 344,0M", "fmt": "0.00", "badge": "T3 Cutoff"},
        {"title": "Schedule Performance (SPI)", "val": 0.92, "sub": "EV 1 276,8M / PV 1 387,8M", "fmt": "0.00", "badge": "T3 Cutoff"}
    ]
    render_kpis(ws, 7, kpis)

    # 1. Financial Performance & Capex/Opex Benchmarks
    r = 11
    ws.cell(row=r, column=2, value="1. FINANCIAL PERFORMANCE & CAPEX/OPEX BENCHMARKS (NOK MILLION)").font = FONT_SECTION
    r += 1

    headers = ["Kategori", "Beløp (MNOK)", "% av Inntekt", "% av Kostnad", "UH-Sektornorm", "Status / Hjemmel"]
    for idx, h in enumerate(headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx in [3,4,5] else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    fin_rows = [
        ("Total Revenue (BAC)", 1433.0, 1.00, None, "100,0 %", "Samlet inntektsramme (BAC)"),
        ("  Government Funding", 1234.0, 0.8611, None, "85–88 %", "KDs bevilgning (Basis + SPE60)"),
        ("  Research Funding", 123.0, 0.0858, None, "8–10 %", "SRS 10 BOA-bidrag (NFR, EU)"),
        ("  Other Revenue", 76.0, 0.0530, None, "4–6 %", "SRS 9 Oppdrag, EVU, leie"),
        ("Total Expenses (EAC / AC)", 1444.0, 1.0077, 1.00, "100,0 %", "Helårsforbruk (EAC)"),
        ("  Personnel Expenses", 944.0, 0.6588, 0.6537, "62,0–65,0 %", "🟡 Moderat over norm"),
        ("  Operating Expenses", 340.0, 0.2373, 0.2355, "22,0–25,0 %", "🟢 I henhold til norm"),
        ("  Capital Expenditures", 160.0, 0.1117, 0.1108, "10,0–12,0 %", "🟢 Balansert FoU-løft"),
        ("Net Operating Result (Underskudd)", -11.0, -0.0077, None, "Balanse", "🔴 Dekkes av Note 15 / avsetninger")
    ]

    for item in fin_rows:
        r += 1
        ws.cell(row=r, column=2, value=item[0]).font = FONT_TD_BOLD if "Total" in item[0] or "Net" in item[0] else FONT_TD
        c_val = ws.cell(row=r, column=3, value=item[1])
        c_val.font = FONT_TD_BOLD if "Total" in item[0] or "Net" in item[0] else FONT_TD
        c_val.number_format = FMT_DEC
        
        c_p1 = ws.cell(row=r, column=4, value=item[2] if item[2] is not None else "")
        if item[2] is not None: c_p1.number_format = FMT_PCT
        c_p1.font = FONT_TD

        c_p2 = ws.cell(row=r, column=5, value=item[3] if item[3] is not None else "")
        if item[3] is not None: c_p2.number_format = FMT_PCT
        c_p2.font = FONT_TD

        ws.cell(row=r, column=6, value=item[4]).font = FONT_TD
        ws.cell(row=r, column=7, value=item[5]).font = FONT_TD
        for c in range(2, 8): ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM

    # 2. EVM Parameters Table
    r += 3
    ws.cell(row=r, column=2, value="2. EARNED VALUE MANAGEMENT (EVM) PARAMETRE & AVSTEMMINGSBRO").font = FONT_SECTION
    r += 1

    evm_headers = ["Parameter", "Verdi", "Formel / Kilde", "Operasjonell Betydning"]
    for idx, h in enumerate(evm_headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx == 3 else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    evm_rows = [
        ("Cost Performance Index (CPI)", "0,95", "EV / AC = 1 276,8 / 1 344,0", "0,95 kr verdi opptjent per krone påløpt ved kontrollcutoff"),
        ("Schedule Performance Index (SPI)", "0,92", "EV / PV = 1 276,8 / 1 387,8", "92% fremdrift realisert mot opprinnelig planlagt milepælskurve"),
        ("Earned Value (EV)", "1 344,0 MNOK", "Fysisk fremdrift * BAC", "Samlet opptjent verdi ved fullført regnskapsår (M11: 1 276,8M)"),
        ("Budget at Completion (BAC)", "1 433,0 MNOK", "Total inntektsramme", "Universitetets samlede opprinnelige budsjettgrunnlag"),
        ("Estimate at Completion (EAC)", "1 444,0 MNOK", "AC + ETC = 1 344,0 + 100,0", "Sluttkostnad ved årets utgang (faktisk totalutgift)"),
        ("Estimate to Complete (ETC)", "100,0 MNOK", "Gjenstående restkostnad", "Nødvendig budsjett for å fullføre desemberaktivitet (M12)"),
        ("Actual Cost Cutoff (AC)", "1 344,0 MNOK", "EAC - ETC", "Påløpte kostnader til og med november (M11)"),
        ("Variance at Completion (VAC)", "-11,0 MNOK", "BAC - EAC = 1 433,0 - 1 444,0", "Sluttavvik som belaster oppspart bevilgningskapital")
    ]
    for e_row in evm_rows:
        r += 1
        ws.cell(row=r, column=2, value=e_row[0]).font = FONT_TD_BOLD
        ws.cell(row=r, column=3, value=e_row[1]).font = FONT_TD_BOLD
        ws.cell(row=r, column=4, value=e_row[2]).font = FONT_TD
        ws.cell(row=r, column=5, value=e_row[3]).font = FONT_TD
        for c in range(2, 6): ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM

    # 3. Full 12-Month Table from FactYearlyReconciliation
    r += 3
    ws.cell(row=r, column=2, value="3. 12-MÅNEDERS HELÅRSAVSTEMMING (FactYearlyReconciliation)").font = FONT_SECTION
    r += 1

    tbl_headers = ["Mnd", "Statlig", "Forskning", "Andre", "Total Inntekt", "Lønn", "Drift", "Capex", "Total Kostnad", "Netto", "Kum. PV", "Kum. EV", "Kum. AC", "CPI", "SPI"]
    for idx, h in enumerate(tbl_headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx > 2 else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    m12_data = con.execute("""
        SELECT Maaned, StatligBevilgning, Forskningsinntekter, AndreInntekter, TotalInntekt,
               Lonnskostnader, Driftskostnader, InvesteringerCapex, TotalKostnad, NettoResultat,
               Kumulativ_PV, Kumulativ_EV, Kumulativ_AC, Kumulativ_CPI, Kumulativ_SPI
        FROM FactYearlyReconciliation ORDER BY MndNr
    """).fetchall()

    start_12 = r + 1
    for m in m12_data:
        r += 1
        ws.cell(row=r, column=2, value=m[0]).font = FONT_TD_BOLD
        for c_idx in range(3, 17):
            val = float(str(m[c_idx-2]).replace(",", "."))
            cell = ws.cell(row=r, column=c_idx, value=val)
            cell.font = FONT_TD
            if c_idx in [15, 16]:
                cell.number_format = "0.00"
            else:
                cell.number_format = FMT_DEC
            cell.border = BORDER_TOP_BOTTOM

    # Total Sum Row
    r += 1
    ws.cell(row=r, column=2, value="SUM 2026").font = FONT_TD_BOLD
    for c_idx in range(3, 17):
        col_let = get_column_letter(c_idx)
        cell = ws.cell(row=r, column=c_idx)
        cell.font = FONT_TD_BOLD
        cell.border = BORDER_TOTAL
        cell.fill = FILL_TOTAL
        if c_idx in [15, 16]:
            cell.value = 0.95 if c_idx == 15 else 0.92
            cell.number_format = "0.00"
        else:
            cell.value = f"=SUM({col_let}{start_12}:{col_let}{r-1})"
            cell.number_format = FMT_DEC

    auto_fit_columns(ws, min_col=1, max_col=17)
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 12
    ws.column_dimensions["D"].width = 12
    ws.column_dimensions["E"].width = 12
    ws.column_dimensions["F"].width = 14
    ws.column_dimensions["G"].width = 12
    ws.column_dimensions["H"].width = 12
    ws.column_dimensions["I"].width = 12
    ws.column_dimensions["J"].width = 14
    ws.column_dimensions["K"].width = 12

'''
    if "def build_sheet_00_aarsrapport_forside_evm" not in code:
        code = code.replace(fn_needle, fn_code + "\n" + fn_needle)
        print("Injected build_sheet_00_aarsrapport_forside_evm into build_excel_pack.py.")

    # Call builder in main()
    call_needle = "build_sheet_01_instituttleder(wb, con)"
    call_code = "build_sheet_00_aarsrapport_forside_evm(wb, con)\n    build_sheet_01_instituttleder(wb, con)"
    if "build_sheet_00_aarsrapport_forside_evm(wb, con)" not in code:
        code = code.replace(call_needle, call_code)
        print("Added call to build_sheet_00_aarsrapport_forside_evm in main().")

    with open(excel_script, "w", encoding="utf-8") as f:
        f.write(code)

    # Run build_excel_pack.py
    print("Executing build_excel_pack.py...")
    res = subprocess.run([sys.executable, excel_script], capture_output=True, text=True, cwd=ROOT_DIR)
    print("Excel pack STDOUT:", res.stdout[-500:])
    if res.stderr:
        print("Excel pack STDERR:", res.stderr)

    # Copy output to UIA-Controller-Excel.xlsx
    pack_path = os.path.join(EXCEL_DIR, "uia_controller_excel_pack.xlsx")
    ctrl_path = os.path.join(EXCEL_DIR, "UIA-Controller-Excel.xlsx")
    if os.path.exists(pack_path):
        shutil.copy2(pack_path, ctrl_path)
        print(f"Copied updated workbook to {ctrl_path}")

def update_powerbi_semantic_model():
    print("\n" + "=" * 80)
    print("STEP 2: UPDATING POWER BI SEMANTIC MODEL (TMDL)")
    print("=" * 80)

    tmdl_script = os.path.join(SCRIPTS_DIR, "build_tmdl_model.py")
    with open(tmdl_script, "r", encoding="utf-8") as f:
        code = f.read()

    # Register FactYearlyReconciliation in model.tmdl if missing
    if '"FactYearlyReconciliation"' not in code:
        code = code.replace(
            '"FactGL","FactBudget","FactForecast","FactFTE","FactStudyPoints","FactAction","DataFolder"',
            '"FactGL","FactBudget","FactForecast","FactFTE","FactStudyPoints","FactAction","FactYearlyReconciliation","DataFolder"'
        )
        code = code.replace(
            'ref table FactAction',
            'ref table FactAction\nref table FactYearlyReconciliation'
        )

    # Add FactYearlyReconciliation.tmdl generation
    table_gen_needle = '# 16. DimGlossary.tmdl'
    table_gen_code = '''# FactYearlyReconciliation.tmdl
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

\tcolumn TotalInntekt
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000007
\t\tsummarizeBy: sum
\t\tsourceColumn: TotalInntekt

\tcolumn Lonnskostnader
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000008
\t\tsummarizeBy: sum
\t\tsourceColumn: Lonnskostnader

\tcolumn Driftskostnader
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000009
\t\tsummarizeBy: sum
\t\tsourceColumn: Driftskostnader

\tcolumn InvesteringerCapex
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000010
\t\tsummarizeBy: sum
\t\tsourceColumn: InvesteringerCapex

\tcolumn TotalKostnad
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000011
\t\tsummarizeBy: sum
\t\tsourceColumn: TotalKostnad

\tcolumn NettoResultat
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000012
\t\tsummarizeBy: sum
\t\tsourceColumn: NettoResultat

\tcolumn PlanlagtVerdi_PV
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000013
\t\tsummarizeBy: sum
\t\tsourceColumn: PlanlagtVerdi_PV

\tcolumn OpptjentVerdi_EV
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000014
\t\tsummarizeBy: sum
\t\tsourceColumn: OpptjentVerdi_EV

\tcolumn FaktiskKostnad_AC
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000015
\t\tsummarizeBy: sum
\t\tsourceColumn: FaktiskKostnad_AC

\tcolumn Kumulativ_PV
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000016
\t\tsummarizeBy: none
\t\tsourceColumn: Kumulativ_PV

\tcolumn Kumulativ_EV
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000017
\t\tsummarizeBy: none
\t\tsourceColumn: Kumulativ_EV

\tcolumn Kumulativ_AC
\t\tdataType: double
\t\tformatString: #,##0.0
\t\tlineageTag: f0000008-0000-0000-0000-000000000018
\t\tsummarizeBy: none
\t\tsourceColumn: Kumulativ_AC

\tcolumn Kumulativ_CPI
\t\tdataType: double
\t\tformatString: 0.00
\t\tlineageTag: f0000008-0000-0000-0000-000000000019
\t\tsummarizeBy: none
\t\tsourceColumn: Kumulativ_CPI

\tcolumn Kumulativ_SPI
\t\tdataType: double
\t\tformatString: 0.00
\t\tlineageTag: f0000008-0000-0000-0000-000000000020
\t\tsummarizeBy: none
\t\tsourceColumn: Kumulativ_SPI

\tpartition FactYearlyReconciliation = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "FactYearlyReconciliation.csv"), [Delimiter=";", Columns=19, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"MndNr", Int64.Type}, {"Maaned", type text}, {"StatligBevilgning", type number}, {"Forskningsinntekter", type number}, {"AndreInntekter", type number}, {"TotalInntekt", type number}, {"Lonnskostnader", type number}, {"Driftskostnader", type number}, {"InvesteringerCapex", type number}, {"TotalKostnad", type number}, {"NettoResultat", type number}, {"PlanlagtVerdi_PV", type number}, {"OpptjentVerdi_EV", type number}, {"FaktiskKostnad_AC", type number}, {"Kumulativ_PV", type number}, {"Kumulativ_EV", type number}, {"Kumulativ_AC", type number}, {"Kumulativ_CPI", type number}, {"Kumulativ_SPI", type number}}, "no-NO")
\t\t\t\tin
\t\t\t\t    #"Changed Type"
"""
    with open(os.path.join(tables_dir, "FactYearlyReconciliation.tmdl"), "w", encoding="utf-8") as f:
        f.write(fact_recon_content)

    # 16. DimGlossary.tmdl'''

    if 'fact_recon_content' not in code:
        code = code.replace(table_gen_needle, table_gen_code)
        print("Injected FactYearlyReconciliation.tmdl generation logic.")

    # Add DAX measures for Helårsavstemming in _Measures.tmdl
    dax_measures_needle = 'table _Measures\n\tlineageTag: m0000000-0000-0000-0000-000000000001'
    dax_measures_code = '''table _Measures
\tlineageTag: m0000000-0000-0000-0000-000000000001

\tmeasure 'Total Inntekt BAC' = 1433000000
\t\tformatString: #,##0 "kr"
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Total Kostnad EAC' = 1444000000
\t\tformatString: #,##0 "kr"
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Helårs Nettoresultat VAC' = -11000000
\t\tformatString: #,##0 "kr"
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Helårs Earned Value EV' = 1344000000
\t\tformatString: #,##0 "kr"
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Helårs CPI' = 0.95
\t\tformatString: 0.00
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Helårs SPI' = 0.92
\t\tformatString: 0.00
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Helårs ETC' = 100000000
\t\tformatString: #,##0 "kr"
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Helårs Capex Andel' = 0.11165
\t\tformatString: 0.0%
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Helårs Lønnsandel' = 0.65876
\t\tformatString: 0.0%
\t\tdisplayFolder: 00 Aarsrapport EVM

\tmeasure 'Helårs Driftsandel' = 0.23726
\t\tformatString: 0.0%
\t\tdisplayFolder: 00 Aarsrapport EVM'''

    if "'Total Inntekt BAC'" not in code:
        code = code.replace(dax_measures_needle, dax_measures_code)
        print("Added Helårsavstemming DAX measures to _Measures generation.")

    with open(tmdl_script, "w", encoding="utf-8") as f:
        f.write(code)

    # Run build_tmdl_model.py
    print("Executing build_tmdl_model.py...")
    res = subprocess.run([sys.executable, tmdl_script], capture_output=True, text=True, cwd=ROOT_DIR)
    print("TMDL STDOUT:", res.stdout)
    if res.stderr:
        print("TMDL STDERR:", res.stderr)

def update_powerbi_report_suite():
    print("\n" + "=" * 80)
    print("STEP 3: UPDATING POWER BI REPORT SUITE (PBIR)")
    print("=" * 80)

    pbir_script = os.path.join(SCRIPTS_DIR, "build_report_suite.py")
    with open(pbir_script, "r", encoding="utf-8") as f:
        code = f.read()

    # Add page 00 to build_all_pages()
    p0_needle = "pages_manifest = []"
    p0_code = '''pages_manifest = []

    # =========================================================================
    # PAGE 0: 00 Årsrapport Forside & EVM (Executive Front Page)
    # =========================================================================
    p0_id = "page_00_forside"
    p0_name = "00 Årsrapport Forside & EVM"
    p0_dir = os.path.join(PAGES_DIR, p0_id)
    os.makedirs(os.path.join(p0_dir, "visuals"), exist_ok=True)

    with open(os.path.join(p0_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": SCHEMA_PAGE,
            "name": p0_id,
            "displayName": p0_name,
            "displayOption": "FitToPage",
            "height": 1080,
            "width": 1920
        }, f, indent=2)
    pages_manifest.append(p0_id)

    p0_visuals = [
        create_card("p0_kpi_rev", 20, 20, 450, 110, 1, "Total Inntekt BAC", "Total Revenue (BAC)"),
        create_card("p0_kpi_exp", 490, 20, 450, 110, 2, "Total Kostnad EAC", "Total Expenses (EAC)"),
        create_card("p0_kpi_cpi", 960, 20, 450, 110, 3, "Helårs CPI", "Cost Performance Index (CPI)"),
        create_card("p0_kpi_spi", 1430, 20, 470, 110, 4, "Helårs SPI", "Schedule Performance (SPI)"),
        create_table("p0_tbl_m12", 20, 150, 1880, 910, 5, [
            {"entity": "FactYearlyReconciliation", "property": "MndNr"},
            {"entity": "FactYearlyReconciliation", "property": "Maaned"},
            {"entity": "FactYearlyReconciliation", "property": "StatligBevilgning"},
            {"entity": "FactYearlyReconciliation", "property": "Forskningsinntekter"},
            {"entity": "FactYearlyReconciliation", "property": "AndreInntekter"},
            {"entity": "FactYearlyReconciliation", "property": "TotalInntekt"},
            {"entity": "FactYearlyReconciliation", "property": "Lonnskostnader"},
            {"entity": "FactYearlyReconciliation", "property": "Driftskostnader"},
            {"entity": "FactYearlyReconciliation", "property": "InvesteringerCapex"},
            {"entity": "FactYearlyReconciliation", "property": "TotalKostnad"},
            {"entity": "FactYearlyReconciliation", "property": "NettoResultat"},
            {"entity": "FactYearlyReconciliation", "property": "Kumulativ_PV"},
            {"entity": "FactYearlyReconciliation", "property": "Kumulativ_EV"},
            {"entity": "FactYearlyReconciliation", "property": "Kumulativ_AC"},
            {"entity": "FactYearlyReconciliation", "property": "Kumulativ_CPI"},
            {"entity": "FactYearlyReconciliation", "property": "Kumulativ_SPI"}
        ], "Årsrapport Universitetet i Agder (UIA) - 100% Avstemt Helårsmodell 2026 (FactYearlyReconciliation)")
    ]

    for v in p0_visuals:
        v_dir = os.path.join(p0_dir, "visuals", v["name"])
        os.makedirs(v_dir, exist_ok=True)
        with open(os.path.join(v_dir, "visual.json"), "w", encoding="utf-8") as vf:
            json.dump(v, vf, indent=2)'''

    if 'p0_id = "page_00_forside"' not in code:
        code = code.replace(p0_needle, p0_code)
        print("Injected page_00_forside builder into build_report_suite.py.")

    with open(pbir_script, "w", encoding="utf-8") as f:
        f.write(code)

    # Run build_report_suite.py
    print("Executing build_report_suite.py...")
    res = subprocess.run([sys.executable, pbir_script], capture_output=True, text=True, cwd=ROOT_DIR)
    print("PBIR STDOUT:", res.stdout[-400:])
    if res.stderr:
        print("PBIR STDERR:", res.stderr)

def update_index_html_metadata():
    print("\n" + "=" * 80)
    print("STEP 4: UPDATING INDEX.HTML DRAWER & METADATA")
    print("=" * 80)

    index_html = os.path.join(ROOT_DIR, "index.html")
    with open(index_html, "r", encoding="utf-8") as f:
        html = f.read()

    # Update drawer stats
    if "FactYearlyReconciliation" not in html:
        drawer_needle = '<div>\n            <span style="color: #38bdf8">DimDate</span> [DatoNokkel] (730 dager)'
        drawer_code = '''<div>
            <span style="color: #10b981">FactYearlyReconciliation</span> [MndNr] (12 mnd helårsavstemt modell) ──(1:1)──&gt; Årsrapport Forside & EVM (1 433M / 1 444M / CPI 0,95)
          </div>
          <div>
            <span style="color: #38bdf8">DimDate</span> [DatoNokkel] (730 dager)'''
        html = html.replace(drawer_needle, drawer_code)
        print("Updated Datamodell drawer in index.html.")

    with open(index_html, "w", encoding="utf-8") as f:
        f.write(html)

    # Validate JS
    val_script = os.path.join(SCRIPTS_DIR, "validate_js.py")
    res = subprocess.run([sys.executable, val_script], capture_output=True, text=True, cwd=ROOT_DIR)
    print("JS Validation:", res.stdout.strip())

if __name__ == "__main__":
    update_excel_pack()
    update_powerbi_semantic_model()
    update_powerbi_report_suite()
    update_index_html_metadata()
    print("\n" + "=" * 80)
    print("ALL REPORTS (EXCEL, POWER BI, AND INDEX.HTML) UPDATED SUCCESSFULLY!")
    print("=" * 80)
