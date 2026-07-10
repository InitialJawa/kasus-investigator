"""Download foto via Wikimedia API (get correct thumbnail URL)"""
import time
import requests
from pathlib import Path
from PIL import Image

PHOTOS_DIR = Path(r"D:\ALL IN ONE\CODE\kasus-investigator\photos")
PHOTOS_DIR.mkdir(exist_ok=True)

HEADERS = {"User-Agent": "KasusInvestigator/1.0 (research)"}

# Wikimedia API: get thumbnail URL for specific width
def get_thumb_url(filename, width=400):
    api = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": width,
        "format": "json"
    }
    r = requests.get(api, params=params, headers=HEADERS, timeout=20)
    data = r.json()
    pages = data["query"]["pages"]
    for page in pages.values():
        if "imageinfo" in page:
            return page["imageinfo"][0].get("thumburl", page["imageinfo"][0]["url"])
    return None

FILES = {
    "prabowo.jpg": "Prabowo_Subianto_2024_official_portrait.jpg",
    "burhanuddin.jpg": "JAKSAAGUNG,Sanitiar_Burhanuddin.jpg",
}

for local, wiki in FILES.items():
    target = PHOTOS_DIR / local
    if target.exists() and target.stat().st_size > 5000:
        print(f"[SKIP] {local} OK")
        continue
    
    print(f"[API] {wiki}...", end=" ", flush=True)
    url = get_thumb_url(wiki, 400)
    if not url:
        print("URL not found")
        continue
    
    print(f"URL={url[:60]}...", end=" ", flush=True)
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        with open(target, "wb") as f:
            f.write(r.content)
        img = Image.open(target)
        img.thumbnail((400, 400), Image.LANCZOS)
        img.save(target, quality=85)
        print(f"OK ({img.size[0]}x{img.size[1]})")
    except Exception as e:
        print(f"FAIL: {e}")
    time.sleep(2)

print("\n--- Status ---")
for f in sorted(PHOTOS_DIR.glob("*")):
    print(f"  {f.name}: {f.stat().st_size} bytes")
