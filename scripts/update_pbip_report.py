import json, os
from pathlib import Path

pages_dir = Path('UIA-Controller-Prosjekt.Report/definition/pages')

# 1. Update pages.json
pages_json_path = pages_dir / 'pages.json'
with open(pages_json_path, 'r', encoding='utf-8') as f:
    pages_data = json.load(f)

order = pages_data.get('pageOrder', [])
for p in ['page_use_cases', 'page_laereplaner']:
    if p not in order:
        dt_idx = next((i for i, x in enumerate(order) if x.startswith('page_dt_')), len(order))
        order.insert(dt_idx, p)

pages_data['pageOrder'] = order
with open(pages_json_path, 'w', encoding='utf-8') as f:
    json.dump(pages_data, f, indent=2, ensure_ascii=False)
print(f'pages.json updated with {len(order)} pages.')

# 2. Create page_use_cases
p_uc = pages_dir / 'page_use_cases'
p_uc.mkdir(exist_ok=True)
with open(p_uc / 'page.json', 'w', encoding='utf-8') as f:
    json.dump({
        '$schema': 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json',
        'name': 'page_use_cases',
        'displayName': 'UC Statlig Regelverkskontroll (UC1–UC6)',
        'displayOption': 'FitToPage',
        'height': 1080,
        'width': 1920
    }, f, indent=2, ensure_ascii=False)

# Visual for page_use_cases: table of actions with UseCasesRef
vis_uc = p_uc / 'visuals' / 'uc_tbl_actions'
vis_uc.mkdir(parents=True, exist_ok=True)
with open(vis_uc / 'visual.json', 'w', encoding='utf-8') as f:
    json.dump({
        '$schema': 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.0.0/schema.json',
        'name': 'uc_tbl_actions',
        'position': {'x': 20, 'y': 220, 'z': 1, 'width': 1880, 'height': 830, 'tabOrder': 1},
        'visual': {
            'visualType': 'tableEx',
            'query': {
                'queryState': {
                    'Values': {
                        'projections': [
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactAction'}}, 'Property': 'UseCasesRef'}}, 'queryRef': 'FactAction.UseCasesRef', 'nativeQueryRef': 'Use Case'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactAction'}}, 'Property': 'TiltakID'}}, 'queryRef': 'FactAction.TiltakID', 'nativeQueryRef': 'Tiltak ID'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactAction'}}, 'Property': 'Tiltaksbeskrivelse'}}, 'queryRef': 'FactAction.Tiltaksbeskrivelse', 'nativeQueryRef': 'Tiltak'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactAction'}}, 'Property': 'Avviksarsak'}}, 'queryRef': 'FactAction.Avviksarsak', 'nativeQueryRef': 'Regelverksavvik & Årsak'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactAction'}}, 'Property': 'AnsvarligRolle'}}, 'queryRef': 'FactAction.AnsvarligRolle', 'nativeQueryRef': 'Ansvarlig Rolle'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactAction'}}, 'Property': 'ForventetEffekt'}}, 'queryRef': 'FactAction.ForventetEffekt', 'nativeQueryRef': 'Forventet Effekt'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactAction'}}, 'Property': 'RealisertEffekt'}}, 'queryRef': 'FactAction.RealisertEffekt', 'nativeQueryRef': 'Realisert Effekt'},
                            {'field': {'Measure': {'Expression': {'SourceRef': {'Entity': '_Measures'}}, 'Property': 'Tiltak RAG Status'}}, 'queryRef': '_Measures.Tiltak RAG Status', 'nativeQueryRef': 'Status RAG'}
                        ]
                    }
                }
            },
            'visualContainerObjects': {
                'title': [{'properties': {'show': {'expr': {'Literal': {'Value': 'true'}}}, 'text': {'expr': {'Literal': {'Value': "'Statlige Use Cases (UC1–UC6) & Forankrede Styringstiltak (FactAction.csv)'"}}}}}]
            }
        }
    }, f, indent=2, ensure_ascii=False)

