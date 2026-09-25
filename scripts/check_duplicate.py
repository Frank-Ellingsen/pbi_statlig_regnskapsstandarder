with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

block1 = "".join(lines[3809:4516])
block2 = "".join(lines[4516:5222])

print(f"Block 1 length: {len(block1)}, Block 2 length: {len(block2)}")
print(f"Are they identical? {block1 == block2}")
if block1 != block2:
    import difflib
    diff = list(difflib.unified_diff(lines[3809:4516], lines[4516:5222]))
    print(f"Diff lines: {len(diff)}")
    for d in diff[:20]:
        print(d, end='')
