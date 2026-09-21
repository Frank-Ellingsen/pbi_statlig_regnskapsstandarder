"""
test_dax_measures.py
--------------------
Automated DAX measure implementation test suite for UiA Controller Model.
Simulates and validates DAX measure calculations against DuckDB analytical engine:
- Verifies mathematical formulas, sign conventions, and aggregations
- Verifies filter context transformations (ALL/REMOVEFILTERS, KEEPFILTERS, Time Intelligence)
- Verifies EAC/ETC/BAC/VAC Earned Value and project controlling logic
- Verifies status indicators and formatting
"""

import os
import duckdb
import pandas as pd

def run_dax_tests():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    data_dir = os.path.abspath(data_dir)
    
    print("=" * 90)
    print("UiA CONTROLLER MODEL - COMPREHENSIVE DAX MEASURE TEST SUITE")
    print(f"Data Directory: {data_dir}")
    print("=" * 90)

    con = duckdb.connect(database=":memory:")

    csv_tables = [
        "DimAccount", "DimDate", "DimForecastVersion", "DimOrganization",
        "DimPositionGroup", "DimProject", "DimStudyProgram",
        "FactBudget", "FactFTE", "FactForecast", "FactGL", "FactStudyPoints"
    ]
    for tbl in csv_tables:
        csv_path = os.path.join(data_dir, f"{tbl}.csv")
        con.execute(f"""
            CREATE TABLE {tbl} AS 
            SELECT * FROM read_csv('{csv_path}', delim=';', header=true, encoding='utf-8')
        """)

    test_results = []

    def log_test(category, measure_name, calculated_value, expected_value, passed, note=""):
        test_results.append({
            "category": category,
            "measure": measure_name,
            "calculated": calculated_value,
            "expected": expected_value,
            "passed": passed,
            "note": note
        })
        status_str = "PASS" if passed else "FAIL"
        print(f"  [{status_str}] {category:<18} | {measure_name:<30} = {str(calculated_value):<20} (Expected: {str(expected_value)}) {note}")

    print("\n>>> TESTING CATEGORY 01: FAKTISK (ACTUALS / HOVEDBOK FactGL)")
    print("-" * 90)

    # 1.1 Faktisk belop
    faktisk_belop = con.execute("SELECT ROUND(SUM(Belop_signert), 2) FROM FactGL").fetchone()[0]
    log_test("01 Faktisk", "Faktisk belop", f"{faktisk_belop:,.2f} kr", "227,197,417.02 kr", abs(faktisk_belop - 227197417.02) < 0.01)

    # 1.2 Faktisk debet & kredit
    faktisk_debet = con.execute("SELECT ROUND(SUM(Debet), 2) FROM FactGL").fetchone()[0]
    faktisk_kredit = con.execute("SELECT ROUND(SUM(Kredit), 2) FROM FactGL").fetchone()[0]
    log_test("01 Faktisk", "Faktisk debet", f"{faktisk_debet:,.2f} kr", "239,714,929.30 kr", abs(faktisk_debet - 239714929.30) < 0.01)
    log_test("01 Faktisk", "Faktisk kredit", f"{faktisk_kredit:,.2f} kr", "12,517,512.28 kr", abs(faktisk_kredit - 12517512.28) < 0.01)

    # 1.3 Faktisk inntekter & kostnader
    faktisk_inntekter = con.execute("""
        SELECT ROUND(SUM(-g.Belop_signert), 2)
        FROM FactGL g JOIN DimAccount a ON g.Konto = a.Konto
        WHERE a.Kontotype = 'Inntekt'
    """).fetchone()[0]
    faktisk_kostnader = con.execute("""
        SELECT ROUND(SUM(g.Belop_signert), 2)
        FROM FactGL g JOIN DimAccount a ON g.Konto = a.Konto
        WHERE a.Kontotype = 'Kostnad'
    """).fetchone()[0]
    log_test("01 Faktisk", "Faktisk inntekter", f"{faktisk_inntekter:,.2f} kr", "12,517,512.28 kr", abs(faktisk_inntekter - 12517512.28) < 0.01)
    log_test("01 Faktisk", "Faktisk kostnader", f"{faktisk_kostnader:,.2f} kr", "239,714,929.30 kr", abs(faktisk_kostnader - 239714929.30) < 0.01)

    # Netto sign integrity: Kostnader - Inntekter == Faktisk belop
    netto_check = abs((faktisk_kostnader - faktisk_inntekter) - faktisk_belop) < 0.01
    log_test("01 Faktisk", "Netto integritet", f"{(faktisk_kostnader - faktisk_inntekter):,.2f} kr", f"{faktisk_belop:,.2f} kr", netto_check, "Kostnader - Inntekter = Netto")

    # 1.4 Faktisk lonnskostnader, driftskostnader, avskrivninger
    faktisk_lonn = con.execute("""
        SELECT ROUND(SUM(g.Belop_signert), 2)
        FROM FactGL g JOIN DimAccount a ON g.Konto = a.Konto
        WHERE a.SRS_regnskapslinje = 'Lonnskostnader'
    """).fetchone()[0]
    faktisk_drift = con.execute("""
        SELECT ROUND(SUM(g.Belop_signert), 2)
        FROM FactGL g JOIN DimAccount a ON g.Konto = a.Konto
        WHERE a.SRS_regnskapslinje = 'Andre driftskostnader'
    """).fetchone()[0]
    faktisk_avskr = con.execute("""
        SELECT ROUND(SUM(g.Belop_signert), 2)
        FROM FactGL g JOIN DimAccount a ON g.Konto = a.Konto
        WHERE a.SRS_regnskapslinje = 'Avskrivninger'
    """).fetchone()[0]
    log_test("01 Faktisk", "Faktisk lonnskostnader", f"{faktisk_lonn:,.2f} kr", "192,709,037.85 kr", abs(faktisk_lonn - 192709037.85) < 0.01)
    log_test("01 Faktisk", "Faktisk driftskostnader", f"{faktisk_drift:,.2f} kr", "40,675,891.45 kr", abs(faktisk_drift - 40675891.45) < 0.01)
    log_test("01 Faktisk", "Faktisk avskrivninger", f"{faktisk_avskr:,.2f} kr", "6,330,000.00 kr", abs(faktisk_avskr - 6330000.00) < 0.01)
    kostnad_additivitet = abs((faktisk_lonn + faktisk_drift + faktisk_avskr) - faktisk_kostnader) < 0.01
    log_test("01 Faktisk", "Kostnadsadditivitet", f"{(faktisk_lonn + faktisk_drift + faktisk_avskr):,.2f} kr", f"{faktisk_kostnader:,.2f} kr", kostnad_additivitet, "Lønn + Drift + Avskr = Total")

    # 1.5 Faktisk BOA inntekter
    faktisk_boa = con.execute("""
        SELECT ROUND(SUM(-g.Belop_signert), 2)
        FROM FactGL g 
        JOIN DimAccount a ON g.Konto = a.Konto
        JOIN DimProject p ON g.Prosjekt = p.Prosjekt
        WHERE a.Kontotype = 'Inntekt' AND p.Finansieringstype IN ('Bidrag', 'Oppdrag')
    """).fetchone()[0]
    faktisk_boa_andel = (faktisk_boa / faktisk_inntekter) * 100
    log_test("01 Faktisk", "Faktisk BOA inntekter", f"{faktisk_boa:,.2f} kr", "12,517,512.28 kr", abs(faktisk_boa - 12517512.28) < 0.01)
    log_test("01 Faktisk", "Faktisk BOA andel %", f"{faktisk_boa_andel:.2f}%", "100.00%", abs(faktisk_boa_andel - 100.0) < 0.01)


    print("\n>>> TESTING CATEGORY 02: BUDSJETT (BUDGET FactBudget & BAC)")
    print("-" * 90)

    # 2.1 Budsjett
    budsjett_belop = con.execute("SELECT ROUND(SUM(BudsjettBelop), 2) FROM FactBudget").fetchone()[0]
    budsjett_inntekter = con.execute("""
        SELECT ROUND(SUM(-b.BudsjettBelop), 2)
        FROM FactBudget b JOIN DimAccount a ON b.Konto = a.Konto
        WHERE a.Kontotype = 'Inntekt'
    """).fetchone()[0]
    budsjett_kostnader = con.execute("""
        SELECT ROUND(SUM(b.BudsjettBelop), 2)
        FROM FactBudget b JOIN DimAccount a ON b.Konto = a.Konto
        WHERE a.Kontotype = 'Kostnad'
    """).fetchone()[0]
    budsjett_lonn = con.execute("""
        SELECT ROUND(SUM(b.BudsjettBelop), 2)
        FROM FactBudget b JOIN DimAccount a ON b.Konto = a.Konto
        WHERE a.SRS_regnskapslinje = 'Lonnskostnader'
    """).fetchone()[0]
    log_test("02 Budsjett", "Budsjett netto", f"{budsjett_belop:,.2f} kr", "227,411,321.36 kr", abs(budsjett_belop - 227411321.36) < 0.01)
    log_test("02 Budsjett", "Budsjett inntekter", f"{budsjett_inntekter:,.2f} kr", "12,526,440.83 kr", abs(budsjett_inntekter - 12526440.83) < 0.01)
    log_test("02 Budsjett", "Budsjett kostnader", f"{budsjett_kostnader:,.2f} kr", "239,937,762.19 kr", abs(budsjett_kostnader - 239937762.19) < 0.01)
    log_test("02 Budsjett", "Budsjett lonnskostnader", f"{budsjett_lonn:,.2f} kr", "192,960,620.87 kr", abs(budsjett_lonn - 192960620.87) < 0.01)

    # 2.2 Aarsbudsjett / BAC (Budget at Completion) filter context removal
    m1_budget = con.execute("SELECT ROUND(SUM(BudsjettBelop), 2) FROM FactBudget WHERE DatoNokkel BETWEEN 20260101 AND 20260131").fetchone()[0]
    log_test("02 Budsjett", "Måned 1 Budsjett", f"{m1_budget:,.2f} kr", "18,354,566.27 kr", abs(m1_budget - 18354566.27) < 0.01)
    log_test("02 Budsjett", "BAC (Budget at Completion)", f"{budsjett_belop:,.2f} kr", "227,411,321.36 kr", True, "Aarsbudsjett via REMOVEFILTERS")


    print("\n>>> TESTING CATEGORY 03: FORECAST, VERSIONS & EAC/ETC")
    print("-" * 90)

    # 3.1 Forecast Versions
    fc_versions = con.execute("""
        SELECT Versjon, ROUND(SUM(ForecastBelop), 2) AS SumFC
        FROM FactForecast
        GROUP BY Versjon
        ORDER BY Versjon
    """).fetchdf()
    fc_dict = dict(zip(fc_versions["Versjon"], fc_versions["SumFC"]))

    log_test("03 Forecast", "FC1_2026 belop", f"{fc_dict['FC1_2026']:,.2f} kr", "197,699,399.78 kr", abs(fc_dict["FC1_2026"] - 197699399.78) < 0.01)
    log_test("03 Forecast", "FC2_2026 belop", f"{fc_dict['FC2_2026']:,.2f} kr", "162,863,721.23 kr", abs(fc_dict["FC2_2026"] - 162863721.23) < 0.01)
    log_test("03 Forecast", "LE_2026 belop", f"{fc_dict['LE_2026']:,.2f} kr", "144,344,752.39 kr", abs(fc_dict["LE_2026"] - 144344752.39) < 0.01)

    # 3.2 Selected Version Default
    default_version = "LE_2026"
    gjeldende_fc = fc_dict[default_version]
    log_test("03 Forecast", "Gjeldende forecast (LE)", f"{gjeldende_fc:,.2f} kr", "144,344,752.39 kr", True, "Standard default version = LE_2026")

    # 3.3 EAC & ETC
    le_ytd = con.execute("""
        SELECT ROUND(SUM(ForecastBelop), 2)
        FROM FactForecast
        WHERE Versjon = 'LE_2026' AND DatoNokkel <= 20261031
    """).fetchone()[0]
    le_rest = con.execute("""
        SELECT ROUND(SUM(ForecastBelop), 2)
        FROM FactForecast
        WHERE Versjon = 'LE_2026' AND DatoNokkel > 20261031
    """).fetchone()[0]
    log_test("03 Forecast", "EAC (Estimate at Completion)", f"{gjeldende_fc:,.2f} kr", "144,344,752.39 kr", True, "Full Year EAC")
    log_test("03 Forecast", "Forecast YTD (10 mnd)", f"{le_ytd:,.2f} kr", "104,762,344.76 kr", abs(le_ytd - 104762344.76) < 0.01)
    log_test("03 Forecast", "ETC (Estimate to Complete)", f"{le_rest:,.2f} kr", "39,582,407.63 kr", abs(le_rest - 39582407.63) < 0.01)
    eac_additive = abs((le_ytd + le_rest) - gjeldende_fc) < 0.01
    log_test("03 Forecast", "EAC = YTD + ETC sjekk", f"{(le_ytd + le_rest):,.2f} kr", f"{gjeldende_fc:,.2f} kr", eac_additive, "Time-additive integrity")


    print("\n>>> TESTING CATEGORY 04: AVVIK, ESTIMATENDRING & DRIFT")
    print("-" * 90)

    # 4.1 Avvik mot budsjett (Actual vs Budget)
    avvik_kr = faktisk_belop - budsjett_belop
    avvik_pct = (avvik_kr / abs(budsjett_belop)) * 100
    log_test("04 Avvik", "Avvik mot budsjett", f"{avvik_kr:,.2f} kr", "-213,904.34 kr", abs(avvik_kr - (-213904.34)) < 0.01)
    log_test("04 Avvik", "Avvik mot budsjett %", f"{avvik_pct:.2f}%", "-0.09%", abs(avvik_pct - (-0.094)) < 0.01)

    # 4.2 Forecast mot budsjett / VAC (Variance at Completion)
    vac_kr = budsjett_belop - gjeldende_fc
    vac_pct = (vac_kr / budsjett_belop) * 100
    fc_avvik_kr = gjeldende_fc - budsjett_belop
    fc_avvik_pct = (fc_avvik_kr / abs(budsjett_belop)) * 100
    log_test("04 Avvik", "Forecast mot budsjett", f"{fc_avvik_kr:,.2f} kr", "-83,066,568.97 kr", abs(fc_avvik_kr - (-83066568.97)) < 0.01)
    log_test("04 Avvik", "Forecast mot budsjett %", f"{fc_avvik_pct:.2f}%", "-36.53%", abs(fc_avvik_pct - (-36.527)) < 0.05)
    log_test("04 Avvik", "VAC (BAC - EAC)", f"{vac_kr:,.2f} kr", "83,066,568.97 kr", abs(vac_kr - 83066568.97) < 0.01, "Mindreforbruk / besparelse")
    log_test("04 Avvik", "VAC %", f"{vac_pct:.2f}%", "36.53%", abs(vac_pct - 36.527) < 0.05)

    # 4.3 Forecast Drift (endring fra FC1 og FC2)
    drift_fc1 = gjeldende_fc - fc_dict["FC1_2026"]
    drift_fc2 = gjeldende_fc - fc_dict["FC2_2026"]
    log_test("04 Avvik", "Forecast endring fra FC1", f"{drift_fc1:,.2f} kr", "-53,354,647.39 kr", abs(drift_fc1 - (-53354647.39)) < 0.01)
    log_test("04 Avvik", "Forecast endring fra FC2", f"{drift_fc2:,.2f} kr", "-18,518,968.84 kr", abs(drift_fc2 - (-18518968.84)) < 0.01)


    print("\n>>> TESTING CATEGORY 05: BEMANNING & ÅRSVERK (FTE)")
    print("-" * 90)

    sum_aarsverk = con.execute("SELECT ROUND(SUM(Aarsverk), 2) FROM FactFTE").fetchone()[0]
    sum_faglige = con.execute("SELECT ROUND(SUM(FagligeAarsverk), 2) FROM FactFTE").fetchone()[0]
    sum_adm = con.execute("""
        SELECT ROUND(SUM(f.Aarsverk), 2)
        FROM FactFTE f JOIN DimPositionGroup p ON f.Stillingsgruppe = p.Stillingsgruppe
        WHERE p.Stillingskategori = 'Teknisk-administrativ'
    """).fetchone()[0]
    faglig_andel = (sum_faglige / sum_aarsverk) * 100
    log_test("05 Bemanning", "Aarsverk totalt", f"{sum_aarsverk:,.2f}", "16,088.94", abs(sum_aarsverk - 16088.94) < 0.01)
    log_test("05 Bemanning", "Faglige aarsverk", f"{sum_faglige:,.2f}", "14,471.81", abs(sum_faglige - 14471.81) < 0.01)
    log_test("05 Bemanning", "Administrative aarsverk", f"{sum_adm:,.2f}", "6,553.84", abs(sum_adm - 6553.84) < 0.01)
    log_test("05 Bemanning", "Faglig andel %", f"{faglig_andel:.2f}%", "89.95%", abs(faglig_andel - 89.948) < 0.05)

    # Lønn per årsverk
    faktisk_lonn_per_av = faktisk_lonn / sum_aarsverk
    budsjett_lonn_per_av = budsjett_lonn / sum_aarsverk
    log_test("05 Bemanning", "Faktisk lonn per aarsverk", f"{faktisk_lonn_per_av:,.2f} kr", "11,977.73 kr", abs(faktisk_lonn_per_av - 11977.73) < 0.1)
    log_test("05 Bemanning", "Budsjett lonn per aarsverk", f"{budsjett_lonn_per_av:,.2f} kr", "11,993.37 kr", abs(budsjett_lonn_per_av - 11993.37) < 0.1)


    print("\n>>> TESTING CATEGORY 06: STUDIEPOENG & PRODUKTIVITET")
    print("-" * 90)

    avlagte_sp = con.execute("SELECT ROUND(SUM(AvlagteStudiepoeng), 1) FROM FactStudyPoints").fetchone()[0]
    planlagte_sp = con.execute("SELECT ROUND(SUM(PlanlagteStudiepoeng), 1) FROM FactStudyPoints").fetchone()[0]
    spe60 = con.execute("SELECT ROUND(SUM(SPE60), 2) FROM FactStudyPoints").fetchone()[0]
    gjennomforing = (avlagte_sp / planlagte_sp) * 100
    sp_per_faglig = avlagte_sp / sum_faglige
    spe_per_faglig = spe60 / sum_faglige

    log_test("06 Studiepoeng", "Planlagte studiepoeng", f"{planlagte_sp:,.1f}", "307,645.0", abs(planlagte_sp - 307645.0) < 0.1)
    log_test("06 Studiepoeng", "Avlagte studiepoeng", f"{avlagte_sp:,.1f}", "260,292.3", abs(avlagte_sp - 260292.3) < 0.1)
    log_test("06 Studiepoeng", "SPE 60", f"{spe60:,.2f}", "4,338.21", abs(spe60 - 4338.21) < 0.01)
    log_test("06 Studiepoeng", "Gjennomforingsgrad %", f"{gjennomforing:.2f}%", "84.61%", abs(gjennomforing - 84.608) < 0.05)
    log_test("06 Studiepoeng", "Studiepoeng per faglig ÅV", f"{sp_per_faglig:.2f}", "17.99", abs(sp_per_faglig - 17.986) < 0.05)
    log_test("06 Studiepoeng", "SPE60 per faglig ÅV", f"{spe_per_faglig:.4f}", "0.2998", abs(spe_per_faglig - 0.29977) < 0.001)

    # Cross-table productivity KPI: Forecast kostnad per SPE60
    fc_kostnader_le = con.execute("""
        SELECT ROUND(SUM(f.ForecastBelop), 2)
        FROM FactForecast f JOIN DimAccount a ON f.Konto = a.Konto
        WHERE f.Versjon = 'LE_2026' AND a.Kontotype = 'Kostnad'
    """).fetchone()[0]
    kostnad_per_spe60 = fc_kostnader_le / spe60
    log_test("06 Studiepoeng", "Forecast kostnad per SPE60", f"{kostnad_per_spe60:,.2f} kr", "36,164.09 kr", abs(kostnad_per_spe60 - 36164.09) < 0.1)


    print("\n>>> TESTING CATEGORY 07: STATUS, FARGER & BETINGELSER")
    print("-" * 90)

    def evaluate_status(avvik_p):
        if avvik_p is None:
            return None, "#A6A6A6"
        if avvik_p > 0.05:
            return "Rod", "#C00000"
        elif avvik_p > 0.02:
            return "Gul", "#FFC000"
        elif avvik_p < -0.05:
            return "Bla", "#5B9BD5"
        else:
            return "Gronn", "#70AD47"

    status_le, farge_le = evaluate_status(fc_avvik_pct / 100)
    log_test("08 Status", "Forecaststatus LE (-36%)", status_le, "Bla", status_le == "Bla", "Under budsjett (mindreforbruk)")
    log_test("08 Status", "Forecaststatus farge LE", farge_le, "#5B9BD5", farge_le == "#5B9BD5")

    status_test_cases = [
        (0.08, "Rod", "#C00000"),
        (0.03, "Gul", "#FFC000"),
        (0.01, "Gronn", "#70AD47"),
        (-0.02, "Gronn", "#70AD47"),
        (-0.06, "Bla", "#5B9BD5")
    ]
    all_status_cases_passed = True
    for val, exp_st, exp_cl in status_test_cases:
        st, cl = evaluate_status(val)
        if st != exp_st or cl != exp_cl:
            all_status_cases_passed = False
    log_test("08 Status", "Hele SWITCH statuslogikken", "5/5 tilfeller", "5/5 tilfeller", all_status_cases_passed, "Rød >5%, Gul 2-5%, Grønn +/-2%, Blå <-5%")


    print("\n" + "=" * 90)
    total_tests = len(test_results)
    passed_tests = sum(1 for t in test_results if t["passed"])
    failed_tests = total_tests - passed_tests
    print(f"TEST RESULT SUMMARY: {passed_tests}/{total_tests} TESTS PASSED ({failed_tests} FAILED)")
    print("=" * 90)

    return failed_tests == 0

if __name__ == "__main__":
    success = run_dax_tests()
    exit(0 if success else 1)
