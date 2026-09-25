import re
import shutil

# 1. Create a backup
shutil.copy('index.html', 'index.html.bak')
print("Created index.html.bak")

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Verify initial presence of targets
print("Initial checks:")
print("  modelData presence:", "const modelData" in content)
print("  page_01 presence:", "page_01:" in content)
print("  page_03 presence:", "page_03:" in content)
print("  page_04 presence:", "page_04:" in content)

# 2. Update line 1318 (table header explanation)
old_1318 = "<td>[Forecast aarsbelop] - [Aarsbudsjett] (Merforbruk: +26,05 MNOK)</td>"
new_1318 = "<td>[Forecast aarsbelop] - [Aarsbudsjett] (Merforbruk: -14,62 MNOK / Sluttavvik VAC)</td>"
if old_1318 in content:
    content = content.replace(old_1318, new_1318)
    print("Replaced line 1318 table note")

# 3. Update modelData
old_model_data = """const modelData = {
  regnskapYTD: 10617128.19,
  budsjettYTD: 10747732.82,
  avvikYTD: -130604.63,
  aarsbudsjett: 10747732.82,
  forecastAar: 36793524.31,
  forecastAvvik: 26045791.49,
  aarsverk: 1285.93,
  fagligeAarsverk: 661.77,
  studenter: 6490,
  avlagteSP: 336945.4,
  spe60: 5615.74,
  spMaaloppnaelse: 86.38,
  boaInntekter: 25678288.24,
  nfrInntekter: 12903450.00,
  euInntekter: 7425100.00,
  antallTiltak: 16,
  aapneTiltak: 12,
  forsinkedeTiltak: 4,
  forventetTiltak: -10005000.00,
  realisertTiltak: -5562081.66,
  tiltakGrad: 55.59,
  forecastEtterTiltak: 26788524.31,
  restavvikEtterTiltak: 16040791.49
};"""

new_model_data = """const modelData = {
  regnskapYTD: 68381200.00,
  budsjettYTD: 54560000.00,
  avvikYTD: -13821200.00,
  aarsbudsjett: 81840000.00,
  forecastAar: 96460000.00,
  forecastAvvik: -14620000.00,
  aarsverk: 1285.93,
  fagligeAarsverk: 661.77,
  studenter: 6490,
  avlagteSP: 336945.4,
  spe60: 2589.60,
  bfeInntekt: 176012760.00,
  spMaaloppnaelse: 86.38,
  boaInntekter: 20460000.00,
  boaPortefolje: 61500000.00,
  tdiBudsjett: 20200000.00,
  nfrInntekter: 11450000.00,
  euInntekter: 6820000.00,
  lonnskostnader: 50970000.00,
  lonnsandel: 78.31,
  konto2080Avsetning: -4800000.00,
  avsetningsgradF05: 8.96,
  antallTiltak: 7,
  aapneTiltak: 4,
  forsinkedeTiltak: 1,
  forventetTiltak: -10250000.00,
  realisertTiltak: -4850000.00,
  tiltakGrad: 47.32,
  forecastEtterTiltak: 86210000.00,
  restavvikEtterTiltak: 4370000.00
};"""

if old_model_data in content:
    content = content.replace(old_model_data, new_model_data)
    print("Updated modelData")
else:
    print("WARNING: old_model_data exact match failed, using regex")
    content = re.sub(r'const modelData\s*=\s*\{.*?\};', new_model_data, content, flags=re.DOTALL)

# 4. Update page_01 KPIs and content
old_page_01_kpis = """    kpis: [
      { title: "Regnskap YTD", val: "10,62 M", unit: "NOK", badge: "-1,2% vs Budsjett", badgeCls: "variance-favorable", sub: "Budsjett YTD: 10,75 M" },
      { title: "Avvik YTD", val: "-130 k", unit: "NOK", badge: "Mindreforbruk", badgeCls: "variance-favorable", sub: "Netto gunstig stilling YTD" },
      { title: "Forecast årsbeløp (LE)", val: "36,79 M", unit: "NOK", badge: "EAC", badgeCls: "variance-info", sub: "Forventet helårsforbruk" },
      { title: "Forecastavvik", val: "+26,05 M", unit: "NOK", badge: "+242% vs Budsjett", badgeCls: "variance-unfavorable", sub: "Forventet merforbruk før tiltak" },
      { title: "Årsverk", val: "1 285,9", unit: "FTE", badge: "51,5% Vitenskapelig", badgeCls: "variance-info", sub: "Faglige årsverk: 661,8" }
    ],"""

new_page_01_kpis = """    kpis: [
      { title: "Regnskap YTD", val: "68,38 M", unit: "NOK", badge: "+25,3% vs Budsjett", badgeCls: "variance-unfavorable", sub: "Budsjett YTD: 54,56 M" },
      { title: "Avvik YTD", val: "-13,82 M", unit: "NOK", badge: "Merforbruk YTD", badgeCls: "variance-unfavorable", sub: "M01-M08 Faktisk avvik" },
      { title: "Forecast årsbeløp (LE)", val: "96,46 M", unit: "NOK", badge: "EAC Slutt", badgeCls: "variance-unfavorable", sub: "Forventet helårsforbruk" },
      { title: "Forecastavvik", val: "-14,62 M", unit: "NOK", badge: "Budsjettbrudd M10", badgeCls: "variance-unfavorable", sub: "Vedtatt ramme (BAC): 81,84 M" },
      { title: "Årsverk", val: "1 285,9", unit: "FTE", badge: "51,5% Vitenskapelig", badgeCls: "variance-info", sub: "Faglige årsverk: 661,8" }
    ],"""

