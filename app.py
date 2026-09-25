# -*- coding: utf-8 -*-
"""
AI Controller App - Standalone Web Application
Multi-Agent Controller Suite (Diagnose, Prognose, Prescribe)
Compatible with raw CSVs, DuckDB, scikit-learn, and APIs from .env:
- OpenRouter
- Google Gemini
- GitHub Models / Copilot
- Hugging Face
- Ollama
- Deterministic ML Fallback
"""

import os
import sys
import json
import socket
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# Import AI Controller Engine
from scripts.ai_engine import (
    ControllerDataRepository,
    MLForecastEngine,
    AIAgentOrchestrator,
    load_env_file
)

# Global instances
REPO = ControllerDataRepository("data")
ML_ENGINE = MLForecastEngine(REPO)
ORCHESTRATOR = AIAgentOrchestrator(REPO, ML_ENGINE)

# Initialize standard tables on startup
try:
    INITIAL_TABLES = REPO.load_all_standard_tables()
    print(f"Loaded {len(INITIAL_TABLES)} tables into DuckDB.")
except Exception as e:
    print(f"Startup table load notice: {e}")
    INITIAL_TABLES = {}


HTML_PAGE = """<!DOCTYPE html>
<html lang="no">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Multi-Agent Controller Hub | Diagnose, Prognose & Preskripsjon</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-primary: #0a0e17;
      --bg-secondary: #0f172a;
      --bg-card: #131d33;
      --bg-card-hover: #182440;
      --bg-elevated: #1e293b;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-strong: rgba(255, 255, 255, 0.16);
      --border-accent: rgba(59, 130, 246, 0.4);
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      --text-accent: #38bdf8;
      --color-green: #10b981;
      --color-green-bg: rgba(16, 185, 129, 0.12);
      --color-amber: #f59e0b;
      --color-amber-bg: rgba(245, 158, 11, 0.12);
      --color-red: #ef4444;
      --color-red-bg: rgba(239, 68, 68, 0.12);
      --color-blue: #3b82f6;
      --color-blue-bg: rgba(59, 130, 246, 0.12);
      --color-purple: #a855f7;
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-display: 'Outfit', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
      --radius-sm: 4px;
      --radius-md: 8px;
      --radius-lg: 12px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg-primary);
      color: var(--text-primary);
      font-family: var(--font-sans);
      font-size: 13px;
      line-height: 1.5;
      padding-bottom: 60px;
    }

    header {
      background: var(--bg-secondary);
      border-bottom: 1px solid var(--border-subtle);
      padding: 16px 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 100;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-logo {
      width: 36px;
      height: 36px;
      background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%);
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      color: #fff;
    }
    .brand-title h1 {
      font-family: var(--font-display);
      font-size: 16px;
      font-weight: 600;
      letter-spacing: -0.2px;
    }
    .brand-title p {
      font-size: 11px;
      color: var(--text-secondary);
    }

    .status-bar {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 9px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 500;
      border: 1px solid transparent;
    }
    .badge-live {
      background: var(--color-green-bg);
      color: var(--color-green);
      border-color: rgba(16, 185, 129, 0.3);
    }
    .badge-active-ai {
      background: rgba(99, 102, 241, 0.15);
      color: #a5b4fc;
      border-color: rgba(99, 102, 241, 0.3);
    }

    .btn {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      padding: 8px 14px;
      border-radius: var(--radius-md);
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
      font-family: var(--font-sans);
    }
    .btn:hover {
      background: var(--bg-card-hover);
      border-color: var(--border-strong);
    }
    .btn-primary {
      background: #0284c7;
      border-color: #0284c7;
      color: #fff;
    }
    .btn-primary:hover { background: #0369a1; }
    .btn-purple {
      background: #4f46e5;
      border-color: #4f46e5;
      color: #fff;
    }
    .btn-purple:hover { background: #4338ca; }

    .main-wrap {
      max-width: 1600px;
      margin: 24px auto;
      padding: 0 24px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    /* Top Grid: KPI Cards */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 14px;
    }
    .kpi-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .kpi-title {
      font-size: 11px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      font-weight: 600;
    }
    .kpi-val {
      font-family: var(--font-display);
      font-size: 24px;
      font-weight: 700;
      margin: 4px 0;
      font-variant-numeric: tabular-nums;
    }
    .kpi-sub {
      font-size: 11px;
      color: var(--text-secondary);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* Controls Bar */
    .controls-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 14px 20px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
    }
    .controls-group {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }
    .select-input {
      background: var(--bg-secondary);
      border: 1px solid var(--border-strong);
      color: var(--text-primary);
      padding: 6px 12px;
      border-radius: var(--radius-md);
      font-size: 12px;
      outline: none;
    }

    /* 3-Agent Section Stepper */
    .agent-pipeline-grid {
      display: grid;
      grid-template-columns: 1fr 1.3fr 1.2fr;
      gap: 16px;
    }

    .agent-box {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    .agent-header {
      padding: 14px 18px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(255, 255, 255, 0.02);
    }
    .agent-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-family: var(--font-display);
      font-size: 14px;
      font-weight: 600;
    }
    .agent-badge {
      font-size: 10px;
      padding: 2px 7px;
      border-radius: 4px;
      font-weight: 600;
    }
    .agent-body {
      padding: 18px;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    /* Edward Tufte Data-Ink Tables */
    table.tufte-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
    }
    table.tufte-table th {
      background: rgba(255, 255, 255, 0.02);
      color: var(--text-muted);
      font-weight: 600;
      font-size: 10.5px;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      padding: 8px 10px;
      border-bottom: 1px solid var(--border-strong);
      text-align: left;
    }
    table.tufte-table th.num, table.tufte-table td.num {
      text-align: right;
      font-variant-numeric: tabular-nums;
    }
    table.tufte-table td {
      padding: 8px 10px;
      border-bottom: 1px solid var(--border-subtle);
      color: var(--text-secondary);
    }
    table.tufte-table tr:hover td {
      background: rgba(255, 255, 255, 0.02);
      color: var(--text-primary);
    }

    /* Status Pills */
    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 2px 7px;
      border-radius: 9999px;
      font-size: 10px;
      font-weight: 600;
    }
    .rag-green { background: var(--color-green-bg); color: var(--color-green); }
    .rag-amber { background: var(--color-amber-bg); color: var(--color-amber); }
    .rag-red { background: var(--color-red-bg); color: var(--color-red); }

    /* SVG Chart Containers */
    .chart-container {
      width: 100%;
      height: 260px;
      position: relative;
    }
    svg.interactive-chart {
      width: 100%;
      height: 100%;
      overflow: visible;
    }

    .analysis-text-box {
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 12px 14px;
      font-size: 11.5px;
      line-height: 1.6;
      color: #cbd5e1;
      max-height: 240px;
      overflow-y: auto;
      white-space: pre-wrap;
      font-family: var(--font-sans);
    }

    /* CSV Upload Modal / Section */
    .raw-data-panel {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 16px 20px;
    }
    .raw-table-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 10px;
    }
    .table-chip {
      background: var(--bg-secondary);
      border: 1px solid var(--border-subtle);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-family: var(--font-mono);
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .table-chip span {
      color: #38bdf8;
      font-weight: 600;
    }

    @media (max-width: 1200px) {
      .kpi-grid { grid-template-columns: repeat(2, 1fr); }
      .agent-pipeline-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>

  <header>
    <div class="brand">
      <div class="brand-logo">AI</div>
      <div class="brand-title">
        <h1>AI Multi-Agent Controller Hub</h1>
        <p>Diagnose, Prognose & Preskripsjon | Støtter Google Gemini, Copilot, Hugging Face & Lokal Ollama</p>
      </div>
    </div>

    <div class="status-bar">
      <span class="badge badge-live">DuckDB In-Memory Aktiv</span>
      <span class="badge badge-active-ai" id="activeProviderBadge">Laster KI-motor...</span>
      <button class="btn btn-primary" onclick="runCompletePipeline()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
        Kjør 3-Agent Syklus
      </button>
      <a href="index.html" class="btn" target="_blank">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
        Rapporteringsportal
      </a>
    </div>
  </header>

  <main class="main-wrap">

    <!-- KPI SUMMARY ROW -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-title">Regnskap YTD</div>
        <div class="kpi-val" id="kpiActual">10,62 M</div>
        <div class="kpi-sub">Budsjett YTD: <span id="kpiBudget">10,75 M</span></div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Helårsprognose (EAC)</div>
        <div class="kpi-val" style="color: #f59e0b;" id="kpiEAC">36,79 M</div>
        <div class="kpi-sub">Budsjettramme: 10,75 M</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Prognosert Sluttavvik (VAC)</div>
        <div class="kpi-val" style="color: #ef4444;" id="kpiVAC">+26,05 M</div>
        <div class="kpi-sub">Ugunstig merforbruk før tiltak</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">ML Modellkonfidens (R²)</div>
        <div class="kpi-val" style="color: #38bdf8;" id="kpiR2">94,2%</div>
        <div class="kpi-sub">Ridge & Eksponentiell trend</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">EVM Prosjektindeks</div>
        <div class="kpi-val" id="kpiCPI">0.88 CPI</div>
        <div class="kpi-sub">SPI: 0.94 (Tidsforsinkelse BOA)</div>
      </div>
    </div>

    <!-- CONTROLS & MODEL PROVIDER BAR -->
    <div class="controls-card">
      <div class="controls-group">
        <label style="font-weight: 600; color: var(--text-secondary);">KI Leverandør / LLM:</label>
        <select class="select-input" id="providerSelect" onchange="updateProviderSelection()">
          <option value="auto">Auto (Beste tilgjengelige fra .env)</option>
          <option value="openrouter">OpenRouter (DeepSeek R1 / Llama-3.3)</option>
          <option value="gemini">Google Gemini 1.5/2.0 Flash</option>
          <option value="github">GitHub Models / Copilot</option>
          <option value="ollama">Ollama (Lokal & Konfidensiell)</option>
          <option value="huggingface">Hugging Face Inference</option>
          <option value="deterministic_ml">Deterministisk ML Fallback (Lokal)</option>
        </select>

        <label style="font-weight: 600; color: var(--text-secondary); margin-left: 12px;">Fokusområde:</label>
        <select class="select-input" id="focusSelect">
          <option value="all">Hele Institusjonen (Total)</option>
          <option value="salary">Lønn & Årsverk (UF/TA)</option>
          <option value="boa">BOA & Eksternfinansierte Prosjekter</option>
          <option value="operations">Driftskostnader & Konsulenter</option>
        </select>
      </div>

      <div class="controls-group">
        <button class="btn" onclick="document.getElementById('csvFileInput').click()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
          Last opp rå CSV
        </button>
        <input type="file" id="csvFileInput" style="display: none;" accept=".csv" onchange="uploadCSV(this)">
        <button class="btn btn-purple" onclick="exportPrescriptionsToFactAction()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
          Synk Preskripsjoner til FactAction.csv
        </button>
      </div>
    </div>

    <!-- TRI-AGENT PIPELINE CARDS -->
    <div class="agent-pipeline-grid">

      <!-- AGENT 1: DIAGNOSE -->
      <div class="agent-box">
        <div class="agent-header">
          <div class="agent-title">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            1. Diagnose Agent
          </div>
          <span class="agent-badge" style="background: var(--color-red-bg); color: var(--color-red);">Avvik & Årsak</span>
        </div>
        <div class="agent-body">
          <div>
            <div style="font-weight: 600; font-size: 11px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 6px;">
              Hovedavviksdrivere (MNOK)
            </div>
            <table class="tufte-table">
              <thead>
                <tr>
                  <th>Kostnadskategori</th>
                  <th class="num">Avvik</th>
                  <th class="num">Andel</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody id="diagnoseDriversTable">
                <tr>
                  <td>Lønn UF/TA (5000-5899)</td>
                  <td class="num" style="color: #ef4444;">+18,20 M</td>
                  <td class="num">69,8%</td>
                  <td><span class="status-pill rag-red">Kritisk</span></td>
                </tr>
                <tr>
                  <td>Driftskostnader (6000-7999)</td>
                  <td class="num" style="color: #f59e0b;">+5,40 M</td>
                  <td class="num">20,7%</td>
                  <td><span class="status-pill rag-amber">Vurder</span></td>
                </tr>
                <tr>
                  <td>Avskrivninger & IT</td>
                  <td class="num" style="color: #f59e0b;">+2,10 M</td>
                  <td class="num">8,1%</td>
                  <td><span class="status-pill rag-amber">Vurder</span></td>
                </tr>
                <tr>
                  <td>Inntektsbortfall (BOA)</td>
                  <td class="num" style="color: #10b981;">+0,35 M</td>
                  <td class="num">1,4%</td>
                  <td><span class="status-pill rag-green">Lav</span></td>
                </tr>
              </tbody>
            </table>
          </div>

          <div>
            <div style="font-weight: 600; font-size: 11px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 6px;">
              Rotårsaksanalyse (Agent Reasoning)
            </div>
            <div class="analysis-text-box" id="diagnoseReasoning">Laster diagnose fra agent...</div>
          </div>
        </div>
      </div>

      <!-- AGENT 2: PROGNOSE -->
      <div class="agent-box">
        <div class="agent-header">
          <div class="agent-title">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
            2. Prognose Agent
          </div>
          <span class="agent-badge" style="background: rgba(56,189,248,0.15); color: #38bdf8;">ML Fan Chart</span>
        </div>
        <div class="agent-body">
          <div class="chart-container">
            <svg class="interactive-chart" id="mlForecastSVG" viewBox="0 0 480 220">
              <!-- S-Curve Fan Chart will be drawn by JS -->
            </svg>
          </div>

          <div>
            <div style="font-weight: 600; font-size: 11px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 6px;">
              ML Konfidensspenn & Budsjettbrudd
            </div>
            <div class="analysis-text-box" id="prognoseReasoning">Laster prognose og konfidensberegning...</div>
          </div>
        </div>
      </div>

      <!-- AGENT 3: PRESCRIBE -->
      <div class="agent-box">
        <div class="agent-header">
          <div class="agent-title">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            3. Prescribe Agent
          </div>
          <span class="agent-badge" style="background: var(--color-green-bg); color: var(--color-green);">Styringstiltak</span>
        </div>
        <div class="agent-body">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <span style="font-weight: 600; font-size: 11px; text-transform: uppercase; color: var(--text-muted);">
                Anbefalte Tiltak (FactAction)
              </span>
              <span style="font-size: 11px; color: #10b981; font-weight: 600;" id="totalPrescribedEffect">-10,25 MNOK</span>
            </div>
            <table class="tufte-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Tiltak</th>
                  <th>Rolle</th>
                  <th class="num">Effekt</th>
                </tr>
              </thead>
              <tbody id="prescriptionsTableBody">
                <!-- Injected by JS -->
              </tbody>
            </table>
          </div>

          <div>
            <div style="font-weight: 600; font-size: 11px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 6px;">
              Preskriptiv Vurdering & Prioritering
            </div>
            <div class="analysis-text-box" id="prescribeReasoning">Laster anbefalte styringstiltak fra agent...</div>
          </div>
        </div>
      </div>

    </div>

    <!-- RAW CSV INGESTION & DATASET STATUS -->
    <div class="raw-data-panel">
      <div style="display: flex; align-items: center; justify-content: space-between;">
        <div>
          <h3 style="font-family: var(--font-display); font-size: 14px; font-weight: 600; color: #fff;">
            Tilknyttet Rådatastruktur (DuckDB In-Memory)
          </h3>
          <p style="font-size: 11px; color: var(--text-secondary);">
            Automatisert skjema- og semikolondeteksjon for statlig DFØ SRS regnskaps- og prognosedata
          </p>
        </div>
        <button class="btn" onclick="fetchDatasetStatus()">Oppfrisk Tabellstatus</button>
      </div>

      <div class="raw-table-chips" id="tableChipsContainer">
        <!-- Injected by JS -->
      </div>
    </div>

  </main>

  <script>
    let currentPrescriptions = [];

    async function fetchDatasetStatus() {
      try {
        const res = await fetch('/api/status');
        const data = await res.json();

        // Update provider badge
        const badge = document.getElementById('activeProviderBadge');
        if (data.providers) {
          const avail = Object.keys(data.providers).filter(k => data.providers[k]);
          badge.textContent = "KI: " + avail.slice(0, 3).join(', ');
        }

        // Update table chips
        const chipContainer = document.getElementById('tableChipsContainer');
        chipContainer.innerHTML = '';
        if (data.tables) {
          for (const [tbl, count] of Object.entries(data.tables)) {
            const chip = document.createElement('div');
            chip.className = 'table-chip';
            chip.innerHTML = `${tbl}: <span>${new Intl.NumberFormat('no-NO').format(count)}</span> rader`;
            chipContainer.appendChild(chip);
          }
        }
      } catch (err) {
        console.error('Status fetch error:', err);
      }
    }

    async function fetchMLForecast() {
      try {
        const res = await fetch('/api/ml_forecast');
        const ml = await res.json();

        document.getElementById('kpiEAC').textContent = ml.eac_point_mnok.toFixed(2).replace('.', ',') + " M";
        document.getElementById('kpiVAC').textContent = (ml.variance_at_completion_mnok > 0 ? "+" : "") + ml.variance_at_completion_mnok.toFixed(2).replace('.', ',') + " M";
        document.getElementById('kpiR2').textContent = (ml.confidence_score_r2 * 100).toFixed(1).replace('.', ',') + "%";

        renderForecastSVG(ml.timeline);
      } catch (err) {
        console.error('ML fetch error:', err);
      }
    }

    function renderForecastSVG(timeline) {
      const svg = document.getElementById('mlForecastSVG');
      if (!timeline || timeline.length === 0) return;

      const w = 480, h = 220, padLeft = 40, padRight = 30, padTop = 20, padBottom = 30;
      const plotW = w - padLeft - padRight;
      const plotH = h - padTop - padBottom;

      const maxVal = 42; // MNOK scale
      const numPoints = timeline.length;

      const getX = i => padLeft + (i / (numPoints - 1)) * plotW;
      const getY = v => padTop + plotH - (v / maxVal) * plotH;

      // Build SVG paths
      // 1. Budget Baseline
      let budgetD = timeline.map((pt, i) => `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(pt.budget_ytd)}`).join(' ');

      // 2. Official LE / ML Point
      let mlD = timeline.map((pt, i) => `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(pt.official_le)}`).join(' ');

      // 3. 95% Confidence Fan Area
      let fanTop = timeline.map((pt, i) => `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(pt.upper_95)}`).join(' ');
      let fanBottom = timeline.slice().reverse().map(pt => `L ${getX(pt.month_num - 1)} ${getY(pt.lower_95)}`).join(' ');
      let fanD = `${fanTop} ${fanBottom} Z`;

      // 4. Actuals (up to observed months)
      let actualD = timeline.map((pt, i) => `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(pt.actual_ytd)}`).join(' ');

      svg.innerHTML = `
        <defs>
          <linearGradient id="fanGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.05" />
            <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.25" />
          </linearGradient>
        </defs>

        <!-- Horizontal Guides (Tufte muted) -->
        <line x1="${padLeft}" y1="${getY(10)}" x2="${w - padRight}" y2="${getY(10)}" stroke="rgba(255,255,255,0.06)" />
        <line x1="${padLeft}" y1="${getY(20)}" x2="${w - padRight}" y2="${getY(20)}" stroke="rgba(255,255,255,0.06)" />
        <line x1="${padLeft}" y1="${getY(30)}" x2="${w - padRight}" y2="${getY(30)}" stroke="rgba(255,255,255,0.06)" />

        <text x="${padLeft - 6}" y="${getY(10) + 3}" fill="#64748b" font-size="9" text-anchor="end">10M</text>
        <text x="${padLeft - 6}" y="${getY(20) + 3}" fill="#64748b" font-size="9" text-anchor="end">20M</text>
        <text x="${padLeft - 6}" y="${getY(30) + 3}" fill="#64748b" font-size="9" text-anchor="end">30M</text>

        <!-- Fan Confidence Cone -->
        <path d="${fanD}" fill="url(#fanGrad)" />

        <!-- Lines -->
        <path d="${budgetD}" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4" />
        <path d="${mlD}" fill="none" stroke="#f59e0b" stroke-width="2.5" />
        <path d="${actualD}" fill="none" stroke="#38bdf8" stroke-width="2" />

        <!-- Direct Labels (Edward Tufte Principle) -->
        <text x="${getX(numPoints - 1) + 4}" y="${getY(timeline[numPoints - 1].budget_ytd) + 3}" fill="#94a3b8" font-size="10" font-weight="600">Budsjett (10,75M)</text>
        <text x="${getX(numPoints - 1) + 4}" y="${getY(timeline[numPoints - 1].official_le) + 3}" fill="#f59e0b" font-size="10" font-weight="700">EAC (36,79M)</text>
        <text x="${getX(numPoints - 1) + 4}" y="${getY(timeline[numPoints - 1].upper_95) + 3}" fill="#38bdf8" font-size="9">P90 (41,2M)</text>

        <!-- Month ticks -->
        ${timeline.map((pt, i) => `
          <text x="${getX(i)}" y="${h - 10}" fill="#64748b" font-size="9" text-anchor="middle">${pt.month}</text>
        `).join('')}
      `;
    }

    async function runCompletePipeline() {
      const provider = document.getElementById('providerSelect').value;
      const btn = event?.target;
      if (btn) btn.disabled = true;

      document.getElementById('diagnoseReasoning').textContent = "Agent 1: Kjører avviksanalyse...";
      document.getElementById('prognoseReasoning').textContent = "Agent 2: Beregner ML-bane og konfidens...";
      document.getElementById('prescribeReasoning').textContent = "Agent 3: Formulerer styringstiltak...";

      try {
        const res = await fetch('/api/run_pipeline', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ provider })
        });
        const data = await res.json();

        // 1. Diagnose
        if (data.diagnose) {
          document.getElementById('diagnoseReasoning').textContent = data.diagnose.analysis_text;
        }

        // 2. Prognose
        if (data.prognose) {
          document.getElementById('prognoseReasoning').textContent = data.prognose.analysis_text;
          if (data.prognose.ml_data) {
            renderForecastSVG(data.prognose.ml_data.timeline);
          }
        }

        // 3. Prescribe
        if (data.prescribe) {
          document.getElementById('prescribeReasoning').textContent = data.prescribe.analysis_text;
          currentPrescriptions = data.prescribe.prescriptions || [];
          document.getElementById('totalPrescribedEffect').textContent = data.prescribe.total_effect_mnok.toFixed(2) + " MNOK";

          const tbody = document.getElementById('prescriptionsTableBody');
          tbody.innerHTML = '';
          currentPrescriptions.forEach(p => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
              <td><code>${p.TiltakID}</code></td>
              <td>${p.Tiltaksbeskrivelse}</td>
              <td>${p.AnsvarligRolle}</td>
              <td class="num" style="color: #10b981; font-weight: 600;">${new Intl.NumberFormat('no-NO').format(p.ForventetEffekt)} kr</td>
            `;
            tbody.appendChild(tr);
          });
        }

      } catch (err) {
        console.error('Pipeline error:', err);
        alert('Feil ved kjøring av agent-syklus: ' + err.message);
      } finally {
        if (btn) btn.disabled = false;
      }
    }

    async function exportPrescriptionsToFactAction() {
      if (!currentPrescriptions || currentPrescriptions.length === 0) {
        alert("Kjør først agent-syklusen for å generere preskripsjoner.");
        return;
      }

      try {
        const res = await fetch('/api/export_actions', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prescriptions: currentPrescriptions })
        });
        const resData = await res.json();
        alert(`Suksess! ${resData.added_count} nye tiltak er lagt til i data/FactAction.csv og klar for Power BI.`);
        fetchDatasetStatus();
      } catch (err) {
        console.error('Export error:', err);
        alert('Eksportfeil: ' + err.message);
      }
    }

    function uploadCSV(input) {
      const file = input.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = async (e) => {
        const content = e.target.result;
        try {
          const res = await fetch('/api/upload_csv', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename: file.name, content: content })
          });
          const result = await res.json();
          alert(`Fil ${file.name} lastet inn i DuckDB (${result.rows} rader).`);
          fetchDatasetStatus();
          fetchMLForecast();
        } catch (err) {
          alert('Opplastingsfeil: ' + err.message);
        }
      };
      reader.readAsText(file, 'utf-8');
    }

    function updateProviderSelection() {
      // triggers on select change
    }

    // Init on page load
    window.addEventListener('DOMContentLoaded', () => {
      fetchDatasetStatus();
      fetchMLForecast();
      runCompletePipeline();
    });
  </script>
</body>
</html>
"""


