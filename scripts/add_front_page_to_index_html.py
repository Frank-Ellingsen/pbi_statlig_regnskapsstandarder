"""
add_front_page_to_index_html.py
--------------------------------
Injects 'page_00_forside' into const dashboards in index.html.
"""

import os

INDEX_HTML_PATH = r"C:\Users\frank\Desktop\UIA\uia_powerbi_complete_forecast_model\index.html"

with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
    content = f.read()

needle = "const dashboards = {\n        page_01: {"

page_00_body = '''const dashboards = {
        page_00_forside: {
          id: 'page_00_forside',
          title: 'Årsrapport Universitetet i Agder (UIA) - Project Controlling & Earned Value (EV) Analysis',
          role: 'Universitetsledelsen / Styret / Senior Controller',
          desc: 'Helhetlig årsrapport for Universitetet i Agder (UiA). Finansiell ytelse, Capex/Opex benchmarks, Earned Value (EVM) analyse og 100 % avstemt 12-måneders tidsrekke iht. DFØ SRS standarder og Edward Tufte Data-Ink Ratio.',
          slicers: [
            {
              label: 'Rapportvisning',
              options: [
                'Hele året 2026 (12 Mnd Fullført)',
                'T3 November Cutoff (AC 1 344M / ETC 100M)',
                'Fakultetsfordeling',
                'EVM S-Kurve Detaljer',
              ],
            },
            {
              label: 'Regnskapsstandard',
              options: [
                'DFØ SRS Opptjening (SRS 1, 9, 10, 17)',
                'Bevilgningsregnskap (Kontantprinsipp)',
                'KD Finansieringsmodell 2025',
              ],
            },
            {
              label: 'Avstemmingskontroll',
              options: [
                '100% Avstemt (1 433M Inntekt / 1 444M Kostnad)',
                'Underskudd -11,0M (Dekket av Note 15)',
              ],
            },
          ],
          kpis: [
            {
              title: 'Total Revenue (Inntekt)',
              val: '1 433,0 M',
              unit: 'NOK (BAC)',
              badge: '100,0 % BAC',
              badgeCls: 'variance-info',
              sub: 'Stat 1 234,0M (86,1%) | Forskning 123,0M | Andre 76,0M',
            },
            {
              title: 'Total Expenses (Kostnad)',
              val: '1 444,0 M',
              unit: 'NOK (EAC)',
              badge: '-11,0 M Avvik',
              badgeCls: 'variance-unfavorable',
              sub: 'Lønn 944,0M (65,4%) | Drift 340,0M | Capex 160,0M',
            },
            {
              title: 'Cost Performance Index (CPI)',
              val: '0,95',
              unit: 'Indeks',
              badge: 'T3 / M11 Cutoff',
              badgeCls: 'rag-amber',
              sub: 'EV 1 276,8M / AC 1 344,0M = 0,950 | Fullår EV: 1 344M',
            },
            {
              title: 'Schedule Performance (SPI)',
              val: '0,92',
              unit: 'Indeks',
              badge: 'T3 / M11 Cutoff',
              badgeCls: 'rag-amber',
              sub: 'EV 1 276,8M / PV 1 387,8M = 0,920 | Fremdriftsforsinkelse',
            },
          ],
          renderContent: () => `
      <!-- ======================================================================
           EXECUTIVE SUMMARY & FRONT PAGE BANNER
           ====================================================================== -->
      <div class="card-panel" style="margin-bottom: 24px; border-left: 4px solid #38bdf8; background: linear-gradient(135deg, rgba(19, 29, 51, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px;">
          <div>
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
              <span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; font-weight: 700; font-size: 11px; padding: 3px 8px; border-radius: 4px; border: 1px solid rgba(56, 189, 248, 0.3);">
                OFFISIELL VIRKSOMHETSRAPPORT 2026
              </span>
              <span style="color: var(--text-muted); font-size: 11px;">Universitetet i Agder | Org.nr 970 546 200</span>
            </div>
            <h1 style="font-size: 22px; font-weight: 700; color: #fff; margin-bottom: 6px; font-family: var(--font-display);">
              Årsrapport Universitetet i Agder (UIA) - Project Controlling & Earned Value (EV) Analysis
            </h1>
            <p style="font-size: 12.5px; color: var(--text-secondary); max-width: 900px; line-height: 1.6;">
              Rapportansvarlig: Senior Controller Frank Ellingsen | Standard: DFØ Statlige regnskapsstandarder (SRS 1, SRS 9, SRS 10, SRS 17) |
              KDs Finansieringsmodell 2025 | Edward Tufte Data-Ink standarder (desimaljusterte tall, ingen unødvendig støy).
            </p>
          </div>
          <div style="text-align: right; background: rgba(255,255,255,0.03); padding: 10px 16px; border-radius: 8px; border: 1px solid var(--border-subtle);">
            <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px;">Årsresultat (Underskudd)</div>
            <div style="font-size: 22px; font-weight: 700; color: #ef4444; font-family: var(--font-mono);">-11,0 MNOK</div>
            <div style="font-size: 10.5px; color: #94a3b8;">Avstemt mot Note 15 / Avsetninger</div>
          </div>
        </div>

        <div style="border-top: 1px solid var(--border-subtle); padding-top: 14px; margin-top: 8px;">
          <h3 style="font-size: 13.5px; font-weight: 600; color: #38bdf8; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">
            Executive Summary
          </h3>
          <p style="font-size: 13.5px; color: #e2e8f0; line-height: 1.65;">
            This report provides an analysis of the University of Agder's (UIA) financial performance, using Project Controlling and Earned Value (EV) analysis. The report highlights key findings, recommendations, and action items to ensure the university's financial stability. The underlying data represents a fully reconciled 12-month fiscal year with total revenue of <strong>1,433.0 MNOK</strong>, total expenditures of <strong>1,444.0 MNOK</strong>, an operating deficit of <strong>-11.0 MNOK</strong>, and a Cost Performance Index (CPI) of <strong>0.95</strong> with a Schedule Performance Index (SPI) of <strong>0.92</strong>.
          </p>
        </div>
      </div>

      <!-- ======================================================================
           KEY FINDINGS: 2 COLUMN PANELS (Financial Performance & Capex/Opex)
           ====================================================================== -->
      <div class="dash-grid-two-col" style="margin-bottom: 24px;">
        
        <!-- Panel 1: Financial Performance -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Financial Performance (NOK million)</div>
              <div class="panel-subtitle">Konsistent oppstilling iht. SRS 1 og bevilgningsvedtak</div>
            </div>
            <span class="status-pill gjennomfort">100% Avstemt</span>
          </div>
          <div class="table-container">
            <table class="tufte-table">
              <thead>
                <tr>
                  <th>Category</th>
                  <th class="num">Amount (NOK million)</th>
                  <th class="num">Andel av Inntekt</th>
                  <th>Regnskapsstandard / Merknad</th>
                </tr>
              </thead>
              <tbody>
                <tr style="background: rgba(56, 189, 248, 0.04); font-weight: 600;">
                  <td style="color: #38bdf8;">Total Revenue</td>
                  <td class="num font-mono" style="color: #38bdf8; font-weight: 700;">1 433,0</td>
                  <td class="num font-mono">100,0 %</td>
                  <td>Samlet budsjettramme (BAC)</td>
                </tr>
                <tr>
                  <td style="padding-left: 20px;">Government Funding</td>
                  <td class="num font-mono">1 234,0</td>
                  <td class="num font-mono">86,1 %</td>
                  <td>KDs bevilgningsbrev (Basis + SPE)</td>
                </tr>
                <tr>
                  <td style="padding-left: 20px;">Research Funding</td>
                  <td class="num font-mono">123,0</td>
                  <td class="num font-mono">8,6 %</td>
                  <td>SRS 10 BOA Bidrag (NFR, EU)</td>
                </tr>
                <tr>
                  <td style="padding-left: 20px;">Other Revenue</td>
                  <td class="num font-mono">76,0</td>
                  <td class="num font-mono">5,3 %</td>
                  <td>SRS 9 Oppdrag, EVU, leie, avgifter</td>
                </tr>
                <tr style="border-top: 1px solid var(--border-strong); background: rgba(239, 68, 68, 0.04); font-weight: 600;">
                  <td style="color: #f87171;">Total Expenses</td>
                  <td class="num font-mono" style="color: #f87171; font-weight: 700;">1 444,0</td>
                  <td class="num font-mono">100,8 %</td>
                  <td>Helårsforbruk (EAC / AC)</td>
                </tr>
                <tr>
                  <td style="padding-left: 20px;">Personnel Expenses</td>
                  <td class="num font-mono">944,0</td>
                  <td class="num font-mono">65,9 %</td>
                  <td>Konto 5000-5999 (65,4% av kostnad)</td>
                </tr>
                <tr>
                  <td style="padding-left: 20px;">Operating Expenses</td>
                  <td class="num font-mono">340,0</td>
                  <td class="num font-mono">23,7 %</td>
                  <td>Konto 6000-7999 (23,5% av kostnad)</td>
                </tr>
                <tr>
                  <td style="padding-left: 20px;">Capital Expenditures</td>
                  <td class="num font-mono">160,0</td>
                  <td class="num font-mono">11,2 %</td>
                  <td>SRS 17 FoU-investering (11,1% av kostnad)</td>
                </tr>
                <tr style="border-top: 2px solid var(--border-strong); background: rgba(255, 255, 255, 0.03); font-weight: 700;">
                  <td>Net Operating Result (Underskudd)</td>
                  <td class="num font-mono" style="color: #ef4444;">-11,0</td>
                  <td class="num font-mono" style="color: #ef4444;">-0,8 %</td>
                  <td>Dekkes av oppspart formålskapital (Note 15)</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Panel 2: Capex/Opex Benchmarks -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Capex/Opex Benchmarks & Sektornormer</div>
              <div class="panel-subtitle">Forholdstall mot nasjonale UH-referanser</div>
            </div>
            <span class="status-pill rag-amber">1 Obs-punkt</span>
          </div>
          <div class="table-container">
            <table class="tufte-table">
              <thead>
                <tr>
                  <th>Category</th>
                  <th class="num">% av Inntekt</th>
                  <th class="num">% av Kostnad</th>
                  <th>UH-Sektornorm</th>
                  <th>Vurdering</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Personnel Expenses</strong></td>
                  <td class="num font-mono" style="color: #f59e0b; font-weight: 600;">65,7 % &ndash; 65,9 %</td>
                  <td class="num font-mono">65,4 %</td>
                  <td>62,0 % &ndash; 65,0 %</td>
                  <td><span class="status-pill rag-amber">🟡 Moderat over norm</span></td>
                </tr>
                <tr>
                  <td><strong>Operating Expenses</strong></td>
                  <td class="num font-mono" style="color: #10b981; font-weight: 600;">23,7 %</td>
                  <td class="num font-mono">23,5 %</td>
                  <td>22,0 % &ndash; 25,0 %</td>
                  <td><span class="status-pill gjennomfort">🟢 I henhold til norm</span></td>
                </tr>
                <tr>
                  <td><strong>Capital Expenditures</strong></td>
                  <td class="num font-mono" style="color: #10b981; font-weight: 600;">11,1 % &ndash; 11,2 %</td>
                  <td class="num font-mono">11,1 %</td>
                  <td>10,0 % &ndash; 12,0 %</td>
                  <td><span class="status-pill gjennomfort">🟢 Balansert FoU-løft</span></td>
                </tr>
                <tr style="border-top: 1px solid var(--border-strong); font-weight: 600;">
                  <td>Sum Kostnadsandel</td>
                  <td class="num font-mono" style="color: #ef4444;">100,8 %</td>
                  <td class="num font-mono">100,0 %</td>
                  <td>100,0 %</td>
                  <td><span class="status-pill forsinket">🔴 0,8 % netto merforbruk</span></td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div style="margin-top: 18px; padding: 12px 14px; background: rgba(255,255,255,0.02); border-radius: 6px; border: 1px solid var(--border-subtle);">
            <div style="font-size: 11px; font-weight: 600; color: #94a3b8; margin-bottom: 8px; text-transform: uppercase;">
              Visuell kostnadsfordeling (Andel av 1 444 MNOK)
            </div>
            <div style="display: flex; height: 18px; border-radius: 4px; overflow: hidden; background: #1e293b; margin-bottom: 6px;">
              <div style="width: 65.4%; background: #6366f1;" title="Lønn: 65.4%"></div>
              <div style="width: 23.5%; background: #38bdf8;" title="Drift: 23.5%"></div>
              <div style="width: 11.1%; background: #10b981;" title="Capex: 11.1%"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 10.5px; color: var(--text-muted);">
              <span style="color: #a5b4fc;">■ Lønn (944M / 65,4%)</span>
              <span style="color: #7dd3fc;">■ Drift (340M / 23,5%)</span>
              <span style="color: #6ee7b7;">■ Capex (160M / 11,1%)</span>
            </div>
          </div>
        </div>
      </div>

      <!-- ======================================================================
           EVM PARAMETERS & S-CURVE CHART (2 COLUMN PANELS)
           ====================================================================== -->
      <div class="dash-grid-two-col" style="margin-bottom: 24px;">
        
        <!-- Panel 3: EVM Parameters Table & Math Proof -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">EVM Parameters & Matematisk Avstemming</div>
              <div class="panel-subtitle">Earned Value Management (EVM) etter standard ISO 21508</div>
            </div>
            <span class="status-pill forsinket">CPI &lt; 1.0</span>
          </div>
          <div class="table-container">
            <table class="tufte-table">
              <thead>
                <tr>
                  <th>Category</th>
                  <th class="num">Value</th>
                  <th>Formel / Forklaring</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Cost Performance Index (CPI)</strong></td>
                  <td class="num font-mono" style="color: #f59e0b; font-weight: 700;">0,95</td>
                  <td><code>EV / AC</code> = 1 276,8 / 1 344,0 = 0,950 (Kostnadsoverskridelse)</td>
                </tr>
                <tr>
                  <td><strong>Schedule Performance Index (SPI)</strong></td>
                  <td class="num font-mono" style="color: #f59e0b; font-weight: 700;">0,92</td>
                  <td><code>EV / PV</code> = 1 276,8 / 1 387,8 = 0,920 (Fremdriftsforsinkelse)</td>
                </tr>
                <tr>
                  <td><strong>Earned Value (EV)</strong></td>
                  <td class="num font-mono" style="color: #38bdf8; font-weight: 700;">1 344 M</td>
                  <td>Verdi av opptjent arbeid ved fullført regnskapsår (M11: 1 276,8M)</td>
                </tr>
                <tr>
                  <td><strong>Budget at Completion (BAC)</strong></td>
                  <td class="num font-mono">1 433 M</td>
                  <td>Opprinnelig vedtatt budsjettgrunnlag / inntektsramme</td>
                </tr>
                <tr>
                  <td><strong>Estimate at Completion (EAC)</strong></td>
                  <td class="num font-mono" style="color: #f87171; font-weight: 700;">1 444 M</td>
                  <td><code>AC + ETC</code> = 1 344,0 + 100,0 = 1 444,0 MNOK helårskostnad</td>
                </tr>
                <tr>
                  <td><strong>Estimate to Complete (ETC)</strong></td>
                  <td class="num font-mono">100 M</td>
                  <td>Gjenstående restkostnad per T3-cutoff (Desember: 100,0 MNOK)</td>
                </tr>
                <tr style="border-top: 1px solid var(--border-subtle); color: var(--text-secondary);">
                  <td>Actual Cost YTD (AC Cutoff)</td>
                  <td class="num font-mono">1 344 M</td>
                  <td>Påløpt kostnad per november (M11) = <code>EAC - ETC</code></td>
                </tr>
                <tr style="color: var(--text-secondary);">
                  <td>Variance at Completion (VAC)</td>
                  <td class="num font-mono" style="color: #ef4444;">-11 M</td>
                  <td><code>BAC - EAC</code> = 1 433,0 - 1 444,0 = -11,0 MNOK sluttavvik</td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div style="margin-top: 12px; font-size: 11px; color: var(--text-muted); line-height: 1.5; padding: 10px; background: rgba(255,255,255,0.02); border-radius: 6px;">
            <strong>Controller-presisering om avstemming:</strong><br>
            Per T3-cutoff (november) var påløpt kostnad <strong>AC = 1 344 MNOK</strong> og gjenstående desemberbudsjett <strong>ETC = 100 MNOK</strong>, som ga sluttprognose <strong>EAC = 1 444 MNOK</strong>. Opptjent verdi ved cutoff var 1 276,8 MNOK (CPI 0,95 og SPI 0,92). Ved årsslutt ble levert samlet EV på <strong>1 344 MNOK</strong>, som bekrefter det endelige sluttavviket på -11 MNOK mot opprinnelig budsjettramme.
          </div>
        </div>

        <!-- Panel 4: EVM S-Curve Chart -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">EVM S-Kurve: Helårlig Tidsrekke (PV, EV, AC)</div>
              <div class="panel-subtitle">Planlagt fremdrift (PV) vs Opptjent verdi (EV) vs Faktisk kostnad (AC)</div>
            </div>
            <span class="status-pill under-arbeid">Månedlig S-Kurve</span>
          </div>
          <div class="chart-container" style="min-height: 250px;">
            ${generateLineChartSVG([
              {
                name: 'PV (Plan)',
                data: [121.0, 243.0, 371.0, 498.0, 629.0, 774.0, 869.0, 992.0, 1124.0, 1256.0, 1387.8, 1507.8],
                color: '#94a3b8',
                dashed: true,
              },
              {
                name: 'EV (Opptjent)',
                data: [111.0, 223.0, 341.0, 458.0, 578.0, 711.0, 799.0, 912.0, 1034.0, 1155.5, 1276.8, 1344.0],
                color: '#10b981',
              },
              {
                name: 'AC (Faktisk)',
                data: [114.5, 229.0, 350.0, 469.5, 593.5, 758.5, 848.0, 966.0, 1092.0, 1218.5, 1344.0, 1444.0],
                color: '#ef4444',
              },
            ])}
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 11px; margin-top: 8px; color: var(--text-muted); border-top: 1px solid var(--border-subtle); padding-top: 8px;">
            <span><strong style="color: #94a3b8;">--- PV:</strong> Planlagt budsjettkurve</span>
            <span><strong style="color: #10b981;">― EV:</strong> Opptjent fysisk fremdrift</span>
            <span><strong style="color: #ef4444;">― AC:</strong> Faktisk påløpte regnskapskostnader</span>
          </div>
        </div>
      </div>

      <!-- ======================================================================
           FULL 12-MONTH RECONCILED DATA TABLE (Full Width)
           ====================================================================== -->
      <div class="card-panel" style="margin-bottom: 24px;">
        <div class="panel-header">
          <div>
            <div class="panel-title">FactYearlyReconciliation - Helårlig Månedlig Avstemming (12 Måneder, NOK Million)</div>
            <div class="panel-subtitle">Hver måned summerer seg eksakt opp til årsrapportens offisielle nøkkeltall</div>
          </div>
          <span class="status-pill gjennomfort">100% Avstemt CSV</span>
        </div>
        <div class="table-container" style="max-height: 420px; overflow-y: auto;">
          <table class="tufte-table">
            <thead>
              <tr>
                <th>Mnd</th>
                <th class="num">Statlig</th>
                <th class="num">Forskning</th>
                <th class="num">Andre</th>
                <th class="num" style="color: #38bdf8;">Total Inntekt</th>
                <th class="num">Lønn</th>
                <th class="num">Drift</th>
                <th class="num">Capex</th>
                <th class="num" style="color: #f87171;">Total Kostnad</th>
                <th class="num">Netto</th>
                <th class="num">Kum. PV</th>
                <th class="num">Kum. EV</th>
                <th class="num">Kum. AC</th>
                <th class="num">CPI</th>
                <th class="num">SPI</th>
              </tr>
            </thead>
            <tbody>
              <tr><td>01 Jan</td><td class="num font-mono">102,8</td><td class="num font-mono">8,5</td><td class="num font-mono">5,8</td><td class="num font-mono" style="font-weight:600;">117,1</td><td class="num font-mono">76,5</td><td class="num font-mono">27,5</td><td class="num font-mono">10,5</td><td class="num font-mono" style="font-weight:600;">114,5</td><td class="num font-mono" style="color:#10b981;">+2,6</td><td class="num font-mono">121,0</td><td class="num font-mono">111,0</td><td class="num font-mono">114,5</td><td class="num font-mono">0,97</td><td class="num font-mono">0,92</td></tr>
              <tr><td>02 Feb</td><td class="num font-mono">102,8</td><td class="num font-mono">9,2</td><td class="num font-mono">7,5</td><td class="num font-mono" style="font-weight:600;">119,5</td><td class="num font-mono">77,0</td><td class="num font-mono">26,5</td><td class="num font-mono">11,0</td><td class="num font-mono" style="font-weight:600;">114,5</td><td class="num font-mono" style="color:#10b981;">+5,0</td><td class="num font-mono">243,0</td><td class="num font-mono">223,0</td><td class="num font-mono">229,0</td><td class="num font-mono">0,97</td><td class="num font-mono">0,92</td></tr>
              <tr><td>03 Mar</td><td class="num font-mono">102,8</td><td class="num font-mono">10,1</td><td class="num font-mono">6,2</td><td class="num font-mono" style="font-weight:600;">119,1</td><td class="num font-mono">78,5</td><td class="num font-mono">30,0</td><td class="num font-mono">12,5</td><td class="num font-mono" style="font-weight:600;">121,0</td><td class="num font-mono" style="color:#ef4444;">-1,9</td><td class="num font-mono">371,0</td><td class="num font-mono">341,0</td><td class="num font-mono">350,0</td><td class="num font-mono">0,97</td><td class="num font-mono">0,92</td></tr>
              <tr><td>04 Apr</td><td class="num font-mono">102,8</td><td class="num font-mono">10,5</td><td class="num font-mono">6,4</td><td class="num font-mono" style="font-weight:600;">119,7</td><td class="num font-mono">78,0</td><td class="num font-mono">28,5</td><td class="num font-mono">13,0</td><td class="num font-mono" style="font-weight:600;">119,5</td><td class="num font-mono" style="color:#10b981;">+0,2</td><td class="num font-mono">498,0</td><td class="num font-mono">458,0</td><td class="num font-mono">469,5</td><td class="num font-mono">0,98</td><td class="num font-mono">0,92</td></tr>
              <tr><td>05 Mai</td><td class="num font-mono">102,9</td><td class="num font-mono">11,2</td><td class="num font-mono">6,5</td><td class="num font-mono" style="font-weight:600;">120,6</td><td class="num font-mono">79,5</td><td class="num font-mono">30,5</td><td class="num font-mono">14,0</td><td class="num font-mono" style="font-weight:600;">124,0</td><td class="num font-mono" style="color:#ef4444;">-3,4</td><td class="num font-mono">629,0</td><td class="num font-mono">578,0</td><td class="num font-mono">593,5</td><td class="num font-mono">0,97</td><td class="num font-mono">0,92</td></tr>
              <tr style="background: rgba(239, 68, 68, 0.04);"><td>06 Jun (FP)</td><td class="num font-mono">102,9</td><td class="num font-mono">11,5</td><td class="num font-mono">6,8</td><td class="num font-mono" style="font-weight:600;">121,2</td><td class="num font-mono">116,0</td><td class="num font-mono">33,0</td><td class="num font-mono">16,0</td><td class="num font-mono" style="font-weight:600;">165,0</td><td class="num font-mono" style="color:#ef4444;">-43,8</td><td class="num font-mono">774,0</td><td class="num font-mono">711,0</td><td class="num font-mono">758,5</td><td class="num font-mono">0,94</td><td class="num font-mono">0,92</td></tr>
              <tr><td>07 Jul</td><td class="num font-mono">102,8</td><td class="num font-mono">6,2</td><td class="num font-mono">4,2</td><td class="num font-mono" style="font-weight:600;">113,2</td><td class="num font-mono">60,5</td><td class="num font-mono">20,0</td><td class="num font-mono">9,0</td><td class="num font-mono" style="font-weight:600;">89,5</td><td class="num font-mono" style="color:#10b981;">+23,7</td><td class="num font-mono">869,0</td><td class="num font-mono">799,0</td><td class="num font-mono">848,0</td><td class="num font-mono">0,94</td><td class="num font-mono">0,92</td></tr>
              <tr><td>08 Aug</td><td class="num font-mono">102,8</td><td class="num font-mono">9,8</td><td class="num font-mono">6,6</td><td class="num font-mono" style="font-weight:600;">119,2</td><td class="num font-mono">77,0</td><td class="num font-mono">27,0</td><td class="num font-mono">14,0</td><td class="num font-mono" style="font-weight:600;">118,0</td><td class="num font-mono" style="color:#10b981;">+1,2</td><td class="num font-mono">992,0</td><td class="num font-mono">912,0</td><td class="num font-mono">966,0</td><td class="num font-mono">0,94</td><td class="num font-mono">0,92</td></tr>
              <tr><td>09 Sep</td><td class="num font-mono">102,9</td><td class="num font-mono">11,4</td><td class="num font-mono">8,2</td><td class="num font-mono" style="font-weight:600;">122,5</td><td class="num font-mono">79,5</td><td class="num font-mono">31,5</td><td class="num font-mono">15,0</td><td class="num font-mono" style="font-weight:600;">126,0</td><td class="num font-mono" style="color:#ef4444;">-3,5</td><td class="num font-mono">1 124,0</td><td class="num font-mono">1 034,0</td><td class="num font-mono">1 092,0</td><td class="num font-mono">0,95</td><td class="num font-mono">0,92</td></tr>
              <tr><td>10 Okt</td><td class="num font-mono">102,8</td><td class="num font-mono">11,8</td><td class="num font-mono">6,5</td><td class="num font-mono" style="font-weight:600;">121,1</td><td class="num font-mono">79,0</td><td class="num font-mono">31,5</td><td class="num font-mono">16,0</td><td class="num font-mono" style="font-weight:600;">126,5</td><td class="num font-mono" style="color:#ef4444;">-5,4</td><td class="num font-mono">1 256,0</td><td class="num font-mono">1 155,5</td><td class="num font-mono">1 218,5</td><td class="num font-mono">0,95</td><td class="num font-mono">0,92</td></tr>
              <tr style="background: rgba(245, 158, 11, 0.05); font-weight: 600;">
                <td style="color: #fbbf24;">11 Nov (T3)</td>
                <td class="num font-mono">102,8</td><td class="num font-mono">11,6</td><td class="num font-mono">6,0</td><td class="num font-mono" style="font-weight:600;">120,4</td><td class="num font-mono">78,5</td><td class="num font-mono">31,0</td><td class="num font-mono">16,0</td><td class="num font-mono" style="font-weight:600;">125,5</td>
                <td class="num font-mono" style="color:#ef4444;">-5,1</td>
                <td class="num font-mono" style="color:#fbbf24;">1 387,8</td>
                <td class="num font-mono" style="color:#fbbf24;">1 276,8</td>
                <td class="num font-mono" style="color:#fbbf24;">1 344,0</td>
                <td class="num font-mono" style="color:#fbbf24;">0,95</td>
                <td class="num font-mono" style="color:#fbbf24;">0,92</td>
              </tr>
              <tr><td>12 Des</td><td class="num font-mono">102,9</td><td class="num font-mono">11,2</td><td class="num font-mono">5,3</td><td class="num font-mono" style="font-weight:600;">119,4</td><td class="num font-mono">64,0</td><td class="num font-mono">23,0</td><td class="num font-mono">13,0</td><td class="num font-mono" style="font-weight:600;">100,0</td><td class="num font-mono" style="color:#10b981;">+19,4</td><td class="num font-mono">1 507,8</td><td class="num font-mono">1 344,0</td><td class="num font-mono">1 444,0</td><td class="num font-mono">0,93</td><td class="num font-mono">0,89</td></tr>
            </tbody>
            <tfoot>
              <tr style="border-top: 2px solid var(--border-strong); background: rgba(56, 189, 248, 0.08); font-weight: 700;">
                <td style="color: #fff;">TOTALT 2026</td>
                <td class="num font-mono" style="color: #38bdf8;">1 234,0</td>
                <td class="num font-mono" style="color: #38bdf8;">123,0</td>
                <td class="num font-mono" style="color: #38bdf8;">76,0</td>
                <td class="num font-mono" style="color: #38bdf8; font-weight: 800;">1 433,0</td>
                <td class="num font-mono" style="color: #f87171;">944,0</td>
                <td class="num font-mono" style="color: #f87171;">340,0</td>
                <td class="num font-mono" style="color: #f87171;">160,0</td>
                <td class="num font-mono" style="color: #f87171; font-weight: 800;">1 444,0</td>
                <td class="num font-mono" style="color: #ef4444; font-weight: 800;">-11,0</td>
                <td class="num font-mono">1 507,8</td>
                <td class="num font-mono" style="color: #10b981;">1 344,0</td>
                <td class="num font-mono" style="color: #ef4444;">1 444,0</td>
                <td class="num font-mono" style="color: #f59e0b;">0,95*</td>
                <td class="num font-mono" style="color: #f59e0b;">0,92*</td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>

      <!-- ======================================================================
           KEY RISKS, RECOMMENDATIONS & ACTION ITEMS (2 Column Grid)
           ====================================================================== -->
      <div class="dash-grid-two-col">
        
        <!-- Panel 5: Key Risks -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Key Risks (Universitetets Hovedrisikoer)</div>
              <div class="panel-subtitle">Sårbarhetsfaktorer identifisert i årsoppgjøret</div>
            </div>
            <span class="status-pill forsinket">4 Risikoområder</span>
          </div>
          <div style="display: flex; flex-direction: column; gap: 12px;">
            <div style="padding: 12px; background: rgba(239, 68, 68, 0.06); border-left: 3px solid #ef4444; border-radius: 4px;">
              <div style="font-weight: 600; color: #fff; font-size: 13px; margin-bottom: 2px;">1. Government Funding (Statlig bevilgning)</div>
              <p style="font-size: 11.5px; color: var(--text-secondary); line-height: 1.5;">
                Innstramming i KDs budsjettrammer og ny finansieringsmodell 2025 (forenkling til 3 studiepoengkategorier). Kritisk risiko dersom nye lavere satser feilanvendes på eksisterende studieplassvolum fremfor kun marginale endringer.
              </p>
            </div>
            <div style="padding: 12px; background: rgba(245, 158, 11, 0.06); border-left: 3px solid #f59e0b; border-radius: 4px;">
              <div style="font-weight: 600; color: #fff; font-size: 13px; margin-bottom: 2px;">2. Research Funding (Forskningsfinansiering)</div>
              <p style="font-size: 11.5px; color: var(--text-secondary); line-height: 1.5;">
                Økt konkurranse om NFR- og EU Horizon-midler. Forsinkelser i stipendiatrekruttering og milepælsleveranser (f.eks. NFR001) reduserer BOA-inntektsføring etter SRS 10 og belaster institusjonens faste kapasitet.
              </p>
            </div>
            <div style="padding: 12px; background: rgba(239, 68, 68, 0.06); border-left: 3px solid #ef4444; border-radius: 4px;">
              <div style="font-weight: 600; color: #fff; font-size: 13px; margin-bottom: 2px;">3. Personnel Expenses (Lønnskostnader)</div>
              <p style="font-size: 11.5px; color: var(--text-secondary); line-height: 1.5;">
                Lønnsandelen utgjør 65,9 % av total inntekt (944,0 MNOK), som overskrider referansenormen på 62–65 %. Høy fast bemanning i kombinasjon med lønnsoppgjør og feriepengeforpliktelser skaper stivhet i kostnadsstrukturen.
              </p>
            </div>
            <div style="padding: 12px; background: rgba(56, 189, 248, 0.06); border-left: 3px solid #38bdf8; border-radius: 4px;">
              <div style="font-weight: 600; color: #fff; font-size: 13px; margin-bottom: 2px;">4. Capital Expenditures (Investeringer)</div>
              <p style="font-size: 11.5px; color: var(--text-secondary); line-height: 1.5;">
                Kapitalbehov på 160,0 MNOK (11,2 % av inntekt) for laboratorieoppgraderinger og IT-infrastruktur krever streng overholdelse av anbudsregler (FOA) og må balanseres mot 5 %-regelen (F-05-20) for ubrukte midler.
              </p>
            </div>
          </div>
        </div>

        <!-- Panel 6: Recommendations & Action Items -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Recommendations & Action Plan</div>
              <div class="panel-subtitle">Forpliktende omstillingstiltak vedtatt av ledelsen</div>
            </div>
            <span class="status-pill planlagt">Handlingsplan</span>
          </div>
          
          <div style="margin-bottom: 14px;">
            <h4 style="font-size: 12.5px; font-weight: 600; color: #38bdf8; margin-bottom: 8px; text-transform: uppercase;">
              Strategic Recommendations
            </h4>
            <ol style="padding-left: 18px; font-size: 12px; color: var(--text-secondary); line-height: 1.6;">
              <li style="margin-bottom: 6px;">
                <strong style="color: #fff;">Optimize personnel expenses:</strong> Reduce personnel expenses while maintaining academic quality through natural attrition, vacancy control, and reallocating teaching resources (Tiltak T001 / T002).
              </li>
              <li style="margin-bottom: 6px;">
                <strong style="color: #fff;">Diversify funding sources:</strong> Seek to diversify funding sources to reduce reliance on government funding by scaling EU Horizon applications, industry co-funding, and commissioned courses (EVU).
              </li>
              <li style="margin-bottom: 6px;">
                <strong style="color: #fff;">Prioritize capital expenditures:</strong> Prioritize capital expenditures to ensure essential projects are completed on time and within budget, with strict stage-gate approvals and minikonkurranser (Tiltak T005).
              </li>
            </ol>
          </div>

          <div style="border-top: 1px solid var(--border-subtle); padding-top: 12px;">
            <h4 style="font-size: 12.5px; font-weight: 600; color: #10b981; margin-bottom: 8px; text-transform: uppercase;">
              Concrete Action Items (Knyttet til Omstillingsplanen)
            </h4>
            <div style="display: flex; flex-direction: column; gap: 8px;">
              <div style="display: flex; gap: 10px; align-items: flex-start; font-size: 11.5px;">
                <span class="status-pill gjennomfort" style="flex-shrink: 0;">T001/T002</span>
                <span style="color: var(--text-secondary);">
                  <strong style="color: #fff;">Develop a personnel expense reduction plan:</strong> Etablert ansettelsesstopp for administrative stillinger og omdisponering av 5,0 faglige årsverk. Forventet netto helårseffekt: <strong>-4,85 MNOK</strong>.
                </span>
              </div>
              <div style="display: flex; gap: 10px; align-items: flex-start; font-size: 11.5px;">
                <span class="status-pill under-arbeid" style="flex-shrink: 0;">T003/T004</span>
                <span style="color: var(--text-secondary);">
                  <strong style="color: #fff;">Diversify funding sources:</strong> Etablert felles BOA-støtteenhet for EU Horizon og NFR-søknader med mål om å øke eksternfinansiering til <strong>150 MNOK</strong> innen 2028.
                </span>
              </div>
              <div style="display: flex; gap: 10px; align-items: flex-start; font-size: 11.5px;">
                <span class="status-pill planlagt" style="flex-shrink: 0;">T005/T006</span>
                <span style="color: var(--text-secondary);">
                  <strong style="color: #fff;">Prioritize capital expenditures:</strong> Gjennomgang av alle IT- og labinvesteringer over 500 000 kr i henhold til anskaffelsesregelverket (FOA). Sikrer at capex holdes innenfor <strong>160,0 MNOK</strong>.
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    `,
        },
        page_01: {'''

if needle in content:
    content = content.replace(needle, page_00_body)
    print("Successfully injected page_00_forside into const dashboards!")
else:
    print("Could not find needle in content. Check if page_00_forside is already there.")

with open(INDEX_HTML_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated index.html successfully.")
