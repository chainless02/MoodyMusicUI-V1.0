import json
import os
import requests
import hashlib
from concurrent.futures import ThreadPoolExecutor

with open('data.json', 'r', encoding='utf-8-sig') as f:
    json_data = json.load(f)

data = json_data.get('data', [])
os.makedirs('assets/images/downloaded', exist_ok=True)

requests.packages.urllib3.disable_warnings() # suppress SSL warnings

def download_image(url):
    if not url or url.startswith('/src/'):
        return url
        
    full_url = url
    if url.startswith('/storage/'):
        full_url = 'https://m-api.changgepd.top' + url
        
    ext = full_url.split('.')[-1].split('?')[0]
    if len(ext) > 4 or not ext:
        ext = 'jpg'
        
    hash_name = hashlib.md5(full_url.encode('utf-8')).hexdigest()
    local_path = f'assets/images/downloaded/{hash_name}.{ext}'
    
    if os.path.exists(local_path):
        return local_path
        
    try:
        resp = requests.get(full_url, timeout=10, verify=False)
        if resp.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(resp.content)
            return local_path
        else:
            # print(f"Failed {resp.status_code}: {full_url}")
            pass
    except Exception as e:
        # print(f"Error {e}: {full_url}")
        pass
        
    return url

urls_to_download = set()
for artist in data:
    if artist.get('avatar'): urls_to_download.add(artist['avatar'])
    for album in artist.get('albums', []):
        if album.get('cover'): urls_to_download.add(album['cover'])

valid_urls = [u for u in urls_to_download if not u.startswith('/src/')]
print(f"Found {len(valid_urls)} external/storage URLs to process...")

url_map = {}
success_count = 0
with ThreadPoolExecutor(max_workers=20) as executor:
    results = executor.map(lambda u: (u, download_image(u)), valid_urls)
    for orig, local in results:
        url_map[orig] = local
        if local != orig:
            success_count += 1

print(f"Successfully downloaded {success_count} images.")

# Update JSON
for artist in data:
    if artist.get('avatar'):
        artist['avatar'] = url_map.get(artist['avatar'], artist['avatar'])
    for album in artist.get('albums', []):
        if album.get('cover'):
            album['cover'] = url_map.get(album['cover'], album['cover'])

json_data['data'] = data

with open('data_local.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False)

print("Saved updated data to data_local.json")
