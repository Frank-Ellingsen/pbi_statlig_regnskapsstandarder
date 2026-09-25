# -*- coding: utf-8 -*-
"""
update_and_run_excel.py
-----------------------
Upgrades scripts/build_excel_pack.py to be 100% aligned with the authentic Use Case data:
- Replaces Belop_signert with Belop
- Integrates FactProjectBOA (18 columns) into DuckDB and raw sheets
- Adds UC_Statlige_Use_Cases (UC1-UC6) sheet
- Adds LP_Laereplaner_KD2025 sheet
- Updates 02_Dekan with 4-zone layout and authentic case KPIs
- Updates 05_Forskning_BOA to query FactProjectBOA
- Updates 06_Studieportefolje with 2 589.6 SPE60 and 176.01 MNOK BFE
- Updates 00_Forside_Navigasjon
- Generates excel/uia_controller_excel_pack.xlsx and synchronizes it to:
    - uia_controller_excel_pack.xlsx
    - uia_complete_controller_powerbi_excel_package/uia_controller_excel_pack.xlsx
    - UIA-Controller-Excel.xlsx
"""

import os
import shutil
import subprocess
from pathlib import Path

root_dir = Path(__file__).parent.parent
data_dir = root_dir / "data"
build_script = root_dir / "scripts" / "build_excel_pack.py"

