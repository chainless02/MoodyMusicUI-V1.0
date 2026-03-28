import json
import re

with open('data.json', 'r', encoding='utf-8') as f:
    text = f.read()

ext_urls = list(set(re.findall(r'"(https?://[^"]+)"', text)))
print('=== 外部HTTP图片URL (Top 20) ===')
for u in sorted(ext_urls)[:20]:
    print(u)
print(f"总计外部URL: {len(ext_urls)}")

storage_paths = list(set(re.findall(r'"(/storage/[^"]+)"', text)))
print('\n=== /storage/ 路径 (Top 20) ===')
for p in sorted(storage_paths)[:20]:
    print(p)
print(f"总计 /storage/ 路径: {len(storage_paths)}")

src_paths = list(set(re.findall(r'"(/src/[^"]+)"', text)))
print('\n=== /src/ 路径 ===')
for p in sorted(src_paths):
    print(p)
print(f"总计 /src/ 路径: {len(src_paths)}")
