# -*- coding: utf-8 -*-
"""
update_controller_excel.py
--------------------------
Synchronizes UIA-Controller-Excel.xlsx with authentic Use Case metrics:
1. Updates Benchmarks sheet with exact case metrics.
2. Updates Projects sheet with 6 BOA projects + TDI columns.
3. Updates Actions sheet with FactAction.csv (including UseCasesRef).
4. Adds FactProjectBOA sheet with complete 18 columns.
5. Adds UseCases sheet with UC1-UC6 details.
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import csv
from pathlib import Path

root_dir = Path(__file__).parent.parent
data_dir = root_dir / "data"
excel_path = root_dir / "UIA-Controller-Excel.xlsx"

wb = openpyxl.load_workbook(excel_path)

# 1. Update Benchmarks
if "Benchmarks" in wb.sheetnames:
    ws_bench = wb["Benchmarks"]
    benchmarks_data = {
        "Kilderader – totalt": (11850, "rader"),
        "FactGL – transaksjoner": (722, "rader"),
        "Bokførte inntekter": (14270000.0, "NOK"),
        "Driftskostnader": (68381200.0, "NOK"),
        "Lønnskostnader": (50970000.0, "NOK"),
        "Lønnsandel": (0.7831, "%"),
        "Konto 2080 Avsetning": (-4800000.0, "NOK"),
        "Avsetningsgrad F-05-20": (0.0896, "%"),
        "Netto regnskap": (54111200.0, "NOK"),
        "Årsbudsjett": (81840000.0, "NOK"),
        "Forecast FC1": (88500000.0, "NOK"),
        "Forecast FC2": (92300000.0, "NOK"),
        "Latest Estimate": (96460000.0, "NOK"),
        "Forecastavvik": (-14620000.0, "NOK"),
        "Forventet tiltakseffekt": (-10250000.0, "NOK"),
        "Realisert tiltakseffekt": (-4850000.0, "NOK"),
        "Realiseringsgrad": (0.4731, "%"),
        "Forecast etter tiltak": (86210000.0, "NOK"),
        "Restavvik etter tiltak": (4370000.0, "NOK"),
        "BOA-inntekter": (20460000.0, "NOK"),
        "BOA-portefølje": (61500000.0, "NOK"),
        "TDI-årsbudsjett": (20200000.0, "NOK"),
        "Årsverk siste måned": (1285.93, "FTE"),
        "Faglige årsverk siste måned": (661.77, "FTE"),
        "Registrerte studenter siste måned": (6490, "antall"),
        "Avlagte studiepoeng helår": (336945.0, "SP"),
        "SPE60 helår": (2589.6, "SPE60"),
        "BFE-inntekt": (176012760.0, "NOK")
    }

    # Clear and rewrite Benchmarks
    ws_bench.delete_rows(1, ws_bench.max_row + 1)
    ws_bench.append(["Nøkkeltall", "Verdi", "Enhet"])
    for k, (v, u) in benchmarks_data.items():
        ws_bench.append([k, v, u])
    print(f"Benchmarks updated with {len(benchmarks_data)} indicators.")

# 2. Update Projects sheet with FactProjectBOA
if "Projects" in wb.sheetnames:
    ws_proj = wb["Projects"]
    ws_proj.delete_rows(1, ws_proj.max_row + 1)
    
    boa_csv = data_dir / "FactProjectBOA.csv"
    with open(boa_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        ws_proj.append([c.lstrip('\ufeff') for c in header])
        for row in reader:
            parsed = []
            for val in row:
                try:
                    if "." in val:
                        parsed.append(float(val))
                    else:
                        parsed.append(int(val))
                except ValueError:
                    parsed.append(val)
            ws_proj.append(parsed)
    print("Projects sheet updated with 6 BOA TDI projects.")

# 3. Update Actions sheet with FactAction.csv
if "Actions" in wb.sheetnames:
    ws_act = wb["Actions"]
    ws_act.delete_rows(1, ws_act.max_row + 1)
    
    act_csv = data_dir / "FactAction.csv"
    with open(act_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        ws_act.append([c.lstrip('\ufeff') for c in header])
        for row in reader:
            parsed = []
            for val in row:
                try:
                    if "." in val:
                        parsed.append(float(val))
                    else:
                        parsed.append(int(val))
                except ValueError:
                    parsed.append(val)
            ws_act.append(parsed)
    print("Actions sheet updated with FactAction.csv.")

# 4. Add or update FactProjectBOA sheet
if "FactProjectBOA" in wb.sheetnames:
    del wb["FactProjectBOA"]
ws_boa = wb.create_sheet(title="FactProjectBOA")
boa_csv = data_dir / "FactProjectBOA.csv"
with open(boa_csv, "r", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=";")
    header = next(reader)
    ws_boa.append([c.lstrip('\ufeff') for c in header])
    for row in reader:
        parsed = []
        for val in row:
            try:
                if "." in val:
                    parsed.append(float(val))
                else:
                    parsed.append(int(val))
            except ValueError:
                parsed.append(val)
        ws_boa.append(parsed)
print("FactProjectBOA sheet created.")

# 5. Add or update UseCases sheet
if "UseCases" in wb.sheetnames:
    del wb["UseCases"]
ws_uc = wb.create_sheet(title="UseCases")
ws_uc.append(["Use Case", "Rettslig Standard", "Kjerneavvik / Problemstilling", "Finansielt Omfang", "Tiltak ID", "Forankret Styringstiltak", "Ansvarlig Rolle", "Status"])
uc_rows = [
    ["UC1", "Rundskriv F-05-20", "5 %-regelen overskredet: Avsetning på konto 2080 er 8,96 % (-4,8 MNOK mot 5,0 % sperre 2,68 MNOK)", 2120000.0, "T002", "Fremskynde strategiske IT- og labinvesteringer innen Q4", "Fakultetsdirektør", "Kritisk"],
    ["UC2", "DFØ SRS 10", "Oppdrags-/bidragsinntekt feilaktig inntektsført før kostnadspåløp (motsatt sammenstilling)", 2010000.0, "T005", "Innføre månedlig automatisk avstemming mellom påløpte BOA-kostnader og konto 2900", "Prosjektcontroller", "Korrigert"],
    ["UC3", "DFØ SRS 9", "Tapskontrakt på oppdrag EVU001: Merforbruk krever umiddelbar tapsavsetning", 450000.0, "T003", "Bokføre tapsavsetning på konto 7790 mot 2800; stramme timeføring på EVU", "Instituttleder", "Tapsført"],
    ["UC4", "DFØ SRS 17", "Varige driftsmidler (lab/servere) feilaktig kostnadsført direkte på konto 6500", 1200000.0, "T001", "Omklassifisere og aktivere på konto 1200 i balansen med 5 års avskrivning", "Regnskapssjef", "Fullført"],
    ["UC5", "FOA / LOA", "Konsulentanskaffelse bestilt over terskelverdi uten tilstrekkelig kunngjøring", 620000.0, "T004", "Protokollføre anskaffelsesavvik og innføre obligatorisk forhåndsgodkjenning", "Innkjøpsansvarlig", "Rutine endret"],
    ["UC6", "Folketrygdloven", "Lønnsandel på 78,3 %; manglende oppfølging av utestående sykepengerefusjoner fra NAV", 1150000.0, "T006", "Etablere ukentlig purrerutine mot NAV på konto 1570 med innbetaling innen 45 dager", "HR- / Lønnscontroller", "Pågår"]
]
for r in uc_rows:
    ws_uc.append(r)
print("UseCases sheet created.")

wb.save(excel_path)
print(f"UIA-Controller-Excel.xlsx saved successfully ({excel_path.stat().st_size:,} bytes)!")
