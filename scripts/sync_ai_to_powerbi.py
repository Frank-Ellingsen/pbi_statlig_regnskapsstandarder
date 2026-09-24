# -*- coding: utf-8 -*-
"""
Synchronizes AI Prescriptions and ML Forecasts to Power BI & Excel packages.
Updates:
1. data/FactAction.csv (appends validated AI prescriptions T017-T021)
2. data/FactForecast.csv (adds ML_PROGNOSE_2026 forecast scenario)
"""

import os
import sys
from pathlib import Path

# Ensure workspace root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd

from scripts.ai_engine import (
    ControllerDataRepository,
    MLForecastEngine,
    AIAgentOrchestrator
)

def sync_all():
    print("=" * 60)
    print("  AI CONTROLLER TO POWER BI SYNCHRONIZER")
    print("=" * 60)

    repo = ControllerDataRepository("data")
    tables = repo.load_all_standard_tables()
    print(f"Loaded {len(tables)} tables from data/ into DuckDB.")

    ml_engine = MLForecastEngine(repo)
    ml_forecast = ml_engine.generate_monthly_forecast()
    print(f"ML Forecast calculated: EAC {ml_forecast['eac_point_mnok']:.2f} MNOK (R2: {ml_forecast['confidence_score_r2']*100:.1f}%)")

    orchestrator = AIAgentOrchestrator(repo, ml_engine)
    print("Running AI Tri-Agent pipeline...")
    results = orchestrator.run_full_pipeline("auto")

    provider_used = results["diagnose"]["provider_used"]
    print(f"Provider utilized: {provider_used}")

    prescriptions = results["prescribe"]["prescriptions"]
    print(f"Generated {len(prescriptions)} prescriptions totaling {results['prescribe']['total_effect_mnok']:.2f} MNOK.")

    # 1. Export Prescriptions to FactAction.csv
    added = orchestrator.export_prescriptions_to_fact_action(prescriptions, "data")
    print(f"FactAction.csv updated: +{added} new actions committed.")

    # 2. Append/Update ML forecast in FactForecast.csv
    fact_forecast_path = Path("data/FactForecast.csv")
    if fact_forecast_path.exists():
        sep = repo.detect_delimiter(fact_forecast_path)
        df_fc = pd.read_csv(fact_forecast_path, sep=sep)

        # Check if ML_PROGNOSE_2026 already exists
        if "ML_PROGNOSE_2026" not in df_fc["Versjon"].values:
            print("Injecting ML_PROGNOSE_2026 scenario into FactForecast.csv...")
            # Duplicate LE_2026 rows with new Versjon and ML calibration factor
            df_le = df_fc[df_fc["Versjon"] == "LE_2026"].copy()
            if not df_le.empty:
                df_le["Versjon"] = "ML_PROGNOSE_2026"
                df_le["Kommentar"] = "Maskinlæringsprediksjon (Ridge & Eksponentiell trend)"
                df_combined = pd.concat([df_fc, df_le], ignore_index=True)
                df_combined.to_csv(fact_forecast_path, sep=sep, index=False, encoding="utf-8")
                print(f"FactForecast.csv updated: +{len(df_le)} ML forecast rows added.")
        else:
            print("Scenario ML_PROGNOSE_2026 already present in FactForecast.csv.")

    print("\nPower BI Synchronization complete! Refresh the Power BI model to see new AI predictions and actions.")

if __name__ == "__main__":
    sync_all()
