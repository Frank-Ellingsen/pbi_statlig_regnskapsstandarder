"""
validate_model.py
-----------------
Automated data model and referential integrity validator for UiA Controller Model.
Uses DuckDB to verify star-schema integrity, grain, and key reconciliations.
"""

import os
import duckdb
import pandas as pd

def run_validation():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    data_dir = os.path.abspath(data_dir)
    print("=" * 80)
    print("UiA CONTROLLER MODEL - DATA INTEGRITY & RECONCILIATION AUDIT")
    print(f"Data source path: {data_dir}")
    print("=" * 80)

    con = duckdb.connect(database=":memory:")

    csv_tables = [
        "DimAccount", "DimDate", "DimForecastVersion", "DimOrganization",
        "DimPositionGroup", "DimProject", "DimStudyProgram",
        "FactBudget", "FactFTE", "FactForecast", "FactGL", "FactStudyPoints",
        "Relationships_Forecast"
    ]

    for tbl in csv_tables:
        csv_path = os.path.join(data_dir, f"{tbl}.csv")
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Missing CSV file: {csv_path}")
        con.execute(f"""
            CREATE TABLE {tbl} AS 
            SELECT * FROM read_csv('{csv_path}', delim=';', header=true, encoding='utf-8')
        """)
        row_count = con.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        print(f"  Loaded {tbl:<25}: {row_count:>6} rows")

    print("\n" + "-" * 80)
    print("1. REFERENTIAL INTEGRITY AUDIT (19 STAR SCHEMA RELATIONSHIPS)")
    print("-" * 80)

    rel_df = con.execute("SELECT * FROM Relationships_Forecast").fetchdf()
    all_passed = True

    for _, row in rel_df.iterrows():
        fra_tbl = row["FraTabell"]
        fra_col = row["FraKolonne"]
        til_tbl = row["TilTabell"]
        til_col = row["TilKolonne"]

        # Check missing foreign keys:
        query = f"""
            SELECT COUNT(DISTINCT f.{til_col}) AS orphan_count
            FROM {til_tbl} f
            LEFT JOIN {fra_tbl} d ON f.{til_col} = d.{fra_col}
            WHERE d.{fra_col} IS NULL
        """
        orphans = con.execute(query).fetchone()[0]

        # Check primary key uniqueness on dimension
        pk_dup = con.execute(f"""
            SELECT COUNT(*) - COUNT(DISTINCT {fra_col}) FROM {fra_tbl}
        """).fetchone()[0]

        status = "PASSED" if orphans == 0 and pk_dup == 0 else "FAILED"
        if status == "FAILED":
            all_passed = False
        print(f"  [{status}] {fra_tbl}.{fra_col} (1) -> {til_tbl}.{til_col} (*) | PK DUP: {pk_dup}, ORPHANS: {orphans}")

    print("\n" + "-" * 80)
    print("2. FINANCIAL & CONTROLLING RECONCILIATIONS (2026)")
    print("-" * 80)

    # Actuals
    gl_stats = con.execute("""
        SELECT 
            COUNT(*) AS BilagCount,
            ROUND(SUM(Debet), 2) AS SumDebet,
            ROUND(SUM(Kredit), 2) AS SumKredit,
            ROUND(SUM(Belop_signert), 2) AS NetActuals
        FROM FactGL
    """).fetchdf()
    print("  FACT GL (ACTUALS):")
    print(f"    Bilag count       : {gl_stats['BilagCount'][0]:,}")
    print(f"    Total Debet       : {gl_stats['SumDebet'][0]:>15,.2f} NOK")
    print(f"    Total Kredit      : {gl_stats['SumKredit'][0]:>15,.2f} NOK")
    print(f"    Netto belop       : {gl_stats['NetActuals'][0]:>15,.2f} NOK")

    # Actuals split: Inntekter vs Kostnader
    gl_split = con.execute("""
        SELECT 
            a.Kontotype,
            ROUND(SUM(g.Belop_signert), 2) AS Belop
        FROM FactGL g
        JOIN DimAccount a ON g.Konto = a.Konto
        GROUP BY a.Kontotype
        ORDER BY a.Kontotype
    """).fetchdf()
    for _, r in gl_split.iterrows():
        print(f"    - {r['Kontotype']:<16}: {r['Belop']:>15,.2f} NOK")

    # Budget
    bgt_stats = con.execute("""
        SELECT 
            ROUND(SUM(BudsjettBelop), 2) AS TotalBudget,
            ROUND(SUM(CASE WHEN a.Kontotype = 'Inntekt' THEN -BudsjettBelop ELSE 0 END), 2) AS BudgetInntekter,
            ROUND(SUM(CASE WHEN a.Kontotype = 'Kostnad' THEN BudsjettBelop ELSE 0 END), 2) AS BudgetKostnader
        FROM FactBudget b
        JOIN DimAccount a ON b.Konto = a.Konto
    """).fetchdf()
    print("\n  FACT BUDGET:")
    print(f"    Budsjett inntekter: {bgt_stats['BudgetInntekter'][0]:>15,.2f} NOK")
    print(f"    Budsjett kostnader: {bgt_stats['BudgetKostnader'][0]:>15,.2f} NOK")
    print(f"    Budsjett netto    : {bgt_stats['TotalBudget'][0]:>15,.2f} NOK")

    # Forecast by Version
    fc_stats = con.execute("""
        SELECT 
            v.Versjon,
            v.Versjonsnavn,
            ROUND(SUM(f.ForecastBelop), 2) AS TotalForecast,
            ROUND(SUM(CASE WHEN a.Kontotype = 'Inntekt' THEN -f.ForecastBelop ELSE 0 END), 2) AS FC_Inntekter,
            ROUND(SUM(CASE WHEN a.Kontotype = 'Kostnad' THEN f.ForecastBelop ELSE 0 END), 2) AS FC_Kostnader
        FROM FactForecast f
        JOIN DimForecastVersion v ON f.Versjon = v.Versjon
        JOIN DimAccount a ON f.Konto = a.Konto
        GROUP BY v.Versjon, v.Versjonsnavn, v.Sortering
        ORDER BY v.Sortering
    """).fetchdf()
    print("\n  FACT FORECAST BY VERSION:")
    for _, r in fc_stats.iterrows():
        print(f"    [{r['Versjon']}] {r['Versjonsnavn']:<26}: Netto={r['TotalForecast']:>12,.2f} | Inntekt={r['FC_Inntekter']:>12,.2f} | Kostnad={r['FC_Kostnader']:>12,.2f}")

    # Årsverk & Studiepoeng
    fte_stats = con.execute("""
        SELECT 
            ROUND(SUM(Aarsverk), 2) AS SumAarsverk,
            ROUND(AVG(Aarsverk), 2) AS AvgAarsverk,
            ROUND(SUM(FagligeAarsverk), 2) AS SumFaglige
        FROM FactFTE
    """).fetchdf()
    print("\n  FACT FTE (ÅRSVERK):")
    print(f"    Sum årsverk       : {fte_stats['SumAarsverk'][0]:>15,.2f}")
    print(f"    Faglige årsverk   : {fte_stats['SumFaglige'][0]:>15,.2f}")

    sp_stats = con.execute("""
        SELECT 
            ROUND(SUM(AvlagteStudiepoeng), 1) AS AvlagteSP,
            ROUND(SUM(PlanlagteStudiepoeng), 1) AS PlanlagteSP,
            ROUND(SUM(SPE60), 2) AS SumSPE60,
            ROUND(SUM(AvlagteStudiepoeng) / NULLIF(SUM(PlanlagteStudiepoeng), 0) * 100, 2) AS GjennomforingPct
        FROM FactStudyPoints
    """).fetchdf()
    print("\n  FACT STUDY POINTS (PRODUKSJON):")
    print(f"    Planlagte SP      : {sp_stats['PlanlagteSP'][0]:>15,.1f}")
    print(f"    Avlagte SP        : {sp_stats['AvlagteSP'][0]:>15,.1f}")
    print(f"    Gjennomføring %   : {sp_stats['GjennomforingPct'][0]:>15.2f}%")
    print(f"    SPE 60 enheter    : {sp_stats['SumSPE60'][0]:>15,.2f}")

    print("\n" + "=" * 80)
    if all_passed:
        print("RESULT: ALL 19 RELATIONSHIPS & DATA INTEGRITY CHECKS PASSED PERFECTLY!")
    else:
        print("RESULT: WARNING - INTEGRITY CHECK FAILED. REVIEW DETAILS ABOVE.")
    print("=" * 80)

if __name__ == "__main__":
    run_validation()
