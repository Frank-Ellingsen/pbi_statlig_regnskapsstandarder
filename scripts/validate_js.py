import re
import subprocess

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
print(f"Found {len(scripts)} inline script block(s)")

for idx, script in enumerate(scripts):
    filename = f'temp_script_{idx}.js'
    with open(filename, 'w', encoding='utf-8') as sf:
        sf.write(script)
    
    res = subprocess.run(['node', '--check', filename], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Script {idx}: SYNTAX VALID (node --check passed)")
    else:
        print(f"Script {idx}: SYNTAX ERROR:\n{res.stderr}")