if old_page_01_kpis in content:
    content = content.replace(old_page_01_kpis, new_page_01_kpis)
    print("Updated page_01 KPIs")

# Update page_01 SVG chart data
old_page_01_chart = """            ${generateLineChartSVG([
              { name: "Regnskap", color: "#38bdf8", data: [0.8, 1.7, 2.6, 3.5, 4.4, 5.3, 6.2, 7.1, 8.0, 8.9, 9.8, 10.6] },
              { name: "Budsjett", color: "#94a3b8", dashed: true, data: [0.9, 1.8, 2.7, 3.6, 4.5, 5.4, 6.3, 7.2, 8.1, 9.0, 9.9, 10.7] },
              { name: "Forecast (LE)", color: "#f59e0b", data: [0.8, 1.7, 2.6, 4.2, 7.8, 11.5, 15.6, 20.1, 24.5, 28.9, 32.8, 36.8] }
            ])}"""

new_page_01_chart = """            ${generateLineChartSVG([
              { name: "Regnskap", color: "#38bdf8", data: [8.5, 17.1, 25.6, 34.2, 42.7, 51.3, 59.8, 68.38] },
              { name: "Budsjett", color: "#94a3b8", dashed: true, data: [6.82, 13.64, 20.46, 27.28, 34.10, 40.92, 47.74, 54.56, 61.38, 68.20, 75.02, 81.84] },
              { name: "Forecast (LE)", color: "#f59e0b", data: [8.5, 17.1, 25.6, 34.2, 42.7, 51.3, 59.8, 68.38, 75.4, 82.5, 89.5, 96.46] }
            ])}"""

if old_page_01_chart in content:
    content = content.replace(old_page_01_chart, new_page_01_chart)
    print("Updated page_01 chart data")

# Update page_01 Drivers
old_page_01_drivers = """            ${generateBarChartSVG([
              { label: "Lønnskostnader (UF/TA)", val: 18.2, color: "#ef4444" },
              { label: "Andre driftskostnader", val: 5.4, color: "#f59e0b" },
              { label: "Av- og nedskrivninger", val: 2.1, color: "#f59e0b" },
              { label: "Inntektsbortfall (BOA)", val: 0.3, color: "#10b981" }
            ], "MNOK")}"""

new_page_01_drivers = """            ${generateBarChartSVG([
              { label: "Lønnskostnader (UF/TA)", val: 9.8, color: "#ef4444" },
              { label: "Andre driftskostnader", val: 3.2, color: "#f59e0b" },
              { label: "Av- og nedskrivninger", val: 1.1, color: "#f59e0b" },
              { label: "Inntektsbortfall / prosjektavvik", val: 0.52, color: "#10b981" }
            ], "MNOK")}"""

if old_page_01_drivers in content:
    content = content.replace(old_page_01_drivers, new_page_01_drivers)
    print("Updated page_01 drivers")

# Update page_01 bottom summary strip
old_page_01_strip = """      <!-- Bottom Summary Formula Strip -->
      <div class="formula-summary-strip">
        <div class="formula-card">
          <div class="formula-step">1. Forecast før tiltak</div>
          <div class="formula-val" style="color:#ef4444;">36,79 MNOK</div>
          <div style="font-size:11px; color:var(--text-muted);">Ujustert helårsestimat</div>
        </div>
        <div class="formula-card">
          <div class="formula-step">2. Identifisert tiltakseffekt</div>
          <div class="formula-val" style="color:#10b981;">-10,01 MNOK</div>
          <div style="font-size:11px; color:var(--text-muted);">16 vedtatte tiltak</div>
        </div>
        <div class="formula-card">
          <div class="formula-step">3. Netto prognose etter tiltak</div>
          <div class="formula-val" style="color:#38bdf8;">26,79 MNOK</div>
          <div style="font-size:11px; color:var(--text-muted);">[Forecast] + [Tiltak]</div>
        </div>
        <div class="formula-card">
          <div class="formula-step">4. Gjenstående restavvik</div>
          <div class="formula-val" style="color:#f59e0b;">+16,04 MNOK</div>
          <div style="font-size:11px; color:var(--text-muted);">Restgap mot årsbudsjett</div>
        </div>
      </div>"""

