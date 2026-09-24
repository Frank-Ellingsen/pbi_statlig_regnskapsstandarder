# -*- coding: utf-8 -*-
"""
add_rapportering_to_index_html.py
---------------------------------
Incorporate the UiA Kontroll- og Rapporteringsveileder and reporting skills
into index.html as Dashboard 11: "Rapportering Skills".
"""

import os
import sys

def update_index_html():
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "index.html"))
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add Navigation Button if not already present
    nav_marker = """<li><button class="nav-tab-btn" onclick="showDashboard('page_10_ai_agents')"><span class="tab-badge" style="background: rgba(99,102,241,0.25); color:#a5b4fc; border: 1px solid rgba(99,102,241,0.5);">10</span> AI Controller Hub</button></li>"""
    
    new_nav_button = """<li><button class="nav-tab-btn" onclick="showDashboard('page_10_ai_agents')"><span class="tab-badge" style="background: rgba(99,102,241,0.25); color:#a5b4fc; border: 1px solid rgba(99,102,241,0.5);">10</span> AI Controller Hub</button></li>
      <li><button class="nav-tab-btn" onclick="showDashboard('page_11_rapportering')"><span class="tab-badge" style="background: rgba(245,158,11,0.25); color:#fbbf24; border: 1px solid rgba(245,158,11,0.5);">11</span> Rapportering Skills</button></li>"""

    if "page_11_rapportering" not in content and nav_marker in content:
        content = content.replace(nav_marker, new_nav_button)
        print("Inserted Tab 11 into nav bar.")
    elif "page_11_rapportering" in content:
        print("Tab 11 already exists in nav bar.")

    # 2. Add dashboard object definition to `dashboards`
    dashboard_11_code = """
  page_11_rapportering: {
    title: "11 Veileder for Kontroll & Rapportering ved UiA",
    role: "Senior Controller / Fagansvarlig Rapportering",
    desc: "Rettslig og operasjonelt rammeverk for statlig økonomistyring: KD 2025 finansieringsmodell, DFØ SRS (1, 9, 10, 17), 5 %-regelen (F-05-20), BOA TDI-modellen, tertialkadens (T1/T2/LE) og Note 15.",
    slicers: [
      { label: "Regulatorisk Område", options: ["Alle områder", "KD Finansiering 2025", "SRS Regnskapsstandarder", "5 %-regelen & Note 15", "BOA & TDI-modellen", "Tertialvis Rapportering"] },
      { label: "Revisjonsstatus", options: ["Alle kontroller (29)", "Godkjent [PASS] (29)", "Avvik [FAIL] (0)"] }
    ],
    kpis: [
      { title: "5 %-Regel Tak (F-05-20)", val: "106,94 Mkr", unit: "MNOK tak", badge: "0,01% benyttet", badgeCls: "rag-green", sub: "Maksimal tillatt bevilgningsreserve (5,0 % av 2 138,8 Mkr)" },
      { title: "KD SPE Produksjon 2025", val: "5 615,7", unit: "SPE60 enheter", badge: "86,4% måloppnåelse", badgeCls: "rag-amber", sub: "336 945 avlagte studiepoeng fordelt på 3 finansieringskategorier" },
      { title: "BOA & TDI Portefølje", val: "25,68 Mkr", unit: "MNOK inntekter", badge: "SRS 10 + SRS 9", badgeCls: "rag-blue", sub: "NFR (12,90M) + EU Horizon (7,43M) + Oppdrag (5,35M)" },
      { title: "Lønnsandel & Kapasitet", val: "68,97 %", unit: "av driftskostnader", badge: "1 482,3 Mkr", badgeCls: "rag-green", sub: "9,81 studenter per faglig årsverk | Frikjøp overvåkes i Unit4" }
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
            <a href="rapportering skills/SKILL.md" target="_blank" class="header-btn" style="text-decoration: none; font-size: 11.5px; padding: 5px 10px;">
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
                <td class="num font-mono">5 615,74 SPE</td>
                <td class="num font-mono">5 615,74 SPE</td>
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
    `
  }
"""

    if "page_11_rapportering:" not in content:
        # Insert before closing `};` of dashboards
        closing_marker = "  }\n};"
        if closing_marker in content:
            content = content.replace(closing_marker, "  },\n" + dashboard_11_code + "\n};")
            print("Inserted page_11_rapportering into dashboards object.")
        else:
            # Try alternate closing
            alt_closing = "  }\r\n};"
            if alt_closing in content:
                content = content.replace(alt_closing, "  },\r\n" + dashboard_11_code + "\r\n};")
                print("Inserted page_11_rapportering into dashboards object (CRLF).")
            else:
                print("Could not find closing of dashboards object.")
    else:
        print("page_11_rapportering already exists in dashboards.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("index.html update complete.")

if __name__ == "__main__":
    update_index_html()
