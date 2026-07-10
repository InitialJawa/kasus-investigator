"""Merge websearch data into raw_data.json"""
import json
from pathlib import Path

OUTPUT_DIR = Path(r"D:\ALL IN ONE\CODE\kasus-investigator\output")

with open(OUTPUT_DIR / "raw_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

websearch_articles = [
    {"title": "Kejaksaan Agung: Hubungan dengan Polri Baik-baik Saja", "snippet": "Kejaksaan Agung mengklaim tak mencampuri penangkapan Ferry Hongkiriwang. Konflik polisi-jaksa memanas. Personel TNI berjaga di rumah Jampidsus Febrie Adriansyah.", "source": "Tempo", "url": "https://www.tempo.co/hukum/konflik-polisi-jaksa-berebut-perkara-2062243", "keyword": "websearch", "scraped_from": "websearch", "date": "2025-08-23"},
    {"title": "Konflik Polri vs Kejaksaan dan Bayang-Bayang Intervensi Militer", "snippet": "Polri geledah kafe Ferry Hongkiriwang linked to Jampidsus Febrie Adriansyah. TNI deployed to protect Febrie house. Densus 88 officer kidnapped by Bais TNI. Skema pemerasan korupsi timah, Jiwasraya, laptop Chromebook.", "source": "Infonews", "url": "https://infonews.id/baca-9959-konflik-polri-vs-kejaksaan", "keyword": "websearch", "scraped_from": "websearch", "date": "2026-07-09"},
    {"title": "Peristiwa Jampidsus Kejagung: Membaca Ketegangan Polri, TNI, dan Kejaksaan", "snippet": "Bukan sekadar riak kecil dalam dinamika birokrasi. Ini adalah sinyal kuat adanya pergeseran tektonik dalam relasi kuasa antar-lembaga penegak hukum.", "source": "Sindikatpost", "url": "https://www.sindikatpost.com/opini/peristiwa-jampidsus-kejagung", "keyword": "websearch", "scraped_from": "websearch", "date": "2026-07-09"},
    {"title": "Mengapa Prabowo Tak Kunjung Mengganti Kapolri dan Jaksa Agung", "snippet": "Prabowo Subianto tak mengganti Kapolri dan Jaksa Agung karena dianggap berjasa. Keduanya bakal diganti pada Januari 2026.", "source": "Tempo", "url": "https://www.tempo.co/hukum/pergantian-kapolri-dan-jaksa-agung-2080994", "keyword": "websearch", "scraped_from": "websearch", "date": "2025-10-30"},
    {"title": "Soal Perpres Perlindungan Jaksa, Komjak Bantah Ada Konflik Kejaksaan dengan Polri", "snippet": "Ketua Komjak RI Pujiyono Suwadi menanggapi isu ketidak harmonisan hubungan Kejaksaan dan Polri, seiring terbitnya Perpres 66/2025.", "source": "Kompas", "url": "https://nasional.kompas.com/read/2025/06/06/soal-perpres-perlindungan-jaksa", "keyword": "websearch", "scraped_from": "websearch", "date": "2025-06-06"},
    {"title": "Prabowo Panggil Panglima TNI, Kapolri, hingga Jaksa Agung ke Istana", "snippet": "Presiden RI Prabowo Subianto memanggil Panglima TNI, Kapolri, hingga Jaksa Agung ke Istana Kepresidenan Jakarta.", "source": "CNN Indonesia", "url": "https://www.cnnindonesia.com/nasional/20250827134614-20-1266987", "keyword": "websearch", "scraped_from": "websearch", "date": "2025-08-27"},
    {"title": "Presiden Prabowo Mendadak Panggil Kapolri-Jaksa Agung ke Istana", "snippet": "Presiden Prabowo Subianto mendadak memanggil Kapolri Jenderal Listyo Sigit Prabowo hingga Jaksa Agung ST Burhanuddin di Istana Negara.", "source": "Sindonews", "url": "https://nasional.sindonews.com/read/1600129", "keyword": "websearch", "scraped_from": "websearch", "date": "2025-07-31"},
    {"title": "Penyusunan Kabinet, Penunjukan Jaksa Agung Diingatkan Tak Berafiliasi Parpol", "snippet": "Prabowo diminta tak memilih Jaksa Agung yang berafiliasi dengan partai politik. Putusan MK mensyaratkan Jaksa Agung bukan pengurus parpol.", "source": "MetroTV", "url": "https://www.metrotvnews.com/read/penyusunan-kabinet-penunjukan-jaksa-agung", "keyword": "websearch", "scraped_from": "websearch", "date": "2024-10-15"},
    {"title": "Jaksa Agung dan Kapolri Satukan Persepsi Perkuat Kerja Sama Hadapi KUHP Baru", "snippet": "Jaksa Agung ST Burhanuddin dan Kapolri Jenderal Listyo Sigit Prabowo menyamakan persepsi menghadapi KUHP baru. Pertemuan sinergitas di Mabes Polri.", "source": "Badiklat Kejaksaan", "url": "https://badiklat.kejaksaan.go.id/berita/s/jaksa-agung-dan-kapolri-satukan-persepsi", "keyword": "websearch", "scraped_from": "websearch", "date": "2025-12-16"},
    {"title": "Presiden Prabowo Tunjuk Sanitiar Burhanuddin Sebagai Jaksa Agung 2024-2029", "snippet": "Presiden Prabowo Subianto melantik Sanitiar Burhanuddin sebagai Jaksa Agung berdasarkan Keputusan Presiden Nomor 135/P Tahun 2024.", "source": "Badiklat Kejaksaan", "url": "https://badiklat.kejaksaan.go.id/berita/s/presiden-prabowo-tunjuk-jaksa-agung", "keyword": "websearch", "scraped_from": "websearch", "date": "2024-10-21"},
    {"title": "Kejaksaan Agung Terbitkan Surat Rahasia Meningkatkan Kewaspadaan", "snippet": "Kejaksaan Agung menerbitkan surat rahasia memerintahkan seluruh jajaran Kejati dan Kejari meningkatkan kewaspadaan terhadap Ancaman Gangguan Hambatan Tantangan.", "source": "Infonews", "url": "https://infonews.id/baca-9959", "keyword": "websearch", "scraped_from": "websearch", "date": "2026-07-08"},
    {"title": "Prabowo Panggil Kapolri-Jaksa Agung ke Istana Perintahkan Tindak Tegas Pengoplos Beras", "snippet": "Presiden Prabowo Subianto rapat terbatas bersama Kapolri Jenderal Listyo Sigit Prabowo hingga Jaksa Agung ST Burhanuddin di Istana Negara.", "source": "iNews", "url": "https://www.inews.id/news/nasional/prabowo-panggil-kapolri-jaksa-agung", "keyword": "websearch", "scraped_from": "websearch", "date": "2025-07-31"},
]

data["articles"].extend(websearch_articles)

known_actors = {
    "ST Burhanuddin": "Jaksa Agung", "Burhanuddin": "Jaksa Agung", "Sanitiar Burhanuddin": "Jaksa Agung",
    "Listyo Sigit Prabowo": "Kapolri", "Listyo Sigit": "Kapolri",
    "Febrie Adriansyah": "Jampidsus", "Ferry Hongkiriwang": "Pengusaha/Operator",
    "Prabowo Subianto": "Presiden", "Prabowo": "Presiden",
    "TNI": "Militer", "Densus 88": "Antiteror", "Komisi III DPR": "DPR",
}

data["actor_mentions"] = {}
for article in data["articles"]:
    text = f"{article['title']} {article['snippet']}"
    for actor, role in known_actors.items():
        if actor.lower() in text.lower():
            if actor not in data["actor_mentions"]:
                data["actor_mentions"][actor] = {"role": role, "count": 0, "articles": []}
            data["actor_mentions"][actor]["count"] += 1
            if article["title"] not in data["actor_mentions"][actor]["articles"]:
                data["actor_mentions"][actor]["articles"].append(article["title"][:100])

data["metadata"]["total_articles"] = len(data["articles"])
source_counts = {}
for art in data["articles"]:
    src = art["source"]
    source_counts[src] = source_counts.get(src, 0) + 1
data["statistics"]["by_source"] = source_counts
data["metadata"]["sources"] = list(source_counts.keys())

with open(OUTPUT_DIR / "raw_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Total: {len(data['articles'])} artikel")
print(f"Aktors: {len(data['actor_mentions'])}")
for actor, info in sorted(data["actor_mentions"].items(), key=lambda x: -x[1]["count"])[:12]:
    print(f"  {actor} ({info['role']}): {info['count']}")
