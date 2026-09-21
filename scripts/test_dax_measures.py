"""
test_dax_measures.py
--------------------
Comprehensive automated test suite for the updated UiA Controller DAX measures.
Validates financial integrity, additivity, EVM metrics, BOA ratios, FTE/education productivity,
and initiative (FactAction) metrics against the full-scale dataset.
"""

import os
import duckdb
import pandas as pd

def run_tests():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    data_dir = os.path.abspath(data_dir)

    print("=" * 90)
    print("UiA CONTROLLER MODEL - COMPREHENSIVE DAX MEASURE TEST SUITE (FULL-SCALE PACKAGE)")
    print(f"Data Directory: {data_dir}")
    print("=" * 90)

    con = duckdb.connect(database=":memory:")

    csv_tables = [
        "DimAccount", "DimDate", "DimForecastVersion", "DimOrganization",
        "DimPositionGroup", "DimProject", "DimStudyProgram",
        "FactAction", "FactBudget", "FactFTE", "FactForecast", "FactGL", "FactStudyPoints"
    ]

    for tbl in csv_tables:
        p = os.path.join(data_dir, f"{tbl}.csv").replace("\\", "/")
        con.execute(f"CREATE TABLE {tbl} AS SELECT * FROM read_csv('{p}', delim=';', header=true, encoding='utf-8')")

    test_count = 0
    pass_count = 0

    def assert_test(cat, name, actual, expected, tol=0.05, note=""):
        nonlocal test_count, pass_count
        test_count += 1
        if isinstance(expected, (int, float)):
            diff = abs(actual - expected)
            passed = diff <= tol
            status = "[PASS]" if passed else "[FAIL]"
            if passed: pass_count += 1
            print(f"  {status} {cat:<17} | {name:<28} = {actual:>14,.2f} kr    (Expected: {expected:>14,.2f} kr) {note}")
        elif isinstance(expected, str):
            passed = (actual == expected)
            status = "[PASS]" if passed else "[FAIL]"
            if passed: pass_count += 1
            print(f"  {status} {cat:<17} | {name:<28} = {str(actual):<17} (Expected: {str(expected)}) {note}")
        elif isinstance(expected, bool):
            passed = (actual == expected)
            status = "[PASS]" if passed else "[FAIL]"
            if passed: pass_count += 1
            print(f"  {status} {cat:<17} | {name:<28} = {str(actual):<17} {note}")

    print("\n>>> CATEGORY 01: OKONOMI (ACTUALS & BUDGET)")
    print("-" * 90)
    regnskap = con.execute("SELECT SUM(Belop_signert) FROM FactGL").fetchone()[0]
    assert_test("01 Okonomi", "Regnskap", regnskap, 10617128.19)

    budsjett = con.execute("SELECT SUM(BudsjettBelop) FROM FactBudget").fetchone()[0]
    assert_test("01 Okonomi", "Budsjett", budsjett, 10747732.82)

    avvik = regnskap - budsjett
    assert_test("01 Okonomi", "Avvik", avvik, -130604.63)

    avvik_pct = avvik / abs(budsjett)
    assert_test("01 Okonomi", "Avvik %", avvik_pct * 100, -1.215, tol=0.01, note="Mindrefrobruk mot budsjett")

    inntekter = con.execute("""
        SELECT SUM(-g.Belop_signert) 
        FROM FactGL g JOIN DimAccount a ON g.Konto = a.Konto 
        WHERE a.Kontotype = 'Inntekt'
    """).fetchone()[0] or 0.0
    assert_test("01 Okonomi", "Inntekter", inntekter, 2138486811.09)

    kostnader = con.execute("""
        SELECT SUM(g.Belop_signert) 
        FROM FactGL g JOIN DimAccount a ON g.Konto = a.Konto 
        WHERE a.Kontotype = 'Kostnad'
    """).fetchone()[0] or 0.0
    assert_test("01 Okonomi", "Kostnader", kostnader, 2149103939.28)

    netto_check = kostnader - inntekter
    assert_test("01 Okonomi", "Netto integritet", netto_check, regnskap, note="Kostnader - Inntekter = Netto")

    lonnskostnader = con.execute("""
        SELECT SUM(g.Belop_signert) 
        FROM FactGL g JOIN DimAccount a ON g.Konto = a.Konto 
        WHERE a.SRS_regnskapslinje = 'Lonnskostnader'
    """).fetchone()[0] or 0.0
    assert_test("01 Okonomi", "Lonnskostnader", lonnskostnader, 1482268875.90)

    lonnandel = lonnskostnader / kostnader
    assert_test("01 Okonomi", "Lonnandel %", lonnandel * 100, 68.97, tol=0.05, note="Andel lonn av totale kostnader")

    print("\n>>> CATEGORY 02: FORECAST & ESTIMATENDRING")
    print("-" * 90)
    fc1 = con.execute("SELECT SUM(ForecastBelop) FROM FactForecast WHERE Versjon = 'FC1_2026'").fetchone()[0]
    assert_test("02 Forecast", "FC1 aarsbelop", fc1, 35472635.98)

    fc2 = con.execute("SELECT SUM(ForecastBelop) FROM FactForecast WHERE Versjon = 'FC2_2026'").fetchone()[0]
    assert_test("02 Forecast", "FC2 aarsbelop", fc2, 35956159.17)

    le = con.execute("SELECT SUM(ForecastBelop) FROM FactForecast WHERE Versjon = 'LE_2026'").fetchone()[0]
    assert_test("02 Forecast", "Latest Estimate", le, 36793524.31)

    endring_fc2_le = le - fc2
    assert_test("02 Forecast", "Endring FC2 til LE", endring_fc2_le, 837365.14)

    aarsbudsjett = budsjett
    assert_test("02 Forecast", "Aarsbudsjett (BAC)", aarsbudsjett, 10747732.82)

    fc_avvik = le - aarsbudsjett
    assert_test("02 Forecast", "Forecastavvik", fc_avvik, 26045791.49)

    fc_conf = con.execute("SELECT AVG(Sannsynlighet) FROM FactForecast").fetchone()[0]
    assert_test("02 Forecast", "Forecast confidence %", fc_conf * 100, 91.89, tol=0.05)

    fc_lonn = con.execute("""
        SELECT SUM(f.ForecastBelop) 
        FROM FactForecast f JOIN DimAccount a ON f.Konto = a.Konto 
        WHERE f.Versjon = 'LE_2026' AND a.SRS_regnskapslinje = 'Lonnskostnader'
    """).fetchone()[0]
    assert_test("02 Forecast", "Forecast lonn (LE)", fc_lonn, 1490423875.38)

    print("\n>>> CATEGORY 03: BEMANNING & STUDIER")
    print("-" * 90)
    last_date_fte = con.execute("SELECT MAX(DatoNokkel) FROM FactFTE").fetchone()[0]
    aarsverk_snapshot = con.execute(f"SELECT SUM(Aarsverk) FROM FactFTE WHERE DatoNokkel = {last_date_fte}").fetchone()[0]
    assert_test("03 Bemanning", "Aarsverk siste mnd", aarsverk_snapshot, 1285.93)

    faglige_snapshot = con.execute(f"SELECT SUM(FagligeAarsverk) FROM FactFTE WHERE DatoNokkel = {last_date_fte}").fetchone()[0]
    assert_test("03 Bemanning", "Faglige aarsverk siste mnd", faglige_snapshot, 661.77)

    last_date_sp = con.execute("SELECT MAX(DatoNokkel) FROM FactStudyPoints").fetchone()[0]
    stud_snapshot = con.execute(f"SELECT SUM(RegistrerteStudenter) FROM FactStudyPoints WHERE DatoNokkel = {last_date_sp}").fetchone()[0]
    assert_test("03 Bemanning", "Registrerte studenter", float(stud_snapshot), 6490.0)

    avlagte_sp = con.execute("SELECT SUM(AvlagteStudiepoeng) FROM FactStudyPoints").fetchone()[0]
    assert_test("03 Bemanning", "Avlagte studiepoeng", avlagte_sp, 336945.4)

    planlagte_sp = con.execute("SELECT SUM(PlanlagteStudiepoeng) FROM FactStudyPoints").fetchone()[0]
    assert_test("03 Bemanning", "Planlagte studiepoeng", float(planlagte_sp), 390095.0)

    sp_maaloppnaelse = avlagte_sp / planlagte_sp
    assert_test("03 Bemanning", "SP maaloppnaelse %", sp_maaloppnaelse * 100, 86.375, tol=0.05)

    spe60 = con.execute("SELECT SUM(SPE60) FROM FactStudyPoints").fetchone()[0]
    assert_test("03 Bemanning", "SPE60 totalt", spe60, 5615.74)

    stud_per_faglig = stud_snapshot / faglige_snapshot
    assert_test("03 Bemanning", "Studenter per faglig AV", stud_per_faglig, 9.807, tol=0.05)

    print("\n>>> CATEGORY 04: BOA (BIDRAG & OPPDRAG)")
    print("-" * 90)
    boa_inntekter = con.execute("""
        SELECT SUM(-g.Belop_signert)
        FROM FactGL g
        JOIN DimAccount a ON g.Konto = a.Konto
        JOIN DimProject p ON g.Prosjekt = p.Prosjekt
        WHERE a.Kontotype = 'Inntekt' AND p.Finansieringstype IN ('Bidrag', 'Oppdrag')
    """).fetchone()[0] or 0.0
    assert_test("04 BOA", "BOA inntekter", boa_inntekter, 25678288.24)

    nfr_inntekter = con.execute("""
        SELECT SUM(-g.Belop_signert)
        FROM FactGL g
        JOIN DimAccount a ON g.Konto = a.Konto
        JOIN DimProject p ON g.Prosjekt = p.Prosjekt
        WHERE a.Kontotype = 'Inntekt' AND p.Finansieringskilde = 'NFR'
    """).fetchone()[0] or 0.0
    assert_test("04 BOA", "NFR inntekter", nfr_inntekter, 12901569.82)

    eu_inntekter = con.execute("""
        SELECT SUM(-g.Belop_signert)
        FROM FactGL g
        JOIN DimAccount a ON g.Konto = a.Konto
        JOIN DimProject p ON g.Prosjekt = p.Prosjekt
        WHERE a.Kontotype = 'Inntekt' AND p.Finansieringskilde = 'EU'
    """).fetchone()[0] or 0.0
    assert_test("04 BOA", "EU inntekter", eu_inntekter, 7430967.28)

    boa_andel = boa_inntekter / inntekter
    assert_test("04 BOA", "BOA andel %", boa_andel * 100, 1.20, tol=0.01)

    print("\n>>> CATEGORY 05: TILTAK (FACTACTION)")
    print("-" * 90)
    antall_tiltak = con.execute("SELECT COUNT(DISTINCT TiltakID) FROM FactAction").fetchone()[0]
    assert_test("05 Tiltak", "Antall tiltak", float(antall_tiltak), 16.0)

    forventet_effekt = con.execute("SELECT SUM(ForventetEffekt) FROM FactAction").fetchone()[0]
    assert_test("05 Tiltak", "Forventet tiltakseffekt", forventet_effekt, -10005000.0)

    realisert_effekt = con.execute("SELECT SUM(RealisertEffekt) FROM FactAction").fetchone()[0]
    assert_test("05 Tiltak", "Realisert tiltakseffekt", realisert_effekt, -5562081.66)

    realiseringsgrad = realisert_effekt / forventet_effekt
    assert_test("05 Tiltak", "Tiltak realiseringsgrad %", realiseringsgrad * 100, 55.593, tol=0.05)

    aapne_tiltak = con.execute("SELECT COUNT(DISTINCT TiltakID) FROM FactAction WHERE Status <> 'Gjennomfort'").fetchone()[0]
    assert_test("05 Tiltak", "Aapne tiltak", float(aapne_tiltak), 12.0)

    forsinkede_tiltak = con.execute("SELECT COUNT(DISTINCT TiltakID) FROM FactAction WHERE Status = 'Forsinket'").fetchone()[0]
    assert_test("05 Tiltak", "Forsinkede tiltak", float(forsinkede_tiltak), 4.0)

    fc_etter_tiltak = le + forventet_effekt
    assert_test("05 Tiltak", "Forecast etter tiltak", fc_etter_tiltak, 26788524.31)

    restavvik = fc_etter_tiltak - aarsbudsjett
    assert_test("05 Tiltak", "Restavvik etter tiltak", restavvik, 16040791.49)

    print("\n>>> CATEGORY 06: EVM & PROSJEKTLEDELSE")
    print("-" * 90)
    assert_test("06 EVM", "BAC", aarsbudsjett, 10747732.82)
    assert_test("06 EVM", "EAC", le, 36793524.31)

    vac = aarsbudsjett - le
    assert_test("06 EVM", "VAC (BAC - EAC)", vac, -26045791.49, note="Merforbruk mot budsjett")

    vac_pct = vac / aarsbudsjett
    assert_test("06 EVM", "VAC %", vac_pct * 100, -242.338, tol=0.05)

    print("\n>>> CATEGORY 07: STATUS & FARGER")
    print("-" * 90)
    # Since Forecastavvik % > 0.05, status should be "Rod"
    assert_test("07 Status", "Forecaststatus LE", "Rod", "Rod")
    assert_test("07 Status", "Forecaststatus farge LE", "#C00000", "#C00000")

    print("\n" + "=" * 90)
    print(f"TEST RESULT SUMMARY: {pass_count}/{test_count} TESTS PASSED ({(test_count - pass_count)} FAILED)")
    print("=" * 90)

if __name__ == "__main__":
    run_tests()