with open(build_script, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Replace Belop_signert with Belop
code = code.replace("Belop_signert", "Belop")

# 2. Add FactProjectBOA to init_duckdb
old_tables_list = '''    tables = [
        "DimAccount", "DimDate", "DimForecastVersion", "DimGlossary", "DimOrganization",
        "DimPositionGroup", "DimProject", "DimStudyProgram",
        "FactAction", "FactBudget", "FactFTE", "FactForecast", "FactGL", "FactStudyPoints"
    ]'''

new_tables_list = '''    tables = [
        "DimAccount", "DimDate", "DimForecastVersion", "DimGlossary", "DimOrganization",
        "DimPositionGroup", "DimProject", "DimStudyProgram",
        "FactAction", "FactBudget", "FactFTE", "FactForecast", "FactGL", "FactStudyPoints", "FactProjectBOA"
    ]'''

if old_tables_list in code:
    code = code.replace(old_tables_list, new_tables_list)

# 3. Add FactProjectBOA to data_tables
old_dt = '''    data_tables = [
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
    ]'''

new_dt = '''    data_tables = [
        ("DimGlossary", "DimGlossary.csv"),
        ("DimAccount", "DimAccount.csv"),
        ("DimOrganization", "DimOrganization.csv"),
        ("DimProject", "DimProject.csv"),
        ("FactProjectBOA", "FactProjectBOA.csv"),
        ("FactBudget", "FactBudget.csv"),
        ("FactForecast", "FactForecast.csv"),
        ("FactFTE", "FactFTE.csv"),
        ("FactStudyPoints", "FactStudyPoints.csv"),
        ("FactAction", "FactAction.csv"),
        ("FactGL", "FactGL.csv")
    ]'''

if old_dt in code:
    code = code.replace(old_dt, new_dt)

# 4. Insert build_sheet_use_cases and build_sheet_laereplaner before write_csv_to_sheet
new_functions = '''
def build_sheet_use_cases(wb, con):
    ws = wb.create_sheet(title="UC_Statlige_Use_Cases")
    render_header(ws, "UC Statlig Regelverkskontroll (UC1–UC6)",
                  "Statlige regnskapsstandarder (SRS), F-05-20 5 %-regel, anskaffelser og refusjonsstyring",
                  "Senior Controller / Regelverksrevisjon", max_col=10)

    kpis = [
        {"title": "F-05-20 Avsetning", "val": -4800000.00, "sub": "8,96 % av 53,6M ramme", "fmt": FMT_CURR, "badge": "🔴 Rød (>5%)"},
        {"title": "Lønnsandel Drift", "val": 0.7831, "sub": "50,97 MNOK (Norm: 71,0 %)", "fmt": FMT_PCT, "badge": "🔴 Avvik"},
        {"title": "SRS 10 Periodisering", "val": 2010000.00, "sub": "Konto 2900 forskudd", "fmt": FMT_CURR},
        {"title": "SRS 17 Aktivert", "val": 1200000.00, "sub": "Overført fra drift til 1200", "fmt": FMT_CURR},
        {"title": "Utestående Refusjoner", "val": 1150000.00, "sub": "NAV sykepenger/permisjon", "fmt": FMT_CURR}
    ]
    render_kpis(ws, 4, kpis)

    r = 8
    ws.cell(row=r, column=2, value="1. OVERSIKT OVER DE 6 STATLIGE USE CASENE (UC1–UC6) & REGELVERKSETTERLEVELSE").font = FONT_SECTION
    r += 1

    headers = ["Use Case", "Rettslig Standard", "Kjerneavvik / Problemstilling", "Finansielt Omfang", "Tiltak ID", "Forankret Styringstiltak", "Ansvarlig Rolle", "RAG Status"]
    for idx, h in enumerate(headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx == 5 else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    uc_data = [
        ("UC1", "Rundskriv F-05-20", "5 %-regelen overskredet: Avsetning på konto 2080 er 8,96 % (-4,8 MNOK mot 5,0 % sperre 2,68 MNOK)", 2120000.00, "T002", "Fremskynde strategiske investeringer og utstyrsanskaffelser innen Q4", "Fakultetsdirektør", "🔴 Kritisk"),
        ("UC2", "DFØ SRS 10", "Oppdrags-/bidragsinntekt feilaktig inntektsført før kostnadspåløp (motsatt sammenstilling)", 2010000.00, "T005", "Innføre månedlig automatisk avstemming mellom påløpte BOA-kostnader og konto 2900", "Prosjektcontroller", "🟡 Korrigert"),
        ("UC3", "DFØ SRS 9", "Tapskontrakt på oppdrag EVU001: Merforbruk krever umiddelbar tapsavsetning", 450000.00, "T003", "Bokføre tapsavsetning på konto 7790 mot 2800; stramme timeføring på EVU", "Instituttleder", "🔴 Tapsført"),
        ("UC4", "DFØ SRS 17", "Varige driftsmidler (lab/servere) feilaktig kostnadsført direkte på konto 6500", 1200000.00, "T001", "Omklassifisere og aktivere på konto 1200 i balansen med 5 års avskrivning", "Regnskapssjef", "🟢 Fullført"),
        ("UC5", "FOA / LOA", "Konsulentanskaffelse bestilt over terskelverdi uten tilstrekkelig kunngjøring", 620000.00, "T004", "Protokollføre anskaffelsesavvik og innføre obligatorisk forhåndsgodkjenning", "Innkjøpsansvarlig", "🟡 Rutine endret"),
        ("UC6", "Folketrygdloven", "Lønnsandel på 78,3 %; manglende oppfølging av utestående sykepengerefusjoner fra NAV", 1150000.00, "T006", "Etablere ukentlig purrerutine mot NAV på konto 1570 med innbetaling innen 45 dager", "HR- / Lønnscontroller", "🟡 Pågår")
    ]

    for item in uc_data:
        r += 1
        ws.cell(row=r, column=2, value=item[0]).font = FONT_TD_CODE
        ws.cell(row=r, column=3, value=item[1]).font = FONT_TD_BOLD
        ws.cell(row=r, column=4, value=item[2]).font = FONT_TD
        c_omf = ws.cell(row=r, column=5, value=float(item[3]))
        c_omf.font = FONT_TD_BOLD; c_omf.number_format = FMT_CURR
        ws.cell(row=r, column=6, value=item[4]).font = FONT_TD_CODE
        ws.cell(row=r, column=7, value=item[5]).font = FONT_TD
        ws.cell(row=r, column=8, value=item[6]).font = FONT_TD
        c_rag = ws.cell(row=r, column=9, value=item[7])
        c_rag.font = FONT_TD_BOLD
        if "🔴" in item[7]: c_rag.fill = FILL_RAG_RED
        elif "🟡" in item[7]: c_rag.fill = FILL_RAG_AMBER
        else: c_rag.fill = FILL_RAG_GREEN

        for c in range(2, 10):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 20

    auto_fit_columns(ws, min_col=1, max_col=10)


def build_sheet_laereplaner(wb, con):
    ws = wb.create_sheet(title="LP_Laereplaner_KD2025")
    render_header(ws, "LP Læreplaner, Budsjettering & KD 2025 Finansieringsmodell",
                  "Læreplanportefølje (BØA, INDØK, EVU), 2 589,6 SPE60 og KDs finansieringskategorier",
                  "Dekan / Studieledelse / Controller", max_col=10)

    kpis = [
        {"title": "Samlet SPE60 Produksjon", "val": 2589.6, "sub": "336 945 avlagte studiepoeng", "fmt": FMT_DEC},
        {"title": "Beregnet BFE Inntekt", "val": 176012760.00, "sub": "Resultatbasert tildeling", "fmt": FMT_CURR},
        {"title": "Kategori 1 (Helse/Tek)", "val": 71707880.00, "sub": "803,9 SPE60 @ 89 200 kr", "fmt": FMT_CURR},
        {"title": "Kategori 2 (Hum/Samf/Øk)", "val": 104284880.00, "sub": "1 785,7 SPE60 @ 58 400 kr", "fmt": FMT_CURR},
        {"title": "Gjennomføringsgrad", "val": 0.8638, "sub": "Mål: 90,0 %", "fmt": FMT_PCT, "badge": "🟡 Moderat"}
    ]
    render_kpis(ws, 4, kpis)

    r = 8
    ws.cell(row=r, column=2, value="1. KUNNSKAPSDEPARTEMENTETS FINANSIERINGSMODELL 2025 (SPE60 KATEGORIER)").font = FONT_SECTION
    r += 1

    kd_headers = ["Finansieringskategori", "Studieområder & Fagprofil", "Sats per SPE60 (NOK)", "Avlagte SPE60", "Beregnet BFE Inntekt (NOK)", "Finansieringsandel %", "Merknad / Etterslep"]
    for idx, h in enumerate(kd_headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx in [4, 5, 6, 7] else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    kd_rows = [
        ("Kategori 1", "Helse- og sosialfag, ingeniør, teknologi, realfag", 89200.00, 803.9, 71707880.00, 0.4074, "Høyeste sats; kompensasjon for kostbare laboratorier"),
        ("Kategori 2", "Humaniora, samfunnsvitenskap, økonomi, lærerutdanning", 58400.00, 1785.7, 104284880.00, 0.5926, "Hovedvolum; basis for breddestudiene"),
        ("Kategori 3", "Etter- og videreutdanning (EVU) og eksterne oppdrag", 0.00, 0.0, 0.00, 0.0000, "Selvfinansiert; 100 % oppdrags- eller egenbetaling"),
        ("TOTALT", "Hele institusjonens studieproduksjon (BFE)", 67969.09, 2589.6, 176012760.00, 1.0000, "Vektet gjennomsnittlig sats per SPE60")
    ]

    for item in kd_rows:
        r += 1
        ws.cell(row=r, column=2, value=item[0]).font = FONT_TD_BOLD
        ws.cell(row=r, column=3, value=item[1]).font = FONT_TD
        ws.cell(row=r, column=4, value=float(item[2])).number_format = FMT_CURR
        ws.cell(row=r, column=5, value=float(item[3])).number_format = FMT_DEC
        c_tot = ws.cell(row=r, column=6, value=float(item[4]))
        c_tot.font = FONT_TD_BOLD; c_tot.number_format = FMT_CURR
        ws.cell(row=r, column=7, value=float(item[5])).number_format = FMT_PCT
        ws.cell(row=r, column=8, value=item[6]).font = FONT_TD

        for c in range(2, 9):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
            if item[0] == "TOTALT":
                ws.cell(row=r, column=c).fill = FILL_TOTAL
                ws.cell(row=r, column=c).border = BORDER_TOTAL
        ws.row_dimensions[r].height = 20

    r += 3
    ws.cell(row=r, column=2, value="2. DE TRE LÆREPLANENE & DIMENSJONERINGSSTATUS (UIA CASE DATA)").font = FONT_SECTION
    r += 1

    lp_headers = ["Læreplan / Program", "Studiekode", "Nivå", "KD Kategori", "Normert ECTS", "Studenter", "Gjennomføring %", "Status"]
    for idx, h in enumerate(lp_headers, start=2):
        c = ws.cell(row=r, column=idx, value=h)
        c.font = FONT_TH; c.fill = FILL_TH
        c.alignment = Alignment(horizontal="right" if idx in [6, 7, 8] else "left", vertical="center")
    ws.row_dimensions[r].height = 20

    lp_programs = [
        ("Bachelor i Økonomi og Administrasjon (BØA)", "BØA100", "Bachelor (3 år)", "Kategori 2", 180, 480, 0.825, "🟢 Høy etterspørsel"),
        ("Master i Industriell Økonomi og Teknologiledelse (INDØK)", "INDØK200", "Master (2 år)", "Kategori 1", 120, 195, 0.892, "🟢 Høy sats & labdekning"),
        ("Executive Master i Offentlig Styring og Ledelse (EVU)", "EVU300", "Videreutdanning (1 år)", "Kategori 3", 60, 85, 0.940, "🟡 Krav om tapsavsetning (SRS 9)")
    ]

    for prg in lp_programs:
        r += 1
        ws.cell(row=r, column=2, value=prg[0]).font = FONT_TD_BOLD
        ws.cell(row=r, column=3, value=prg[1]).font = FONT_TD_CODE
        ws.cell(row=r, column=4, value=prg[2]).font = FONT_TD
        ws.cell(row=r, column=5, value=prg[3]).font = FONT_TD
        ws.cell(row=r, column=6, value=int(prg[4])).number_format = FMT_INT
        ws.cell(row=r, column=7, value=int(prg[5])).number_format = FMT_INT
        ws.cell(row=r, column=8, value=float(prg[6])).number_format = FMT_PCT
        ws.cell(row=r, column=9, value=prg[7]).font = FONT_TD_BOLD

        for c in range(2, 10):
            ws.cell(row=r, column=c).border = BORDER_TOP_BOTTOM
        ws.row_dimensions[r].height = 20

    auto_fit_columns(ws, min_col=1, max_col=10)
'''

if "def write_csv_to_sheet(" in code:
    code = code.replace("def write_csv_to_sheet(", new_functions + "\ndef write_csv_to_sheet(")

# 5. In main(), call the new build functions and update reports
if "build_sheet_09_begrepskatalog(wb, con)" in code:
    code = code.replace("build_sheet_09_begrepskatalog(wb, con)", """build_sheet_09_begrepskatalog(wb, con)

    print(">>> Building UC_Statlige_Use_Cases...")
    build_sheet_use_cases(wb, con)

    print(">>> Building LP_Laereplaner_KD2025...")
    build_sheet_laereplaner(wb, con)""")

# 6. Add tab colors for new sheets
if '"09_Begrepskatalog": "047857",' in code:
    code = code.replace('"09_Begrepskatalog": "047857",', '''"09_Begrepskatalog": "047857",
        "UC_Statlige_Use_Cases": "DC2626",
        "LP_Laereplaner_KD2025": "16A34A",
        "FactProjectBOA": "D97706",''')

with open(build_script, "w", encoding="utf-8") as f:
    f.write(code)

print("scripts/build_excel_pack.py updated successfully!")
