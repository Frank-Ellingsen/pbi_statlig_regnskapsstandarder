# -*- coding: utf-8 -*-
"""
Script to update index.html with Page 09 Begrepskatalog & Metodikk,
glossary CSS, navigation button, and interactive filtering.
Completely bulletproof against quotes and backticks.
"""
import json
import os
import re
import html

def main():
    html_path = "index.html"
    json_path = "scratch/glossary_data.json"

    # We start from git checkout or clean base of index.html
    # Let's read index.html
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    with open(json_path, "r", encoding="utf-8") as f:
        glossary_items = json.load(f)

    print(f"Loaded {len(glossary_items)} glossary terms.")

    # 1. CSS
    glossary_css = """
    /* ==========================================================================
       09 BEGREPSKATALOG & METODIKK STYLES (Edward Tufte compliant)
       ========================================================================== */
    .glossary-controls {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 16px;
      padding: 14px 18px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
    }
    .glossary-cat-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      align-items: center;
    }
    .glossary-cat-btn {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      font-size: 11.5px;
      padding: 5px 11px;
      border-radius: 20px;
      cursor: pointer;
      transition: all 0.15s ease;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }
    .glossary-cat-btn:hover {
      background: rgba(255, 255, 255, 0.08);
      color: var(--text-primary);
    }
    .glossary-cat-btn.active {
      background: rgba(2, 132, 199, 0.2);
      border-color: #0284c7;
      color: #38bdf8;
      font-weight: 600;
    }
    .glossary-count-tag {
      background: rgba(255, 255, 255, 0.1);
      border-radius: 10px;
      padding: 1px 6px;
      font-size: 10px;
      font-variant-numeric: tabular-nums;
    }
    .glossary-cat-btn.active .glossary-count-tag {
      background: rgba(2, 132, 199, 0.4);
      color: #fff;
    }
    .glossary-search-wrap {
      position: relative;
      display: flex;
      align-items: center;
    }
    .glossary-search-input {
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      padding: 6px 12px 6px 32px;
      border-radius: var(--radius-md);
      font-size: 12px;
      width: 260px;
      outline: none;
      transition: all 0.2s ease;
    }
    .glossary-search-input:focus {
      border-color: #38bdf8;
      width: 310px;
    }
    .glossary-method-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-bottom: 20px;
    }
    @media (max-width: 1200px) {
      .glossary-method-grid {
        grid-template-columns: 1fr;
      }
    }
    .method-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 16px 18px;
      border-top: 3px solid #0284c7;
    }
    .method-card.evm {
      border-top-color: #10b981;
    }
    .method-card.rag {
      border-top-color: #f59e0b;
    }
    .method-title {
      font-size: 13.5px;
      font-weight: 600;
      color: var(--text-primary);
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .method-desc {
      font-size: 11.5px;
      color: var(--text-secondary);
      line-height: 1.55;
    }
    .method-formula {
      font-family: var(--font-mono);
      font-size: 10.5px;
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid rgba(255, 255, 255, 0.06);
      padding: 3px 7px;
      border-radius: 4px;
      color: #38bdf8;
      margin-top: 8px;
      display: inline-block;
    }
    .dax-code-pill {
      font-family: var(--font-mono);
      font-size: 10.5px;
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid rgba(255, 255, 255, 0.08);
      padding: 2px 6px;
      border-radius: 4px;
      color: #7dd3fc;
      white-space: pre-wrap;
      word-break: break-all;
      max-width: 290px;
      display: inline-block;
      line-height: 1.35;
    }
    .role-badge {
      display: inline-block;
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 500;
      background: rgba(148, 163, 184, 0.12);
      color: var(--text-secondary);
      border: 1px solid rgba(148, 163, 184, 0.2);
      white-space: nowrap;
    }
    .cat-badge {
      display: inline-block;
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 600;
      letter-spacing: 0.3px;
      white-space: nowrap;
    }
    .cat-01 { background: rgba(56, 189, 248, 0.12); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.25); }
    .cat-02 { background: rgba(16, 185, 129, 0.12); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.25); }
    .cat-03 { background: rgba(245, 158, 11, 0.12); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.25); }
    .cat-04 { background: rgba(139, 92, 246, 0.12); color: #a78bfa; border: 1px solid rgba(139, 92, 246, 0.25); }
    .cat-05 { background: rgba(236, 72, 153, 0.12); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.25); }
    .cat-06 { background: rgba(20, 184, 166, 0.12); color: #2dd4bf; border: 1px solid rgba(20, 184, 166, 0.25); }
    .cat-07 { background: rgba(239, 68, 68, 0.12); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.25); }
    .cat-08 { background: rgba(148, 163, 184, 0.12); color: #cbd5e1; border: 1px solid rgba(148, 163, 184, 0.25); }
    .tufte-table td.desc-cell {
      white-space: normal;
      max-width: 320px;
      line-height: 1.45;
      font-size: 11.5px;
    }
    .tufte-table td.interp-cell {
      white-space: normal;
      max-width: 300px;
      line-height: 1.45;
      font-size: 11.5px;
      color: var(--text-secondary);
    }
  </style>"""

    if "/* ==========================================================================\n       09 BEGREPSKATALOG" not in html_content:
        html_content = html_content.replace("</style>", glossary_css)
        print("Injected glossary CSS.")

    # 2. Header badges
    html_content = html_content.replace('<span class="badge badge-spec">13 Dashboards</span>',
                                        '<span class="badge badge-spec">14 Dashboards & Begrepskatalog</span>')
    html_content = html_content.replace('<span class="badge badge-spec">14 Tabeller / 22 Relasjoner</span>',
                                        '<span class="badge badge-spec">15 Tabeller / 22 Relasjoner</span>')
    html_content = html_content.replace('QA 43/43 Bestått', 'QA 61/61 Bestått')
    html_content = html_content.replace('QA 59/59 Bestått', 'QA 61/61 Bestått')

    # 3. Navigation tabs
    p8_nav_btn = '<li><button class="nav-tab-btn" onclick="showDashboard(\'page_08\')"><span class="tab-badge">08</span> Controller Cockpit</button></li>'
    glossary_nav_btn = (
        '<li><button class="nav-tab-btn" onclick="showDashboard(\'page_08\')"><span class="tab-badge">08</span> Controller Cockpit</button></li>\n'
        '      <li><button class="nav-tab-btn" onclick="showDashboard(\'page_glossary\')"><span class="tab-badge" style="background: rgba(16,185,129,0.2); color:#10b981; border: 1px solid rgba(16,185,129,0.4);">09</span> Begrepskatalog</button></li>'
    )
    if 'showDashboard(\'page_glossary\')' not in html_content:
        html_content = html_content.replace(p8_nav_btn, glossary_nav_btn)
        print("Injected Begrepskatalog into nav-tabs.")

    # 4. Drawer
    html_content = html_content.replace("TMDL Semantisk Modell | 14 Tabeller | 22 Relasjoner | 60+ Mål",
                                        "TMDL Semantisk Modell | 15 Tabeller | 22 Relasjoner | 60+ Mål & Begrepskatalog")
    drawer_target = '<div><span style="color:#38bdf8;">DimStudyProgram</span> [Program] (22 programmer) ──(1:*)──&gt; FactStudyPoints</div>'
    drawer_replacement = (
        '<div><span style="color:#38bdf8;">DimStudyProgram</span> [Program] (22 programmer) ──(1:*)──&gt; FactStudyPoints</div>\n'
        '      <div><span style="color:#10b981;">DimGlossary</span> [BegrepID] (60 nøkkelbegreper) ── Dekan, Controller & Prosjekt referanseordbok</div>'
    )
    if 'DimGlossary' not in html_content:
        html_content = html_content.replace(drawer_target, drawer_replacement)
        print("Updated drawer with DimGlossary.")

    # 5. Build HTML rows for all 60 terms with safe HTML escaping and NO backticks
    def get_cat_class(cat):
        return f"cat-{cat[:2]}"

    rows_html_list = []
    for item in glossary_items:
        bid = item["BegrepID"]
        begrep = item["Begrep"]
        fullt = item["FulltNavn"]
        kat = item["Kategori"]
        defn = item["Definisjon"].replace("`", "'")
        tolk = item["PraktiskTolkning"].replace("`", "'")
        dax = item["FormelDAX"].replace("`", "'")
        rolle = item["RolleKontekst"]
        rapp = item["RelevantRapport"]
        target_page = item.get("targetPage", "")

        cat_cls = get_cat_class(kat)
        
        # Search blob without quotes or backticks to be safe in data-search attribute
        search_blob = f"{begrep} {fullt} {kat} {defn} {tolk} {dax} {rolle} {rapp}".lower()
        search_blob = search_blob.replace('"', ' ').replace("'", ' ').replace('`', ' ')
        search_attr = html.escape(search_blob, quote=True)
        kat_attr = html.escape(kat, quote=True)

        begrep_html = html.escape(begrep)
        fullt_html = html.escape(fullt)
        kat_html = html.escape(kat)
        defn_html = html.escape(defn)
        tolk_html = html.escape(tolk)
        dax_html = html.escape(dax)
        rolle_html = html.escape(rolle)
        rapp_html = html.escape(rapp)

        if target_page:
            link_html = f'<a class="drill-link" onclick="showDashboard(\'{target_page}\')">{rapp_html} &rarr;</a>'
        else:
            link_html = f'<span style="color:var(--text-muted); font-size:11px;">{rapp_html}</span>'

        row = f"""              <tr class="glossary-row" data-cat="{kat_attr}" data-search="{search_attr}">
                <td><strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">{begrep_html}</strong></td>
                <td>{fullt_html}</td>
                <td><span class="cat-badge {cat_cls}">{kat_html}</span></td>
                <td class="desc-cell">{defn_html}</td>
                <td class="interp-cell">{tolk_html}</td>
                <td><span class="dax-code-pill">{dax_html}</span></td>
                <td><span class="role-badge">{rolle_html}</span></td>
                <td>{link_html}</td>
              </tr>"""
        rows_html_list.append(row)

    all_rows_html = "\n".join(rows_html_list)

    # 6. Page glossary definition
    page_glossary_code = f"""
  page_glossary: {{
    id: "page_09_begrepskatalog",
    title: "09 Begrepskatalog & Metodikk",
    role: "Felles referanseramme: Controller, Dekan, Prosjektleder & Ledelse",
    desc: "Komplett ordbok og metodebeskrivelse for økonomistyring, SRS-regnskap, prognostisering og prosjektcontrolling (EVM) ved UiA. Inkluderer 60 definerte nøkkelbegreper med praktisk tolkning og tilhørende DAX-formler.",
    slicers: [
      {{ label: "Kategori", options: ["Alle kategorier", "01 Regnskap & Sektor", "02 Prosjektcontrolling (EVM)", "03 Prognose & Avvik", "04 Bemanning & Kapasitet", "05 Utdanningsproduksjon", "06 Omstilling & Tiltak", "07 RAG & Farger", "08 Teknisk & Modell"] }},
      {{ label: "Rollekontekst", options: ["Alle roller", "Controller", "Project Controller", "Dekan", "Instituttleder", "Ledelse / Styret"] }},
      {{ label: "Tilknyttet rapport", options: ["Alle rapporter", "01 Instituttleder", "02 Dekan & Fakultet", "03 Executive", "04 Styret", "05 Forskning & BOA", "06 Studieportefølje", "07 Action Tracker", "08 Controller Cockpit", "DT Prosjekt EVM", "DT Bilagslogg"] }}
    ],
    kpis: [
      {{ title: "Definerte begreper", val: "60", unit: "Begreper", badge: "DimGlossary", badgeCls: "variance-info", sub: "Fullstendig ordbok for UH-sektoren" }},
      {{ title: "Faglige kategorier", val: "8", unit: "Kategorier", badge: "Styringsakser", badgeCls: "variance-info", sub: "SRS, EVM, BOA, FTE, RAG" }},
      {{ title: "Sluttkostnad (EAC)", val: "36,79 M", unit: "NOK", badge: "LE_2026", badgeCls: "variance-unfavorable", sub: "Avvik mot BAC: +26,05 M" }},
      {{ title: "RAG Avviksnivåer", val: "3", unit: "Nivåer", badge: "🟢 Grønn | 🟡 Gul | 🔴 Rød", badgeCls: "variance-favorable", sub: "Terskel: <2% / 2-5% / >5%" }},
      {{ title: "Metodestandard", val: "DFØ SRS", unit: "R-102", badge: "Statlig regnskap", badgeCls: "variance-info", sub: "Periodisering & opptjening" }}
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
          <div class="method-formula">[Regnskap] = SUM(FactGL[Belop_signert])</div>
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
{all_rows_html}
            </tbody>
          </table>
        </div>
      </div>
    `
  }},
"""

    # If page_glossary already exists, replace it cleanly
    pattern = r"  page_glossary: \{.*?\}\},\n  page_dt_studier:"
    if re.search(pattern, html_content, re.DOTALL):
        html_content = re.sub(pattern, page_glossary_code.lstrip() + "  page_dt_studier:", html_content, flags=re.DOTALL)
        print("Replaced existing page_glossary in dashboards.")
    else:
        html_content = html_content.replace("  page_dt_studier: {", page_glossary_code + "  page_dt_studier: {")
        print("Injected page_glossary into dashboards.")

    # 7. JS Helpers
    js_helpers = """
// ============================================================================
// GLOSSARY CLIENT-SIDE INTERACTIVE FILTERING & SEARCH
// ============================================================================
let activeGlossaryCat = "ALL";
let activeGlossaryQuery = "";

function filterGlossaryCat(cat, btnElem) {
  activeGlossaryCat = cat;
  
  const btns = document.querySelectorAll("#glossaryCatPills .glossary-cat-btn");
  btns.forEach(b => b.classList.remove("active"));
  if (btnElem) btnElem.classList.add("active");
  
  applyGlossaryFilters();
}

function filterGlossarySearch(query) {
  activeGlossaryQuery = (query || "").toLowerCase().trim();
  applyGlossaryFilters();
}

function applyGlossaryFilters() {
  const rows = document.querySelectorAll("#glossaryMainTable tbody tr.glossary-row");
  let visible = 0;
  
  rows.forEach(row => {
    const rowCat = row.getAttribute("data-cat") || "";
    const rowSearch = row.getAttribute("data-search") || "";
    
    const catMatch = (activeGlossaryCat === "ALL") || (rowCat === activeGlossaryCat);
    const searchMatch = (!activeGlossaryQuery) || (rowSearch.includes(activeGlossaryQuery));
    
    if (catMatch && searchMatch) {
      row.style.display = "";
      visible++;
    } else {
      row.style.display = "none";
    }
  });
  
  const countEl = document.getElementById("glossaryVisibleCount");
  if (countEl) countEl.textContent = visible;
}
"""

    if "function filterGlossaryCat" not in html_content:
        target_js = 'document.getElementById("globalSearch").addEventListener'
        html_content = html_content.replace(target_js, js_helpers + "\n" + target_js)
        print("Injected glossary JS filtering helpers.")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Successfully rewritten index.html with bulletproof escaping!")

if __name__ == "__main__":
    main()