# Card 1 for page_use_cases: F-05-20 Avsetningsgrad
kpi_f05 = p_uc / 'visuals' / 'uc_kpi_f05'
kpi_f05.mkdir(parents=True, exist_ok=True)
with open(kpi_f05 / 'visual.json', 'w', encoding='utf-8') as f:
    json.dump({
        '$schema': 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.0.0/schema.json',
        'name': 'uc_kpi_f05',
        'position': {'x': 20, 'y': 95, 'z': 2, 'width': 450, 'height': 105, 'tabOrder': 2},
        'visual': {
            'visualType': 'card',
            'query': {
                'queryState': {
                    'Values': {
                        'projections': [{'field': {'Measure': {'Expression': {'SourceRef': {'Entity': '_Measures'}}, 'Property': 'Avsetningsgrad F-05-20 %'}}, 'queryRef': '_Measures.Avsetningsgrad F-05-20 %', 'nativeQueryRef': 'F-05-20 Avsetningsgrad'}]
                    }
                }
            },
            'visualContainerObjects': {
                'title': [{'properties': {'show': {'expr': {'Literal': {'Value': 'true'}}}, 'text': {'expr': {'Literal': {'Value': "'UC1: Avsetningsgrad F-05-20 (Maks 5,0 %)'"}}}}}]
            }
        }
    }, f, indent=2, ensure_ascii=False)

# Card 2 for page_use_cases: Lønnsandel %
kpi_lonn = p_uc / 'visuals' / 'uc_kpi_lonn'
kpi_lonn.mkdir(parents=True, exist_ok=True)
with open(kpi_lonn / 'visual.json', 'w', encoding='utf-8') as f:
    json.dump({
        '$schema': 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.0.0/schema.json',
        'name': 'uc_kpi_lonn',
        'position': {'x': 490, 'y': 95, 'z': 3, 'width': 450, 'height': 105, 'tabOrder': 3},
        'visual': {
            'visualType': 'card',
            'query': {
                'queryState': {
                    'Values': {
                        'projections': [{'field': {'Measure': {'Expression': {'SourceRef': {'Entity': '_Measures'}}, 'Property': 'Lonnandel %'}}, 'queryRef': '_Measures.Lonnandel %', 'nativeQueryRef': 'Lønnsandel %'}]
                    }
                }
            },
            'visualContainerObjects': {
                'title': [{'properties': {'show': {'expr': {'Literal': {'Value': 'true'}}}, 'text': {'expr': {'Literal': {'Value': "'UC6: Lønnsandel av Driftskostnader (Norm 71 %)'"}}}}}]
            }
        }
    }, f, indent=2, ensure_ascii=False)

# 3. Create page_laereplaner
p_lp = pages_dir / 'page_laereplaner'
p_lp.mkdir(exist_ok=True)
with open(p_lp / 'page.json', 'w', encoding='utf-8') as f:
    json.dump({
        '$schema': 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json',
        'name': 'page_laereplaner',
        'displayName': 'LP Læreplaner & Budsjettering (KD 2025)',
        'displayOption': 'FitToPage',
        'height': 1080,
        'width': 1920
    }, f, indent=2, ensure_ascii=False)

vis_lp = p_lp / 'visuals' / 'lp_tbl_studier'
vis_lp.mkdir(parents=True, exist_ok=True)
with open(vis_lp / 'visual.json', 'w', encoding='utf-8') as f:
    json.dump({
        '$schema': 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.0.0/schema.json',
        'name': 'lp_tbl_studier',
        'position': {'x': 20, 'y': 220, 'z': 1, 'width': 1880, 'height': 830, 'tabOrder': 1},
        'visual': {
            'visualType': 'tableEx',
            'query': {
                'queryState': {
                    'Values': {
                        'projections': [
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'DimStudyProgram'}}, 'Property': 'Studieprogram'}}, 'queryRef': 'DimStudyProgram.Studieprogram', 'nativeQueryRef': 'Programkode'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'DimStudyProgram'}}, 'Property': 'Programnavn'}}, 'queryRef': 'DimStudyProgram.Programnavn', 'nativeQueryRef': 'Læreplan & Programnavn'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'DimStudyProgram'}}, 'Property': 'Nivaa'}}, 'queryRef': 'DimStudyProgram.Nivaa', 'nativeQueryRef': 'Nivå'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'DimStudyProgram'}}, 'Property': 'Finansieringskategori'}}, 'queryRef': 'DimStudyProgram.Finansieringskategori', 'nativeQueryRef': 'KD Kategori'},
                            {'field': {'Measure': {'Expression': {'SourceRef': {'Entity': '_Measures'}}, 'Property': 'Avlagte studiepoeng'}}, 'queryRef': '_Measures.Avlagte studiepoeng', 'nativeQueryRef': 'Avlagte ECTS'},
                            {'field': {'Measure': {'Expression': {'SourceRef': {'Entity': '_Measures'}}, 'Property': 'SPE60'}}, 'queryRef': '_Measures.SPE60', 'nativeQueryRef': 'SPE60 Produksjon'},
                            {'field': {'Measure': {'Expression': {'SourceRef': {'Entity': '_Measures'}}, 'Property': 'Registrerte studenter'}}, 'queryRef': '_Measures.Registrerte studenter', 'nativeQueryRef': 'Studenttall'},
                            {'field': {'Measure': {'Expression': {'SourceRef': {'Entity': '_Measures'}}, 'Property': 'Studiepoeng maaloppnaelse %'}}, 'queryRef': '_Measures.Studiepoeng maaloppnaelse %', 'nativeQueryRef': 'Gjennomføring %'}
                        ]
                    }
                }
            },
            'visualContainerObjects': {
                'title': [{'properties': {'show': {'expr': {'Literal': {'Value': 'true'}}}, 'text': {'expr': {'Literal': {'Value': "'Læreplaner, Studieproduksjon og KD 2025 Finansieringsuttelling'"}}}}}]
            }
        }
    }, f, indent=2, ensure_ascii=False)

