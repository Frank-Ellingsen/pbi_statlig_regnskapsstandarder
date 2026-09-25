with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

targets = [
    "10617128", "10747732", "36793524", "26045791", "5615.74", "25678288", "10005000", "5562081",
    "10,62 M", "36,79 M", "26,05 M", "10,75 M", "5 615,7", "25,68 M", "1 285,9",
    "36.79", "10.75"
]

current_page = "GLOBAL"
for i, line in enumerate(lines):
    line_str = line.strip()
    if 'page_' in line_str and ':' in line_str and '{' in line_str:
        current_page = line_str.split(':')[0].strip()
    
    found = [t for t in targets if t in line]
    if found:
        print(f"Line {i+1} [{current_page}] (matches {found}):\n  {line_str[:120]}")
