import duckdb
import os

con = duckdb.connect(':memory:')
pkg = r'C:/Users/frank/Desktop/UIA/uia_powerbi_complete_forecast_model/uia_complete_controller_powerbi_excel_package'

csvs = [f for f in os.listdir(pkg) if f.endswith('.csv') and f != 'Relationships.csv']
for f in csvs:
    tbl = f.replace('.csv', '')
    p = f"{pkg}/{f}"
    con.execute(f"CREATE TABLE {tbl} AS SELECT * FROM read_csv('{p}', delim=';', header=true, encoding='utf-8')")

rels = con.execute(f"SELECT * FROM read_csv('{pkg}/Relationships.csv', delim=';', header=true, encoding='utf-8')").fetchall()
print("=== REFERENTIAL INTEGRITY CHECK ===")
for r in rels:
    fra_tbl, fra_col, til_tbl, til_col = r[0], r[1], r[2], r[3]
    dups = con.execute(f"SELECT COUNT(*) FROM (SELECT {fra_col}, COUNT(*) FROM {fra_tbl} GROUP BY {fra_col} HAVING COUNT(*) > 1)").fetchone()[0]
    orphans = con.execute(f"SELECT COUNT(*) FROM {til_tbl} t WHERE NOT EXISTS (SELECT 1 FROM {fra_tbl} f WHERE f.{fra_col} = t.{til_col})").fetchone()[0]
    status = 'PASS' if dups == 0 and orphans == 0 else 'FAIL'
    print(f"[{status}] {fra_tbl}.{fra_col} (1) -> {til_tbl}.{til_col} (*) | PK_DUPS: {dups}, ORPHANS: {orphans}")
