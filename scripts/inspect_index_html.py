import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find dashboard definitions
matches = re.findall(r'(\bpage_[a-zA-Z0-9_]+)\s*:\s*\{', text)
print("Dashboard keys found:", matches)

# Find modelData definition
md_match = re.search(r'const modelData\s*=\s*\{([^}]+)\};', text, re.DOTALL)
if md_match:
    print("modelData content:\n", md_match.group(1))

# Check for old numbers
old_nums = [
    "10617128", "10747732", "36793524", "26045791", "1285.93", "661.77",
    "5615.74", "336945.4", "25678288", "10005000", "5562081",
    "10,62 M", "36,79 M", "26,05 M", "10,75 M", "1 285,9", "5 615,7", "25,68 M",
    "10.62", "36.79", "26.05", "10.75"
]

print("\nOccurrences of old numbers in index.html:")
for num in old_nums:
    c = text.count(num)
    if c > 0:
        print(f"  '{num}': {c} occurrences")
