"""
validate_model.py
-----------------
Automated data model and referential integrity validator for UiA Controller Model.
Uses DuckDB to verify star-schema integrity, grain, and key reconciliations for all 22 relationships.
"""

import os
import duckdb
import pandas as pd

def run_validation():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    data_dir = os.path.abspath(data_dir)
    print("=" * 85)
    print("UiA CONTROLLER MODEL - DATA INTEGRITY & RECONCILIATION AUDIT")
    print(f"Data source path: {data_dir}")
    print("=" * 85)

    con = duckdb.connect(database=":memory:")

    csv_tables = [
        "DimAccount", "DimDate", "DimForecastVersion", "DimGlossary", "DimOrganization",
        "DimPositionGroup", "DimProject", "DimStudyProgram",
        "FactAction", "FactBudget", "FactFTE", "FactForecast", "FactGL", "FactStudyPoints"
    ]

    print("\n>>> LOADING CSV TABLES:")
    for tbl in csv_tables:
        csv_path = os.path.join(data_dir, f"{tbl}.csv").replace("\\", "/")
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Missing CSV file: {csv_path}")
        con.execute(f"""
            CREATE TABLE {tbl} AS 
            SELECT * FROM read_csv('{csv_path}', delim=';', header=true, encoding='utf-8')
        """)
        row_count = con.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        print(f"  Loaded {tbl:<25}: {row_count:>7,} rows")

    rel_path = os.path.join(data_dir, "Relationships.csv").replace("\\", "/")
    con.execute(f"CREATE TABLE Relationships AS SELECT * FROM read_csv('{rel_path}', delim=';', header=true, encoding='utf-8')")

    print("\n" + "-" * 85)
    print("1. REFERENTIAL INTEGRITY AUDIT (22 STAR SCHEMA RELATIONSHIPS)")
    print("-" * 85)

    rel_df = con.execute("SELECT * FROM Relationships").fetchdf()
    all_passed = True

    for _, row in rel_df.iterrows():
        fra_tbl = row["FraTabell"]
        fra_col = row["FraKolonne"]
        til_tbl = row["TilTabell"]
        til_col = row["TilKolonne"]

        # Check missing foreign keys (orphans)
        query = f"""
            SELECT COUNT(DISTINCT f.{til_col}) AS orphan_count
            FROM {til_tbl} f
            LEFT JOIN {fra_tbl} d ON f.{til_col} = d.{fra_col}
            WHERE d.{fra_col} IS NULL
        """
        orphans = con.execute(query).fetchone()[0]

        # Check primary key duplicates
        pk_dup_query = f"""
            SELECT COUNT(*) FROM (
                SELECT {fra_col}, COUNT(*) 
                FROM {fra_tbl} 
                GROUP BY {fra_col} 
                HAVING COUNT(*) > 1
            )
        """
        pk_dups = con.execute(pk_dup_query).fetchone()[0]

        status = "[PASSED]" if (orphans == 0 and pk_dups == 0) else "[FAILED]"
        if orphans > 0 or pk_dups > 0:
            all_passed = False

        print(f"  {status} {fra_tbl}.{fra_col} (1) -> {til_tbl}.{til_col} (*) | PK DUP: {pk_dups}, ORPHANS: {orphans}")

    print("\n" + "-" * 85)
    print("2. FINANCIAL RECONCILIATION SUMMARY (FULL SCALE DATASET)")
    print("-" * 85)

    gl_net = con.execute("SELECT ROUND(SUM(Belop_signert), 2) FROM FactGL").fetchone()[0]
    gl_count = con.execute("SELECT COUNT(*) FROM FactGL").fetchone()[0]
    print(f"  FactGL Transactions     : {gl_count:>7,} bilag | Netto: {gl_net:>14,.2f} NOK")

    b_sum = con.execute("SELECT ROUND(SUM(BudsjettBelop), 2) FROM FactBudget").fetchone()[0]
    b_count = con.execute("SELECT COUNT(*) FROM FactBudget").fetchone()[0]
    print(f"  FactBudget Lines        : {b_count:>7,} linjer | Netto: {b_sum:>14,.2f} NOK")

    fc_versions = con.execute("SELECT Versjon, ROUND(SUM(ForecastBelop), 2) FROM FactForecast GROUP BY Versjon ORDER BY Versjon").fetchall()
    for v, s in fc_versions:
        print(f"  FactForecast {v:<10} : {s:>20,.2f} NOK")

    act_forv = con.execute("SELECT ROUND(SUM(ForventetEffekt), 2) FROM FactAction").fetchone()[0]
    act_real = con.execute("SELECT ROUND(SUM(RealisertEffekt), 2) FROM FactAction").fetchone()[0]
    print(f"  FactAction Savings      : Forventet: {act_forv:>14,.2f} NOK | Realisert: {act_real:>14,.2f} NOK")

    fte_sum = con.execute("SELECT ROUND(SUM(Aarsverk), 2), ROUND(SUM(FagligeAarsverk), 2) FROM FactFTE").fetchone()
    print(f"  FactFTE Total           : {fte_sum[0]:>10,.2f} årsverk (Faglige: {fte_sum[1]:>10,.2f})")

    sp_sum = con.execute("SELECT ROUND(SUM(PlanlagteStudiepoeng), 1), ROUND(SUM(AvlagteStudiepoeng), 1), ROUND(SUM(SPE60), 2) FROM FactStudyPoints").fetchone()
    print(f"  FactStudyPoints         : Planlagt: {sp_sum[0]:>10,.1f} SP | Avlagt: {sp_sum[1]:>10,.1f} SP | SPE60: {sp_sum[2]:>10,.2f}")

    gloss_count = con.execute("SELECT COUNT(*), COUNT(DISTINCT BegrepID), COUNT(DISTINCT Begrep), COUNT(DISTINCT Kategori) FROM DimGlossary").fetchone()
    print(f"  DimGlossary Terms       : {gloss_count[0]:>7,} definisjoner | PK Unike: {gloss_count[1]} | Kategorier: {gloss_count[3]}")
    if gloss_count[0] != gloss_count[1] or gloss_count[0] != gloss_count[2]:
        all_passed = False
        print("  [FAILED] DimGlossary contains duplicate BegrepID or Begrep keys!")

    print("\n" + "=" * 85)
    if all_passed:
        print("ALL 22 RELATIONSHIPS PASSED REFERENTIAL INTEGRITY AUDIT WITHOUT ERRORS.")
    else:
        print("REFERENTIAL INTEGRITY AUDIT ENCOUNTERED FAILURES.")
    print("=" * 85)

if __name__ == "__main__":
    run_validation()
