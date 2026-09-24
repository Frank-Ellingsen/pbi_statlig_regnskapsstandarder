"""
Apply RAG status badges and styling to index.html
Synchronizes the web portal tables with Power BI PBIR report tables and DAX RAG measures.
"""
import sys

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update CSS for .status-pill
    old_css = """    /* Status Pill (FactAction) */
    .status-pill {
      display: inline-block;
      padding: 2px 7px;
      border-radius: 9999px;
      font-size: 10px;
      font-weight: 600;
    }
    .status-pill.gjennomfort {
      background: var(--color-green-bg);
      color: var(--color-green);
    }
    .status-pill.pagar {
      background: var(--color-blue-bg);
      color: #60a5fa;
    }
    .status-pill.forsinket {
      background: var(--color-red-bg);
      color: var(--color-red);
    }
    .status-pill.planlagt {
      background: rgba(255, 255, 255, 0.06);
      color: var(--text-secondary);
    }"""

    new_css = """    /* Status Pill (FactAction & RAG Status) */
    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 2px 7px;
      border-radius: 9999px;
      font-size: 10px;
      font-weight: 600;
      white-space: nowrap;
    }
    .status-pill.gjennomfort, .status-pill.rag-green {
      background: var(--color-green-bg);
      color: var(--color-green);
    }
    .status-pill.pagar, .status-pill.rag-amber {
      background: var(--color-amber-bg);
      color: var(--color-amber);
    }
    .status-pill.forsinket, .status-pill.rag-red {
      background: var(--color-red-bg);
      color: var(--color-red);
    }
    .status-pill.planlagt, .status-pill.rag-neutral {
      background: rgba(255, 255, 255, 0.06);
      color: var(--text-secondary);
    }"""

    assert old_css in html, "Failed to locate old CSS in index.html"
    html = html.replace(old_css, new_css, 1)

    # 2. Table 3 (Page 1 Tiltak)
    old_t3 = """              <tbody>
                <tr>
                  <td><code>T-01</code></td>
                  <td>Vakansestopp adm. stillinger</td>
                  <td>Instituttleder</td>
                  <td class="num">-1 200 000</td>
                  <td class="num">-950 000</td>
                  <td><span class="status-pill gjennomfort">Gjennomført</span></td>
                </tr>
                <tr>
                  <td><code>T-02</code></td>
                  <td>Redusert sensorhonorar digital eksamen</td>
                  <td>Studieleder</td>
                  <td class="num">-450 000</td>
                  <td class="num">-310 000</td>
                  <td><span class="status-pill pagar">Pågår</span></td>
                </tr>
                <tr>
                  <td><code>T-03</code></td>
                  <td>Kutt i eksterne konsulenttjenester</td>
                  <td>Kontorsjef</td>
                  <td class="num">-800 000</td>
                  <td class="num">-200 000</td>
                  <td><span class="status-pill forsinket">Forsinket</span></td>
                </tr>
                <tr>
                  <td><code>T-04</code></td>
                  <td>Samleslåing av valgemner < 15 stud</td>
                  <td>Instituttleder</td>
                  <td class="num">-1 500 000</td>
                  <td class="num">-1 100 000</td>
                  <td><span class="status-pill pagar">Pågår</span></td>
                </tr>
              </tbody>"""

    new_t3 = """              <tbody>
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
              </tbody>"""

    assert old_t3 in html, "Failed to locate Table 3 in index.html"
    html = html.replace(old_t3, new_t3, 1)

    # 3. Table 6 (Page 3 Executive)
    old_t6 = """            <thead>
              <tr>
                <th>Fakultet / Område</th>
                <th class="num">Årsbudsjett</th>
                <th class="num">Regnskap YTD</th>
                <th class="num">Forecast LE</th>
                <th class="num">Forecastavvik</th>
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
                <td class="num">1 285,9</td>
                <td class="num">25 678 288 kr</td>
                <td class="num" style="color:#38bdf8;">2 678 524 kr</td>
              </tr>
            </tfoot>"""

    # Note: check if total netto etter tiltak is 26 788 524 or 2 678 524
    # let's find the exact block for Table 6
    if "Totalt institusjonen" in html:
        sub_t6_start = html.find('<table class="tufte-table">\n            <thead>\n              <tr>\n                <th>Fakultet / Område')
        sub_t6_end = html.find('</table>', sub_t6_start) + len('</table>')
        existing_t6 = html[sub_t6_start:sub_t6_end]
        
        # Replace header and rows with RAG status
        updated_t6 = existing_t6.replace(
            '<th>Fakultet / Område</th>\n                <th class="num">Årsbudsjett</th>\n                <th class="num">Regnskap YTD</th>\n                <th class="num">Forecast LE</th>\n                <th class="num">Forecastavvik</th>',
            '<th>Fakultet / Område</th>\n                <th class="num">Årsbudsjett</th>\n                <th class="num">Regnskap YTD</th>\n                <th class="num">Forecast LE</th>\n                <th class="num">Forecastavvik</th>\n                <th>Forecast RAG</th>'
        )
        updated_t6 = updated_t6.replace(
            '<td class="num" style="color:#ef4444;">+8 400 000</td>\n                <td class="num">342,0</td>',
            '<td class="num" style="color:#ef4444;">+8 400 000</td>\n                <td><span class="status-pill rag-red">🔴 Rød (&gt;5%)</span></td>\n                <td class="num">342,0</td>'
        )
        updated_t6 = updated_t6.replace(
            '<td class="num" style="color:#ef4444;">+9 800 000</td>\n                <td class="num">410,5</td>',
            '<td class="num" style="color:#ef4444;">+9 800 000</td>\n                <td><span class="status-pill rag-red">🔴 Rød (&gt;5%)</span></td>\n                <td class="num">410,5</td>'
        )
        updated_t6 = updated_t6.replace(
            '<td class="num" style="color:#ef4444;">+4 200 000</td>\n                <td class="num">265,0</td>',
            '<td class="num" style="color:#ef4444;">+4 200 000</td>\n                <td><span class="status-pill rag-red">🔴 Rød (&gt;5%)</span></td>\n                <td class="num">265,0</td>'
        )
        updated_t6 = updated_t6.replace(
            '<td class="num" style="color:#f59e0b;">+3 645 791</td>\n                <td class="num">268,4</td>',
            '<td class="num" style="color:#f59e0b;">+3 645 791</td>\n                <td><span class="status-pill rag-red">🔴 Rød (&gt;5%)</span></td>\n                <td class="num">268,4</td>'
        )
        updated_t6 = updated_t6.replace(
            '<td class="num" style="color:#ef4444;">+26 045 791 kr</td>\n                <td class="num">1 285,9</td>',
            '<td class="num" style="color:#ef4444;">+26 045 791 kr</td>\n                <td><span class="status-pill rag-red">🔴 Rød (&gt;5%)</span></td>\n                <td class="num">1 285,9</td>'
        )
        html = html[:sub_t6_start] + updated_t6 + html[sub_t6_end:]

    # 4. Table 7 (Page 4 Styret Utdanning)
    old_t7 = """              <thead>
                <tr>
                  <th>Fakultet</th>
                  <th class="num">Reg. Studenter</th>
                  <th class="num">Avlagte SP</th>
                  <th class="num">SPE60</th>
                  <th class="num">Måloppnåelse</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Handelshøyskolen</td>
                  <td class="num">2 410</td>
                  <td class="num">128 430</td>
                  <td class="num">2 140,5</td>
                  <td class="num" style="color:#10b981;">89,2%</td>
                </tr>
                <tr>
                  <td>Fakultet for teknologi og realfag</td>
                  <td class="num">1 750</td>
                  <td class="num">88 400</td>
                  <td class="num">1 473,3</td>
                  <td class="num" style="color:#f59e0b;">82,4%</td>
                </tr>
                <tr>
                  <td>Fakultet for samfunnsvitenskap</td>
                  <td class="num">1 380</td>
                  <td class="num">74 215</td>
                  <td class="num">1 236,9</td>
                  <td class="num" style="color:#10b981;">88,1%</td>
                </tr>
                <tr>
                  <td>Fakultet for helse og idrett</td>
                  <td class="num">950</td>
                  <td class="num">45 900</td>
                  <td class="num">765,0</td>
                  <td class="num" style="color:#f59e0b;">84,0%</td>
                </tr>
              </tbody>"""

    new_t7 = """              <thead>
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
              </tbody>"""

    assert old_t7 in html, "Failed to locate Table 7 in index.html"
    html = html.replace(old_t7, new_t7, 1)

    # 5. Table 8 (Page 4 Styret Risiko)
    old_t8 = """              <tbody>
                <tr>
                  <td>Fak. for teknologi og realfag</td>
                  <td class="num" style="color:#ef4444;">+9 800 000</td>
                  <td class="num" style="color:#10b981;">-2 800 000</td>
                  <td class="num" style="color:#f59e0b;">+7 000 000</td>
                  <td><span class="status-pill forsinket">Høy</span></td>
                </tr>
                <tr>
                  <td>Handelshøyskolen</td>
                  <td class="num" style="color:#ef4444;">+8 400 000</td>
                  <td class="num" style="color:#10b981;">-3 400 000</td>
                  <td class="num" style="color:#f59e0b;">+5 000 000</td>
                  <td><span class="status-pill forsinket">Høy</span></td>
                </tr>
                <tr>
                  <td>Fak. for samfunnsvitenskap</td>
                  <td class="num" style="color:#f59e0b;">+4 200 000</td>
                  <td class="num" style="color:#10b981;">-1 500 000</td>
                  <td class="num" style="color:#f59e0b;">+2 700 000</td>
                  <td><span class="status-pill pagar">Middels</span></td>
                </tr>
                <tr>
                  <td>Fellesområde / Adm.</td>
                  <td class="num" style="color:#f59e0b;">+3 645 791</td>
                  <td class="num" style="color:#10b981;">-2 305 000</td>
                  <td class="num" style="color:#10b981;">+1 340 791</td>
                  <td><span class="status-pill gjennomfort">Lav</span></td>
                </tr>
              </tbody>"""

    new_t8 = """              <tbody>
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

    assert old_t8 in html, "Failed to locate Table 8 in index.html"
    html = html.replace(old_t8, new_t8, 1)

    # 6. Table 9 (Page 4 Styret Kritiske tiltak)
    old_t9 = """            <tbody>
              <tr>
                <td><code>T-01</code></td>
                <td>Vakansestopp i administrative stillinger</td>
                <td>Lønnsvekst og overkapasitet</td>
                <td>HR-direktør</td>
                <td class="num">-1 200 000</td>
                <td class="num">-950 000</td>
                <td><span class="status-pill gjennomfort">Gjennomført</span></td>
              </tr>
              <tr>
                <td><code>T-05</code></td>
                <td>Reduksjon av eksterne konsulentavtaler IT</td>
                <td>Høye konsulentkostnader</td>
                <td>IT-direktør</td>
                <td class="num">-1 500 000</td>
                <td class="num">-800 000</td>
                <td><span class="status-pill pagar">Pågår</span></td>
              </tr>
              <tr>
                <td><code>T-08</code></td>
                <td>Nedskalering av arealleie Campus Hoved</td>
                <td>Høye leiekostnader</td>
                <td>Eiendomsdirektør</td>
                <td class="num">-2 000 000</td>
                <td class="num">-600 000</td>
                <td><span class="status-pill forsinket">Forsinket</span></td>
              </tr>
              <tr>
                <td><code>T-12</code></td>
                <td>Optimalisering av studietilbud og samkjøring</td>
                <td>Små studentkull</td>
                <td>Dekan Helse</td>
                <td class="num">-1 100 000</td>
                <td class="num">-900 000</td>
                <td><span class="status-pill pagar">Pågår</span></td>
              </tr>
            </tbody>"""

    new_t9 = """            <tbody>
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
            </tbody>"""

    assert old_t9 in html, "Failed to locate Table 9 in index.html"
    html = html.replace(old_t9, new_t9, 1)

    # 7. Table 11 (Page 6 Studieportefølje)
    old_t11 = """            <thead>
              <tr>
                <th>Kode</th>
                <th>Studieprogramnavn</th>
                <th>Nivå</th>
                <th class="num">Normert</th>
                <th class="num">Studenter</th>
                <th class="num">Planlagte SP</th>
                <th class="num">Avlagte SP</th>
                <th class="num">SPE60</th>
                <th class="num">Måloppnåelse</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>BOKADM</code></td>
                <td>Bachelor i økonomi og administrasjon</td>
                <td>Bachelor</td>
                <td class="num">180</td>
                <td class="num">850</td>
                <td class="num">51 000</td>
                <td class="num">46 200</td>
                <td class="num">770,0</td>
                <td class="num" style="color:#10b981;">90,6%</td>
              </tr>
              <tr>
                <td><code>MOKLED</code></td>
                <td>Master i økonomi og ledelse (Siviløkonom)</td>
                <td>Master</td>
                <td class="num">120</td>
                <td class="num">420</td>
                <td class="num">25 200</td>
                <td class="num">23 100</td>
                <td class="num">385,0</td>
                <td class="num" style="color:#10b981;">91,7%</td>
              </tr>
              <tr>
                <td><code>BRETT</code></td>
                <td>Bachelor i rettsvitenskap</td>
                <td>Bachelor</td>
                <td class="num">180</td>
                <td class="num">520</td>
                <td class="num">31 200</td>
                <td class="num">26 400</td>
                <td class="num">440,0</td>
                <td class="num" style="color:#f59e0b;">84,6%</td>
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
                <td class="num" style="color:#ef4444;">80,5%</td>
              </tr>
            </tbody>"""

    new_t11 = """            <thead>
              <tr>
                <th>Kode</th>
                <th>Studieprogramnavn</th>
                <th>Nivå</th>
                <th class="num">Normert</th>
                <th class="num">Studenter</th>
                <th class="num">Planlagte SP</th>
                <th class="num">Avlagte SP</th>
                <th class="num">SPE60</th>
                <th class="num">Måloppnåelse</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>BOKADM</code></td>
                <td>Bachelor i økonomi og administrasjon</td>
                <td>Bachelor</td>
                <td class="num">180</td>
                <td class="num">850</td>
                <td class="num">51 000</td>
                <td class="num">46 200</td>
                <td class="num">770,0</td>
                <td class="num" style="color:#10b981;">90,6%</td>
                <td><span class="status-pill rag-green">🟢 Mål nådd (&gt;=90%)</span></td>
              </tr>
              <tr>
                <td><code>MOKLED</code></td>
                <td>Master i økonomi og ledelse (Siviløkonom)</td>
                <td>Master</td>
                <td class="num">120</td>
                <td class="num">420</td>
                <td class="num">25 200</td>
                <td class="num">23 100</td>
                <td class="num">385,0</td>
                <td class="num" style="color:#10b981;">91,7%</td>
                <td><span class="status-pill rag-green">🟢 Mål nådd (&gt;=90%)</span></td>
              </tr>
              <tr>
                <td><code>BRETT</code></td>
                <td>Bachelor i rettsvitenskap</td>
                <td>Bachelor</td>
                <td class="num">180</td>
                <td class="num">520</td>
                <td class="num">31 200</td>
                <td class="num">26 400</td>
                <td class="num">440,0</td>
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
                <td class="num" style="color:#ef4444;">80,5%</td>
                <td><span class="status-pill rag-amber">🟡 Moderat (80-90%)</span></td>
              </tr>
            </tbody>"""

    assert old_t11 in html, "Failed to locate Table 11 in index.html"
    html = html.replace(old_t11, new_t11, 1)

    # 8. Table 12 (Page 7 Action Tracker)
    old_t12 = """            <tbody>
              <tr>
                <td><code>T-01</code></td>
                <td>Vakansestopp adm. stillinger</td>
                <td>Lønnsvekst over ramme</td>
                <td>HR-direktør</td>
                <td>2026-06-30</td>
                <td class="num">-1 200 000</td>
                <td class="num">-950 000</td>
                <td><span class="status-pill gjennomfort">Gjennomført</span></td>
                <td>Høy</td>
              </tr>
              <tr>
                <td><code>T-02</code></td>
                <td>Redusert sensorhonorar digital eksamen</td>
                <td>Høye sensorkostnader</td>
                <td>Studieleder</td>
                <td>2026-10-15</td>
                <td class="num">-450 000</td>
                <td class="num">-310 000</td>
                <td><span class="status-pill pagar">Pågår</span></td>
                <td>Medium</td>
              </tr>
              <tr>
                <td><code>T-03</code></td>
                <td>Kutt i konsulenter økonomisystem</td>
                <td>Dyrt eksternt bistand</td>
                <td>Kontorsjef</td>
                <td>2026-08-01</td>
                <td class="num">-800 000</td>
                <td class="num">-200 000</td>
                <td><span class="status-pill forsinket">Forsinket</span></td>
                <td>Høy</td>
              </tr>
              <tr>
                <td><code>T-04</code></td>
                <td>Samleslåing av valgemner < 15 stud</td>
                <td>Små emner og lav timeeffektivitet</td>
                <td>Instituttleder</td>
                <td>2026-11-30</td>
                <td class="num">-1 500 000</td>
                <td class="num">-1 100 000</td>
                <td><span class="status-pill pagar">Pågår</span></td>
                <td>Høy</td>
              </tr>
              <tr>
                <td><code>T-08</code></td>
                <td>Nedskalering av arealleie Campus Hoved</td>
                <td>Tomme kontorer / hybridarbeid</td>
                <td>Eiendomsdirektør</td>
                <td>2026-09-01</td>
                <td class="num">-2 000 000</td>
                <td class="num">-600 000</td>
                <td><span class="status-pill forsinket">Forsinket</span></td>
                <td>Høy</td>
              </tr>
            </tbody>"""

    new_t12 = """            <tbody>
              <tr>
                <td><code>T-01</code></td>
                <td>Vakansestopp adm. stillinger</td>
                <td>Lønnsvekst over ramme</td>
                <td>HR-direktør</td>
                <td>2026-06-30</td>
                <td class="num">-1 200 000</td>
                <td class="num">-950 000</td>
                <td><span class="status-pill gjennomfort">🟢 Gjennomført</span></td>
                <td>Høy</td>
              </tr>
              <tr>
                <td><code>T-02</code></td>
                <td>Redusert sensorhonorar digital eksamen</td>
                <td>Høye sensorkostnader</td>
                <td>Studieleder</td>
                <td>2026-10-15</td>
                <td class="num">-450 000</td>
                <td class="num">-310 000</td>
                <td><span class="status-pill pagar">🟡 Pågår</span></td>
                <td>Medium</td>
              </tr>
              <tr>
                <td><code>T-03</code></td>
                <td>Kutt i konsulenter økonomisystem</td>
                <td>Dyrt eksternt bistand</td>
                <td>Kontorsjef</td>
                <td>2026-08-01</td>
                <td class="num">-800 000</td>
                <td class="num">-200 000</td>
                <td><span class="status-pill forsinket">🔴 Forsinket</span></td>
                <td>Høy</td>
              </tr>
              <tr>
                <td><code>T-04</code></td>
                <td>Samleslåing av valgemner &lt; 15 stud</td>
                <td>Små emner og lav timeeffektivitet</td>
                <td>Instituttleder</td>
                <td>2026-11-30</td>
                <td class="num">-1 500 000</td>
                <td class="num">-1 100 000</td>
                <td><span class="status-pill pagar">🟡 Pågår</span></td>
                <td>Høy</td>
              </tr>
              <tr>
                <td><code>T-08</code></td>
                <td>Nedskalering av arealleie Campus Hoved</td>
                <td>Tomme kontorer / hybridarbeid</td>
                <td>Eiendomsdirektør</td>
                <td>2026-09-01</td>
                <td class="num">-2 000 000</td>
                <td class="num">-600 000</td>
                <td><span class="status-pill forsinket">🔴 Forsinket</span></td>
                <td>Høy</td>
              </tr>
            </tbody>"""

    assert old_t12 in html, "Failed to locate Table 12 in index.html"
    html = html.replace(old_t12, new_t12, 1)

    # 9. Table 13 (Page 8 Controller Cockpit)
    old_t13 = """            <thead>
              <tr>
                <th>Fakultet</th>
                <th>Institutt</th>
                <th>Regnskapslinje</th>
                <th>Konto</th>
                <th class="num">Regnskap YTD</th>
                <th class="num">Budsjett YTD</th>
                <th class="num">Avvik YTD</th>
                <th class="num">Forecast Helår</th>
                <th class="num">Forecastavvik</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Handelshøyskolen</td>
                <td>Inst. for økonomi</td>
                <td>Lønnskostnader</td>
                <td>5000 Fast lønn</td>
                <td class="num">1 840 200</td>
                <td class="num">1 860 000</td>
                <td class="num" style="color:#10b981;">-19 800</td>
                <td class="num">6 450 000</td>
                <td class="num" style="color:#ef4444;">+1 420 000</td>
              </tr>
              <tr>
                <td>Handelshøyskolen</td>
                <td>Inst. for økonomi</td>
                <td>Lønnskostnader</td>
                <td>5010 Sensorer</td>
                <td class="num">380 400</td>
                <td class="num">350 000</td>
                <td class="num" style="color:#ef4444;">+30 400</td>
                <td class="num">1 240 000</td>
                <td class="num" style="color:#ef4444;">+290 000</td>
              </tr>
              <tr>
                <td>Handelshøyskolen</td>
                <td>Inst. for rettsvitenskap</td>
                <td>Andre driftskostnader</td>
                <td>6700 Konsulenter</td>
                <td class="num">140 000</td>
                <td class="num">160 000</td>
                <td class="num" style="color:#10b981;">-20 000</td>
                <td class="num">480 000</td>
                <td class="num" style="color:#10b981;">-40 000</td>
              </tr>
              <tr>
                <td>Teknologi & realfag</td>
                <td>Inst. for IKT</td>
                <td>Lønnskostnader</td>
                <td>5000 Fast lønn</td>
                <td class="num">2 410 000</td>
                <td class="num">2 450 000</td>
                <td class="num" style="color:#10b981;">-40 000</td>
                <td class="num">8 120 000</td>
                <td class="num" style="color:#ef4444;">+1 850 000</td>
              </tr>
            </tbody>"""

    new_t13 = """            <thead>
              <tr>
                <th>Fakultet</th>
                <th>Institutt</th>
                <th>Regnskapslinje</th>
                <th>Konto</th>
                <th class="num">Regnskap YTD</th>
                <th class="num">Budsjett YTD</th>
                <th class="num">Avvik YTD</th>
                <th>Avvik RAG</th>
                <th class="num">Forecast Helår</th>
                <th class="num">Forecastavvik</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Handelshøyskolen</td>
                <td>Inst. for økonomi</td>
                <td>Lønnskostnader</td>
                <td>5000 Fast lønn</td>
                <td class="num">1 840 200</td>
                <td class="num">1 860 000</td>
                <td class="num" style="color:#10b981;">-19 800</td>
                <td><span class="status-pill rag-green">🟢 Grønn (&lt;=2%)</span></td>
                <td class="num">6 450 000</td>
                <td class="num" style="color:#ef4444;">+1 420 000</td>
              </tr>
              <tr>
                <td>Handelshøyskolen</td>
                <td>Inst. for økonomi</td>
                <td>Lønnskostnader</td>
                <td>5010 Sensorer</td>
                <td class="num">380 400</td>
                <td class="num">350 000</td>
                <td class="num" style="color:#ef4444;">+30 400</td>
                <td><span class="status-pill rag-red">🔴 Rød (&gt;5%)</span></td>
                <td class="num">1 240 000</td>
                <td class="num" style="color:#ef4444;">+290 000</td>
              </tr>
              <tr>
                <td>Handelshøyskolen</td>
                <td>Inst. for rettsvitenskap</td>
                <td>Andre driftskostnader</td>
                <td>6700 Konsulenter</td>
                <td class="num">140 000</td>
                <td class="num">160 000</td>
                <td class="num" style="color:#10b981;">-20 000</td>
                <td><span class="status-pill rag-green">🟢 Grønn (&lt;=2%)</span></td>
                <td class="num">480 000</td>
                <td class="num" style="color:#10b981;">-40 000</td>
              </tr>
              <tr>
                <td>Teknologi & realfag</td>
                <td>Inst. for IKT</td>
                <td>Lønnskostnader</td>
                <td>5000 Fast lønn</td>
                <td class="num">2 410 000</td>
                <td class="num">2 450 000</td>
                <td class="num" style="color:#10b981;">-40 000</td>
                <td><span class="status-pill rag-green">🟢 Grønn (&lt;=2%)</span></td>
                <td class="num">8 120 000</td>
                <td class="num" style="color:#ef4444;">+1 850 000</td>
              </tr>
            </tbody>"""

    assert old_t13 in html, "Failed to locate Table 13 in index.html"
    html = html.replace(old_t13, new_t13, 1)

    # 10. Table 16 (Drill-down Prosjekt EVM)
    old_t16 = """            <thead>
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
              </tr>
            </tbody>"""

    new_t16 = """            <thead>
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
            </tbody>"""

    assert old_t16 in html, "Failed to locate Table 16 in index.html"
    html = html.replace(old_t16, new_t16, 1)

    # 11. Table 17 (Drill-down Tiltak)
    old_t17 = """            <tbody>
              <tr>
                <td><code>T-01</code></td>
                <td>Vakansestopp adm. stillinger</td>
                <td>Lønnsvekst</td>
                <td>HR-direktør</td>
                <td>2026-01-01</td>
                <td>2026-06-30</td>
                <td class="num">-1 200 000</td>
                <td class="num">-950 000</td>
                <td><span class="status-pill gjennomfort">Gjennomført</span></td>
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
                <td><span class="status-pill pagar">Pågår</span></td>
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
                <td><span class="status-pill forsinket">Forsinket</span></td>
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
                <td><span class="status-pill pagar">Pågår</span></td>
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
                <td><span class="status-pill forsinket">Forsinket</span></td>
                <td>Høy</td>
                <td class="num">50%</td>
              </tr>
            </tbody>"""

    new_t17 = """            <tbody>
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
            </tbody>"""

    assert old_t17 in html, "Failed to locate Table 17 in index.html"
    html = html.replace(old_t17, new_t17, 1)

    # 12. Table 18 (Drill-down Studier)
    old_t18 = """            <thead>
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
              </tr>
              <tr>
                <td><code>BIKT</code></td>
                <td>Bachelor i informatikk og cybersikkerhet</td>
                <td>Bachelor</td>
                <td class="num">410</td>
                <td class="num">24 600</td>
                <td class="num">19 800</td>
                <td class="num">330,0</td>
                <td class="num">85,4%</td>
                <td class="num" style="color:#ef4444;">80,5%</td>
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
              </tr>
            </tbody>"""

    new_t18 = """            <thead>
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
            </tbody>"""

    assert old_t18 in html, "Failed to locate Table 18 in index.html"
    html = html.replace(old_t18, new_t18, 1)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Successfully updated index.html with RAG status badges and styling across all tables!")

if __name__ == '__main__':
    main()
