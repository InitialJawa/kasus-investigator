---
name: kasus-investigator
description: Investigasi kasus multi-domain — OSINT, forensik digital, SNA, analisis data, dan keamanan siber. Sistematis, paralel, dan menghasilkan laporan lengkap.
---

# Kasus Investigator 🔍

Skill untuk melakukan investigasi kasus secara sistematis dan terstruktur. Mendukung berbagai jenis investigasi: kejahatan siber, analisis jaringan sosial (SNA), forensik data, OSINT, dan insiden keamanan.

## Kapan Skill Ini Aktif

Gunakan skill ini ketika user:
- Meminta investigasi kasus atau insiden tertentu
- Meminta analisis pola/kejahatan dalam data
- Menyebut "investigasi", "forensik", "analisis kasus", "audit", "sumber terbuka"
- Membutuhkan tracing/traceback suatu kejadian
- Meminta laporan investigasi lengkap

## Fase Investigasi

### Fase 1: Penerimaan Kasus (Intake)

Kumpulkan informasi awal secara sistematis:

1. **Identifikasi Kasus**
   - Apa yang terjadi? (Deskripsi kejadian)
   - Kapan terjadi? (Timeline)
   - Di mana? (Lokasi/scope)
   - Siapa yang terlibat? (Aktor/entitas)
   - Apa dampaknya? (Severity)

2. **Klasifikasi Kasus**
   - `CYBER` — Kejahatan siber, hacking, malware, phishing
   - `OSINT` — Investigasi sumber terbuka, profiling, tracing
   - `SNA` — Analisis jaringan sosial, clustering, influencer mapping
   - `DATA` — Forensik data, anomali detection, pattern analysis
   - `INCIDENT` — Insiden keamanan, breach, unauthorized access
   - `MIXED` — Gabungan beberapa kategori

3. **Definisi Scope**
   - Target investigasi (akun, server, dataset, jaringan)
   - Batasan waktu
   - Sumber data yang tersedia
   - Tool/platform yang bisa digunakan

### Fase 2: Pengumpulan Bukti (Collection)

Kumpulkan semua bukti dan data secara paralel:

1. **Data Sumber Terbuka (OSINT)**
   - Media sosial (Twitter/X, Instagram, TikTok, Telegram)
   - Forum dan komunitas online
   - Public records dan database
   - WHOIS, DNS, IP geolocation
   - Web archive (Wayback Machine)

2. **Data Internal**
   - Log files (application, system, network)
   - Database dumps
   - Email headers
   - File metadata
   - Network traffic captures

3. **Data Jaringan (untuk SNA)**
   - Nodes (akun/pengguna/entitas)
   - Edges (koneksi/interaksi/relasi)
   - Attributes (metadata tiap node)
   - Temporal data (waktu interaksi)

4. **Metode Pengumpulan**
   - Web scraping (playwright, requests)
   - API calls (Twitter API, Telegram API)
   - Log parsing (regex, awk)
   - Packet analysis (Wireshark/tshark)
   - Database queries (SQL)

### Fase 3: Analisis (Analysis)

Lakukan analisis mendalam dengan pendekatan yang sesuai:

1. **Analisis Temporal**
   - Buat timeline kronologis kejadian
   - Identifikasi burst activity (lonjakan aktivitas)
   - Cari pola periodik atau anomali waktu
   - Gunakan: `pandas`, `matplotlib`

2. **Analisis Jaringan (SNA)**
   - Hitung centrality metrics (degree, betweenness, closeness, eigenvector)
   - Deteksi komunitas/clusters (Louvain, Label Propagation)
   - Identifikasi influencer dan bridge nodes
   - Analisis retweet/mention chains
   - Gunakan: `networkx`, `igraph`, `community`

3. **Analisis Sentimen & NLP**
   - Sentimen analysis (positif/negatif/netral)
   - Topic modeling (LDA, BERTopic)
   - Named Entity Recognition (NER)
   - Keyword extraction
   - Gunakan: `transformers`, `spacy`, `nltk`

4. **Analisis Anomali**
   - Statistical outlier detection (Z-score, IQR)
   - Time series anomaly detection
   - Behavioral pattern deviation
   - Gunakan: `scikit-learn`, `isolation forest`

5. **Forensik Digital**
   - File metadata analysis (exiftool)
   - Email header tracing
   - Image forensik (error level analysis)
   - Browser history analysis
   - Gunakan: `exiftool`, `volatility`

### Fase 4: Verifikasi & Korelasi

1. **Cross-Reference**
   - Cocokkan bukti dari berbagai sumber
   - Validasi dengan sumber independen
   - Eliminasi false positives

2. **Korelasi Bukti**
   - Buat hubungan antar bukti
   - Identifikasi chain of evidence
   - Diagram korelasi

3. **Confidence Scoring**
   - `HIGH` (>80%): Bukti kuat, banyak sumber
   - `MEDIUM` (50-80%): Bukti cukup, perlu verifikasi
   - `LOW` (<50%): Bukti lemah, indikatif saja

### Fase 5: Pelaporan (Reporting)

Hasilkan laporan investigasi lengkap:

