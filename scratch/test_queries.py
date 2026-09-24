import os
import duckdb

data_dir = "data"
con = duckdb.connect()
tables = [
    "DimAccount", "DimDate", "DimForecastVersion", "DimGlossary", "DimOrganization",
    "DimPositionGroup", "DimProject", "DimStudyProgram",
    "FactAction", "FactBudget", "FactFTE", "FactForecast", "FactGL", "FactStudyPoints"
]
for tbl in tables:
    p = os.path.join(data_dir, f"{tbl}.csv").replace("\\", "/")
    con.execute(f"CREATE TABLE {tbl} AS SELECT * FROM read_csv('{p}', delim=';', header=true, encoding='utf-8')")

print("Testing all queries:")

# 1. Action query for sheet 04
q4 = """
SELECT TiltakID, Tiltaksbeskrivelse, AnsvarligRolle, FristDatoNokkel, ForventetEffekt, RealisertEffekt, Prioritet, Status
FROM FactAction
ORDER BY ForventetEffekt ASC
"""
res4 = con.execute(q4).fetchall()
print(f"Sheet 04 actions: {len(res4)} rows")

# 2. Action query for sheet 07
q7 = """
SELECT TiltakID, Tiltaksbeskrivelse, AnsvarligRolle, Avviksarsak, FristDatoNokkel, ForventetEffekt, RealisertEffekt, Prioritet, Status
FROM FactAction
ORDER BY TiltakID
"""
res7 = con.execute(q7).fetchall()
print(f"Sheet 07 actions: {len(res7)} rows")

# 3. Action query for DT Tiltak
q_dt4 = """
SELECT TiltakID, Tiltaksbeskrivelse, Konto, Organisasjonsnokkel, StartDatoNokkel, FristDatoNokkel, ForventetEffekt, RealisertEffekt, Prioritet, Status
FROM FactAction
ORDER BY TiltakID
"""
res_dt4 = con.execute(q_dt4).fetchall()
print(f"DT Tiltak actions: {len(res_dt4)} rows")

# 4. FTE query for DT Bemanning
q_fte = """
SELECT 
    p.Stillingsgruppenavn,
    p.Stillingskategori,
    round(sum(f.Aarsverk), 2) as AV,
    round(sum(f.FagligeAarsverk), 2) as FagligAV
FROM FactFTE f
JOIN DimPositionGroup p ON f.Stillingsgruppe = p.Stillingsgruppe
GROUP BY 1, 2
ORDER BY 3 DESC
"""
res_fte = con.execute(q_fte).fetchall()
print(f"DT Bemanning FTE: {len(res_fte)} rows")

# 5. EVM query for DT Prosjekt
q_evm = """
SELECT 
    p.Prosjekt,
    p.Prosjektnavn,
    p.Finansieringstype,
    round(sum(coalesce(b.BudsjettBelop, 0)), 2) as BAC,
    round(sum(coalesce(g.Belop_signert, 0)), 2) as AC,
    round(sum(coalesce(fc.ForecastBelop, 0)), 2) as EAC
FROM DimProject p
LEFT JOIN FactGL g ON p.Prosjekt = g.Prosjekt
LEFT JOIN FactBudget b ON p.Prosjekt = b.Prosjekt
LEFT JOIN FactForecast fc ON p.Prosjekt = fc.Prosjekt AND fc.Versjon = 'LE_2026'
GROUP BY 1, 2, 3
ORDER BY 6 DESC
"""
res_evm = con.execute(q_evm).fetchall()
print(f"DT Prosjekt EVM: {len(res_evm)} rows")

# 6. Study query for DT Studieaktivitet
q_sp = """
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
"""
res_sp = con.execute(q_sp).fetchall()
print(f"DT Study: {len(res_sp)} rows")

print("All queries passed successfully!")
