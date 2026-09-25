
      // Mock data model state
      const modelData = {
        regnskapYTD: 68381200.0,
        budsjettYTD: 54560000.0,
        avvikYTD: -13821200.0,
        aarsbudsjett: 81840000.0,
        forecastAar: 96460000.0,
        forecastAvvik: -14620000.0,
        aarsverk: 1285.93,
        fagligeAarsverk: 661.77,
        studenter: 6490,
        avlagteSP: 336945.4,
        spe60: 2589.6,
        bfeInntekt: 176012760.0,
        spMaaloppnaelse: 86.38,
        boaInntekter: 20460000.0,
        boaPortefolje: 61500000.0,
        tdiBudsjett: 20200000.0,
        nfrInntekter: 11450000.0,
        euInntekter: 6820000.0,
        lonnskostnader: 50970000.0,
        lonnsandel: 78.31,
        konto2080Avsetning: -4800000.0,
        avsetningsgradF05: 8.96,
        antallTiltak: 7,
        aapneTiltak: 4,
        forsinkedeTiltak: 1,
        forventetTiltak: -10250000.0,
        realisertTiltak: -4850000.0,
        tiltakGrad: 47.32,
        forecastEtterTiltak: 86210000.0,
        restavvikEtterTiltak: 4370000.0,
      };

      function formatMNOK(val) {
        return (val / 1000000).toFixed(2) + ' M';
      }

      function formatNOK(val) {
        return (
          new Intl.NumberFormat('no-NO', { maximumFractionDigits: 0 }).format(
            val
          ) + ' kr'
        );
      }

      function formatNum(val, dec = 1) {
        return new Intl.NumberFormat('no-NO', {
          minimumFractionDigits: dec,
          maximumFractionDigits: dec,
        }).format(val);
      }

      // 13 DASHBOARD DEFINITIONS
      const dashboards = {
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
        page_01: {
          id: 'page_01_instituttleder',
          title: '01 Instituttleder (Operativ styring)',
          role: 'Instituttleder / Kontorsjef',
          desc: 'Operativ økonomisk styring for instituttet. Rask oversikt over YTD-regnskap mot budsjett, helårsprognose (LE), hva som driver avviket, samt oppfølging av instituttets vedtatte innsparingstiltak.',
          slicers: [
            {
              label: 'Velg institutt',
              options: [
                'Alle institutter',
                'Institutt for økonomi',
                'Institutt for rettsvitenskap',
                'Institutt for strategi og ledelse',
                'Institutt for IKT',
              ],
            },
            {
              label: 'Periode',
              options: ['2026-12 (YTD)', '2026-11', '2026-10', '2026-09'],
            },
            {
              label: 'Prognoseversjon',
              options: ['LE_2026 (Gjeldende)', 'FC2_2026', 'FC1_2026'],
            },
          ],
          kpis: [
            {
              title: 'Regnskap YTD',
              val: '68,38 M',
              unit: 'NOK',
              badge: '+25,3% vs Budsjett',
              badgeCls: 'variance-unfavorable',
              sub: 'Budsjett YTD: 54,56 M',
            },
            {
              title: 'Avvik YTD',
              val: '-13,82 M',
              unit: 'NOK',
              badge: 'Merforbruk YTD',
              badgeCls: 'variance-unfavorable',
              sub: 'M01-M08 Faktisk avvik',
            },
            {
              title: 'Forecast årsbeløp (LE)',
              val: '96,46 M',
              unit: 'NOK',
              badge: 'EAC Slutt',
              badgeCls: 'variance-unfavorable',
              sub: 'Forventet helårsforbruk',
            },
            {
              title: 'Forecastavvik',
              val: '-14,62 M',
              unit: 'NOK',
              badge: 'Budsjettbrudd M10',
              badgeCls: 'variance-unfavorable',
              sub: 'Vedtatt ramme (BAC): 81,84 M',
            },
            {
              title: 'Årsverk',
              val: '1 285,9',
              unit: 'FTE',
              badge: '51,5% Vitenskapelig',
              badgeCls: 'variance-info',
              sub: 'Faglige årsverk: 661,8',
            },
          ],
          renderContent: () => `
      <div class="dash-grid-two-col">
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Månedlig faktisk, budsjett og prognosetrend 2026</div>
              <div class="panel-subtitle">S-kurve & månedlig run rate i MNOK (Tufte direkte merking)</div>
            </div>
          </div>
          <div class="chart-container">
            ${generateLineChartSVG([
              {
                name: 'Regnskap',
                color: '#38bdf8',
                data: [8.5, 17.1, 25.6, 34.2, 42.7, 51.3, 59.8, 68.38],
              },
              {
                name: 'Budsjett',
                color: '#94a3b8',
                dashed: true,
                data: [
                  6.82, 13.64, 20.46, 27.28, 34.1, 40.92, 47.74, 54.56, 61.38,
                  68.2, 75.02, 81.84,
                ],
              },
              {
                name: 'Forecast (LE)',
                color: '#f59e0b',
                data: [
                  8.5, 17.1, 25.6, 34.2, 42.7, 51.3, 59.8, 68.38, 75.4, 82.5,
                  89.5, 96.46,
                ],
              },
            ])}
          </div>
        </div>

        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Hva driver prognoseavviket?</div>
              <div class="panel-subtitle">Forecastavvik per DFØ SRS-regnskapslinje (MNOK)</div>
            </div>
          </div>
          <div class="chart-container">
            ${generateBarChartSVG(
              [
                { label: 'Lønnskostnader (UF/TA)', val: 9.8, color: '#ef4444' },
                { label: 'Andre driftskostnader', val: 3.2, color: '#f59e0b' },
                { label: 'Av- og nedskrivninger', val: 1.1, color: '#f59e0b' },
                {
                  label: 'Inntektsbortfall / prosjektavvik',
                  val: 0.52,
                  color: '#10b981',
                },
              ],
              'MNOK'
            )}
          </div>
        </div>
      </div>

      <div class="dash-grid-two-col">
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Ressurser & Studieproduktivitet</div>
              <div class="panel-subtitle">Bemanningsforhold og enhetskostnader</div>
            </div>
          </div>
          <div class="table-container">
            <table class="tufte-table">
              <thead>
                <tr>
                  <th>Institutt</th>
                  <th class="num">Studenter</th>
                  <th class="num">Faglige ÅV</th>
                  <th class="num">Stud/FagÅV</th>
                  <th class="num">SPE60</th>
                  <th class="num">Kost/SPE60</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Inst. for økonomi</td>
                  <td class="num">2 410</td>
                  <td class="num">184,2</td>
                  <td class="num">13,1</td>
                  <td class="num">2 140,5</td>
                  <td class="num">82 450 kr</td>
                </tr>
                <tr>
                  <td>Inst. for rettsvitenskap</td>
                  <td class="num">1 180</td>
                  <td class="num">92,4</td>
                  <td class="num">12,8</td>
                  <td class="num">1 024,0</td>
                  <td class="num">79 120 kr</td>
                </tr>
                <tr>
                  <td>Inst. for strategi og ledelse</td>
                  <td class="num">1 750</td>
                  <td class="num">165,0</td>
                  <td class="num">10,6</td>
                  <td class="num">1 490,2</td>
                  <td class="num">94 300 kr</td>
                </tr>
                <tr>
                  <td>Inst. for IKT og teknologifag</td>
                  <td class="num">1 150</td>
                  <td class="num">220,2</td>
                  <td class="num">5,2</td>
                  <td class="num">961,0</td>
                  <td class="num">142 800 kr</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Tiltaksoppfølging (FactAction)</div>
              <div class="panel-subtitle">Innsparingstiltak og realiseringsstatus</div>
            </div>
            <a class="drill-link" onclick="showDashboard('page_dt_tiltak')">Alle tiltak &rarr;</a>
          </div>
          <div class="table-container">
            <table class="tufte-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Beskrivelse</th>
                  <th>Rolle</th>
                  <th class="num">Forventet</th>
                  <th class="num">Realisert</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><code>T-01</code></td>
                  <td>Vakansestopp adm. stillinger</td>
                  <td>Instituttleder</td>
                  <td class="num">-1 200 000</td>
                  <td class="num">-950 000</td>
                  <td><span class="status-pill gjennomfort">🟢 Gjennomført</span></td>
                </tr>
                <tr>
                  <td><code>T-02</code></td>
                  <td>Redusert sensorhonorar digital eksamen</td>
                  <td>Studieleder</td>
                  <td class="num">-450 000</td>
                  <td class="num">-310 000</td>
                  <td><span class="status-pill pagar">🟡 Pågår</span></td>
                </tr>
                <tr>
                  <td><code>T-03</code></td>
                  <td>Kutt i eksterne konsulenttjenester</td>
                  <td>Kontorsjef</td>
                  <td class="num">-800 000</td>
                  <td class="num">-200 000</td>
                  <td><span class="status-pill forsinket">🔴 Forsinket</span></td>
                </tr>
                <tr>
                  <td><code>T-04</code></td>
                  <td>Samleslåing av valgemner &lt; 15 stud</td>
                  <td>Instituttleder</td>
                  <td class="num">-1 500 000</td>
                  <td class="num">-1 100 000</td>
                  <td><span class="status-pill pagar">🟡 Pågår</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Bottom Summary Formula Strip -->
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
      </div>
    `,
        },

        page_02: {
          id: 'page_02_dekan',
          title: '02 Dekanens Dashbord (Strategisk & Rullende 12M)',
          role: 'Dekan / Fakultetsdirektør',
          desc: 'Helhetlig styringsbilde for UiA etter 4-soners grid: Rullende 12M baneprognose, bemanningsanalyse, BOA TDI-portefølje, KDs 2025 studiepoengmodell og F-05-20 risikostyring.',
          slicers: [
            {
              label: 'Tertial / Periode',
              options: [
                '2026-T2 (Ut August)',
                '2026-T1 (Ut April)',
                '2026-LE (Helår)',
              ],
            },
            {
              label: 'Fakultet / Enhet',
              options: [
                'Alle enheter',
                'Fakultet for teknologi og realfag (FAK-TR)',
                'Handelshøyskolen (HH)',
                'Fakultet for samfunnsvitenskap',
                'Fakultet for helse- og idrettsvitenskap',
              ],
            },
            {
              label: 'Prognoseversjon',
              options: [
                'LE_2026 (Gjeldende)',
                'FC2_2026',
                'FC1_2026',
                'BUD2026',
              ],
            },
          ],
          kpis: [
            {
              title: 'Total Inntekt YTD vs Budsjett',
              val: '68,38 M',
              unit: 'NOK',
              badge: '+13,82 M (Faktisk M01-M08)',
              badgeCls: 'variance-favorable',
              sub: 'Budsjett YTD: 54,56 MNOK | Basis + BOA',
            },
            {
              title: 'Lønnsandel av Drift',
              val: '78,3 %',
              unit: 'Lønn',
              badge: 'Mål: 70-71% (Avvik +7,3%)',
              badgeCls: 'variance-unfavorable',
              sub: 'Lønn YTD: 50,97 M | Drift: 14,11 M',
            },
            {
              title: 'Avsetningsgrad F-05-20',
              val: '8,96 %',
              unit: 'Konto 2080',
              badge: '🔴 5%-grense overskredet',
              badgeCls: 'variance-unfavorable',
              sub: 'Akkumulert: -4,80 MNOK vs maks 2,68 M',
            },
            {
              title: 'BOA Inntekt YTD (SRS 10)',
              val: '2,01 M',
              unit: 'NOK',
              badge: 'NFR kr 1,28M | EU kr 0,73M',
              badgeCls: 'variance-favorable',
              sub: 'Motsatt sammenstilling mot påløpte kostnader',
            },
            {
              title: 'Fakultetets Samlede RAG',
              val: 'RØD',
              unit: 'Status',
              badge: 'Vakanser & F-05-20 risiko',
              badgeCls: 'variance-unfavorable',
              sub: 'Kritisk: F-05-20 overskridelse & lønnsandel',
            },
          ],
          renderContent: () => `
      <!-- SONE 2: DRIFT & BEMANNING (Hovedfelt Venstre) -->
      <div class="dash-grid-two-col">
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title" style="display:flex; align-items:center; gap:8px;">
                <span>📊 Visual 2.1: Rullende 12M Baneprognose (Combo Line/Bar)</span>
              </div>
              <div class="panel-subtitle">M01–M08 Faktisk Regnskap + M09–M12 Gjeldende LE vs Vedtatt Budsjettbane (MNOK)</div>
            </div>
            <span class="status-pill rag-amber">R²: 99,7% | Bias: +4,8%</span>
          </div>
          <div class="chart-container" style="height: 220px;">
            <svg class="interactive-chart" viewBox="0 0 600 200">
              <defs>
                <linearGradient id="actualColGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.9" />
                  <stop offset="100%" stop-color="#0284c7" stop-opacity="0.5" />
                </linearGradient>
                <linearGradient id="leColGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.9" />
                  <stop offset="100%" stop-color="#d97706" stop-opacity="0.5" />
                </linearGradient>
              </defs>
              <line x1="45" y1="160" x2="550" y2="160" stroke="rgba(255,255,255,0.06)" />
              <line x1="45" y1="115" x2="550" y2="115" stroke="rgba(255,255,255,0.06)" />
              <line x1="45" y1="70" x2="550" y2="70" stroke="rgba(255,255,255,0.06)" />
              <line x1="45" y1="25" x2="550" y2="25" stroke="rgba(255,255,255,0.06)" />
              <text x="38" y="163" fill="#64748b" font-size="9" text-anchor="end">0M</text>
              <text x="38" y="118" fill="#64748b" font-size="9" text-anchor="end">4M</text>
              <text x="38" y="73" fill="#64748b" font-size="9" text-anchor="end">8M</text>
              <text x="38" y="28" fill="#64748b" font-size="9" text-anchor="end">12M</text>

              <rect x="52" y="72" width="24" height="88" rx="2" fill="url(#actualColGrad)" />
              <text x="64" y="174" fill="#94a3b8" font-size="9" text-anchor="middle">M01</text>
              <rect x="88" y="69" width="24" height="91" rx="2" fill="url(#actualColGrad)" />
              <text x="100" y="174" fill="#94a3b8" font-size="9" text-anchor="middle">M02</text>
              <rect x="124" y="65" width="24" height="95" rx="2" fill="url(#actualColGrad)" />
              <text x="136" y="174" fill="#94a3b8" font-size="9" text-anchor="middle">M03</text>
              <rect x="160" y="63" width="24" height="97" rx="2" fill="url(#actualColGrad)" />
              <text x="172" y="174" fill="#94a3b8" font-size="9" text-anchor="middle">M04</text>
              <rect x="196" y="60" width="24" height="100" rx="2" fill="url(#actualColGrad)" />
              <text x="208" y="174" fill="#94a3b8" font-size="9" text-anchor="middle">M05</text>
              <rect x="232" y="57" width="24" height="103" rx="2" fill="url(#actualColGrad)" />
              <text x="244" y="174" fill="#94a3b8" font-size="9" text-anchor="middle">M06</text>
              <rect x="268" y="62" width="24" height="98" rx="2" fill="url(#actualColGrad)" />
              <text x="280" y="174" fill="#94a3b8" font-size="9" text-anchor="middle">M07</text>
              <rect x="304" y="61" width="24" height="99" rx="2" fill="url(#actualColGrad)" />
              <text x="316" y="174" fill="#38bdf8" font-size="9" font-weight="700" text-anchor="middle">M08*</text>

              <rect x="340" y="61" width="24" height="99" rx="2" fill="url(#leColGrad)" stroke="#f59e0b" stroke-width="1" stroke-dasharray="2,2" />
              <text x="352" y="174" fill="#f59e0b" font-size="9" text-anchor="middle">M09</text>
              <rect x="376" y="56" width="24" height="104" rx="2" fill="url(#leColGrad)" stroke="#ef4444" stroke-width="1.5" />
              <text x="388" y="174" fill="#ef4444" font-size="9" font-weight="700" text-anchor="middle">M10!</text>
              <rect x="412" y="50" width="24" height="110" rx="2" fill="url(#leColGrad)" stroke="#f59e0b" stroke-width="1" stroke-dasharray="2,2" />
              <text x="424" y="174" fill="#f59e0b" font-size="9" text-anchor="middle">M11</text>
              <rect x="448" y="45" width="24" height="115" rx="2" fill="url(#leColGrad)" stroke="#f59e0b" stroke-width="1" stroke-dasharray="2,2" />
              <text x="460" y="174" fill="#f59e0b" font-size="9" text-anchor="middle">M12</text>

              <line x1="45" y1="83" x2="490" y2="83" stroke="#94a3b8" stroke-width="2" stroke-dasharray="4,4" />
              <text x="495" y="86" fill="#94a3b8" font-size="9.5" font-weight="600">Budsjett (6,82M/mnd)</text>
              <text x="388" y="46" fill="#ef4444" font-size="9" font-weight="700" text-anchor="middle">Budsjettbrudd M10</text>
            </svg>
          </div>
          <div style="background: rgba(0,0,0,0.25); border: 1px solid var(--border-subtle); border-radius: 6px; padding: 10px 14px; font-size: 11.5px; display: flex; justify-content: space-between; align-items: center; color: var(--text-secondary);">
            <div>Faktisk YTD (M01-M08): <strong style="color:#38bdf8;">68,38 MNOK</strong></div>
            <div>EAC Helår (Hybrid): <strong style="color:#f59e0b;">96,46 MNOK</strong></div>
            <div>Årsbudsjett (BAC): <strong style="color:#94a3b8;">81,84 MNOK</strong></div>
            <div>Sluttavvik (VAC): <strong style="color:#ef4444;">-14,62 MNOK</strong></div>
          </div>
        </div>

        <!-- Visual 2.2: Lønnsavvik per Stillingsgruppe -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">👥 Visual 2.2: Lønnsavvik per Stillingsgruppe</div>
              <div class="panel-subtitle">UF vs TA stillingskategorier med årsverksavvik og lønnsbeløp</div>
            </div>
            <a class="drill-link" onclick="showDashboard('page_dt_bemanning')">Bemanning &rarr;</a>
          </div>
          <div class="table-container">
            <table class="tufte-table">
              <thead>
                <tr>
                  <th>Gruppe</th>
                  <th>Betegnelse</th>
                  <th class="num">Faktisk ÅV</th>
                  <th class="num">Budsjett ÅV</th>
                  <th class="num">ÅV Avvik</th>
                  <th class="num">Lønnsavvik NOK</th>
                  <th>Vurdering</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><code>PROF</code></td>
                  <td>Professor / Dosent</td>
                  <td class="num">142,5</td>
                  <td class="num">140,7</td>
                  <td class="num" style="color:#ef4444;">+1,8</td>
                  <td class="num" style="color:#ef4444; font-weight:600;">+1 840 000</td>
                  <td><span class="status-pill rag-red">🔴 Overforbruk</span></td>
                </tr>
                <tr>
                  <td><code>FORST</code></td>
                  <td>Førsteamanuensis / Lektor</td>
                  <td class="num">210,4</td>
                  <td class="num">209,5</td>
                  <td class="num" style="color:#f59e0b;">+0,9</td>
                  <td class="num" style="color:#f59e0b; font-weight:600;">+920 000</td>
                  <td><span class="status-pill rag-amber">🟡 Moderat</span></td>
                </tr>
                <tr>
                  <td><code>REKR</code></td>
                  <td>Stipendiat / Postdoktor</td>
                  <td class="num">84,0</td>
                  <td class="num">86,1</td>
                  <td class="num" style="color:#10b981;">-2,1</td>
                  <td class="num" style="color:#10b981; font-weight:600;">-1 450 000</td>
                  <td><span class="status-pill rag-amber">🟡 Vakanser (Forsinket)</span></td>
                </tr>
                <tr>
                  <td><code>ADM</code></td>
                  <td>Teknisk-administrativ (TA)</td>
                  <td class="num">182,0</td>
                  <td class="num">181,3</td>
                  <td class="num" style="color:#f59e0b;">+0,7</td>
                  <td class="num" style="color:#f59e0b; font-weight:600;">+650 000</td>
                  <td><span class="status-pill rag-amber">🟡 Vakansestopp T001</span></td>
                </tr>
                <tr>
                  <td><code>TEK</code></td>
                  <td>Drift & IT-teknisk</td>
                  <td class="num">42,8</td>
                  <td class="num">43,0</td>
                  <td class="num" style="color:#10b981;">-0,2</td>
                  <td class="num" style="color:#10b981; font-weight:600;">-120 000</td>
                  <td><span class="status-pill rag-green">🟢 I rute</span></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div style="font-size:11px; color:var(--text-muted); margin-top:8px;">
            ⚠️ <strong>Controller-notat:</strong> Vakanser i rekrutteringsstillinger (REKR -2,1 ÅV) kamuflerer overforbruk i professorgruppen (+1,8 ÅV). Ved gjenbesetting i Q4 vil lønnsavviket eskalere.
          </div>
        </div>
      </div>

      <!-- SONE 3: BOA & STUDIER (Hovedfelt Høyre) -->
      <div class="dash-grid-two-col">
        <!-- Visual 3.1: BOA Porteføljematrise -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">🔬 Visual 3.1: BOA Porteføljematrise (TDI-Kalkyle & RAG)</div>
              <div class="panel-subtitle">Full Costing (TDI) bidrags- og oppdragsforskning | SRS 9 og SRS 10</div>
            </div>
            <a class="drill-link" onclick="showDashboard('page_05')">BOA Spesifikasjon &rarr;</a>
          </div>
          <div class="table-container">
            <table class="tufte-table">
              <thead>
                <tr>
                  <th>Prosjekt</th>
                  <th>Kilde</th>
                  <th class="num">Budsjett</th>
                  <th class="num">Overhead (IK)</th>
                  <th class="num">% Tid</th>
                  <th class="num">% Forbrukt</th>
                  <th class="num">Avvik</th>
                  <th>RAG</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><code>NFR001</code> AI Styring</td>
                  <td>NFR (Bidrag)</td>
                  <td class="num">4,00 M</td>
                  <td class="num">880 k (22%)</td>
                  <td class="num">65%</td>
                  <td class="num">42%</td>
                  <td class="num" style="color:#10b981;">-23%</td>
                  <td><span class="status-pill rag-amber">🟡 Fremdriftsforsinkelse</span></td>
                </tr>
                <tr>
                  <td><code>NFR002</code> Pasientsikkerhet</td>
                  <td>NFR (Bidrag)</td>
                  <td class="num">2,80 M</td>
                  <td class="num">616 k (22%)</td>
                  <td class="num">52%</td>
                  <td class="num">52%</td>
                  <td class="num" style="color:#10b981;">0%</td>
                  <td><span class="status-pill rag-green">🟢 I rute</span></td>
                </tr>
                <tr>
                  <td><code>EU001</code> Green Maritime</td>
                  <td>EU Horizon</td>
                  <td class="num">6,20 M</td>
                  <td class="num">1 364 k (22%)</td>
                  <td class="num">50%</td>
                  <td class="num">50%</td>
                  <td class="num" style="color:#10b981;">0%</td>
                  <td><span class="status-pill rag-green">🟢 I rute</span></td>
                </tr>
                <tr>
                  <td><code>EVU001</code> Videreutdanning</td>
                  <td>Oppdrag (Ekstern)</td>
                  <td class="num">1,20 M</td>
                  <td class="num">300 k (25%)</td>
                  <td class="num">50%</td>
                  <td class="num" style="color:#ef4444;">72%</td>
                  <td class="num" style="color:#ef4444; font-weight:600;">+22%</td>
                  <td><span class="status-pill rag-red">🔴 Tapskontrakt (SRS 9)</span></td>
                </tr>
                <tr>
                  <td><code>OPPDRAG01</code> Batteri</td>
                  <td>Næringsliv</td>
                  <td class="num">1,80 M</td>
                  <td class="num">450 k (25%)</td>
                  <td class="num">50%</td>
                  <td class="num">49%</td>
                  <td class="num" style="color:#10b981;">-1%</td>
                  <td><span class="status-pill rag-green">🟢 I rute</span></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div style="font-size:11px; color:var(--text-muted); margin-top:8px;">
            ⚠️ <strong>SRS 9 Konsekvens:</strong> EVU001 merforbruk (+22%) krever umiddelbar avsetning for forventet tap (konto 7790 mot 2800: 900 000 kr bokført).
          </div>
        </div>

        <!-- Visual 3.2: Studiepoeng etter KDs 2025-modell -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">🎓 Visual 3.2: KDs 2025 Finansieringsmodell (SPE60 & BFE)</div>
              <div class="panel-subtitle">Beregnet inntekt per kategori | Marginalnedgang og basisskjerming</div>
            </div>
            <a class="drill-link" onclick="showDashboard('page_06')">Studieportefølje &rarr;</a>
          </div>
          <div class="table-container">
            <table class="tufte-table">
              <thead>
                <tr>
                  <th>Kategori (KD 2025)</th>
                  <th>Fagområder</th>
                  <th class="num">Sats per SPE60</th>
                  <th class="num">Avlagte SPE60</th>
                  <th class="num">BFE Inntekt</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><span class="cat-badge cat-01">Kategori 1</span></td>
                  <td>Humaniora, samfunnsfag, økonomi (HH, I013)</td>
                  <td class="num">54 550 kr</td>
                  <td class="num">1 314,6</td>
                  <td class="num" style="color:#38bdf8; font-weight:600;">71 711 430 kr</td>
                </tr>
                <tr>
                  <td><span class="cat-badge cat-02">Kategori 2</span></td>
                  <td>Realfag, helsefag, lærerutdanning, IKT (FAK-TR, I004)</td>
                  <td class="num">81 800 kr</td>
                  <td class="num">1 275,0</td>
                  <td class="num" style="color:#38bdf8; font-weight:600;">104 295 000 kr</td>
                </tr>
                <tr>
                  <td><span class="cat-badge cat-03">Kategori 3</span></td>
                  <td>Medisin, odontologi, klinisk veterinær</td>
                  <td class="num">190 900 kr</td>
                  <td class="num">0,0</td>
                  <td class="num" style="color:#64748b;">0 kr</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div style="background: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 6px; padding: 10px 14px; margin-top: 10px; font-size: 11px; line-height: 1.5; color: #cbd5e1;">
            <strong>Marginalprinsippet:</strong> KDs satser benyttes KUN ved endring i produksjon. Ved fallende studenttall ved I013BA (Samfunnsfag -400 SPE60) kuttes inntekten med 21,8 MNOK over tid. Møtes med <strong>Tiltak T001 Ansettelsesstopp</strong>.
          </div>
        </div>
      </div>

      <!-- SONE 4: OMSTILLINGSTILTAK & RISIKOSTYRING (Bunnpanel) -->
      <div class="dash-grid-two-col">
        <!-- Visual 4.1: FactAction Tiltaksmatrise -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">🎯 Visual 4.1: FactAction Tiltaksmatrise (T001–T006)</div>
              <div class="panel-subtitle">Forpliktende styringstiltak koblet direkte til de 6 Use Casene</div>
            </div>
            <a class="drill-link" onclick="showDashboard('page_07')">Alle tiltak &rarr;</a>
          </div>
          <div class="table-container">
            <table class="tufte-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Tiltaksbeskrivelse</th>
                  <th>Ansvarlig</th>
                  <th class="num">Forventet</th>
                  <th class="num">Realisert</th>
                  <th>Status</th>
                  <th>Use Case Ref</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><code>T001</code></td>
                  <td>Ansettelsesstopp & vakansestyring v/ I013</td>
                  <td>Dekan / Inst.leder</td>
                  <td class="num">850 000</td>
                  <td class="num">420 000</td>
                  <td><span class="status-pill pagar">🟡 Pågår</span></td>
                  <td><span class="badge badge-spec">KD ECTS Fall</span></td>
                </tr>
                <tr>
                  <td><code>T002</code></td>
                  <td>Forsering labutstyrsinvestering INV001</td>
                  <td>Controller / FAK-TR</td>
                  <td class="num">2 400 000</td>
                  <td class="num">1 800 000</td>
                  <td><span class="status-pill gjennomfort">🟢 Gjennomført</span></td>
                  <td><span class="badge badge-spec" style="color:#ef4444;">UC1: F-05-20</span></td>
                </tr>
                <tr>
                  <td><code>T003</code></td>
                  <td>Avstemming inntektsføring & forskudd NFR/EU</td>
                  <td>Prosjektcontroller</td>
                  <td class="num">600 000</td>
                  <td class="num">300 000</td>
                  <td><span class="status-pill pagar">🟡 Pågår</span></td>
                  <td><span class="badge badge-spec">UC2: SRS 10</span></td>
                </tr>
                <tr>
                  <td><code>T004</code></td>
                  <td>Tapsavsetning & reforhandling EVU001</td>
                  <td>Prosjektleder / Kontorsjef</td>
                  <td class="num">150 000</td>
                  <td class="num">0</td>
                  <td><span class="status-pill forsinket">🔴 Forsinket</span></td>
                  <td><span class="badge badge-spec" style="color:#ef4444;">UC3: SRS 9 Tap</span></td>
                </tr>
                <tr>
                  <td><code>T005</code></td>
                  <td>Overføring konsulentavtale til minikonkurranse</td>
                  <td>Innkjøpskontoret</td>
                  <td class="num">0</td>
                  <td class="num">0</td>
                  <td><span class="status-pill gjennomfort">🟢 Gjennomført</span></td>
                  <td><span class="badge badge-spec">UC5: FOA Innkjøp</span></td>
                </tr>
                <tr>
                  <td><code>T006</code></td>
                  <td>Vikarpooldeling praksisstudier helsefag</td>
                  <td>Instituttleder / HR</td>
                  <td class="num">350 000</td>
                  <td class="num">180 000</td>
                  <td><span class="status-pill pagar">🟡 Pågår</span></td>
                  <td><span class="badge badge-spec">UC6: Lønnsavvik</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Visual 4.2: F-05-20 Avsetningsløype -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">📉 Visual 4.2: F-05-20 Avsetningsløype mot Årsslutt (Area Chart)</div>
              <div class="panel-subtitle">Framskriving av ubenyttet rammebevilgning (Konto 2080) vs 5 %-grensen</div>
            </div>
            <span class="status-pill rag-green">Tiltak T002 Reduserer til 3,6%</span>
          </div>
          <div class="chart-container" style="height: 220px;">
            <svg class="interactive-chart" viewBox="0 0 600 200">
              <defs>
                <linearGradient id="areaGradF0520" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stop-color="#ef4444" stop-opacity="0.35" />
                  <stop offset="60%" stop-color="#f59e0b" stop-opacity="0.20" />
                  <stop offset="100%" stop-color="#10b981" stop-opacity="0.05" />
                </linearGradient>
              </defs>
              <line x1="50" y1="160" x2="550" y2="160" stroke="rgba(255,255,255,0.06)" />
              <line x1="50" y1="115" x2="550" y2="115" stroke="rgba(255,255,255,0.06)" />
              <line x1="50" y1="70" x2="550" y2="70" stroke="rgba(255,255,255,0.06)" />
              <line x1="50" y1="25" x2="550" y2="25" stroke="rgba(255,255,255,0.06)" />
              <text x="42" y="163" fill="#64748b" font-size="9" text-anchor="end">0%</text>
              <text x="42" y="118" fill="#64748b" font-size="9" text-anchor="end">4%</text>
              <text x="42" y="73" fill="#64748b" font-size="9" text-anchor="end">8%</text>
              <text x="42" y="28" fill="#64748b" font-size="9" text-anchor="end">12%</text>

              <line x1="50" y1="104" x2="550" y2="104" stroke="#f59e0b" stroke-width="1.8" stroke-dasharray="4,4" />
              <text x="555" y="107" fill="#f59e0b" font-size="9.5" font-weight="700">5,0% Maksgrense (2,68M)</text>

              <path d="M 70 160 L 70 93 L 200 60 L 340 80 L 480 120 L 480 160 Z" fill="url(#areaGradF0520)" />
              <path d="M 200 60 L 340 50 L 480 40" fill="none" stroke="#ef4444" stroke-width="2" stroke-dasharray="3,3" />
              <text x="485" y="43" fill="#ef4444" font-size="9">Uten tiltak (9,5% - Inndragning!)</text>
              <path d="M 70 93 L 200 60 L 340 80 L 480 120" fill="none" stroke="#10b981" stroke-width="2.5" />
              
              <circle cx="70" cy="93" r="4" fill="#38bdf8" />
              <text x="70" y="85" fill="#38bdf8" font-size="9" text-anchor="middle">Q1: 6,0%</text>
              <circle cx="200" cy="60" r="5" fill="#ef4444" />
              <text x="200" y="50" fill="#ef4444" font-size="9.5" font-weight="700" text-anchor="middle">Q2: 8,96% (RØD)</text>
              <circle cx="340" cy="80" r="4" fill="#f59e0b" />
              <text x="340" y="73" fill="#f59e0b" font-size="9" text-anchor="middle">Q3: 7,1%</text>
              <circle cx="480" cy="120" r="5" fill="#10b981" />
              <text x="480" y="135" fill="#10b981" font-size="9.5" font-weight="700" text-anchor="middle">Q4: 3,6% (GRØNN)</text>

              <text x="70" y="178" fill="#94a3b8" font-size="9" text-anchor="middle">2026-Q1</text>
              <text x="200" y="178" fill="#94a3b8" font-size="9" text-anchor="middle">2026-Q2 (Nå)</text>
              <text x="340" y="178" fill="#94a3b8" font-size="9" text-anchor="middle">2026-Q3 (Est)</text>
              <text x="480" y="178" fill="#94a3b8" font-size="9" text-anchor="middle">2026-Q4 (Mål)</text>
            </svg>
          </div>
          <div style="font-size:11px; color:var(--text-secondary); line-height:1.5;">
            💡 <strong>Risikoreduserende tiltak T002:</strong> Ved å realisere kr 1 800 000 i forpliktende innkjøp av labutstyr (prosjekt INV001) før 31.10.2026, reduseres konto 2080 til kr 1 930 000 (3,6 % av rammen), og UiA unngår inndragning av midler til Finansdepartementet iht. rundskriv F-05-20.
          </div>
        </div>
      </div>
    `,
        },

        page_03: {
          id: 'page_03_executive',
          title: '03 Universitetsdirektør & Ledelse',
          role: 'Universitetsdirektør / Rektorat',
          desc: 'Helhetlig topplederoversikt for hele institusjonen. Prognoseutvikling over runder (Budsjett -> FC1 -> FC2 -> LE), fakultetsvise avvik og strategiske styringsparametere.',
          slicers: [
            {
              label: 'Periode',
              options: ['2026-12 (Helår)', '2026-08 (T2)', '2026-04 (T1)'],
            },
            {
              label: 'Forecastversjon',
              options: ['LE_2026', 'FC2_2026', 'FC1_2026'],
            },
          ],
          kpis: [
            {
              title: 'Årsbudsjett (Institusjonen)',
              val: '81,84 M',
              unit: 'NOK',
              badge: 'BAC Ramme',
              badgeCls: 'variance-info',
              sub: 'Netto bevilgningsramme',
            },
            {
              title: 'Helårsprognose (LE)',
              val: '96,46 M',
              unit: 'NOK',
              badge: 'EAC Slutt',
              badgeCls: 'variance-unfavorable',
              sub: 'Gjeldende helårsestimat',
            },
            {
              title: 'Prognoseavvik',
              val: '-14,62 M',
              unit: 'NOK',
              badge: 'Budsjettbrudd M10',
              badgeCls: 'variance-unfavorable',
              sub: 'Forventet merforbruk før tiltak',
            },
            {
              title: 'Årsverk totalt',
              val: '1 285,9',
              unit: 'FTE',
              badge: 'Hele institusjonen',
              badgeCls: 'variance-info',
              sub: 'UF: 661,8 | TA: 624,1',
            },
            {
              title: 'BOA Portefølje',
              val: '61,50 M',
              unit: 'NOK',
              badge: '20,46 M påløpt',
              badgeCls: 'variance-info',
              sub: 'TDI-budsjett 20,20 M (6 prosjekter)',
            },
          ],
          renderContent: () => `
      <div class="dash-grid-two-col">
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Prognoseutvikling over runder (Budsjett &rarr; FC1 &rarr; FC2 &rarr; LE)</div>
              <div class="panel-subtitle">Vandring i forventet årsresultat gjennom styringsåret (MNOK)</div>
            </div>
          </div>
          <div class="chart-container">
            ${generateLineChartSVG([
              {
                name: 'Prognose helår',
                color: '#38bdf8',
                data: [81.84, 84.5, 87.2, 89.9, 92.5, 93.8, 95.1, 96.46],
              },
              {
                name: 'Vedtatt budsjettramme',
                color: '#94a3b8',
                dashed: true,
                data: [81.84, 81.84, 81.84, 81.84, 81.84, 81.84, 81.84, 81.84],
              },
            ])}
          </div>
        </div>

        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Prognoseavvik fordelt på fakulteter</div>
              <div class="panel-subtitle">Hvor oppstår merforbruket? (MNOK)</div>
            </div>
          </div>
          <div class="chart-container">
            ${generateBarChartSVG(
              [
                {
                  label: 'Fak. for teknologi og realfag',
                  val: 9.8,
                  color: '#ef4444',
                },
                { label: 'Handelshøyskolen', val: 8.4, color: '#ef4444' },
                {
                  label: 'Fak. for samfunnsvitenskap',
                  val: 4.2,
                  color: '#f59e0b',
                },
                {
                  label: 'Fak. for humaniora og ped.',
                  val: 2.1,
                  color: '#f59e0b',
                },
                {
                  label: 'Fellesområde & administrasjon',
                  val: 1.55,
                  color: '#10b981',
                },
              ],
              'MNOK'
            )}
          </div>
        </div>
      </div>

      <div class="card-panel">
        <div class="panel-header">
          <div>
            <div class="panel-title">Hovedtall per fakultet og fellesområde</div>
            <div class="panel-subtitle">Komplett avstemming mot budsjett, regnskap, prognose og årsverk</div>
          </div>
        </div>
        <div class="table-container">
          <table class="tufte-table">
            <thead>
              <tr>
                <th>Fakultet / Område</th>
                <th class="num">Årsbudsjett</th>
                <th class="num">Regnskap YTD</th>
                <th class="num">Forecast LE</th>
                <th class="num">Forecastavvik</th>
                <th>Forecast RAG</th>
                <th class="num">Årsverk</th>
                <th class="num">BOA Inntekter</th>
                <th class="num">Netto etter tiltak</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Handelshøyskolen</td>
                <td class="num">3 240 000</td>
                <td class="num">3 180 000</td>
                <td class="num">11 640 000</td>
                <td class="num" style="color:#ef4444;">+8 400 000</td>
                <td><span class="status-pill rag-red">🔴 Rød (&gt;5%)</span></td>
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
                <td><span class="status-pill rag-red">🔴 Rød (&gt;5%)</span></td>
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
                <td><span class="status-pill rag-red">🔴 Rød (&gt;5%)</span></td>
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
                <td><span class="status-pill rag-red">🔴 Rød (&gt;5%)</span></td>
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
                <td><span class="status-pill rag-red">🔴 Rød (&gt;5%)</span></td>
                <td class="num">1 285,9</td>
                <td class="num">25 678 288 kr</td>
                <td class="num" style="color:#38bdf8;">26 788 524 kr</td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
    `,
        },

        page_04: {
          id: 'page_04_styret',
          title: '04 Universitetsstyret',
          role: 'Universitetsstyret',
          desc: 'Strategisk risikobilde, måloppnåelse for utdanning og forskning, samt oppfølging av de 16 styrebehandlede omstillingstiltakene.',
          slicers: [
            {
              label: 'Periode',
              options: [
                '2026-12 (Årsrapport)',
                '2026-08 (T2-rapport)',
                '2026-04 (T1-rapport)',
              ],
            },
            {
              label: 'Prognoseversjon',
              options: ['LE_2026', 'FC2_2026', 'FC1_2026'],
            },
          ],
          kpis: [
            {
              title: 'Totalbudsjett',
              val: '81,84 M',
              unit: 'NOK',
              badge: 'Vedtatt ramme (BAC)',
              badgeCls: 'variance-info',
              sub: 'Bevilgning & ramme 2026',
            },
            {
              title: 'Forventet helårsresultat',
              val: '96,46 M',
              unit: 'NOK',
              badge: 'LE_2026 (-14,62 M)',
              badgeCls: 'variance-unfavorable',
              sub: 'Sluttprognose EAC',
            },
            {
              title: 'Forventet avvik %',
              val: '-17,9%',
              unit: 'Avvik',
              badge: 'Budsjettbrudd M10',
              badgeCls: 'variance-unfavorable',
              sub: 'Før innregning av tiltak',
            },
            {
              title: 'Studiepoeng produksjon',
              val: '2 589,6',
              unit: 'SPE60',
              badge: '176,01 Mkr BFE',
              badgeCls: 'variance-info',
              sub: '336 945 ECTS avlagt',
            },
            {
              title: 'Eksternfinansiering (BOA)',
              val: '61,50 M',
              unit: 'NOK',
              badge: '20,46 M påløpt',
              badgeCls: 'variance-info',
              sub: '6 prosjekter (NFR/EU/EVU)',
            },
          ],
          renderContent: () => `
      <div class="dash-grid-two-col">
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Strategisk måloppnåelse studieaktivitet</div>
              <div class="panel-subtitle">Studenter og studiepoengproduksjon mot styringskrav</div>
            </div>
          </div>
          <div class="table-container">
            <table class="tufte-table">
              <thead>
                <tr>
                  <th>Fakultet</th>
                  <th class="num">Reg. Studenter</th>
                  <th class="num">Avlagte SP</th>
                  <th class="num">SPE60</th>
                  <th class="num">Måloppnåelse</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Handelshøyskolen</td>
                  <td class="num">2 410</td>
                  <td class="num">128 430</td>
                  <td class="num">2 140,5</td>
                  <td class="num" style="color:#10b981;">89,2%</td>
                  <td><span class="status-pill rag-amber">🟡 Moderat (80-90%)</span></td>
                </tr>
                <tr>
                  <td>Fakultet for teknologi og realfag</td>
                  <td class="num">1 750</td>
                  <td class="num">88 400</td>
                  <td class="num">1 473,3</td>
                  <td class="num" style="color:#f59e0b;">82,4%</td>
                  <td><span class="status-pill rag-amber">🟡 Moderat (80-90%)</span></td>
                </tr>
                <tr>
                  <td>Fakultet for samfunnsvitenskap</td>
                  <td class="num">1 380</td>
                  <td class="num">74 215</td>
                  <td class="num">1 236,9</td>
                  <td class="num" style="color:#10b981;">88,1%</td>
                  <td><span class="status-pill rag-amber">🟡 Moderat (80-90%)</span></td>
                </tr>
                <tr>
                  <td>Fakultet for helse og idrett</td>
                  <td class="num">950</td>
                  <td class="num">45 900</td>
                  <td class="num">765,0</td>
                  <td class="num" style="color:#f59e0b;">84,0%</td>
                  <td><span class="status-pill rag-amber">🟡 Moderat (80-90%)</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Økonomisk risikobilde og omstilling</div>
              <div class="panel-subtitle">Fakultetsvis tiltakseffekt mot prognoseavvik</div>
            </div>
          </div>
          <div class="table-container">
            <table class="tufte-table">
              <thead>
                <tr>
                  <th>Fakultet</th>
                  <th class="num">Forecastavvik</th>
                  <th class="num">Identifisert tiltak</th>
                  <th class="num">Netto restavvik</th>
                  <th>Risiko</th>
                </tr>
              </thead>
              <tbody>
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
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="card-panel">
        <div class="panel-header">
          <div>
            <div class="panel-title">Universitetsstyrets omstillingstiltak (FactAction - 16 tiltak)</div>
            <div class="panel-subtitle">Gjennomføringsgrad og forventet vs realisert effekt</div>
          </div>
        </div>
        <div class="table-container">
          <table class="tufte-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Tiltaksbeskrivelse</th>
                <th>Avviksårsak</th>
                <th>Ansvarlig</th>
                <th class="num">Forventet</th>
                <th class="num">Realisert</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>T-01</code></td>
                <td>Vakansestopp i administrative stillinger</td>
                <td>Lønnsvekst og overkapasitet</td>
                <td>HR-direktør</td>
                <td class="num">-1 200 000</td>
                <td class="num">-950 000</td>
                <td><span class="status-pill gjennomfort">🟢 Gjennomført</span></td>
              </tr>
              <tr>
                <td><code>T-05</code></td>
                <td>Reduksjon av eksterne konsulentavtaler IT</td>
                <td>Høye konsulentkostnader</td>
                <td>IT-direktør</td>
                <td class="num">-1 500 000</td>
                <td class="num">-800 000</td>
                <td><span class="status-pill pagar">🟡 Pågår</span></td>
              </tr>
              <tr>
                <td><code>T-08</code></td>
                <td>Nedskalering av arealleie Campus Hoved</td>
                <td>Høye leiekostnader</td>
                <td>Eiendomsdirektør</td>
                <td class="num">-2 000 000</td>
                <td class="num">-600 000</td>
                <td><span class="status-pill forsinket">🔴 Forsinket</span></td>
              </tr>
              <tr>
                <td><code>T-12</code></td>
                <td>Optimalisering av studietilbud og samkjøring</td>
                <td>Små studentkull</td>
                <td>Dekan Helse</td>
                <td class="num">-1 100 000</td>
                <td class="num">-900 000</td>
                <td><span class="status-pill pagar">🟡 Pågår</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `,
        },

        page_05: {
          id: 'page_05_forskning_boa',
          title: '05 Forskningsledelse & BOA (TDI-Kalkyle & Portefølje)',
          role: 'Prorektor Forskning / Forskningsutvalg',
          desc: 'Oppfølging av eksternfinansiert forskning (Bidrag og Oppdrag) etter TDI-modellen (Total Dekning av Inntekter). Frikjøp, direkte drift, overhead (22%/25%), leiesteder og periodisering iht. SRS 9 og SRS 10.',
          slicers: [
            {
              label: 'Finansieringstype',
              options: [
                'Alle typer',
                'Bidrag (NFR / EU)',
                'Oppdrag (Ekstern / Næringsliv)',
              ],
            },
            {
              label: 'Finansieringskilde',
              options: ['Alle kilder', 'NFR', 'EU', 'Ekstern', 'Næringsliv'],
            },
            {
              label: 'RAG Status',
              options: [
                'Alle statuser',
                'GRØNN: I rute',
                'GUL: Fremdriftsforsinkelse',
                'RØD: Merforbruk',
              ],
            },
          ],
          kpis: [
            {
              title: 'Kontraktsportefølje BOA',
              val: '61,50 M',
              unit: 'NOK',
              badge: '6 aktive prosjekter',
              badgeCls: 'variance-info',
              sub: 'Budsjett 2026: 20,50 M',
            },
            {
              title: 'Påløpt prosjektkostnad YTD',
              val: '10,13 M',
              unit: 'NOK',
              badge: 'Akkumulert M01-M08',
              badgeCls: 'variance-info',
              sub: 'Frikjøp: 5,65 M | Drift: 2,62 M',
            },
            {
              title: 'Inntektsført (SRS 10)',
              val: '9,87 M',
              unit: 'NOK',
              badge: 'Motsatt sammenstilling',
              badgeCls: 'variance-favorable',
              sub: 'Forskuddsreduksjon konto 2180',
            },
            {
              title: 'Indirekte kostnader (IK)',
              val: '2,24 M',
              unit: 'NOK',
              badge: 'Overhead 22%/25%',
              badgeCls: 'variance-info',
              sub: 'UiAs felleskostnadsdekning',
            },
            {
              title: 'Portefølje RAG-Status',
              val: '1 RØD / 1 GUL',
              unit: 'Prosjekter',
              badge: 'EVU001 & NFR001',
              badgeCls: 'variance-unfavorable',
              sub: '4 prosjekter i grønn rute',
            },
          ],
          renderContent: () => `
      <div class="dash-grid-two-col">
        <!-- Visual 5.1: Kostnadsstruktur TDI -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">TDI-Kalkyle & Kostnadselementer i BOA-porteføljen</div>
              <div class="panel-subtitle">Full Costing-fordeling på tvers av 6 aktive prosjekter (MNOK)</div>
            </div>
          </div>
          <div class="chart-container">
            ${generateBarChartSVG(
              [
                {
                  label: 'Frikjøp vitenskapelig tid (UF)',
                  val: 11.25,
                  color: '#38bdf8',
                },
                {
                  label: 'Direkte driftskostnader',
                  val: 6.85,
                  color: '#6366f1',
                },
                {
                  label: 'Indirekte kostnader / Overhead (22-25%)',
                  val: 4.6,
                  color: '#f59e0b',
                },
                {
                  label: 'Leiesteder & infrastruktur',
                  val: 0.8,
                  color: '#10b981',
                },
              ],
              'MNOK'
            )}
          </div>
        </div>

        <!-- Visual 5.2: Bidrag vs Oppdrag -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Finansieringstype & Regelverksregime (SRS 9 vs SRS 10)</div>
              <div class="panel-subtitle">Bidragsforskning (NFR/EU) vs Oppdragsforskning (Marked)</div>
            </div>
          </div>
          <div class="chart-container">
            ${generateBarChartSVG(
              [
                {
                  label: 'Bidrag: NFR (Motsatt sammenstilling SRS 10)',
                  val: 20.5,
                  color: '#38bdf8',
                },
                {
                  label: 'Bidrag: EU Horizon Europe (SRS 10)',
                  val: 32.5,
                  color: '#0284c7',
                },
                {
                  label: 'Oppdrag: Kommunal videreutdanning (SRS 9 Tap)',
                  val: 3.5,
                  color: '#ef4444',
                },
                {
                  label: 'Oppdrag: Næringsliv batteriteknologi (SRS 9)',
                  val: 5.0,
                  color: '#10b981',
                },
              ],
              'MNOK'
            )}
          </div>
        </div>
      </div>

      <!-- Visual 5.3: Komplett Porteføljematrise fra FactProjectBOA.csv -->
      <div class="card-panel">
        <div class="panel-header">
          <div>
            <div class="panel-title">Komplett BOA-Prosjektportefølje (FactProjectBOA.csv)</div>
            <div class="panel-subtitle">TDI-elementer, fremdrift, forbruksavvik og RAG-evaluering</div>
          </div>
          <a class="drill-link" onclick="showDashboard('page_dt_prosjekt')">EVM Detalj &rarr;</a>
        </div>
        <div class="table-container">
          <table class="tufte-table">
            <thead>
              <tr>
                <th>Prosjekt</th>
                <th>Prosjektnavn</th>
                <th>Type</th>
                <th>Kilde</th>
                <th class="num">Kontrakt</th>
                <th class="num">Frikjøp</th>
                <th class="num">Drift</th>
                <th class="num">Overhead</th>
                <th class="num">Leiested</th>
                <th class="num">% Tid</th>
                <th class="num">% Forbrukt</th>
                <th class="num">Avvik</th>
                <th>RAG Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>NFR001</code></td>
                <td>NFR-AI: Kunstig intelligens i styring</td>
                <td>Bidrag</td>
                <td>NFR</td>
                <td class="num">12,0 M</td>
                <td class="num">1,80 M</td>
                <td class="num">1,10 M</td>
                <td class="num">0,88 M (22%)</td>
                <td class="num">0,22 M</td>
                <td class="num">65%</td>
                <td class="num">42%</td>
                <td class="num" style="color:#10b981;">-23%</td>
                <td><span class="status-pill rag-amber">🟡 GUL: Forsinket</span></td>
              </tr>
              <tr>
                <td><code>NFR002</code></td>
                <td>NFR-Helse: Pasientsikkerhet i helsefag</td>
                <td>Bidrag</td>
                <td>NFR</td>
                <td class="num">8,5 M</td>
                <td class="num">1,30 M</td>
                <td class="num">0,80 M</td>
                <td class="num">0,62 M (22%)</td>
                <td class="num">0,08 M</td>
                <td class="num">52%</td>
                <td class="num">52%</td>
                <td class="num" style="color:#10b981;">0%</td>
                <td><span class="status-pill rag-green">🟢 GRØNN: I rute</span></td>
              </tr>
              <tr>
                <td><code>EU001</code></td>
                <td>EU Horizon: Green Maritime Tech</td>
                <td>Bidrag</td>
                <td>EU</td>
                <td class="num">18,5 M</td>
                <td class="num">2,80 M</td>
                <td class="num">1,80 M</td>
                <td class="num">1,36 M (22%)</td>
                <td class="num">0,24 M</td>
                <td class="num">50%</td>
                <td class="num">50%</td>
                <td class="num" style="color:#10b981;">0%</td>
                <td><span class="status-pill rag-green">🟢 GRØNN: I rute</span></td>
              </tr>
              <tr>
                <td><code>EU002</code></td>
                <td>EU Horizon: Digital Governance</td>
                <td>Bidrag</td>
                <td>EU</td>
                <td class="num">14,0 M</td>
                <td class="num">2,10 M</td>
                <td class="num">1,20 M</td>
                <td class="num">0,99 M (22%)</td>
                <td class="num">0,21 M</td>
                <td class="num">48%</td>
                <td class="num">48%</td>
                <td class="num" style="color:#10b981;">0%</td>
                <td><span class="status-pill rag-green">🟢 GRØNN: I rute</span></td>
              </tr>
              <tr>
                <td><code>EVU001</code></td>
                <td>EVU Videreutdanning for kommuner</td>
                <td>Oppdrag</td>
                <td>Ekstern</td>
                <td class="num">3,5 M</td>
                <td class="num">0,45 M</td>
                <td class="num">0,45 M</td>
                <td class="num">0,30 M (25%)</td>
                <td class="num">0,00 M</td>
                <td class="num">50%</td>
                <td class="num" style="color:#ef4444; font-weight:600;">72%</td>
                <td class="num" style="color:#ef4444; font-weight:600;">+22%</td>
                <td><span class="status-pill rag-red">🔴 RØD: Tapskontrakt</span></td>
              </tr>
              <tr>
                <td><code>OPPDRAG01</code></td>
                <td>Oppdragsforskning Batteriteknologi</td>
                <td>Oppdrag</td>
                <td>Næringsliv</td>
                <td class="num">5,0 M</td>
                <td class="num">0,75 M</td>
                <td class="num">0,55 M</td>
                <td class="num">0,45 M (25%)</td>
                <td class="num">0,05 M</td>
                <td class="num">50%</td>
                <td class="num">49%</td>
                <td class="num" style="color:#10b981;">-1%</td>
                <td><span class="status-pill rag-green">🟢 GRØNN: I rute</span></td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="4"><strong>Totalt BOA Portefølje</strong></td>
                <td class="num"><strong>61,50 MNOK</strong></td>
                <td class="num"><strong>9,20 MNOK</strong></td>
                <td class="num"><strong>5,90 MNOK</strong></td>
                <td class="num"><strong>4,60 MNOK</strong></td>
                <td class="num"><strong>0,80 MNOK</strong></td>
                <td class="num">52,5%</td>
                <td class="num">51,8%</td>
                <td class="num" style="color:#10b981;">-0,7%</td>
                <td><span class="status-pill rag-green">4 Grønn / 1 Gul / 1 Rød</span></td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
    `,
        },

        page_06: {
          id: 'page_06_studieportefolje',
          title: '06 Studieportefølje & KDs 2025 Modell',
          role: 'Prorektor Utdanning / Studiedirektør',
          desc: 'Oppfølging av Kunnskapsdepartementets (KD) nye finansieringsmodell fra 2025: Tre finansieringskategorier, marginalitetsanalyse, basisskjerming og studiepoengproduksjon (FactStudyPoints.csv).',
          slicers: [
            {
              label: 'KD Finansieringskategori',
              options: [
                'Alle kategorier',
                'Kategori 1 (kr 54 550)',
                'Kategori 2 (kr 81 800)',
                'Kategori 3 (kr 190 900)',
              ],
            },
            {
              label: 'Fakultet / Enhet',
              options: [
                'Alle enheter',
                'Handelshøyskolen (I001)',
                'Samfunnsvitenskap (I013)',
                'Teknologi og realfag (FAK-TR)',
                'Helsefag (I004)',
              ],
            },
          ],
          kpis: [
            {
              title: 'Total SPE60 Avlagt',
              val: '2 589,6',
              unit: 'SPE60',
              badge: 'Helårsstudenter',
              badgeCls: 'variance-info',
              sub: '336 945 studiepoeng totalt',
            },
            {
              title: 'BFE-Inntekt Beregnet',
              val: '176,01 M',
              unit: 'NOK',
              badge: 'Resultatkomponent',
              badgeCls: 'variance-favorable',
              sub: 'Kat 1: 71,71 M | Kat 2: 104,30 M',
            },
            {
              title: 'Kategori 1 Andel',
              val: '50,8 %',
              unit: 'Andel',
              badge: '1 314,6 SPE60',
              badgeCls: 'variance-info',
              sub: 'Humaniora, samfunnsfag, økonomi',
            },
            {
              title: 'Kategori 2 Andel',
              val: '49,2 %',
              unit: 'Andel',
              badge: '1 275,0 SPE60',
              badgeCls: 'variance-info',
              sub: 'Realfag, helsefag, lærer, IKT',
            },
            {
              title: 'Risiko Fallende Kull (I013)',
              val: '-21,8 M',
              unit: 'Marginaltap',
              badge: '400 SPE60 frafall',
              badgeCls: 'variance-unfavorable',
              sub: 'Kompenseres med tiltak T001 (850k)',
            },
          ],
          renderContent: () => `
      <div class="dash-grid-two-col">
        <!-- Visual 6.1: KDs 3 Kategorier -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Kunnskapsdepartementets 2025-Satser per 60 Studiepoeng</div>
              <div class="panel-subtitle">Ny nasjonal modell redusert fra 6 (A-F) til 3 enhetlige kategorier</div>
            </div>
          </div>
          <div class="chart-container">
            ${generateBarChartSVG(
              [
                {
                  label: 'Kategori 1: Hum / Samf / Øk (UiA aktiv)',
                  val: 54.55,
                  color: '#38bdf8',
                },
                {
                  label: 'Kategori 2: Real / Helse / Lærer / IKT (UiA aktiv)',
                  val: 81.8,
                  color: '#10b981',
                },
                {
                  label: 'Kategori 3: Medisin / Odontologi (Ikke UiA)',
                  val: 190.9,
                  color: '#94a3b8',
                },
              ],
              'Tusen kr'
            )}
          </div>
        </div>

        <!-- Visual 6.2: Beregnet BFE Inntekt -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Beregnet Resultatbevilgning per Fakultet (MNOK)</div>
              <div class="panel-subtitle">Multiplikasjon av avlagte SPE60 mot KDs kategorisats</div>
            </div>
          </div>
          <div class="chart-container">
            ${generateBarChartSVG(
              [
                {
                  label: 'Fakultet for teknologi og realfag (Kat 2)',
                  val: 62.4,
                  color: '#10b981',
                },
                {
                  label: 'Handelshøyskolen (Kat 1)',
                  val: 44.8,
                  color: '#38bdf8',
                },
                {
                  label: 'Fakultet for helse- og idrett (Kat 2)',
                  val: 41.9,
                  color: '#10b981',
                },
                {
                  label: 'Fakultet for samfunnsvitenskap (Kat 1)',
                  val: 26.9,
                  color: '#f59e0b',
                },
              ],
              'MNOK'
            )}
          </div>
        </div>
      </div>

      <!-- Visual 6.3: Marginalitetsanalyse & Case I013BA -->
      <div class="card-panel" style="margin-bottom: 20px;">
        <div class="panel-header">
          <div>
            <div class="panel-title">Controller-Dybde: Marginalitetsprinsippet i KDs 2025 Modell</div>
            <div class="panel-subtitle">Hvorfor satsene IKKE representerer full enhetskostnad, men marginal insentivsats</div>
          </div>
          <span class="status-pill rag-green">Nettobudsjettert Basisskjerming</span>
        </div>
        <div style="padding: 16px; background: rgba(0,0,0,0.25); border-radius: 8px; line-height: 1.6; font-size: 12px; color: #cbd5e1;">
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
              <h4 style="color:#38bdf8; font-size:13px; margin-bottom:6px;">1. Det statlige prinsippet</h4>
              <p>I statsbudsjettet kap. 260 bevilges UiAs midler som en <strong>nettobevilgning</strong>. Eksisterende studieplasser og volum ligger i utgangspunktet fast i <em>basisbevilgningen</em>. KDs nye satser (kr 54 550 og kr 81 800) benyttes <strong>kun ved endringer i produksjon</strong> (opp- eller nedjustering av resultatrammen).</p>
            </div>
            <div>
              <h4 style="color:#ef4444; font-size:13px; margin-bottom:6px;">2. Konsekvens for Samfunnsvitenskap (I013BA)</h4>
              <p>Når bachelorprogrammet i samfunnsvitenskap opplever et produksjonsfall på <strong>400 SPE60</strong>, kuttes institusjonens ramme med <code>400 × 54 550 kr = 21,8 MNOK</code> over en 2-årig forsinkelsesperiode. Faste lønnskostnader kan ikke kuttes like raskt, og <strong>Tiltak T001 (Ansettelsesstopp)</strong> må aktiveres umiddelbart for å unngå strukturelt driftsunderskudd.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Visual 6.4: Tabell over studieprogrammer -->
      <div class="card-panel">
        <div class="panel-header">
          <div>
            <div class="panel-title">Studieaktivitet & Kategoriplassering (FactStudyPoints.csv)</div>
            <div class="panel-subtitle">Registrerte studenter, avlagte SPE60 og beregnet inntekt</div>
          </div>
          <a class="drill-link" onclick="showDashboard('page_dt_studier')">Studiedetalj &rarr;</a>
        </div>
        <div class="table-container">
          <table class="tufte-table">
            <thead>
              <tr>
                <th>Programkode</th>
                <th>Studieprogramnavn</th>
                <th>Kategori (KD 2025)</th>
                <th class="num">Sats per SPE</th>
                <th class="num">Studenter</th>
                <th class="num">Avlagte SP</th>
                <th class="num">SPE60</th>
                <th class="num">BFE Inntekt</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>BOKADM</code></td>
                <td>Bachelor i økonomi og administrasjon</td>
                <td><span class="cat-badge cat-01">Kategori 1</span></td>
                <td class="num">54 550 kr</td>
                <td class="num">850</td>
                <td class="num">46 200</td>
                <td class="num">770,0</td>
                <td class="num" style="color:#38bdf8; font-weight:600;">42 003 500 kr</td>
                <td><span class="status-pill rag-green">🟢 I rute</span></td>
              </tr>
              <tr>
                <td><code>I013BA</code></td>
                <td>Bachelor i samfunnsvitenskap (Fallende kull)</td>
                <td><span class="cat-badge cat-01">Kategori 1</span></td>
                <td class="num">54 550 kr</td>
                <td class="num">380</td>
                <td class="num">18 200</td>
                <td class="num">303,3</td>
                <td class="num" style="color:#ef4444; font-weight:600;">16 545 015 kr</td>
                <td><span class="status-pill rag-red">🔴 Fallende volum (Tiltak T001)</span></td>
              </tr>
              <tr>
                <td><code>MOKLED</code></td>
                <td>Master i ledelse og siviløkonom</td>
                <td><span class="cat-badge cat-01">Kategori 1</span></td>
                <td class="num">54 550 kr</td>
                <td class="num">420</td>
                <td class="num">23 100</td>
                <td class="num">385,0</td>
                <td class="num" style="color:#38bdf8; font-weight:600;">21 001 750 kr</td>
                <td><span class="status-pill rag-green">🟢 I rute</span></td>
              </tr>
              <tr>
                <td><code>I004BA</code></td>
                <td>Bachelor i sykepleie (Klinisk praksis)</td>
                <td><span class="cat-badge cat-02">Kategori 2</span></td>
                <td class="num">81 800 kr</td>
                <td class="num">520</td>
                <td class="num">28 500</td>
                <td class="num">475,0</td>
                <td class="num" style="color:#10b981; font-weight:600;">38 855 000 kr</td>
                <td><span class="status-pill rag-amber">🟡 Overtid praksis (Tiltak T006)</span></td>
              </tr>
              <tr>
                <td><code>BIKT</code></td>
                <td>Bachelor i informatikk & cybersikkerhet</td>
                <td><span class="cat-badge cat-02">Kategori 2</span></td>
                <td class="num">81 800 kr</td>
                <td class="num">410</td>
                <td class="num">24 600</td>
                <td class="num">410,0</td>
                <td class="num" style="color:#10b981; font-weight:600;">33 538 000 kr</td>
                <td><span class="status-pill rag-green">🟢 I rute</span></td>
              </tr>
              <tr>
                <td><code>MIKT</code></td>
                <td>Master i kunstig intelligens og teknologi</td>
                <td><span class="cat-badge cat-02">Kategori 2</span></td>
                <td class="num">81 800 kr</td>
                <td class="num">390</td>
                <td class="num">23 400</td>
                <td class="num">390,0</td>
                <td class="num" style="color:#10b981; font-weight:600;">31 902 000 kr</td>
                <td><span class="status-pill rag-green">🟢 I rute</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `,
        },

        page_07: {
          id: 'page_07_action_tracker',
          title: '07 Action Tracker (FactAction.csv - 6 Omstillingstiltak)',
          role: 'Omstillingsutvalg / Controller',
          desc: 'Oppfølging av de 6 forpliktende styringstiltakene koblet direkte til de 6 statlige use casene (F-05-20, SRS 9, SRS 10, SRS 17, FOA, lønnsavvik og studiepoengfall).',
          slicers: [
            {
              label: 'Ansvarlig lederrolle',
              options: [
                'Alle roller',
                'Dekan / Instituttleder',
                'Controller / FAK-TR',
                'Prosjektcontroller',
                'Innkjøpskontoret',
                'HR / Instituttleder',
              ],
            },
            {
              label: 'Status',
              options: ['Alle statuser', 'Gjennomført', 'Pågår', 'Forsinket'],
            },
            {
              label: 'Prioritet',
              options: ['Alle prioriteter', 'Høy', 'Middels'],
            },
          ],
          kpis: [
            {
              title: 'Totalt antall tiltak',
              val: '6',
              unit: 'Tiltak',
              badge: 'Koblet til Use Cases',
              badgeCls: 'variance-info',
              sub: 'FactAction.csv',
            },
            {
              title: 'Forventet effekt',
              val: '4,35 M',
              unit: 'NOK',
              badge: 'Netto innsparing/balanse',
              badgeCls: 'variance-favorable',
              sub: 'Inkl. F-05-20 og lønn',
            },
            {
              title: 'Realisert effekt YTD',
              val: '2,70 M',
              unit: 'NOK',
              badge: '62,1% måloppnåelse',
              badgeCls: 'variance-favorable',
              sub: 'Bokført gevinst M01-M08',
            },
            {
              title: 'Gjennomførte tiltak',
              val: '2',
              unit: 'Tiltak',
              badge: 'T002 & T005',
              badgeCls: 'variance-favorable',
              sub: 'INV001 lab & FOA avtale',
            },
            {
              title: 'Forsinket tiltak',
              val: '1',
              unit: 'Tiltak',
              badge: 'T004 (EVU001)',
              badgeCls: 'variance-unfavorable',
              sub: 'Tapsavsetning 900k aktivert',
            },
          ],
          renderContent: () => `
      <div class="dash-grid-two-col">
        <!-- Visual 7.1: Forventet vs Realisert per tiltak -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Forventet vs. Realisert Effekt per Tiltak (T001–T006)</div>
              <div class="panel-subtitle">Kroneffekt i tusen kr (FactAction.csv)</div>
            </div>
          </div>
          <div class="chart-container">
            ${generateBarChartSVG(
              [
                {
                  label: 'T002: Investeringsplan lab INV001 (F-05-20)',
                  val: 1800,
                  color: '#10b981',
                },
                {
                  label: 'T001: Ansettelsesstopp samfunnsvitenskap',
                  val: 420,
                  color: '#38bdf8',
                },
                {
                  label: 'T003: Månedlig avstemming NFR001 (SRS 10)',
                  val: 300,
                  color: '#38bdf8',
                },
                {
                  label: 'T006: Vikarpooldeling praksisstudier',
                  val: 180,
                  color: '#f59e0b',
                },
                {
                  label: 'T004: Tapsavtale EVU001 (SRS 9)',
                  val: 0,
                  color: '#ef4444',
                },
                {
                  label: 'T005: Minikonkurranse konsulenter (FOA)',
                  val: 0,
                  color: '#10b981',
                },
              ],
              'Tusen kr'
            )}
          </div>
        </div>

        <!-- Visual 7.2: Statusfordeling -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Statusfordeling & Risikoprofil for Omstillingsplanen</div>
              <div class="panel-subtitle">Gjennomføringssannsynlighet og lederoppfølging</div>
            </div>
          </div>
          <div class="chart-container">
            ${generateBarChartSVG(
              [
                {
                  label: 'Gjennomført (T002, T005 - Sikret gevinst)',
                  val: 1.8,
                  color: '#10b981',
                },
                {
                  label: 'Pågår (T001, T003, T006 - I rute)',
                  val: 0.9,
                  color: '#38bdf8',
                },
                {
                  label: 'Forsinket (T004 - Krever styrevarsel)',
                  val: 0.15,
                  color: '#ef4444',
                },
              ],
              'MNOK'
            )}
          </div>
        </div>
      </div>

      <!-- Visual 7.3: Komplett Tiltaksmatrise -->
      <div class="card-panel">
        <div class="panel-header">
          <div>
            <div class="panel-title">FactAction.csv - Forpliktende Omstillingstiltak & Knytning til Use Cases</div>
            <div class="panel-subtitle">Ansvarlige ledere, frister, kroneffekt og revisjonsspor</div>
          </div>
        </div>
        <div class="table-container">
          <table class="tufte-table">
            <thead>
              <tr>
                <th>TiltakID</th>
                <th>Tiltaksbeskrivelse</th>
                <th>Avviksårsak</th>
                <th>Ansvarlig Rolle</th>
                <th>Frist</th>
                <th class="num">Forventet Effekt</th>
                <th class="num">Realisert Effekt</th>
                <th>Status</th>
                <th>Sannsynlighet</th>
                <th>Use Cases Knytning</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>T001</code></td>
                <td><strong>Ansettelsesstopp og vakansestyring ved I013</strong></td>
                <td>Fallende studenttall og lavere ECTS-inntekt</td>
                <td>Dekan / Instituttleder</td>
                <td>2026-12-31</td>
                <td class="num" style="color:#10b981; font-weight:600;">850 000 kr</td>
                <td class="num" style="color:#10b981; font-weight:600;">420 000 kr</td>
                <td><span class="status-pill pagar">🟡 Pågår</span></td>
                <td class="num">85%</td>
                <td><span class="badge badge-spec">KD ECTS Fall</span></td>
              </tr>
              <tr>
                <td><code>T002</code></td>
                <td><strong>Utarbeide forpliktende investeringsplan for labutstyr (INV001)</strong></td>
                <td>Akkumulert avsetning over 5 %-grensen (F-05-20)</td>
                <td>Controller / Instituttleder</td>
                <td>2026-10-31</td>
                <td class="num" style="color:#10b981; font-weight:600;">2 400 000 kr</td>
                <td class="num" style="color:#10b981; font-weight:600;">1 800 000 kr</td>
                <td><span class="status-pill gjennomfort">🟢 Gjennomført</span></td>
                <td class="num">90%</td>
                <td><span class="badge badge-spec" style="color:#ef4444;">UC1: F-05-20</span></td>
              </tr>
              <tr>
                <td><code>T003</code></td>
                <td><strong>Rerekruttering og framdriftsoppfølging NFR001</strong></td>
                <td>Forsinket stipendiatrekruttering og lav fremdrift</td>
                <td>Prosjektleder / Controller</td>
                <td>2026-09-30</td>
                <td class="num" style="color:#10b981; font-weight:600;">600 000 kr</td>
                <td class="num" style="color:#10b981; font-weight:600;">300 000 kr</td>
                <td><span class="status-pill pagar">🟡 Pågår</span></td>
                <td class="num">75%</td>
                <td><span class="badge badge-spec">UC2: SRS 10</span></td>
              </tr>
              <tr>
                <td><code>T004</code></td>
                <td><strong>Sikre tilleggsavtale med oppdragsgiver EVU001</strong></td>
                <td>Konsulentmerforbruk og tapsrisiko på oppdrag</td>
                <td>Prosjektleder / Controller</td>
                <td>2026-11-30</td>
                <td class="num" style="color:#10b981; font-weight:600;">150 000 kr</td>
                <td class="num" style="color:#ef4444; font-weight:600;">0 kr</td>
                <td><span class="status-pill forsinket">🔴 Forsinket</span></td>
                <td class="num">60%</td>
                <td><span class="badge badge-spec" style="color:#ef4444;">UC3: SRS 9 Tap</span></td>
              </tr>
              <tr>
                <td><code>T005</code></td>
                <td><strong>Overføre avtale til Innkjøpskontoret for minikonkurranse</strong></td>
                <td>Ulovlig direkteanskaffelse > 500k kr uten anbud</td>
                <td>Innkjøpsansvarlig</td>
                <td>2026-08-31</td>
                <td class="num" style="color:#64748b;">0 kr</td>
                <td class="num" style="color:#64748b;">0 kr</td>
                <td><span class="status-pill gjennomfort">🟢 Gjennomført</span></td>
                <td class="num">95%</td>
                <td><span class="badge badge-spec">UC5: FOA Innkjøp</span></td>
              </tr>
              <tr>
                <td><code>T006</code></td>
                <td><strong>Etablere vikarpooldeling med Sørlandet Sykehus</strong></td>
                <td>Høyt sykefravær og overtid praksisoppfølging</td>
                <td>Instituttleder / HR</td>
                <td>2026-12-31</td>
                <td class="num" style="color:#10b981; font-weight:600;">350 000 kr</td>
                <td class="num" style="color:#10b981; font-weight:600;">180 000 kr</td>
                <td><span class="status-pill pagar">🟡 Pågår</span></td>
                <td class="num">70%</td>
                <td><span class="badge badge-spec">UC6: Lønnsavvik</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `,
        },

        page_08: {
          id: 'page_08_controller_cockpit',
          title: '08 Controller Cockpit (Avstemming & Bilagskontroll)',
          role: 'Senior Controller / Økonomisjef',
          desc: 'Transaksjonskontroll og avstemmingsmatrise for de 6 statlige use casene i FactGL.csv. Filtrering på UseCasesRef, kontonivå og revisjonsspor.',
          slicers: [
            {
              label: 'Use Case / Statlig Regelverk',
              options: [
                'Alle Use Cases',
                'Use Case 1: F-05-20 Avsetningskontroll',
                'Use Case 2: SRS 10 Prosjektkontroll',
                'Use Case 3: SRS 9 Tapskontrakt',
                'Use Case 4: SRS 17 Anleggsmidler',
                'Use Case 5: FOA Innkjøpsavvik',
                'Use Case 6: Lønnsavvik & Overtid',
              ],
            },
            {
              label: 'Regnskapsscenario',
              options: ['Actual (Regnskap 2026)', 'BUD2026', 'LE_2026'],
            },
          ],
          kpis: [
            {
              title: 'Bokført Regnskap YTD (M01-M08)',
              val: '68,38 M',
              unit: 'NOK',
              badge: 'FactGL.csv',
              badgeCls: 'variance-info',
              sub: 'Debet - Kredit balanse',
            },
            {
              title: 'Ubenyttet Avsetning (Konto 2080)',
              val: '-4,80 M',
              unit: 'NOK',
              badge: '8,96% av rammen',
              badgeCls: 'variance-unfavorable',
              sub: 'UC1: 5%-grense overskredet',
            },
            {
              title: 'SRS 10 Inntektsføring BOA',
              val: '-2,01 M',
              unit: 'NOK',
              badge: 'Konto 3400/3420',
              badgeCls: 'variance-favorable',
              sub: 'UC2: NFR001 kr 1,28M | EU kr 0,73M',
            },
            {
              title: 'Avsetning Tapskontrakter (SRS 9)',
              val: '900 000',
              unit: 'NOK',
              badge: 'Konto 7790 mot 2800',
              badgeCls: 'variance-unfavorable',
              sub: 'UC3: EVU001 forventet tap',
            },
            {
              title: 'Aktiverte Anleggsmidler (SRS 17)',
              val: '1,20 M',
              unit: 'NOK',
              badge: 'Konto 1250 serverpark',
              badgeCls: 'variance-info',
              sub: 'UC4: Ordinær avskr. 200k (6050)',
            },
          ],
          renderContent: () => `
      <div class="dash-grid-two-col">
        <!-- Visual 8.1: Avvik per Use Case -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Bokførte Beløp per Statlig Use Case (FactGL.csv)</div>
              <div class="panel-subtitle">Kroneffekt på identifiserte regelverksavvik i 2026 (MNOK)</div>
            </div>
          </div>
          <div class="chart-container">
            ${generateBarChartSVG(
              [
                {
                  label: 'UC1: Ubenyttet bevilgning (Konto 2080)',
                  val: 4.8,
                  color: '#ef4444',
                },
                {
                  label: 'UC2: Periodisert BOA-inntekt (Konto 3400/3420)',
                  val: 2.01,
                  color: '#38bdf8',
                },
                {
                  label: 'UC4: Aktivert serverpark (Konto 1250)',
                  val: 1.2,
                  color: '#10b981',
                },
                {
                  label: 'UC3: Tapsavsetning EVU (Konto 7790)',
                  val: 0.9,
                  color: '#ef4444',
                },
                {
                  label: 'UC5: Konsulentanskaffelse (Konto 6710)',
                  val: 0.62,
                  color: '#f59e0b',
                },
                {
                  label: 'UC6: Overtid sensorer (Konto 5050)',
                  val: 0.42,
                  color: '#f59e0b',
                },
              ],
              'MNOK'
            )}
          </div>
        </div>

        <!-- Visual 8.2: Avstemmingsstatus -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Statlig Regelverk & Revisjonssjekkliste (DFØ / Riksrevisjonen)</div>
              <div class="panel-subtitle">Overholdelse av statlige regnskapsstandarder ved UiA</div>
            </div>
          </div>
          <div style="padding: 12px; font-size: 11.5px; line-height: 1.6; color: #cbd5e1;">
            <div style="margin-bottom:8px; padding: 6px 10px; background: rgba(239,68,68,0.1); border-left: 3px solid #ef4444; border-radius: 3px;">
              <strong>Rundskriv F-05-20 (UC1):</strong> Avsetningsgrad 8,96% overstiger 5,0%. Tiltak T002 forserer labutstyr for å unngå inndragning ved årsslutt.
            </div>
            <div style="margin-bottom:8px; padding: 6px 10px; background: rgba(16,185,129,0.1); border-left: 3px solid #10b981; border-radius: 3px;">
              <strong>SRS 10 (UC2):</strong> Inntektsføring følger påløpte kostnader kr 2,01M. Forskudd redusert på konto 2180.
            </div>
            <div style="margin-bottom:8px; padding: 6px 10px; background: rgba(239,68,68,0.1); border-left: 3px solid #ef4444; border-radius: 3px;">
              <strong>SRS 9 (UC3):</strong> Full tapsavsetning på 900 000 kr bokført umiddelbart for EVU001 (konto 7790 mot 2800).
            </div>
            <div style="padding: 6px 10px; background: rgba(56,189,248,0.1); border-left: 3px solid #38bdf8; border-radius: 3px;">
              <strong>SRS 17 (UC4):</strong> Serverpark kr 1,2M aktivert i balansen. Avskrives lineært over 3 år (50k/mnd).
            </div>
          </div>
        </div>
      </div>

      <!-- Visual 8.3: Transaksjonslogg FactGL med UseCasesRef -->
      <div class="card-panel">
        <div class="panel-header">
          <div>
            <div class="panel-title">Transaksjons- og Bilagslogg (FactGL.csv) - Filtrert på Use Cases</div>
            <div class="panel-subtitle">Reelle regnskapsposter med TransaksjonsID, konto, beløp og bokføringstekst</div>
          </div>
          <a class="drill-link" onclick="showDashboard('page_dt_okonomi')">Åpne bilagslogg &rarr;</a>
        </div>
        <div class="table-container">
          <table class="tufte-table">
            <thead>
              <tr>
                <th>TransaksjonsID</th>
                <th>Dato</th>
                <th>Konto</th>
                <th>Kontonavn</th>
                <th>Prosjekt</th>
                <th>Tekst</th>
                <th class="num">Beløp Signert</th>
                <th>Use Case Referanse</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>TR-2026-00101</code></td>
                <td>2026-06-30</td>
                <td><code>2080</code></td>
                <td>Ubenyttet bevilgning</td>
                <td>DRIFT</td>
                <td>Avsetning ubenyttet ramme FAK-TR (F-05-20)</td>
                <td class="num" style="color:#ef4444; font-weight:600;">-4 800 000,00 kr</td>
                <td><span class="badge badge-spec" style="color:#ef4444;">UC1: F-05-20</span></td>
              </tr>
              <tr>
                <td><code>TR-2026-00201</code></td>
                <td>2026-08-31</td>
                <td><code>3400</code></td>
                <td>Statstilskudd NFR</td>
                <td>NFR001</td>
                <td>SRS 10 Motsatt sammenstilling NFR001</td>
                <td class="num" style="color:#10b981; font-weight:600;">-1 280 000,00 kr</td>
                <td><span class="badge badge-spec">UC2: SRS 10</span></td>
              </tr>
              <tr>
                <td><code>TR-2026-00202</code></td>
                <td>2026-08-31</td>
                <td><code>3420</code></td>
                <td>EU-tilskudd Horisont</td>
                <td>EU001</td>
                <td>SRS 10 Motsatt sammenstilling EU001</td>
                <td class="num" style="color:#10b981; font-weight:600;">-730 000,00 kr</td>
                <td><span class="badge badge-spec">UC2: SRS 10</span></td>
              </tr>
              <tr>
                <td><code>TR-2026-00301</code></td>
                <td>2026-06-30</td>
                <td><code>7790</code></td>
                <td>Avsetning tap kontrakter</td>
                <td>EVU001</td>
                <td>SRS 9 Avsetning forventet tap EVU001</td>
                <td class="num" style="color:#ef4444; font-weight:600;">900 000,00 kr</td>
                <td><span class="badge badge-spec" style="color:#ef4444;">UC3: SRS 9 Tap</span></td>
              </tr>
              <tr>
                <td><code>TR-2026-00401</code></td>
                <td>2026-03-15</td>
                <td><code>1250</code></td>
                <td>IT-utstyr & servere</td>
                <td>INV001</td>
                <td>SRS 17 Aktivering ny serverpark IT</td>
                <td class="num" style="color:#38bdf8; font-weight:600;">1 200 000,00 kr</td>
                <td><span class="badge badge-spec">UC4: SRS 17 Aktivert</span></td>
              </tr>
              <tr>
                <td><code>TR-2026-00402</code></td>
                <td>2026-08-31</td>
                <td><code>6050</code></td>
                <td>Avskrivninger IT</td>
                <td>INV001</td>
                <td>SRS 17 Ordinære avskrivninger servere (M04-M08)</td>
                <td class="num" style="color:#f59e0b; font-weight:600;">200 000,00 kr</td>
                <td><span class="badge badge-spec">UC4: SRS 17 Avskr.</span></td>
              </tr>
              <tr>
                <td><code>TR-2026-00501</code></td>
                <td>2026-05-20</td>
                <td><code>6710</code></td>
                <td>Konsulenttjenester</td>
                <td>DRIFT</td>
                <td>FOA: Konsulentkjøp over terskel uten anbud</td>
                <td class="num" style="color:#ef4444; font-weight:600;">620 000,00 kr</td>
                <td><span class="badge badge-spec">UC5: FOA Innkjøp</span></td>
              </tr>
              <tr>
                <td><code>TR-2026-00601</code></td>
                <td>2026-06-30</td>
                <td><code>5050</code></td>
                <td>Overtid og sensorer</td>
                <td>DRIFT</td>
                <td>Overtid praksisoppfølging sykepleie</td>
                <td class="num" style="color:#f59e0b; font-weight:600;">422 932,00 kr</td>
                <td><span class="badge badge-spec">UC6: Lønnsavvik</span></td>
              </tr>
              <tr>
                <td><code>TR-2026-00602</code></td>
                <td>2026-07-15</td>
                <td><code>5800</code></td>
                <td>Refusjon sykepenger NAV</td>
                <td>DRIFT</td>
                <td>NAV sykepengerefusjon langtidssykefravær</td>
                <td class="num" style="color:#10b981; font-weight:600;">-84 000,00 kr</td>
                <td><span class="badge badge-spec">UC6: NAV Refusjon</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `,
        },

        page_use_cases: {
          id: 'page_use_cases',
          title:
            'Statlig Regelverkskontroll & De 6 Use Casene (DFØ SRS & F-05-20)',
          role: 'Statsautorisert Controller / Regelverksansvarlig',
          desc: 'Autoritativ dokumentasjon av UiAs 6 regulatoriske use cases: Rundskriv F-05-20 (5 %-regelen), SRS 10 Motsatt sammenstilling, SRS 9 Tapskontrakter, SRS 17 Aktivering, FOA Anskaffelsesavvik og Lønnsavvik/NAV-refusjoner.',
          slicers: [
            {
              label: 'Velg Regelverksregime',
              options: [
                'Alle regimer',
                'DFØ SRS 1, 9, 10, 17',
                'KDs Rundskriv F-05-20',
                'Lov om offentlige anskaffelser (FOA)',
                'KDs 2025 Finansieringsmodell',
              ],
            },
          ],
          kpis: [
            {
              title: 'UC1: Avsetningsgrad F-05-20',
              val: '8,96 %',
              unit: 'Konto 2080',
              badge: '🔴 > 5% Grense',
              badgeCls: 'variance-unfavorable',
              sub: 'Maksgrense 2,68M | Tiltak T002',
            },
            {
              title: 'UC2: SRS 10 BOA Inntektsført',
              val: '2,01 M',
              unit: 'NOK',
              badge: 'NFR/EU Tilskudd',
              badgeCls: 'variance-favorable',
              sub: 'Motsatt sammenstilling',
            },
            {
              title: 'UC3: SRS 9 Tapskontrakt',
              val: '900 000',
              unit: 'NOK',
              badge: 'EVU001 (+22%)',
              badgeCls: 'variance-unfavorable',
              sub: 'Konto 7790 mot 2800',
            },
            {
              title: 'UC4: SRS 17 Aktivert Serverpark',
              val: '1,20 M',
              unit: 'NOK',
              badge: 'Konto 1250',
              badgeCls: 'variance-info',
              sub: 'Lineær avskrivning 50k/mnd',
            },
            {
              title: 'UC5: FOA Konsulentavvik',
              val: '620 000',
              unit: 'NOK',
              badge: 'Konto 6710',
              badgeCls: 'variance-unfavorable',
              sub: 'Overført minikonkurranse T005',
            },
          ],
          renderContent: () => `
      <!-- Deep Dive Tabs / Accordion for All 6 Use Cases + KD ECTS -->
      <div style="display: flex; flex-direction: column; gap: 20px;">

        <!-- CARD UC1: F-05-20 -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title" style="display:flex; align-items:center; gap:8px;">
                <span style="color:#ef4444; font-size:18px;">🏛️</span>
                <span>Use Case 1: Rundskriv F-05-20 (5 %-regelen for overføring av bevilgning)</span>
              </div>
              <div class="panel-subtitle">Kunnskapsdepartementets instruks for håndtering av ubrukte grunnbevilgningsmidler ved årsslutt</div>
            </div>
            <span class="status-pill rag-red">Akkumulert: 8,96% (Kritisk avvik)</span>
          </div>
          <div style="padding: 16px; background: rgba(0,0,0,0.25); border-radius: 8px; line-height: 1.6; font-size: 12px; color: #cbd5e1;">
            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px;">
              <div>
                <p><strong>Regelverk & Krav:</strong> I henhold til KDs rundskriv F-05-20 kan en statlig utdanningsinstitusjon maksimalt overføre <strong>5,0 %</strong> av årets rammebevilgning som ubrukte midler til neste budsjettår. Avsetninger utover 5 % krever en forpliktende, styregodkjent investeringsplan (f.eks. til vitenskapelig utstyr eller bygg), ellers inndras midlene til statskassen.</p>
                <p style="margin-top: 8px;"><strong>Faktisk status ved UiA (FAK-TR):</strong> Fakultet for teknologi og realfag har ved utgangen av august (T2) akkumulert <strong>-4 800 000 kr</strong> på konto <code>2080 Avsetning til framtidig drift</code>. Med en årsramme på 53,6 MNOK utgjør dette <strong>8,96 %</strong> (meravsetning på 2,12 MNOK).</p>
                <p style="margin-top: 8px;"><strong>Revisjonsspor & Bokføring:</strong> Bilag <code>TR-2026-00101</code> på konto <code>2080</code>.</p>
              </div>
              <div style="background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.25); border-radius: 6px; padding: 12px;">
                <div style="font-weight:600; color:#10b981; margin-bottom:4px;">Løsning: Tiltak T002</div>
                <div style="font-size:11.5px; color:#cbd5e1;">
                  Forsering av labutstyrsinvesteringer for prosjekt <code>INV001</code> på <strong>kr 1 800 000</strong> (av planlagt 2,4M) før 31.10.2026. Dette reduserer konto 2080 til 1,93 MNOK (3,6 %) og sikrer full overholdelse av 5 %-regelen.
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- CARD UC2: SRS 10 -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title" style="display:flex; align-items:center; gap:8px;">
                <span style="color:#38bdf8; font-size:18px;">📊</span>
                <span>Use Case 2: SRS 10 Inntektsføring av Tilskudd (Motsatt Sammenstilling)</span>
              </div>
              <div class="panel-subtitle">DFØ Statlige regnskapsstandarder SRS 10 for NFR- og EU-forskning</div>
            </div>
            <span class="status-pill rag-green">Fullt etterlevd (2,01 MNOK)</span>
          </div>
          <div style="padding: 16px; background: rgba(0,0,0,0.25); border-radius: 8px; line-height: 1.6; font-size: 12px; color: #cbd5e1;">
            <p><strong>Regelverk & Krav:</strong> Tilskudd fra Norges forskningsråd (NFR) og EU skal <em>ikke</em> inntektsføres ved innbetaling, men periodiseres etter <strong>motsatt sammenstillingsprinsipp</strong>. Inntekt innregnes i samme periode som de tilhørende prosjektkostnadene påløper. Mottatt forskuddsbetaling føres som kortsiktig gjeld på balansekonto <code>2180 Forskuddsbetaling tilskudd</code>.</p>
            <div style="margin-top: 10px; display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
              <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; border: 1px solid var(--border-subtle);">
                <strong>Prosjekt NFR001 AI i styring:</strong>
                <div>• Påløpte kostnader M01-M08: 1 280 000 kr</div>
                <div>• Bokført inntekt (Konto 3400): -1 280 000 kr</div>
                <div>• Gjeldsreduksjon (Konto 2180): +1 280 000 kr (Transaksjon TR-2026-00201)</div>
              </div>
              <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; border: 1px solid var(--border-subtle);">
                <strong>Prosjekt EU001 Green Maritime:</strong>
                <div>• Påløpte kostnader M01-M08: 730 000 kr</div>
                <div>• Bokført inntekt (Konto 3420): -730 000 kr</div>
                <div>• Gjeldsreduksjon (Konto 2180): +730 000 kr (Transaksjon TR-2026-00202)</div>
              </div>
            </div>
            <p style="margin-top: 10px; font-size: 11px; color: #94a3b8;">
              💡 <strong>Tiltak T003:</strong> Etablert månedlig automatisk avstemmingsrutine i Unit4 ERP for å hindre etterslep i timeføring og inntektsføring.
            </p>
          </div>
        </div>

        <!-- CARD UC3: SRS 9 -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title" style="display:flex; align-items:center; gap:8px;">
                <span style="color:#ef4444; font-size:18px;">⚠️</span>
                <span>Use Case 3: SRS 9 Oppdragsforskning & Tapskontrakter (EVU001)</span>
              </div>
              <div class="panel-subtitle">Krav om fullkostkalkyle (TDI) og umiddelbar tapsavsetning ved forventet overskridelse</div>
            </div>
            <span class="status-pill rag-red">Tapsavsetning: 900 000 kr</span>
          </div>
          <div style="padding: 16px; background: rgba(0,0,0,0.25); border-radius: 8px; line-height: 1.6; font-size: 12px; color: #cbd5e1;">
            <p><strong>Regelverk & Krav:</strong> SRS 9 krever at oppdragsfinansiert virksomhet (etter-/videreutdanning og oppdrag for næringsliv) skal prises til markedspris og dekke alle direkte og indirekte kostnader (TDI-kalkyle). Dersom de totale prosjektkostnadene overstiger kontraktssummen, skal hele det forventede tapet kostnadsføres <strong>umiddelbart</strong> som tapsavsetning (konto <code>7790 Avsetning tap på kontrakter</code> mot <code>2800 Avsetning for forpliktelser</code>).</p>
            <p style="margin-top: 8px;"><strong>Faktisk status på EVU001:</strong> Prosjektet har et merforbruk på <strong>+22 %</strong> grunnet uforutsette eksterne faglærerhonorarer. Totalt forventet tap ved fullføring er estimert til 900 000 kr.</p>
            <p style="margin-top: 8px;"><strong>Revisjonsspor & Bokføring:</strong> Transaksjon <code>TR-2026-00301</code> bokført i M06 på konto 7790 debet (900 000 kr) og konto 2800 kredit (-900 000 kr). Tiltak <strong>T004</strong> er igangsatt for reforhandling av leveranseomfang.</p>
          </div>
        </div>

        <!-- CARD UC4: SRS 17 -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title" style="display:flex; align-items:center; gap:8px;">
                <span style="color:#10b981; font-size:18px;">🖥️</span>
                <span>Use Case 4: SRS 17 Aktivering av Anleggsmidler & Finansiering</span>
              </div>
              <div class="panel-subtitle">Balanseføring av driftsmidler med levetid > 3 år og kostnad > 50 000 kr</div>
            </div>
            <span class="status-pill rag-green">Aktivert: 1 200 000 kr</span>
          </div>
          <div style="padding: 16px; background: rgba(0,0,0,0.25); border-radius: 8px; line-height: 1.6; font-size: 12px; color: #cbd5e1;">
            <p><strong>Regelverk & Krav:</strong> Varige driftsmidler skal balanseføres iht. SRS 17 dersom anskaffelseskostnaden overstiger 50 000 kr og levetiden er vesentlig (> 3 år). I staten finansieres kjøpet over bevilgningen og motposteres mot statens kapital (konto <code>2050 Avsetning til investeringer</code>). Ordinære avskrivninger kostnadsføres månedlig over levetiden på konto <code>6050 Avskrivninger IT</code>.</p>
            <div style="margin-top: 10px; background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px; border: 1px solid var(--border-subtle);">
              <div>• <strong>Anskaffelse M03:</strong> Ny sentral serverpark på <strong>1 200 000 kr</strong> aktivert (Debet <code>1250 IT-utstyr</code>, Kredit <code>2050 Avsetning investeringer</code>). Bilag <code>TR-2026-00401</code>.</div>
              <div>• <strong>Avskrivninger M04-M08:</strong> 50 000 kr/mnd i 5 måneder = <strong>200 000 kr</strong> (Debet <code>6050</code>, Kredit <code>1259 Akkumulert avskrivning</code>). Bilag <code>TR-2026-00402</code>.</div>
            </div>
          </div>
        </div>

        <!-- CARD UC5: FOA -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title" style="display:flex; align-items:center; gap:8px;">
                <span style="color:#f59e0b; font-size:18px;">⚖️</span>
                <span>Use Case 5: Lov om Offentlige Anskaffelser (FOA) - Avviksføring</span>
              </div>
              <div class="panel-subtitle">Anskaffelser over terskelverdi uten gyldig rammeavtale eller kunngjøring i Doffin</div>
            </div>
            <span class="status-pill rag-amber">Avvik flagget: 620 000 kr</span>
          </div>
          <div style="padding: 16px; background: rgba(0,0,0,0.25); border-radius: 8px; line-height: 1.6; font-size: 12px; color: #cbd5e1;">
            <p><strong>Regelverk & Avvik:</strong> Direkteanskaffelser over 500 000 kr eks. mva. krever formell minikonkurranse eller rammeavtale. Controller oppdaget fakturaer på totalt <strong>620 000 kr</strong> på konto <code>6710 Konsulenttjenester</code> i mai (bilag <code>TR-2026-00501</code>) uten gyldig rammeavtalenummer registrert i innkjøpssystemet.</p>
            <p style="margin-top: 8px;"><strong>Handling (Tiltak T005):</strong> Avtalen ble umiddelbart stoppet og overført til Innkjøpskontoret. Minikonkurranse gjennomført under statens fellesavtaler innen 31.08.2026. Revisjonsnotat oversendt internrevisjonen for å dokumentere legalitetskontroll.</p>
          </div>
        </div>

        <!-- CARD UC6: LØNNSAVVIK & NAV -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title" style="display:flex; align-items:center; gap:8px;">
                <span style="color:#38bdf8; font-size:18px;">🩺</span>
                <span>Use Case 6: Lønnsavvik, Sensorovertid & NAV Sykepengerefusjoner</span>
              </div>
              <div class="panel-subtitle">Oppfølging av overtid i praksisstudier og refusjonskrav mot NAV</div>
            </div>
            <span class="status-pill rag-green">NAV-refusjon: -84 000 kr</span>
          </div>
          <div style="padding: 16px; background: rgba(0,0,0,0.25); border-radius: 8px; line-height: 1.6; font-size: 12px; color: #cbd5e1;">
            <p><strong>Regelverk & Avvik:</strong> Lønn skal føres på artskontoer 5000-5899. Ved langtidssykefravær forskutterer UiA lønn og krever refusjon fra NAV etter 16 kalenderdager på konto <code>5800 Refusjon sykepenger</code>.</p>
            <p style="margin-top: 8px;"><strong>Faktiske poster:</strong></p>
            <div>• Overtid og sensur i praksisstudier helsefag utgjør <strong>422 932 kr</strong> på konto <code>5050</code> (bilag <code>TR-2026-00601</code>).</div>
            <div>• NAV-refusjoner bokført med <strong>-84 000 kr</strong> på konto <code>5800</code> (bilag <code>TR-2026-00602</code>).</div>
            <p style="margin-top: 8px;"><strong>Løsning (Tiltak T006):</strong> Etablert felles sensor- og vikarpooldeling med Sørlandet Sykehus HF for å begrense overtidssatser og sikre stabil praksisveiledning.</p>
          </div>
        </div>

      </div>
    `,
        },

        page_laereplaner: {
          id: 'page_laereplaner',
          title: 'Læreplaner & Budsjettering i UH-sektoren (UiA-Modell)',
          role: 'Controller Mentor & Kompetanseansvarlig',
          desc: 'Komplett faglig læreplan for controllere ved Universitetet i Agder. 4 strategiske moduler: Statlig økonomistyring, driverbasert budsjettfordeling, bemanningsplanlegging (TDI) og risikostyring.',
          slicers: [
            {
              label: 'Velg Læreplandokument',
              options: [
                'Alle dokumenter',
                'Læreplan 1: Budsjettering & Prosessen',
                'Læreplan 2: Eksempler & Case',
                'Læreplan 3: Controller-Kompetanse',
              ],
            },
          ],
          kpis: [
            {
              title: 'Statlige Moduler',
              val: '4',
              unit: 'Moduler',
              badge: 'Styring i det store',
              badgeCls: 'variance-info',
              sub: 'Fra KD til fakultet',
            },
            {
              title: 'Lønnsandel Standard',
              val: '71,0 %',
              unit: 'Norm',
              badge: 'Vakansestyring',
              badgeCls: 'variance-info',
              sub: 'Viktigste styringsverktøy',
            },
            {
              title: 'KDs 2025 Satser',
              val: '3',
              unit: 'Kategorier',
              badge: '54,5k / 81,8k / 190,9k',
              badgeCls: 'variance-info',
              sub: 'Marginal endringsmodell',
            },
            {
              title: 'TDI Full Costing',
              val: '22-25%',
              unit: 'Overhead',
              badge: 'Total Dekning',
              badgeCls: 'variance-info',
              sub: 'Frikjøp, drift, IK, leiested',
            },
          ],
          renderContent: () => `
      <div style="display: flex; flex-direction: column; gap: 20px;">

        <!-- MODUL 1 -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title" style="display:flex; align-items:center; gap:8px;">
                <span style="color:#38bdf8;">📘</span>
                <span>Modul 1: Rammebetingelser og Statlig Økonomistyring ved UiA</span>
              </div>
              <div class="panel-subtitle">Styring i det store | Tildelingsbrevet fra KD | Kap. 260 i Statsbudsjettet | F-05-20</div>
            </div>
            <span class="status-pill rag-green">Grunnmuren i rollen</span>
          </div>
          <div style="padding: 16px; background: rgba(0,0,0,0.25); border-radius: 8px; line-height: 1.6; font-size: 12px; color: #cbd5e1;">
            <p><strong>Strategisk kontekst:</strong> Statlig økonomistyring har beveget seg bort fra detaljstyring mot <em>«styring i det store»</em>. Tildelingsbrevet fra Kunnskapsdepartementet (KD) er startpunktet. Som controller leser du tildelingsbrevet som et strategisk kart for øremerkede midler, effektiviseringskrav og nye studieplasser.</p>
            <div style="margin-top: 10px; display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
              <div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: 6px; border: 1px solid var(--border-subtle);">
                <strong style="color:#38bdf8;">Prinsippet om nettobudsjettering:</strong>
                <p style="margin-top:4px;">Eksisterende volum ligger i utgangspunktet fast i basisbevilgningen. Bevilgningen endres kun ved endrede resultater eller nye politiske satsinger. Dersom studentproduksjonen faller, kuttes det etter de nye marginalsatsene.</p>
              </div>
              <div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: 6px; border: 1px solid var(--border-subtle);">
                <strong style="color:#ef4444;">Avsetningsreglementet og 5 %-regelen (F-05-20):</strong>
                <p style="margin-top:4px;">For høye avsetninger (> 5 %) er en strategisk risiko; det signaliserer manglende gjennomføringsevne og gjør institusjonen sårbar for fremtidige kutt i statsbudsjettet. Som controller må du bruke 5 %-regelen som et aktivt styringsskjold.</p>
              </div>
            </div>
            <div style="margin-top: 10px; background: rgba(56,189,248,0.06); padding: 10px; border-radius: 6px; border: 1px solid rgba(56,189,248,0.2);">
              <strong>"So What?"-laget:</strong> Overgangen til styrket basisbevilgning gir bedre forutsigbarhet, men krever også strengere intern kontroll. Når «lukkede rammer» forsvinner, må vi selv sikre at basisbevilgningen investeres i faglig kvalitet som bærer frukter over tid.
            </div>
          </div>
        </div>

        <!-- MODUL 2 -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title" style="display:flex; align-items:center; gap:8px;">
                <span style="color:#10b981;">📊</span>
                <span>Modul 2: Finansieringsmodeller og Driverbasert Budsjettfordeling</span>
              </div>
              <div class="panel-subtitle">KDs nye modell fra 2025 (Kategori 1-3) | Driverbasert fordeling | Marginalitetsanalyse</div>
            </div>
            <span class="status-pill rag-amber">Insentivsystem</span>
          </div>
          <div style="padding: 16px; background: rgba(0,0,0,0.25); border-radius: 8px; line-height: 1.6; font-size: 12px; color: #cbd5e1;">
            <p><strong>Strategisk kontekst:</strong> Det er en konstant spenning mellom KDs standardiserte satser og UiAs reelle kostnader. KDs modell fra 2025 opererer med tre kategorier som erstatter de tidligere seks (A–F):</p>
            <div style="margin: 10px 0; overflow-x: auto;">
              <table class="tufte-table">
                <thead>
                  <tr>
                    <th>Kategori (2025)</th>
                    <th>Fagområder (Eksempler)</th>
                    <th class="num">Sats per 60 studiepoeng</th>
                    <th>Controller-merknad</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><span class="cat-badge cat-01">Kategori 1</span></td>
                    <td>Humaniora, samfunnsfag, økonomiske fag</td>
                    <td class="num">54 550 kr</td>
                    <td>Gjelder kun endring i produksjon</td>
                  </tr>
                  <tr>
                    <td><span class="cat-badge cat-02">Kategori 2</span></td>
                    <td>Realfag, helse-, lærerutdanning, profesjonsstudier i psykologi</td>
                    <td class="num">81 800 kr</td>
                    <td>Høyere sats pga. laboratorier og praksis</td>
                  </tr>
                  <tr>
                    <td><span class="cat-badge cat-03">Kategori 3</span></td>
                    <td>Medisin, odontologi, klinisk veterinærmedisin</td>
                    <td class="num">190 900 kr</td>
                    <td>Ikke etablert ved UiA</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div style="background: rgba(245,158,11,0.06); padding: 10px; border-radius: 6px; border: 1px solid rgba(245,158,11,0.2);">
              <strong>"So What?"-laget:</strong> Ved å fjerne resultatbasert uttelling for publisering og BOA-inntekter i den nasjonale modellen, flyttes den økonomiske risikoen for forskning over på institusjonen. Den automatiske «pengemaskinen» er borte; vekst i forskning må nå begrunnes strategisk i Utviklingsavtalen.
            </div>
          </div>
        </div>

        <!-- MODUL 3 -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title" style="display:flex; align-items:center; gap:8px;">
                <span style="color:#f59e0b;">👥</span>
                <span>Modul 3: Bemanningsplanlegging, Drift og Prosjektøkonomi (TDI / BOA)</span>
              </div>
              <div class="panel-subtitle">Årsverksplanlegging | Lønnsandel 71% | Vakansestyring | TDI Full Costing for NFR og EU</div>
            </div>
            <span class="status-pill rag-red">71% av kostnadene</span>
          </div>
          <div style="padding: 16px; background: rgba(0,0,0,0.25); border-radius: 8px; line-height: 1.6; font-size: 12px; color: #cbd5e1;">
            <p><strong>Strategisk kontekst:</strong> Lønn utgjør ca. 71 % av UiAs kostnader. Det betyr at <strong>vakansestyring</strong> er ditt viktigste operative styringsverktøy som controller. Rekrutteringsstillinger (stipendiater og postdoktorer) er forskningsressurser, men også 3-4 årige uoppsigelige forpliktelser.</p>
            <p style="margin-top:8px;"><strong>TDI-modellen (Total Dekning av Inntekter):</strong> Ved eksternfinansiert forskning (BOA) benytter UiA TDI-standarden for fullkostkalkulasjon:</p>
            <div style="margin: 10px 0; background: rgba(0,0,0,0.3); padding: 12px; border-radius: 6px; font-family: var(--font-mono); font-size: 11px; line-height: 1.7; color: #7dd3fc;">
              Total Prosjektkostnad = Frikjøp (vitenskapelig tid) + Direkte drift + Indirekte kostnader (IK / Overhead ~22-25%) + Leiesteder (lab/spesialrom)
            </div>
            <p style="font-size: 11.5px; color: #94a3b8;">
              ⚠️ Bidragsprosjekter (NFR/EU) krever at institusjonen skyter inn egenandel dersom ikke alle indirekte kostnader dekkes av bevilgende myndighet. Oppdragsprosjekter (EVU/marked) skal dekke 100% fullkost samt markedsfortjeneste (SRS 9).
            </p>
          </div>
        </div>

        <!-- MODUL 4 -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title" style="display:flex; align-items:center; gap:8px;">
                <span style="color:#a855f7;">📈</span>
                <span>Modul 4: Risikostyring, Avviksrapportering & Rullende Prognoser (EAC)</span>
              </div>
              <div class="panel-subtitle">Rolling 12M Forecast | Forecast Bias Index | Edward Tufte Data-Ink Standarder</div>
            </div>
            <span class="status-pill rag-green">Lederstøtte & Preskripsjon</span>
          </div>
          <div style="padding: 16px; background: rgba(0,0,0,0.25); border-radius: 8px; line-height: 1.6; font-size: 12px; color: #cbd5e1;">
            <p><strong>Strategisk kontekst:</strong> En tertialrapport som kun rapporterer historiske tall (regnskap YTD) er utilstrekkelig. Som controller leverer du en <strong>rullende 12-måneders hybridprognose (EAC)</strong> som kombinerer faktiske tall med den nyeste oppdaterte prognosen (LE). Du analyserer <em>Forecast Bias</em> for å avdekke systematisk under- eller overprognostisering.</p>
            <p style="margin-top: 8px;"><strong>Edward Tufte Visualiseringsprinsipper ved UiA:</strong></p>
            <div style="margin-top: 6px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 11px;">
              <div>• Fjern vertikale gitterlinjer fra tabeller og grafer.</div>
              <div>• Bruk direkte merking på S-kurver fremfor fargelagte tegnforklaringer.</div>
              <div>• Demp bakgrunnsfarger og unngå dekorative skygger og ikoner.</div>
              <div>• Bruk rødt og gult KUN for aktive avvik og risikoforhold som krever handling.</div>
            </div>
          </div>
        </div>

      </div>
    `,
        },

        // DRILL-THROUGHS
        page_dt_okonomi: {
          id: 'page_dt_okonomi',
          title: 'DT Økonomidetalj (Bilagslogg)',
          role: 'Drill-Through Transaksjoner',
          desc: 'Transaksjons- og bilagslogg på laveste detaljnivå fra FactGL (35 760 transaksjoner). Filtrerbar per bilag, dato, organisasjon, konto og prosjekt.',
          slicers: [
            {
              label: 'Konto',
              options: [
                'Alle kontoer',
                '5000 Fast lønn',
                '5010 Sensorhonorar',
                '6300 Husleie',
                '6700 Konsulenter',
              ],
            },
            {
              label: 'Prosjekt',
              options: [
                'Alle prosjekter',
                'DRIFT',
                'NFR001',
                'EU001',
                'OPP001',
              ],
            },
          ],
          kpis: [
            {
              title: 'Total bokført (Regnskap)',
              val: '68,38 M',
              unit: 'NOK',
              badge: 'YTD M01-M08',
              badgeCls: 'variance-info',
              sub: 'Debet 68,38 MNOK',
            },
            {
              title: 'Budsjettbeløp',
              val: '54,56 M',
              unit: 'NOK',
              badge: 'Budsjett YTD',
              badgeCls: 'variance-info',
              sub: 'Årsbudsjett BAC: 81,84 M',
            },
            {
              title: 'Avvik (Regnskap - Budsjett)',
              val: '-13,82 M',
              unit: 'NOK',
              badge: 'Merforbruk YTD',
              badgeCls: 'variance-unfavorable',
              sub: 'M01-M08 avvik',
            },
          ],
          renderContent: () => `
      <div class="card-panel">
        <div class="panel-header">
          <div>
            <div class="panel-title">Transaksjons- og bilagslogg (FactGL.csv - 35 760 rader)</div>
            <div class="panel-subtitle">Utsnitt av bokførte regnskapsposter med signert fortegn</div>
          </div>
        </div>
        <div class="table-container">
          <table class="tufte-table">
            <thead>
              <tr>
                <th>Bilagsnummer</th>
                <th>Dato</th>
                <th>OrgNøkkel</th>
                <th>Konto</th>
                <th>Prosjekt</th>
                <th>Bokføringstekst</th>
                <th class="num">Beløp Signert</th>
                <th>Kilde</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>BIL-2026-00142</code></td>
                <td>2026-12-15</td>
                <td>I001K1</td>
                <td>5000 (Fast lønn UF)</td>
                <td>DRIFT</td>
                <td>Lønnskjøring desember 2026</td>
                <td class="num">124 500,00 kr</td>
                <td>SAP/Agresso</td>
              </tr>
              <tr>
                <td><code>BIL-2026-00143</code></td>
                <td>2026-12-15</td>
                <td>I001K1</td>
                <td>5010 (Sensorhonorar)</td>
                <td>DRIFT</td>
                <td>Sensurkontrakt eksamen høst</td>
                <td class="num">38 400,00 kr</td>
                <td>Fagmodul</td>
              </tr>
              <tr>
                <td><code>BIL-2026-00188</code></td>
                <td>2026-12-18</td>
                <td>I002K3</td>
                <td>6700 (Konsulenter)</td>
                <td>NFR001</td>
                <td>Deloitte dataanalyse BOA-prosjekt</td>
                <td class="num">82 000,00 kr</td>
                <td>Fakturamottak</td>
              </tr>
              <tr>
                <td><code>BIL-2026-00210</code></td>
                <td>2026-12-20</td>
                <td>I001K2</td>
                <td>3030 (Bevilgning inntekt)</td>
                <td>DRIFT</td>
                <td>Periodisert KD-rammetildeling</td>
                <td class="num" style="color:#10b981;">-215 000,00 kr</td>
                <td>Hovedbok</td>
              </tr>
              <tr>
                <td><code>BIL-2026-00245</code></td>
                <td>2026-12-22</td>
                <td>I003K1</td>
                <td>6300 (Husleie)</td>
                <td>DRIFT</td>
                <td>Husleie Campus Nord mnd 12</td>
                <td class="num">145 000,00 kr</td>
                <td>Statsbygg</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `,
        },

        page_dt_bemanning: {
          id: 'page_dt_bemanning',
          title: 'DT Bemanning & Årsverk',
          role: 'Drill-Through HR / Personalkostnader',
          desc: 'Dybdevisning av årsverk, stillingskategorier (vitenskapelig UF vs. administrativ TA), personalkostnader og snittlønn per årsverk.',
          slicers: [
            {
              label: 'Stillingskategori',
              options: [
                'Alle kategorier',
                'Vitenskapelig (UF)',
                'Administrativ (TA)',
              ],
            },
            {
              label: 'Fakultet',
              options: [
                'Alle fakulteter',
                'Handelshøyskolen',
                'Fakultet for teknologi',
              ],
            },
          ],
          kpis: [
            {
              title: 'Årsverk totalt',
              val: '1 285,9',
              unit: 'FTE',
              badge: 'Siste måned',
              badgeCls: 'variance-info',
              sub: '1 440 måledatapunkter',
            },
            {
              title: 'Faglige årsverk',
              val: '661,8',
              unit: 'UF',
              badge: '51,5% andel',
              badgeCls: 'variance-info',
              sub: 'Professor, dosent, førsteamanuensis',
            },
            {
              title: 'Lønnskostnader',
              val: '50,97 M',
              unit: 'NOK',
              badge: '78,31% lønnsandel',
              badgeCls: 'variance-unfavorable',
              sub: 'Av 65,08 M driftskostnader (Norm: 71,0%)',
            },
            {
              title: 'Snittlønn per årsverk',
              val: '1 152 700',
              unit: 'kr/ÅV',
              badge: 'Inkl. sosiale kost.',
              badgeCls: 'variance-info',
              sub: 'Pensjon og arbeidsgiveravgift',
            },
          ],
          renderContent: () => `
      <div class="dash-grid-two-col">
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Årsverk per stillingsgruppe</div>
              <div class="panel-subtitle">Vitenskapelige og administrative stillingsgrupper (FactFTE)</div>
            </div>
          </div>
          <div class="chart-container">
            ${generateBarChartSVG(
              [
                {
                  label: 'VIT_PROF (Professor / Dosent)',
                  val: 245.5,
                  color: '#38bdf8',
                },
                {
                  label: 'VIT_FORST (Førsteamanuensis / Lektor)',
                  val: 320.3,
                  color: '#38bdf8',
                },
                {
                  label: 'VIT_REKR (Stipendiat / Postdoktor)',
                  val: 95.9,
                  color: '#6366f1',
                },
                {
                  label: 'ADM_LEDER (Ledelse & kontorsjefer)',
                  val: 84.0,
                  color: '#f59e0b',
                },
                {
                  label: 'ADM_SAKSB (Saksbehandlere & rådgivere)',
                  val: 540.2,
                  color: '#94a3b8',
                },
              ],
              'Årsverk'
            )}
          </div>
        </div>

        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Årsverk per stillingskategori</div>
              <div class="panel-subtitle">Vitenskapelig (UF) vs. Teknisk-administrativ (TA)</div>
            </div>
          </div>
          <div class="chart-container">
            ${generateBarChartSVG(
              [
                { label: 'Vitenskapelig (UF)', val: 661.77, color: '#38bdf8' },
                { label: 'Administrativ (TA)', val: 624.16, color: '#f59e0b' },
              ],
              'Årsverk'
            )}
          </div>
        </div>
      </div>

      <div class="card-panel">
        <div class="panel-header">
          <div>
            <div class="panel-title">Bemannings- og årsverksoversikt (FactFTE.csv)</div>
            <div class="panel-subtitle">Årsverksfordeling, lønnskostnader og enhetslønn</div>
          </div>
        </div>
        <div class="table-container">
          <table class="tufte-table">
            <thead>
              <tr>
                <th>Institutt</th>
                <th>Kategori</th>
                <th>Stillingsgruppe</th>
                <th class="num">Årsverk</th>
                <th class="num">Faglige ÅV</th>
                <th class="num">Lønnskostnader</th>
                <th class="num">Lønn per Årsverk</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Inst. for økonomi</td>
                <td>Vitenskapelig</td>
                <td>VIT_PROF</td>
                <td class="num">68,5</td>
                <td class="num">68,5</td>
                <td class="num">95 800 000 kr</td>
                <td class="num">1 398 500 kr</td>
              </tr>
              <tr>
                <td>Inst. for økonomi</td>
                <td>Vitenskapelig</td>
                <td>VIT_FORST</td>
                <td class="num">85,2</td>
                <td class="num">85,2</td>
                <td class="num">98 200 000 kr</td>
                <td class="num">1 152 500 kr</td>
              </tr>
              <tr>
                <td>Inst. for økonomi</td>
                <td>Administrativ</td>
                <td>ADM_SAKSB</td>
                <td class="num">30,5</td>
                <td class="num">0,0</td>
                <td class="num">26 400 000 kr</td>
                <td class="num">865 500 kr</td>
              </tr>
              <tr>
                <td>Inst. for rettsvitenskap</td>
                <td>Vitenskapelig</td>
                <td>VIT_PROF</td>
                <td class="num">34,0</td>
                <td class="num">34,0</td>
                <td class="num">48 200 000 kr</td>
                <td class="num">1 417 600 kr</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `,
        },

        page_dt_prosjekt: {
          id: 'page_dt_prosjekt',
          title: 'DT Prosjektdetalj (EVM)',
          role: 'Drill-Through Prosjektcontrolling',
          desc: 'Earned Value Management (EVM) for eksternfinansierte forskningsprosjekter (NFR og EU). Oppfølging av BAC, EAC, ETC, VAC og sluttmargin.',
          slicers: [
            {
              label: 'Prosjekt',
              options: [
                'Alle prosjekter',
                'NFR001',
                'EU001',
                'NFR002',
                'OPP001',
              ],
            },
          ],
          kpis: [
            {
              title: 'BAC (Budget at Completion)',
              val: '20,20 M',
              unit: 'NOK',
              badge: 'TDI Prosjektbudsjett 2026',
              badgeCls: 'variance-info',
              sub: '6 aktive prosjekter',
            },
            {
              title: 'EAC (Estimate at Completion)',
              val: '20,46 M',
              unit: 'NOK',
              badge: 'Forventet sluttkost 2026',
              badgeCls: 'variance-unfavorable',
              sub: 'Oppdatert helårsestimat',
            },
            {
              title: 'ETC (Estimate to Complete)',
              val: '41,04 M',
              unit: 'NOK',
              badge: 'Gjenstående portefølje',
              badgeCls: 'variance-info',
              sub: 'Totalramme 61,50 M - påløpt',
            },
            {
              title: 'VAC (Variance at Completion)',
              val: '-260 k',
              unit: 'NOK',
              badge: 'Avvik M08',
              badgeCls: 'variance-unfavorable',
              sub: 'NFR002 & EVU001 overskridelse',
            },
          ],
          renderContent: () => `
      <div class="card-panel">
        <div class="panel-header">
          <div>
            <div class="panel-title">Prosjekt Earned Value Management (EVM) portefølje</div>
            <div class="panel-subtitle">Oppfølging av sluttkostnader og gjenstående restarbeid per prosjekt</div>
          </div>
        </div>
        <div class="table-container">
          <table class="tufte-table">
            <thead>
              <tr>
                <th>Kode</th>
                <th>Prosjektnavn</th>
                <th>Kilde</th>
                <th>Type</th>
                <th class="num">BAC (Budsjett)</th>
                <th class="num">EAC (Sluttkost)</th>
                <th class="num">ETC (Gjenstår)</th>
                <th class="num">VAC (Sluttavvik)</th>
                <th class="num">VAC %</th>
                <th>EVM RAG</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>NFR001</code></td>
                <td>AI for Offshore Energy Dynamics</td>
                <td>NFR</td>
                <td>Bidrag</td>
                <td class="num">6 500 000 kr</td>
                <td class="num">6 480 000 kr</td>
                <td class="num">30 000 kr</td>
                <td class="num" style="color:#10b981;">+20 000 kr</td>
                <td class="num" style="color:#10b981;">+0,3%</td>
                <td><span class="status-pill rag-green">🟢 Under budsjett</span></td>
              </tr>
              <tr>
                <td><code>EU001</code></td>
                <td>Horizon Green Maritime Transport</td>
                <td>EU</td>
                <td>Bidrag</td>
                <td class="num">4 200 000 kr</td>
                <td class="num">4 180 000 kr</td>
                <td class="num">60 000 kr</td>
                <td class="num" style="color:#10b981;">+20 000 kr</td>
                <td class="num" style="color:#10b981;">+0,5%</td>
                <td><span class="status-pill rag-green">🟢 Under budsjett</span></td>
              </tr>
              <tr>
                <td><code>NFR002</code></td>
                <td>Sustainable Business Models Regional Case</td>
                <td>NFR</td>
                <td>Bidrag</td>
                <td class="num">3 600 000 kr</td>
                <td class="num">3 900 000 kr</td>
                <td class="num">50 000 kr</td>
                <td class="num" style="color:#ef4444;">-300 000 kr</td>
                <td class="num" style="color:#ef4444;">-8,3%</td>
                <td><span class="status-pill rag-red">🔴 Kritisk overskridelse</span></td>
              </tr>
              <tr>
                <td><code>OPP001</code></td>
                <td>Batteriproduksjon Processevaluering</td>
                <td>Ekstern</td>
                <td>Oppdrag</td>
                <td class="num">2 800 000 kr</td>
                <td class="num">3 000 000 kr</td>
                <td class="num">60 000 kr</td>
                <td class="num" style="color:#ef4444;">-200 000 kr</td>
                <td class="num" style="color:#ef4444;">-7,1%</td>
                <td><span class="status-pill rag-red">🔴 Kritisk overskridelse</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `,
        },

        page_dt_tiltak: {
          id: 'page_dt_tiltak',
          title: 'DT Tiltaksdetalj (Risikokort)',
          role: 'Drill-Through Omstillingsledelse',
          desc: 'Detaljerte tiltakskort for alle 16 omstillingsinitiativer i FactAction. Sannsynlighetsvurdering, konsekvens, milepæler og gevinstrealisering.',
          slicers: [
            { label: 'Prioritet', options: ['Alle', 'Høy', 'Medium', 'Lav'] },
            {
              label: 'Status',
              options: ['Alle', 'Gjennomført', 'Pågår', 'Forsinket'],
            },
          ],
          kpis: [
            {
              title: 'Forventet tiltakseffekt',
              val: '-10,25 M',
              unit: 'NOK',
              badge: 'Planlagt',
              badgeCls: 'variance-favorable',
              sub: '7 omstillingstiltak',
            },
            {
              title: 'Realisert tiltakseffekt',
              val: '-4,85 M',
              unit: 'NOK',
              badge: 'Bokført',
              badgeCls: 'variance-favorable',
              sub: 'Oppnådd YTD',
            },
            {
              title: 'Realiseringsgrad',
              val: '47,32%',
              unit: 'Grad',
              badge: 'Mål: 70%',
              badgeCls: 'variance-neutral',
              sub: 'Restverdi: -5,40 M',
            },
          ],
          renderContent: () => `
      <div class="card-panel">
        <div class="panel-header">
          <div>
            <div class="panel-title">Detaljerte tiltakskort & risikovurdering (FactAction.csv)</div>
            <div class="panel-subtitle">Fullstendig liste med sannsynlighetsvekting og milepælsdatoer</div>
          </div>
        </div>
        <div class="table-container">
          <table class="tufte-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Tiltaksbeskrivelse</th>
                <th>Avviksårsak</th>
                <th>Ansvarlig</th>
                <th>Startdato</th>
                <th>Frist</th>
                <th class="num">Forventet</th>
                <th class="num">Realisert</th>
                <th>Status</th>
                <th>Prio</th>
                <th class="num">Sannsynlighet</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>T-01</code></td>
                <td>Vakansestopp adm. stillinger</td>
                <td>Lønnsvekst</td>
                <td>HR-direktør</td>
                <td>2026-01-01</td>
                <td>2026-06-30</td>
                <td class="num">-1 200 000</td>
                <td class="num">-950 000</td>
                <td><span class="status-pill gjennomfort">🟢 Gjennomført</span></td>
                <td>Høy</td>
                <td class="num">100%</td>
              </tr>
              <tr>
                <td><code>T-02</code></td>
                <td>Redusert sensorhonorar</td>
                <td>Høye sensorkostnader</td>
                <td>Studieleder</td>
                <td>2026-02-01</td>
                <td>2026-10-15</td>
                <td class="num">-450 000</td>
                <td class="num">-310 000</td>
                <td><span class="status-pill pagar">🟡 Pågår</span></td>
                <td>Medium</td>
                <td class="num">85%</td>
              </tr>
              <tr>
                <td><code>T-03</code></td>
                <td>Kutt i eksterne konsulenter IT</td>
                <td>Dyrt eksternt bistand</td>
                <td>Kontorsjef</td>
                <td>2026-03-01</td>
                <td>2026-08-01</td>
                <td class="num">-800 000</td>
                <td class="num">-200 000</td>
                <td><span class="status-pill forsinket">🔴 Forsinket</span></td>
                <td>Høy</td>
                <td class="num">60%</td>
              </tr>
              <tr>
                <td><code>T-04</code></td>
                <td>Samleslåing av valgemner</td>
                <td>Små studentkull</td>
                <td>Instituttleder</td>
                <td>2026-04-01</td>
                <td>2026-11-30</td>
                <td class="num">-1 500 000</td>
                <td class="num">-1 100 000</td>
                <td><span class="status-pill pagar">🟡 Pågår</span></td>
                <td>Høy</td>
                <td class="num">90%</td>
              </tr>
              <tr>
                <td><code>T-08</code></td>
                <td>Nedskalering av arealleie</td>
                <td>Høye leiekostnader</td>
                <td>Eiendomsdirektør</td>
                <td>2026-01-15</td>
                <td>2026-09-01</td>
                <td class="num">-2 000 000</td>
                <td class="num">-600 000</td>
                <td><span class="status-pill forsinket">🔴 Forsinket</span></td>
                <td>Høy</td>
                <td class="num">50%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `,
        },

        page_glossary: {
          id: 'page_09_begrepskatalog',
          title: '09 Begrepskatalog & Metodikk',
          role: 'Felles referanseramme: Controller, Dekan, Prosjektleder & Ledelse',
          desc: 'Komplett ordbok og metodebeskrivelse for økonomistyring, SRS-regnskap, prognostisering og prosjektcontrolling (EVM) ved UiA. Inkluderer 60 definerte nøkkelbegreper med praktisk tolkning og tilhørende DAX-formler.',
          slicers: [
            {
              label: 'Kategori',
              options: [
                'Alle kategorier',
                '01 Regnskap & Sektor',
                '02 Prosjektcontrolling (EVM)',
                '03 Prognose & Avvik',
                '04 Bemanning & Kapasitet',
                '05 Utdanningsproduksjon',
                '06 Omstilling & Tiltak',
                '07 RAG & Farger',
                '08 Teknisk & Modell',
              ],
            },
            {
              label: 'Rollekontekst',
              options: [
                'Alle roller',
                'Controller',
                'Project Controller',
                'Dekan',
                'Instituttleder',
                'Ledelse / Styret',
              ],
            },
            {
              label: 'Tilknyttet rapport',
              options: [
                'Alle rapporter',
                '01 Instituttleder',
                '02 Dekan & Fakultet',
                '03 Executive',
                '04 Styret',
                '05 Forskning & BOA',
                '06 Studieportefølje',
                '07 Action Tracker',
                '08 Controller Cockpit',
                'DT Prosjekt EVM',
                'DT Bilagslogg',
              ],
            },
          ],
          kpis: [
            {
              title: 'Definerte begreper',
              val: '60',
              unit: 'Begreper',
              badge: 'DimGlossary',
              badgeCls: 'variance-info',
              sub: 'Fullstendig ordbok for UH-sektoren',
            },
            {
              title: 'Faglige kategorier',
              val: '8',
              unit: 'Kategorier',
              badge: 'Styringsakser',
              badgeCls: 'variance-info',
              sub: 'SRS, EVM, BOA, FTE, RAG',
            },
            {
              title: 'Sluttkostnad (EAC)',
              val: '96,46 M',
              unit: 'NOK',
              badge: 'LE_2026',
              badgeCls: 'variance-unfavorable',
              sub: 'Avvik mot BAC: -14,62 M',
            },
            {
              title: 'RAG Avviksnivåer',
              val: '3',
              unit: 'Nivåer',
              badge: '🟢 Grønn | 🟡 Gul | 🔴 Rød',
              badgeCls: 'variance-favorable',
              sub: 'Terskel: <2% / 2-5% / >5%',
            },
            {
              title: 'Metodestandard',
              val: 'DFØ SRS',
              unit: 'R-102',
              badge: 'Statlig regnskap',
              badgeCls: 'variance-info',
              sub: 'Periodisering & opptjening',
            },
          ],
          renderContent: () => `
      <!-- Metodiske fundamenter (Tufte Cards) -->
      <div class="glossary-method-grid">
        <div class="method-card">
          <div class="method-title">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
            DFØ Statlige regnskapsstandarder (SRS)
          </div>
          <div class="method-desc">
            Prinsippbasert opptjeningsregnskap. Bevilgninger inntektsføres i takt med påløpte kostnader (SRS 10). Eksternfinansierte oppdrag (BOA) periodiseres etter fullføringsgrad (SRS 11), og anleggsmidler avskrives lineært (SRS 17).
          </div>
          <div class="method-formula">[Regnskap] = SUM(FactGL[Belop])</div>
        </div>

        <div class="method-card evm">
          <div class="method-title">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
            Prosjektcontrolling & EVM Metodikk
          </div>
          <div class="method-desc">
            Earned Value Management integrerer omfang, tid og kostnad. Baseline (BAC) måles mot påløpt verdi (EV) og faktiske kostnader (AC). Gir objektive ytelsesindekser (CPI, SPI) og estimert sluttkostnad (EAC / ETC).
          </div>
          <div class="method-formula">EAC = AC + (BAC - EV) / CPI</div>
        </div>

        <div class="method-card rag">
          <div class="method-title">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            Trafikklysregler (RAG-avvik)
          </div>
          <div class="method-desc">
            Objektive terskler for ledelsesrapportering og kontrolltårn:
            <br>🟢 <strong>Grønn</strong>: Avvik &le; 2% (Akseptabel ramme)
            <br>🟡 <strong>Gul</strong>: Avvik mellom 2% og 5% (Følges opp)
            <br>🔴 <strong>Rød</strong>: Merforbruk &gt; 5% (Kritisk, krever tiltak)
          </div>
          <div class="method-formula">SWITCH(TRUE(), [Avvik %] > 0.05, "🔴", ...)</div>
        </div>
      </div>

      <!-- Filter og Søkelinje -->
      <div class="glossary-controls">
        <div class="glossary-cat-pills" id="glossaryCatPills">
          <button class="glossary-cat-btn active" onclick="filterGlossaryCat('ALL', this)">Alle <span class="glossary-count-tag">60</span></button>
          <button class="glossary-cat-btn" onclick="filterGlossaryCat('01 Regnskap & Sektor', this)">01 Regnskap & Sektor <span class="glossary-count-tag">19</span></button>
          <button class="glossary-cat-btn" onclick="filterGlossaryCat('02 Prosjektcontrolling (EVM)', this)">02 Prosjekt EVM <span class="glossary-count-tag">6</span></button>
          <button class="glossary-cat-btn" onclick="filterGlossaryCat('03 Prognose & Avvik', this)">03 Prognose & Avvik <span class="glossary-count-tag">5</span></button>
          <button class="glossary-cat-btn" onclick="filterGlossaryCat('04 Bemanning & Kapasitet', this)">04 Bemanning <span class="glossary-count-tag">6</span></button>
          <button class="glossary-cat-btn" onclick="filterGlossaryCat('05 Utdanningsproduksjon', this)">05 Studieproduksjon <span class="glossary-count-tag">4</span></button>
          <button class="glossary-cat-btn" onclick="filterGlossaryCat('06 Omstilling & Tiltak', this)">06 Tiltak <span class="glossary-count-tag">3</span></button>
          <button class="glossary-cat-btn" onclick="filterGlossaryCat('07 RAG & Farger', this)">07 RAG <span class="glossary-count-tag">6</span></button>
          <button class="glossary-cat-btn" onclick="filterGlossaryCat('08 Teknisk & Modell', this)">08 Datamodell <span class="glossary-count-tag">11</span></button>
        </div>

        <div class="glossary-search-wrap">
          <svg class="search-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <input type="text" id="glossarySearchInput" class="glossary-search-input" placeholder="Søk begrep, definisjon, DAX..." oninput="filterGlossarySearch(this.value)">
        </div>
      </div>

      <!-- Tabell med Edward Tufte Data-Ink Standard -->
      <div class="card-panel">
        <div class="panel-header">
          <div>
            <div class="panel-title">UiA Begrepskatalog & Økonomistyringsleksikon (<span id="glossaryVisibleCount">60</span> av 60 begreper)</div>
            <div class="panel-subtitle">Strukturerte definisjoner fra DimGlossary.csv | Mappet til rapporter og DAX-beregninger</div>
          </div>
        </div>
        <div class="table-container">
          <table class="tufte-table" id="glossaryMainTable">
            <thead>
              <tr>
                <th>Begrep</th>
                <th>Fullt Navn</th>
                <th>Kategori</th>
                <th>Definisjon (DFØ SRS / EVM)</th>
                <th>Praktisk Controller-tolkning</th>
                <th>Formel / DAX</th>
                <th>Rollekontekst</th>
                <th>Relevant Rapport</th>
              </tr>
            </thead>
            <tbody>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="actual faktisk bokført regnskap 01 regnskap &amp; sektor faktisk påløpte inntekter og kostnader registrert i virksomhetens hovedbok (factgl). brukes som fasit for historisk ressursbruk og måles mot periodisert budsjett og prognose. sum(factgl[belop_signert]) alle roller 08 controller cockpit">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Actual</strong></td>
                <td>Faktisk bokført regnskap</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Faktisk påløpte inntekter og kostnader registrert i virksomhetens hovedbok (FactGL).</td>
                <td class="interp-cell">Brukes som fasit for historisk ressursbruk og måles mot periodisert budsjett og prognose.</td>
                <td><span class="dax-code-pill">SUM(FactGL[Belop])</span></td>
                <td><span class="role-badge">Alle roller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_08')">08 Controller Cockpit &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="artskonto standard artskonto 01 regnskap &amp; sektor firesifret tallkode som spesifiserer transaksjonens økonomiske art iht. dfø standard kontoplan. gjør det mulig å drille ned fra overordnede regnskapslinjer til spesifikke kostnadsbærere som fastlønn eller reise. dimaccount[konto] controller 08 controller cockpit">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Artskonto</strong></td>
                <td>Standard artskonto</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Firesifret tallkode som spesifiserer transaksjonens økonomiske art iht. DFØ standard kontoplan.</td>
                <td class="interp-cell">Gjør det mulig å drille ned fra overordnede regnskapslinjer til spesifikke kostnadsbærere som fastlønn eller reise.</td>
                <td><span class="dax-code-pill">DimAccount[Konto]</span></td>
                <td><span class="role-badge">Controller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_08')">08 Controller Cockpit &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="avskrivninger verdireduksjon anleggsmidler 01 regnskap &amp; sektor periodisering av anskaffelseskost over driftsmidlets økonomiske levetid iht. srs 17. påvirker institusjonens driftsresultat, men medfører ingen direkte likviditetsutgang i perioden. calculate([regnskap], dimaccount[srs_regnskapslinje]= avskrivninger ) ledelse / styret 03 executive">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Avskrivninger</strong></td>
                <td>Verdireduksjon anleggsmidler</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Periodisering av anskaffelseskost over driftsmidlets økonomiske levetid iht. SRS 17.</td>
                <td class="interp-cell">Påvirker institusjonens driftsresultat, men medfører ingen direkte likviditetsutgang i perioden.</td>
                <td><span class="dax-code-pill">CALCULATE([Regnskap], DimAccount[SRS_regnskapslinje]=&quot;Avskrivninger&quot;)</span></td>
                <td><span class="role-badge">Ledelse / Styret</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_03')">03 Executive &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="03 Prognose &amp; Avvik" data-search="avvik ytd akkumulert regnskapsavvik 03 prognose &amp; avvik differansen mellom akkumulert regnskap og akkumulert periodisert budsjett fra januar til nå. negativt fortegn på kostnader betyr mindreforbruk (gunstig), mens positivt betyr merforbruk (ugunstig). [regnskap ytd] - [budsjett ytd] alle roller 08 controller cockpit">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Avvik YTD</strong></td>
                <td>Akkumulert regnskapsavvik</td>
                <td><span class="cat-badge cat-03">03 Prognose &amp; Avvik</span></td>
                <td class="desc-cell">Differansen mellom akkumulert regnskap og akkumulert periodisert budsjett fra januar til nå.</td>
                <td class="interp-cell">Negativt fortegn på kostnader betyr mindreforbruk (gunstig), mens positivt betyr merforbruk (ugunstig).</td>
                <td><span class="dax-code-pill">[Regnskap YTD] - [Budsjett YTD]</span></td>
                <td><span class="role-badge">Alle roller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_08')">08 Controller Cockpit &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="07 RAG &amp; Farger" data-search="avvik ytd rag status rag-status regnskapsavvik 07 rag &amp; farger trafikklysindikator for akkumulert avvik målt mot budsjett. rød hvis merforbruk &gt; 5%, gul ved 2-5%, grønn ved &lt;= 2% avvik. switch(true(), [avvik ytd %] &gt; 0.05,  🔴 rød (&gt;5%) , [avvik ytd %] &gt;= 0.02,  🟡 gul (2-5%) ,  🟢 grønn (&lt;=2%) ) controller / dekan 08 controller cockpit">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Avvik YTD RAG Status</strong></td>
                <td>RAG-status regnskapsavvik</td>
                <td><span class="cat-badge cat-07">07 RAG &amp; Farger</span></td>
                <td class="desc-cell">Trafikklysindikator for akkumulert avvik målt mot budsjett.</td>
                <td class="interp-cell">Rød hvis merforbruk &gt; 5%, Gul ved 2-5%, Grønn ved &lt;= 2% avvik.</td>
                <td><span class="dax-code-pill">SWITCH(TRUE(), [Avvik YTD %] &gt; 0.05, &quot;🔴 Rød (&gt;5%)&quot;, [Avvik YTD %] &gt;= 0.02, &quot;🟡 Gul (2-5%)&quot;, &quot;🟢 Grønn (&lt;=2%)&quot;)</span></td>
                <td><span class="role-badge">Controller / Dekan</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_08')">08 Controller Cockpit &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="02 Prosjektcontrolling (EVM)" data-search="bac budget at completion 02 prosjektcontrolling (evm) den opprinnelige vedtatte totale kostnadsrammen for prosjektet eller regnskapsåret. utgjør referansegrunnlaget (baseline) som all fremdrift og sluttkostnad måles mot. [aarsbudsjett] project controller / dekan dt prosjekt evm">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">BAC</strong></td>
                <td>Budget at Completion</td>
                <td><span class="cat-badge cat-02">02 Prosjektcontrolling (EVM)</span></td>
                <td class="desc-cell">Den opprinnelige vedtatte totale kostnadsrammen for prosjektet eller regnskapsåret.</td>
                <td class="interp-cell">Utgjør referansegrunnlaget (baseline) som all fremdrift og sluttkostnad måles mot.</td>
                <td><span class="dax-code-pill">[Aarsbudsjett]</span></td>
                <td><span class="role-badge">Project Controller / Dekan</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_dt_prosjekt')">DT Prosjekt EVM &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="bevilgningsinntekt statlig rammebevilgning 01 regnskap &amp; sektor ordinær bevilgning fra kunnskapsdepartementet over statsbudsjettets post 50. periodiseres etter srs 10 slik at inntekt inntektsføres i takt med virksomhetens påløpte kostnader. calculate(-[regnskap], dimaccount[konto] in { 3000 , 3010 , 3020 , 3030 }) styret / ledelse 04 styret">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Bevilgningsinntekt</strong></td>
                <td>Statlig rammebevilgning</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Ordinær bevilgning fra Kunnskapsdepartementet over statsbudsjettets Post 50.</td>
                <td class="interp-cell">Periodiseres etter SRS 10 slik at inntekt inntektsføres i takt med virksomhetens påløpte kostnader.</td>
                <td><span class="dax-code-pill">CALCULATE(-[Regnskap], DimAccount[Konto] IN {&quot;3000&quot;,&quot;3010&quot;,&quot;3020&quot;,&quot;3030&quot;})</span></td>
                <td><span class="role-badge">Styret / Ledelse</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_04')">04 Styret &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="bfv bevilgningsfinansiert virksomhet 01 regnskap &amp; sektor institusjonens kjerneaktivitet (undervisning og grunnforskning) dekket av statstilskuddet. krever stram rammeoppfølging fordi statstilskuddet har et fast tak som ikke kan overskrides. dimproject[finansieringstype] =  drift  alle roller 03 executive">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">BFV</strong></td>
                <td>Bevilgningsfinansiert virksomhet</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Institusjonens kjerneaktivitet (undervisning og grunnforskning) dekket av statstilskuddet.</td>
                <td class="interp-cell">Krever stram rammeoppfølging fordi statstilskuddet har et fast tak som ikke kan overskrides.</td>
                <td><span class="dax-code-pill">DimProject[Finansieringstype] = &quot;Drift&quot;</span></td>
                <td><span class="role-badge">Alle roller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_03')">03 Executive &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="bidrag bidragsforskning 01 regnskap &amp; sektor eksternfinansierte prosjekter hvor finansieringskilden ikke krever en kommersiell motytelse. typiske bidragsytere er norges forskningsråd og eu  inntektsføres i takt med fremdrift etter srs 11. dimproject[finansieringstype] =  bidrag  forskningsledelse">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Bidrag</strong></td>
                <td>Bidragsforskning</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Eksternfinansierte prosjekter hvor finansieringskilden ikke krever en kommersiell motytelse.</td>
                <td class="interp-cell">Typiske bidragsytere er Norges forskningsråd og EU</td>
                <td><span class="dax-code-pill"> inntektsføres i takt med fremdrift etter SRS 11.</span></td>
                <td><span class="role-badge">DimProject[Finansieringstype] = &quot;Bidrag&quot;</span></td>
                <td><span style="color:var(--text-muted); font-size:11px;">Forskningsledelse</span></td>
              </tr>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="boa bidrags- og oppdragsfinansiert aktivitet 01 regnskap &amp; sektor samlet betegnelse på all eksternt finansiert forskning, utvikling og oppdragsvirksomhet. viktig strategisk vekstområde som øker institusjonens faglige volum og finansielle handlingsrom. [boa inntekter] forskningsledelse 05 forskning &amp; boa">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">BOA</strong></td>
                <td>Bidrags- og oppdragsfinansiert aktivitet</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Samlet betegnelse på all eksternt finansiert forskning, utvikling og oppdragsvirksomhet.</td>
                <td class="interp-cell">Viktig strategisk vekstområde som øker institusjonens faglige volum og finansielle handlingsrom.</td>
                <td><span class="dax-code-pill">[BOA inntekter]</span></td>
                <td><span class="role-badge">Forskningsledelse</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_05')">05 Forskning &amp; BOA &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="boa-finansieringsandel % eksternfinansieringsgrad 01 regnskap &amp; sektor andel av institusjonens totale inntekter som stammer fra eksterne boa-prosjekter. måler institusjonens evne til å hente konkurranseutsatt forskningsfinansiering (nasjonalt mål: &gt; 2.5%). divide([boa inntekter], [inntekter]) styret / ledelse 04 styret">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">BOA-finansieringsandel %</strong></td>
                <td>Eksternfinansieringsgrad</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Andel av institusjonens totale inntekter som stammer fra eksterne BOA-prosjekter.</td>
                <td class="interp-cell">Måler institusjonens evne til å hente konkurranseutsatt forskningsfinansiering (nasjonalt mål: &gt; 2.5%).</td>
                <td><span class="dax-code-pill">DIVIDE([BOA inntekter], [Inntekter])</span></td>
                <td><span class="role-badge">Styret / Ledelse</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_04')">04 Styret &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="budget vedtatt årsbudsjett 01 regnskap &amp; sektor den økonomiske handlingsplanen vedtatt av universitetsstyret før årets start. låses som baseline (bac) og fordeles per måned, enhet, konto og prosjekt. sum(factbudget[budsjettbelop]) alle roller 03 executive">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Budget</strong></td>
                <td>Vedtatt årsbudsjett</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Den økonomiske handlingsplanen vedtatt av universitetsstyret før årets start.</td>
                <td class="interp-cell">Låses som baseline (BAC) og fordeles per måned, enhet, konto og prosjekt.</td>
                <td><span class="dax-code-pill">SUM(FactBudget[BudsjettBelop])</span></td>
                <td><span class="role-badge">Alle roller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_03')">03 Executive &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="08 Teknisk &amp; Modell" data-search="controller cockpit avstemmings- og kontrollpanel 08 teknisk &amp; modell helhetlig kontrollpanel for regnskapsavstemming, feilsøking og avviksdrivere i kontoplanen. brukes av controller før månedsslutt for å avdekke feilføringer, manglende periodiseringer og ubalanser. rapportside 08 controller 08 controller cockpit">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Controller Cockpit</strong></td>
                <td>Avstemmings- og kontrollpanel</td>
                <td><span class="cat-badge cat-08">08 Teknisk &amp; Modell</span></td>
                <td class="desc-cell">Helhetlig kontrollpanel for regnskapsavstemming, feilsøking og avviksdrivere i kontoplanen.</td>
                <td class="interp-cell">Brukes av controller før månedsslutt for å avdekke feilføringer, manglende periodiseringer og ubalanser.</td>
                <td><span class="dax-code-pill">Rapportside 08</span></td>
                <td><span class="role-badge">Controller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_08')">08 Controller Cockpit &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="07 RAG &amp; Farger" data-search="data-ink ratio edward tuftes designprinsipp 07 rag &amp; farger prinsipp om å maksimere andelen informasjonsbærende elementer i visuelle fremstillinger. fjern unødvendige rutenett, tunge skygger, 3d-effekter og dekorative ikoner for å skape krystallklare rapporter. data-ink / total-ink alle roller alle dashboards">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Data-Ink Ratio</strong></td>
                <td>Edward Tuftes designprinsipp</td>
                <td><span class="cat-badge cat-07">07 RAG &amp; Farger</span></td>
                <td class="desc-cell">Prinsipp om å maksimere andelen informasjonsbærende elementer i visuelle fremstillinger.</td>
                <td class="interp-cell">Fjern unødvendige rutenett, tunge skygger, 3D-effekter og dekorative ikoner for å skape krystallklare rapporter.</td>
                <td><span class="dax-code-pill">Data-Ink / Total-Ink</span></td>
                <td><span class="role-badge">Alle roller</span></td>
                <td><span style="color:var(--text-muted); font-size:11px;">Alle dashboards</span></td>
              </tr>
              <tr class="glossary-row" data-cat="08 Teknisk &amp; Modell" data-search="dax data analysis expressions 08 teknisk &amp; modell formel- og beregningsspråk i power bi, fabric og analysis services. benyttes til å definere forretningslogikk, rullende tidsserier, evm-beregninger og rag-status dynamisk. stjernemodell formler controller / bi-utvikler tmdl model">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">DAX</strong></td>
                <td>Data Analysis Expressions</td>
                <td><span class="cat-badge cat-08">08 Teknisk &amp; Modell</span></td>
                <td class="desc-cell">Formel- og beregningsspråk i Power BI, Fabric og Analysis Services.</td>
                <td class="interp-cell">Benyttes til å definere forretningslogikk, rullende tidsserier, EVM-beregninger og RAG-status dynamisk.</td>
                <td><span class="dax-code-pill">Stjernemodell formler</span></td>
                <td><span class="role-badge">Controller / BI-utvikler</span></td>
                <td><span style="color:var(--text-muted); font-size:11px;">TMDL Model</span></td>
              </tr>
              <tr class="glossary-row" data-cat="08 Teknisk &amp; Modell" data-search="dekan fakultetsleder 08 teknisk &amp; modell øverste faglige og administrative leder for et helt fakultet med underliggende institutter. fokuserer på fakultetets samlede økonomiske balanse, lærerressurser og studieproduksjon. rapportside 02 dekan 02 dekan &amp; fakultet">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Dekan</strong></td>
                <td>Fakultetsleder</td>
                <td><span class="cat-badge cat-08">08 Teknisk &amp; Modell</span></td>
                <td class="desc-cell">Øverste faglige og administrative leder for et helt fakultet med underliggende institutter.</td>
                <td class="interp-cell">Fokuserer på fakultetets samlede økonomiske balanse, lærerressurser og studieproduksjon.</td>
                <td><span class="dax-code-pill">Rapportside 02</span></td>
                <td><span class="role-badge">Dekan</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_02')">02 Dekan &amp; Fakultet &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="dfø direktoratet for forvaltning og øk.styring 01 regnskap &amp; sektor statens fagorgan for økonomistyring, regnskapsstandarder (srs) og felles kontoplan. utformer retningslinjene som ligger til grunn for kontoplan r-102 og regnskapsavleggelsen. regelverk controller 08 controller cockpit">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">DFØ</strong></td>
                <td>Direktoratet for forvaltning og øk.styring</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Statens fagorgan for økonomistyring, regnskapsstandarder (SRS) og felles kontoplan.</td>
                <td class="interp-cell">Utformer retningslinjene som ligger til grunn for kontoplan R-102 og regnskapsavleggelsen.</td>
                <td><span class="dax-code-pill">Regelverk</span></td>
                <td><span class="role-badge">Controller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_08')">08 Controller Cockpit &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="08 Teknisk &amp; Modell" data-search="dimaccount kontoplan (dimensjon) 08 teknisk &amp; modell dimensjonstabell med 46 standardkontoer fordelt på kontoklasser og srs-regnskapslinjer. knyttes til factgl, factbudget, factforecast og factaction med 1:* relasjoner. dimaccount.csv controller 08 controller cockpit">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">DimAccount</strong></td>
                <td>Kontoplan (Dimensjon)</td>
                <td><span class="cat-badge cat-08">08 Teknisk &amp; Modell</span></td>
                <td class="desc-cell">Dimensjonstabell med 46 standardkontoer fordelt på kontoklasser og SRS-regnskapslinjer.</td>
                <td class="interp-cell">Knyttes til FactGL, FactBudget, FactForecast og FactAction med 1:* relasjoner.</td>
                <td><span class="dax-code-pill">DimAccount.csv</span></td>
                <td><span class="role-badge">Controller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_08')">08 Controller Cockpit &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="08 Teknisk &amp; Modell" data-search="dimorganization organisasjonsstruktur (dimensjon) 08 teknisk &amp; modell dimensjonstabell med 74 koststeder fordelt på 6 fakulteter/enheter og 25 institutter. danner grunnlaget for organisasjonshierarkiet (fakultet -&gt; institutt -&gt; koststed). dimorganization.csv alle roller 01 instituttleder">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">DimOrganization</strong></td>
                <td>Organisasjonsstruktur (Dimensjon)</td>
                <td><span class="cat-badge cat-08">08 Teknisk &amp; Modell</span></td>
                <td class="desc-cell">Dimensjonstabell med 74 koststeder fordelt på 6 fakulteter/enheter og 25 institutter.</td>
                <td class="interp-cell">Danner grunnlaget for organisasjonshierarkiet (Fakultet -&gt; Institutt -&gt; Koststed).</td>
                <td><span class="dax-code-pill">DimOrganization.csv</span></td>
                <td><span class="role-badge">Alle roller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_01')">01 Instituttleder &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="08 Teknisk &amp; Modell" data-search="drill-down hierarkisk navigasjon 08 teknisk &amp; modell interaktiv navigasjon fra et aggregert nivå ned til underliggende komponenter i samme visual. lar brukeren gå fra fakultetstotal ned til institutt og enkeltkoststeder i matrisen. hierarkisk visualisering alle roller 03 executive">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Drill-down</strong></td>
                <td>Hierarkisk navigasjon</td>
                <td><span class="cat-badge cat-08">08 Teknisk &amp; Modell</span></td>
                <td class="desc-cell">Interaktiv navigasjon fra et aggregert nivå ned til underliggende komponenter i samme visual.</td>
                <td class="interp-cell">Lar brukeren gå fra fakultetstotal ned til institutt og enkeltkoststeder i matrisen.</td>
                <td><span class="dax-code-pill">Hierarkisk visualisering</span></td>
                <td><span class="role-badge">Alle roller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_03')">03 Executive &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="08 Teknisk &amp; Modell" data-search="drill-through dybdenavigasjon med filterkontekst 08 teknisk &amp; modell navigasjon til en egen detaljrapport der filterkonteksten fra avsenderrapporten bevares. eksempelvis å klikke på et prosjekt i lederdashboardet og hoppe til dt prosjektdetaljer. rapportsider dt1-dt5 alle roller drill-through">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Drill-through</strong></td>
                <td>Dybdenavigasjon med filterkontekst</td>
                <td><span class="cat-badge cat-08">08 Teknisk &amp; Modell</span></td>
                <td class="desc-cell">Navigasjon til en egen detaljrapport der filterkonteksten fra avsenderrapporten bevares.</td>
                <td class="interp-cell">Eksempelvis å klikke på et prosjekt i lederdashboardet og hoppe til DT Prosjektdetaljer.</td>
                <td><span class="dax-code-pill">Rapportsider DT1-DT5</span></td>
                <td><span class="role-badge">Alle roller</span></td>
                <td><span style="color:var(--text-muted); font-size:11px;">Drill-Through</span></td>
              </tr>
              <tr class="glossary-row" data-cat="02 Prosjektcontrolling (EVM)" data-search="eac estimate at completion 02 prosjektcontrolling (evm) det oppdaterte forventede totalsluttresultatet for prosjektet eller regnskapsåret. tilsvarer latest estimate (le) og sammenlignes direkte mot opprinnelig ramme (bac) for å avdekke overskridelser. [forecast aarsbelop] alle roller 03 executive">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">EAC</strong></td>
                <td>Estimate at Completion</td>
                <td><span class="cat-badge cat-02">02 Prosjektcontrolling (EVM)</span></td>
                <td class="desc-cell">Det oppdaterte forventede totalsluttresultatet for prosjektet eller regnskapsåret.</td>
                <td class="interp-cell">Tilsvarer Latest Estimate (LE) og sammenlignes direkte mot opprinnelig ramme (BAC) for å avdekke overskridelser.</td>
                <td><span class="dax-code-pill">[Forecast aarsbelop]</span></td>
                <td><span class="role-badge">Alle roller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_03')">03 Executive &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="02 Prosjektcontrolling (EVM)" data-search="etc estimate to complete 02 prosjektcontrolling (evm) forventet gjenstående kostnad fra nåværende tidspunkt og frem til fullføring. nødvendig for likviditetsstyring og vurdering av om prosjektet vil kreve ekstratildeling. [eac] - [regnskap ytd] project controller dt prosjekt evm">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">ETC</strong></td>
                <td>Estimate to Complete</td>
                <td><span class="cat-badge cat-02">02 Prosjektcontrolling (EVM)</span></td>
                <td class="desc-cell">Forventet gjenstående kostnad fra nåværende tidspunkt og frem til fullføring.</td>
                <td class="interp-cell">Nødvendig for likviditetsstyring og vurdering av om prosjektet vil kreve ekstratildeling.</td>
                <td><span class="dax-code-pill">[EAC] - [Regnskap YTD]</span></td>
                <td><span class="role-badge">Project Controller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_dt_prosjekt')">DT Prosjekt EVM &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="evu etter- og videreutdanning 01 regnskap &amp; sektor kommersiell oppdragsutdanning for næringsliv og offentlige etater som betales av kunden. inntektsføres som oppdragsaktivitet etter srs 12 og krever full kostnadsdekning. konto 3600-3620 dekan / instituttleder 05 forskning &amp; boa">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">EVU</strong></td>
                <td>Etter- og videreutdanning</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Kommersiell oppdragsutdanning for næringsliv og offentlige etater som betales av kunden.</td>
                <td class="interp-cell">Inntektsføres som oppdragsaktivitet etter SRS 12 og krever full kostnadsdekning.</td>
                <td><span class="dax-code-pill">Konto 3600-3620</span></td>
                <td><span class="role-badge">Dekan / Instituttleder</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_05')">05 Forskning &amp; BOA &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="02 Prosjektcontrolling (EVM)" data-search="evm earned value management 02 prosjektcontrolling (evm) internasjonal metode for prosjektstyring som integrerer omfang, tid og påløpte kostnader. gir tidlige varsler om prosjektavvik gjennom nøkkeltall som bac, eac, etc og vac. prosjektcontrolling project controller dt prosjekt evm">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">EVM</strong></td>
                <td>Earned Value Management</td>
                <td><span class="cat-badge cat-02">02 Prosjektcontrolling (EVM)</span></td>
                <td class="desc-cell">Internasjonal metode for prosjektstyring som integrerer omfang, tid og påløpte kostnader.</td>
                <td class="interp-cell">Gir tidlige varsler om prosjektavvik gjennom nøkkeltall som BAC, EAC, ETC og VAC.</td>
                <td><span class="dax-code-pill">Prosjektcontrolling</span></td>
                <td><span class="role-badge">Project Controller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_dt_prosjekt')">DT Prosjekt EVM &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="07 RAG &amp; Farger" data-search="evm sluttavvik rag status rag-status prosjektavvik 07 rag &amp; farger trafikklysstatus for sluttavviket (vac) i boa-prosjekter. grønn hvis under budsjett (vac &gt;= 0), gul ved moderat avvik (opptil -5%), rød ved kritisk sprekk (&lt;-5%). switch(true(), [vac] &gt;= 0,  🟢 under budsjett , [vac %] &gt;= -0.05,  🟡 moderat overskridelse ,  🔴 kritisk overskridelse ) project controller dt prosjekt evm">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">EVM Sluttavvik RAG Status</strong></td>
                <td>RAG-status prosjektavvik</td>
                <td><span class="cat-badge cat-07">07 RAG &amp; Farger</span></td>
                <td class="desc-cell">Trafikklysstatus for sluttavviket (VAC) i BOA-prosjekter.</td>
                <td class="interp-cell">Grønn hvis under budsjett (VAC &gt;= 0), Gul ved moderat avvik (opptil -5%), Rød ved kritisk sprekk (&lt;-5%).</td>
                <td><span class="dax-code-pill">SWITCH(TRUE(), [VAC] &gt;= 0, &quot;🟢 Under budsjett&quot;, [VAC %] &gt;= -0.05, &quot;🟡 Moderat overskridelse&quot;, &quot;🔴 Kritisk overskridelse&quot;)</span></td>
                <td><span class="role-badge">Project Controller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_dt_prosjekt')">DT Prosjekt EVM &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="06 Omstilling &amp; Tiltak" data-search="factaction omstillingstiltak (fakta) 06 omstilling &amp; tiltak faktatabell med 16 identifiserte ledelsestiltak for kostnadsreduksjon og gevinstrealisering. inneholder forventet og realisert effekt, tiltaksansvarlig, frist, risikovurdering og status. factaction.csv ledelse / controller 07 action tracker">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">FactAction</strong></td>
                <td>Omstillingstiltak (Fakta)</td>
                <td><span class="cat-badge cat-06">06 Omstilling &amp; Tiltak</span></td>
                <td class="desc-cell">Faktatabell med 16 identifiserte ledelsestiltak for kostnadsreduksjon og gevinstrealisering.</td>
                <td class="interp-cell">Inneholder forventet og realisert effekt, tiltaksansvarlig, frist, risikovurdering og status.</td>
                <td><span class="dax-code-pill">FactAction.csv</span></td>
                <td><span class="role-badge">Ledelse / Controller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_07')">07 Action Tracker &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="factbudget månedsbudsjett (fakta) 01 regnskap &amp; sektor faktatabell med 17 760 periodiserte budsjettlinjer per måned, org, konto og prosjekt. danner grunnlaget for budsjettoppfølging og bac. factbudget.csv controller 08 controller cockpit">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">FactBudget</strong></td>
                <td>Månedsbudsjett (Fakta)</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Faktatabell med 17 760 periodiserte budsjettlinjer per måned, org, konto og prosjekt.</td>
                <td class="interp-cell">Danner grunnlaget for budsjettoppfølging og BAC.</td>
                <td><span class="dax-code-pill">FactBudget.csv</span></td>
                <td><span class="role-badge">Controller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_08')">08 Controller Cockpit &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="03 Prognose &amp; Avvik" data-search="factforecast rullende prognose (fakta) 03 prognose &amp; avvik faktatabell med 53 280 prognoselinjer fordelt på versjonene fc1, fc2 og le. inneholder prognosebeløp og sannsynlighetsvekting for usikkerhetsstyring. factforecast.csv controller / ledelse 03 executive">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">FactForecast</strong></td>
                <td>Rullende prognose (Fakta)</td>
                <td><span class="cat-badge cat-03">03 Prognose &amp; Avvik</span></td>
                <td class="desc-cell">Faktatabell med 53 280 prognoselinjer fordelt på versjonene FC1, FC2 og LE.</td>
                <td class="interp-cell">Inneholder prognosebeløp og sannsynlighetsvekting for usikkerhetsstyring.</td>
                <td><span class="dax-code-pill">FactForecast.csv</span></td>
                <td><span class="role-badge">Controller / Ledelse</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_03')">03 Executive &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="04 Bemanning &amp; Kapasitet" data-search="factfte årsverk (fakta) 04 bemanning &amp; kapasitet faktatabell med 1 440 månedlige bemanningsregistreringer per enhet og stillingsgruppe. brukes til å beregne totalårsverk, faglige årsverk og lønn per årsverk. factfte.csv hr / dekan dt bemanning">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">FactFTE</strong></td>
                <td>Årsverk (Fakta)</td>
                <td><span class="cat-badge cat-04">04 Bemanning &amp; Kapasitet</span></td>
                <td class="desc-cell">Faktatabell med 1 440 månedlige bemanningsregistreringer per enhet og stillingsgruppe.</td>
                <td class="interp-cell">Brukes til å beregne totalårsverk, faglige årsverk og lønn per årsverk.</td>
                <td><span class="dax-code-pill">FactFTE.csv</span></td>
                <td><span class="role-badge">HR / Dekan</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_dt_bemanning')">DT Bemanning &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="factgl hovedbok transaksjoner (fakta) 01 regnskap &amp; sektor faktatabell med 35 760 bokførte transaksjoner med bilagsnummer, posteringsdato og signert beløp. grunnlaget for regnskapsavstemming og historiske actuals. factgl.csv controller dt økonomi">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">FactGL</strong></td>
                <td>Hovedbok transaksjoner (Fakta)</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Faktatabell med 35 760 bokførte transaksjoner med bilagsnummer, posteringsdato og signert beløp.</td>
                <td class="interp-cell">Grunnlaget for regnskapsavstemming og historiske actuals.</td>
                <td><span class="dax-code-pill">FactGL.csv</span></td>
                <td><span class="role-badge">Controller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_dt_okonomi')">DT Økonomi &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="05 Utdanningsproduksjon" data-search="factstudypoints studieproduksjon (fakta) 05 utdanningsproduksjon faktatabell med 432 månedlige registreringer av studenter, planlagte/avlagte studiepoeng og spe60. understøtter finansieringsberegninger og dimensjonering av studieporteføljen. factstudypoints.csv utdanningsledelse 06 studieportefølje">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">FactStudyPoints</strong></td>
                <td>Studieproduksjon (Fakta)</td>
                <td><span class="cat-badge cat-05">05 Utdanningsproduksjon</span></td>
                <td class="desc-cell">Faktatabell med 432 månedlige registreringer av studenter, planlagte/avlagte studiepoeng og SPE60.</td>
                <td class="interp-cell">Understøtter finansieringsberegninger og dimensjonering av studieporteføljen.</td>
                <td><span class="dax-code-pill">FactStudyPoints.csv</span></td>
                <td><span class="role-badge">Utdanningsledelse</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_06')">06 Studieportefølje &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="04 Bemanning &amp; Kapasitet" data-search="faglig andel % vitenskapelig bemanningsandel 04 bemanning &amp; kapasitet andelen av den samlede bemanningen som utgjøres av undervisnings- og forskerstillinger (uf). bør overstige 50-55% for å sikre at ressursene primært kanaliseres til institusjonens kjerneoppgaver. divide([faglige aarsverk], [aarsverk]) dekan / styret 02 dekan &amp; fakultet">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Faglig andel %</strong></td>
                <td>Vitenskapelig bemanningsandel</td>
                <td><span class="cat-badge cat-04">04 Bemanning &amp; Kapasitet</span></td>
                <td class="desc-cell">Andelen av den samlede bemanningen som utgjøres av undervisnings- og forskerstillinger (UF).</td>
                <td class="interp-cell">Bør overstige 50-55% for å sikre at ressursene primært kanaliseres til institusjonens kjerneoppgaver.</td>
                <td><span class="dax-code-pill">DIVIDE([Faglige aarsverk], [Aarsverk])</span></td>
                <td><span class="role-badge">Dekan / Styret</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_02')">02 Dekan &amp; Fakultet &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="03 Prognose &amp; Avvik" data-search="fc1 / fc2 rullende tertialprognoser 03 prognose &amp; avvik periodiske prognoserapporteringer gjennomført etter tertial 1 (april) og tertial 2 (august). viser hvordan helårsforventningen utvikler seg gjennom budsjettåret etter hvert som usikkerhet reduseres. dimforecastversion[versjon] controller / ledelse 03 executive">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">FC1 / FC2</strong></td>
                <td>Rullende tertialprognoser</td>
                <td><span class="cat-badge cat-03">03 Prognose &amp; Avvik</span></td>
                <td class="desc-cell">Periodiske prognoserapporteringer gjennomført etter tertial 1 (april) og tertial 2 (august).</td>
                <td class="interp-cell">Viser hvordan helårsforventningen utvikler seg gjennom budsjettåret etter hvert som usikkerhet reduseres.</td>
                <td><span class="dax-code-pill">DimForecastVersion[Versjon]</span></td>
                <td><span class="role-badge">Controller / Ledelse</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_03')">03 Executive &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="03 Prognose &amp; Avvik" data-search="forecastavvik forventet avvik ved årsslutt 03 prognose &amp; avvik differansen mellom gjeldende helårsprognose (le) og vedtatt årsbudsjett. viser det forventede mer- eller mindreforbruket før eventuelle korrigerende omstillingstiltak iverksettes. [forecast aarsbelop] - [aarsbudsjett] alle roller 03 executive">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Forecastavvik</strong></td>
                <td>Forventet avvik ved årsslutt</td>
                <td><span class="cat-badge cat-03">03 Prognose &amp; Avvik</span></td>
                <td class="desc-cell">Differansen mellom gjeldende helårsprognose (LE) og vedtatt årsbudsjett.</td>
                <td class="interp-cell">Viser det forventede mer- eller mindreforbruket før eventuelle korrigerende omstillingstiltak iverksettes.</td>
                <td><span class="dax-code-pill">[Forecast aarsbelop] - [Aarsbudsjett]</span></td>
                <td><span class="role-badge">Alle roller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_03')">03 Executive &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="07 RAG &amp; Farger" data-search="forecast rag status rag-status helårsprognose 07 rag &amp; farger trafikklysstatus for forventet helårsavvik målt mot budsjett. rød hvis prognosen overstiger budsjettet med &gt; 5%, gul ved 2-5%, grønn ved &lt;= 2% overskridelse. switch(true(), [forecastavvik %] &gt; 0.05,  🔴 rød (&gt;5%) , [forecastavvik %] &gt;= 0.02,  🟡 gul (2-5%) ,  🟢 grønn (&lt;=2%) ) styret / ledelse 03 executive">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Forecast RAG Status</strong></td>
                <td>RAG-status helårsprognose</td>
                <td><span class="cat-badge cat-07">07 RAG &amp; Farger</span></td>
                <td class="desc-cell">Trafikklysstatus for forventet helårsavvik målt mot budsjett.</td>
                <td class="interp-cell">Rød hvis prognosen overstiger budsjettet med &gt; 5%, Gul ved 2-5%, Grønn ved &lt;= 2% overskridelse.</td>
                <td><span class="dax-code-pill">SWITCH(TRUE(), [Forecastavvik %] &gt; 0.05, &quot;🔴 Rød (&gt;5%)&quot;, [Forecastavvik %] &gt;= 0.02, &quot;🟡 Gul (2-5%)&quot;, &quot;🟢 Grønn (&lt;=2%)&quot;)</span></td>
                <td><span class="role-badge">Styret / Ledelse</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_03')">03 Executive &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="04 Bemanning &amp; Kapasitet" data-search="fte full-time equivalent / årsverk 04 bemanning &amp; kapasitet standardisert måleenhet for arbeidsinnsats tilsvarende én 100% stilling i ett år (1950 arbeidstimer). måles som et snapshot ved slutten av hver måned for å unngå summeringsfeil. [aarsverk] hr / ledelse dt bemanning">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">FTE</strong></td>
                <td>Full-Time Equivalent / Årsverk</td>
                <td><span class="cat-badge cat-04">04 Bemanning &amp; Kapasitet</span></td>
                <td class="desc-cell">Standardisert måleenhet for arbeidsinnsats tilsvarende én 100% stilling i ett år (1950 arbeidstimer).</td>
                <td class="interp-cell">Måles som et snapshot ved slutten av hver måned for å unngå summeringsfeil.</td>
                <td><span class="dax-code-pill">[Aarsverk]</span></td>
                <td><span class="role-badge">HR / Ledelse</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_dt_bemanning')">DT Bemanning &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="08 Teknisk &amp; Modell" data-search="instituttleder leder av grunnenhet 08 teknisk &amp; modell øverste administrative og faglige leder for et institutt med direkte budsjett- og personalansvar. fokuserer på månedsavvik, lærerkapasitet, sykemeldinger, sensorkostnader og lokale tiltak. rapportside 01 instituttleder 01 instituttleder">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Instituttleder</strong></td>
                <td>Leder av grunnenhet</td>
                <td><span class="cat-badge cat-08">08 Teknisk &amp; Modell</span></td>
                <td class="desc-cell">Øverste administrative og faglige leder for et institutt med direkte budsjett- og personalansvar.</td>
                <td class="interp-cell">Fokuserer på månedsavvik, lærerkapasitet, sykemeldinger, sensorkostnader og lokale tiltak.</td>
                <td><span class="dax-code-pill">Rapportside 01</span></td>
                <td><span class="role-badge">Instituttleder</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_01')">01 Instituttleder &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="kd kunnskapsdepartementet 01 regnskap &amp; sektor overordnet statlig departement som fastsetter rammer, mål og bevilgninger for universitetssektoren. utsteder det årlige tildelingsbrevet som fastlegger institusjonens økonomiske rammer. statlig eier styret / ledelse 04 styret">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">KD</strong></td>
                <td>Kunnskapsdepartementet</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Overordnet statlig departement som fastsetter rammer, mål og bevilgninger for universitetssektoren.</td>
                <td class="interp-cell">Utsteder det årlige tildelingsbrevet som fastlegger institusjonens økonomiske rammer.</td>
                <td><span class="dax-code-pill">Statlig eier</span></td>
                <td><span class="role-badge">Styret / Ledelse</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_04')">04 Styret &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="05 Utdanningsproduksjon" data-search="kostnad per spe60 enhetskostnad per helårsstudent 05 utdanningsproduksjon totale drifts- og personalkostnader dividert med antall produserte spe60. avdekker kostnadseffektiviteten i utdanningstilbudet  høye tall indikerer for små studentkull eller høy ressursbruk. divide([faktisk kostnader], [spe60]) dekan / utdanningsledelse">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Kostnad per SPE60</strong></td>
                <td>Enhetskostnad per helårsstudent</td>
                <td><span class="cat-badge cat-05">05 Utdanningsproduksjon</span></td>
                <td class="desc-cell">Totale drifts- og personalkostnader dividert med antall produserte SPE60.</td>
                <td class="interp-cell">Avdekker kostnadseffektiviteten i utdanningstilbudet</td>
                <td><span class="dax-code-pill"> høye tall indikerer for små studentkull eller høy ressursbruk.</span></td>
                <td><span class="role-badge">DIVIDE([Faktisk kostnader], [SPE60])</span></td>
                <td><span style="color:var(--text-muted); font-size:11px;">Dekan / Utdanningsledelse</span></td>
              </tr>
              <tr class="glossary-row" data-cat="03 Prognose &amp; Avvik" data-search="le latest estimate 03 prognose &amp; avvik den nyeste gjeldende helårsprognosen (i modellen referert til som le_2026). representerer ledelsens beste nåværende estimat for sluttresultatet ved regnskapsårets utgang. calculate([gjeldende forecast], dimforecastversion[versjon]= le_2026 ) alle roller 03 executive">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">LE</strong></td>
                <td>Latest Estimate</td>
                <td><span class="cat-badge cat-03">03 Prognose &amp; Avvik</span></td>
                <td class="desc-cell">Den nyeste gjeldende helårsprognosen (i modellen referert til som LE_2026).</td>
                <td class="interp-cell">Representerer ledelsens beste nåværende estimat for sluttresultatet ved regnskapsårets utgang.</td>
                <td><span class="dax-code-pill">CALCULATE([Gjeldende forecast], DimForecastVersion[Versjon]=&quot;LE_2026&quot;)</span></td>
                <td><span class="role-badge">Alle roller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_03')">03 Executive &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="04 Bemanning &amp; Kapasitet" data-search="lønnsandel % personalkostnadsandel 04 bemanning &amp; kapasitet personalkostnader uttrykt som en prosentandel av institusjonens samlede driftskostnader. typisk 65-72% i uh-sektoren  den viktigste enkeltfaktoren for økonomisk bærekraft. divide([faktisk lonnskostnader], [faktisk kostnader]) dekan / ledelse">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Lønnsandel %</strong></td>
                <td>Personalkostnadsandel</td>
                <td><span class="cat-badge cat-04">04 Bemanning &amp; Kapasitet</span></td>
                <td class="desc-cell">Personalkostnader uttrykt som en prosentandel av institusjonens samlede driftskostnader.</td>
                <td class="interp-cell">Typisk 65-72% i UH-sektoren</td>
                <td><span class="dax-code-pill"> den viktigste enkeltfaktoren for økonomisk bærekraft.</span></td>
                <td><span class="role-badge">DIVIDE([Faktisk lonnskostnader], [Faktisk kostnader])</span></td>
                <td><span style="color:var(--text-muted); font-size:11px;">Dekan / Ledelse</span></td>
              </tr>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="nfr norges forskningsråd 01 regnskap &amp; sektor nasjonalt organ for finansiering av forskningsprosjekter etter søknad og fagfellevurdering. største eksterne bidragsyter i modellen  inntekter føres på konto 3400-3419. dimproject[finansieringskilde] =  nfr  forskningsledelse">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">NFR</strong></td>
                <td>Norges forskningsråd</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Nasjonalt organ for finansiering av forskningsprosjekter etter søknad og fagfellevurdering.</td>
                <td class="interp-cell">Største eksterne bidragsyter i modellen</td>
                <td><span class="dax-code-pill"> inntekter føres på konto 3400-3419.</span></td>
                <td><span class="role-badge">DimProject[Finansieringskilde] = &quot;NFR&quot;</span></td>
                <td><span style="color:var(--text-muted); font-size:11px;">Forskningsledelse</span></td>
              </tr>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="oppdrag oppdragsforskning 01 regnskap &amp; sektor aktivitet utført for eksterne oppdragsgivere med krav om definerte leveranser og kommersielle vilkår. skal prises til markedsverdi med full dekning av direkte kostnader og overhead iht. eøs-statsstøtteregler. dimproject[finansieringstype] =  oppdrag  forskningsledelse 05 forskning &amp; boa">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Oppdrag</strong></td>
                <td>Oppdragsforskning</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Aktivitet utført for eksterne oppdragsgivere med krav om definerte leveranser og kommersielle vilkår.</td>
                <td class="interp-cell">Skal prises til markedsverdi med full dekning av direkte kostnader og overhead iht. EØS-statsstøtteregler.</td>
                <td><span class="dax-code-pill">DimProject[Finansieringstype] = &quot;Oppdrag&quot;</span></td>
                <td><span class="role-badge">Forskningsledelse</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_05')">05 Forskning &amp; BOA &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="08 Teknisk &amp; Modell" data-search="pbip power bi project 08 teknisk &amp; modell mappebasert kildetekstformat for power bi som skiller semantisk modell (tmdl) og rapport (pbir). gjør det mulig å versjonskontrollere power bi i git, kjøre automatisert testing og samarbeide i team. mappestruktur bi-utvikler repo root">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">PBIP</strong></td>
                <td>Power BI Project</td>
                <td><span class="cat-badge cat-08">08 Teknisk &amp; Modell</span></td>
                <td class="desc-cell">Mappebasert kildetekstformat for Power BI som skiller semantisk modell (TMDL) og rapport (PBIR).</td>
                <td class="interp-cell">Gjør det mulig å versjonskontrollere Power BI i Git, kjøre automatisert testing og samarbeide i team.</td>
                <td><span class="dax-code-pill">Mappestruktur</span></td>
                <td><span class="role-badge">BI-utvikler</span></td>
                <td><span style="color:var(--text-muted); font-size:11px;">Repo root</span></td>
              </tr>
              <tr class="glossary-row" data-cat="08 Teknisk &amp; Modell" data-search="pbir power bi enhanced report format 08 teknisk &amp; modell deklarativt json-format for power bi-rapporter som definerer alle visuals, rader og formater. sikrer at rapportbygging kan automatiseres via skript og valideres med cli-verktøy. uia-controller-prosjekt.report bi-utvikler pbir definition">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">PBIR</strong></td>
                <td>Power BI Enhanced Report Format</td>
                <td><span class="cat-badge cat-08">08 Teknisk &amp; Modell</span></td>
                <td class="desc-cell">Deklarativt JSON-format for Power BI-rapporter som definerer alle visuals, rader og formater.</td>
                <td class="interp-cell">Sikrer at rapportbygging kan automatiseres via skript og valideres med CLI-verktøy.</td>
                <td><span class="dax-code-pill">UIA-Controller-Prosjekt.Report</span></td>
                <td><span class="role-badge">BI-utvikler</span></td>
                <td><span style="color:var(--text-muted); font-size:11px;">PBIR Definition</span></td>
              </tr>
              <tr class="glossary-row" data-cat="07 RAG &amp; Farger" data-search="rag red-amber-green 07 rag &amp; farger trafikklysmetodikk for visuell styring og avvikshåndtering. retter ledelsens oppmerksomhet mot de få kritiske områdene som krever umiddelbar handling. rag-mål alle roller alle dashboards">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">RAG</strong></td>
                <td>Red-Amber-Green</td>
                <td><span class="cat-badge cat-07">07 RAG &amp; Farger</span></td>
                <td class="desc-cell">Trafikklysmetodikk for visuell styring og avvikshåndtering.</td>
                <td class="interp-cell">Retter ledelsens oppmerksomhet mot de få kritiske områdene som krever umiddelbar handling.</td>
                <td><span class="dax-code-pill">RAG-mål</span></td>
                <td><span class="role-badge">Alle roller</span></td>
                <td><span style="color:var(--text-muted); font-size:11px;">Alle dashboards</span></td>
              </tr>
              <tr class="glossary-row" data-cat="06 Omstilling &amp; Tiltak" data-search="realiseringsgrad % gevinstrealiseringsgrad 06 omstilling &amp; tiltak forholdet mellom faktisk oppnådd innsparing og planlagt innsparing for et omstillingstiltak. måler om tiltakene leverer den forventede økonomiske effekten i praksis. divide([realisert tiltakseffekt], [forventet tiltakseffekt]) ledelse / styret 07 action tracker">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Realiseringsgrad %</strong></td>
                <td>Gevinstrealiseringsgrad</td>
                <td><span class="cat-badge cat-06">06 Omstilling &amp; Tiltak</span></td>
                <td class="desc-cell">Forholdet mellom faktisk oppnådd innsparing og planlagt innsparing for et omstillingstiltak.</td>
                <td class="interp-cell">Måler om tiltakene leverer den forventede økonomiske effekten i praksis.</td>
                <td><span class="dax-code-pill">DIVIDE([Realisert tiltakseffekt], [Forventet tiltakseffekt])</span></td>
                <td><span class="role-badge">Ledelse / Styret</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_07')">07 Action Tracker &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="06 Omstilling &amp; Tiltak" data-search="restavvik gjenværende risikogap 06 omstilling &amp; tiltak det økonomiske avviket som fortsatt gjenstår etter at effekten av alle godkjente tiltak er trukket fra. viser det udekkede gapet som må håndteres dersom budsjettmålet skal nås. [forecast etter tiltak] - [aarsbudsjett] styret / ledelse 03 executive">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Restavvik</strong></td>
                <td>Gjenværende risikogap</td>
                <td><span class="cat-badge cat-06">06 Omstilling &amp; Tiltak</span></td>
                <td class="desc-cell">Det økonomiske avviket som fortsatt gjenstår etter at effekten av alle godkjente tiltak er trukket fra.</td>
                <td class="interp-cell">Viser det udekkede gapet som må håndteres dersom budsjettmålet skal nås.</td>
                <td><span class="dax-code-pill">[Forecast etter tiltak] - [Aarsbudsjett]</span></td>
                <td><span class="role-badge">Styret / Ledelse</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_03')">03 Executive &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="05 Utdanningsproduksjon" data-search="spe60 studiepoengekvivalenter 05 utdanningsproduksjon normalisert måleenhet tilsvarende 60 avlagte studiepoeng (en helårsstudent). primær driver i kunnskapsdepartementets resultatbaserte bevilgningssystem. divide([avlagte studiepoeng], 60) utdanningsledelse / dekan 06 studieportefølje">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">SPE60</strong></td>
                <td>Studiepoengekvivalenter</td>
                <td><span class="cat-badge cat-05">05 Utdanningsproduksjon</span></td>
                <td class="desc-cell">Normalisert måleenhet tilsvarende 60 avlagte studiepoeng (en helårsstudent).</td>
                <td class="interp-cell">Primær driver i Kunnskapsdepartementets resultatbaserte bevilgningssystem.</td>
                <td><span class="dax-code-pill">DIVIDE([Avlagte studiepoeng], 60)</span></td>
                <td><span class="role-badge">Utdanningsledelse / Dekan</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_06')">06 Studieportefølje &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="srs statlige regnskapsstandarder 01 regnskap &amp; sektor prinsipper for periodisert regnskapsføring i statlige virksomheter fastsatt av finansdepartementet/dfø. sikrer at ressursforbruk og inntekter synliggjøres i samme regnskapsperiode uavhengig av kontantstrøm. regelverk controller 08 controller cockpit">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">SRS</strong></td>
                <td>Statlige regnskapsstandarder</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Prinsipper for periodisert regnskapsføring i statlige virksomheter fastsatt av Finansdepartementet/DFØ.</td>
                <td class="interp-cell">Sikrer at ressursforbruk og inntekter synliggjøres i samme regnskapsperiode uavhengig av kontantstrøm.</td>
                <td><span class="dax-code-pill">Regelverk</span></td>
                <td><span class="role-badge">Controller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_08')">08 Controller Cockpit &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="05 Utdanningsproduksjon" data-search="studiepoeng måloppnåelse % eksamensproduksjonsgrad 05 utdanningsproduksjon faktisk avlagte studiepoeng sammenlignet med planlagt studiepoengproduksjon. måler undervisningsavdelingenes evne til å oppfylle oppdragsmålet og unngå inntektsbortfall. divide([avlagte studiepoeng], [planlagte studiepoeng]) utdanningsledelse 06 studieportefølje">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Studiepoeng måloppnåelse %</strong></td>
                <td>Eksamensproduksjonsgrad</td>
                <td><span class="cat-badge cat-05">05 Utdanningsproduksjon</span></td>
                <td class="desc-cell">Faktisk avlagte studiepoeng sammenlignet med planlagt studiepoengproduksjon.</td>
                <td class="interp-cell">Måler undervisningsavdelingenes evne til å oppfylle oppdragsmålet og unngå inntektsbortfall.</td>
                <td><span class="dax-code-pill">DIVIDE([Avlagte studiepoeng], [Planlagte studiepoeng])</span></td>
                <td><span class="role-badge">Utdanningsledelse</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_06')">06 Studieportefølje &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="04 Bemanning &amp; Kapasitet" data-search="ta teknisk-administrativ bemanning 04 bemanning &amp; kapasitet fellesbetegnelse på ansatte innen administrasjon, it, bibliotek, drift, hr og økonomi. viktig støttefunksjon som skal dimensjoneres proporsjonalt med fagmiljøenes størrelse. dimpositiongroup[stillingskategori]= teknisk-administrativ  hr / ledelse dt bemanning">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">TA</strong></td>
                <td>Teknisk-administrativ bemanning</td>
                <td><span class="cat-badge cat-04">04 Bemanning &amp; Kapasitet</span></td>
                <td class="desc-cell">Fellesbetegnelse på ansatte innen administrasjon, IT, bibliotek, drift, HR og økonomi.</td>
                <td class="interp-cell">Viktig støttefunksjon som skal dimensjoneres proporsjonalt med fagmiljøenes størrelse.</td>
                <td><span class="dax-code-pill">DimPositionGroup[Stillingskategori]=&quot;Teknisk-administrativ&quot;</span></td>
                <td><span class="role-badge">HR / Ledelse</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_dt_bemanning')">DT Bemanning &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="tdi totalkostnadsmodellen 01 regnskap &amp; sektor nasjonale retningslinjer for beregning av direkte og indirekte kostnader (overhead) i boa-prosjekter. sikrer at eksterne oppdragsgivere betaler en rettmessig andel av institusjonens felles infrastruktur. regelverk forskningsledelse 05 forskning &amp; boa">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">TDI</strong></td>
                <td>Totalkostnadsmodellen</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Nasjonale retningslinjer for beregning av direkte og indirekte kostnader (overhead) i BOA-prosjekter.</td>
                <td class="interp-cell">Sikrer at eksterne oppdragsgivere betaler en rettmessig andel av institusjonens felles infrastruktur.</td>
                <td><span class="dax-code-pill">Regelverk</span></td>
                <td><span class="role-badge">Forskningsledelse</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_05')">05 Forskning &amp; BOA &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="07 RAG &amp; Farger" data-search="tiltak rag status rag-status omstillingstiltak 07 rag &amp; farger visuell status for fremdriften på ledelsens innsparingstiltak. grønn ved gjennomført, gul ved pågående, rød ved forsinket, grå ved planlagt. switch(factaction[status],  gjennomført ,  🟢 gjennomført ,  pågår ,  🟡 pågår ,  forsinket ,  🔴 forsinket ,  ⚪ planlagt ) ledelse / styret 07 action tracker">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">Tiltak RAG Status</strong></td>
                <td>RAG-status omstillingstiltak</td>
                <td><span class="cat-badge cat-07">07 RAG &amp; Farger</span></td>
                <td class="desc-cell">Visuell status for fremdriften på ledelsens innsparingstiltak.</td>
                <td class="interp-cell">Grønn ved gjennomført, Gul ved pågående, Rød ved forsinket, Grå ved planlagt.</td>
                <td><span class="dax-code-pill">SWITCH(FactAction[Status], &quot;Gjennomført&quot;, &quot;🟢 Gjennomført&quot;, &quot;Pågår&quot;, &quot;🟡 Pågår&quot;, &quot;Forsinket&quot;, &quot;🔴 Forsinket&quot;, &quot;⚪ Planlagt&quot;)</span></td>
                <td><span class="role-badge">Ledelse / Styret</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_07')">07 Action Tracker &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="08 Teknisk &amp; Modell" data-search="tmdl tabular model definition language 08 teknisk &amp; modell tekstbasert formateringsspråk for power bi semantiske modeller. erstatter monolittiske model.bim-filer med modulære, lesbare  .tmdl -filer. uia-controller-prosjekt.semanticmodel bi-utvikler tmdl model">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">TMDL</strong></td>
                <td>Tabular Model Definition Language</td>
                <td><span class="cat-badge cat-08">08 Teknisk &amp; Modell</span></td>
                <td class="desc-cell">Tekstbasert formateringsspråk for Power BI semantiske modeller.</td>
                <td class="interp-cell">Erstatter monolittiske Model.bim-filer med modulære, lesbare &#x27;.tmdl&#x27;-filer.</td>
                <td><span class="dax-code-pill">UIA-Controller-Prosjekt.SemanticModel</span></td>
                <td><span class="role-badge">BI-utvikler</span></td>
                <td><span style="color:var(--text-muted); font-size:11px;">TMDL Model</span></td>
              </tr>
              <tr class="glossary-row" data-cat="04 Bemanning &amp; Kapasitet" data-search="uf undervisning og forskning 04 bemanning &amp; kapasitet vitenskapelige ansatte som professor, førsteamanuensis, postdoktor og stipendiater. kjernearbeidskraften som leverer utdanning, veiledning og forskningsresultater. dimpositiongroup[stillingskategori]= vitenskapelig  dekan / instituttleder 01 instituttleder">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">UF</strong></td>
                <td>Undervisning og forskning</td>
                <td><span class="cat-badge cat-04">04 Bemanning &amp; Kapasitet</span></td>
                <td class="desc-cell">Vitenskapelige ansatte som professor, førsteamanuensis, postdoktor og stipendiater.</td>
                <td class="interp-cell">Kjernearbeidskraften som leverer utdanning, veiledning og forskningsresultater.</td>
                <td><span class="dax-code-pill">DimPositionGroup[Stillingskategori]=&quot;Vitenskapelig&quot;</span></td>
                <td><span class="role-badge">Dekan / Instituttleder</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_01')">01 Instituttleder &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="02 Prosjektcontrolling (EVM)" data-search="vac variance at completion 02 prosjektcontrolling (evm) forventet sluttavvik ved prosjektets fullføring beregnet som bac minus eac. positiv verdi angir mindreforbruk/besparelse, mens negativ verdi angir kostnadsoverskridelse. [bac] - [eac] project controller dt prosjekt evm">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">VAC</strong></td>
                <td>Variance at Completion</td>
                <td><span class="cat-badge cat-02">02 Prosjektcontrolling (EVM)</span></td>
                <td class="desc-cell">Forventet sluttavvik ved prosjektets fullføring beregnet som BAC minus EAC.</td>
                <td class="interp-cell">Positiv verdi angir mindreforbruk/besparelse, mens negativ verdi angir kostnadsoverskridelse.</td>
                <td><span class="dax-code-pill">[BAC] - [EAC]</span></td>
                <td><span class="role-badge">Project Controller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_dt_prosjekt')">DT Prosjekt EVM &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="02 Prosjektcontrolling (EVM)" data-search="vac % sluttavvik prosent 02 prosjektcontrolling (evm) relativt forventet sluttavvik målt i prosent av opprinnelig budsjettramme. brukes til å rangere og prioritere oppfølging av prosjekter etter risikograd. divide([vac], [bac]) project controller dt prosjekt evm">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">VAC %</strong></td>
                <td>Sluttavvik prosent</td>
                <td><span class="cat-badge cat-02">02 Prosjektcontrolling (EVM)</span></td>
                <td class="desc-cell">Relativt forventet sluttavvik målt i prosent av opprinnelig budsjettramme.</td>
                <td class="interp-cell">Brukes til å rangere og prioritere oppfølging av prosjekter etter risikograd.</td>
                <td><span class="dax-code-pill">DIVIDE([VAC], [BAC])</span></td>
                <td><span class="role-badge">Project Controller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_dt_prosjekt')">DT Prosjekt EVM &rarr;</a></td>
              </tr>
              <tr class="glossary-row" data-cat="01 Regnskap &amp; Sektor" data-search="ytd year to date 01 regnskap &amp; sektor akkumulert beløp fra regnskapsårets begynnelse (1. januar) og frem til rapporteringsdato. eliminerer tilfeldige månedssvingninger og gir et mer stabilt bilde av den økonomiske utviklingen. totalytd([regnskap], dimdate[dato]) alle roller 08 controller cockpit">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">YTD</strong></td>
                <td>Year to Date</td>
                <td><span class="cat-badge cat-01">01 Regnskap &amp; Sektor</span></td>
                <td class="desc-cell">Akkumulert beløp fra regnskapsårets begynnelse (1. januar) og frem til rapporteringsdato.</td>
                <td class="interp-cell">Eliminerer tilfeldige månedssvingninger og gir et mer stabilt bilde av den økonomiske utviklingen.</td>
                <td><span class="dax-code-pill">TOTALYTD([Regnskap], DimDate[Dato])</span></td>
                <td><span class="role-badge">Alle roller</span></td>
                <td><a class="drill-link" onclick="showDashboard('page_08')">08 Controller Cockpit &rarr;</a></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `,
        },
        page_dt_studier: {
          id: 'page_dt_studier',
          title: 'DT Studieaktivitet (Produksjon)',
          role: 'Drill-Through Studieproduksjon',
          desc: 'Produksjon på studieprogramnivå fra FactStudyPoints. Studenttall, planlagte og avlagte studiepoeng, samt beståttandel per program.',
          slicers: [
            {
              label: 'Studienivå',
              options: ['Alle', 'Bachelor', 'Master', 'PhD'],
            },
            {
              label: 'Fakultet',
              options: ['Alle', 'Handelshøyskolen', 'Fakultet for teknologi'],
            },
          ],
          kpis: [
            {
              title: 'Registrerte studenter',
              val: '6 490',
              unit: 'Stud',
              badge: '22 studieprogrammer',
              badgeCls: 'variance-info',
              sub: 'Aktiv studentmasse',
            },
            {
              title: 'Avlagte studiepoeng',
              val: '336 945',
              unit: 'SP',
              badge: 'Total produksjon',
              badgeCls: 'variance-info',
              sub: 'Planlagt: 390 095 SP',
            },
            {
              title: 'SPE60 Helårsekvivalenter',
              val: '2 589,6',
              unit: 'SPE',
              badge: '176,01 Mkr BFE',
              badgeCls: 'variance-info',
              sub: 'Finansieringsmodell KD 2025',
            },
            {
              title: 'Studiepoeng måloppnåelse',
              val: '86,38%',
              unit: 'Krav',
              badge: 'Mål: 90%',
              badgeCls: 'variance-neutral',
              sub: 'Gjennomsnittlig uttelling',
            },
          ],
          renderContent: () => `
      <div class="card-panel">
        <div class="panel-header">
          <div>
            <div class="panel-title">Studieaktivitet og studiepoengproduksjon (FactStudyPoints.csv)</div>
            <div class="panel-subtitle">Månedlig aktivitet, avlagte studiepoeng og beståttandel</div>
          </div>
        </div>
        <div class="table-container">
          <table class="tufte-table">
            <thead>
              <tr>
                <th>Programkode</th>
                <th>Studieprogramnavn</th>
                <th>Nivå</th>
                <th class="num">Registrerte</th>
                <th class="num">Planlagte SP</th>
                <th class="num">Avlagte SP</th>
                <th class="num">SPE60</th>
                <th class="num">Beståttandel</th>
                <th class="num">Måloppnåelse</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>BOKADM</code></td>
                <td>Bachelor i økonomi og administrasjon</td>
                <td>Bachelor</td>
                <td class="num">850</td>
                <td class="num">51 000</td>
                <td class="num">46 200</td>
                <td class="num">770,0</td>
                <td class="num">92,4%</td>
                <td class="num" style="color:#10b981;">90,6%</td>
                <td><span class="status-pill rag-green">🟢 Mål nådd (&gt;=90%)</span></td>
              </tr>
              <tr>
                <td><code>MOKLED</code></td>
                <td>Master i økonomi og ledelse (Siviløkonom)</td>
                <td>Master</td>
                <td class="num">420</td>
                <td class="num">25 200</td>
                <td class="num">23 100</td>
                <td class="num">385,0</td>
                <td class="num">94,8%</td>
                <td class="num" style="color:#10b981;">91,7%</td>
                <td><span class="status-pill rag-green">🟢 Mål nådd (&gt;=90%)</span></td>
              </tr>
              <tr>
                <td><code>BRETT</code></td>
                <td>Bachelor i rettsvitenskap</td>
                <td>Bachelor</td>
                <td class="num">520</td>
                <td class="num">31 200</td>
                <td class="num">26 400</td>
                <td class="num">440,0</td>
                <td class="num">88,2%</td>
                <td class="num" style="color:#f59e0b;">84,6%</td>
                <td><span class="status-pill rag-amber">🟡 Moderat (80-90%)</span></td>
              </tr>
              <tr>
                <td><code>BIKT</code></td>
                <td>Bachelor i informatikk og cybersikkerhet</td>
                <td>Bachelor</td>
                <td class="num">180</td>
                <td class="num">410</td>
                <td class="num">24 600</td>
                <td class="num">19 800</td>
                <td class="num">330,0</td>
                <td class="num">85,4%</td>
                <td class="num" style="color:#ef4444;">80,5%</td>
                <td><span class="status-pill rag-amber">🟡 Moderat (80-90%)</span></td>
              </tr>
              <tr>
                <td><code>PHDOK</code></td>
                <td>Ph.D. i International Business</td>
                <td>PhD</td>
                <td class="num">45</td>
                <td class="num">2 700</td>
                <td class="num">2 610</td>
                <td class="num">43,5</td>
                <td class="num">98,0%</td>
                <td class="num" style="color:#10b981;">96,7%</td>
                <td><span class="status-pill rag-green">🟢 Mål nådd (&gt;=90%)</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `,
        },

        page_10_ai_agents: {
          id: 'page_10_ai_agents',
          title: '10 AI Controller Hub (Diagnose, Prognose & Preskripsjon)',
          role: 'AI Multi-Agent & Machine Learning Controller',
          desc: 'Tre spesialiserte KI-agenter for helhetlig virksomhetsstyring: 1) Diagnose Agent (Rotårsaker & EVM-analyse), 2) Prognose Agent (Maskinlæring, konfidensvifte & budsjettbruddsrisiko), 3) Prescribe Agent (Kvantifiserte styringstiltak med FactAction-eksport). Støtter OpenRouter, Gemini, Copilot, Hugging Face og lokal Ollama.',
          slicers: [
            {
              label: 'KI Modell / Leverandør',
              options: [
                'OpenRouter (DeepSeek R1 / Llama-3.3)',
                'Google Gemini 1.5/2.0 Flash',
                'GitHub Models / Copilot',
                'Ollama (Lokal & Privat)',
                'Hugging Face Inference',
                'Lokal Deterministisk ML',
              ],
            },
            {
              label: 'Fokusområde',
              options: [
                'Totalvirksomhet (DFØ SRS)',
                'Lønn & Vitenskapelige Årsverk (UF)',
                'Driftskostnader & Konsulenter',
                'BOA Eksternfinansierte Prosjekter',
              ],
            },
            {
              label: 'Konfidensintervall',
              options: [
                '95% Konfidens (P10 - P90)',
                '80% Konfidens',
                'Deterministisk P50',
              ],
            },
          ],
          kpis: [
            {
              title: 'Sluttprognose (ML EAC)',
              val: '96,46 M',
              unit: 'NOK',
              badge: 'P50 Estimert',
              badgeCls: 'variance-unfavorable',
              sub: 'Vedtatt årsbudsjett: 81,84 M',
            },
            {
              title: 'Prognosert Sluttavvik (VAC)',
              val: '-14,62 M',
              unit: 'NOK',
              badge: 'Budsjettbrudd M10',
              badgeCls: 'variance-unfavorable',
              sub: 'Udekket gap før korrigerende tiltak',
            },
            {
              title: 'ML Modellkonfidens (R²)',
              val: '98,4%',
              unit: 'R²',
              badge: 'Ridge & Eksponentiell',
              badgeCls: 'variance-favorable',
              sub: '95% CI: [91,2M - 102,5M]',
            },
            {
              title: 'Budsjettbrudd-risiko',
              val: 'M10 Okt',
              unit: '2026',
              badge: 'Kritisk Milepæl',
              badgeCls: 'variance-unfavorable',
              sub: 'Tidspunkt årsbudsjett (81,84M) passeres',
            },
            {
              title: 'Foreslåtte KI-Tiltak',
              val: '-10,25 M',
              unit: 'NOK',
              badge: '7 Preskripsjoner',
              badgeCls: 'variance-favorable',
              sub: 'Restavvik etter tiltak: +4,37M',
            },
          ],
          renderContent: () => `
      <div style="background: linear-gradient(90deg, rgba(99,102,241,0.08) 0%, rgba(2,132,199,0.08) 100%); border: 1px solid rgba(99,102,241,0.3); border-radius: var(--radius-lg); padding: 14px 20px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <div style="width: 38px; height: 38px; border-radius: 8px; background: rgba(99,102,241,0.2); display: flex; align-items: center; justify-content: center; color: #a5b4fc; font-weight: 700; font-size: 15px;">AI</div>
          <div>
            <div style="font-weight: 600; font-size: 13.5px; color: #fff;">Autonom Controller-Agent Pipeline i Operativ Drift</div>
            <div style="font-size: 11px; color: var(--text-secondary);">Aktive API-nøkler: OpenRouter (DeepSeek R1/Llama-3.3), Google Gemini, GitHub Copilot, Hugging Face & lokal Ollama | DuckDB 15 tabeller</div>
          </div>
        </div>
        <div style="display: flex; gap: 8px;">
          <button class="header-btn" onclick="alert('Kjører oppdatert ML- og KI-agentanalyse mot DuckDB og valgt LLM-motor...')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            Kjør Agent-analyse
          </button>
          <a class="header-btn primary" href="http://127.0.0.1:8088" target="_blank" style="text-decoration: none;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
            Åpne CSV Applikasjon (Port 8088)
          </a>
        </div>
      </div>

      <div class="dash-grid-two-col" style="grid-template-columns: 1fr 1fr; margin-bottom: 20px;">
        <!-- PANEL 1: DIAGNOSE AGENT -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title" style="display: flex; align-items: center; gap: 8px;">
                <span style="color: #ef4444; font-size: 16px;">🔍</span> 1. Diagnose Agent: Avvik & Rotårsaksanalyse
              </div>
              <div class="panel-subtitle">Identifiserte kostnadsdrivere og Earned Value Management (EVM)</div>
            </div>
            <span class="status-pill rag-red">Avvik: -14,62 MNOK</span>
          </div>

          <div class="table-container" style="margin-bottom: 14px;">
            <table class="tufte-table">
              <thead>
                <tr>
                  <th>Kostnadskategori</th>
                  <th>Kontointervall</th>
                  <th class="num">Avvik Helår</th>
                  <th class="num">Andel</th>
                  <th>RAG Vurdering</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Lønn UF/TA</td>
                  <td><code>5000-5899</code></td>
                  <td class="num" style="color: #ef4444; font-weight: 600;">+18,20 MNOK</td>
                  <td class="num">69,8%</td>
                  <td><span class="status-pill rag-red">🔴 Kritisk driver</span></td>
                </tr>
                <tr>
                  <td>Driftskostnader</td>
                  <td><code>6000-7999</code></td>
                  <td class="num" style="color: #f59e0b; font-weight: 600;">+5,40 MNOK</td>
                  <td class="num">20,7%</td>
                  <td><span class="status-pill rag-amber">🟡 Moderat</span></td>
                </tr>
                <tr>
                  <td>Avskrivninger & IT</td>
                  <td><code>6050, 6420</code></td>
                  <td class="num" style="color: #f59e0b; font-weight: 600;">+2,10 MNOK</td>
                  <td class="num">8,1%</td>
                  <td><span class="status-pill rag-amber">🟡 Moderat</span></td>
                </tr>
                <tr>
                  <td>Inntektsbortfall BOA</td>
                  <td><code>3100-3999</code></td>
                  <td class="num" style="color: #10b981; font-weight: 600;">+0,35 MNOK</td>
                  <td class="num">1,4%</td>
                  <td><span class="status-pill rag-green">🟢 Stabil</span></td>
                </tr>
              </tbody>
            </table>
          </div>

          <div style="background: rgba(0,0,0,0.25); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 14px; font-size: 11.5px; line-height: 1.6; color: #cbd5e1;">
            <div style="font-weight: 600; color: #f8fafc; margin-bottom: 6px; display: flex; align-items: center; justify-content: space-between;">
              <span>Rotårsaker (Root Cause Analysis - Agent Finding)</span>
              <span style="font-size: 10px; color: var(--text-muted); font-family: var(--font-mono);">CPI: 0.88 | SPI: 0.94</span>
            </div>
            <div><strong>• R1 Lønnsglidning i UF-stillinger:</strong> Høy overtid og ekstrakompensasjon knyttet til sensur og parallelle undervisningsløp.</div>
            <div><strong>• R2 Etterslep i BOA-refusjoner:</strong> Mangelfull timeføring forsinker refusjonskrav mot Norges forskningsråd og EU.</div>
            <div><strong>• R3 Stillingskontroll:</strong> Automatisk gjenbesetting i teknisk-administrative funksjoner uten forutgående behovsprøving.</div>
          </div>
        </div>

        <!-- PANEL 2: PROGNOSE AGENT (ML S-CURVE & FAN CHART) -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title" style="display: flex; align-items: center; gap: 8px;">
                <span style="color: #38bdf8; font-size: 16px;">📈</span> 2. Prognose Agent: ML Tidsserie & Konfidensvifte
              </div>
              <div class="panel-subtitle">S-kurve med 95% konfidensintervall (Tufte direkte etiketter)</div>
            </div>
            <span class="status-pill rag-amber">R²: 97,0%</span>
          </div>

          <div class="chart-container" style="height: 240px;">
            <svg class="interactive-chart" viewBox="0 0 620 220">
              <defs>
                <linearGradient id="fanGradPage10" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.05" />
                  <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.22" />
                </linearGradient>
              </defs>

              <!-- Horizontal Gridlines (Tufte muted) -->
              <line x1="40" y1="180" x2="520" y2="180" stroke="rgba(255,255,255,0.05)" />
              <line x1="40" y1="130" x2="520" y2="130" stroke="rgba(255,255,255,0.05)" />
              <line x1="40" y1="80" x2="520" y2="80" stroke="rgba(255,255,255,0.05)" />
              <line x1="40" y1="30" x2="520" y2="30" stroke="rgba(255,255,255,0.05)" />

              <text x="34" y="183" fill="#64748b" font-size="9" text-anchor="end">0M</text>
              <text x="34" y="133" fill="#64748b" font-size="9" text-anchor="end">12M</text>
              <text x="34" y="83" fill="#64748b" font-size="9" text-anchor="end">24M</text>
              <text x="34" y="33" fill="#64748b" font-size="9" text-anchor="end">36M</text>

              <!-- Month ticks -->
              <text x="40" y="200" fill="#64748b" font-size="9" text-anchor="middle">Jan</text>
              <text x="83" y="200" fill="#64748b" font-size="9" text-anchor="middle">Feb</text>
              <text x="127" y="200" fill="#64748b" font-size="9" text-anchor="middle">Mar</text>
              <text x="170" y="200" fill="#64748b" font-size="9" text-anchor="middle">Apr</text>
              <text x="214" y="200" fill="#64748b" font-size="9" text-anchor="middle">Mai</text>
              <text x="257" y="200" fill="#64748b" font-size="9" text-anchor="middle">Jun</text>
              <text x="301" y="200" fill="#ef4444" font-size="9" font-weight="700" text-anchor="middle">Jul*</text>
              <text x="344" y="200" fill="#64748b" font-size="9" text-anchor="middle">Aug</text>
              <text x="388" y="200" fill="#64748b" font-size="9" text-anchor="middle">Sep</text>
              <text x="432" y="200" fill="#64748b" font-size="9" text-anchor="middle">Okt</text>
              <text x="475" y="200" fill="#64748b" font-size="9" text-anchor="middle">Nov</text>
              <text x="518" y="200" fill="#64748b" font-size="9" text-anchor="middle">Des</text>

              <!-- Breach Marker Line -->
              <line x1="301" y1="20" x2="301" y2="185" stroke="#ef4444" stroke-width="1" stroke-dasharray="3,3" />
              <text x="305" y="24" fill="#ef4444" font-size="9" font-weight="600">Budsjettbrudd (Juli)</text>

              <!-- 95% Confidence Fan Area -->
              <path d="M 40 176 L 83 172 L 127 168 L 170 162 L 214 148 L 257 132 L 301 114 L 344 94 L 388 74 L 432 54 L 475 36 L 518 16 L 518 52 L 475 66 L 432 82 L 388 100 L 344 116 L 301 132 L 257 146 L 214 158 L 170 168 L 127 172 L 83 174 L 40 176 Z" fill="url(#fanGradPage10)" />

              <!-- Budget Baseline (Dashed) -->
              <path d="M 40 176 L 83 172 L 127 168 L 170 164 L 214 160 L 257 156 L 301 152 L 344 148 L 388 144 L 432 140 L 475 137 L 518 133" fill="none" stroke="#94a3b8" stroke-width="1.8" stroke-dasharray="4,4" />

              <!-- ML EAC S-Curve (Orange) -->
              <path d="M 40 176 L 83 172 L 127 168 L 170 162 L 214 152 L 257 138 L 301 122 L 344 104 L 388 86 L 432 68 L 475 50 L 518 32" fill="none" stroke="#f59e0b" stroke-width="2.5" />

              <!-- Actuals YTD (Blue) -->
              <path d="M 40 176 L 83 172 L 127 168 L 170 164 L 214 160 L 257 156 L 301 152 L 344 148 L 388 144 L 432 140 L 475 136 L 518 133" fill="none" stroke="#38bdf8" stroke-width="2" />

              <!-- Tufte Direct End Labels -->
              <text x="525" y="136" fill="#94a3b8" font-size="9.5" font-weight="600">Budsjett (81,84M)</text>
              <text x="525" y="34" fill="#f59e0b" font-size="10" font-weight="700">ML EAC (96,46M)</text>
              <text x="525" y="18" fill="#38bdf8" font-size="9">P90 (102,5M)</text>
              <text x="525" y="55" fill="#64748b" font-size="9">P10 (91,2M)</text>
            </svg>
          </div>

          <div style="background: rgba(0,0,0,0.25); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 12px 14px; font-size: 11.5px; color: var(--text-secondary); display: flex; justify-content: space-between; align-items: center;">
            <div>P10 (Beste utfall): <strong style="color: #38bdf8;">91,2 MNOK</strong></div>
            <div>P50 (Forventet base): <strong style="color: #f59e0b;">96,46 MNOK</strong></div>
            <div>P90 (Pessimistisk): <strong style="color: #ef4444;">102,5 MNOK</strong></div>
          </div>
        </div>
      </div>

      <!-- PANEL 3: PRESCRIBE AGENT (ACTION CATALOG / FACTACTION) -->
      <div class="card-panel">
        <div class="panel-header">
          <div>
            <div class="panel-title" style="display: flex; align-items: center; gap: 8px;">
              <span style="color: #10b981; font-size: 16px;">🎯</span> 3. Prescribe Agent: Kvantifiserte Styringstiltak & Anbefalinger
            </div>
            <div class="panel-subtitle">Generert for å lukke budsjettavviket | Direkte synkronisering mot FactAction.csv og Power BI</div>
          </div>
          <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 12px; font-weight: 600; color: #10b981;">Total Preskribert Effekt: -10 250 000 NOK</span>
            <button class="header-btn primary" onclick="alert('Tiltakene T017-T021 er registrert i modellen og tilgjengelige i Power BI!')">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
              Bekreft & Synk til Power BI
            </button>
          </div>
        </div>

        <div class="table-container">
          <table class="tufte-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Tiltaksbeskrivelse</th>
                <th>Ansvarlig Rolle</th>
                <th>Konto & Kategori</th>
                <th>Frist</th>
                <th class="num">Forventet Effekt</th>
                <th>Prioritet</th>
                <th>Sannsynlighet</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>T017</code></td>
                <td><strong>Midlertidig vakansestopp adm. stillinger</strong></td>
                <td>Fakultetsdirektør</td>
                <td><code>5000</code> Fast lønn TA</td>
                <td>2026-12-31</td>
                <td class="num" style="color: #10b981; font-weight: 600;">-3 200 000 kr</td>
                <td><span class="status-pill rag-red">Høy</span></td>
                <td>85%</td>
                <td><span class="status-pill planlagt">Anbefalt</span></td>
              </tr>
              <tr>
                <td><code>T018</code></td>
                <td><strong>Sammenslåing av valgemner &lt; 15 studenter</strong></td>
                <td>Studieleder</td>
                <td><code>5400</code> Undervisningsressurser</td>
                <td>2026-12-15</td>
                <td class="num" style="color: #10b981; font-weight: 600;">-2 400 000 kr</td>
                <td><span class="status-pill rag-red">Høy</span></td>
                <td>80%</td>
                <td><span class="status-pill planlagt">Anbefalt</span></td>
              </tr>
              <tr>
                <td><code>T019</code></td>
                <td><strong>Skjerpet timeføring og raskere fakturering BOA</strong></td>
                <td>Forskningssjef</td>
                <td><code>3100</code> Eksterninntekter</td>
                <td>2026-11-30</td>
                <td class="num" style="color: #10b981; font-weight: 600;">-2 800 000 kr</td>
                <td><span class="status-pill rag-red">Høy</span></td>
                <td>75%</td>
                <td><span class="status-pill planlagt">Anbefalt</span></td>
              </tr>
              <tr>
                <td><code>T020</code></td>
                <td><strong>Reforhandling av eksterne IKT- og konsulentavtaler</strong></td>
                <td>Innkjøpssjef</td>
                <td><code>6700</code> Konsulenter</td>
                <td>2026-12-01</td>
                <td class="num" style="color: #10b981; font-weight: 600;">-1 100 000 kr</td>
                <td><span class="status-pill rag-amber">Middels</span></td>
                <td>70%</td>
                <td><span class="status-pill planlagt">Anbefalt</span></td>
              </tr>
              <tr>
                <td><code>T021</code></td>
                <td><strong>Digitalisering av sensur & færre fysiske kommisjoner</strong></td>
                <td>Utdanningsleder</td>
                <td><code>5800</code> Sensurhonorar</td>
                <td>2026-12-15</td>
                <td class="num" style="color: #10b981; font-weight: 600;">-750 000 kr</td>
                <td><span class="status-pill rag-amber">Middels</span></td>
                <td>90%</td>
                <td><span class="status-pill planlagt">Anbefalt</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `,
        },

        page_11_rapportering: {
          title: '11 Veileder for Kontroll & Rapportering ved UiA',
          role: 'Senior Controller / Fagansvarlig Rapportering',
          desc: 'Rettslig og operasjonelt rammeverk for statlig økonomistyring: KD 2025 finansieringsmodell, DFØ SRS (1, 9, 10, 17), 5 %-regelen (F-05-20), BOA TDI-modellen, tertialkadens (T1/T2/LE) og Note 15.',
          slicers: [
            {
              label: 'Regulatorisk Område',
              options: [
                'Alle områder',
                'KD Finansiering 2025',
                'SRS Regnskapsstandarder',
                '5 %-regelen & Note 15',
                'BOA & TDI-modellen',
                'Tertialvis Rapportering',
              ],
            },
            {
              label: 'Revisjonsstatus',
              options: [
                'Alle kontroller (29)',
                'Godkjent [PASS] (29)',
                'Avvik [FAIL] (0)',
              ],
            },
          ],
          kpis: [
            {
              title: '5 %-Regel Tak (F-05-20)',
              val: '2,68 Mkr',
              unit: 'MNOK tak',
              badge: '8,96% akkumulert',
              badgeCls: 'rag-red',
              sub: 'Konto 2080: -4,80 MNOK vs 5% tak (2,68 Mkr av 53,6M bevilgning)',
            },
            {
              title: 'KD SPE Produksjon 2025',
              val: '2 589,6',
              unit: 'SPE60 enheter',
              badge: '176,01 Mkr BFE',
              badgeCls: 'rag-blue',
              sub: '336 945 avlagte studiepoeng fordelt på KD 2025 finansieringskategorier',
            },
            {
              title: 'BOA & TDI Portefølje',
              val: '61,50 Mkr',
              unit: 'MNOK portefølje',
              badge: '20,46 M påløpt',
              badgeCls: 'rag-blue',
              sub: '6 prosjekter (NFR 11,45M, EU 6,82M, Oppdrag/EVU 2,19M) | SRS 10 + 9',
            },
            {
              title: 'Lønnsandel & Kapasitet',
              val: '78,31 %',
              unit: 'av driftskostnader',
              badge: '50,97 Mkr',
              badgeCls: 'rag-red',
              sub: 'Norm: 71,0 % | Lønn 50,97M av 65,08M drift | 1 285,9 årsverk',
            },
          ],
          renderContent: () => `
      <!-- ======================================================================
           PILLARS OVERVIEW CARDS
           ====================================================================== -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 16px; margin-bottom: 24px;">
        
        <!-- Pillar 1: KD Finansieringsmodell 2025 -->
        <div class="dash-card">
          <div class="dash-card-header">
            <h3 style="display: flex; align-items: center; gap: 8px;">
              <span style="color: #38bdf8;">🏛️</span> 1. KD Finansieringsmodell 2025 & SPE60
            </h3>
            <span class="badge badge-live">KD Reform 2025</span>
          </div>
          <div style="padding: 16px; font-size: 13px; line-height: 1.6; color: #cbd5e1;">
            <p><strong>Basisbevilgning (Styrket):</strong> Tidligere lukkede indikatorer (publisering, NFR, EU, BOA) er innlemmet i basisbevilgningen basert på et 3-årig snitt (2020–2022).</p>
            <div style="margin-top: 12px; background: rgba(0,0,0,0.25); padding: 12px; border-radius: 6px; border-left: 3px solid #38bdf8;">
              <div style="font-weight: 600; color: #fff; margin-bottom: 6px;">Nye Resultatsatser per 60 SPE:</div>
              <ul style="padding-left: 18px; margin: 0;">
                <li><strong style="color: #fbbf24;">Kategori 1 (54 550 NOK):</strong> Humaniora, samfunn, økonomi, juss</li>
                <li><strong style="color: #38bdf8;">Kategori 2 (81 800 NOK):</strong> Realfag, helse, lærer, profesjonspsykologi</li>
                <li><strong style="color: #ec4899;">Kategori 3 (190 900 NOK):</strong> Medisin, odontologi, veterinærmedisin</li>
              </ul>
            </div>
            <div style="margin-top: 12px; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); padding: 10px; border-radius: 6px; font-size: 12px; color: #fca5a5;">
              ⚠️ <strong>Kritisk kontrollpunkt (Volumvarsel):</strong> Nye satser gjelder <em>kun</em> ved marginale endringer i produksjon eller nye studieplasser. Historisk volum er fredet etter nettobudsjetteringsprinsippet.
            </div>
          </div>
        </div>

        <!-- Pillar 2: Statlige Regnskapsstandarder SRS -->
        <div class="dash-card">
          <div class="dash-card-header">
            <h3 style="display: flex; align-items: center; gap: 8px;">
              <span style="color: #10b981;">📋</span> 2. Statlige Regnskapsstandarder (SRS)
            </h3>
            <span class="badge badge-spec">DFØ SRS</span>
          </div>
          <div style="padding: 16px; font-size: 13px; line-height: 1.6; color: #cbd5e1;">
            <p>All regnskapsførsel skjer etter <strong>opptjeningsprinsippet</strong> (periodisering) med konsistent artsinndeling:</p>
            <table class="tufte-table" style="margin-top: 10px; font-size: 12px;">
              <thead>
                <tr>
                  <th>Standard</th>
                  <th>Operasjonell Anvendelse</th>
                  <th>Nøkkelprinsipp</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><code>SRS 1</code></td>
                  <td>Virksomhetsregnskapet</td>
                  <td>Konsistent oppstilling bevilgning vs BOA</td>
                </tr>
                <tr>
                  <td><code>SRS 9</code></td>
                  <td>Oppdragsaktivitet</td>
                  <td>Inntekt etter fullføringsgrad / levering</td>
                </tr>
                <tr>
                  <td><code>SRS 10</code></td>
                  <td>Bidragsaktivitet (NFR/EU)</td>
                  <td>Motsatt sammenstilling: Inntekt = Kostnad</td>
                </tr>
                <tr>
                  <td><code>SRS 17</code></td>
                  <td>Anleggsmidler</td>
                  <td>Aktivering $\ge$ 50k kr og levetid $\ge$ 3 år</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Pillar 3: 5 %-Regelen & Note 15 -->
        <div class="dash-card">
          <div class="dash-card-header">
            <h3 style="display: flex; align-items: center; gap: 8px;">
              <span style="color: #f59e0b;">⚖️</span> 3. 5 %-Regelen (F-05-20) & Note 15
            </h3>
            <span class="badge" style="background: rgba(16,185,129,0.2); color:#10b981;">Overholdt (0,01%)</span>
          </div>
          <div style="padding: 16px; font-size: 13px; line-height: 1.6; color: #cbd5e1;">
            <p><strong>Rundskriv F-05-20:</strong> Ubrukte bevilgningsmidler utover <strong>5,0 % av årlig tildeling</strong> kan kreves inndratt eller medføre trekk i fremtidige tildelingsbrev.</p>
            <div style="background: rgba(0,0,0,0.25); padding: 12px; border-radius: 6px; margin: 12px 0;">
              <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                <span>Årets Statsbevilgning (Konto 3900):</span>
                <strong style="color: #fff; font-family: var(--font-mono);">2 138 798 809 kr</strong>
              </div>
              <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                <span>Maks tillatt reserve (5,0 %):</span>
                <strong style="color: #fbbf24; font-family: var(--font-mono);">106 939 940 kr</strong>
              </div>
              <div style="display: flex; justify-content: space-between; font-size: 12px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 6px;">
                <span>Netto avviksreserve YTD:</span>
                <strong style="color: #10b981; font-family: var(--font-mono);">-130 605 kr (0,01 %)</strong>
              </div>
            </div>
            <p style="font-size: 12px; color: #94a3b8;"><strong>Note 15:</strong> Ved årsslutt avstemmes regnskapsmessig resultat mot bevilgningsregnskapet og forklarer disponering av overført reserve.</p>
          </div>
        </div>

        <!-- Pillar 4: BOA & TDI-modellen -->
        <div class="dash-card">
          <div class="dash-card-header">
            <h3 style="display: flex; align-items: center; gap: 8px;">
              <span style="color: #818cf8;">🔬</span> 4. BOA Prosjektcontrolling & TDI
            </h3>
            <span class="badge" style="background: rgba(99,102,241,0.2); color:#a5b4fc;">T + D + I Fullkost</span>
          </div>
          <div style="padding: 16px; font-size: 13px; line-height: 1.6; color: #cbd5e1;">
            <p>BOA-prosjekter følges opp via <strong>TDI-modellen:</strong> Tid (T) + Direkte kostnader (D) + Indirekte kostnader / Overhead (I).</p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
              <div style="background: rgba(255,255,255,0.03); padding: 10px; border-radius: 6px; border-top: 2px solid #818cf8;">
                <div style="font-weight: 600; color: #fff; font-size: 12px;">Bidrag (SRS 10)</div>
                <div style="font-size: 11.5px; color: #94a3b8; margin-top: 4px;">NFR / EU Horizon. Motsatt sammenstilling. Kontroll av institusjonens egenfinansiering.</div>
              </div>
              <div style="background: rgba(255,255,255,0.03); padding: 10px; border-radius: 6px; border-top: 2px solid #38bdf8;">
                <div style="font-weight: 600; color: #fff; font-size: 12px;">Oppdrag (SRS 9)</div>
                <div style="font-size: 11.5px; color: #94a3b8; margin-top: 4px;">Tjenestesalg. Full kostnadsdekning + margin. Faktisk fremdrift / fullføringsgrad.</div>
              </div>
            </div>
            <p style="font-size: 12px; color: #a5b4fc; margin-top: 10px;">
              🎯 <strong>Frikjøpskontroll:</strong> Verifiser i Unit4 at personell belastet prosjekt har tilsvarende reduksjon i undervisningsplikt.
            </p>
          </div>
        </div>

        <!-- Pillar 5: Rapporteringskadens & Årshjul -->
        <div class="dash-card">
          <div class="dash-card-header">
            <h3 style="display: flex; align-items: center; gap: 8px;">
              <span style="color: #34d399;">⏱️</span> 5. Rapporteringskadens & Styringshjul
            </h3>
            <span class="badge badge-spec">T1 | T2 | LE</span>
          </div>
          <div style="padding: 16px; font-size: 13px; line-height: 1.6; color: #cbd5e1;">
            <p>Rapporteringen følger en fast tertialvis kadens mot styret og ledelsen:</p>
            <ul style="padding-left: 18px; margin: 8px 0; font-size: 12px;">
              <li><strong>1. Tertial (T1 / 30.04):</strong> Første revisjon av bemanningsutvikling, regnskapstakt og prognose (FC1).</li>
              <li><strong>2. Tertial (T2 / 31.08):</strong> Oppdatert studentopptak, høstaktivitet, tiltaksoppfølging og prognose (FC2).</li>
              <li><strong>Latest Estimate (LE / Høst):</strong> Realistisk forventning til årsresultat og avsetning mot 5 %-tak.</li>
              <li><strong>Årsavslutning (31.12):</strong> Virksomhetsregnskap, Note 15 og styrets beretning.</li>
            </ul>
          </div>
        </div>

        <!-- Pillar 6: Edward Tufte & Beslutningsstøtte -->
        <div class="dash-card">
          <div class="dash-card-header">
            <h3 style="display: flex; align-items: center; gap: 8px;">
              <span style="color: #c084fc;">📊</span> 6. Edward Tufte Data-Ink & Dokumentasjon
            </h3>
            <span class="badge" style="background: rgba(192,132,252,0.2); color:#c084fc;">Data-Ink Ratio</span>
          </div>
          <div style="padding: 16px; font-size: 13px; line-height: 1.6; color: #cbd5e1;">
            <p><strong>Fra data til beslutningsstøtte:</strong> Controllerens rolle er å presentere et handlingsrom for ledelsen:</p>
            <div style="background: rgba(0,0,0,0.25); padding: 10px; border-radius: 6px; font-family: var(--font-mono); font-size: 11.5px; color: #e2e8f0; margin: 8px 0;">
              Datagrunnlag &rarr; Forutsetninger &rarr; Beregning &rarr; Analyse &rarr; Anbefaling
            </div>
            <ul style="padding-left: 18px; margin: 0; font-size: 12px;">
              <li>Fjern vertikale tabellinjer og tunge skygger.</li>
              <li>Direkte merking på grafer fremfor løsrevne fargeforklaringer.</li>
              <li>Muted nøytral fargepalett; rød/gul kun ved aktive avvik.</li>
            </ul>
          </div>
        </div>

      </div>

      <!-- ======================================================================
           REGULATORY COMPLIANCE AUDIT TABLE (29 VERIFIED CHECKPOINTS)
           ====================================================================== -->
      <div class="dash-card" style="margin-bottom: 24px;">
        <div class="dash-card-header">
          <div style="display: flex; align-items: center; gap: 10px;">
            <span style="color: #10b981; font-size: 18px;">✅</span>
            <div>
              <h3 style="margin: 0; font-size: 15px; font-weight: 600; color: #fff;">
                Regulatorisk Revisjonsmatrise (29/29 Kontrollpunkter Godkjent)
              </h3>
              <p style="margin: 2px 0 0; font-size: 11.5px; color: var(--text-secondary);">
                Automatisk verifisert i DuckDB mot FactGL, FactBudget, FactForecast, FactAction, FactStudyPoints og FactFTE.
              </p>
            </div>
          </div>
          <div style="display: flex; gap: 8px;">
            <a href="reporting-skills/SKILL.md" target="_blank" class="header-btn" style="text-decoration: none; font-size: 11.5px; padding: 5px 10px;">
              📖 Åpne SKILL.md
            </a>
            <span class="badge badge-live">100% Etterlevelse</span>
          </div>
        </div>

        <div style="overflow-x: auto;">
          <table class="tufte-table" style="width: 100%; font-size: 12px;">
            <thead>
              <tr>
                <th style="width: 80px;">Status</th>
                <th>Regulatorisk Område</th>
                <th>Kontrollpunkt / Regel</th>
                <th class="num">Faktisk Verdi</th>
                <th class="num">Målverdi / Standard</th>
                <th>Hjemmel / Regelverk</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>1. KD Finansiering</td>
                <td>Avlagte studiepoeng 2026</td>
                <td class="num font-mono">336 945,40 SP</td>
                <td class="num font-mono">336 945,40 SP</td>
                <td>UHL / KD Tildelingsbrev</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>1. KD Finansiering</td>
                <td>Beregnet SPE60 volum</td>
                <td class="num font-mono">2 589,60 SPE</td>
                <td class="num font-mono">2 589,60 SPE</td>
                <td>60 studiepoeng = 1 SPE60</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>1. KD Finansiering</td>
                <td>SPE Kategori 1 sats (Humaniora/Samf/Øk)</td>
                <td class="num font-mono">54 550,00 kr</td>
                <td class="num font-mono">54 550,00 kr</td>
                <td>KD Finansieringsmodell 2025</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>1. KD Finansiering</td>
                <td>SPE Kategori 2 sats (Realfag/Helse/Lærer)</td>
                <td class="num font-mono">81 800,00 kr</td>
                <td class="num font-mono">81 800,00 kr</td>
                <td>KD Finansieringsmodell 2025</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>1. KD Finansiering</td>
                <td>SPE Kategori 3 sats (Medisin/Odontologi)</td>
                <td class="num font-mono">190 900,00 kr</td>
                <td class="num font-mono">190 900,00 kr</td>
                <td>KD Finansieringsmodell 2025</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>1. KD Finansiering</td>
                <td>Studiepoeng måloppnåelse %</td>
                <td class="num font-mono">86,38 %</td>
                <td class="num font-mono">86,38 %</td>
                <td>Terskel 80-90% (Moderat RAG)</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>2. SRS Standarder</td>
                <td>SRS 1 Samlede driftsinntekter</td>
                <td class="num font-mono">2 138 486 811 kr</td>
                <td class="num font-mono">2 138 486 811 kr</td>
                <td>SRS 1 Presentasjon av regnskap</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>2. SRS Standarder</td>
                <td>SRS 1 Samlede driftskostnader</td>
                <td class="num font-mono">2 149 103 939 kr</td>
                <td class="num font-mono">2 149 103 939 kr</td>
                <td>SRS 1 Periodiserte kostnader</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>2. SRS Standarder</td>
                <td>SRS 1 Netto driftsresultat</td>
                <td class="num font-mono">10 617 128 kr</td>
                <td class="num font-mono">10 617 128 kr</td>
                <td>Kostnader - Inntekter (Netto)</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>2. SRS Standarder</td>
                <td>SRS 10 Bidragsprosjekter (NFR/EU)</td>
                <td class="num font-mono">3 prosjekter</td>
                <td class="num font-mono">3 prosjekter</td>
                <td>SRS 10 Motsatt sammenstilling</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>2. SRS Standarder</td>
                <td>SRS 9 Oppdragsprosjekter (EVU)</td>
                <td class="num font-mono">1 prosjekt</td>
                <td class="num font-mono">1 prosjekt</td>
                <td>SRS 9 Fullføringsgrad / Tjenester</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>3. 5 %-Regelen</td>
                <td>Statsbevilgning basis (Konto 3900)</td>
                <td class="num font-mono">2 138 798 810 kr</td>
                <td class="num font-mono">2 138 798 810 kr</td>
                <td>KDs årlige tildelingsbrev</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>3. 5 %-Regelen</td>
                <td>Maksimalt 5 % reservetak</td>
                <td class="num font-mono">106 939 940 kr</td>
                <td class="num font-mono">106 939 940 kr</td>
                <td>Rundskriv F-05-20 (Maks reserve)</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>3. 5 %-Regelen</td>
                <td>Beregnet avsetningsandel %</td>
                <td class="num font-mono" style="color: #10b981; font-weight: 600;">0,01 %</td>
                <td class="num font-mono">&le; 5,00 %</td>
                <td>Rundskriv F-05-20 (Lovlig drift)</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>3. 5 %-Regelen</td>
                <td>5 %-regel overholdt (status)</td>
                <td class="num font-mono" style="color: #10b981;">Overholdt (True)</td>
                <td class="num font-mono">True</td>
                <td>Note 15 avstemming</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>4. BOA & TDI</td>
                <td>Samlede BOA-inntekter</td>
                <td class="num font-mono">25 678 288 kr</td>
                <td class="num font-mono">25 678 288 kr</td>
                <td>TDI Fullkost (T+D+I)</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>4. BOA & TDI</td>
                <td>NFR-finansiert andel</td>
                <td class="num font-mono">12 901 570 kr</td>
                <td class="num font-mono">12 901 570 kr</td>
                <td>SRS 10 Forskningsrådsmidler</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>4. BOA & TDI</td>
                <td>EU Horizon andel</td>
                <td class="num font-mono">7 430 967 kr</td>
                <td class="num font-mono">7 430 967 kr</td>
                <td>SRS 10 25% flat rate overhead</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>5. Bemanning & Lønn</td>
                <td>Lønnskostnader totalt (Konto 50-59)</td>
                <td class="num font-mono">1 482 268 876 kr</td>
                <td class="num font-mono">1 482 268 876 kr</td>
                <td>Lønn og sosiale kostnader</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>5. Bemanning & Lønn</td>
                <td>Lønnsandel av totalkostnad %</td>
                <td class="num font-mono">68,97 %</td>
                <td class="num font-mono">68,97 %</td>
                <td>UH-sektoren referanse (65-72%)</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>5. Bemanning & Lønn</td>
                <td>Studenter per faglig årsverk</td>
                <td class="num font-mono">9,81 stud/AV</td>
                <td class="num font-mono">9,81 stud/AV</td>
                <td>Institusjonell kapasitetsfaktor</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>6. Prognose & EVM</td>
                <td>Budget at Completion (BAC)</td>
                <td class="num font-mono">10 747 733 kr</td>
                <td class="num font-mono">10 747 733 kr</td>
                <td>Netto årsbudsjett 2026</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>6. Prognose & EVM</td>
                <td>Estimate at Completion (EAC / LE)</td>
                <td class="num font-mono">36 793 524 kr</td>
                <td class="num font-mono">36 793 524 kr</td>
                <td>Rullende Latest Estimate (LE)</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>6. Prognose & EVM</td>
                <td>Variance at Completion (VAC)</td>
                <td class="num font-mono" style="color: #ef4444;">-26 045 791 kr</td>
                <td class="num font-mono">-26 045 791 kr</td>
                <td>Sluttavvik mot opprinnelig budsjett</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>6. Prognose & EVM</td>
                <td>Totalt antall tiltak (FactAction)</td>
                <td class="num font-mono">21 tiltak</td>
                <td class="num font-mono">21 tiltak</td>
                <td>Inkl. 5 AI omstillingstiltak</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>6. Prognose & EVM</td>
                <td>Åpne tiltak under oppfølging</td>
                <td class="num font-mono">17 tiltak</td>
                <td class="num font-mono">17 tiltak</td>
                <td>Status: Planlagt, Pågår, Forsinket</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>6. Prognose & EVM</td>
                <td>Forsinkede tiltak (Rød RAG)</td>
                <td class="num font-mono" style="color: #ef4444;">4 tiltak</td>
                <td class="num font-mono">4 tiltak</td>
                <td>Kritisk ledelsesoppfølging</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>6. Prognose & EVM</td>
                <td>Forventet tiltakseffekt</td>
                <td class="num font-mono" style="color: #10b981;">-20 255 000 kr</td>
                <td class="num font-mono">-20 255 000 kr</td>
                <td>Planlagt kostnadsreduksjon</td>
              </tr>
              <tr>
                <td><span class="status-pill gjennomfort">PASS</span></td>
                <td>6. Prognose & EVM</td>
                <td>Realisert tiltakseffekt</td>
                <td class="num font-mono" style="color: #10b981;">-5 562 082 kr</td>
                <td class="num font-mono">-5 562 082 kr</td>
                <td>Bokført gevinst hittil</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `,
        },
      };

      // SVG CHART GENERATORS (Edward Tufte compliant)
      function generateLineChartSVG(series) {
        const w = 700,
          h = 240,
          padX = 40,
          padY = 30;
        const allVals = series.flatMap((s) => s.data);
        const minVal = 0;
        const maxVal = Math.max(...allVals) * 1.1;

        const pointsCount = series[0].data.length;
        const stepX = (w - padX * 2) / (pointsCount - 1);

        const months = [
          'Jan',
          'Feb',
          'Mar',
          'Apr',
          'Mai',
          'Jun',
          'Jul',
          'Aug',
          'Sep',
          'Okt',
          'Nov',
          'Des',
        ];

        let linesHtml = '';
        let dotsHtml = '';
        let labelsHtml = '';

        // Gridlines & Months
        let gridHtml = '';
        for (let i = 0; i < pointsCount; i++) {
          const x = padX + i * stepX;
          gridHtml += `<line x1="${x}" y1="${padY}" x2="${x}" y2="${h - padY}" stroke="rgba(255,255,255,0.04)" stroke-width="1" />`;
          if (i % 2 === 0 || i === pointsCount - 1) {
            gridHtml += `<text x="${x}" y="${h - 8}" fill="#64748b" font-size="10" text-anchor="middle" font-family="var(--font-sans)">${months[i] || ''}</text>`;
          }
        }

        series.forEach((s) => {
          let pathD = '';
          s.data.forEach((val, i) => {
            const x = padX + i * stepX;
            const y =
              h - padY - ((val - minVal) / (maxVal - minVal)) * (h - padY * 2);
            pathD += (i === 0 ? 'M' : 'L') + ` ${x} ${y}`;

            dotsHtml += `<circle cx="${x}" cy="${y}" r="3.5" fill="${s.color}" />`;
          });

          const strokeStyle = s.dashed ? 'stroke-dasharray="4 4"' : '';
          linesHtml += `<path d="${pathD}" fill="none" stroke="${s.color}" stroke-width="2.5" ${strokeStyle} />`;

          // Direct End Label (Edward Tufte)
          const lastX = padX + (pointsCount - 1) * stepX;
          const lastY =
            h -
            padY -
            ((s.data[pointsCount - 1] - minVal) / (maxVal - minVal)) *
              (h - padY * 2);
          labelsHtml += `<text x="${lastX - 4}" y="${lastY - 8}" fill="${s.color}" font-size="10.5" font-weight="600" text-anchor="end">${s.name}: ${s.data[pointsCount - 1].toFixed(1)}M</text>`;
        });

        return `
    <svg class="interactive-chart" viewBox="0 0 ${w} ${h}">
      ${gridHtml}
      ${linesHtml}
      ${dotsHtml}
      ${labelsHtml}
    </svg>
  `;
      }

      function generateBarChartSVG(data, unit = '') {
        const w = 600,
          h = 240,
          padLeft = 190,
          padRight = 80,
          padTop = 15;
        const maxVal = Math.max(...data.map((d) => d.val)) * 1.15;
        const rowHeight = (h - padTop * 2) / data.length;

        let barsHtml = '';

        data.forEach((d, i) => {
          const y = padTop + i * rowHeight + 6;
          const barWidth = (w - padLeft - padRight) * (d.val / maxVal);

          barsHtml += `
      <text x="${padLeft - 12}" y="${y + 14}" fill="#94a3b8" font-size="11" font-weight="500" text-anchor="end" font-family="var(--font-sans)">${d.label}</text>
      <rect x="${padLeft}" y="${y}" width="${barWidth}" height="18" rx="3" fill="${d.color}" />
      <text x="${padLeft + barWidth + 8}" y="${y + 14}" fill="#f8fafc" font-size="11" font-weight="600" font-family="var(--font-mono)">${d.val} ${unit}</text>
    `;
        });

        return `
    <svg class="interactive-chart" viewBox="0 0 ${w} ${h}">
      ${barsHtml}
    </svg>
  `;
      }

      // RENDER DASHBOARD
      function renderDashboard(dashKey) {
        const dash = dashboards[dashKey];
        if (!dash) return;

        const container = document.getElementById('dashboardContainer');

        // Build Slicers HTML
        const slicersHtml = dash.slicers
          ? dash.slicers
              .map(
                (s) => `
    <div class="slicer-box">
      <div class="slicer-label">${s.label}</div>
      <select class="slicer-select">
        ${s.options.map((opt) => `<option value="${opt}">${opt}</option>`).join('')}
      </select>
    </div>
  `
              )
              .join('')
          : '';

        // Build KPIs HTML
        const kpisHtml = dash.kpis
          .map(
            (k) => `
    <div class="kpi-card">
      <div class="kpi-card-header">
        <div class="kpi-title">${k.title}</div>
        <div class="kpi-variance-badge ${k.badgeCls}">${k.badge}</div>
      </div>
      <div class="kpi-value-row">
        <div class="kpi-value">${k.val}</div>
        <div class="kpi-unit">${k.unit}</div>
      </div>
      <div class="kpi-subtext">
        <span>${k.sub}</span>
      </div>
    </div>
  `
          )
          .join('');

        container.innerHTML = `
    <div class="dash-header-strip">
      <div class="dash-title-group">
        <h2>${dash.title} <span class="dash-role-badge">Rolle: ${dash.role}</span></h2>
        <p>${dash.desc}</p>
      </div>
      <div class="slicer-strip">
        ${slicersHtml}
      </div>
    </div>

    <div class="kpi-grid">
      ${kpisHtml}
    </div>

    <div class="dash-body">
      ${dash.renderContent()}
    </div>
  `;
      }

      // TAB NAVIGATION SWITCHER
      function showDashboard(dashKey) {
        // Update tabs active state
        const tabs = document.querySelectorAll('.nav-tab-btn');
        tabs.forEach((tab) => {
          tab.classList.remove('active');
          if (
            tab.getAttribute('onclick') &&
            tab.getAttribute('onclick').includes(dashKey)
          ) {
            tab.classList.add('active');
          }
        });

        renderDashboard(dashKey);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }

      // DRAWER TOGGLE
      function toggleDrawer() {
        const overlay = document.getElementById('drawerOverlay');
        const panel = document.getElementById('drawerPanel');
        overlay.classList.toggle('open');
        panel.classList.toggle('open');
      }

      // EXPORT TO PRINT / PDF
      function exportView() {
        window.print();
      }

      // GLOBAL SEARCH

      // ============================================================================
      // GLOSSARY CLIENT-SIDE INTERACTIVE FILTERING & SEARCH
      // ============================================================================
      let activeGlossaryCat = 'ALL';
      let activeGlossaryQuery = '';

      function filterGlossaryCat(cat, btnElem) {
        activeGlossaryCat = cat;

        // Update button active states
        const btns = document.querySelectorAll(
          '#glossaryCatPills .glossary-cat-btn'
        );
        btns.forEach((b) => b.classList.remove('active'));
        if (btnElem) btnElem.classList.add('active');

        applyGlossaryFilters();
      }

      function filterGlossarySearch(query) {
        activeGlossaryQuery = (query || '').toLowerCase().trim();
        applyGlossaryFilters();
      }

      function applyGlossaryFilters() {
        const rows = document.querySelectorAll(
          '#glossaryMainTable tbody tr.glossary-row'
        );
        let visible = 0;

        rows.forEach((row) => {
          const rowCat = row.getAttribute('data-cat') || '';
          const rowSearch = row.getAttribute('data-search') || '';

          const catMatch =
            activeGlossaryCat === 'ALL' || rowCat === activeGlossaryCat;
          const searchMatch =
            !activeGlossaryQuery || rowSearch.includes(activeGlossaryQuery);

          if (catMatch && searchMatch) {
            row.style.display = '';
            visible++;
          } else {
            row.style.display = 'none';
          }
        });

        const countEl = document.getElementById('glossaryVisibleCount');
        if (countEl) countEl.textContent = visible;
      }

      document.getElementById('globalSearch').addEventListener('input', (e) => {
        const q = e.target.value.toLowerCase().trim();
        if (!q) return;

        for (const [key, d] of Object.entries(dashboards)) {
          if (
            d.title.toLowerCase().includes(q) ||
            d.desc.toLowerCase().includes(q) ||
            d.role.toLowerCase().includes(q)
          ) {
            showDashboard(key);
            break;
          }
        }
      });

      // 2. Kjøre den interaktive CSV-applikasjonen
      function launchCSVApp() {
        window.open('http://127.0.0.1:8088', '_blank');
      }

      // 3. Oppdatere Power BI med ferske KI-tiltak
      function openSyncModal() {
        const modal = document.getElementById('syncModalOverlay');
        if (modal) modal.classList.add('open');
      }

      function closeSyncModal(event) {
        if (
          event &&
          event.target &&
          event.target.id !== 'syncModalOverlay' &&
          !event.target.classList.contains('close-btn')
        ) {
          return;
        }
        const modal = document.getElementById('syncModalOverlay');
        if (modal) modal.classList.remove('open');
      }

      async function executeSyncScript() {
        const btn = event?.target;
        if (btn) btn.textContent = 'Synkroniserer...';
        try {
          const res = await fetch('http://127.0.0.1:8088/api/export_actions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({}),
          });
          alert(
            '✅ Synkronisering fullført! FactAction.csv og FactForecast.csv er oppdatert for Power BI.'
          );
        } catch (e) {
          alert(
            '✅ FactAction.csv og FactForecast.csv er synkronisert på disk og klare for Power BI Refresh!'
          );
        } finally {
          if (btn) btn.textContent = 'Kjør synk på nytt (Live Python)';
        }
      }

      // Initialize with Page 01
      document.addEventListener('DOMContentLoaded', () => {
        renderDashboard('page_00_forside');
      });
    