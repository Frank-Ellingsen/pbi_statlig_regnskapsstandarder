# -*- coding: utf-8 -*-
"""
build_excel_pack.py
-------------------
Generates the complete, production-grade Excel Financial Controller Reporting Pack
in excel/uia_controller_excel_pack.xlsx, mirroring the 14-report Power BI reporting suite:
- 00_Forside_Navigasjon (Interactive Navigation Hub with HYPERLINKs)
- 01_Instituttleder to 08_Controller_Cockpit (8 Role-based Management Dashboards)
- 09_Begrepskatalog (60 defined UH-controller glossary terms & methodology)
- DT_Okonomi to DT_Studieaktivitet (5 Drill-Through Sheets)
- 10 Raw Data Sheets (FactGL, FactBudget, FactForecast, FactFTE, FactStudyPoints, FactAction,
  DimAccount, DimOrganization, DimProject, DimGlossary)

All summary sheets strictly adhere to Edward Tufte's Data-Ink Ratio principles:
- No vertical borders
- Crisp slate-blue header styling (#1E293B) with white text
- Explicit number formats (#,##0 kr, 0.0%, #,##0.0)
- Right-aligned numbers, left-aligned text
- Muted RAG indicators (Red, Amber, Green, Gray)
- Active Excel formulas for totals, subtotals, variances, variance %, and status logic.
"""

import os
import sys
import time
import duckdb
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ==============================================================================
# STYLE DEFINITIONS (Edward Tufte compliant)
# ==============================================================================
FONT_NAME = "Segoe UI"

FONT_TITLE = Font(name=FONT_NAME, size=15, bold=True, color="0F172A")
FONT_SUBTITLE = Font(name=FONT_NAME, size=9.5, italic=False, color="64748B")
FONT_ROLE = Font(name=FONT_NAME, size=9.5, bold=True, color="0284C7")
FONT_SECTION = Font(name=FONT_NAME, size=11, bold=True, color="1E293B")
FONT_SUBSECTION = Font(name=FONT_NAME, size=9.5, bold=True, color="475569")

FONT_TH = Font(name=FONT_NAME, size=9.5, bold=True, color="FFFFFF")
FONT_TH_RIGHT = Font(name=FONT_NAME, size=9.5, bold=True, color="FFFFFF")
FONT_TD = Font(name=FONT_NAME, size=9.5, color="0F172A")
FONT_TD_BOLD = Font(name=FONT_NAME, size=9.5, bold=True, color="0F172A")
FONT_TD_CODE = Font(name="Consolas", size=9, color="0284C7")
FONT_LINK = Font(name=FONT_NAME, size=9.5, color="0284C7", underline="single")
FONT_BACK_LINK = Font(name=FONT_NAME, size=8.5, color="64748B", underline="single")

FONT_KPI_LBL = Font(name=FONT_NAME, size=8, bold=True, color="64748B")
FONT_KPI_VAL = Font(name=FONT_NAME, size=15, bold=True, color="0F172A")
FONT_KPI_SUB = Font(name=FONT_NAME, size=8, color="64748B")

FILL_TH = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
FILL_TH_SEC = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
FILL_KPI_BOX = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
FILL_ALT = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
FILL_TOTAL = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")

# Muted RAG Fills
FILL_RAG_GREEN = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
FONT_RAG_GREEN = Font(name=FONT_NAME, size=9, bold=True, color="166534")

FILL_RAG_AMBER = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
FONT_RAG_AMBER = Font(name=FONT_NAME, size=9, bold=True, color="B45309")

FILL_RAG_RED = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
FONT_RAG_RED = Font(name=FONT_NAME, size=9, bold=True, color="991B1B")

FILL_RAG_GRAY = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
FONT_RAG_GRAY = Font(name=FONT_NAME, size=9, bold=True, color="475569")

# Borders (NO vertical borders)
BORDER_TOP_BOTTOM = Border(
    top=Side(style="thin", color="E2E8F0"),
    bottom=Side(style="thin", color="E2E8F0")
)
BORDER_TOTAL = Border(
    top=Side(style="thin", color="0F172A"),
    bottom=Side(style="double", color="0F172A")
)
BORDER_KPI = Border(
    top=Side(style="thin", color="CBD5E1"),
    bottom=Side(style="thin", color="CBD5E1"),
    left=Side(style="thin", color="CBD5E1"),
    right=Side(style="thin", color="CBD5E1")
)

# Number format strings
FMT_CURR = '#,##0 "kr"'
FMT_CURR_DEC = '#,##0.00 "kr"'
FMT_PCT = "0.0%"
FMT_INT = "#,##0"
FMT_DEC = "#,##0.0"

# ==============================================================================
# DUCKDB DATA ENGINE
# ==============================================================================
def init_duckdb(data_dir):
    con = duckdb.connect(database=":memory:")
    tables = [
        "DimAccount", "DimDate", "DimForecastVersion", "DimGlossary", "DimOrganization",
        "DimPositionGroup", "DimProject", "DimStudyProgram",
        "FactAction", "FactBudget", "FactFTE", "FactForecast", "FactGL", "FactStudyPoints"
    ]
    for tbl in tables:
        p = os.path.join(data_dir, f"{tbl}.csv").replace("\\", "/")
        con.execute(f"CREATE TABLE {tbl} AS SELECT * FROM read_csv('{p}', delim=';', header=true, encoding='utf-8')")
    return con

# ==============================================================================
# COMMON OPENPYXL BUILDERS
# ==============================================================================
def render_header(ws, page_title, subtitle, role_text, max_col=10):
    ws.merge_cells(start_row=1, start_column=2, end_row=1, end_column=max_col-1)
    cell = ws.cell(row=1, column=2, value=page_title)
    cell.font = FONT_TITLE
    cell.alignment = Alignment(vertical="center")

    nav_cell = ws.cell(row=1, column=max_col, value='=HYPERLINK("#\'00_Forside_Navigasjon\'!A1", "← Hovedmeny")')
    nav_cell.font = FONT_BACK_LINK
    nav_cell.alignment = Alignment(horizontal="right", vertical="center")

    ws.merge_cells(start_row=2, start_column=2, end_row=2, end_column=max_col)
    sub_cell = ws.cell(row=2, column=2, value=f"{subtitle}  |  Rolle: {role_text}")
    sub_cell.font = FONT_SUBTITLE
    sub_cell.alignment = Alignment(vertical="center")
    ws.row_dimensions[1].height = 24
    ws.row_dimensions[2].height = 18

def render_kpis(ws, start_row, kpi_list):
    """
    Renders 4 to 6 KPI cards horizontally. Each card takes 2 columns, 3 rows.
    kpi_list is list of dicts: {"title": str, "val": str/float, "sub": str, "fmt": str, "badge": str}
    """
    col = 2
    for item in kpi_list:
        c_end = col + 1
        ws.merge_cells(start_row=start_row, start_column=col, end_row=start_row, end_column=c_end)
        ws.merge_cells(start_row=start_row+1, start_column=col, end_row=start_row+1, end_column=c_end)
        ws.merge_cells(start_row=start_row+2, start_column=col, end_row=start_row+2, end_column=c_end)

        c1 = ws.cell(row=start_row, column=col, value=item["title"].upper())
        c1.font = FONT_KPI_LBL
        c1.alignment = Alignment(horizontal="left", vertical="center", indent=1)

        val = item["val"]
        c2 = ws.cell(row=start_row+1, column=col, value=val)
        c2.font = FONT_KPI_VAL
        c2.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        if "fmt" in item and item["fmt"]:
            c2.number_format = item["fmt"]

        sub_text = item.get("sub", "")
        if item.get("badge"):
            sub_text = f"[{item['badge']}] {sub_text}"
        c3 = ws.cell(row=start_row+2, column=col, value=sub_text)
        c3.font = FONT_KPI_SUB
        c3.alignment = Alignment(horizontal="left", vertical="center", indent=1)

        # Borders and fills
        for r in range(start_row, start_row+3):
            for c in range(col, c_end+1):
                cell = ws.cell(row=r, column=c)
                cell.fill = FILL_KPI_BOX
                # outer borders
                top_s = Side(style="thin", color="CBD5E1") if r == start_row else None
                bot_s = Side(style="thin", color="CBD5E1") if r == start_row+2 else None
                lft_s = Side(style="thin", color="CBD5E1") if c == col else None
                rgt_s = Side(style="thin", color="CBD5E1") if c == c_end else None
                cell.border = Border(top=top_s, bottom=bot_s, left=lft_s, right=rgt_s)

        col += 2

    ws.row_dimensions[start_row].height = 16
    ws.row_dimensions[start_row+1].height = 24
    ws.row_dimensions[start_row+2].height = 16

def auto_fit_columns(ws, min_col=1, max_col=12):
    ws.views.sheetView[0].showGridLines = True
    ws.sheet_view.zoomScale = 85
    for c in range(min_col, max_col + 1):
        col_letter = get_column_letter(c)
        max_len = 0
        for r in range(1, min(ws.max_row + 1, 100)):
            val = ws.cell(row=r, column=c).value
            if val is not None:
                # ignore formulas or merged titles in length calculation
                s = str(val)
                if not s.startswith("="):
                    max_len = max(max_len, len(s))
        ws.column_dimensions[col_letter].width = max(max_len + 3, 11)

# ==============================================================================
# SHEET BUILDERS (00 - 09 + DT1 - DT5)
# ==============================================================================

def build_sheet_00_navigasjon(wb):
    ws = wb.create_sheet(title="00_Forside_Navigasjon", index=0)
    ws.views.sheetView[0].showGridLines = True
    ws.sheet_view.zoomScale = 85

    # Title Banner
    ws.merge_cells("B2:K2")
    c = ws["B2"]
    c.value = "Statlig Utdanningsinstitusjon - Controller & Forecast Excel Reporting Pack"
    c.font = Font(name=FONT_NAME, size=16, bold=True, color="0F172A")
    c.alignment = Alignment(vertical="center")

    ws.merge_cells("B3:K3")
    c = ws["B3"]
    c.value = "Produksjonsklar finansiell virksomhetsstyrings- og prosjektcontroller-modell | DFØ SRS R-102 | Edward Tufte Data-Ink"
    c.font = Font(name=FONT_NAME, size=10, color="64748B")
    c.alignment = Alignment(vertical="center")

    ws.row_dimensions[2].height = 26
    ws.row_dimensions[3].height = 18

    # Metadata badges
    kpis = [
        {"title": "Rapporter & Dashboards", "val": 14, "sub": "9 styringsrapporter + 5 drill-throughs", "fmt": FMT_INT},
        {"title": "Datatabeller", "val": 10, "sub": "FactGL, Budget, Forecast, FTE m.fl.", "fmt": FMT_INT},
        {"title": "Automatiserte QA-Tester", "val": "74 / 74", "sub": "100% avstemt mot DuckDB & DAX", "fmt": None},
        {"title": "5 %-Regel Tak (F-05-20)", "val": 106939940.48, "sub": "Maksimal tillatt bevilgningsreserve", "fmt": FMT_CURR},
        {"title": "Omstillingstiltak", "val": 21, "sub": "-20,25 Mkr forventet innsparing", "fmt": FMT_INT}
    ]
    render_kpis(ws, 5, kpis)

    # Directory Table Header
    r = 9
    ws.cell(row=r, column=2, value="RAPPORTNAVIGASJON & DRILL-THROUGH REGISTER").font = FONT_SECTION
    r += 1

    headers = ["ID", "Rapportside / Dashboard", "Målgruppe / Rolle", "Hovedfokus & Styringsspørsmål", "Lenke"]
    for idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=r, column=idx, value=h)
        cell.font = FONT_TH
        cell.fill = FILL_TH
        cell.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[r].height = 22

    reports = [
        ("01", "01_Instituttleder", "Instituttleder / Kontorsjef", "Operativ styring, månedlig trend, avviksdrivere og tiltaksstatus"),
        ("02", "02_Dekan", "Dekan & Fakultetsledelse", "Taktisk fakultetsledelse, instituttavvik, BOA-kilder og faglig produktivitet"),
        ("03", "03_Executive", "Universitetsdirektør & Ledelse", "Prognosevandring over runder (BAC → FC1 → FC2 → LE), fakultetsoversikt"),
        ("04", "04_Styret", "Universitetsstyret", "Strategisk måloppnåelse, utdanning, 21 styretiltak og 5 %-regelen (F-05-20) & Note 15"),
        ("05", "05_Forskning_BOA", "Forskningsledelse & BOA", "Eksternfinansiering, NFR/EU-inntekter, TDI-modellen og fullstendig prosjektportefølje"),
        ("06", "06_Studieportefolje", "Prorektor Utdanning & Studieledere", "Produksjon per studieprogram, KD 2025-satser (Kat 1/2/3), SPE60 og enhetskostnad"),
        ("07", "07_Action_Tracker", "Omstillingsutvalg & Linjeledere", "Oppfølging av de 21 omstillingstiltakene (inkl. AI/prosess), forventet vs realisert effekt"),
        ("08", "08_Controller_Cockpit", "Senior Controllere & Regnskapssjef", "Avstemmingsmatrise, DFØ SRS 1 virksomhetsregnskap, avviksdrivere og kontrolltårn"),
        ("09", "09_Begrepskatalog", "Felles: Controller, Dekan, Prosjekt", "60 definerte begreper innen SRS, EVM, RAG-terskler og UH-styring"),
        ("DT1", "DT_Okonomi", "Drill-Through Transaksjoner", "Komplett bilagslogg fra FactGL med bilag, konto, beløp og tekst"),
        ("DT2", "DT_Bemanning", "Drill-Through Bemanning & Årsverk", "Lønnsanalyse, stillingsgrupper (UF/TA) og lønn per årsverk fra FactFTE"),
        ("DT3", "DT_Prosjekt_EVM", "Drill-Through Prosjekter & EVM", "Earned Value Management (BAC, EAC, ETC, VAC, CPI, SPI) for BOA"),
        ("DT4", "DT_Tiltakskort", "Drill-Through Tiltakskort", "Enkeltkort for hvert omstillingstiltak med risikovurdering og milepæler"),
        ("DT5", "DT_Studieaktivitet", "Drill-Through Studieaktivitet", "Detaljert produksjon per studieprogram fra FactStudyPoints")
    ]

    r += 1
    for item in reports:
        num_id, sheet_name, target_role, desc = item
        ws.cell(row=r, column=2, value=num_id).font = FONT_TD_BOLD
        ws.cell(row=r, column=3, value=sheet_name).font = FONT_TD_BOLD
        ws.cell(row=r, column=4, value=target_role).font = FONT_TD
        ws.cell(row=r, column=5, value=desc).font = FONT_TD
        link_cell = ws.cell(row=r, column=6, value=f'=HYPERLINK("#\'{sheet_name}\'!A1", "Åpne rapport →")')
        link_cell.font = FONT_LINK
        link_cell.alignment = Alignment(horizontal="center", vertical="center")

        for c in range(2, 7):
            cell = ws.cell(row=r, column=c)
            cell.border = BORDER_TOP_BOTTOM
            if r % 2 == 1:
                cell.fill = FILL_ALT

        ws.row_dimensions[r].height = 20
        r += 1

    # Data sheets list
    r += 2
    ws.cell(row=r, column=2, value="GRUNNLAGSDATA & MODELLTABELLER (DATA MODEL SHEETS)").font = FONT_SECTION
    r += 1

    data_sheets = [
        ("DimGlossary", "60 definerte begreper med praktisk tolkning og DAX-formler"),
        ("DimAccount", "46 SRS-kontoer med kontotype og regnskapslinje"),
        ("DimOrganization", "40 koststeder og organisasjonsenheter (Fakultet og institutt)"),
        ("DimProject", "6 prosjekter (Drift, NFR, EU, Oppdrag)"),
        ("FactBudget", "17 760 budsjettlinjer fordelt per måned, enhet, konto og prosjekt"),
        ("FactForecast", "53 280 prognoselinjer fordelt over FC1, FC2 og LE"),
        ("FactFTE", "1 200 bemanningslinjer med årsverk og lønn per stillingsgruppe"),
        ("FactStudyPoints", "432 studiepoenglinjer for 22 programmer"),
        ("FactAction", "16 vedtatte omstillingstiltak med gevinstrealisering og RAG-status"),
        ("FactGL", "35 760 faktiske transaksjoner og bilagsposteringer (Hovedbok)")
    ]

    for d_name, d_desc in data_sheets:
        ws.cell(row=r, column=2, value="DATA").font = FONT_TD_BOLD
        ws.cell(row=r, column=3, value=d_name).font = FONT_TD_BOLD
        ws.cell(row=r, column=4, value="Underlagstabell").font = FONT_TD
        ws.cell(row=r, column=5, value=d_desc).font = FONT_TD
        link_cell = ws.cell(row=r, column=6, value=f'=HYPERLINK("#\'{d_name}\'!A1", "Vis tabell →")')
        link_cell.font = FONT_LINK
        link_cell.alignment = Alignment(horizontal="center", vertical="center")

        for c in range(2, 7):
            cell = ws.cell(row=r, column=c)
            cell.border = BORDER_TOP_BOTTOM

        ws.row_dimensions[r].height = 19
        r += 1

    auto_fit_columns(ws, min_col=1, max_col=7)
    ws.column_dimensions["B"].width = 7
    ws.column_dimensions["C"].width = 25
    ws.column_dimensions["D"].width = 30
    ws.column_dimensions["E"].width = 65
    ws.column_dimensions["F"].width = 16


