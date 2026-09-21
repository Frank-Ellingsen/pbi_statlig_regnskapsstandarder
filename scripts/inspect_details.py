import duckdb

con = duckdb.connect(":memory:")
tables = ["FactGL", "DimProject", "DimAccount", "FactFTE", "DimPositionGroup", "FactForecast", "FactBudget"]
for t in tables:
    con.execute(f"CREATE TABLE {t} AS SELECT * FROM read_csv('data/{t}.csv', delim=';', header=true, encoding='utf-8')")

print("=== INNTEKTER PER PROSJEKT I FACTGL ===")
print(con.execute("""
    SELECT g.Prosjekt, p.Prosjektnavn, p.Finansieringstype, p.Finansieringskilde, ROUND(SUM(-g.Belop_signert), 2) AS SumInntekt
    FROM FactGL g
    JOIN DimAccount a ON g.Konto = a.Konto
    JOIN DimProject p ON g.Prosjekt = p.Prosjekt
    WHERE a.Kontotype = 'Inntekt'
    GROUP BY g.Prosjekt, p.Prosjektnavn, p.Finansieringstype, p.Finansieringskilde
""").fetchdf())

print("\n=== STILLINGSGRUPPER I FACTFTE ===")
print(con.execute("""
    SELECT f.Stillingsgruppe, pg.Stillingsgruppenavn, pg.Stillingskategori, ROUND(SUM(f.Aarsverk), 2) AS SumAarsverk
    FROM FactFTE f
    LEFT JOIN DimPositionGroup pg ON f.Stillingsgruppe = pg.Stillingsgruppe
    GROUP BY f.Stillingsgruppe, pg.Stillingsgruppenavn, pg.Stillingskategori
""").fetchdf())

print("\n=== INNTEKTER I FACTFORECAST (LE_2026) ===")
print(con.execute("""
    SELECT f.Prosjekt, p.Prosjektnavn, p.Finansieringstype, ROUND(SUM(-f.ForecastBelop), 2) AS SumFCInntekt
    FROM FactForecast f
    JOIN DimAccount a ON f.Konto = a.Konto
    JOIN DimProject p ON f.Prosjekt = p.Prosjekt
    WHERE a.Kontotype = 'Inntekt' AND f.Versjon = 'LE_2026'
    GROUP BY f.Prosjekt, p.Prosjektnavn, p.Finansieringstype
""").fetchdf())
