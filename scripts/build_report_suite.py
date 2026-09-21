"""
build_report_suite.py
---------------------
Generates the complete UiA Controller Reporting Suite in Power BI Enhanced Report Format (PBIR).
Tailored for each stakeholder according to PBI_Layout.txt and Edward Tufte's Data-Ink Ratio standards.
"""

import os
import shutil
import json
import subprocess

REPORT_DIR = r"C:\Users\frank\Desktop\UIA\uia_powerbi_complete_forecast_model\UIA-Controller-Prosjekt.Report"
PAGES_DIR = os.path.join(REPORT_DIR, "definition", "pages")
SCHEMA_VC = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.0.0/schema.json"
SCHEMA_PAGE = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json"
SCHEMA_PAGES = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json"

def make_title(title_text):
    return {
        "title": [
            {
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "true"}}},
                    "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}}
                }
            }
        ]
    }

def create_card(name, x, y, width, height, z, measure_name, title_text=None, entity="_Measures"):
    vco = make_title(title_text) if title_text else {}
    return {
        "$schema": SCHEMA_VC,
        "name": name,
        "position": {"x": x, "y": y, "z": z, "width": width, "height": height, "tabOrder": z},
        "visual": {
            "visualType": "card",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [
                            {
                                "field": {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Entity": entity}},
                                        "Property": measure_name
                                    }
                                },
                                "queryRef": f"{entity}.{measure_name}",
                                "nativeQueryRef": measure_name
                            }
                        ]
                    }
                }
            },
            "visualContainerObjects": vco
        }
    }

def create_slicer(name, x, y, width, height, z, entity, column_name, title_text=None):
    vco = make_title(title_text) if title_text else {}
    return {
        "$schema": SCHEMA_VC,
        "name": name,
        "position": {"x": x, "y": y, "z": z, "width": width, "height": height, "tabOrder": z},
        "visual": {
            "visualType": "slicer",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [
                            {
                                "field": {
                                    "Column": {
                                        "Expression": {"SourceRef": {"Entity": entity}},
                                        "Property": column_name
                                    }
                                },
                                "queryRef": f"{entity}.{column_name}",
                                "nativeQueryRef": column_name
                            }
                        ]
                    }
                }
            },
            "visualContainerObjects": vco
        }
    }

def create_line_chart(name, x, y, width, height, z, cat_entity, cat_column, measures, title_text=None):
    y_projections = []
    for m in measures:
        entity = m.get("entity", "_Measures")
        prop = m["property"]
        y_projections.append({
            "field": {
                "Measure": {
                    "Expression": {"SourceRef": {"Entity": entity}},
                    "Property": prop
                }
            },
            "queryRef": f"{entity}.{prop}",
            "nativeQueryRef": prop
        })
    
    vco = make_title(title_text) if title_text else {}
    return {
        "$schema": SCHEMA_VC,
        "name": name,
        "position": {"x": x, "y": y, "z": z, "width": width, "height": height, "tabOrder": z},
        "visual": {
            "visualType": "lineChart",
            "query": {
                "queryState": {
                    "Category": {
                        "projections": [
                            {
                                "field": {
                                    "Column": {
                                        "Expression": {"SourceRef": {"Entity": cat_entity}},
                                        "Property": cat_column
                                    }
                                },
                                "queryRef": f"{cat_entity}.{cat_column}",
                                "nativeQueryRef": cat_column
                            }
                        ]
                    },
                    "Y": {
                        "projections": y_projections
                    }
                }
            },
            "visualContainerObjects": vco
        }
    }

def create_bar_chart(name, x, y, width, height, z, cat_entity, cat_column, measure_name, title_text=None, entity="_Measures"):
    vco = make_title(title_text) if title_text else {}
    return {
        "$schema": SCHEMA_VC,
        "name": name,
        "position": {"x": x, "y": y, "z": z, "width": width, "height": height, "tabOrder": z},
        "visual": {
            "visualType": "clusteredBarChart",
            "query": {
                "queryState": {
                    "Category": {
                        "projections": [
                            {
                                "field": {
                                    "Column": {
                                        "Expression": {"SourceRef": {"Entity": cat_entity}},
                                        "Property": cat_column
                                    }
                                },
                                "queryRef": f"{cat_entity}.{cat_column}",
                                "nativeQueryRef": cat_column
                            }
                        ]
                    },
                    "Y": {
                        "projections": [
                            {
                                "field": {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Entity": entity}},
                                        "Property": measure_name
                                    }
                                },
                                "queryRef": f"{entity}.{measure_name}",
                                "nativeQueryRef": measure_name
                            }
                        ]
                    }
                }
            },
            "visualContainerObjects": vco
        }
    }

def create_table(name, x, y, width, height, z, columns, title_text=None):
    projections = []
    for col in columns:
        entity = col["entity"]
        prop = col["property"]
        is_measure = col.get("is_measure", False)
        if is_measure:
            field_def = {
                "Measure": {
                    "Expression": {"SourceRef": {"Entity": entity}},
                    "Property": prop
                }
            }
        else:
            field_def = {
                "Column": {
                    "Expression": {"SourceRef": {"Entity": entity}},
                    "Property": prop
                }
            }
        projections.append({
            "field": field_def,
            "queryRef": f"{entity}.{prop}",
            "nativeQueryRef": prop
        })
        
    vco = make_title(title_text) if title_text else {}
    return {
        "$schema": SCHEMA_VC,
        "name": name,
        "position": {"x": x, "y": y, "z": z, "width": width, "height": height, "tabOrder": z},
        "visual": {
            "visualType": "tableEx",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": projections
                    }
                }
            },
            "visualContainerObjects": vco
        }
    }