new_page_01_strip = """      <!-- Bottom Summary Formula Strip -->
      <div class="formula-summary-strip">
        <div class="formula-card">
          <div class="formula-step">1. Forecast før tiltak</div>
          <div class="formula-val" style="color:#ef4444;">96,46 MNOK</div>
          <div style="font-size:11px; color:var(--text-muted);">Ujustert helårsestimat (EAC)</div>
        </div>
        <div class="formula-card">
          <div class="formula-step">2. Identifisert tiltakseffekt</div>
          <div class="formula-val" style="color:#10b981;">-10,25 MNOK</div>
          <div style="font-size:11px; color:var(--text-muted);">7 omstillingstiltak</div>
        </div>
        <div class="formula-card">
          <div class="formula-step">3. Netto prognose etter tiltak</div>
          <div class="formula-val" style="color:#38bdf8;">86,21 MNOK</div>
          <div style="font-size:11px; color:var(--text-muted);">[Forecast] + [Tiltak]</div>
        </div>
        <div class="formula-card">
          <div class="formula-step">4. Gjenstående restavvik</div>
          <div class="formula-val" style="color:#f59e0b;">+4,37 MNOK</div>
          <div style="font-size:11px; color:var(--text-muted);">Restgap mot årsbudsjett (81,84 M)</div>
        </div>
      </div>"""

if old_page_01_strip in content:
    content = content.replace(old_page_01_strip, new_page_01_strip)
    print("Updated page_01 summary strip")

# 5. Update page_03 (Universitetsdirektør & Ledelse)
old_page_03_kpis = """    kpis: [
      { title: "Årsbudsjett (Institusjonen)", val: "10,75 M", unit: "NOK", badge: "BAC Ramme", badgeCls: "variance-info", sub: "Netto bevilgningsramme" },
      { title: "Helårsprognose (LE)", val: "36,79 M", unit: "NOK", badge: "EAC Slutt", badgeCls: "variance-unfavorable", sub: "Gjeldende helårsestimat" },
      { title: "Prognoseavvik", val: "+26,05 M", unit: "NOK", badge: "Risikogap", badgeCls: "variance-unfavorable", sub: "Forventet merforbruk før tiltak" },
      { title: "Årsverk totalt", val: "1 285,9", unit: "FTE", badge: "Hele institusjonen", badgeCls: "variance-info", sub: "UF: 661,8 | TA: 624,1" },
      { title: "BOA-finansieringsandel", val: "1,20%", unit: "Andel", badge: "Mål: 2,5%", badgeCls: "variance-neutral", sub: "BOA inntekter: 25,68 M" }
    ],"""

new_page_03_kpis = """    kpis: [
      { title: "Årsbudsjett (Institusjonen)", val: "81,84 M", unit: "NOK", badge: "BAC Ramme", badgeCls: "variance-info", sub: "Netto bevilgningsramme" },
      { title: "Helårsprognose (LE)", val: "96,46 M", unit: "NOK", badge: "EAC Slutt", badgeCls: "variance-unfavorable", sub: "Gjeldende helårsestimat" },
      { title: "Prognoseavvik", val: "-14,62 M", unit: "NOK", badge: "Budsjettbrudd M10", badgeCls: "variance-unfavorable", sub: "Forventet merforbruk før tiltak" },
      { title: "Årsverk totalt", val: "1 285,9", unit: "FTE", badge: "Hele institusjonen", badgeCls: "variance-info", sub: "UF: 661,8 | TA: 624,1" },
      { title: "BOA Portefølje", val: "61,50 M", unit: "NOK", badge: "20,46 M påløpt", badgeCls: "variance-info", sub: "TDI-budsjett 20,20 M (6 prosjekter)" }
    ],"""

if old_page_03_kpis in content:
    content = content.replace(old_page_03_kpis, new_page_03_kpis)
    print("Updated page_03 KPIs")

# page_03 line chart
old_page_03_chart = """            ${generateLineChartSVG([
              { name: "Prognose helår", color: "#38bdf8", data: [10.75, 15.2, 22.4, 28.1, 35.47, 35.7, 35.96, 36.2, 36.5, 36.79] },
              { name: "Vedtatt budsjettramme", color: "#94a3b8", dashed: true, data: [10.75, 10.75, 10.75, 10.75, 10.75, 10.75, 10.75, 10.75, 10.75, 10.75] }
            ])}"""

new_page_03_chart = """            ${generateLineChartSVG([
              { name: "Prognose helår", color: "#38bdf8", data: [81.84, 84.50, 87.20, 89.90, 92.50, 93.80, 95.10, 96.46] },
              { name: "Vedtatt budsjettramme", color: "#94a3b8", dashed: true, data: [81.84, 81.84, 81.84, 81.84, 81.84, 81.84, 81.84, 81.84] }
            ])}"""

if old_page_03_chart in content:
    content = content.replace(old_page_03_chart, new_page_03_chart)
    print("Updated page_03 chart")

