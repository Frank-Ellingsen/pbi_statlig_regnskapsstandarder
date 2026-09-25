import duckdb
from pathlib import Path

p = Path("c:/Users/frank/Desktop/UIA/uia_powerbi_complete_forecast_model/data")
con = duckdb.connect()

for f in ["FactGL", "FactBudget", "DimAccount", "FactFTE", "FactStudyPoints", "FactAction", "FactProjectBOA", "DimProject", "DimOrganization"]:
    csv_file = p / f"{f}.csv"
    if csv_file.exists():
        con.execute(f"CREATE TABLE {f} AS SELECT * FROM read_csv_auto('{csv_file.as_posix()}', delim=';', header=True)")

print("=== FACT GL BY USECASESREF ===")
print(con.execute("SELECT UseCasesRef, COUNT(*) as cnt, ROUND(SUM(Belop),2) as total_kr FROM FactGL GROUP BY UseCasesRef ORDER BY cnt DESC").df().to_string())

print("\n=== FACT BUDGET BY SCENARIO ===")
print(con.execute("SELECT Scenario, COUNT(*) as cnt, ROUND(SUM(BudsjettBelop),2) as total_kr FROM FactBudget GROUP BY Scenario ORDER BY Scenario").df().to_string())

print("\n=== KONTOKLASSER I FACT GL ===")
print(con.execute("""
    SELECT a.SRS_regnskapslinje, a.Kontotype, COUNT(*) as cnt, ROUND(SUM(g.Belop),2) as total_kr
    FROM FactGL g
    LEFT JOIN DimAccount a ON g.Konto = a.Konto
    GROUP BY a.SRS_regnskapslinje, a.Kontotype
    ORDER BY total_kr DESC
""").df().to_string())

print("\n=== F-05-20 AVSETNING (KONTO 2080) ===")
print(con.execute("""
    SELECT g.DatoNokkel, g.Organisasjonsnokkel, o.Fakultetsnavn, g.Konto, g.Belop, g.Tekst, g.UseCasesRef
    FROM FactGL g
    LEFT JOIN DimOrganization o ON g.Organisasjonsnokkel = o.Organisasjonsnokkel
    WHERE g.Konto = 2080
""").df().to_string())

print("\n=== BOA PROSJEKTER (FactProjectBOA) ===")
print(con.execute('SELECT Prosjekt, Prosjektnavn, Finansieringstype, Kontraktsbelop, PåløptKostnad, Inntektsført, "%TidGått", "%BudsjettForbrukt", RAG_Status FROM FactProjectBOA').df().to_string())

print("\n=== TILTAK (FactAction) ===")
print(con.execute("SELECT TiltakID, Organisasjonsnokkel, AnsvarligRolle, ForventetEffekt, RealisertEffekt, Status, UseCasesRef FROM FactAction").df().to_string())

print("\n=== STUDIEPOENG (FactStudyPoints) ===")
print(con.execute("""
    SELECT Studiekategori, COUNT(*) as cnt, ROUND(SUM(SPE60),1) as sum_spe60, ROUND(SUM(BeregnetInntekt),2) as sum_inntekt
    FROM FactStudyPoints
    GROUP BY Studiekategori
""").df().to_string())
print("\n=== MONTHLY ACTUALS VS BUDGET 2026 ===")
print(con.execute("""
    SELECT 
        SUBSTRING(CAST(DatoNokkel AS VARCHAR), 5, 2) as mnd,
        ROUND(SUM(CASE WHEN Belop > 0 THEN Belop ELSE 0 END)/1e6, 2) as kostnad_faktisk_m,
        ROUND(SUM(CASE WHEN Belop < 0 THEN -Belop ELSE 0 END)/1e6, 2) as inntekt_faktisk_m
    FROM FactGL
    GROUP BY mnd
    ORDER BY mnd
""").df().to_string())

print("\n=== MONTHLY BUDGET 2026 ===")
print(con.execute("""
    SELECT 
        SUBSTRING(CAST(DatoNokkel AS VARCHAR), 5, 2) as mnd,
        Scenario,
        ROUND(SUM(CASE WHEN BudsjettBelop > 0 THEN BudsjettBelop ELSE 0 END)/1e6, 2) as kostnad_bud_m,
        ROUND(SUM(CASE WHEN BudsjettBelop < 0 THEN -BudsjettBelop ELSE 0 END)/1e6, 2) as inntekt_bud_m
    FROM FactBudget
    WHERE Scenario IN ('BUD2026', 'LE_2026')
    GROUP BY mnd, Scenario
    ORDER BY mnd, Scenario
""").df().to_string())
