# -*- coding: utf-8 -*-
"""
test_rapportering_skills.py
----------------------------
Test suite for UiA Controller & Rapportering skills.
Directly invokes the compliance audit from verify_reporting_rules.py and executes
all regulatory tests (KD 2025 SPE satser, SRS 1/9/10/17, 5%-regelen F-05-20,
TDI-modellen, Lønnsandel, EVM & RAG risikostyring).
"""

import os
import sys

# Ensure UTF-8 output
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add skill script to path
skill_script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "rapportering skills", "scripts"))
if skill_script_dir not in sys.path:
    sys.path.insert(0, skill_script_dir)

from verify_reporting_rules import run_compliance_audit

if __name__ == "__main__":
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    code = run_compliance_audit(data_dir=data_dir)
    sys.exit(code)
