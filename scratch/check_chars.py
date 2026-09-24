import json

with open('scratch/glossary_data.json', encoding='utf-8') as f:
    terms = json.load(f)

for t in terms:
    for k, v in t.items():
        val = str(v)
        if "${" in val:
            print("Found ${ in:", t["Begrep"], k)
        if "`" in val:
            print("Found ` in:", t["Begrep"], k)
        if '"' in val:
            print("Found \" in:", t["Begrep"], k, "->", val)