# page_03 table
old_page_03_table = """            <tbody>
              <tr>
                <td>Handelshøyskolen</td>
                <td class="num">3 240 000</td>
                <td class="num">3 180 000</td>
                <td class="num">11 640 000</td>
                <td class="num" style="color:#ef4444;">+8 400 000</td>
                <td><span class="status-pill rag-red">🔴 Rød (>5%)</span></td>
                <td class="num">342,0</td>
                <td class="num">8 450 000</td>
                <td class="num" style="color:#38bdf8;">8 240 000</td>
              </tr>
              <tr>
                <td>Fakultet for teknologi og realfag</td>
                <td class="num">4 120 000</td>
                <td class="num">4 090 000</td>
                <td class="num">13 920 000</td>
                <td class="num" style="color:#ef4444;">+9 800 000</td>
                <td><span class="status-pill rag-red">🔴 Rød (>5%)</span></td>
                <td class="num">410,5</td>
                <td class="num">11 820 000</td>
                <td class="num" style="color:#38bdf8;">11 120 000</td>
              </tr>
              <tr>
                <td>Fakultet for samfunnsvitenskap</td>
                <td class="num">1 850 000</td>
                <td class="num">1 840 000</td>
                <td class="num">6 050 000</td>
                <td class="num" style="color:#ef4444;">+4 200 000</td>
                <td><span class="status-pill rag-red">🔴 Rød (>5%)</span></td>
                <td class="num">265,0</td>
                <td class="num">3 110 000</td>
                <td class="num" style="color:#38bdf8;">4 850 000</td>
              </tr>
              <tr>
                <td>Fellesområde & administrasjon</td>
                <td class="num">1 537 733</td>
                <td class="num">1 507 128</td>
                <td class="num">5 183 524</td>
                <td class="num" style="color:#f59e0b;">+3 645 791</td>
                <td><span class="status-pill rag-red">🔴 Rød (>5%)</span></td>
                <td class="num">268,4</td>
                <td class="num">2 298 288</td>
                <td class="num" style="color:#38bdf8;">2 578 524</td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td>Totalt institusjonen</td>
                <td class="num">10 747 733 kr</td>
                <td class="num">10 617 128 kr</td>
                <td class="num">36 793 524 kr</td>
                <td class="num" style="color:#ef4444;">+26 045 791 kr</td>
                <td><span class="status-pill rag-red">🔴 Rød (>5%)</span></td>
                <td class="num">1 285,9</td>
                <td class="num">25 678 288 kr</td>
                <td class="num" style="color:#38bdf8;">26 788 524 kr</td>
              </tr>
            </tfoot>"""

new_page_03_table = """            <tbody>
              <tr>
                <td>Handelshøyskolen</td>
                <td class="num">24 680 000</td>
                <td class="num">20 620 000</td>
                <td class="num">29 100 000</td>
                <td class="num" style="color:#ef4444;">-4 420 000</td>
                <td><span class="status-pill rag-red">🔴 Rød (&gt;5%)</span></td>
                <td class="num">342,0</td>
                <td class="num">6 740 000</td>
                <td class="num" style="color:#38bdf8;">25 990 000</td>
              </tr>
              <tr>
                <td>Fakultet for teknologi og realfag</td>
                <td class="num">31 380 000</td>
                <td class="num">26 210 000</td>
                <td class="num">36 980 000</td>
                <td class="num" style="color:#ef4444;">-5 600 000</td>
                <td><span class="status-pill rag-red">🔴 Rød (&gt;5%)</span></td>
                <td class="num">410,5</td>
                <td class="num">9 440 000</td>
                <td class="num" style="color:#38bdf8;">33 070 000</td>
              </tr>
              <tr>
                <td>Fakultet for samfunnsvitenskap</td>
                <td class="num">14 090 000</td>
                <td class="num">11 780 000</td>
                <td class="num">16 610 000</td>
                <td class="num" style="color:#ef4444;">-2 520 000</td>
                <td><span class="status-pill rag-red">🔴 Rød (&gt;5%)</span></td>
                <td class="num">265,0</td>
                <td class="num">2 480 000</td>
                <td class="num" style="color:#38bdf8;">14 840 000</td>
              </tr>
              <tr>
                <td>Fellesområde & administrasjon</td>
                <td class="num">11 690 000</td>
                <td class="num">9 771 200</td>
                <td class="num">13 770 000</td>
                <td class="num" style="color:#f59e0b;">-2 080 000</td>
                <td><span class="status-pill rag-red">🔴 Rød (&gt;5%)</span></td>
                <td class="num">268,4</td>
                <td class="num">1 800 000</td>
                <td class="num" style="color:#38bdf8;">12 310 000</td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td>Totalt institusjonen</td>
                <td class="num">81 840 000 kr</td>
                <td class="num">68 381 200 kr</td>
                <td class="num">96 460 000 kr</td>
                <td class="num" style="color:#ef4444;">-14 620 000 kr</td>
                <td><span class="status-pill rag-red">🔴 Rød (&gt;5%)</span></td>
                <td class="num">1 285,9</td>
                <td class="num">20 460 000 kr</td>
                <td class="num" style="color:#38bdf8;">86 210 000 kr</td>
              </tr>
            </tfoot>"""

if old_page_03_table in content:
    content = content.replace(old_page_03_table, new_page_03_table)
    print("Updated page_03 table")

