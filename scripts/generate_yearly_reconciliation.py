"""
generate_yearly_reconciliation.py
---------------------------------
Generates realistic, 100% reconciled 12-month data for Universitetet i Agder (UiA)
Project Controlling & Earned Value (EV) Analysis.

Targets:
- Total Revenue: 1,433.0 MNOK (Govt: 1,234.0, Research: 123.0, Other: 76.0)
- Total Expenses: 1,444.0 MNOK (Personnel: 944.0, Opex: 340.0, Capex: 160.0)
- Net Operating Result: -11.0 MNOK (Underskudd som dekkes av oppspart bevilgningskapital/Note 15)
- Benchmarks: Capex 11.1-11.2%, Opex 23.7%, Personnel 65.7-65.9%
- EVM Parameters:
  * BAC (Budget at Completion): 1,433.0 MNOK
  * EAC (Estimate at Completion): 1,444.0 MNOK
  * ETC (Estimate to Complete per Nov): 100.0 MNOK
  * AC per Nov (M11): 1,344.0 MNOK
  * EV per Nov (M11): 1,276.8 MNOK -> CPI = 0.950
  * PV per Nov (M11): 1,387.8 MNOK -> SPI = 0.920
  * Year-End EV delivered: 1,344.0 MNOK
  * Year-End Final AC: 1,444.0 MNOK
  * VAC (BAC - EAC): -11.0 MNOK
"""

import os
import pandas as pd
import numpy as np

months_data = [
    # Mnd, Navn, Govt, Research, Other, Pers, Opex, Capex, PV, EV, AC
    (1,  "Januar",    102.8,   8.5,  5.8,  76.5, 27.5, 10.5, 121.0, 111.0, 114.5),
    (2,  "Februar",   102.8,   9.2,  7.5,  77.0, 26.5, 11.0, 122.0, 112.0, 114.5),
    (3,  "Mars",      102.8,  10.1,  6.2,  78.5, 30.0, 12.5, 128.0, 118.0, 121.0),
    (4,  "April",     102.8,  10.5,  6.4,  78.0, 28.5, 13.0, 127.0, 117.0, 119.5),
    (5,  "Mai",       102.9,  11.2,  6.5,  79.5, 30.5, 14.0, 131.0, 120.0, 124.0),
    (6,  "Juni",      102.9,  11.5,  6.8, 116.0, 33.0, 16.0, 145.0, 133.0, 165.0), # Feriepenger
    (7,  "Juli",      102.8,   6.2,  4.2,  60.5, 20.0,  9.0,  95.0,  88.0,  89.5), # Sommerferie
    (8,  "August",    102.8,   9.8,  6.6,  77.0, 27.0, 14.0, 123.0, 113.0, 118.0), # Semesterstart
    (9,  "September", 102.9,  11.4,  8.2,  79.5, 31.5, 15.0, 132.0, 122.0, 126.0), # Høstsemester
    (10, "Oktober",  102.8,  11.8,  6.5,  79.0, 31.5, 16.0, 132.0, 121.5, 126.5),
    (11, "November", 102.8,  11.6,  6.0,  78.5, 31.0, 16.0, 131.8, 121.3, 125.5), # T3 Cutoff
    (12, "Desember", 102.9,  11.2,  5.3,  64.0, 23.0, 13.0, 120.0,  67.2, 100.0), # Årsavslutning (ETC=100)
]

cols = [
    "MndNr", "Maaned", "StatligBevilgning", "Forskningsinntekter", "AndreInntekter",
    "Lonnskostnader", "Driftskostnader", "InvesteringerCapex", "PlanlagtVerdi_PV", "OpptjentVerdi_EV", "FaktiskKostnad_AC"
]

df = pd.DataFrame(months_data, columns=cols)

# Calculate monthly totals
df["TotalInntekt"] = (df["StatligBevilgning"] + df["Forskningsinntekter"] + df["AndreInntekter"]).round(1)
df["TotalKostnad"] = (df["Lonnskostnader"] + df["Driftskostnader"] + df["InvesteringerCapex"]).round(1)
df["NettoResultat"] = (df["TotalInntekt"] - df["TotalKostnad"]).round(1)

# Cumulative series
df["Kumulativ_Inntekt"] = df["TotalInntekt"].cumsum().round(1)
df["Kumulativ_Kostnad"] = df["TotalKostnad"].cumsum().round(1)
df["Kumulativ_PV"] = df["PlanlagtVerdi_PV"].cumsum().round(1)
df["Kumulativ_EV"] = df["OpptjentVerdi_EV"].cumsum().round(1)
df["Kumulativ_AC"] = df["FaktiskKostnad_AC"].cumsum().round(1)