def build_all_pages():
    print("=" * 80)
    print("BUILDING COMPLETE UiA CONTROLLER REPORT SUITE (PBIR)")
    print("=" * 80)

    # Clean existing page directories
    if os.path.exists(PAGES_DIR):
        for item in os.listdir(PAGES_DIR):
            p = os.path.join(PAGES_DIR, item)
            if os.path.isdir(p):
                shutil.rmtree(p)
            elif item != "pages.json":
                os.remove(p)
    else:
        os.makedirs(PAGES_DIR, exist_ok=True)

    pages_manifest = []

    # =========================================================================
    # PAGE 1: 01 Instituttleder (Operativ økonomistyring)
    # =========================================================================
    p1_id = "page_01_instituttleder"
    p1_name = "01 Instituttleder (Operativ styring)"
    p1_dir = os.path.join(PAGES_DIR, p1_id)
    os.makedirs(os.path.join(p1_dir, "visuals"), exist_ok=True)

    with open(os.path.join(p1_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": SCHEMA_PAGE,
            "name": p1_id,
            "displayName": p1_name,
            "displayOption": "FitToPage",
            "height": 1080,
            "width": 1920
        }, f, indent=2)
    pages_manifest.append(p1_id)

    p1_visuals = [
        # Slicers
        create_slicer("p1_slc_inst", 20, 15, 360, 65, 1, "DimOrganization", "Instituttnavn", "Velg institutt"),
        create_slicer("p1_slc_date", 400, 15, 280, 65, 2, "DimDate", "AarMaaned", "Rapporteringsperiode"),
        create_slicer("p1_slc_fc", 700, 15, 280, 65, 3, "DimForecastVersion", "Versjonsnavn", "Forecastversjon"),
        create_slicer("p1_slc_proj", 1000, 15, 340, 65, 4, "DimProject", "Prosjektnavn", "Prosjektfilter"),
        # KPI Strip (5 cards)
        create_card("p1_kpi_regnskap", 20, 95, 360, 105, 5, "Regnskap YTD", "Regnskap YTD (MNOK)"),
        create_card("p1_kpi_avvik_ytd", 400, 95, 360, 105, 6, "Avvik YTD", "Avvik YTD mot budsjett"),
        create_card("p1_kpi_fc_aar", 780, 95, 360, 105, 7, "Forecast aarsbelop", "Forecast årsbeløp (LE)"),
        create_card("p1_kpi_fc_avvik", 1160, 95, 360, 105, 8, "Forecastavvik", "Forecastavvik mot årsbudsjett"),
        create_card("p1_kpi_aarsverk", 1540, 95, 360, 105, 9, "Aarsverk", "Årsverk (siste status)"),
        # Middle row
        create_line_chart("p1_cht_trend", 20, 215, 1120, 390, 10, "DimDate", "AarMaaned", [
            {"property": "Regnskap"},
            {"property": "Budsjett"},
            {"property": "Gjeldende forecast"}
        ], "Månedlig faktisk / budsjett / prognosetrend"),
        create_bar_chart("p1_cht_driver", 1160, 215, 740, 390, 11, "DimAccount", "SRS_regnskapslinje", "Forecastavvik", "Hva driver prognoseavviket? (per regnskapslinje)"),
        # Bottom row
        create_table("p1_tbl_ressurs", 20, 620, 860, 310, 12, [
            {"entity": "DimOrganization", "property": "Instituttnavn"},
            {"entity": "_Measures", "property": "Registrerte studenter", "is_measure": True},
            {"entity": "_Measures", "property": "Faglige aarsverk", "is_measure": True},
            {"entity": "_Measures", "property": "Studenter per faglig aarsverk", "is_measure": True},
            {"entity": "_Measures", "property": "SPE60", "is_measure": True},
            {"entity": "_Measures", "property": "Kostnad per SPE60", "is_measure": True}
        ], "Ressurser & Studieproduktivitet"),
        create_table("p1_tbl_tiltak", 900, 620, 1000, 310, 13, [
            {"entity": "FactAction", "property": "TiltakID"},
            {"entity": "FactAction", "property": "Tiltaksbeskrivelse"},
            {"entity": "FactAction", "property": "AnsvarligRolle"},
            {"entity": "FactAction", "property": "ForventetEffekt"},
            {"entity": "FactAction", "property": "RealisertEffekt"},
            {"entity": "FactAction", "property": "Status"}
        ], "Tiltaksoppfølging (FactAction)"),
        # Bottom summary strip
        create_card("p1_bot_fc", 20, 945, 450, 115, 14, "Forecast aarsbelop", "1. Forecast før tiltak"),
        create_card("p1_bot_tiltak", 490, 945, 450, 115, 15, "Forventet tiltakseffekt", "2. Identifisert tiltakseffekt"),
        create_card("p1_bot_etter", 960, 945, 450, 115, 16, "Forecast etter tiltak", "3. Netto prognose etter tiltak"),
        create_card("p1_bot_rest", 1430, 945, 470, 115, 17, "Restavvik etter tiltak", "4. Gjenstående restavvik")
    ]

    for v in p1_visuals:
        v_dir = os.path.join(p1_dir, "visuals", v["name"])
        os.makedirs(v_dir, exist_ok=True)
        with open(os.path.join(v_dir, "visual.json"), "w", encoding="utf-8") as vf:
            json.dump(v, vf, indent=2)

    # =========================================================================
    # PAGE 2: 02 Dekan & Fakultetsledelse (Faculty Performance)
    # =========================================================================
    p2_id = "page_02_dekan"
    p2_name = "02 Dekan & Fakultetsledelse"
    p2_dir = os.path.join(PAGES_DIR, p2_id)
    os.makedirs(os.path.join(p2_dir, "visuals"), exist_ok=True)

    with open(os.path.join(p2_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": SCHEMA_PAGE,
            "name": p2_id,
            "displayName": p2_name,
            "displayOption": "FitToPage",
            "height": 1080,
            "width": 1920
        }, f, indent=2)
    pages_manifest.append(p2_id)

    p2_visuals = [
        # Slicers
        create_slicer("p2_slc_fak", 20, 15, 400, 65, 1, "DimOrganization", "Fakultetsnavn", "Velg fakultet"),
        create_slicer("p2_slc_date", 440, 15, 320, 65, 2, "DimDate", "AarMaaned", "Rapporteringsperiode"),
        create_slicer("p2_slc_fc", 780, 15, 320, 65, 3, "DimForecastVersion", "Versjonsnavn", "Forecastversjon"),
        # KPI Strip (6 cards)
        create_card("p2_kpi_fc", 20, 95, 300, 105, 4, "Forecast aarsbelop", "Forecast helår"),
        create_card("p2_kpi_avvik", 340, 95, 300, 105, 5, "Forecastavvik", "Forecastavvik"),
        create_card("p2_kpi_aarsverk", 660, 95, 300, 105, 6, "Aarsverk", "Årsverk totalt"),
        create_card("p2_kpi_studenter", 980, 95, 300, 105, 7, "Registrerte studenter", "Registrerte studenter"),
        create_card("p2_kpi_boa", 1300, 95, 300, 105, 8, "BOA inntekter", "BOA-inntekter"),
        create_card("p2_kpi_tiltak", 1620, 95, 280, 105, 9, "Forventet tiltakseffekt", "Identifisert tiltakseffekt"),
        # Middle row
        create_bar_chart("p2_cht_inst_avvik", 20, 215, 930, 420, 10, "DimOrganization", "Instituttnavn", "Forecastavvik", "Instituttenes prognoseavvik"),
        create_bar_chart("p2_cht_boa_kilde", 970, 215, 930, 420, 11, "DimProject", "Finansieringskilde", "BOA inntekter", "Eksternfinansiering per kilde (NFR, EU, Oppdrag)"),
        # Bottom row
        create_table("p2_tbl_produktivitet", 20, 650, 930, 410, 12, [
            {"entity": "DimOrganization", "property": "Instituttnavn"},
            {"entity": "_Measures", "property": "Kostnad per SPE60", "is_measure": True},
            {"entity": "_Measures", "property": "Studenter per faglig aarsverk", "is_measure": True},
            {"entity": "_Measures", "property": "SPE60 per faglig aarsverk", "is_measure": True},
            {"entity": "_Measures", "property": "Lonnandel %", "is_measure": True}
        ], "Faglig produktivitet og lønnsandel per institutt"),
        create_table("p2_tbl_tiltak_oversikt", 970, 650, 930, 410, 13, [
            {"entity": "DimOrganization", "property": "Instituttnavn"},
            {"entity": "_Measures", "property": "Antall tiltak", "is_measure": True},
            {"entity": "_Measures", "property": "Aapne tiltak", "is_measure": True},
            {"entity": "_Measures", "property": "Forsinkede tiltak", "is_measure": True},
            {"entity": "_Measures", "property": "Forventet tiltakseffekt", "is_measure": True},
            {"entity": "_Measures", "property": "Realisert tiltakseffekt", "is_measure": True},
            {"entity": "_Measures", "property": "Tiltak realiseringsgrad %", "is_measure": True}
        ], "Omstilling og tiltaksdekning per institutt")
    ]

    for v in p2_visuals:
        v_dir = os.path.join(p2_dir, "visuals", v["name"])
        os.makedirs(v_dir, exist_ok=True)
        with open(os.path.join(v_dir, "visual.json"), "w", encoding="utf-8") as vf:
            json.dump(v, vf, indent=2)

    # =========================================================================
    # PAGE 3: 03 Universitetsdirektør & Ledelse (Executive Overview)
    # =========================================================================
    p3_id = "page_03_executive"
    p3_name = "03 Universitetsdirektør & Ledelse"
    p3_dir = os.path.join(PAGES_DIR, p3_id)
    os.makedirs(os.path.join(p3_dir, "visuals"), exist_ok=True)

    with open(os.path.join(p3_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": SCHEMA_PAGE,
            "name": p3_id,
            "displayName": p3_name,
            "displayOption": "FitToPage",
            "height": 1080,
            "width": 1920
        }, f, indent=2)
    pages_manifest.append(p3_id)

    p3_visuals = [
        # Slicers
        create_slicer("p3_slc_date", 20, 15, 350, 65, 1, "DimDate", "AarMaaned", "Rapporteringsperiode"),
        create_slicer("p3_slc_fc", 390, 15, 350, 65, 2, "DimForecastVersion", "Versjonsnavn", "Forecastversjon"),
        # KPI Strip (5 cards)
        create_card("p3_kpi_budsjett", 20, 95, 360, 105, 3, "Aarsbudsjett", "Årsbudsjett UiA"),
        create_card("p3_kpi_forecast", 400, 95, 360, 105, 4, "Forecast aarsbelop", "Helårsprognose (LE)"),
        create_card("p3_kpi_avvik", 780, 95, 360, 105, 5, "Forecastavvik", "Prognoseavvik mot budsjett"),
        create_card("p3_kpi_aarsverk", 1160, 95, 360, 105, 6, "Aarsverk", "Årsverk totalt"),
        create_card("p3_kpi_boa", 1540, 95, 360, 105, 7, "BOA andel %", "BOA-finansieringsandel %"),
        # Middle row
        create_line_chart("p3_cht_fc_dev", 20, 215, 930, 420, 8, "DimForecastVersion", "Versjonsnavn", [
            {"property": "Forecast"}
        ], "Prognoseutvikling over runder (Budsjett, FC1, FC2, LE)"),
        create_bar_chart("p3_cht_fak_avvik", 970, 215, 930, 420, 9, "DimOrganization", "Fakultetsnavn", "Forecastavvik", "Prognoseavvik fordelt på fakulteter"),
        # Bottom row
        create_table("p3_tbl_fakultet", 20, 650, 1100, 410, 10, [
            {"entity": "DimOrganization", "property": "Fakultetsnavn"},
            {"entity": "_Measures", "property": "Aarsbudsjett", "is_measure": True},
            {"entity": "_Measures", "property": "Regnskap YTD", "is_measure": True},
            {"entity": "_Measures", "property": "Forecast aarsbelop", "is_measure": True},
            {"entity": "_Measures", "property": "Forecastavvik", "is_measure": True},
            {"entity": "_Measures", "property": "Aarsverk", "is_measure": True},
            {"entity": "_Measures", "property": "BOA inntekter", "is_measure": True}
        ], "Hovedtall per fakultet og fellesområde"),
        create_table("p3_tbl_omstilling", 1140, 650, 760, 410, 11, [
            {"entity": "DimOrganization", "property": "Fakultetsnavn"},
            {"entity": "_Measures", "property": "Forventet tiltakseffekt", "is_measure": True},
            {"entity": "_Measures", "property": "Realisert tiltakseffekt", "is_measure": True},
            {"entity": "_Measures", "property": "Forecast etter tiltak", "is_measure": True},
            {"entity": "_Measures", "property": "Restavvik etter tiltak", "is_measure": True}
        ], "Omstillingsstatus & Netto resultat etter tiltak")
    ]

    for v in p3_visuals:
        v_dir = os.path.join(p3_dir, "visuals", v["name"])
        os.makedirs(v_dir, exist_ok=True)
        with open(os.path.join(v_dir, "visual.json"), "w", encoding="utf-8") as vf:
            json.dump(v, vf, indent=2)

    # =========================================================================
    # PAGE 4: 04 Universitetsstyret (Styreoversikt)
    # =========================================================================
    p4_id = "page_04_styret"
    p4_name = "04 Universitetsstyret"
    p4_dir = os.path.join(PAGES_DIR, p4_id)
    os.makedirs(os.path.join(p4_dir, "visuals"), exist_ok=True)

    with open(os.path.join(p4_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": SCHEMA_PAGE,
            "name": p4_id,
            "displayName": p4_name,
            "displayOption": "FitToPage",
            "height": 1080,
            "width": 1920
        }, f, indent=2)
    pages_manifest.append(p4_id)

    p4_visuals = [
        create_slicer("p4_slc_date", 20, 15, 400, 65, 1, "DimDate", "AarMaaned", "Rapporteringsperiode"),
        create_slicer("p4_slc_fc", 440, 15, 400, 65, 2, "DimForecastVersion", "Versjonsnavn", "Forecastversjon"),
        # KPI Strip
        create_card("p4_kpi_budsjett", 20, 95, 360, 105, 3, "Aarsbudsjett", "Totalbudsjett"),
        create_card("p4_kpi_forecast", 400, 95, 360, 105, 4, "Forecast aarsbelop", "Forventet helårsresultat"),
        create_card("p4_kpi_avvik_pct", 780, 95, 360, 105, 5, "Forecastavvik %", "Forventet avvik %"),
        create_card("p4_kpi_spe_oppnaaelse", 1160, 95, 360, 105, 6, "Studiepoeng maaloppnaelse %", "Studiepoeng måloppnåelse"),
        create_card("p4_kpi_boa", 1540, 95, 360, 105, 7, "BOA inntekter", "Eksternfinansiering (BOA)"),
        # Middle row
        create_table("p4_tbl_maal", 20, 215, 930, 420, 8, [
            {"entity": "DimOrganization", "property": "Fakultetsnavn"},
            {"entity": "_Measures", "property": "Registrerte studenter", "is_measure": True},
            {"entity": "_Measures", "property": "Avlagte studiepoeng", "is_measure": True},
            {"entity": "_Measures", "property": "SPE60", "is_measure": True},
            {"entity": "_Measures", "property": "Studiepoeng maaloppnaelse %", "is_measure": True}
        ], "Strategisk måloppnåelse studieaktivitet"),
        create_table("p4_tbl_risiko", 970, 215, 930, 420, 9, [
            {"entity": "DimOrganization", "property": "Fakultetsnavn"},
            {"entity": "_Measures", "property": "Forecast aarsbelop", "is_measure": True},
            {"entity": "_Measures", "property": "Forecastavvik", "is_measure": True},
            {"entity": "_Measures", "property": "Forventet tiltakseffekt", "is_measure": True},
            {"entity": "_Measures", "property": "Restavvik etter tiltak", "is_measure": True}
        ], "Økonomisk risikobilde og omstilling"),
        # Bottom row
        create_table("p4_tbl_tiltak_detalj", 20, 650, 1880, 410, 10, [
            {"entity": "FactAction", "property": "TiltakID"},
            {"entity": "FactAction", "property": "Tiltaksbeskrivelse"},
            {"entity": "FactAction", "property": "Avviksarsak"},
            {"entity": "FactAction", "property": "AnsvarligRolle"},
            {"entity": "FactAction", "property": "ForventetEffekt"},
            {"entity": "FactAction", "property": "RealisertEffekt"},
            {"entity": "FactAction", "property": "Status"}
        ], "Universitetsstyrets omstillingstiltak (FactAction)")
    ]

    for v in p4_visuals:
        v_dir = os.path.join(p4_dir, "visuals", v["name"])
        os.makedirs(v_dir, exist_ok=True)
        with open(os.path.join(v_dir, "visual.json"), "w", encoding="utf-8") as vf:
            json.dump(v, vf, indent=2)

    # =========================================================================
    # PAGE 5: 05 Forskningsledelse & BOA (Research & Projects)
    # =========================================================================
    p5_id = "page_05_forskning_boa"
    p5_name = "05 Forskningsledelse & BOA"
    p5_dir = os.path.join(PAGES_DIR, p5_id)
    os.makedirs(os.path.join(p5_dir, "visuals"), exist_ok=True)

    with open(os.path.join(p5_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": SCHEMA_PAGE,
            "name": p5_id,
            "displayName": p5_name,
            "displayOption": "FitToPage",
            "height": 1080,
            "width": 1920
        }, f, indent=2)
    pages_manifest.append(p5_id)

    p5_visuals = [
        create_slicer("p5_slc_fak", 20, 15, 360, 65, 1, "DimOrganization", "Fakultetsnavn", "Fakultet"),
        create_slicer("p5_slc_inst", 400, 15, 360, 65, 2, "DimOrganization", "Instituttnavn", "Institutt"),
        create_slicer("p5_slc_kilde", 780, 15, 360, 65, 3, "DimProject", "Finansieringskilde", "Finansieringskilde"),
        # KPI Strip
        create_card("p5_kpi_boa", 20, 95, 450, 105, 4, "BOA inntekter", "Total BOA-inntekt"),
        create_card("p5_kpi_nfr", 490, 95, 450, 105, 5, "NFR inntekter", "NFR inntekter"),
        create_card("p5_kpi_eu", 960, 95, 450, 105, 6, "EU inntekter", "EU inntekter"),
        create_card("p5_kpi_boa_aarsverk", 1430, 95, 470, 105, 7, "BOA per faglig aarsverk", "BOA per faglig årsverk"),
        # Middle row
        create_bar_chart("p5_cht_kilde", 20, 215, 930, 420, 8, "DimProject", "Finansieringskilde", "BOA inntekter", "BOA-inntekter fordelt på finansieringskilder"),
        create_bar_chart("p5_cht_type", 970, 215, 930, 420, 9, "DimProject", "Finansieringstype", "BOA inntekter", "Fordeling bidrag vs. oppdrag"),
        # Bottom row
        create_table("p5_tbl_portefolje", 20, 650, 1880, 410, 10, [
            {"entity": "DimProject", "property": "Prosjekt"},
            {"entity": "DimProject", "property": "Prosjektnavn"},
            {"entity": "DimProject", "property": "Finansieringskilde"},
            {"entity": "DimProject", "property": "Finansieringstype"},
            {"entity": "DimProject", "property": "Prosjektkategori"},
            {"entity": "_Measures", "property": "Regnskap", "is_measure": True},
            {"entity": "_Measures", "property": "Budsjett", "is_measure": True},
            {"entity": "_Measures", "property": "Forecast", "is_measure": True},
            {"entity": "_Measures", "property": "Avvik", "is_measure": True}
        ], "Fullstendig prosjektportefølje (DimProject / FactGL)")
    ]

    for v in p5_visuals:
        v_dir = os.path.join(p5_dir, "visuals", v["name"])
        os.makedirs(v_dir, exist_ok=True)
        with open(os.path.join(v_dir, "visual.json"), "w", encoding="utf-8") as vf:
            json.dump(v, vf, indent=2)

    # =========================================================================
    # PAGE 6: 06 Studieportefølje & Aktivitet (Study Portfolio)
    # =========================================================================
    p6_id = "page_06_studieportefolje"
    p6_name = "06 Studieportefølje & Aktivitet"
    p6_dir = os.path.join(PAGES_DIR, p6_id)
    os.makedirs(os.path.join(p6_dir, "visuals"), exist_ok=True)

    with open(os.path.join(p6_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": SCHEMA_PAGE,
            "name": p6_id,
            "displayName": p6_name,
            "displayOption": "FitToPage",
            "height": 1080,
            "width": 1920
        }, f, indent=2)
    pages_manifest.append(p6_id)

    p6_visuals = [
        create_slicer("p6_slc_fak", 20, 15, 360, 65, 1, "DimOrganization", "Fakultetsnavn", "Fakultet"),
        create_slicer("p6_slc_inst", 400, 15, 360, 65, 2, "DimOrganization", "Instituttnavn", "Institutt"),
        create_slicer("p6_slc_nivaa", 780, 15, 360, 65, 3, "DimStudyProgram", "Studienivaa", "Studienivå"),
        # KPI Strip
        create_card("p6_kpi_stud", 20, 95, 300, 105, 4, "Registrerte studenter", "Registrerte studenter"),
        create_card("p6_kpi_sp", 340, 95, 300, 105, 5, "Avlagte studiepoeng", "Avlagte studiepoeng"),
        create_card("p6_kpi_spe60", 660, 95, 300, 105, 6, "SPE60", "SPE60 (helårsekvivalenter)"),
        create_card("p6_kpi_oppnaa", 980, 95, 300, 105, 7, "Studiepoeng maaloppnaelse %", "Måloppnåelse %"),
        create_card("p6_kpi_kst_stud", 1300, 95, 300, 105, 8, "Kostnad per student", "Kostnad per student"),
        create_card("p6_kpi_kst_spe", 1620, 95, 280, 105, 9, "Kostnad per SPE60", "Kostnad per SPE60"),
        # Middle row
        create_bar_chart("p6_cht_kst_spe", 20, 215, 930, 420, 10, "DimOrganization", "Instituttnavn", "Kostnad per SPE60", "Enhetskostnad per SPE60 per institutt"),
        create_bar_chart("p6_cht_nivaa", 970, 215, 930, 420, 11, "DimStudyProgram", "Studienivaa", "SPE60", "SPE60 fordelt på studienivå"),
        # Bottom row
        create_table("p6_tbl_programmer", 20, 650, 1880, 410, 12, [
            {"entity": "DimStudyProgram", "property": "Studieprogram"},
            {"entity": "DimStudyProgram", "property": "Studieprogramnavn"},
            {"entity": "DimStudyProgram", "property": "Studienivaa"},
            {"entity": "DimStudyProgram", "property": "NormerteStudiepoeng"},
            {"entity": "_Measures", "property": "Registrerte studenter", "is_measure": True},
            {"entity": "_Measures", "property": "Avlagte studiepoeng", "is_measure": True},
            {"entity": "_Measures", "property": "SPE60", "is_measure": True},
            {"entity": "_Measures", "property": "Studiepoeng maaloppnaelse %", "is_measure": True}
        ], "Studieprogramaktivitet og produksjonsgrad (FactStudyPoints)")
    ]

    for v in p6_visuals:
        v_dir = os.path.join(p6_dir, "visuals", v["name"])
        os.makedirs(v_dir, exist_ok=True)
        with open(os.path.join(v_dir, "visual.json"), "w", encoding="utf-8") as vf:
            json.dump(v, vf, indent=2)

    # =========================================================================
    # PAGE 7: 07 Action Tracker (Tiltaks- & Omstillingsportefølje)
    # =========================================================================
    p7_id = "page_07_action_tracker"
    p7_name = "07 Action Tracker (Tiltak)"
    p7_dir = os.path.join(PAGES_DIR, p7_id)
    os.makedirs(os.path.join(p7_dir, "visuals"), exist_ok=True)

    with open(os.path.join(p7_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": SCHEMA_PAGE,
            "name": p7_id,
            "displayName": p7_name,
            "displayOption": "FitToPage",
            "height": 1080,
            "width": 1920
        }, f, indent=2)
    pages_manifest.append(p7_id)

    p7_visuals = [
        create_slicer("p7_slc_rolle", 20, 15, 360, 65, 1, "FactAction", "AnsvarligRolle", "Ansvarlig lederrolle"),
        create_slicer("p7_slc_status", 400, 15, 360, 65, 2, "FactAction", "Status", "Gjennomføringsstatus"),
        create_slicer("p7_slc_prio", 780, 15, 360, 65, 3, "FactAction", "Prioritet", "Prioritetsnivå"),
        # KPI Strip
        create_card("p7_kpi_antall", 20, 95, 300, 105, 4, "Antall tiltak", "Totalt antall tiltak"),
        create_card("p7_kpi_aapne", 340, 95, 300, 105, 5, "Aapne tiltak", "Aktive åpne tiltak"),
        create_card("p7_kpi_forsinket", 660, 95, 300, 105, 6, "Forsinkede tiltak", "Forsinkede tiltak"),
        create_card("p7_kpi_forventet", 980, 95, 300, 105, 7, "Forventet tiltakseffekt", "Identifisert effekt"),
        create_card("p7_kpi_realisert", 1300, 95, 300, 105, 8, "Realisert tiltakseffekt", "Realisert effekt"),
        create_card("p7_kpi_grad", 1620, 95, 280, 105, 9, "Tiltak realiseringsgrad %", "Realiseringsgrad %"),
        # Middle row
        create_bar_chart("p7_cht_rolle", 20, 215, 930, 420, 10, "FactAction", "AnsvarligRolle", "Forventet tiltakseffekt", "Identifisert besparelse per ansvarlig rolle"),
        create_bar_chart("p7_cht_status", 970, 215, 930, 420, 11, "FactAction", "Status", "Forventet tiltakseffekt", "Tiltakseffekt per status (Gjennomført, Pågår, Forsinket)"),
        # Bottom row
        create_table("p7_tbl_alle_tiltak", 20, 650, 1880, 410, 12, [
            {"entity": "FactAction", "property": "TiltakID"},
            {"entity": "FactAction", "property": "Tiltaksbeskrivelse"},
            {"entity": "FactAction", "property": "Avviksarsak"},
            {"entity": "FactAction", "property": "AnsvarligRolle"},
            {"entity": "FactAction", "property": "StartDatoNokkel"},
            {"entity": "FactAction", "property": "FristDatoNokkel"},
            {"entity": "FactAction", "property": "ForventetEffekt"},
            {"entity": "FactAction", "property": "RealisertEffekt"},
            {"entity": "FactAction", "property": "Status"},
            {"entity": "FactAction", "property": "Prioritet"}
        ], "Komplett omstillingslogg (FactAction.csv)")
    ]

    for v in p7_visuals:
        v_dir = os.path.join(p7_dir, "visuals", v["name"])
        os.makedirs(v_dir, exist_ok=True)
        with open(os.path.join(v_dir, "visual.json"), "w", encoding="utf-8") as vf:
            json.dump(v, vf, indent=2)

    # =========================================================================
    # PAGE 8: 08 Controller Cockpit (Dybdeanalyse & Kontrolltårn)
    # =========================================================================
    p8_id = "page_08_controller_cockpit"
    p8_name = "08 Controller Cockpit"
    p8_dir = os.path.join(PAGES_DIR, p8_id)
    os.makedirs(os.path.join(p8_dir, "visuals"), exist_ok=True)

    with open(os.path.join(p8_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": SCHEMA_PAGE,
            "name": p8_id,
            "displayName": p8_name,
            "displayOption": "FitToPage",
            "height": 1080,
            "width": 1920
        }, f, indent=2)
    pages_manifest.append(p8_id)

    p8_visuals = [
        create_slicer("p8_slc_fak", 20, 15, 360, 65, 1, "DimOrganization", "Fakultetsnavn", "Fakultet"),
        create_slicer("p8_slc_inst", 400, 15, 360, 65, 2, "DimOrganization", "Instituttnavn", "Institutt"),
        create_slicer("p8_slc_konto", 780, 15, 360, 65, 3, "DimAccount", "SRS_regnskapslinje", "Regnskapslinje"),
        # KPI Strip
        create_card("p8_kpi_avvik", 20, 95, 360, 105, 4, "Forecastavvik", "Helårsavvik mot budsjett"),
        create_card("p8_kpi_avvik_pct", 400, 95, 360, 105, 5, "Forecastavvik %", "Avvik i prosent"),
        create_card("p8_kpi_conf", 780, 95, 360, 105, 6, "Forecast confidence %", "Forecast confidence %"),
        create_card("p8_kpi_aapne_tiltak", 1160, 95, 360, 105, 7, "Aapne tiltak", "Aktive tiltak"),
        create_card("p8_kpi_rest", 1540, 95, 360, 105, 8, "Restavvik etter tiltak", "Gjenstående restavvik"),
        # Middle row
        create_bar_chart("p8_cht_konto", 20, 215, 930, 420, 9, "DimAccount", "Kontonavn", "Forecastavvik", "Avviksdrivere på kontonavn (Største avvik)"),
        create_line_chart("p8_cht_ytd_trend", 970, 215, 930, 420, 10, "DimDate", "AarMaaned", [
            {"property": "Regnskap YTD"},
            {"property": "Budsjett YTD"}
        ], "Akkumulert YTD-utvikling (Regnskap vs Budsjett)"),
        # Bottom row
        create_table("p8_tbl_kontroll", 20, 650, 1880, 410, 11, [
            {"entity": "DimOrganization", "property": "Fakultetsnavn"},
            {"entity": "DimOrganization", "property": "Instituttnavn"},
            {"entity": "DimAccount", "property": "SRS_regnskapslinje"},
            {"entity": "DimAccount", "property": "Kontonavn"},
            {"entity": "_Measures", "property": "Regnskap YTD", "is_measure": True},
            {"entity": "_Measures", "property": "Budsjett YTD", "is_measure": True},
            {"entity": "_Measures", "property": "Avvik YTD", "is_measure": True},
            {"entity": "_Measures", "property": "Forecast aarsbelop", "is_measure": True},
            {"entity": "_Measures", "property": "Forecastavvik", "is_measure": True}
        ], "Hierarkisk avstemmingsmatrise (Fakultet → Institutt → Regnskapslinje → Konto)")
    ]

    for v in p8_visuals:
        v_dir = os.path.join(p8_dir, "visuals", v["name"])
        os.makedirs(v_dir, exist_ok=True)
        with open(os.path.join(v_dir, "visual.json"), "w", encoding="utf-8") as vf:
            json.dump(v, vf, indent=2)

    # =========================================================================
    # DRILL-THROUGH 1: DT Økonomidetalj (Bilagsnivå fra FactGL)
    # =========================================================================
    dt1_id = "page_dt_okonomi"
    dt1_name = "DT Økonomidetalj (Bilag)"
    dt1_dir = os.path.join(PAGES_DIR, dt1_id)
    os.makedirs(os.path.join(dt1_dir, "visuals"), exist_ok=True)

    with open(os.path.join(dt1_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": SCHEMA_PAGE,
            "name": dt1_id,
            "displayName": dt1_name,
            "displayOption": "FitToPage",
            "height": 1080,
            "width": 1920
        }, f, indent=2)
    pages_manifest.append(dt1_id)

    dt1_visuals = [
        create_card("dt1_kpi_regnskap", 20, 20, 600, 110, 1, "Regnskap", "Total sum posteringer (Regnskap)"),
        create_card("dt1_kpi_budsjett", 660, 20, 600, 110, 2, "Budsjett", "Budsjettbeløp"),
        create_card("dt1_kpi_avvik", 1300, 20, 600, 110, 3, "Avvik", "Avvik (Regnskap - Budsjett)"),
        create_table("dt1_tbl_bilag", 20, 150, 1880, 910, 4, [
            {"entity": "FactGL", "property": "Bilag"},
            {"entity": "FactGL", "property": "DatoNokkel"},
            {"entity": "FactGL", "property": "Organisasjonsnokkel"},
            {"entity": "FactGL", "property": "Konto"},
            {"entity": "FactGL", "property": "Prosjekt"},
            {"entity": "FactGL", "property": "Tekst"},
            {"entity": "FactGL", "property": "Belop_signert"},
            {"entity": "FactGL", "property": "Datakilde"},
            {"entity": "_Measures", "property": "Regnskap", "is_measure": True}
        ], "Transaksjons- og bilagslogg (FactGL.csv)")
    ]

    for v in dt1_visuals:
        v_dir = os.path.join(dt1_dir, "visuals", v["name"])
        os.makedirs(v_dir, exist_ok=True)
        with open(os.path.join(v_dir, "visual.json"), "w", encoding="utf-8") as vf:
            json.dump(v, vf, indent=2)

    # =========================================================================
    # DRILL-THROUGH 2: DT Bemanning & Årsverk (FactFTE)
    # =========================================================================
    dt2_id = "page_dt_bemanning"
    dt2_name = "DT Bemanning & Årsverk"
    dt2_dir = os.path.join(PAGES_DIR, dt2_id)
    os.makedirs(os.path.join(dt2_dir, "visuals"), exist_ok=True)

    with open(os.path.join(dt2_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": SCHEMA_PAGE,
            "name": dt2_id,
            "displayName": dt2_name,
            "displayOption": "FitToPage",
            "height": 1080,
            "width": 1920
        }, f, indent=2)
    pages_manifest.append(dt2_id)

    dt2_visuals = [
        create_card("dt2_kpi_aarsverk", 20, 20, 450, 110, 1, "Aarsverk", "Årsverk totalt"),
        create_card("dt2_kpi_faglige", 490, 20, 450, 110, 2, "Faglige aarsverk", "Faglige årsverk"),
        create_card("dt2_kpi_lonn", 960, 20, 450, 110, 3, "Lonnskostnader", "Lønnskostnader"),
        create_card("dt2_kpi_per_av", 1430, 20, 470, 110, 4, "Lonn per aarsverk", "Snittlønn per årsverk"),
        create_bar_chart("dt2_cht_gruppe", 20, 150, 930, 420, 5, "DimPositionGroup", "Stillingsgruppenavn", "Aarsverk", "Årsverk per stillingsgruppe"),
        create_bar_chart("dt2_cht_kat", 970, 150, 930, 420, 6, "DimPositionGroup", "Stillingskategori", "Aarsverk", "Årsverk per stillingskategori"),
        create_table("dt2_tbl_detalj", 20, 590, 1880, 470, 7, [
            {"entity": "DimOrganization", "property": "Instituttnavn"},
            {"entity": "DimPositionGroup", "property": "Stillingskategori"},
            {"entity": "DimPositionGroup", "property": "Stillingsgruppenavn"},
            {"entity": "_Measures", "property": "Aarsverk", "is_measure": True},
            {"entity": "_Measures", "property": "Faglige aarsverk", "is_measure": True},
            {"entity": "_Measures", "property": "Lonnskostnader", "is_measure": True},
            {"entity": "_Measures", "property": "Lonn per aarsverk", "is_measure": True}
        ], "Bemannings- og årsverksoversikt (FactFTE.csv)")
    ]

    for v in dt2_visuals:
        v_dir = os.path.join(dt2_dir, "visuals", v["name"])
        os.makedirs(v_dir, exist_ok=True)
        with open(os.path.join(v_dir, "visual.json"), "w", encoding="utf-8") as vf:
            json.dump(v, vf, indent=2)

    # =========================================================================
    # DRILL-THROUGH 3: DT Prosjektdetalj (EVM & Portefølje)
    # =========================================================================
    dt3_id = "page_dt_prosjekt"
    dt3_name = "DT Prosjektdetalj"
    dt3_dir = os.path.join(PAGES_DIR, dt3_id)
    os.makedirs(os.path.join(dt3_dir, "visuals"), exist_ok=True)

    with open(os.path.join(dt3_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": SCHEMA_PAGE,
            "name": dt3_id,
            "displayName": dt3_name,
            "displayOption": "FitToPage",
            "height": 1080,
            "width": 1920
        }, f, indent=2)
    pages_manifest.append(dt3_id)

    dt3_visuals = [
        create_card("dt3_kpi_bac", 20, 20, 450, 110, 1, "BAC (Budget at Completion)", "BAC (Budget at Completion)"),
        create_card("dt3_kpi_eac", 490, 20, 450, 110, 2, "EAC (Estimate at Completion)", "EAC (Estimate at Completion)"),
        create_card("dt3_kpi_etc", 960, 20, 450, 110, 3, "ETC (Estimate to Complete)", "ETC (Estimate to Complete)"),
        create_card("dt3_kpi_vac", 1430, 20, 470, 110, 4, "VAC (Variance at Completion)", "VAC (Variance at Completion)"),
        create_table("dt3_tbl_prosjekt_info", 20, 150, 1880, 910, 5, [
            {"entity": "DimProject", "property": "Prosjekt"},
            {"entity": "DimProject", "property": "Prosjektnavn"},
            {"entity": "DimProject", "property": "Finansieringskilde"},
            {"entity": "DimProject", "property": "Finansieringstype"},
            {"entity": "DimProject", "property": "Prosjektkategori"},
            {"entity": "_Measures", "property": "BAC (Budget at Completion)", "is_measure": True},
            {"entity": "_Measures", "property": "EAC (Estimate at Completion)", "is_measure": True},
            {"entity": "_Measures", "property": "ETC (Estimate to Complete)", "is_measure": True},
            {"entity": "_Measures", "property": "VAC (Variance at Completion)", "is_measure": True},
            {"entity": "_Measures", "property": "VAC %", "is_measure": True}
        ], "Prosjekt Earned Value Management (EVM) oversikt")
    ]

    for v in dt3_visuals:
        v_dir = os.path.join(dt3_dir, "visuals", v["name"])
        os.makedirs(v_dir, exist_ok=True)
        with open(os.path.join(v_dir, "visual.json"), "w", encoding="utf-8") as vf:
            json.dump(v, vf, indent=2)

    # =========================================================================
    # DRILL-THROUGH 4: DT Tiltaksdetalj (Tiltakskort)
    # =========================================================================
    dt4_id = "page_dt_tiltak"
    dt4_name = "DT Tiltaksdetalj"
    dt4_dir = os.path.join(PAGES_DIR, dt4_id)
    os.makedirs(os.path.join(dt4_dir, "visuals"), exist_ok=True)

    with open(os.path.join(dt4_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": SCHEMA_PAGE,
            "name": dt4_id,
            "displayName": dt4_name,
            "displayOption": "FitToPage",
            "height": 1080,
            "width": 1920
        }, f, indent=2)
    pages_manifest.append(dt4_id)

    dt4_visuals = [
        create_card("dt4_kpi_forv", 20, 20, 600, 110, 1, "Forventet tiltakseffekt", "Forventet tiltakseffekt"),
        create_card("dt4_kpi_real", 660, 20, 600, 110, 2, "Realisert tiltakseffekt", "Realisert tiltakseffekt"),
        create_card("dt4_kpi_grad", 1300, 20, 600, 110, 3, "Tiltak realiseringsgrad %", "Realiseringsgrad %"),
        create_table("dt4_tbl_kort", 20, 150, 1880, 910, 4, [
            {"entity": "FactAction", "property": "TiltakID"},
            {"entity": "FactAction", "property": "Tiltaksbeskrivelse"},
            {"entity": "FactAction", "property": "Avviksarsak"},
            {"entity": "FactAction", "property": "AnsvarligRolle"},
            {"entity": "FactAction", "property": "StartDatoNokkel"},
            {"entity": "FactAction", "property": "FristDatoNokkel"},
            {"entity": "FactAction", "property": "ForventetEffekt"},
            {"entity": "FactAction", "property": "RealisertEffekt"},
            {"entity": "FactAction", "property": "Status"},
            {"entity": "FactAction", "property": "Prioritet"},
            {"entity": "FactAction", "property": "Sannsynlighet"}
        ], "Detaljert tiltakskort & risikovurdering (FactAction)")
    ]

    for v in dt4_visuals:
        v_dir = os.path.join(dt4_dir, "visuals", v["name"])
        os.makedirs(v_dir, exist_ok=True)
        with open(os.path.join(v_dir, "visual.json"), "w", encoding="utf-8") as vf:
            json.dump(v, vf, indent=2)

    # =========================================================================
    # DRILL-THROUGH 5: DT Studieaktivitet (Produksjon per studieprogram)
    # =========================================================================
    dt5_id = "page_dt_studier"
    dt5_name = "DT Studieaktivitet"
    dt5_dir = os.path.join(PAGES_DIR, dt5_id)
    os.makedirs(os.path.join(dt5_dir, "visuals"), exist_ok=True)

    with open(os.path.join(dt5_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": SCHEMA_PAGE,
            "name": dt5_id,
            "displayName": dt5_name,
            "displayOption": "FitToPage",
            "height": 1080,
            "width": 1920
        }, f, indent=2)
    pages_manifest.append(dt5_id)

    dt5_visuals = [
        create_card("dt5_kpi_stud", 20, 20, 450, 110, 1, "Registrerte studenter", "Registrerte studenter"),
        create_card("dt5_kpi_sp", 490, 20, 450, 110, 2, "Avlagte studiepoeng", "Avlagte studiepoeng"),
        create_card("dt5_kpi_spe60", 960, 20, 450, 110, 3, "SPE60", "SPE60"),
        create_card("dt5_kpi_oppnaa", 1430, 20, 470, 110, 4, "Studiepoeng maaloppnaelse %", "Studiepoeng måloppnåelse %"),
        create_table("dt5_tbl_programmer", 20, 150, 1880, 910, 5, [
            {"entity": "DimStudyProgram", "property": "Studieprogram"},
            {"entity": "DimStudyProgram", "property": "Studieprogramnavn"},
            {"entity": "DimStudyProgram", "property": "Studienivaa"},
            {"entity": "FactStudyPoints", "property": "RegistrerteStudenter"},
            {"entity": "FactStudyPoints", "property": "PlanlagteStudiepoeng"},
            {"entity": "FactStudyPoints", "property": "AvlagteStudiepoeng"},
            {"entity": "FactStudyPoints", "property": "SPE60"},
            {"entity": "FactStudyPoints", "property": "BestattAndel"},
            {"entity": "_Measures", "property": "Studiepoeng maaloppnaelse %", "is_measure": True}
        ], "Studieaktivitet og studiepoengproduksjon (FactStudyPoints)")
    ]

    for v in dt5_visuals:
        v_dir = os.path.join(dt5_dir, "visuals", v["name"])
        os.makedirs(v_dir, exist_ok=True)
        with open(os.path.join(v_dir, "visual.json"), "w", encoding="utf-8") as vf:
            json.dump(v, vf, indent=2)

    # =========================================================================
    # Write pages.json metadata
    # =========================================================================
    with open(os.path.join(PAGES_DIR, "pages.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": SCHEMA_PAGES,
            "pageOrder": pages_manifest,
            "activePageName": pages_manifest[0]
        }, f, indent=2)

    print(f"Successfully created {len(pages_manifest)} report pages:")
    for idx, pid in enumerate(pages_manifest, 1):
        print(f"  {idx:>2d}. {pid}")

    print("\nValidating PBIR report suite with powerbi-report-author...")
    res = subprocess.run(["powerbi-report-author", "validate", REPORT_DIR], capture_output=True, text=True, shell=True)
    print("STDOUT:", res.stdout)
    if res.stderr:
        print("STDERR:", res.stderr)

if __name__ == "__main__":
    build_all_pages()