# 6. Update page_04 (Universitetsstyret)
old_page_04_kpis = """    kpis: [
      { title: "Totalbudsjett", val: "10,75 M", unit: "NOK", badge: "Vedtatt ramme", badgeCls: "variance-info", sub: "Bevilgning + BOA" },
      { title: "Forventet helårsresultat", val: "36,79 M", unit: "NOK", badge: "LE_2026", badgeCls: "variance-unfavorable", sub: "Merforbruk: +26,05 M" },
      { title: "Forventet avvik %", val: "+242,3%", unit: "Avvik", badge: "Høy risiko", badgeCls: "variance-unfavorable", sub: "Før innregning av tiltak" },
      { title: "Studiepoeng måloppnåelse", val: "86,4%", unit: "Mål", badge: "336 945 / 390 095", badgeCls: "variance-neutral", sub: "SPE60: 5 615,7" },
      { title: "Eksternfinansiering (BOA)", val: "25,68 M", unit: "NOK", badge: "1,20% andel", badgeCls: "variance-favorable", sub: "NFR: 12,9M | EU: 7,4M" }
    ],"""

new_page_04_kpis = """    kpis: [
      { title: "Totalbudsjett", val: "81,84 M", unit: "NOK", badge: "Vedtatt ramme (BAC)", badgeCls: "variance-info", sub: "Bevilgning & ramme 2026" },
      { title: "Forventet helårsresultat", val: "96,46 M", unit: "NOK", badge: "LE_2026 (-14,62 M)", badgeCls: "variance-unfavorable", sub: "Sluttprognose EAC" },
      { title: "Forventet avvik %", val: "-17,9%", unit: "Avvik", badge: "Budsjettbrudd M10", badgeCls: "variance-unfavorable", sub: "Før innregning av tiltak" },
      { title: "Studiepoeng produksjon", val: "2 589,6", unit: "SPE60", badge: "176,01 Mkr BFE", badgeCls: "variance-info", sub: "336 945 ECTS avlagt" },
      { title: "Eksternfinansiering (BOA)", val: "61,50 M", unit: "NOK", badge: "20,46 M påløpt", badgeCls: "variance-info", sub: "6 prosjekter (NFR/EU/EVU)" }
    ],"""

if old_page_04_kpis in content:
    content = content.replace(old_page_04_kpis, new_page_04_kpis)
    print("Updated page_04 KPIs")

# page_04 risikotabell
old_page_04_table = """              <tbody>
                <tr>
                  <td>Fak. for teknologi og realfag</td>
                  <td class="num" style="color:#ef4444;">+9 800 000</td>
                  <td class="num" style="color:#10b981;">-2 800 000</td>
                  <td class="num" style="color:#f59e0b;">+7 000 000</td>
                  <td><span class="status-pill rag-red">🔴 Høy risiko</span></td>
                </tr>
                <tr>
                  <td>Handelshøyskolen</td>
                  <td class="num" style="color:#ef4444;">+8 400 000</td>
                  <td class="num" style="color:#10b981;">-3 400 000</td>
                  <td class="num" style="color:#f59e0b;">+5 000 000</td>
                  <td><span class="status-pill rag-red">🔴 Høy risiko</span></td>
                </tr>
                <tr>
                  <td>Fak. for samfunnsvitenskap</td>
                  <td class="num" style="color:#f59e0b;">+4 200 000</td>
                  <td class="num" style="color:#10b981;">-1 500 000</td>
                  <td class="num" style="color:#f59e0b;">+2 700 000</td>
                  <td><span class="status-pill rag-amber">🟡 Moderat risiko</span></td>
                </tr>
                <tr>
                  <td>Fellesområde / Adm.</td>
                  <td class="num" style="color:#f59e0b;">+3 645 791</td>
                  <td class="num" style="color:#10b981;">-2 305 000</td>
                  <td class="num" style="color:#10b981;">+1 340 791</td>
                  <td><span class="status-pill rag-green">🟢 Lav risiko</span></td>
                </tr>
              </tbody>"""

new_page_04_table = """              <tbody>
                <tr>
                  <td>Fak. for teknologi og realfag</td>
                  <td class="num" style="color:#ef4444;">-5 600 000</td>
                  <td class="num" style="color:#10b981;">-3 910 000</td>
                  <td class="num" style="color:#f59e0b;">+1 690 000</td>
                  <td><span class="status-pill rag-red">🔴 Høy risiko</span></td>
                </tr>
                <tr>
                  <td>Handelshøyskolen</td>
                  <td class="num" style="color:#ef4444;">-4 420 000</td>
                  <td class="num" style="color:#10b981;">-3 110 000</td>
                  <td class="num" style="color:#f59e0b;">+1 310 000</td>
                  <td><span class="status-pill rag-red">🔴 Høy risiko</span></td>
                </tr>
                <tr>
                  <td>Fak. for samfunnsvitenskap</td>
                  <td class="num" style="color:#f59e0b;">-2 520 000</td>
                  <td class="num" style="color:#10b981;">-1 770 000</td>
                  <td class="num" style="color:#f59e0b;">+750 000</td>
                  <td><span class="status-pill rag-amber">🟡 Moderat risiko</span></td>
                </tr>
                <tr>
                  <td>Fellesområde / Adm.</td>
                  <td class="num" style="color:#f59e0b;">-2 080 000</td>
                  <td class="num" style="color:#10b981;">-1 460 000</td>
                  <td class="num" style="color:#10b981;">+620 000</td>
                  <td><span class="status-pill rag-green">🟢 Lav risiko</span></td>
                </tr>
              </tbody>"""