```markdown
# LAPORAN INVESTIGASI: [Judul Kasus]

## Ringkasan Eksekutif
[1-2 paragraf ringkasan temuan utama]

## Informasi Kasus
- **Klasifikasi:** [CYBER/OSINT/SNA/DATA/INCIDENT]
- **Tanggal Investigasi:** [tanggal]
- **Investigator:** AI Kasus Investigator
- **Confidence Level:** [HIGH/MEDIUM/LOW]

## Temuan Utama
1. [Temuan 1 + bukti]
2. [Temuan 2 + bukti]
3. [Temuan 3 + bukti]

## Timeline Kejadian
| Waktu | Kejadian | Sumber | Confidence |
|-------|----------|--------|------------|
| ...   | ...      | ...    | ...        |

## Analisis
### [Jenis Analisis yang Dilakukan]
[Hasil analisis detail]

## Bukti Pendukung
[Bukti-bukti konkret]

## Kesimpulan
[Penyimpulan berdasarkan bukti]

## Rekomendasi Tindak Lanjut
1. [Rekomendasi 1]
2. [Rekomendasi 2]

## Lampiran
- [Daftar file/data yang dilampirkan]
```

## Tool Default

Gunakan tools berikut sesuai kebutuhan:

| Kebutuhan | Tool |
|-----------|------|
| Web scraping | `playwright`, `requests`, `beautifulsoup4` |
| Data analysis | `pandas`, `numpy`, `scipy` |
| Visualisasi | `matplotlib`, `plotly` |
| SNA | `networkx`, `igraph`, `community` |
| NLP | `transformers`, `spacy`, `nltk` |
| CLI | `curl`, `dig`, `whois`, `nmap` |
| File analysis | `exiftool`, `file`, `strings` |
| Database | `sqlite3`, `pandas` |

## Aturan Penting

1. **Objektivitas** — Selalu berbasis bukti, jangan spekulasi tanpa dasar
2. **Catat Sumber** — Setiap klaim harus ada sumbernya
3. **Privasi** — Jangan mengakses data pribadi tanpa otorisasi yang jelas
4. **Confidence Score** — Selalu berikan skor kepercayaan pada setiap temuan
5. **Audit Trail** — Catat semua langkah investigasi untuk reproducibility
6. **Paralel** — Jalankan pengumpulan dan analisis data secara paralel jika memungkinkan
7. **Bahasa** — Gunakan Bahasa Indonesia untuk semua output

## Modul: Political Investigation

Modul khusus untuk investigasi konflik antar institusi/lembaga politik.

### Trigger
- "Investigasi konflik antara [Institusi A] dan [Institusi B]"
- "Analisis perseteruan lembaga penegak hukum"
- "Politik jabatan", "logistik politik", "transisi kekuasaan"

### Workflow Tambahan

1. **Power Mapping**
   - Identifikasi jabatan strategis yang diperebutkan
   - Mapping loyalis vs oposisi dalam institusi
   - Rotasi mutasi dan dampaknya

2. **Media Framing Analysis**
   - Bagaimana media membingkai konflik?
   - Siapa media yang condong ke kubu tertentu?
   - Pola pemberitaan berulang

3. **Institutional Network**
   - Hubungan lintas institusi (Kejaksaan, Polri, DPR, MK, KPK)
   - Identifikasi bridge nodes (tokoh penghubung)
   - Faksi dalam institusi

4. **Output Khusus**
   - Power map visual (siapa mempengaruhi siapa)
   - Faction analysis (siapa di kubu mana)
   - Conflict timeline (kapan konflik memanas)

### Contoh 1: Investigasi Akun Buzzer
```
User: Investigasi akun @suspicious_akun — kayaknya buzzer politik
Agent:
1. Klasifikasi: SNA + OSINT
2. Kumpulan: Scraping tweet, mention, retweet network
3. Analisis: SNA centrality, temporal pattern, content analysis
4. Hasil: Identifikasi cluster, posting pattern, network influence
```

### Contoh 2: Konflik Antar Institusi
```
User: Investigasi konflik Kejaksaan Agung vs Polri
Agent:
1. Klasifikasi: MIXED (OSINT + SNA + DATA)
2. Kumpulan: Scrape 7+ portal berita, 14 keyword, 2023-2026
3. Analisis: SNA centrality, sentimen, timeline, media framing
4. Output: PDF laporan + TXT sumber + PNG visual mapping
```

### Contoh 3: Analisis Data Trading
```
User: Analisis pola trading mencurigakan di data XYZ
Agent:
1. Klasifikasi: DATA
2. Kumpulan: Load CSV, extract features
3. Anomali: Isolation forest, Z-score, time series
4. Hasil: Identifikasi anomali, cluster trader, pattern
```

## Script Pipeline

Skill ini menyediakan pipeline otomatis:

```bash
# 1. Scrape data
python scripts/scrape.py

# 2. Analisis data
python scripts/analyze.py

# 3. Generate PDF
python scripts/generate_pdf.py

# 4. Generate visual mapping
python scripts/generate_map.py

# Output:
# output/laporan_investigasi.pdf  — Laporan lengkap
# output/sumber_data.txt          — Semua sumber & metadata
# output/mapping_kasus.png        — Visual mapping 4-panel
# output/centrality_ranking.png   — Perankingan aktor
```
