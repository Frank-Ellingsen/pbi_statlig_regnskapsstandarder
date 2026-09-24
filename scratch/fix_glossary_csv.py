import csv

# We read the raw lines and fix the 4 lines where the extra semicolon is inside PraktiskTolkning
with open("data/DimGlossary.csv", "r", encoding="utf-8") as f:
    raw_lines = f.readlines()

header = raw_lines[0].strip().split(";")
print("Header:", header)

rows = []
for i, l in enumerate(raw_lines[1:], start=2):
    parts = l.strip().split(";")
    if len(parts) == 9:
        rows.append(parts)
    elif len(parts) == 10:
        # The extra semicolon was in parts[5] (PraktiskTolkning)
        # e.g., parts[0]=ID, parts[1]=Begrep, parts[2]=Fullt, parts[3]=Kat, parts[4]=Def, parts[5]=Tolk1, parts[6]=Tolk2, parts[7]=DAX, parts[8]=Rolle, parts[9]=Rapport
        fixed_tolk = parts[5] + ", " + parts[6]
        fixed_row = [parts[0], parts[1], parts[2], parts[3], parts[4], fixed_tolk, parts[7], parts[8], parts[9]]
        print(f"Fixed row {parts[0]} ({parts[1]}): {fixed_tolk[:60]}")
        rows.append(fixed_row)
    else:
        print(f"Unexpected length {len(parts)} at line {i}")

print(f"Total processed rows: {len(rows)}")

with open("data/DimGlossary.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header)
    for r in rows:
        writer.writerow(r)

print("Saved data/DimGlossary.csv with proper standard CSV quoting.")