if old_page_04_table in content:
    content = content.replace(old_page_04_table, new_page_04_table)
    print("Updated page_04 risikotabell")

# 7. Update page_dt_okonomi
old_dt_oko = """    kpis: [
      { title: "Total bokført (Regnskap)", val: "10,62 M", unit: "NOK", badge: "Netto", badgeCls: "variance-info", sub: "Debet - Kredit" },
      { title: "Budsjettbeløp", val: "10,75 M", unit: "NOK", badge: "BAC", badgeCls: "variance-info", sub: "Periodisert budsjett" },
      { title: "Avvik (Regnskap - Budsjett)", val: "-130 k", unit: "NOK", badge: "Mindreforbruk", badgeCls: "variance-favorable", sub: "Hittil i år" }
    ],"""

new_dt_oko = """    kpis: [
      { title: "Total bokført (Regnskap)", val: "68,38 M", unit: "NOK", badge: "YTD M01-M08", badgeCls: "variance-info", sub: "Debet 68,38 MNOK" },
      { title: "Budsjettbeløp", val: "54,56 M", unit: "NOK", badge: "Budsjett YTD", badgeCls: "variance-info", sub: "Årsbudsjett BAC: 81,84 M" },
      { title: "Avvik (Regnskap - Budsjett)", val: "-13,82 M", unit: "NOK", badge: "Merforbruk YTD", badgeCls: "variance-unfavorable", sub: "M01-M08 avvik" }
    ],"""

if old_dt_oko in content:
    content = content.replace(old_dt_oko, new_dt_oko)
    print("Updated page_dt_okonomi KPIs")

# 8. Update page_dt_bemanning
old_dt_bem = '{ title: "Lønnskostnader", val: "1 482,3 M", unit: "NOK", badge: "68,97% lønnsandel", badgeCls: "variance-unfavorable", sub: "Av 2 149 M totalkostnad" }'
new_dt_bem = '{ title: "Lønnskostnader", val: "50,97 M", unit: "NOK", badge: "78,31% lønnsandel", badgeCls: "variance-unfavorable", sub: "Av 65,08 M driftskostnader (Norm: 71,0%)" }'

if old_dt_bem in content:
    content = content.replace(old_dt_bem, new_dt_bem)
    print("Updated page_dt_bemanning KPI")

# 9. Update page_dt_prosjekt
old_dt_pro = """    kpis: [
      { title: "BAC (Budget at Completion)", val: "10,75 M", unit: "NOK", badge: "Opprinnelig budsjett", badgeCls: "variance-info", sub: "Budsjettramme" },
      { title: "EAC (Estimate at Completion)", val: "36,79 M", unit: "NOK", badge: "Forventet sluttkost", badgeCls: "variance-unfavorable", sub: "Oppdatert helårsestimat" },
      { title: "ETC (Estimate to Complete)", val: "26,18 M", unit: "NOK", badge: "Gjenstående forbruk", badgeCls: "variance-info", sub: "EAC - Påløpt YTD" },
      { title: "VAC (Variance at Completion)", val: "-26,05 M", unit: "NOK", badge: "Forventet overskridelse", badgeCls: "variance-unfavorable", sub: "BAC - EAC (Sluttavvik)" }
    ],"""

new_dt_pro = """    kpis: [
      { title: "BAC (Budget at Completion)", val: "20,20 M", unit: "NOK", badge: "TDI Prosjektbudsjett 2026", badgeCls: "variance-info", sub: "6 aktive prosjekter" },
      { title: "EAC (Estimate at Completion)", val: "20,46 M", unit: "NOK", badge: "Forventet sluttkost 2026", badgeCls: "variance-unfavorable", sub: "Oppdatert helårsestimat" },
      { title: "ETC (Estimate to Complete)", val: "41,04 M", unit: "NOK", badge: "Gjenstående portefølje", badgeCls: "variance-info", sub: "Totalramme 61,50 M - påløpt" },
      { title: "VAC (Variance at Completion)", val: "-260 k", unit: "NOK", badge: "Avvik M08", badgeCls: "variance-unfavorable", sub: "NFR002 & EVU001 overskridelse" }
    ],"""

if old_dt_pro in content:
    content = content.replace(old_dt_pro, new_dt_pro)
    print("Updated page_dt_prosjekt KPIs")

# 10. Update page_dt_tiltak
old_dt_til = """    kpis: [
      { title: "Forventet tiltakseffekt", val: "-10,01 M", unit: "NOK", badge: "Planlagt", badgeCls: "variance-favorable", sub: "16 tiltak" },
      { title: "Realisert tiltakseffekt", val: "-5,56 M", unit: "NOK", badge: "Bokført", badgeCls: "variance-favorable", sub: "Oppnådd YTD" },
      { title: "Realiseringsgrad", val: "55,59%", unit: "Grad", badge: "Mål: 70%", badgeCls: "variance-neutral", sub: "Restverdi: -4,44 M" }
    ],"""

