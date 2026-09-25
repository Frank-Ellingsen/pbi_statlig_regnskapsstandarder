import os
import json
import re

SEM_DIR = r"C:\Users\frank\Desktop\UIA\uia_powerbi_complete_forecast_model\UIA-Controller-Prosjekt.SemanticModel\definition"
REP_DIR = r"C:\Users\frank\Desktop\UIA\uia_powerbi_complete_forecast_model\UIA-Controller-Prosjekt.Report\definition"

tables = {}

for tf in os.listdir(os.path.join(SEM_DIR, "tables")):
    if not tf.endswith(".tmdl"):
        continue
    t_name = tf[:-5]
    tables[t_name] = {"columns": set(), "measures": set()}
    with open(os.path.join(SEM_DIR, "tables", tf), "r", encoding="utf-8") as f:
        for line in f:
            c_match = re.match(r"^\tcolumn\s+(?:'([^']+)'|([^\s]+))", line)
            if c_match:
                col = c_match.group(1) or c_match.group(2)
                tables[t_name]["columns"].add(col)
            m_match = re.match(r"^\tmeasure\s+(?:'([^']+)'|([^\s=]+))", line)
            if m_match:
                meas = m_match.group(1) or m_match.group(2)
                tables[t_name]["measures"].add(meas)

print(f"Loaded {len(tables)} tables from TMDL:")
for t, data in tables.items():
    print(f"  - {t}: {len(data['columns'])} columns, {len(data['measures'])} measures")

# Check model.tmdl
with open(os.path.join(SEM_DIR, "model.tmdl"), "r", encoding="utf-8") as f:
    for line in f:
        m = re.match(r"ref table\s+(.+)", line.strip())
        if m:
            tbl = m.group(1).strip()
            if tbl not in tables:
                print(f"[ERROR] model.tmdl references non-existent table: {tbl}")

# Check all visual.json files in all pages
pages_dir = os.path.join(REP_DIR, "pages")
errors = []

for page in os.listdir(pages_dir):
    p_path = os.path.join(pages_dir, page)
    if not os.path.isdir(p_path):
        continue
    v_dir = os.path.join(p_path, "visuals")
    if not os.path.exists(v_dir):
        continue
    for vis in os.listdir(v_dir):
        vf_path = os.path.join(v_dir, vis, "visual.json")
        if not os.path.exists(vf_path):
            continue
        with open(vf_path, "r", encoding="utf-8") as vf:
            try:
                data = json.load(vf)
            except Exception as e:
                errors.append(f"{page}/{vis}: JSON parse error: {e}")
                continue
            
            # Recursive check of fields
            def check_obj(obj):
                if isinstance(obj, dict):
                    if "field" in obj:
                        fld = obj["field"]
                        for f_type in ["Measure", "Column"]:
                            if f_type in fld:
                                prop = fld[f_type]["Property"]
                                entity = fld[f_type]["Expression"]["SourceRef"]["Entity"]
                                if entity not in tables:
                                    errors.append(f"{page}/{vis}: Entity '{entity}' not in TMDL tables")
                                else:
                                    valid_props = tables[entity]["columns"] if f_type == "Column" else tables[entity]["measures"]
                                    if prop not in valid_props:
                                        errors.append(f"{page}/{vis}: Property '{prop}' not found as {f_type} in '{entity}'")
                    for k, v in obj.items():
                        check_obj(v)
                elif isinstance(obj, list):
                    for item in obj:
                        check_obj(item)
            
            check_obj(data)

print("\n" + "=" * 60)
if errors:
    print(f"FAILED with {len(errors)} errors:")
    for e in errors:
        print("  -", e)
else:
    print("SUCCESS: 0 broken bindings or missing references across all pages!")
print("=" * 60)
