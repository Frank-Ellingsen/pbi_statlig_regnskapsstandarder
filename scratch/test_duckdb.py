import duckdb
import pandas as pd

con = duckdb.connect()
try:
    df = con.execute("SELECT * FROM read_csv('data/DimGlossary.csv', delim=';', header=true, quote='\"', escape='\"')").fetchdf()
    print("Direct duckdb read_csv succeeded:", len(df))
except Exception as e:
    print("Direct duckdb failed:", e)

try:
    df_pd = pd.read_csv('data/DimGlossary.csv', sep=';', encoding='utf-8')
    print("pandas read_csv succeeded:", len(df_pd))
    con.register('df_gloss', df_pd)
    cnt = con.execute("SELECT count(*) FROM df_gloss").fetchone()[0]
    print("Registered pandas df in duckdb count:", cnt)
except Exception as e:
    print("pandas failed:", e)
