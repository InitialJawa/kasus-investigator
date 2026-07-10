"""
KASUS INVESTIGATOR - Scraper Multi-Sumber
Scrape berita dari portal berita Indonesia tentang konflik Kejaksaan vs Polri
Output: output/raw_data.json + output/sumber_data.txt
"""

import json
import os
import re
import time
import hashlib
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
}

KEYWORDS = [
    "kejaksaan polri konflik",
    "kejaksaan agung vs polri",
    "kejaksaan polri perseteruan",
    "jaksa agung kapolri",
    "kejaksaan polri jabatan",
    "kejaksaan polri logistik politik",
    "kejaksaan polri transisi kekuasaan",
    "kejaksaan polri rebut pengaruh",
    "kabareskrim jaksa agung",
    "kejaksaan polri 2024",
    "kejaksaan polri 2025",
    "konflik lembaga hukum indonesia",
    "kejaksaan polri oversight",
    "dpr kejaksaan polri",
]


def safe_get(url, timeout=15):
    """Request dengan error handling."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        return resp
    except Exception as e:
        print(f"  [ERROR] {url}: {e}")
        return None


def scrape_google_news(keyword, max_results=10):
    """Scrape Google News untuk keyword tertentu."""
    articles = []
    search_url = f"https://www.google.com/search?q={keyword.replace(' ', '+')}&tbm=nws&tbs=qdr:3y"
    resp = safe_get(search_url)
    if not resp:
        return articles

    soup = BeautifulSoup(resp.text, "html.parser")
    for item in soup.select("div.SoaBEf")[:max_results]:
        try:
            title_el = item.select_one("div.MBeuO")
            snippet_el = item.select_one(".GI74Re")
            source_el = item.select_one(".CEMjEf")
            link_el = item.select_one("a")

            title = title_el.get_text(strip=True) if title_el else ""
            snippet = snippet_el.get_text(strip=True) if snippet_el else ""
            source = source_el.get_text(strip=True) if source_el else ""
            link = link_el["href"] if link_el and link_el.has_attr("href") else ""

            if link.startswith("/url?q="):
                link = link.split("/url?q=")[1].split("&")[0]

            if title:
                articles.append({
                    "title": title,
                    "snippet": snippet,
                    "source": source,
                    "url": link,
                    "keyword": keyword,
                    "scraped_from": "google_news",
                })
        except Exception:
            continue
    return articles


def scrape_kompas(keyword, max_results=5):
    """Scrape Kompas search."""
    articles = []
    search_url = f"https://search.kompas.com/search/?q={keyword.replace(' ', '+')}"
    resp = safe_get(search_url)
    if not resp:
        return articles

    soup = BeautifulSoup(resp.text, "html.parser")
    for item in soup.select("div.article")[:max_results]:
        try:
            title_el = item.select_one("h3 a")
            snippet_el = item.select_one("p")
            title = title_el.get_text(strip=True) if title_el else ""
            snippet = snippet_el.get_text(strip=True) if snippet_el else ""
            link = title_el["href"] if title_el and title_el.has_attr("href") else ""

            if title:
                articles.append({
                    "title": title,
                    "snippet": snippet,
                    "source": "Kompas",
                    "url": link,
                    "keyword": keyword,
                    "scraped_from": "kompas_search",
                })
        except Exception:
            continue
    return articles


def scrape_cnn_indonesia(keyword, max_results=5):
    """Scrape CNN Indonesia search."""
    articles = []
    search_url = f"https://www.cnnindonesia.com/search?query={keyword.replace(' ', '+')}"
    resp = safe_get(search_url)
    if not resp:
        return articles

    soup = BeautifulSoup(resp.text, "html.parser")
    for item in soup.select("article")[:max_results]:
        try:
            title_el = item.select_one("h2 a, h3 a")
            snippet_el = item.select_one("p")
            title = title_el.get_text(strip=True) if title_el else ""
            snippet = snippet_el.get_text(strip=True) if snippet_el else ""
            link = title_el["href"] if title_el and title_el.has_attr("href") else ""

            if title:
                articles.append({
                    "title": title,
                    "snippet": snippet,
                    "source": "CNN Indonesia",
                    "url": link,
                    "keyword": keyword,
                    "scraped_from": "cnn_search",
                })
        except Exception:
            continue
    return articles


def scrape_detik(keyword, max_results=5):
    """Scrape Detik search."""
    articles = []
    search_url = f"https://www.detik.com/search/searchall?query={keyword.replace(' ', '+')}&siteid=2"
    resp = safe_get(search_url)
    if not resp:
        return articles

    soup = BeautifulSoup(resp.text, "html.parser")
    for item in soup.select("article")[:max_results]:
        try:
            title_el = item.select_one("h2 a, h3 a, span a")
            snippet_el = item.select_one("p")
            title = title_el.get_text(strip=True) if title_el else ""
            snippet = snippet_el.get_text(strip=True) if snippet_el else ""
            link = title_el["href"] if title_el and title_el.has_attr("href") else ""

            if title:
                articles.append({
                    "title": title,
                    "snippet": snippet,
                    "source": "Detik",
                    "url": link,
                    "keyword": keyword,
                    "scraped_from": "detik_search",
                })
        except Exception:
            continue
    return articles


def scrape_tempo(keyword, max_results=5):
    """Scrape Tempo search."""
    articles = []
    search_url = f"https://www.tempo.co/search?q={keyword.replace(' ', '+')}"
    resp = safe_get(search_url)
    if not resp:
        return articles

    soup = BeautifulSoup(resp.text, "html.parser")
    for item in soup.select("div.list-content, article")[:max_results]:
        try:
            title_el = item.select_one("h2 a, h3 a, a")
            snippet_el = item.select_one("p")
            title = title_el.get_text(strip=True) if title_el else ""
            snippet = snippet_el.get_text(strip=True) if snippet_el else ""
            link = title_el["href"] if title_el and title_el.has_attr("href") else ""

            if title and link and not link.startswith("http"):
                link = "https://www.tempo.co" + link

            if title:
                articles.append({
                    "title": title,
                    "snippet": snippet,
                    "source": "Tempo",
                    "url": link,
                    "keyword": keyword,
                    "scraped_from": "tempo_search",
                })
        except Exception:
            continue
    return articles


def scrape_tirto(keyword, max_results=5):
    """Scrape Tirto search."""
    articles = []
    search_url = f"https://tirto.id/search?q={keyword.replace(' ', '+')}"
    resp = safe_get(search_url)
    if not resp:
        return articles

    soup = BeautifulSoup(resp.text, "html.parser")
    for item in soup.select("article, div.search-result")[:max_results]:
        try:
            title_el = item.select_one("h2 a, h3 a, a")
            snippet_el = item.select_one("p")
            title = title_el.get_text(strip=True) if title_el else ""
            snippet = snippet_el.get_text(strip=True) if snippet_el else ""
            link = title_el["href"] if title_el and title_el.has_attr("href") else ""

            if title and link and not link.startswith("http"):
                link = "https://tirto.id" + link

            if title:
                articles.append({
                    "title": title,
                    "snippet": snippet,
                    "source": "Tirto",
                    "url": link,
                    "keyword": keyword,
                    "scraped_from": "tirto_search",
                })
        except Exception:
            continue
    return articles


def extract_actors(articles):
    """Ekstrak aktor/tokoh yang disebut dalam artikel."""
    known_actors = {
        "St Burhanuddin": "Jaksa Agung",
        "Burhanuddin": "Jaksa Agung",
        "Sanitiar Burhanuddin": "Jaksa Agung",
        "Listyo Sigit Prabowo": "Kapolri",
        "Listyo Sigit": "Kapolri",
        "Kapolri Listyo": "Kapolri",
        "Jenderal Listyo": "Kapolri",
        "Kabareskrim": "Kabareskrim",
        "Prabowo Subianto": "Presiden",
        "Prabowo": "Presiden",
        "Joko Widodo": "Presiden RI",
        "Jokowi": "Presiden RI",
        "Mahfud MD": "Menko Polhukam",
        "Mahfud": "Menko Polhukam",
        "Komisi III DPR": "DPR Komisi III",
        "DPR": "DPR",
        "Mahkamah Agung": "MA",
        "Mahkamah Konstitusi": "MK",
        "LPSK": "LPSK",
        "KPK": "KPK",
        "Ombudsman": "Ombudsman",
    }

    actor_mentions = {}
    for article in articles:
        text = f"{article['title']} {article['snippet']}"
        for actor, role in known_actors.items():
            if actor.lower() in text.lower():
                if actor not in actor_mentions:
                    actor_mentions[actor] = {"role": role, "count": 0, "articles": []}
                actor_mentions[actor]["count"] += 1
                actor_mentions[actor]["articles"].append(article["title"])
    return actor_mentions


def extract_dates(articles):
    """Ekstrak dan normalisasi tanggal dari artikel."""
    date_patterns = [
        r"(\d{1,2})\s+(Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)\s+(\d{4})",
        r"(\d{4})-(\d{2})-(\d{2})",
        r"(\d{1,2})/(\d{1,2})/(\d{4})",
    ]
    bulan_map = {
        "Januari": "01", "Februari": "02", "Maret": "03", "April": "04",
        "Mei": "05", "Juni": "06", "Juli": "07", "Agustus": "08",
        "September": "09", "Oktober": "10", "November": "11", "Desember": "12",
    }

    dated_articles = []
    for article in articles:
        text = f"{article['title']} {article['snippet']}"
        found_date = None
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                groups = match.groups()
                if len(groups) == 3 and groups[1] in bulan_map:
                    found_date = f"{groups[2]}-{bulan_map[groups[1]]}-{groups[0].zfill(2)}"
                elif len(groups) == 3 and groups[0].isdigit() and len(groups[0]) == 4:
                    found_date = f"{groups[0]}-{groups[1]}-{groups[2]}"
                break
        article["date"] = found_date
        dated_articles.append(article)
    return dated_articles


def deduplicate(articles):
    """Hapus artikel duplikat berdasarkan judul."""
    seen = set()
    unique = []
    for art in articles:
        key = hashlib.md5(art["title"].lower().encode()).hexdigest()
        if key not in seen:
            seen.add(key)
            unique.append(art)
    return unique


def main():
    print("=" * 60)
    print("KASUS INVESTIGATOR - Scraper Multi-Sumber")
    print("Target: Konflik Kejaksaan Agung vs Polri")
    print("Periode: 2023 - 2026")
    print("=" * 60)

    all_articles = []

    # Scrape dari berbagai sumber untuk setiap keyword
    scrapers = [
        ("Google News", scrape_google_news),
        ("Kompas", scrape_kompas),
        ("CNN Indonesia", scrape_cnn_indonesia),
        ("Detik", scrape_detik),
        ("Tempo", scrape_tempo),
        ("Tirto", scrape_tirto),
    ]

    for keyword in KEYWORDS:
        print(f"\n[KEYWORD] '{keyword}'")
        for scraper_name, scraper_func in scrapers:
            print(f"  [{scraper_name}] ...", end=" ")
            try:
                results = scraper_func(keyword, max_results=5)
                print(f"{len(results)} artikel")
                all_articles.extend(results)
            except Exception as e:
                print(f"ERROR: {e}")
            time.sleep(1)  # Rate limiting

    # Deduplicate
    all_articles = deduplicate(all_articles)
    print(f"\n[DEDUP] Total unik: {len(all_articles)} artikel")

    # Extract dates
    all_articles = extract_dates(all_articles)

    # Extract actors
    actor_mentions = extract_actors(all_articles)

    # Hitung statistik
    source_counts = {}
    for art in all_articles:
        src = art["source"]
        source_counts[src] = source_counts.get(src, 0) + 1

    keyword_counts = {}
    for art in all_articles:
        kw = art["keyword"]
        keyword_counts[kw] = keyword_counts.get(kw, 0) + 1

    # Simpan data
    data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_articles": len(all_articles),
            "period": "2023-2026",
            "keywords_used": KEYWORDS,
            "sources": list(source_counts.keys()),
        },
        "articles": all_articles,
        "actor_mentions": actor_mentions,
        "statistics": {
            "by_source": source_counts,
            "by_keyword": keyword_counts,
        },
    }

    # Simpan JSON
    json_path = OUTPUT_DIR / "raw_data.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n[SAVE] {json_path}")

    # Generate sumber_data.txt
    txt_path = OUTPUT_DIR / "sumber_data.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("LAPORAN SUMBER DATA - KASUS INVESTIGASI\n")
        f.write(f"Konflik Kejaksaan Agung vs Polri (2023-2026)\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")

        f.write("STATISTIK:\n")
        f.write(f"  Total artikel unik: {len(all_articles)}\n")
        f.write(f"  Sumber: {', '.join(source_counts.keys())}\n")
        f.write(f"  Keywords: {len(KEYWORDS)}\n\n")

        f.write("-" * 70 + "\n")
        f.write("STATISTIK PER SUMBER:\n")
        f.write("-" * 70 + "\n")
        for src, count in sorted(source_counts.items(), key=lambda x: -x[1]):
            f.write(f"  {src}: {count} artikel\n")
        f.write("\n")

        f.write("-" * 70 + "\n")
        f.write("STATISTIK PER KEYWORD:\n")
        f.write("-" * 70 + "\n")
        for kw, count in sorted(keyword_counts.items(), key=lambda x: -x[1]):
            f.write(f"  '{kw}': {count} artikel\n")
        f.write("\n")

        f.write("-" * 70 + "\n")
        f.write("AKTOR YANG DISEBUT:\n")
        f.write("-" * 70 + "\n")
        for actor, info in sorted(actor_mentions.items(), key=lambda x: -x[1]["count"]):
            f.write(f"  {actor} ({info['role']}): {info['count']} kali disebut\n")
            for art_title in info["articles"][:5]:
                f.write(f"    - {art_title}\n")
        f.write("\n")

        f.write("-" * 70 + "\n")
        f.write("DAFTAR LENGKAP ARTIKEL:\n")
        f.write("-" * 70 + "\n")
        for i, art in enumerate(all_articles, 1):
            f.write(f"\n[{i:03d}] {art['title']}\n")
            f.write(f"  Sumber: {art['source']}\n")
            f.write(f"  Keyword: {art['keyword']}\n")
            f.write(f"  Tanggal: {art.get('date', 'N/A')}\n")
            f.write(f"  URL: {art['url']}\n")
            f.write(f"  Snippet: {art['snippet'][:200]}\n")

        f.write("\n" + "=" * 70 + "\n")
        f.write("METODOLOGI:\n")
        f.write("=" * 70 + "\n")
        f.write("1. Scraper mengambil data dari Google News, Kompas, CNN Indonesia,\n")
        f.write("   Detik, Tempo, dan Tirto\n")
        f.write("2. Pencarian menggunakan 14 keyword terkait konflik Kejaksaan vs Polri\n")
        f.write("3. Deduplikasi berdasarkan hash judul artikel\n")
        f.write("4. Ekstrak tanggal dan aktor dari teks menggunakan regex & known entities\n")
        f.write("5. Semua data disimpan dalam format JSON untuk analisis lebih lanjut\n")
        f.write("=" * 70 + "\n")

    print(f"[SAVE] {txt_path}")
    print(f"\n[DONE] Scraping selesai! Total: {len(all_articles)} artikel")
    return data


if __name__ == "__main__":
    main()