new_dt_til = """    kpis: [
      { title: "Forventet tiltakseffekt", val: "-10,25 M", unit: "NOK", badge: "Planlagt", badgeCls: "variance-favorable", sub: "7 omstillingstiltak" },
      { title: "Realisert tiltakseffekt", val: "-4,85 M", unit: "NOK", badge: "Bokført", badgeCls: "variance-favorable", sub: "Oppnådd YTD" },
      { title: "Realiseringsgrad", val: "47,32%", unit: "Grad", badge: "Mål: 70%", badgeCls: "variance-neutral", sub: "Restverdi: -5,40 M" }
    ],"""

if old_dt_til in content:
    content = content.replace(old_dt_til, new_dt_til)
    print("Updated page_dt_tiltak KPIs")

# 11. Remove duplicate first page_glossary
# Find line range for first page_glossary
lines = content.split('\n')
gl_indices = [i for i, l in enumerate(lines) if l.strip().startswith('page_glossary: {')]
print("page_glossary indices:", gl_indices)
if len(gl_indices) == 2:
    idx1 = gl_indices[0]
    idx2 = gl_indices[1]
    # Check if lines between idx1 and idx2 end with '},\n'
    # Remove from idx1 to idx2
    print(f"Removing redundant page_glossary from line {idx1+1} to {idx2}")
    lines = lines[:idx1] + lines[idx2:]
    content = '\n'.join(lines)
    print("Redundant duplicate page_glossary removed")

# 12. Update remaining page_glossary
old_gl_eac = '{ title: "Sluttkostnad (EAC)", val: "36,79 M", unit: "NOK", badge: "LE_2026", badgeCls: "variance-unfavorable", sub: "Avvik mot BAC: +26,05 M" }'
new_gl_eac = '{ title: "Sluttkostnad (EAC)", val: "96,46 M", unit: "NOK", badge: "LE_2026", badgeCls: "variance-unfavorable", sub: "Avvik mot BAC: -14,62 M" }'

if old_gl_eac in content:
    content = content.replace(old_gl_eac, new_gl_eac)
    print("Updated page_glossary EAC")

content = content.replace('SUM(FactGL[Belop_signert])', 'SUM(FactGL[Belop])')

# 13. Update page_dt_studier
old_dt_stu = '{ title: "SPE60 Helårsekvivalenter", val: "5 615,7", unit: "SPE", badge: "Finansieringsgrunnlag", badgeCls: "variance-info", sub: "Resultatbasert uttelling" }'
new_dt_stu = '{ title: "SPE60 Helårsekvivalenter", val: "2 589,6", unit: "SPE", badge: "176,01 Mkr BFE", badgeCls: "variance-info", sub: "Finansieringsmodell KD 2025" }'

if old_dt_stu in content:
    content = content.replace(old_dt_stu, new_dt_stu)
    print("Updated page_dt_studier SPE60")

# 14. Update page_10_ai_agents
old_ai_kpis = """    kpis: [
      { title: "Sluttprognose (ML EAC)", val: "36,79 M", unit: "NOK", badge: "P50 Estimert", badgeCls: "variance-unfavorable", sub: "Vedtatt årsbudsjett: 10,75 M" },
      { title: "Prognosert Sluttavvik (VAC)", val: "+26,05 M", unit: "NOK", badge: "+242% Merforbruk", badgeCls: "variance-unfavorable", sub: "Udekket gap før korrigerende tiltak" },
      { title: "ML Modellkonfidens (R²)", val: "97,0%", unit: "R²", badge: "Ridge & Eksponentiell", badgeCls: "variance-favorable", sub: "95% CI: [31,4M - 42,1M]" },
      { title: "Budsjettbrudd-risiko", val: "M07 Juli", unit: "2026", badge: "Kritisk Milepæl", badgeCls: "variance-unfavorable", sub: "Tidspunkt bevilgning passeres" },
      { title: "Foreslåtte KI-Tiltak", val: "-10,25 M", unit: "NOK", badge: "5 Preskripsjoner", badgeCls: "variance-favorable", sub: "Restavvik etter tiltak: +15,8M" }
    ],"""

new_ai_kpis = """    kpis: [
      { title: "Sluttprognose (ML EAC)", val: "96,46 M", unit: "NOK", badge: "P50 Estimert", badgeCls: "variance-unfavorable", sub: "Vedtatt årsbudsjett: 81,84 M" },
      { title: "Prognosert Sluttavvik (VAC)", val: "-14,62 M", unit: "NOK", badge: "Budsjettbrudd M10", badgeCls: "variance-unfavorable", sub: "Udekket gap før korrigerende tiltak" },
      { title: "ML Modellkonfidens (R²)", val: "98,4%", unit: "R²", badge: "Ridge & Eksponentiell", badgeCls: "variance-favorable", sub: "95% CI: [91,2M - 102,5M]" },
      { title: "Budsjettbrudd-risiko", val: "M10 Okt", unit: "2026", badge: "Kritisk Milepæl", badgeCls: "variance-unfavorable", sub: "Tidspunkt årsbudsjett (81,84M) passeres" },
      { title: "Foreslåtte KI-Tiltak", val: "-10,25 M", unit: "NOK", badge: "7 Preskripsjoner", badgeCls: "variance-favorable", sub: "Restavvik etter tiltak: +4,37M" }
    ],"""

