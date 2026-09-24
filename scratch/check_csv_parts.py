with open("data/DimGlossary.csv", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    parts = l.strip().split(";")
    if len(parts) != 9:
        print(f"Line {i+1}: {len(parts)} parts -> {l.strip()}")