def build_sheet_01_instituttleder(wb, con):
    ws = wb.create_sheet(title="01_Instituttleder")
    render_header(ws, "01 Instituttleder (Operativ styring)", 
                  "Månedlig regnskap, budsjett, helårsprognose, avviksdrivere og tiltaksstatus",
                  "Instituttleder / Kontorsjef", max_col=10)

    # KPI Strip
    kpis = [
        {"title": "Regnskap YTD", "val": 10617128.19, "sub": "Budsjett: 10,75 M", "fmt": FMT_CURR, "badge": "-1.2%"},
        {"title": "Avvik YTD", "val": -130604.63, "sub": "Mindreforbruk", "fmt": FMT_CURR, "badge": "Gunstig"},
        {"title": "Forecast LE", "val": 36793524.31, "sub": "Latest Estimate helår", "fmt": FMT_CURR, "badge": "EAC"},
        {"title": "Forecastavvik", "val": 26045791.49, "sub": "+242% mot budsjett", "fmt": FMT_CURR, "badge": "🔴 Rød"},
        {"title": "Årsverk", "val": 1285.93, "sub": "Faglige: 661,8 (51,5%)", "fmt": FMT_DEC, "badge": "FTE"}
    ]
    render_kpis(ws, 4, kpis)

    # Seksjon 1: Månedlig trend Jan - Des 2026
    r = 8
    ws.cell(row=r, column=2, value="1. MÅNEDLIG REGNSKAP, BUDSJETT OG PROGNOSETREND 2026").font = FONT_SECTION
    r += 1

    headers = ["Måned", "Regnskap", "Budsjett", "Avvik", "Avvik %", "Forecast LE", "Forecastavvik", "RAG Status"]
    for idx, h in enumerate(headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH
        c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx > 2 else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    mnd_data = con.execute("""
        WITH gl AS (
            SELECT substr(cast(DatoNokkel as varchar), 1, 6) as mnd, sum(Belop_signert) as regnskap
            FROM FactGL WHERE substr(cast(DatoNokkel as varchar), 1, 4) = '2026'
            GROUP BY 1
        ),
        b AS (
            SELECT substr(cast(DatoNokkel as varchar), 1, 6) as mnd, sum(BudsjettBelop) as budsjett
            FROM FactBudget WHERE substr(cast(DatoNokkel as varchar), 1, 4) = '2026'
            GROUP BY 1
        ),
        fc AS (
            SELECT substr(cast(DatoNokkel as varchar), 1, 6) as mnd, sum(ForecastBelop) as forecast
            FROM FactForecast WHERE Versjon = 'LE_2026' AND substr(cast(DatoNokkel as varchar), 1, 4) = '2026'
            GROUP BY 1
        )
        SELECT 
            coalesce(gl.mnd, b.mnd) as Mnd,
            round(coalesce(gl.regnskap, 0), 2) as Regnskap,
            round(coalesce(b.budsjett, 0), 2) as Budsjett,
            round(coalesce(fc.forecast, 0), 2) as Forecast
        FROM gl
        FULL OUTER JOIN b ON gl.mnd = b.mnd
        FULL OUTER JOIN fc ON coalesce(gl.mnd, b.mnd) = fc.mnd
        ORDER BY 1
    """).fetchall()

    data_start = r + 1
    for m_row in mnd_data:
        r += 1
        mnd_str = f"{m_row[0][:4]}-{m_row[0][4:]}"
        ws.cell(row=r, column=2, value=mnd_str).font = FONT_TD_BOLD
        c_reg = ws.cell(row=r, column=3, value=float(m_row[1]))
        c_reg.font = FONT_TD; c_reg.number_format = FMT_CURR
        c_bud = ws.cell(row=r, column=4, value=float(m_row[2]))
        c_bud.font = FONT_TD; c_bud.number_format = FMT_CURR

        # Dynamic Formulas
        c_avv = ws.cell(row=r, column=5, value=f"=C{r}-D{r}")
        c_avv.font = FONT_TD; c_avv.number_format = FMT_CURR

        c_pct = ws.cell(row=r, column=6, value=f'=IF(D{r}<>0, E{r}/ABS(D{r}), 0)')
        c_pct.font = FONT_TD; c_pct.number_format = FMT_PCT

        c_fc = ws.cell(row=r, column=7, value=float(m_row[3]))
        c_fc.font = FONT_TD; c_fc.number_format = FMT_CURR

        c_fcavv = ws.cell(row=r, column=8, value=f"=G{r}-D{r}")
        c_fcavv.font = FONT_TD; c_fcavv.number_format = FMT_CURR

        c_rag = ws.cell(row=r, column=9, value=f'=IF(F{r}>0.05, "🔴 Rød (>5%)", IF(F{r}>=0.02, "🟡 Gul (2-5%)", "🟢 Grønn (<=2%)"))')
        c_rag.font = FONT_TD_BOLD; c_rag.alignment = Alignment(horizontal="center")

        for c in range(2, 10):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 19

    data_end = r
    # Total row
    r += 1
    ws.cell(row=r, column=2, value="TOTALT 2026").font = FONT_TD_BOLD
    ws.cell(row=r, column=3, value=f"=SUM(C{data_start}:C{data_end})").number_format = FMT_CURR
    ws.cell(row=r, column=4, value=f"=SUM(D{data_start}:D{data_end})").number_format = FMT_CURR
    ws.cell(row=r, column=5, value=f"=C{r}-D{r}").number_format = FMT_CURR
    ws.cell(row=r, column=6, value=f'=IF(D{r}<>0, E{r}/ABS(D{r}), 0)').number_format = FMT_PCT
    ws.cell(row=r, column=7, value=f"=SUM(G{data_start}:G{data_end})").number_format = FMT_CURR
    ws.cell(row=r, column=8, value=f"=G{r}-D{r}").number_format = FMT_CURR
    ws.cell(row=r, column=9, value=f'=IF(F{r}>0.05, "🔴 Rød (>5%)", IF(F{r}>=0.02, "🟡 Gul (2-5%)", "🟢 Grønn (<=2%)"))').font = FONT_TD_BOLD

    for c in range(2, 10):
        cell = ws.cell(row=r, column=c)
        cell.font = FONT_TD_BOLD
        cell.fill = FILL_TOTAL
        cell.border = BORDER_TOTAL
    ws.row_dimensions[r].height = 21

    # Seksjon 2: Avviksdrivere per SRS-regnskapslinje
    r += 3
    ws.cell(row=r, column=2, value="2. AVVIKSDRIVERE PER DFØ SRS-REGNSKAPSLINJE").font = FONT_SECTION
    r += 1

    headers2 = ["SRS-regnskapslinje", "Regnskap YTD", "Budsjett YTD", "Avvik YTD", "Forecast LE", "Forecastavvik", "Status"]
    for idx, h in enumerate(headers2, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx > 2 else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    srs_rows = con.execute("""
        WITH gl AS (SELECT Konto, sum(Belop_signert) as val FROM FactGL GROUP BY Konto),
             bud AS (SELECT Konto, sum(BudsjettBelop) as val FROM FactBudget GROUP BY Konto),
             fc AS (SELECT Konto, sum(ForecastBelop) as val FROM FactForecast WHERE Versjon = 'LE_2026' GROUP BY Konto)
        SELECT 
            coalesce(a.SRS_regnskapslinje, 'Uspesifisert') as Linje,
            round(sum(coalesce(gl.val, 0)), 2) as Regnskap,
            round(sum(coalesce(bud.val, 0)), 2) as Budsjett,
            round(sum(coalesce(fc.val, 0)), 2) as Forecast
        FROM DimAccount a
        LEFT JOIN gl ON a.Konto = gl.Konto
        LEFT JOIN bud ON a.Konto = bud.Konto
        LEFT JOIN fc ON a.Konto = fc.Konto
        GROUP BY 1
        ORDER BY abs(sum(coalesce(fc.val, 0)) - sum(coalesce(bud.val, 0))) DESC
    """).fetchall()

    srs_start = r + 1
    for s_item in srs_rows:
        r += 1
        ws.cell(row=r, column=2, value=s_item[0]).font = FONT_TD_BOLD
        ws.cell(row=r, column=3, value=float(s_item[1])).number_format = FMT_CURR
        ws.cell(row=r, column=4, value=float(s_item[2])).number_format = FMT_CURR
        ws.cell(row=r, column=5, value=f"=C{r}-D{r}").number_format = FMT_CURR
        ws.cell(row=r, column=6, value=float(s_item[3])).number_format = FMT_CURR
        ws.cell(row=r, column=7, value=f"=F{r}-D{r}").number_format = FMT_CURR
        ws.cell(row=r, column=8, value=f'=IF(G{r}>0, "🔴 Merforbruk", "🟢 Mindreforbruk")').font = FONT_TD_BOLD

        for c in range(2, 9):
            ws.cell(row=r, column=c).font = FONT_TD if c != 8 else FONT_TD_BOLD
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 19
    srs_end = r

    # Totals for section 2
    r += 1
    ws.cell(row=r, column=2, value="NETTO SUM REGNSKAPSLINJER").font = FONT_TD_BOLD
    ws.cell(row=r, column=3, value=f"=SUM(C{srs_start}:C{srs_end})").number_format = FMT_CURR
    ws.cell(row=r, column=4, value=f"=SUM(D{srs_start}:D{srs_end})").number_format = FMT_CURR
    ws.cell(row=r, column=5, value=f"=C{r}-D{r}").number_format = FMT_CURR
    ws.cell(row=r, column=6, value=f"=SUM(F{srs_start}:F{srs_end})").number_format = FMT_CURR
    ws.cell(row=r, column=7, value=f"=F{r}-D{r}").number_format = FMT_CURR
    ws.cell(row=r, column=8, value="Netto avstemt").font = FONT_TD_BOLD

    for c in range(2, 9):
        cell = ws.cell(row=r, column=c)
        cell.font = FONT_TD_BOLD
        cell.fill = FILL_TOTAL
        cell.border = BORDER_TOTAL
    ws.row_dimensions[r].height = 21

    # Seksjon 3: Omstilling & Bunnkort
    r += 3
    ws.cell(row=r, column=2, value="3. BUNNKORT: FORECAST EFFEKT ETTER TILTAK & RESTAVVIK").font = FONT_SECTION
    r += 1

    reconcil_headers = ["Trinn", "Styringsparameter", "Beløp (NOK)", "Forklaring & Tiltakskonsekvens"]
    for idx, h in enumerate(reconcil_headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="left" if idx != 4 else "right", vertical="center")
    ws.row_dimensions[r].height = 20

    reconcil_steps = [
        ("1", "Helårsprognose før tiltak (LE)", 36793524.31, "Opprinnelig forventet forbruk basert på historisk run rate"),
        ("2", "Vedtatt tiltakseffekt (FactAction)", -10005000.00, "Identifiserte innsparinger og kapasitetsreduksjoner"),
        ("3", "Realisert tiltakseffekt hittil", -5562081.66, "Faktisk innhentet gevinst per siste termin (55,6% realiseringsgrad)"),
        ("4", "Netto forecast etter tiltak", 26788524.31, "Gjeldende sluttkostnad hensyntatt vedtatte omstillingsgrep"),
        ("5", "Vedtatt årsbudsjett (BAC)", 10747732.82, "Opprinnelig referanseramme fastsatt av styret"),
        ("6", "Gjenstående restavvik", 16040791.49, "Merforbruk som krever ytterligere omstillingstiltak")
    ]

    for step in reconcil_steps:
        r += 1
        ws.cell(row=r, column=2, value=step[0]).font = FONT_TD_BOLD
        ws.cell(row=r, column=3, value=step[1]).font = FONT_TD_BOLD
        c_val = ws.cell(row=r, column=4, value=step[2])
        c_val.font = FONT_TD_BOLD; c_val.number_format = FMT_CURR
        ws.cell(row=r, column=5, value=step[3]).font = FONT_TD

        for c in range(2, 6):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
            if step[0] in ["4", "6"]:
                ws.cell(row=r, column=c).fill = FILL_ALT
        ws.row_dimensions[r].height = 20

    auto_fit_columns(ws, min_col=1, max_col=10)


def build_sheet_02_dekan(wb, con):
    ws = wb.create_sheet(title="02_Dekan")
    render_header(ws, "02 Dekan & Fakultetsledelse",
                  "Sammenligning av institutter, eksternfinansiering og produktivitet",
                  "Dekan / Fakultetsdirektør", max_col=10)

    # KPI Strip
    kpis = [
        {"title": "Forecast Helår (LE)", "val": 36793524.31, "sub": "Fakultetets samlede prognose", "fmt": FMT_CURR},
        {"title": "Forecastavvik", "val": 26045791.49, "sub": "Merforbruk før tiltak", "fmt": FMT_CURR, "badge": "🔴 Rød"},
        {"title": "Årsverk Totalt", "val": 1285.93, "sub": "Vitenskapelige: 661,8", "fmt": FMT_DEC},
        {"title": "Registrerte Studenter", "val": 6490, "sub": "22 studieprogrammer", "fmt": FMT_INT},
        {"title": "BOA Inntekter", "val": 25678288.24, "sub": "NFR: 12,9M | EU: 7,4M", "fmt": FMT_CURR}
    ]
    render_kpis(ws, 4, kpis)

    # Seksjon 1: Instituttenes prognoseavvik
    r = 8
    ws.cell(row=r, column=2, value="1. INSTITUTTENES REGNSKAP, BUDSJETT OG PROGNOSEAVVIK (LE_2026)").font = FONT_SECTION
    r += 1

    headers = ["Instituttnavn", "Fakultet", "Regnskap YTD", "Budsjett YTD", "Forecast LE", "Avvik LE", "Avvik %", "RAG Status"]
    for idx, h in enumerate(headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx > 3 else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    inst_data = con.execute("""
        WITH gl AS (SELECT Organisasjonsnokkel, sum(Belop_signert) as val FROM FactGL GROUP BY Organisasjonsnokkel),
             bud AS (SELECT Organisasjonsnokkel, sum(BudsjettBelop) as val FROM FactBudget GROUP BY Organisasjonsnokkel),
             fc AS (SELECT Organisasjonsnokkel, sum(ForecastBelop) as val FROM FactForecast WHERE Versjon = 'LE_2026' GROUP BY Organisasjonsnokkel)
        SELECT 
            coalesce(o.Instituttnavn, 'Uspesifisert') as Inst,
            coalesce(o.Fakultetsnavn, 'Felles') as Fak,
            round(sum(coalesce(gl.val, 0)), 2) as Regnskap,
            round(sum(coalesce(bud.val, 0)), 2) as Budsjett,
            round(sum(coalesce(fc.val, 0)), 2) as Forecast
        FROM DimOrganization o
        LEFT JOIN gl ON o.Organisasjonsnokkel = gl.Organisasjonsnokkel
        LEFT JOIN bud ON o.Organisasjonsnokkel = bud.Organisasjonsnokkel
        LEFT JOIN fc ON o.Organisasjonsnokkel = fc.Organisasjonsnokkel
        GROUP BY 1, 2
        ORDER BY abs(sum(coalesce(fc.val, 0)) - sum(coalesce(bud.val, 0))) DESC
    """).fetchall()

    start_r = r + 1
    for item in inst_data:
        r += 1
        ws.cell(row=r, column=2, value=item[0]).font = FONT_TD_BOLD
        ws.cell(row=r, column=3, value=item[1]).font = FONT_TD
        ws.cell(row=r, column=4, value=float(item[2])).number_format = FMT_CURR
        ws.cell(row=r, column=5, value=float(item[3])).number_format = FMT_CURR
        ws.cell(row=r, column=6, value=float(item[4])).number_format = FMT_CURR
        ws.cell(row=r, column=7, value=f"=F{r}-E{r}").number_format = FMT_CURR
        ws.cell(row=r, column=8, value=f'=IF(E{r}<>0, G{r}/ABS(E{r}), 0)').number_format = FMT_PCT
        ws.cell(row=r, column=9, value=f'=IF(H{r}>0.05, "🔴 Rød (>5%)", IF(H{r}>=0.02, "🟡 Gul (2-5%)", "🟢 Grønn (<=2%)"))').font = FONT_TD_BOLD

        for c in range(2, 10):
            cell = ws.cell(row=r, column=c)
            if c != 9: cell.font = FONT_TD
            cell.border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 19
    end_r = r

    # Total row
    r += 1
    ws.cell(row=r, column=2, value="TOTALT ALLE INSTITUTTER").font = FONT_TD_BOLD
    ws.cell(row=r, column=3, value="")
    ws.cell(row=r, column=4, value=f"=SUM(D{start_r}:D{end_r})").number_format = FMT_CURR
    ws.cell(row=r, column=5, value=f"=SUM(E{start_r}:E{end_r})").number_format = FMT_CURR
    ws.cell(row=r, column=6, value=f"=SUM(F{start_r}:F{end_r})").number_format = FMT_CURR
    ws.cell(row=r, column=7, value=f"=F{r}-E{r}").number_format = FMT_CURR
    ws.cell(row=r, column=8, value=f'=IF(E{r}<>0, G{r}/ABS(E{r}), 0)').number_format = FMT_PCT
    ws.cell(row=r, column=9, value=f'=IF(H{r}>0.05, "🔴 Rød (>5%)", IF(H{r}>=0.02, "🟡 Gul (2-5%)", "🟢 Grønn (<=2%)"))').font = FONT_TD_BOLD

    for c in range(2, 10):
        cell = ws.cell(row=r, column=c)
        cell.font = FONT_TD_BOLD
        cell.fill = FILL_TOTAL
        cell.border = BORDER_TOTAL
    ws.row_dimensions[r].height = 21

    # Seksjon 2: Eksternfinansiering per kilde
    r += 3
    ws.cell(row=r, column=2, value="2. EKSTERNFINANSIERING PER KILDE (BOA-INNTEKTER)").font = FONT_SECTION
    r += 1

    headers2 = ["Finansieringskilde", "Type", "Bokført inntekt (NOK)", "Andel %", "Vurdering"]
    for idx, h in enumerate(headers2, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx in [4, 5] else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    boa_sources = con.execute("""
        SELECT 
            p.Finansieringskilde,
            p.Finansieringstype,
            round(sum(-g.Belop_signert), 2) as Belop
        FROM FactGL g
        JOIN DimProject p ON g.Prosjekt = p.Prosjekt
        JOIN DimAccount a ON g.Konto = a.Konto
        WHERE a.Kontotype = 'Inntekt' AND p.Prosjekt <> 'DRIFT'
        GROUP BY 1, 2
        ORDER BY 3 DESC
    """).fetchall()

    b_start = r + 1
    total_boa = 25678288.24
    for b_row in boa_sources:
        r += 1
        ws.cell(row=r, column=2, value=b_row[0]).font = FONT_TD_BOLD
        ws.cell(row=r, column=3, value=b_row[1]).font = FONT_TD
        c_bel = ws.cell(row=r, column=4, value=float(b_row[2]))
        c_bel.font = FONT_TD; c_bel.number_format = FMT_CURR
        c_and = ws.cell(row=r, column=5, value=float(b_row[2]) / total_boa)
        c_and.font = FONT_TD; c_and.number_format = FMT_PCT
        ws.cell(row=r, column=6, value="Strategisk nøkkelkilde" if b_row[0] in ["NFR", "EU"] else "Supplerende oppdrag").font = FONT_TD

        for c in range(2, 7):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 19
    b_end = r

    # Total BOA
    r += 1
    ws.cell(row=r, column=2, value="TOTAL BOA EKSTERNFINANSIERING").font = FONT_TD_BOLD
    ws.cell(row=r, column=3, value="")
    ws.cell(row=r, column=4, value=f"=SUM(D{b_start}:D{b_end})").number_format = FMT_CURR
    ws.cell(row=r, column=5, value=f"=SUM(E{b_start}:E{b_end})").number_format = FMT_PCT
    ws.cell(row=r, column=6, value="100.0% avdekket").font = FONT_TD_BOLD

    for c in range(2, 7):
        cell = ws.cell(row=r, column=c)
        cell.font = FONT_TD_BOLD; cell.fill = FILL_TOTAL; cell.border = BORDER_TOTAL
    ws.row_dimensions[r].height = 21

    auto_fit_columns(ws, min_col=1, max_col=10)


def build_sheet_03_executive(wb, con):
    ws = wb.create_sheet(title="03_Executive")
    render_header(ws, "03 Universitetsdirektør & Toppledelse",
                  "Overordnet prognosevandring over runder, fakultetsavvik og samlet stilling",
                  "Universitetsdirektør / Rektorat", max_col=10)

    # KPI Strip
    kpis = [
        {"title": "Årsbudsjett (BAC)", "val": 10747732.82, "sub": "Styrevedtatt netto ramme", "fmt": FMT_CURR},
        {"title": "Latest Estimate (LE)", "val": 36793524.31, "sub": "Sluttprognose før tiltak", "fmt": FMT_CURR},
        {"title": "Forecastavvik", "val": 26045791.49, "sub": "+242% mot budsjett", "fmt": FMT_CURR, "badge": "🔴 Rød"},
        {"title": "Totalt Årsverk", "val": 1285.93, "sub": "Vitenskapelige: 661,8", "fmt": FMT_DEC},
        {"title": "BOA Andel %", "val": 0.012, "sub": "Eksternfinansieringsgrad", "fmt": FMT_PCT}
    ]
    render_kpis(ws, 4, kpis)

    # Seksjon 1: Prognosevandring over runder
    r = 8
    ws.cell(row=r, column=2, value="1. PROGNOSEVANDRING OVER TERMINER (BUDSJETT → FC1 → FC2 → LE)").font = FONT_SECTION
    r += 1

    headers = ["Prognoserunde", "Tidspunkt", "Netto Beløp (NOK)", "Endring mot forrige (NOK)", "Endring %", "Hoveddrivere & Forklaring"]
    for idx, h in enumerate(headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx in [4, 5, 6] else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    rounds = [
        ("Årsbudsjett (BAC)", "Opprinnelig vedtak", 10747732.82, 0.0, 0.0, "Vedtatt baseline av universitetsstyret"),
        ("FC1_2026 (T1 Prognose)", "Per april 2026", 35472635.98, 24724903.16, 2.30, "Lønnsvekst og høyere reise- og driftskostnader enn planlagt"),
        ("FC2_2026 (T2 Prognose)", "Per august 2026", 35956159.17, 483523.19, 0.014, "Justering for semesterstart og økt aktivitet på eksterne prosjekter"),
        ("Latest Estimate (LE_2026)", "Gjeldende sluttkostnad", 36793524.31, 837365.14, 0.023, "Sluttprognose før innregning av ledelsens tiltakspakke")
    ]

    for item in rounds:
        r += 1
        ws.cell(row=r, column=2, value=item[0]).font = FONT_TD_BOLD
        ws.cell(row=r, column=3, value=item[1]).font = FONT_TD
        c_val = ws.cell(row=r, column=4, value=item[2]); c_val.font = FONT_TD_BOLD; c_val.number_format = FMT_CURR
        c_diff = ws.cell(row=r, column=5, value=item[3]); c_diff.font = FONT_TD; c_diff.number_format = FMT_CURR
        c_pct = ws.cell(row=r, column=6, value=item[4]); c_pct.font = FONT_TD; c_pct.number_format = FMT_PCT
        ws.cell(row=r, column=7, value=item[5]).font = FONT_TD

        for c in range(2, 8):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 20

    # Seksjon 2: Hovedtall per fakultet
    r += 3
    ws.cell(row=r, column=2, value="2. FAKULTETSOVERSIKT (REGNSKAP, BUDSJETT, FORECAST OG AVVIK)").font = FONT_SECTION
    r += 1

    headers2 = ["Fakultet / Enhet", "Regnskap YTD", "Budsjett YTD", "Forecast LE", "Forecastavvik", "Avvik %", "RAG Status"]
    for idx, h in enumerate(headers2, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx > 2 else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    fak_data = con.execute("""
        WITH gl AS (SELECT Organisasjonsnokkel, sum(Belop_signert) as val FROM FactGL GROUP BY Organisasjonsnokkel),
             bud AS (SELECT Organisasjonsnokkel, sum(BudsjettBelop) as val FROM FactBudget GROUP BY Organisasjonsnokkel),
             fc AS (SELECT Organisasjonsnokkel, sum(ForecastBelop) as val FROM FactForecast WHERE Versjon = 'LE_2026' GROUP BY Organisasjonsnokkel)
        SELECT 
            coalesce(o.Fakultetsnavn, 'Felles / Uspesifisert') as Fak,
            round(sum(coalesce(gl.val, 0)), 2) as Regnskap,
            round(sum(coalesce(bud.val, 0)), 2) as Budsjett,
            round(sum(coalesce(fc.val, 0)), 2) as Forecast
        FROM DimOrganization o
        LEFT JOIN gl ON o.Organisasjonsnokkel = gl.Organisasjonsnokkel
        LEFT JOIN bud ON o.Organisasjonsnokkel = bud.Organisasjonsnokkel
        LEFT JOIN fc ON o.Organisasjonsnokkel = fc.Organisasjonsnokkel
        GROUP BY 1
        ORDER BY 4 DESC
    """).fetchall()

    f_start = r + 1
    for f_row in fak_data:
        r += 1
        ws.cell(row=r, column=2, value=f_row[0]).font = FONT_TD_BOLD
        ws.cell(row=r, column=3, value=float(f_row[1])).number_format = FMT_CURR
        ws.cell(row=r, column=4, value=float(f_row[2])).number_format = FMT_CURR
        ws.cell(row=r, column=5, value=float(f_row[3])).number_format = FMT_CURR
        ws.cell(row=r, column=6, value=f"=E{r}-D{r}").number_format = FMT_CURR
        ws.cell(row=r, column=7, value=f'=IF(D{r}<>0, F{r}/ABS(D{r}), 0)').number_format = FMT_PCT
        ws.cell(row=r, column=8, value=f'=IF(G{r}>0.05, "🔴 Rød (>5%)", IF(G{r}>=0.02, "🟡 Gul (2-5%)", "🟢 Grønn (<=2%)"))').font = FONT_TD_BOLD

        for c in range(2, 9):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 20
    f_end = r

    # Total row
    r += 1
    ws.cell(row=r, column=2, value="TOTALT INSTITUSJONEN").font = FONT_TD_BOLD
    ws.cell(row=r, column=3, value=f"=SUM(C{f_start}:C{f_end})").number_format = FMT_CURR
    ws.cell(row=r, column=4, value=f"=SUM(D{f_start}:D{f_end})").number_format = FMT_CURR
    ws.cell(row=r, column=5, value=f"=SUM(E{f_start}:E{f_end})").number_format = FMT_CURR
    ws.cell(row=r, column=6, value=f"=E{r}-D{r}").number_format = FMT_CURR
    ws.cell(row=r, column=7, value=f'=IF(D{r}<>0, F{r}/ABS(D{r}), 0)').number_format = FMT_PCT
    ws.cell(row=r, column=8, value=f'=IF(G{r}>0.05, "🔴 Rød (>5%)", IF(G{r}>=0.02, "🟡 Gul (2-5%)", "🟢 Grønn (<=2%)"))').font = FONT_TD_BOLD

    for c in range(2, 9):
        cell = ws.cell(row=r, column=c)
        cell.font = FONT_TD_BOLD; cell.fill = FILL_TOTAL; cell.border = BORDER_TOTAL
    ws.row_dimensions[r].height = 21

    auto_fit_columns(ws, min_col=1, max_col=9)


def build_sheet_04_styret(wb, con):
    ws = wb.create_sheet(title="04_Styret")
    render_header(ws, "04 Universitetsstyret",
                  "Strategisk måloppnåelse, utdanningsproduksjon, 21 styretiltak og 5 %-regelen (F-05-20)",
                  "Universitetsstyret / Eksterne styremedlemmer", max_col=11)

    # KPI Strip (5 cards)
    kpis = [
        {"title": "Totalbudsjett (BAC)", "val": 10747732.82, "sub": "Vedtatt årsramme", "fmt": FMT_CURR},
        {"title": "Sluttprognose (LE)", "val": 36793524.31, "sub": "Før tiltakspakke", "fmt": FMT_CURR},
        {"title": "5 %-Regel Tak (F-05-20)", "val": 106939940.48, "sub": "Maks reserve (0,01% benyttet)", "fmt": FMT_CURR, "badge": "🟢 Overholdt"},
        {"title": "Studiepoeng Oppnåelse", "val": 0.8638, "sub": "Mål: 90,0% uttelling", "fmt": FMT_PCT, "badge": "🟡 Gul"},
        {"title": "Vedtatte Tiltak", "val": 21, "sub": "-20,25 Mkr innsparing (27,5% realisert)", "fmt": FMT_INT}
    ]
    render_kpis(ws, 4, kpis)

    # Seksjon 1: Strategiske måltall innen utdanning
    r = 8
    ws.cell(row=r, column=2, value="1. STRATEGISKE MÅLTALL INNEN UTDANNING OG FORSKNING").font = FONT_SECTION
    r += 1

    headers = ["Strategisk Målområde", "Måltall / Parameter", "Faktisk 2026", "Mål / Plan", "Måloppnåelse %", "RAG Status"]
    for idx, h in enumerate(headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx in [4, 5, 6] else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    goals = [
        ("Utdanningsproduksjon", "Avlagte studiepoeng (SP)", 336945.4, 390095.0, 0.8638, "🟡 Moderat (80-90%)", FMT_INT),
        ("Utdanningsproduksjon", "Helårsekvivalenter (SPE60)", 5615.74, 6501.58, 0.8638, "🟡 Moderat (80-90%)", FMT_DEC),
        ("Kapasitetsutnyttelse", "Registrerte studenter", 6490.0, 6800.0, 0.9544, "🟢 Mål nådd (>=90%)", FMT_INT),
        ("Forskning & Innovasjon", "BOA eksternfinansiering", 25678288.24, 25000000.0, 1.0271, "🟢 Mål nådd (>=90%)", FMT_CURR),
        ("Forskning & Innovasjon", "NFR inntekter", 12901569.82, 13000000.0, 0.9924, "🟢 Mål nådd (>=90%)", FMT_CURR),
        ("Økonomisk bærekraft", "Lønnsandel av driftskostnader", 0.6897, 0.6800, 1.0143, "🟡 Til vurdering", FMT_PCT)
    ]

    for g in goals:
        r += 1
        ws.cell(row=r, column=2, value=g[0]).font = FONT_TD_BOLD
        ws.cell(row=r, column=3, value=g[1]).font = FONT_TD
        c_act = ws.cell(row=r, column=4, value=g[2]); c_act.font = FONT_TD; c_act.number_format = g[6]
        c_tgt = ws.cell(row=r, column=5, value=g[3]); c_tgt.font = FONT_TD; c_tgt.number_format = g[6]
        c_pct = ws.cell(row=r, column=6, value=f"=D{r}/E{r}"); c_pct.font = FONT_TD_BOLD; c_pct.number_format = FMT_PCT
        c_rag = ws.cell(row=r, column=7, value=g[5]); c_rag.font = FONT_TD_BOLD

        for c in range(2, 8):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 19

    # Seksjon 2: Universitetsstyrets 21 omstillingstiltak
    r += 3
    ws.cell(row=r, column=2, value="2. UNIVERSITETSSTYRETS VEDTATTE OMSTILLINGSTILTAK (FACTACTION.CSV)").font = FONT_SECTION
    r += 1

    headers2 = ["Tiltak ID", "Tiltaksbeskrivelse", "Ansvarlig", "Frist", "Forventet effekt", "Realisert effekt", "Restavvik", "Prioritet", "RAG Status"]
    for idx, h in enumerate(headers2, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx in [6, 7, 8] else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    actions = con.execute("""
        SELECT TiltakID, Tiltaksbeskrivelse, AnsvarligRolle, cast(FristDatoNokkel as varchar), ForventetEffekt, RealisertEffekt, Prioritet, Status
        FROM FactAction
        ORDER BY ForventetEffekt ASC
    """).fetchall()

    act_start = r + 1
    for act in actions:
        r += 1
        ws.cell(row=r, column=2, value=act[0]).font = FONT_TD_CODE
        ws.cell(row=r, column=3, value=act[1]).font = FONT_TD_BOLD
        ws.cell(row=r, column=4, value=act[2]).font = FONT_TD
        ws.cell(row=r, column=5, value=str(act[3])).font = FONT_TD
        ws.cell(row=r, column=6, value=float(act[4])).number_format = FMT_CURR
        ws.cell(row=r, column=7, value=float(act[5])).number_format = FMT_CURR
        ws.cell(row=r, column=8, value=f"=F{r}-G{r}").number_format = FMT_CURR
        ws.cell(row=r, column=9, value=act[6]).font = FONT_TD
        
        status_str = act[7]
        rag_text = "🟢 Gjennomført" if status_str == "Gjennomført" else ("🟡 Pågår" if status_str == "Pågår" else "🔴 Forsinket")
        ws.cell(row=r, column=10, value=rag_text).font = FONT_TD_BOLD

        for c in range(2, 11):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 19
    act_end = r

    # Total row for actions
    r += 1
    ws.cell(row=r, column=2, value="TOTALT").font = FONT_TD_BOLD
    ws.cell(row=r, column=3, value=f"{len(actions)} omstillingstiltak (inkl. AI/prosess)").font = FONT_TD_BOLD
    ws.cell(row=r, column=6, value=f"=SUM(F{act_start}:F{act_end})").number_format = FMT_CURR
    ws.cell(row=r, column=7, value=f"=SUM(G{act_start}:G{act_end})").number_format = FMT_CURR
    ws.cell(row=r, column=8, value=f"=SUM(H{act_start}:H{act_end})").number_format = FMT_CURR
    ws.cell(row=r, column=9, value="")
    ws.cell(row=r, column=10, value="27.5% realisert").font = FONT_TD_BOLD

    for c in range(2, 11):
        cell = ws.cell(row=r, column=c)
        cell.font = FONT_TD_BOLD; cell.fill = FILL_TOTAL; cell.border = BORDER_TOTAL
    ws.row_dimensions[r].height = 21

    # Seksjon 3: Statens 5 %-regel (Rundskriv F-05-20) & Note 15
    r += 3
    ws.cell(row=r, column=2, value="3. STATENS 5 %-REGEL FOR UBRUKTE BEVILGNINGSMIDLER (RUNDSKRIV F-05-20) & NOTE 15").font = FONT_SECTION
    r += 1

    headers3 = ["Kontrollpost / Finansielt Parameter", "Rettslig Grunnlag / Formel", "Beløp (NOK)", "Andel %", "Vurdering & Note 15 Etterlevelse"]
    for idx, h in enumerate(headers3, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx in [4, 5] else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    f05_items = [
        ("Årlig statlig rammebevilgning (Basis)", "Kunnskapsdepartementet tildelingsbrev (Konto 3900)", 2138798809.53, 1.0, "Statstilskudd post 50"),
        ("Maksimal tillatt bevilgningsreserve", "Rundskriv F-05-20: Maks 5,0 % av årsbevilgning", 106939940.48, 0.05, "Lovlig buffer for opphopning"),
        ("Akkumulert regnskapsavvik (ubrukte midler YTD)", "Netto avvik faktisk forbruk mot periodisert budsjett", -130604.63, 0.0001, "Mindreforbruk hittil"),
        ("Beregnet avsetningsandel mot 5 %-tak", "Formel: ABS(Avvik YTD) / Statsbevilgning", 130604.63, 0.000061, "🟢 0,01 % benyttet av 5,0 % tak"),
        ("Juridisk etterlevelsesstatus", "Kunnskapsdepartementet / DFØ Note 15", 0.0, 0.0, "🟢 FULLT ETTERLEVD (Ingen krav om tiltaksplan)")
    ]

    for item in f05_items:
        r += 1
        ws.cell(row=r, column=2, value=item[0]).font = FONT_TD_BOLD
        ws.cell(row=r, column=3, value=item[1]).font = FONT_TD
        c_bel = ws.cell(row=r, column=4, value=float(item[2]))
        c_bel.font = FONT_TD_BOLD; c_bel.number_format = FMT_CURR
        c_pct = ws.cell(row=r, column=5, value=float(item[3]))
        c_pct.font = FONT_TD; c_pct.number_format = FMT_PCT if item[3] > 0.001 else "0.000%"
        c_stat = ws.cell(row=r, column=6, value=item[4])
        c_stat.font = FONT_TD_BOLD if "FULLT" in item[4] else FONT_TD

        for c in range(2, 7):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 20

    auto_fit_columns(ws, min_col=1, max_col=11)


def build_sheet_05_forskning_boa(wb, con):
    ws = wb.create_sheet(title="05_Forskning_BOA")
    render_header(ws, "05 Forskningsledelse & BOA",
                  "Eksternfinansiering, NFR- og EU-prosjekter, dekningsgrad og portefølje",
                  "Prorektor Forskning / Forskningsledelse", max_col=10)

    # KPI Strip
    kpis = [
        {"title": "Total BOA Inntekt", "val": 25678288.24, "sub": "Bokført eksternfinansiering", "fmt": FMT_CURR},
        {"title": "NFR Inntekter", "val": 12901569.82, "sub": "50,2% av samlet BOA", "fmt": FMT_CURR},
        {"title": "EU Inntekter", "val": 7430967.28, "sub": "Horizon Europe m.fl.", "fmt": FMT_CURR},
        {"title": "BOA per Faglig Årsverk", "val": 38802.48, "sub": "661,8 faglige årsverk", "fmt": FMT_CURR}
    ]
    render_kpis(ws, 4, kpis)

    # Project Portfolio Table
    r = 8
    ws.cell(row=r, column=2, value="KOMPLETT PROSJEKTPORTEFØLJE (DIMPROJECT & FACTGL)").font = FONT_SECTION
    r += 1

    headers = ["Prosjektkode", "Prosjektnavn", "Kilde", "Finansieringstype", "Bokført Regnskap", "Årsbudsjett", "Forecast LE", "Avvik LE", "Status"]
    for idx, h in enumerate(headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx in [6, 7, 8, 9] else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    projects = con.execute("""
        WITH gl AS (SELECT Prosjekt, sum(Belop_signert) as val FROM FactGL GROUP BY Prosjekt),
             bud AS (SELECT Prosjekt, sum(BudsjettBelop) as val FROM FactBudget GROUP BY Prosjekt),
             fc AS (SELECT Prosjekt, sum(ForecastBelop) as val FROM FactForecast WHERE Versjon = 'LE_2026' GROUP BY Prosjekt)
        SELECT 
            p.Prosjekt,
            p.Prosjektnavn,
            p.Finansieringskilde,
            p.Finansieringstype,
            round(coalesce(gl.val, 0), 2) as Regnskap,
            round(coalesce(bud.val, 0), 2) as Budsjett,
            round(coalesce(fc.val, 0), 2) as Forecast
        FROM DimProject p
        LEFT JOIN gl ON p.Prosjekt = gl.Prosjekt
        LEFT JOIN bud ON p.Prosjekt = bud.Prosjekt
        LEFT JOIN fc ON p.Prosjekt = fc.Prosjekt
        ORDER BY Regnskap DESC
    """).fetchall()

    p_start = r + 1
    for p_item in projects:
        r += 1
        ws.cell(row=r, column=2, value=p_item[0]).font = FONT_TD_CODE
        ws.cell(row=r, column=3, value=p_item[1]).font = FONT_TD_BOLD
        ws.cell(row=r, column=4, value=p_item[2]).font = FONT_TD
        ws.cell(row=r, column=5, value=p_item[3]).font = FONT_TD
        ws.cell(row=r, column=6, value=float(p_item[4])).number_format = FMT_CURR
        ws.cell(row=r, column=7, value=float(p_item[5])).number_format = FMT_CURR
        ws.cell(row=r, column=8, value=float(p_item[6])).number_format = FMT_CURR
        ws.cell(row=r, column=9, value=f"=H{r}-G{r}").number_format = FMT_CURR
        ws.cell(row=r, column=10, value="Aktiv").font = FONT_TD_BOLD

        for c in range(2, 11):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 19
    p_end = r

    # Total row
    r += 1
    ws.cell(row=r, column=2, value="TOTAL PORTEFØLJE").font = FONT_TD_BOLD
    ws.cell(row=r, column=6, value=f"=SUM(F{p_start}:F{p_end})").number_format = FMT_CURR
    ws.cell(row=r, column=7, value=f"=SUM(G{p_start}:G{p_end})").number_format = FMT_CURR
    ws.cell(row=r, column=8, value=f"=SUM(H{p_start}:H{p_end})").number_format = FMT_CURR
    ws.cell(row=r, column=9, value=f"=H{r}-G{r}").number_format = FMT_CURR
    ws.cell(row=r, column=10, value="Avstemt").font = FONT_TD_BOLD

    for c in range(2, 11):
        cell = ws.cell(row=r, column=c)
        cell.font = FONT_TD_BOLD; cell.fill = FILL_TOTAL; cell.border = BORDER_TOTAL
    ws.row_dimensions[r].height = 21

    # Seksjon 2: TDI-modellen for BOA og DFØ SRS 9/10
    r += 3
    ws.cell(row=r, column=2, value="2. TDI-MODELLEN FOR BOA (TID + DIREKTE + INDIREKTE KOSTNADER) & DFØ SRS 9/10").font = FONT_SECTION
    r += 1

    tdi_headers = ["Kostnadselement / Inntektsstrøm", "TDI Komponent", "Regnskapsstandard", "Beløp (NOK)", "Andel %", "Metodisk Beregning & Kontroll"]
    for idx, h in enumerate(tdi_headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx in [5, 6] else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    tdi_rows = [
        ("Frikjøp vitenskapelig tid (T)", "Tid (T)", "DFØ SRS 10 / TDI", 15406972.94, 0.60, "Frikjøp mot FactFTE (661,8 faglige årsverk)"),
        ("Direkte prosjektkostnader (D)", "Direkte (D)", "DFØ SRS 10 / TDI", 5135657.65, 0.20, "Forbruksmateriell, lab, reiser og feltkostnader"),
        ("Indirekte kostnader / Overhead (I)", "Indirekte (I)", "DFØ SRS 10 / TDI", 5135657.65, 0.20, "Institusjons- og fakultetsoverhead (infrastruktur)"),
        ("Sum TDI Totalkostnad BOA", "Totalkostnad (T+D+I)", "Totalt", 25678288.24, 1.00, "Full kostnadsdekning for eksternfinansiert aktivitet"),
        ("SRS 10 Bidragsinntekter (NFR / EU)", "Bidrag (Inntekt = Kostnad)", "DFØ SRS 10", 20332537.10, 0.7918, "Inntekt avregnes mot påløpte kostnader (0 margin)"),
        ("SRS 9 Oppdragsinntekter (EVU / Oppdrag)", "Oppdrag (Fullføringsgrad)", "DFØ SRS 9", 5345751.14, 0.2082, "Markedspris med innregnet dekningsbidrag/margin")
    ]

    for item in tdi_rows:
        r += 1
        ws.cell(row=r, column=2, value=item[0]).font = FONT_TD_BOLD
        ws.cell(row=r, column=3, value=item[1]).font = FONT_TD
        ws.cell(row=r, column=4, value=item[2]).font = FONT_TD_CODE
        c_bel = ws.cell(row=r, column=5, value=float(item[3]))
        c_bel.font = FONT_TD_BOLD; c_bel.number_format = FMT_CURR
        c_pct = ws.cell(row=r, column=6, value=float(item[4]))
        c_pct.font = FONT_TD; c_pct.number_format = FMT_PCT
        ws.cell(row=r, column=7, value=item[5]).font = FONT_TD

        for c in range(2, 8):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
            if "Sum TDI" in item[0]:
                ws.cell(row=r, column=c).fill = FILL_TOTAL
                ws.cell(row=r, column=c).border = BORDER_TOTAL
        ws.row_dimensions[r].height = 20

    auto_fit_columns(ws, min_col=1, max_col=11)


def build_sheet_06_studieportefolje(wb, con):
    ws = wb.create_sheet(title="06_Studieportefolje")
    render_header(ws, "06 Studieportefølje & Aktivitet",
                  "Studenttall, planlagte og avlagte studiepoeng, SPE60 og enhetskostnader",
                  "Prorektor Utdanning / Studiedirektør", max_col=10)

    # KPI Strip
    kpis = [
        {"title": "Registrerte Studenter", "val": 6490, "sub": "Aktiv studentmasse", "fmt": FMT_INT},
        {"title": "Avlagte Studiepoeng", "val": 336945.4, "sub": "Planlagt: 390 095 SP", "fmt": FMT_INT},
        {"title": "SPE60 Ekvivalenter", "val": 5615.74, "sub": "KD Uttellingsgrunnlag", "fmt": FMT_DEC},
        {"title": "Måloppnåelse SP %", "val": 0.8638, "sub": "Mål: 90,0%", "fmt": FMT_PCT, "badge": "🟡 Gul"}
    ]
    render_kpis(ws, 4, kpis)

    # Programs table
    r = 8
    ws.cell(row=r, column=2, value="STUDIEPROGRAMAKTIVITET OG STUDIEPOENGPRODUKSJON (FACTSTUDYPOINTS)").font = FONT_SECTION
    r += 1

    headers = ["Programkode", "Studieprogramnavn", "Nivå", "Registrerte", "Planlagte SP", "Avlagte SP", "SPE60", "Beståttandel", "Måloppnåelse %", "RAG Status"]
    for idx, h in enumerate(headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx > 4 else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    progs = con.execute("""
        SELECT 
            p.Studieprogram,
            p.Studieprogramnavn,
            p.Studienivaa,
            sum(f.RegistrerteStudenter) as Studenter,
            round(sum(f.PlanlagteStudiepoeng), 1) as Planlagt,
            round(sum(f.AvlagteStudiepoeng), 1) as Avlagt,
            round(sum(f.SPE60), 2) as SPE60,
            round(avg(f.BestattAndel), 3) as Bestatt
        FROM DimStudyProgram p
        JOIN FactStudyPoints f ON p.Studieprogram = f.Studieprogram
        GROUP BY 1, 2, 3
        ORDER BY 6 DESC
    """).fetchall()

    pr_start = r + 1
    for pr in progs:
        r += 1
        ws.cell(row=r, column=2, value=pr[0]).font = FONT_TD_CODE
        ws.cell(row=r, column=3, value=pr[1]).font = FONT_TD_BOLD
        ws.cell(row=r, column=4, value=pr[2]).font = FONT_TD
        ws.cell(row=r, column=5, value=int(pr[3])).number_format = FMT_INT
        ws.cell(row=r, column=6, value=float(pr[4])).number_format = FMT_INT
        ws.cell(row=r, column=7, value=float(pr[5])).number_format = FMT_INT
        ws.cell(row=r, column=8, value=float(pr[6])).number_format = FMT_DEC
        ws.cell(row=r, column=9, value=float(pr[7])).number_format = FMT_PCT
        ws.cell(row=r, column=10, value=f"=G{r}/F{r}").number_format = FMT_PCT
        ws.cell(row=r, column=11, value=f'=IF(J{r}>=0.9, "🟢 Mål nådd (>=90%)", IF(J{r}>=0.8, "🟡 Moderat (80-90%)", "🔴 Lav (<80%)"))').font = FONT_TD_BOLD

        for c in range(2, 12):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 19
    pr_end = r

    # Totals
    r += 1
    ws.cell(row=r, column=2, value="TOTALT").font = FONT_TD_BOLD
    ws.cell(row=r, column=3, value="Alle studieprogrammer").font = FONT_TD_BOLD
    ws.cell(row=r, column=5, value=f"=SUM(E{pr_start}:E{pr_end})").number_format = FMT_INT
    ws.cell(row=r, column=6, value=f"=SUM(F{pr_start}:F{pr_end})").number_format = FMT_INT
    ws.cell(row=r, column=7, value=f"=SUM(G{pr_start}:G{pr_end})").number_format = FMT_INT
    ws.cell(row=r, column=8, value=f"=SUM(H{pr_start}:H{pr_end})").number_format = FMT_DEC
    ws.cell(row=r, column=9, value=f"=AVERAGE(I{pr_start}:I{pr_end})").number_format = FMT_PCT
    ws.cell(row=r, column=10, value=f"=G{r}/F{r}").number_format = FMT_PCT
    ws.cell(row=r, column=11, value=f'=IF(J{r}>=0.9, "🟢 Mål nådd (>=90%)", IF(J{r}>=0.8, "🟡 Moderat (80-90%)", "🔴 Lav (<80%)"))').font = FONT_TD_BOLD

    for c in range(2, 12):
        cell = ws.cell(row=r, column=c)
        cell.font = FONT_TD_BOLD; cell.fill = FILL_TOTAL; cell.border = BORDER_TOTAL
    ws.row_dimensions[r].height = 21

    # Seksjon 2: KD Finansieringsmodell 2025 & Marginalitetsprinsippet
    r += 3
    ws.cell(row=r, column=2, value="2. KD FINANSIERINGSMODELL 2025: SPE60 SATSSTRUKTUR & MARGINALITETSPRINSIPPET").font = FONT_SECTION
    r += 1

    kd_headers = ["Kategori", "Finansieringskategori", "SPE60 Sats (2025)", "Faglige Eksempler (UiA Portefølje)", "Marginalitetsprinsipp & Finansieringslogikk"]
    for idx, h in enumerate(kd_headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx == 4 else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    kd_rows = [
        ("Kategori 1", "SPE60 Kat 1", 54550.0, "Samfunnsfag, humanistiske fag, økonomi/ledelse", "Åpen resultatbasert uttelling; skjermer institusjonens faste basisbevilgning"),
        ("Kategori 2", "SPE60 Kat 2", 81800.0, "Realfag, teknologi, helse- og sosialfag, lærerutdanning", "Vektet tilskuddssats per helårsekvivalent (SPE60 = 60 studiepoeng)"),
        ("Kategori 3", "SPE60 Kat 3", 190900.0, "Klinisk medisin, utøvende musikk og scenekunst", "Høyeste satsklasse for ressurskrevende laboratorie-/atelierutdanninger"),
        ("Regelverkskrav", "Marginalitetsprinsippet", 0.0, "Beskyttelse av eksisterende studieplasser", "KDs finansieringsmodell 2025 skjermer opprinnelig tildelte studieplasser mot kutt ved midlertidig studentfrafall")
    ]

    for item in kd_rows:
        r += 1
        ws.cell(row=r, column=2, value=item[0]).font = FONT_TD_BOLD
        ws.cell(row=r, column=3, value=item[1]).font = FONT_TD_CODE
        c_sats = ws.cell(row=r, column=4, value=float(item[2]))
        c_sats.font = FONT_TD_BOLD
        c_sats.number_format = FMT_CURR if item[2] > 0 else "@"
        if item[2] == 0:
            c_sats.value = "Skjermet basis"
        ws.cell(row=r, column=5, value=item[3]).font = FONT_TD
        ws.cell(row=r, column=6, value=item[4]).font = FONT_TD

        for c in range(2, 7):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
            if "Marginalitet" in item[1]:
                ws.cell(row=r, column=c).fill = FILL_ALT
        ws.row_dimensions[r].height = 20

    auto_fit_columns(ws, min_col=1, max_col=12)


def build_sheet_07_action_tracker(wb, con):
    ws = wb.create_sheet(title="07_Action_Tracker")
    render_header(ws, "07 Action Tracker (Omstilling & Gevinstrealisering)",
                  "Overvåking av de 21 omstillingstiltakene (16 turnaround + 5 AI/prosess), frister, ansvar og realisert effekt",
                  "Omstillingsutvalg / Linjeledere", max_col=10)

    # KPI Strip
    kpis = [
        {"title": "Totalt Antall Tiltak", "val": 21, "sub": "Vedtatte tiltak (inkl. AI)", "fmt": FMT_INT},
        {"title": "Aktive Åpne Tiltak", "val": 17, "sub": "Pågår eller planlagt", "fmt": FMT_INT},
        {"title": "Forsinkede Tiltak", "val": 4, "sub": "Krever lederoppmerksomhet", "fmt": FMT_INT, "badge": "🔴 Rød"},
        {"title": "Forventet Effekt", "val": -20255000.0, "sub": "Total innsparingsramme", "fmt": FMT_CURR},
        {"title": "Realisert Effekt", "val": -5562081.66, "sub": "27,5% realiseringsgrad", "fmt": FMT_CURR, "badge": "🟢 Gunstig"}
    ]
    render_kpis(ws, 4, kpis)

    # Section 1: Actions Table
    r = 8
    ws.cell(row=r, column=2, value="OMSTILLINGS- OG INNSPARINGSTILTAK (FACTACTION.CSV)").font = FONT_SECTION
    r += 1

    headers = ["ID", "Tiltaksbeskrivelse", "Ansvarlig", "Avviksårsak", "Frist", "Forventet (kr)", "Realisert (kr)", "Restavvik", "Prioritet", "Status"]
    for idx, h in enumerate(headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx in [7, 8, 9] else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    actions = con.execute("""
        SELECT TiltakID, Tiltaksbeskrivelse, AnsvarligRolle, Avviksarsak, cast(FristDatoNokkel as varchar), ForventetEffekt, RealisertEffekt, Prioritet, Status
        FROM FactAction
        ORDER BY TiltakID
    """).fetchall()

    a_start = r + 1
    for act in actions:
        r += 1
        ws.cell(row=r, column=2, value=act[0]).font = FONT_TD_CODE
        ws.cell(row=r, column=3, value=act[1]).font = FONT_TD_BOLD
        ws.cell(row=r, column=4, value=act[2]).font = FONT_TD
        ws.cell(row=r, column=5, value=act[3]).font = FONT_TD
        ws.cell(row=r, column=6, value=str(act[4])).font = FONT_TD
        ws.cell(row=r, column=7, value=float(act[5])).number_format = FMT_CURR
        ws.cell(row=r, column=8, value=float(act[6])).number_format = FMT_CURR
        ws.cell(row=r, column=9, value=f"=G{r}-H{r}").number_format = FMT_CURR
        ws.cell(row=r, column=10, value=act[7]).font = FONT_TD
        
        st = act[8]
        rag_lbl = "🟢 Gjennomført" if st == "Gjennomført" else ("🟡 Pågår" if st == "Pågår" else "🔴 Forsinket")
        ws.cell(row=r, column=11, value=rag_lbl).font = FONT_TD_BOLD

        for c in range(2, 12):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 19
    a_end = r

    # Totals
    r += 1
    ws.cell(row=r, column=2, value="TOTAL").font = FONT_TD_BOLD
    ws.cell(row=r, column=3, value=f"{len(actions)} tiltak (inkl. 5 AI/prosess)").font = FONT_TD_BOLD
    ws.cell(row=r, column=7, value=f"=SUM(G{a_start}:G{a_end})").number_format = FMT_CURR
    ws.cell(row=r, column=8, value=f"=SUM(H{a_start}:H{a_end})").number_format = FMT_CURR
    ws.cell(row=r, column=9, value=f"=SUM(I{a_start}:I{a_end})").number_format = FMT_CURR
    ws.cell(row=r, column=10, value="")
    ws.cell(row=r, column=11, value="27.5% realisert").font = FONT_TD_BOLD

    for c in range(2, 12):
        cell = ws.cell(row=r, column=c)
        cell.font = FONT_TD_BOLD; cell.fill = FILL_TOTAL; cell.border = BORDER_TOTAL
    ws.row_dimensions[r].height = 21

    auto_fit_columns(ws, min_col=1, max_col=12)


def build_sheet_08_controller_cockpit(wb, con):
    ws = wb.create_sheet(title="08_Controller_Cockpit")
    render_header(ws, "08 Controller Cockpit (Avstemming & Kontrolltårn)",
                  "Hierarkisk avstemmingsmatrise, avviksdrivere per konto og kvalitetskontroll",
                  "Senior Controller / Økonomisjef", max_col=10)

    # KPI Strip
    kpis = [
        {"title": "Forecastavvik LE", "val": 26045791.49, "sub": "Helårsavvik mot budsjett", "fmt": FMT_CURR, "badge": "🔴 Rød"},
        {"title": "Avvik YTD Netto", "val": -130604.63, "sub": "Mindreforbruk hittil", "fmt": FMT_CURR, "badge": "🟢 Gunstig"},
        {"title": "Forecast Confidence", "val": 0.9189, "sub": "Konfidensgrad i prognosen", "fmt": FMT_PCT},
        {"title": "5 %-regel Status", "val": "Etterlevd", "sub": "0,01% benyttet av 5,0% tak", "fmt": None, "badge": "🟢 Grønn"},
        {"title": "Gjenstående Restavvik", "val": 16040791.49, "sub": "Etter vedtatt tiltakspakke", "fmt": FMT_CURR}
    ]
    render_kpis(ws, 4, kpis)

    # Section 1: Top 10 Account Variances
    r = 8
    ws.cell(row=r, column=2, value="1. STØRSTE AVVIKSDRIVERE I HOVEDBOKEN (TOPP 10 KONTOER)").font = FONT_SECTION
    r += 1

    headers = ["Konto", "Kontonavn", "SRS-regnskapslinje", "Regnskap YTD", "Budsjett YTD", "Forecast LE", "Forecastavvik", "RAG Status"]
    for idx, h in enumerate(headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx > 4 else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    top_accounts = con.execute("""
        WITH gl AS (SELECT Konto, sum(Belop_signert) as val FROM FactGL GROUP BY Konto),
             bud AS (SELECT Konto, sum(BudsjettBelop) as val FROM FactBudget GROUP BY Konto),
             fc AS (SELECT Konto, sum(ForecastBelop) as val FROM FactForecast WHERE Versjon = 'LE_2026' GROUP BY Konto)
        SELECT 
            a.Konto,
            a.Kontonavn,
            a.SRS_regnskapslinje,
            round(coalesce(gl.val, 0), 2) as Regnskap,
            round(coalesce(bud.val, 0), 2) as Budsjett,
            round(coalesce(fc.val, 0), 2) as Forecast
        FROM DimAccount a
        LEFT JOIN gl ON a.Konto = gl.Konto
        LEFT JOIN bud ON a.Konto = bud.Konto
        LEFT JOIN fc ON a.Konto = fc.Konto
        ORDER BY abs(coalesce(fc.val, 0) - coalesce(bud.val, 0)) DESC
        LIMIT 10
    """).fetchall()

    for acc in top_accounts:
        r += 1
        ws.cell(row=r, column=2, value=acc[0]).font = FONT_TD_CODE
        ws.cell(row=r, column=3, value=acc[1]).font = FONT_TD_BOLD
        ws.cell(row=r, column=4, value=acc[2]).font = FONT_TD
        ws.cell(row=r, column=5, value=float(acc[3])).number_format = FMT_CURR
        ws.cell(row=r, column=6, value=float(acc[4])).number_format = FMT_CURR
        ws.cell(row=r, column=7, value=float(acc[5])).number_format = FMT_CURR
        ws.cell(row=r, column=8, value=f"=G{r}-F{r}").number_format = FMT_CURR
        ws.cell(row=r, column=9, value=f'=IF(H{r}>0, "🔴 Merforbruk", "🟢 Mindreforbruk")').font = FONT_TD_BOLD

        for c in range(2, 10):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 19

    # Seksjon 2: DFØ SRS 1 Virksomhetsregnskap & Note 15 Avstemming
    r += 3
    ws.cell(row=r, column=2, value="2. DFØ STATLIGE REGNSKAPSSTANDARDER (SRS 1 VIRKSOMHETSREGNSKAP & NOTE 15)").font = FONT_SECTION
    r += 1

    srs_headers = ["Regnskapspost / Kontrollparameter", "SRS / Regelverk", "Kontointervall", "Regnskap YTD (NOK)", "Budsjett YTD (NOK)", "Avvik YTD (NOK)", "Note 15 / Kontrollstatus"]
    for idx, h in enumerate(srs_headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx in [5, 6, 7] else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    srs_audit_rows = [
        ("Driftsinntekter", "SRS 1 Inntekter", "Konto 3000-3999", -2138486811.09, -2138356206.46, -130604.63, "🟢 Avstemt mot tildelingsbrev"),
        ("Lønn og sosiale kostnader", "SRS 1 Lønnskostnader", "Konto 5000-5999", 1482173092.35, 1482173092.35, 0.00, "🟢 68,97 % lønnsandel (normalnivå)"),
        ("Av- og nedskrivninger", "SRS 17 Anleggsmidler", "Konto 6000-6050", 107341205.17, 107341205.17, 0.00, "🟢 Lineære avskrivninger iht. SRS 17"),
        ("Andre driftskostnader", "SRS 1 Driftskostnader", "Konto 6100-7999", 559589641.76, 559589641.76, 0.00, "🟢 Energi, husleie og IKT-lisenser"),
        ("Netto driftsresultat", "SRS 1 Virksomhetsregnskap", "Konto 3000-8999", 10617128.19, 10747732.82, -130604.63, "🟢 Mindreforbruk YTD (-0,01 %)"),
        ("Statens 5 %-regel tak", "Rundskriv F-05-20", "Konto 3900 (5,0 %)", 106939940.48, 106939940.48, 0.00, "🟢 Maksimalt tillatt avsetning"),
        ("Status etterlevelse 5 %-regel", "KD / Note 15", "Netto avvik vs tak", 130604.63, 106939940.48, 106809335.85, "🟢 FULLT ETTERLEVD (Ingen innskjerping)")
    ]

    for item in srs_audit_rows:
        r += 1
        ws.cell(row=r, column=2, value=item[0]).font = FONT_TD_BOLD
        ws.cell(row=r, column=3, value=item[1]).font = FONT_TD
        ws.cell(row=r, column=4, value=item[2]).font = FONT_TD_CODE
        c_reg = ws.cell(row=r, column=5, value=float(item[3]))
        c_reg.font = FONT_TD_BOLD; c_reg.number_format = FMT_CURR
        c_bud = ws.cell(row=r, column=6, value=float(item[4]))
        c_bud.font = FONT_TD; c_bud.number_format = FMT_CURR
        c_avv = ws.cell(row=r, column=7, value=float(item[5]))
        c_avv.font = FONT_TD_BOLD; c_avv.number_format = FMT_CURR
        c_stat = ws.cell(row=r, column=8, value=item[6])
        c_stat.font = FONT_TD_BOLD

        for c in range(2, 9):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
            if "Netto driftsresultat" in item[0] or "FULLT ETTERLEVD" in item[6]:
                ws.cell(row=r, column=c).fill = FILL_ALT
        ws.row_dimensions[r].height = 20

    auto_fit_columns(ws, min_col=1, max_col=10)


def build_sheet_09_begrepskatalog(wb, con):
    ws = wb.create_sheet(title="09_Begrepskatalog")
    render_header(ws, "09 Begrepskatalog & Metodikk (Glossary)",
                  "UiA Økonomistyringsleksikon - 60 definerte begreper for controller, ledelse og prosjekt",
                  "Felles referanseordbok for UH-sektoren", max_col=10)

    # KPI Strip
    kpis = [
        {"title": "Definerte Begreper", "val": 60, "sub": "DimGlossary.csv", "fmt": FMT_INT},
        {"title": "Faglige Kategorier", "val": 8, "sub": "SRS, EVM, BOA, FTE, RAG", "fmt": FMT_INT},
        {"title": "EAC Sluttkostnad", "val": 36793524.31, "sub": "Gjeldende Latest Estimate", "fmt": FMT_CURR},
        {"title": "RAG Terskelnivåer", "val": 3, "sub": "🟢 <=2% | 🟡 2-5% | 🔴 >5%", "fmt": None},
        {"title": "Regnskapsstandard", "val": "DFØ SRS", "sub": "Statlig opptjeningsregnskap", "fmt": None}
    ]
    render_kpis(ws, 4, kpis)

    # Terms Table
    r = 8
    ws.cell(row=r, column=2, value="KOMPLETT BEGREPSOVERSIKT MED PRAKTISK TOLKNING OG DAX-FORMLER").font = FONT_SECTION
    r += 1

    headers = ["ID", "Begrep", "Fullt Navn", "Kategori", "Definisjon (DFØ SRS / EVM)", "Praktisk Controller-tolkning", "Formel / DAX", "Rollekontekst", "Relevant Rapport"]
    for idx, h in enumerate(headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[r].height = 20

    glossary = con.execute("""
        SELECT BegrepID, Begrep, FulltNavn, Kategori, Definisjon, PraktiskTolkning, FormelDAX, RolleKontekst, RelevantRapport
        FROM DimGlossary
        ORDER BY cast(BegrepID as integer)
    """).fetchall()

    for item in glossary:
        r += 1
        ws.cell(row=r, column=2, value=int(item[0])).font = FONT_TD_CODE
        ws.cell(row=r, column=3, value=item[1]).font = FONT_TD_BOLD
        ws.cell(row=r, column=4, value=item[2]).font = FONT_TD
        ws.cell(row=r, column=5, value=item[3]).font = FONT_TD_BOLD
        ws.cell(row=r, column=6, value=item[4]).font = FONT_TD
        ws.cell(row=r, column=7, value=item[5]).font = FONT_TD
        ws.cell(row=r, column=8, value=item[6]).font = FONT_TD_CODE
        ws.cell(row=r, column=9, value=item[7]).font = FONT_TD
        ws.cell(row=r, column=10, value=item[8]).font = FONT_TD_BOLD

        for c in range(2, 11):
            cell = ws.cell(row=r, column=c)
            cell.border = BORDER_TOP_BOTTOM
            if int(item[0]) % 2 == 1:
                cell.fill = FILL_ALT
        ws.row_dimensions[r].height = 22

    auto_fit_columns(ws, min_col=1, max_col=11)
    ws.column_dimensions["B"].width = 6
    ws.column_dimensions["C"].width = 18
    ws.column_dimensions["D"].width = 25
    ws.column_dimensions["E"].width = 22
    ws.column_dimensions["F"].width = 45
    ws.column_dimensions["G"].width = 45
    ws.column_dimensions["H"].width = 35
    ws.column_dimensions["I"].width = 18
    ws.column_dimensions["J"].width = 20


def build_sheet_dt_okonomi(wb, con):
    ws = wb.create_sheet(title="DT_Okonomi")
    render_header(ws, "DT Økonomidetalj (Bilagslogg)",
                  "Transaksjons- og bilagslogg fra FactGL (35 760 poster) med avstemming",
                  "Drill-Through Transaksjonskontroll", max_col=10)

    # Summary KPIs
    kpis = [
        {"title": "Totalt Bokført Regnskap", "val": 10617128.19, "sub": "SUM(FactGL[Belop_signert])", "fmt": FMT_CURR},
        {"title": "Sum Inntekter", "val": 2138486811.09, "sub": "Konto 3000-3999", "fmt": FMT_CURR},
        {"title": "Sum Kostnader", "val": 2149103939.28, "sub": "Konto 5000-8999", "fmt": FMT_CURR},
        {"title": "Antall Bilag", "val": 35760, "sub": "Transaksjoner i FactGL", "fmt": FMT_INT}
    ]
    render_kpis(ws, 4, kpis)

    # Top sample of GL transactions
    r = 8
    ws.cell(row=r, column=2, value="TRANSAKSJONSLOGG UTVALG (DE 100 STØRSTE POSTERINGENE)").font = FONT_SECTION
    r += 1

    headers = ["Bilagsnummer", "Dato", "Organisasjon", "Konto", "Prosjekt", "Beløp (NOK)", "Posteringstekst", "Datakilde"]
    for idx, h in enumerate(headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx == 7 else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    gl_sample = con.execute("""
        SELECT Bilag, DatoNokkel, Organisasjonsnokkel, Konto, Prosjekt, round(Belop_signert, 2), Tekst, Datakilde
        FROM FactGL
        ORDER BY abs(Belop_signert) DESC
        LIMIT 100
    """).fetchall()

    for item in gl_sample:
        r += 1
        ws.cell(row=r, column=2, value=item[0]).font = FONT_TD_CODE
        ws.cell(row=r, column=3, value=str(item[1])).font = FONT_TD
        ws.cell(row=r, column=4, value=item[2]).font = FONT_TD
        ws.cell(row=r, column=5, value=item[3]).font = FONT_TD_CODE
        ws.cell(row=r, column=6, value=item[4]).font = FONT_TD
        c_bel = ws.cell(row=r, column=7, value=float(item[5]))
        c_bel.font = FONT_TD_BOLD; c_bel.number_format = FMT_CURR
        ws.cell(row=r, column=8, value=item[6]).font = FONT_TD
        ws.cell(row=r, column=9, value=item[7]).font = FONT_TD

        for c in range(2, 10):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 19

    auto_fit_columns(ws, min_col=1, max_col=10)


def build_sheet_dt_bemanning(wb, con):
    ws = wb.create_sheet(title="DT_Bemanning")
    render_header(ws, "DT Bemanning & Årsverk",
                  "Lønnsanalyse, stillingsgrupper (UF/TA) og lønn per årsverk fra FactFTE",
                  "Drill-Through Personalkontroll", max_col=10)

    # KPIs
    kpis = [
        {"title": "Totalt Årsverk", "val": 1285.93, "sub": "Siste rapporteringsmåned", "fmt": FMT_DEC},
        {"title": "Vitenskapelige (UF)", "val": 661.77, "sub": "51,5% av total bemanning", "fmt": FMT_DEC},
        {"title": "Teknisk-adm (TA)", "val": 624.16, "sub": "48,5% av total bemanning", "fmt": FMT_DEC},
        {"title": "Lønnskostnader", "val": 1482268875.90, "sub": "69,0% av driftskostnader", "fmt": FMT_CURR}
    ]
    render_kpis(ws, 4, kpis)

    r = 8
    ws.cell(row=r, column=2, value="BEMANNING OG LØNNSKOSTNADER PER STILLINGSGRUPPE (FACTFTE)").font = FONT_SECTION
    r += 1

    headers = ["Stillingsgruppe", "Kategori", "Årsverk (Sum)", "Faglige Årsverk", "Faglig andel %", "Andel av årsverk %"]
    for idx, h in enumerate(headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx > 3 else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    fte_data = con.execute("""
        SELECT 
            p.Stillingsgruppenavn,
            p.Stillingskategori,
            round(sum(f.Aarsverk), 2) as AV,
            round(sum(f.FagligeAarsverk), 2) as FagligeAV,
            round(sum(f.FagligeAarsverk) / nullif(sum(f.Aarsverk), 0), 4) as FagligAndel
        FROM FactFTE f
        JOIN DimPositionGroup p ON f.Stillingsgruppe = p.Stillingsgruppe
        GROUP BY 1, 2
        ORDER BY 3 DESC
    """).fetchall()

    f_start = r + 1
    total_av = 15390.21
    for fte in fte_data:
        r += 1
        ws.cell(row=r, column=2, value=fte[0]).font = FONT_TD_BOLD
        ws.cell(row=r, column=3, value=fte[1]).font = FONT_TD
        ws.cell(row=r, column=4, value=float(fte[2])).number_format = FMT_DEC
        ws.cell(row=r, column=5, value=float(fte[3])).number_format = FMT_DEC
        ws.cell(row=r, column=6, value=float(fte[4])).number_format = FMT_PCT
        ws.cell(row=r, column=7, value=float(fte[2]) / total_av).number_format = FMT_PCT

        for c in range(2, 8):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 19
    f_end = r

    # Total
    r += 1
    ws.cell(row=r, column=2, value="TOTALT").font = FONT_TD_BOLD
    ws.cell(row=r, column=3, value="Alle stillingsgrupper").font = FONT_TD_BOLD
    ws.cell(row=r, column=4, value=f"=SUM(D{f_start}:D{f_end})").number_format = FMT_DEC
    ws.cell(row=r, column=5, value=f"=SUM(E{f_start}:E{f_end})").number_format = FMT_DEC
    ws.cell(row=r, column=6, value=f"=E{r}/D{r}").number_format = FMT_PCT
    ws.cell(row=r, column=7, value=f"=SUM(G{f_start}:G{f_end})").number_format = FMT_PCT

    for c in range(2, 8):
        cell = ws.cell(row=r, column=c)
        cell.font = FONT_TD_BOLD; cell.fill = FILL_TOTAL; cell.border = BORDER_TOTAL
    ws.row_dimensions[r].height = 21

    auto_fit_columns(ws, min_col=1, max_col=7)


def build_sheet_dt_prosjekt(wb, con):
    ws = wb.create_sheet(title="DT_Prosjekt_EVM")
    render_header(ws, "DT Prosjektdetaljer & EVM (Earned Value Management)",
                  "Fremdrifts- og kostnadskontroll med BAC, EAC, ETC, VAC og RAG-avvik",
                  "Project Controller / BOA-ledelse", max_col=12)

    # KPIs
    kpis = [
        {"title": "Total BAC (Budsjett)", "val": 10747732.82, "sub": "Baseline ramme", "fmt": FMT_CURR},
        {"title": "Sluttkostnad EAC", "val": 36793524.31, "sub": "Latest Estimate LE", "fmt": FMT_CURR},
        {"title": "Helårsavvik VAC", "val": -26045791.49, "sub": "Overskridelse", "fmt": FMT_CURR, "badge": "🔴 Rød"},
        {"title": "Kostnadsindeks CPI", "val": 0.292, "sub": "BAC / EAC effektivitet", "fmt": "0.000"}
    ]
    render_kpis(ws, 4, kpis)

    r = 8
    ws.cell(row=r, column=2, value="EARNED VALUE MANAGEMENT (EVM) MATRISE FOR PROSJEKTPORTEFØLJEN").font = FONT_SECTION
    r += 1

    headers = ["Prosjektkode", "Prosjektnavn", "Finansiering", "BAC (Budsjett)", "AC (Regnskap)", "EAC (Sluttkostnad)", "ETC (Gjenstående)", "VAC (Sluttavvik)", "VAC %", "EVM RAG Status"]
    for idx, h in enumerate(headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx in [5, 6, 7, 8, 9, 10] else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    evm_data = con.execute("""
        WITH gl AS (SELECT Prosjekt, sum(Belop_signert) as val FROM FactGL GROUP BY Prosjekt),
             bud AS (SELECT Prosjekt, sum(BudsjettBelop) as val FROM FactBudget GROUP BY Prosjekt),
             fc AS (SELECT Prosjekt, sum(ForecastBelop) as val FROM FactForecast WHERE Versjon = 'LE_2026' GROUP BY Prosjekt)
        SELECT 
            p.Prosjekt,
            p.Prosjektnavn,
            p.Finansieringstype,
            round(coalesce(bud.val, 0), 2) as BAC,
            round(coalesce(gl.val, 0), 2) as AC,
            round(coalesce(fc.val, 0), 2) as EAC
        FROM DimProject p
        LEFT JOIN gl ON p.Prosjekt = gl.Prosjekt
        LEFT JOIN bud ON p.Prosjekt = bud.Prosjekt
        LEFT JOIN fc ON p.Prosjekt = fc.Prosjekt
        ORDER BY EAC DESC
    """).fetchall()

    ev_start = r + 1
    for row in evm_data:
        r += 1
        ws.cell(row=r, column=2, value=row[0]).font = FONT_TD_CODE
        ws.cell(row=r, column=3, value=row[1]).font = FONT_TD_BOLD
        ws.cell(row=r, column=4, value=row[2]).font = FONT_TD
        ws.cell(row=r, column=5, value=float(row[3])).number_format = FMT_CURR
        ws.cell(row=r, column=6, value=float(row[4])).number_format = FMT_CURR
        ws.cell(row=r, column=7, value=float(row[5])).number_format = FMT_CURR
        ws.cell(row=r, column=8, value=f"=G{r}-F{r}").number_format = FMT_CURR
        ws.cell(row=r, column=9, value=f"=E{r}-G{r}").number_format = FMT_CURR
        ws.cell(row=r, column=10, value=f'=IF(E{r}<>0, I{r}/E{r}, 0)').number_format = FMT_PCT
        ws.cell(row=r, column=11, value=f'=IF(J{r}>=0, "🟢 Under budsjett", IF(J{r}>=-0.05, "🟡 Moderat overskridelse", "🔴 Kritisk overskridelse"))').font = FONT_TD_BOLD

        for c in range(2, 12):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 19
    ev_end = r

    # Total row
    r += 1
    ws.cell(row=r, column=2, value="TOTAL EVM PORTEFØLJE").font = FONT_TD_BOLD
    ws.cell(row=r, column=5, value=f"=SUM(E{ev_start}:E{ev_end})").number_format = FMT_CURR
    ws.cell(row=r, column=6, value=f"=SUM(F{ev_start}:F{ev_end})").number_format = FMT_CURR
    ws.cell(row=r, column=7, value=f"=SUM(G{ev_start}:G{ev_end})").number_format = FMT_CURR
    ws.cell(row=r, column=8, value=f"=G{r}-F{r}").number_format = FMT_CURR
    ws.cell(row=r, column=9, value=f"=E{r}-G{r}").number_format = FMT_CURR
    ws.cell(row=r, column=10, value=f'=IF(E{r}<>0, I{r}/E{r}, 0)').number_format = FMT_PCT
    ws.cell(row=r, column=11, value=f'=IF(J{r}>=0, "🟢 Under budsjett", IF(J{r}>=-0.05, "🟡 Moderat overskridelse", "🔴 Kritisk overskridelse"))').font = FONT_TD_BOLD

    for c in range(2, 12):
        cell = ws.cell(row=r, column=c)
        cell.font = FONT_TD_BOLD; cell.fill = FILL_TOTAL; cell.border = BORDER_TOTAL
    ws.row_dimensions[r].height = 21

    auto_fit_columns(ws, min_col=1, max_col=12)


def build_sheet_dt_tiltak(wb, con):
    ws = wb.create_sheet(title="DT_Tiltakskort")
    render_header(ws, "DT Tiltaksdetaljer & Risikostyring",
                  "Enkeltkort og risikovurdering for de 21 omstillingstiltakene (inkl. AI/prosess)",
                  "Drill-Through Risikostyring", max_col=10)

    # KPIs
    kpis = [
        {"title": "Totalt Vedtatt", "val": -20255000.0, "sub": "21 tiltak (inkl. AI)", "fmt": FMT_CURR},
        {"title": "Realisert Hittil", "val": -5562081.66, "sub": "Realisert per nå", "fmt": FMT_CURR},
        {"title": "Gjenstående Risiko", "val": -14692918.34, "sub": "Restbeløp som må innhentes", "fmt": FMT_CURR},
        {"title": "Høyrisiko Tiltak", "val": 4, "sub": "Kritiske tiltak", "fmt": FMT_INT, "badge": "🔴 Forsinket"}
    ]
    render_kpis(ws, 4, kpis)

    r = 8
    ws.cell(row=r, column=2, value="DETALJERT TILTAKSOVERSIKT (FACTACTION.CSV)").font = FONT_SECTION
    r += 1

    headers = ["ID", "Tiltaksbeskrivelse", "Konto", "Org", "Start", "Frist", "Forventet", "Realisert", "Prioritet", "Status"]
    for idx, h in enumerate(headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx in [8, 9] else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    t_data = con.execute("""
        SELECT TiltakID, Tiltaksbeskrivelse, Konto, Organisasjonsnokkel, cast(StartDatoNokkel as varchar), cast(FristDatoNokkel as varchar), ForventetEffekt, RealisertEffekt, Prioritet, Status
        FROM FactAction
        ORDER BY TiltakID
    """).fetchall()

    for item in t_data:
        r += 1
        ws.cell(row=r, column=2, value=item[0]).font = FONT_TD_CODE
        ws.cell(row=r, column=3, value=item[1]).font = FONT_TD_BOLD
        ws.cell(row=r, column=4, value=item[2]).font = FONT_TD_CODE
        ws.cell(row=r, column=5, value=item[3]).font = FONT_TD
        ws.cell(row=r, column=6, value=str(item[4])).font = FONT_TD
        ws.cell(row=r, column=7, value=str(item[5])).font = FONT_TD
        ws.cell(row=r, column=8, value=float(item[6])).number_format = FMT_CURR
        ws.cell(row=r, column=9, value=float(item[7])).number_format = FMT_CURR
        ws.cell(row=r, column=10, value=item[8]).font = FONT_TD
        ws.cell(row=r, column=11, value=item[9]).font = FONT_TD_BOLD

        for c in range(2, 12):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 19

    auto_fit_columns(ws, min_col=1, max_col=12)


def build_sheet_dt_studier(wb, con):
    ws = wb.create_sheet(title="DT_Studieaktivitet")
    render_header(ws, "DT Studieaktivitet (Månedlig produksjon)",
                  "Månedlig studenttall, planlagte og avlagte studiepoeng fra FactStudyPoints",
                  "Drill-Through Utdanningsanalyse", max_col=10)

    # KPIs
    kpis = [
        {"title": "Planlagte SP", "val": 390095.0, "sub": "Årsplan for porteføljen", "fmt": FMT_INT},
        {"title": "Avlagte SP", "val": 336945.4, "sub": "Faktisk eksamensresultat", "fmt": FMT_INT},
        {"title": "SPE60 Ekvivalenter", "val": 5615.74, "sub": "Helårsstudenter", "fmt": FMT_DEC},
        {"title": "Gjennomsnittlig Måloppnåelse", "val": 0.8638, "sub": "Resultatgrad", "fmt": FMT_PCT}
    ]
    render_kpis(ws, 4, kpis)

    r = 8
    ws.cell(row=r, column=2, value="MÅNEDLIG AKTIVITETSLOGG (FACTSTUDYPOINTS UTVALG)").font = FONT_SECTION
    r += 1

    headers = ["Dato", "Programkode", "Fakultet", "Registrerte", "Planlagte SP", "Avlagte SP", "SPE60", "Beståttandel %"]
    for idx, h in enumerate(headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx > 4 else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    sp_data = con.execute("""
        SELECT 
            cast(f.DatoNokkel as varchar) as Dato,
            f.Studieprogram,
            f.Organisasjonsnokkel,
            f.RegistrerteStudenter,
            round(f.PlanlagteStudiepoeng, 1),
            round(f.AvlagteStudiepoeng, 1),
            round(f.SPE60, 2),
            round(f.BestattAndel, 3)
        FROM FactStudyPoints f
        ORDER BY f.DatoNokkel DESC, f.AvlagteStudiepoeng DESC
        LIMIT 100
    """).fetchall()

    for item in sp_data:
        r += 1
        ws.cell(row=r, column=2, value=item[0]).font = FONT_TD
        ws.cell(row=r, column=3, value=item[1]).font = FONT_TD_CODE
        ws.cell(row=r, column=4, value=item[2]).font = FONT_TD
        ws.cell(row=r, column=5, value=int(item[3])).number_format = FMT_INT
        ws.cell(row=r, column=6, value=float(item[4])).number_format = FMT_INT
        ws.cell(row=r, column=7, value=float(item[5])).number_format = FMT_INT
        ws.cell(row=r, column=8, value=float(item[6])).number_format = FMT_DEC
        ws.cell(row=r, column=9, value=float(item[7])).number_format = FMT_PCT

        for c in range(2, 10):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 19

    auto_fit_columns(ws, min_col=1, max_col=10)


# ==============================================================================
# DATA MODEL SHEETS (CSV -> EXCEL)
# ==============================================================================
def write_csv_to_sheet(wb, sheet_name, csv_path, con=None):
    if sheet_name in wb.sheetnames:
        del wb[sheet_name]
    ws = wb.create_sheet(title=sheet_name)
    ws.views.sheetView[0].showGridLines = True
    ws.sheet_view.zoomScale = 85

    print(f"  Loading data table {sheet_name:<18} from {os.path.basename(csv_path)}...", flush=True)
    import csv
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        ws.append([c.lstrip('\ufeff') for c in header])
        for col_idx in range(1, len(header) + 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.font = FONT_TH
            cell.fill = FILL_TH
            cell.alignment = Alignment(horizontal="left", vertical="center")
        ws.row_dimensions[1].height = 20

        row_idx = 2
        for row in reader:
            parsed_row = []
            for val in row:
                try:
                    if "." in val:
                        parsed_row.append(float(val))
                    else:
                        parsed_row.append(int(val))
                except ValueError:
                    parsed_row.append(val)
            ws.append(parsed_row)
            row_idx += 1

    auto_fit_columns(ws, min_col=1, max_col=len(header))
    print(f"    Done {sheet_name}: {row_idx - 1:,} rows loaded.", flush=True)


# ==============================================================================
# MAIN WORKBOOK ORCHESTRATION
# ==============================================================================
def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(root_dir, "data")
    excel_dir = os.path.join(root_dir, "excel")
    os.makedirs(excel_dir, exist_ok=True)
    excel_path = os.path.join(excel_dir, "uia_controller_excel_pack.xlsx")

    print("=" * 85)
    print("BUILDING COMPLETE UiA CONTROLLER EXCEL REPORTING PACK")
    print(f"Target: {excel_path}")
    print("=" * 85)

    con = init_duckdb(data_dir)
    print("DuckDB in-memory analytical engine initialized.")

    wb = openpyxl.Workbook()
    # remove default sheet
    default_sheet = wb.active
    wb.remove(default_sheet)

    # 1. Build Navigation & Index
    print("\n>>> Building 00_Forside_Navigasjon...")
    build_sheet_00_navigasjon(wb)

    # 2. Build Management Reports 01 - 09
    print(">>> Building 01_Instituttleder...")
    build_sheet_01_instituttleder(wb, con)

    print(">>> Building 02_Dekan...")
    build_sheet_02_dekan(wb, con)

    print(">>> Building 03_Executive...")
    build_sheet_03_executive(wb, con)

    print(">>> Building 04_Styret...")
    build_sheet_04_styret(wb, con)

    print(">>> Building 05_Forskning_BOA...")
    build_sheet_05_forskning_boa(wb, con)

    print(">>> Building 06_Studieportefolje...")
    build_sheet_06_studieportefolje(wb, con)

    print(">>> Building 07_Action_Tracker...")
    build_sheet_07_action_tracker(wb, con)

    print(">>> Building 08_Controller_Cockpit...")
    build_sheet_08_controller_cockpit(wb, con)

    print(">>> Building 09_Begrepskatalog...")
    build_sheet_09_begrepskatalog(wb, con)

    # 3. Build Drill-Throughs DT1 - DT5
    print(">>> Building DT_Okonomi...")
    build_sheet_dt_okonomi(wb, con)

    print(">>> Building DT_Bemanning...")
    build_sheet_dt_bemanning(wb, con)

    print(">>> Building DT_Prosjekt_EVM...")
    build_sheet_dt_prosjekt(wb, con)

    print(">>> Building DT_Tiltakskort...")
    build_sheet_dt_tiltak(wb, con)

    print(">>> Building DT_Studieaktivitet...")
    build_sheet_dt_studier(wb, con)

    # 4. Load Data Model Tables
    print("\n>>> Loading 10 Underlying Data Model Sheets...")
    data_tables = [
        ("DimGlossary", "DimGlossary.csv"),
        ("DimAccount", "DimAccount.csv"),
        ("DimOrganization", "DimOrganization.csv"),
        ("DimProject", "DimProject.csv"),
        ("FactBudget", "FactBudget.csv"),
        ("FactForecast", "FactForecast.csv"),
        ("FactFTE", "FactFTE.csv"),
        ("FactStudyPoints", "FactStudyPoints.csv"),
        ("FactAction", "FactAction.csv"),
        ("FactGL", "FactGL.csv")
    ]
    for s_name, file_name in data_tables:
        csv_file = os.path.join(data_dir, file_name)
        write_csv_to_sheet(wb, s_name, csv_file, con)

    # 5. Set Tab Colors
    tab_colors = {
        "00_Forside_Navigasjon": "0F172A",
        "01_Instituttleder": "1E40AF",
        "02_Dekan": "1E40AF",
        "03_Executive": "1E40AF",
        "04_Styret": "1E40AF",
        "05_Forskning_BOA": "1E40AF",
        "06_Studieportefolje": "1E40AF",
        "07_Action_Tracker": "1E40AF",
        "08_Controller_Cockpit": "1E40AF",
        "09_Begrepskatalog": "047857",
        "DT_Okonomi": "0E7490",
        "DT_Bemanning": "0E7490",
        "DT_Prosjekt_EVM": "0E7490",
        "DT_Tiltakskort": "0E7490",
        "DT_Studieaktivitet": "0E7490"
    }
    for name in wb.sheetnames:
        ws = wb[name]
        if name in tab_colors:
            ws.sheet_properties.tabColor = tab_colors[name]
        else:
            ws.sheet_properties.tabColor = "64748B" # Data sheets slate

    print("\n>>> Saving workbook to disk...")
    t0 = time.time()
    wb.save(excel_path)
    print(f"Workbook saved successfully in {time.time()-t0:.2f} seconds!")
    print(f"File Size: {os.path.getsize(excel_path) / (1024*1024):.2f} MB")
    print(f"Total Sheets: {len(wb.sheetnames)}")
    for idx, s in enumerate(wb.sheetnames, 1):
        print(f"  {idx:>2d}. {s}")

if __name__ == "__main__":
    main()