if old_ai_kpis in content:
    content = content.replace(old_ai_kpis, new_ai_kpis)
    print("Updated page_10_ai_agents KPIs")

content = content.replace('<span class="status-pill rag-red">Avvik: +26,05 MNOK</span>', '<span class="status-pill rag-red">Avvik: -14,62 MNOK</span>')

old_ai_fan = """              <text x="525" y="136" fill="#94a3b8" font-size="9.5" font-weight="600">Budsjett (10,75M)</text>
              <text x="525" y="34" fill="#f59e0b" font-size="10" font-weight="700">ML EAC (36,79M)</text>
              <text x="525" y="18" fill="#38bdf8" font-size="9">P90 (42,1M)</text>
              <text x="525" y="55" fill="#64748b" font-size="9">P10 (31,4M)</text>"""

new_ai_fan = """              <text x="525" y="136" fill="#94a3b8" font-size="9.5" font-weight="600">Budsjett (81,84M)</text>
              <text x="525" y="34" fill="#f59e0b" font-size="10" font-weight="700">ML EAC (96,46M)</text>
              <text x="525" y="18" fill="#38bdf8" font-size="9">P90 (102,5M)</text>
              <text x="525" y="55" fill="#64748b" font-size="9">P10 (91,2M)</text>"""

if old_ai_fan in content:
    content = content.replace(old_ai_fan, new_ai_fan)
    print("Updated page_10_ai_agents fan chart labels")

old_ai_p = """            <div>P10 (Beste utfall): <strong style="color: #38bdf8;">31,4 MNOK</strong></div>
            <div>P50 (Forventet base): <strong style="color: #f59e0b;">36,79 MNOK</strong></div>
            <div>P90 (Pessimistisk): <strong style="color: #ef4444;">42,1 MNOK</strong></div>"""

new_ai_p = """            <div>P10 (Beste utfall): <strong style="color: #38bdf8;">91,2 MNOK</strong></div>
            <div>P50 (Forventet base): <strong style="color: #f59e0b;">96,46 MNOK</strong></div>
            <div>P90 (Pessimistisk): <strong style="color: #ef4444;">102,5 MNOK</strong></div>"""

if old_ai_p in content:
    content = content.replace(old_ai_p, new_ai_p)
    print("Updated page_10_ai_agents P10/P50/P90")

# 15. Update page_11_rapportering
old_p11_kpis = """    kpis: [
      { title: "5 %-Regel Tak (F-05-20)", val: "106,94 Mkr", unit: "MNOK tak", badge: "0,01% benyttet", badgeCls: "rag-green", sub: "Maksimal tillatt bevilgningsreserve (5,0 % av 2 138,8 Mkr)" },
      { title: "KD SPE Produksjon 2025", val: "5 615,7", unit: "SPE60 enheter", badge: "86,4% måloppnåelse", badgeCls: "rag-amber", sub: "336 945 avlagte studiepoeng fordelt på 3 finansieringskategorier" },
      { title: "BOA & TDI Portefølje", val: "25,68 Mkr", unit: "MNOK inntekter", badge: "SRS 10 + SRS 9", badgeCls: "rag-blue", sub: "NFR (12,90M) + EU Horizon (7,43M) + Oppdrag (5,35M)" },
      { title: "Lønnsandel & Kapasitet", val: "68,97 %", unit: "av driftskostnader", badge: "1 482,3 Mkr", badgeCls: "rag-green", sub: "9,81 studenter per faglig årsverk | Frikjøp overvåkes i Unit4" }
    ],"""

new_p11_kpis = """    kpis: [
      { title: "5 %-Regel Tak (F-05-20)", val: "2,68 Mkr", unit: "MNOK tak", badge: "8,96% akkumulert", badgeCls: "rag-red", sub: "Konto 2080: -4,80 MNOK vs 5% tak (2,68 Mkr av 53,6M bevilgning)" },
      { title: "KD SPE Produksjon 2025", val: "2 589,6", unit: "SPE60 enheter", badge: "176,01 Mkr BFE", badgeCls: "rag-blue", sub: "336 945 avlagte studiepoeng fordelt på KD 2025 finansieringskategorier" },
      { title: "BOA & TDI Portefølje", val: "61,50 Mkr", unit: "MNOK portefølje", badge: "20,46 M påløpt", badgeCls: "rag-blue", sub: "6 prosjekter (NFR 11,45M, EU 6,82M, Oppdrag/EVU 2,19M) | SRS 10 + 9" },
      { title: "Lønnsandel & Kapasitet", val: "78,31 %", unit: "av driftskostnader", badge: "50,97 Mkr", badgeCls: "rag-red", sub: "Norm: 71,0 % | Lønn 50,97M av 65,08M drift | 1 285,9 årsverk" }
    ],"""

if old_p11_kpis in content:
    content = content.replace(old_p11_kpis, new_p11_kpis)
    print("Updated page_11 KPIs")

content = content.replace('<td class="num font-mono">5 615,74 SPE</td>', '<td class="num font-mono">2 589,60 SPE</td>')

# Write back to index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nSuccessfully updated index.html!")
