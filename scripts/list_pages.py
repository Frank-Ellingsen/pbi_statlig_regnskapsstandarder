with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
# Find dashboard keys and line numbers
for i, line in enumerate(lines):
    if line.strip().startswith('page_') and ':' in line and '{' in line:
        print(f"Line {i+1}: {line.strip()}")