df["Kumulativ_CPI"] = (df["Kumulativ_EV"] / df["Kumulativ_AC"]).round(3)
df["Kumulativ_SPI"] = (df["Kumulativ_EV"] / df["Kumulativ_PV"]).round(3)
df["Kumulativ_CV"] = (df["Kumulativ_EV"] - df["Kumulativ_AC"]).round(1)
df["Kumulativ_SV"] = (df["Kumulativ_EV"] - df["Kumulativ_PV"]).round(1)

# Print Verification
print("="*65)
print("UNIVERSITETET I AGDER (UIA) - 100% AVSTEMT HELÅRSREGNSKAP")
print("="*65)
print(f"Statlig bevilgning:      {df['StatligBevilgning'].sum():8.1f} MNOK (1 234,0)")
print(f"Forskningsinntekter:     {df['Forskningsinntekter'].sum():8.1f} MNOK   (123,0)")
print(f"Andre inntekter:          {df['AndreInntekter'].sum():8.1f} MNOK    (76,0)")
print(f"TOTAL INNTEKT (BAC):     {df['TotalInntekt'].sum():8.1f} MNOK (1 433,0)")
print("-" * 65)
print(f"Lønnskostnader:          {df['Lonnskostnader'].sum():8.1f} MNOK   (944,0)")
print(f"Driftskostnader:         {df['Driftskostnader'].sum():8.1f} MNOK   (340,0)")
print(f"Investeringer (Capex):   {df['InvesteringerCapex'].sum():8.1f} MNOK   (160,0)")
print(f"TOTAL KOSTNAD (EAC/AC):  {df['TotalKostnad'].sum():8.1f} MNOK (1 444,0)")
print("-" * 65)
print(f"NETTO DRIFTSRESULTAT:    {df['NettoResultat'].sum():8.1f} MNOK   (-11,0)")
print("-" * 65)
print(f"Capex % av inntekt:      {(df['InvesteringerCapex'].sum()/df['TotalInntekt'].sum())*100:6.1f}% (Benchmark: 11.1-11.2%)")
print(f"Opex % av inntekt:       {(df['Driftskostnader'].sum()/df['TotalInntekt'].sum())*100:6.1f}% (Benchmark: 23.7%)")
print(f"Lønn % av inntekt:       {(df['Lonnskostnader'].sum()/df['TotalInntekt'].sum())*100:6.1f}% (Benchmark: 65.7-65.9%)")
print("-" * 65)
print("EVM STATUS PER T3 / NOVEMBER (M11 CUTOFF):")
row11 = df.iloc[10]
ac_nov = row11['Kumulativ_AC']
ev_nov = row11['Kumulativ_EV']
pv_nov = row11['Kumulativ_PV']
cpi_nov = ev_nov / ac_nov
spi_nov = ev_nov / pv_nov
etc_dec = df.iloc[11]['TotalKostnad']
eac_tot = ac_nov + etc_dec
print(f"Faktisk kostnad YTD (AC):{ac_nov:8.1f} MNOK (1 344,0)")
print(f"Opptjent verdi YTD (EV): {ev_nov:8.1f} MNOK (1 276,8)")
print(f"Planlagt verdi YTD (PV): {pv_nov:8.1f} MNOK (1 387,8)")
print(f"Kostnadsindeks (CPI):    {cpi_nov:8.2f}      (0,95)")
print(f"Fremdriftsindeks (SPI):  {spi_nov:8.2f}      (0,92)")
print(f"Gjenstående rest (ETC):  {etc_dec:8.1f} MNOK   (100,0)")
print(f"Sluttkostnad (EAC):      {eac_tot:8.1f} MNOK (1 444,0)")
print("-" * 65)
print("EVM STATUS HELE ÅRET (12 MND FULLFØRT):")
print(f"Budsjett ved slutt (BAC):{df['TotalInntekt'].sum():8.1f} MNOK (1 433,0)")
print(f"Sluttkostnad (EAC / AC): {df['TotalKostnad'].sum():8.1f} MNOK (1 444,0)")
print(f"Fullført verdi (EV):     {df['Kumulativ_EV'].iloc[-1]:8.1f} MNOK (1 344,0)")
print(f"Sluttavvik (VAC):        {df['TotalInntekt'].sum() - df['TotalKostnad'].sum():8.1f} MNOK   (-11,0)")
print("="*65)

# Save to CSV
csv_path = r"C:\Users\frank\Desktop\UIA\uia_powerbi_complete_forecast_model\data\FactYearlyReconciliation.csv"
df.to_csv(csv_path, index=False, sep=";", decimal=",", encoding="utf-8-sig")

# Also save a copy in Use Case/case data for convenience
case_data_csv = r"C:\Users\frank\Desktop\UIA\Use Case\case data\FactYearlyReconciliation.csv"
df.to_csv(case_data_csv, index=False, sep=";", decimal=",", encoding="utf-8-sig")

print(f"Lagret oppdatert datasett til data/ og Use Case/case data/")