# ==============================================================================
# HTTP REQUEST HANDLER
# ==============================================================================
class ControllerRequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self, content_type: str = "application/json", status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(status=204)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ["/", "/index.html", "/portal"]:
            index_path = Path(__file__).parent / "index.html"
            if index_path.exists():
                with open(index_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self._set_headers("text/html")
                self.wfile.write(content.encode("utf-8"))
            else:
                self._set_headers("text/html")
                self.wfile.write(HTML_PAGE.encode("utf-8"))

        elif path in ["/ai_hub", "/hub", "/agent_hub"]:
            self._set_headers("text/html")
            self.wfile.write(HTML_PAGE.encode("utf-8"))

        elif path == "/api/status":
            tables = {name: len(df) for name, df in REPO.tables.items()}
            providers = ORCHESTRATOR.get_available_providers()
            self._set_headers("application/json")
            self.wfile.write(json.dumps({
                "status": "online",
                "tables": tables,
                "providers": providers
            }).encode("utf-8"))

        elif path == "/api/summary":
            summary = REPO.get_summary_metrics()
            self._set_headers("application/json")
            self.wfile.write(json.dumps(summary).encode("utf-8"))

        elif path == "/api/ml_forecast":
            ml = ML_ENGINE.generate_monthly_forecast()
            self._set_headers("application/json")
            self.wfile.write(json.dumps(ml).encode("utf-8"))

        elif path == "/api/use_cases":
            use_cases = ORCHESTRATOR.get_use_cases_data()
            self._set_headers("application/json")
            self.wfile.write(json.dumps(use_cases, default=str).encode("utf-8"))

        elif path == "/api/boa_projects":
            boa = ORCHESTRATOR.get_boa_projects()
            self._set_headers("application/json")
            self.wfile.write(json.dumps(boa, default=str).encode("utf-8"))

        elif path == "/api/study_points":
            sp = ORCHESTRATOR.get_study_points_summary()
            self._set_headers("application/json")
            self.wfile.write(json.dumps(sp, default=str).encode("utf-8"))

        elif path == "/api/forecast_hybrid":
            ml = ML_ENGINE.generate_monthly_forecast()
            self._set_headers("application/json")
            self.wfile.write(json.dumps({
                "rolling_12m_timeline": ml.get("rolling_12m_timeline", ml.get("timeline", [])),
                "eac_point_estimate_mnok": ml.get("eac_point_estimate_mnok", ml.get("eac_point_mnok", 0)),
                "r2_score": ml.get("r2_score", ml.get("confidence_score_r2", 0)),
                "forecast_bias_index": ml.get("forecast_bias_index", 0),
                "p10_mnok": ml.get("p10_mnok", ml.get("p10_optimistic_mnok", 0)),
                "p50_mnok": ml.get("p50_mnok", ml.get("p50_base_mnok", 0)),
                "p90_mnok": ml.get("p90_mnok", ml.get("p90_pessimistic_mnok", 0)),
                "budget_breach_month": ml.get("budget_breach_month", "M10")
            }, default=str).encode("utf-8"))

        else:
            self._set_headers("text/plain", 404)
            self.wfile.write(b"Not Found")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"

        try:
            body_data = json.loads(post_body)
        except Exception:
            body_data = {}

        if path == "/api/run_pipeline":
            provider = body_data.get("provider", "auto")
            pipeline_res = ORCHESTRATOR.run_full_pipeline(provider)
            self._set_headers("application/json")
            self.wfile.write(json.dumps(pipeline_res).encode("utf-8"))

        elif path == "/api/export_actions":
            prescriptions = body_data.get("prescriptions", [])
            added = ORCHESTRATOR.export_prescriptions_to_fact_action(prescriptions)
            self._set_headers("application/json")
            self.wfile.write(json.dumps({"success": True, "added_count": added}).encode("utf-8"))

        elif path == "/api/upload_csv":
            filename = body_data.get("filename", "Uploaded.csv")
            content = body_data.get("content", "")
            # Save into data/
            dest = Path("data") / filename
            with open(dest, "w", encoding="utf-8") as f:
                f.write(content)
            # Register in DuckDB
            df = REPO.load_raw_csv(str(dest), dest.stem)
            self._set_headers("application/json")
            self.wfile.write(json.dumps({"success": True, "table": dest.stem, "rows": len(df)}).encode("utf-8"))

        else:
            self._set_headers("text/plain", 404)
            self.wfile.write(b"Not Found")


def run_server(port: int = 8088):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, ControllerRequestHandler)
    print(f"============================================================")
    print(f"  AI Multi-Agent Controller Hub is running at:")
    print(f"  --> http://127.0.0.1:{port}")
    print(f"  Supported Providers: OpenRouter, Gemini, GitHub, Ollama, HF")
    print(f"============================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()


if __name__ == "__main__":
    port = 8088
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)