# 4. In page_05_forskning_boa, add TDI table visual from FactProjectBOA
p5_tdi = pages_dir / 'page_05_forskning_boa' / 'visuals' / 'p5_tbl_tdi_fullkost'
p5_tdi.mkdir(parents=True, exist_ok=True)
with open(p5_tdi / 'visual.json', 'w', encoding='utf-8') as f:
    json.dump({
        '$schema': 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.0.0/schema.json',
        'name': 'p5_tbl_tdi_fullkost',
        'position': {'x': 20, 'y': 220, 'z': 15, 'width': 1880, 'height': 410, 'tabOrder': 15},
        'visual': {
            'visualType': 'tableEx',
            'query': {
                'queryState': {
                    'Values': {
                        'projections': [
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactProjectBOA'}}, 'Property': 'Prosjekt'}}, 'queryRef': 'FactProjectBOA.Prosjekt', 'nativeQueryRef': 'ProsjektID'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactProjectBOA'}}, 'Property': 'Prosjektnavn'}}, 'queryRef': 'FactProjectBOA.Prosjektnavn', 'nativeQueryRef': 'Prosjektnavn'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactProjectBOA'}}, 'Property': 'Finansieringskilde'}}, 'queryRef': 'FactProjectBOA.Finansieringskilde', 'nativeQueryRef': 'Finansieringskilde'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactProjectBOA'}}, 'Property': 'Kontraktsbelop'}}, 'queryRef': 'FactProjectBOA.Kontraktsbelop', 'nativeQueryRef': 'Kontraktsbeløp'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactProjectBOA'}}, 'Property': 'Budsjett'}}, 'queryRef': 'FactProjectBOA.Budsjett', 'nativeQueryRef': 'TDI Budsjett'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactProjectBOA'}}, 'Property': 'Frikjop'}}, 'queryRef': 'FactProjectBOA.Frikjop', 'nativeQueryRef': 'Frikjøp'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactProjectBOA'}}, 'Property': 'DirekteDrift'}}, 'queryRef': 'FactProjectBOA.DirekteDrift', 'nativeQueryRef': 'Direkte Drift'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactProjectBOA'}}, 'Property': 'Overhead'}}, 'queryRef': 'FactProjectBOA.Overhead', 'nativeQueryRef': 'Overhead (22/25%)'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactProjectBOA'}}, 'Property': 'Leiested'}}, 'queryRef': 'FactProjectBOA.Leiested', 'nativeQueryRef': 'Leiested'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactProjectBOA'}}, 'Property': 'PåløptKostnad'}}, 'queryRef': 'FactProjectBOA.PåløptKostnad', 'nativeQueryRef': 'Forbruk YTD'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactProjectBOA'}}, 'Property': 'Forbruksavvik'}}, 'queryRef': 'FactProjectBOA.Forbruksavvik', 'nativeQueryRef': 'Forbruksavvik %'},
                            {'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'FactProjectBOA'}}, 'Property': 'RAG_Status'}}, 'queryRef': 'FactProjectBOA.RAG_Status', 'nativeQueryRef': 'RAG Status'}
                        ]
                    }
                }
            },
            'visualContainerObjects': {
                'title': [{'properties': {'show': {'expr': {'Literal': {'Value': 'true'}}}, 'text': {'expr': {'Literal': {'Value': "'BOA TDI Fullkostkalkyle (T+D+I) – Kontrakt, Frikjøp, Drift & Overhead'"}}}}}]
            }
        }
    }, f, indent=2, ensure_ascii=False)

print('PBIP report successfully updated with page_use_cases, page_laereplaner, and TDI visual in page_05!')
