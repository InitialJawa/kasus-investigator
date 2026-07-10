"""Regenerate sumber_data.txt from updated raw_data.json"""
import json
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(r"D:\ALL IN ONE\CODE\kasus-investigator\output")

with open(OUTPUT_DIR / "raw_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

articles = data["articles"]
source_counts = data["statistics"]["by_source"]
actor_mentions = data.get("actor_mentions", {})
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(OUTPUT_DIR / "sumber_data.txt", "w", encoding="utf-8") as f:
    f.write("=" * 70 + "\n")
    f.write("LAPORAN SUMBER DATA - KASUS INVESTIGASI\n")
    f.write("Konflik Kejaksaan Agung vs Polri (2023-2026)\n")
    f.write("Generated: " + now + "\n")
    f.write("=" * 70 + "\n\n")
    f.write("Total artikel: " + str(len(articles)) + "\n")
    f.write("Sumber: " + ", ".join(source_counts.keys()) + "\n\n")
    f.write("-" * 70 + "\n")
    f.write("STATISTIK PER SUMBER:\n")
    f.write("-" * 70 + "\n")
    for src, count in sorted(source_counts.items(), key=lambda x: -x[1]):
        f.write("  " + src + ": " + str(count) + " artikel\n")
    f.write("\n")
    f.write("-" * 70 + "\n")
    f.write("AKTOR YANG DISEBUT:\n")
    f.write("-" * 70 + "\n")
    for actor, info in sorted(actor_mentions.items(), key=lambda x: -x[1]["count"]):
        f.write("  " + actor + " (" + info["role"] + "): " + str(info["count"]) + " kali\n")
        for t in info["articles"][:3]:
            f.write("    - " + t + "\n")
    f.write("\n")
    f.write("-" * 70 + "\n")
    f.write("DAFTAR LENGKAP ARTIKEL:\n")
    f.write("-" * 70 + "\n")
    for i, art in enumerate(articles, 1):
        f.write("\n[" + str(i).zfill(3) + "] " + art["title"] + "\n")
        f.write("  Sumber: " + art["source"] + "\n")
        f.write("  Tanggal: " + str(art.get("date", "N/A")) + "\n")
        f.write("  URL: " + art["url"] + "\n")
        f.write("  Snippet: " + art["snippet"][:200] + "\n")
    f.write("\n" + "=" * 70 + "\n")
    f.write("SUMBER WEBSSEARCH TAMBAHAN:\n")
    f.write("=" * 70 + "\n")
    for art in articles:
        if art.get("scraped_from") == "websearch":
            f.write("  [" + str(art.get("date", "")) + "] " + art["title"] + "\n")
            f.write("    URL: " + art["url"] + "\n")
    f.write("=" * 70 + "\n")

print("Sumber data updated:", len(articles), "articles")
