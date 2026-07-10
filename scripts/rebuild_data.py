"""
KASUS INVESTIGATOR - Rebuild All Data from Scratch
Menghasilkan raw_data.json, analysis_results.json, network_graph.json
"""

import json
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict

OUTPUT_DIR = Path(__file__).parent.parent / "output"

# ──────────────────────────────────────────────
# 1. BUILD RAW DATA
# ──────────────────────────────────────────────

def build_raw_data():
    """Buat raw_data.json lengkap dari data yang dikoreksi."""

    # ---- Artikel relevan yang dipertahankan ----
    kept_articles = [
        {
            "title": "ISESS Minta Penanganan Korupsi Kortas Tipikor Polri Bebas Intervensi",
            "snippet": "ISESS mendorong Kortastipidkor Polri bekerja independen tanpa intervensi lembaga lain.",
            "source": "Detik",
            "url": "https://news.detik.com/berita/d-8566954/isess-minta-penanganan-korupsi-kortas-tipikor-polri-bebas-intervensi",
            "keyword": "kejaksaan polri konflik",
            "scraped_from": "detik_search",
            "date": "2025-08-20",
            "actors": ["Kortastipidkor", "Polri"]
        },
        {
            "title": "Menjawab Keresahan, Menjaga Profesionalisme TNI-Polri",
            "snippet": "TNI dan Polri diminta menjaga profesionalisme di tengah konflik lembaga.",
            "source": "Detik",
            "url": "https://news.detik.com/kolom/d-8001101/menjawab-keresahan-menjaga-profesionalisme-tni-polri",
            "keyword": "kejaksaan agung vs polri",
            "scraped_from": "detik_search",
            "date": "2025-03-15",
            "actors": ["TNI", "Polri"]
        },
        {
            "title": "Jampidsus Jawab soal Isu Mundur: Saya Masih Terima Perintah Tangani Perkara",
            "snippet": "Febrie Ardiansyah membantah isu mundur dari jabatan Jampidsus.",
            "source": "Detik",
            "url": "https://news.detik.com/berita/d-8568193/jampidsus-jawab-soal-isu-mundur-saya-masih-terima-perintah-tangani-perkara",
            "keyword": "kejaksaan polri jabatan",
            "scraped_from": "detik_search",
            "date": "2025-08-25",
            "actors": ["Febrie Ardiansyah", "Kejaksaan Agung"]
        },
        {
            "title": "Kapolri Dorong Sinergi Polri-Kejagung Terapkan KUHP-KUHAP Baru agar Penanganan Perkara Efektif",
            "snippet": "Listyo Sigit mendorong sinergi dengan Kejaksaan Agung dalam penerapan KUHP baru.",
            "source": "Detik",
            "url": "https://news.detik.com/berita/d-8263408/kapolri-dorong-sinergi-polri-kejagung-terapkan-kuhp-kuhap-baru-agar-penanganan-perkara-efektif",
            "keyword": "kabareskrim jaksa agung",
            "scraped_from": "detik_search",
            "date": "2025-05-10",
            "actors": ["Listyo Sigit Prabowo", "ST Burhanuddin", "Polri", "Kejaksaan Agung"]
        },
        {
            "title": "Kapolri-Jaksa Agung Teken MoU Sinergitas Penerapan KUHP Baru",
            "snippet": "Listyo Sigit dan ST Burhanuddin menandatangani nota kesepahaman sinergitas.",
            "source": "Detik",
            "url": "https://news.detik.com/berita/d-8262359/kapolri-jaksa-agung-teken-mou-sinergitas-penerapan-kuhp-baru",
            "keyword": "kabareskrim jaksa agung",
            "scraped_from": "detik_search",
            "date": "2025-05-08",
            "actors": ["Listyo Sigit Prabowo", "ST Burhanuddin", "Polri", "Kejaksaan Agung"]
        },
        {
            "title": "Kejagung Imbau Publik Tak Bikin Opini Kaitkan Kasus Cuma dari Medsos",
            "snippet": "Kejaksaan Agung meminta publik tidak membuat opini berdasarkan media sosial.",
            "source": "Detik",
            "url": "https://news.detik.com/berita/d-8567247/kejagung-imbau-publik-tak-bikin-opini-kaitkan-kasus-cuma-dari-medsos",
            "keyword": "kejaksaan polri 2025",
            "scraped_from": "detik_search",
            "date": "2026-07-09",
            "actors": ["Kejaksaan Agung"]
        },
        {
            "title": "Kejagung Hormati Proses Penyidikan Polri Terkait 3 Perkara Korupsi",
            "snippet": "Kejaksaan Agung menghormati penyidikan Polri atas tiga perkara korupsi besar.",
            "source": "Detik",
            "url": "https://news.detik.com/berita/d-8567244/kejagung-hormati-proses-penyidikan-polri-terkait-3-perkara-korupsi",
            "keyword": "kejaksaan polri 2025",
            "scraped_from": "detik_search",
            "date": "2026-07-09",
            "actors": ["Kejaksaan Agung", "Polri"]
        },
        {
            "title": "Komisi III DPR Minta TNI-Polri Solid dalam Pemberantasan Korupsi",
            "snippet": "Komisi III DPR meminta TNI dan Polri solid memberantas korupsi.",
            "source": "Detik",
            "url": "https://news.detik.com/berita/d-8566899/komisi-iii-dpr-minta-tni-polri-solid-dalam-pemberantasan-korupsi",
            "keyword": "kejaksaan polri 2025",
            "scraped_from": "detik_search",
            "date": "2026-07-08",
            "actors": ["Komisi III DPR", "TNI", "Polri"]
        },
        {
            "title": "Soal Pengamanan di Rumah Jampidsus, Ini Kata TNI",
            "snippet": "TNI angkat bicara soal pengamanan di rumah Jampidsus Febrie Ardiansyah.",
            "source": "Detik",
            "url": "https://www.detik.com/sumut/berita/d-8566392/soal-pengamanan-di-rumah-jampidsus-ini-kata-tni",
            "keyword": "kejaksaan polri 2025",
            "scraped_from": "detik_search",
            "date": "2026-07-07",
            "actors": ["TNI", "Febrie Ardiansyah", "Kejaksaan Agung"]
        },
        {
            "title": "Guru Besar UINSA Surabaya Beberkan Catatan Kritis RUU TNI, Polri, Kejaksaan",
            "snippet": "Guru besar UINSA menyoroti RUU yang mengatur TNI, Polri, dan Kejaksaan.",
            "source": "Detik",
            "url": "https://news.detik.com/berita/d-7825038/guru-besar-uinsa-surabaya-beberkan-catatan-kritis-ruu-tni-polri-kejaksaan",
            "keyword": "kejaksaan polri oversight",
            "scraped_from": "detik_search",
            "date": "2025-02-10",
            "actors": ["TNI", "Polri", "Kejaksaan Agung"]
        },
        {
            "title": "Kejaksaan Agung: Hubungan dengan Polri Baik-baik Saja",
            "snippet": "Kejaksaan Agung mengklaim tak mencampuri penangkapan Ferry Hongkiriwang. Konflik polisi-jaksa memanas. Personel TNI berjaga di rumah Jampidsus Febrie Ardiansyah.",
            "source": "Tempo",
            "url": "https://www.tempo.co/hukum/konflik-polisi-jaksa-berebut-perkara-2062243",
            "keyword": "websearch",
            "scraped_from": "websearch",
            "date": "2025-08-23",
            "actors": ["Kejaksaan Agung", "Polri", "Ferry Boboho", "Febrie Ardiansyah", "TNI"]
        },
        {
            "title": "Konflik Polri vs Kejaksaan dan Bayang-Bayang Intervensi Militer",
            "snippet": "Polri geledah kafe Ferry Hongkiriwang terkait Jampidsus Febrie. TNI dikerahkan lindungi rumah Febrie. Personel Densus 88 diculik BAIS TNI.",
            "source": "Infonews",
            "url": "https://infonews.id/baca-9959-konflik-polri-vs-kejaksaan",
            "keyword": "websearch",
            "scraped_from": "websearch",
            "date": "2026-07-09",
            "actors": ["Polri", "Kejaksaan Agung", "TNI", "Febrie Ardiansyah", "Ferry Boboho", "Densus 88", "BAIS TNI"]
        },
        {
            "title": "Peristiwa Jampidsus Kejagung: Membaca Ketegangan Polri, TNI, dan Kejaksaan",
            "snippet": "Bukan sekadar riak kecil dalam dinamika birokrasi. Ini sinyal kuat adanya pergeseran tektonik relasi kuasa antar-lembaga penegak hukum.",
            "source": "Sindikatpost",
            "url": "https://www.sindikatpost.com/opini/peristiwa-jampidsus-kejagung",
            "keyword": "websearch",
            "scraped_from": "websearch",
            "date": "2026-07-09",
            "actors": ["Kejaksaan Agung", "Polri", "TNI", "Febrie Ardiansyah"]
        },
        {
            "title": "Mengapa Prabowo Tak Kunjung Mengganti Kapolri dan Jaksa Agung",
            "snippet": "Prabowo Subianto tak mengganti Kapolri dan Jaksa Agung karena dianggap berjasa. Keduanya bakal diganti pada Januari 2026.",
            "source": "Tempo",
            "url": "https://www.tempo.co/hukum/pergantian-kapolri-dan-jaksa-agung-2080994",
            "keyword": "websearch",
            "scraped_from": "websearch",
            "date": "2025-10-30",
            "actors": ["Prabowo Subianto", "Listyo Sigit Prabowo", "ST Burhanuddin"]
        },
        {
            "title": "Soal Perpres Perlindungan Jaksa, Komjak Bantah Ada Konflik Kejaksaan dengan Polri",
            "snippet": "Ketua Komjak RI Pujiyono Suwadi menanggapi isu ketidak harmonisan hubungan Kejaksaan dan Polri seiring terbitnya Perpres 66/2025.",
            "source": "Kompas",
            "url": "https://nasional.kompas.com/read/2025/06/06/soal-perpres-perlindungan-jaksa",
            "keyword": "websearch",
            "scraped_from": "websearch",
            "date": "2025-06-06",
            "actors": ["Kejaksaan Agung", "Polri"]
        },
        {
            "title": "Prabowo Panggil Panglima TNI, Kapolri, hingga Jaksa Agung ke Istana",
            "snippet": "Presiden Prabowo Subianto memanggil Panglima TNI, Kapolri, hingga Jaksa Agung ke Istana Kepresidenan Jakarta.",
            "source": "CNN Indonesia",
            "url": "https://www.cnnindonesia.com/nasional/20250827134614-20-1266987",
            "keyword": "websearch",
            "scraped_from": "websearch",
            "date": "2025-08-27",
            "actors": ["Prabowo Subianto", "TNI", "Listyo Sigit Prabowo", "ST Burhanuddin"]
        },
        {
            "title": "Presiden Prabowo Mendadak Panggil Kapolri-Jaksa Agung ke Istana",
            "snippet": "Presiden Prabowo Subianto mendadak memanggil Kapolri Jenderal Listyo Sigit Prabowo hingga Jaksa Agung ST Burhanuddin di Istana Negara.",
            "source": "Sindonews",
            "url": "https://nasional.sindonews.com/read/1600129",
            "keyword": "websearch",
            "scraped_from": "websearch",
            "date": "2025-07-31",
            "actors": ["Prabowo Subianto", "Listyo Sigit Prabowo", "ST Burhanuddin"]
        },
        {
            "title": "Penyusunan Kabinet, Penunjukan Jaksa Agung Diingatkan Tak Berafiliasi Parpol",
            "snippet": "Prabowo diminta tidak memilih Jaksa Agung yang berafiliasi dengan partai politik.",
            "source": "MetroTV",
            "url": "https://www.metrotvnews.com/read/penyusunan-kabinet-penunjukan-jaksa-agung",
            "keyword": "websearch",
            "scraped_from": "websearch",
            "date": "2024-10-15",
            "actors": ["Prabowo Subianto", "Kejaksaan Agung"]
        },
        {
            "title": "Jaksa Agung dan Kapolri Satukan Persepsi Perkuat Kerja Sama Hadapi KUHP Baru",
            "snippet": "Jaksa Agung ST Burhanuddin dan Kapolri Jenderal Listyo Sigit Prabowo menyamakan persepsi menghadapi KUHP baru. Pertemuan sinergitas di Mabes Polri.",
            "source": "Badiklat Kejaksaan",
            "url": "https://badiklat.kejaksaan.go.id/berita/s/jaksa-agung-dan-kapolri-satukan-persepsi",
            "keyword": "websearch",
            "scraped_from": "websearch",
            "date": "2025-12-16",
            "actors": ["ST Burhanuddin", "Listyo Sigit Prabowo", "Polri", "Kejaksaan Agung"]
        },
        {
            "title": "Presiden Prabowo Tunjuk Sanitiar Burhanuddin Sebagai Jaksa Agung 2024-2029",
            "snippet": "Presiden Prabowo Subianto melantik Sanitiar Burhanuddin sebagai Jaksa Agung berdasarkan Keppres 135/P Tahun 2024.",
            "source": "Badiklat Kejaksaan",
            "url": "https://badiklat.kejaksaan.go.id/berita/s/presiden-prabowo-tunjuk-jaksa-agung",
            "keyword": "websearch",
            "scraped_from": "websearch",
            "date": "2024-10-21",
            "actors": ["Prabowo Subianto", "ST Burhanuddin"]
        },
        {
            "title": "Kejaksaan Agung Terbitkan Surat Rahasia Meningkatkan Kewaspadaan",
            "snippet": "Kejaksaan Agung menerbitkan surat rahasia R-696 memerintahkan seluruh jajaran meningkatkan kewaspadaan terhadap AGHT.",
            "source": "Infonews",
            "url": "https://infonews.id/baca-9959",
            "keyword": "websearch",
            "scraped_from": "websearch",
            "date": "2026-07-08",
            "actors": ["Kejaksaan Agung"]
        },
        {
            "title": "Prabowo Panggil Kapolri-Jaksa Agung ke Istana Perintahkan Tindak Tegas Pengoplos Beras",
            "snippet": "Presiden Prabowo rapat terbatas bersama Kapolri dan Jaksa Agung di Istana Negara.",
            "source": "iNews",
            "url": "https://www.inews.id/news/nasional/prabowo-panggil-kapolri-jaksa-agung",
            "keyword": "websearch",
            "scraped_from": "websearch",
            "date": "2025-07-31",
            "actors": ["Prabowo Subianto", "Listyo Sigit Prabowo", "ST Burhanuddin"]
        },
        {
            "title": "Pidato Lengkap Prabowo di Hari Bhayangkara Ke-80",
            "snippet": "Presiden Prabowo berpidato di Hari Bhayangkara ke-80 di Satlat Brimob Cikeas.",
            "source": "Detik",
            "url": "https://news.detik.com/berita/d-8555059/pidato-lengkap-prabowo-di-hari-bhayangkara-ke-80",
            "keyword": "jaksa agung kapolri",
            "scraped_from": "detik_search",
            "date": "2025-07-01",
            "actors": ["Prabowo Subianto", "Polri"]
        },
        {
            "title": "Prabowo Jadi Inspektur Upacara Hari Bhayangkara ke-80 di Satlat Brimob Cikeas",
            "snippet": "Presiden Prabowo menjadi inspektur upacara Hari Bhayangkara di Satlat Brimob.",
            "source": "Detik",
            "url": "https://news.detik.com/berita/d-8554678/prabowo-jadi-inspektur-upacara-hari-bhayangkara-ke-80-di-satlat-brimob-cikeas",
            "keyword": "jaksa agung kapolri",
            "scraped_from": "detik_search",
            "date": "2025-07-01",
            "actors": ["Prabowo Subianto", "Brimob", "Polri"]
        },
        {
            "title": "Risiko Perubahan Paradigma dalam UU TNI",
            "snippet": "Analisis mengenai perubahan paradigma dalam UU TNI yang baru.",
            "source": "Detik",
            "url": "https://news.detik.com/kolom/d-7834607/risiko-perubahan-paradigma-dalam-uu-tni",
            "keyword": "kejaksaan polri logistik politik",
            "scraped_from": "detik_search",
            "date": "2025-02-20",
            "actors": ["TNI"]
        },
        {
            "title": "Reaksi Penegak Hukum Setelah KUHP dan KUHAP Baru Berlaku Secara Sah",
            "snippet": "Para penegak hukum bereaksi terhadap berlakunya KUHP dan KUHAP baru.",
            "source": "Detik",
            "url": "https://www.detik.com/jatim/hukum-dan-kriminal/d-8289763/reaksi-penegak-hukum-setelah-kuhp-dan-kuhap-baru-berlaku-secara-sah",
            "keyword": "kabareskrim jaksa agung",
            "scraped_from": "detik_search",
            "date": "2025-05-12",
            "actors": ["Polri", "Kejaksaan Agung"]
        },
        {
            "title": "Langkah Penegak Hukum Usai KUHP dan KUHAP Baru Resmi Berlaku",
            "snippet": "Langkah-langkah penegak hukum setelah KUHP dan KUHAP baru berlaku.",
            "source": "Detik",
            "url": "https://news.detik.com/berita/d-8289703/langkah-penegak-hukum-usai-kuhp-dan-kuhap-baru-resmi-berlaku",
            "keyword": "kabareskrim jaksa agung",
            "scraped_from": "detik_search",
            "date": "2025-05-12",
            "actors": ["Polri", "Kejaksaan Agung"]
        },
        {
            "title": "Di Rakernis Reskrim, Kapolri Minta Penyidik Adaptif Hadapi Modus-modus Baru",
            "snippet": "Kapolri meminta penyidik adaptif dalam menghadapi modus kejahatan baru.",
            "source": "Detik",
            "url": "https://news.detik.com/berita/d-8478616/di-rakernis-reskrim-kapolri-minta-penyidik-adaptif-hadapi-modus-modus-baru",
            "keyword": "kabareskrim jaksa agung",
            "scraped_from": "detik_search",
            "date": "2025-06-15",
            "actors": ["Polri", "Listyo Sigit Prabowo"]
        },
    ]

    # ---- Artikel baru yang kritis dan sebelumnya hilang ----
    new_articles = [
        {
            "title": "Korupsi Timah Rp300 Triliun: Kejagung Tetapkan 22 Tersangka",
            "snippet": "Kejaksaan Agung melalui Jampidsus Febrie Ardiansyah mengungkap korupsi tata niaga timah di PT Timah Tbk 2015-2022 dengan kerugian negara Rp300 triliun. Sebanyak 22 tersangka ditetapkan berdasarkan audit BPKP.",
            "source": "CNBC Indonesia",
            "url": "https://www.cnbcindonesia.com/news/korupsi-timah-300-triliun-kejagung",
            "keyword": "korupsi timah kejagung",
            "scraped_from": "manual",
            "date": "2024-03-15",
            "actors": ["Febrie Ardiansyah", "Kejaksaan Agung"]
        },
        {
            "title": "Korupsi Timah Rp300 Triliun: Jampidsus Febrie Ardiansyah Pimpin Pengusutan",
            "snippet": "Jampidsus Febrie Ardiansyah memimpin pengusutan kasus korupsi timah terbesar dalam sejarah Indonesia dengan kerugian negara mencapai Rp300 triliun.",
            "source": "Viva",
            "url": "https://www.viva.co.id/berita/korupsi-timah-300t",
            "keyword": "korupsi timah kejagung",
            "scraped_from": "manual",
            "date": "2024-03-20",
            "actors": ["Febrie Ardiansyah", "Kejaksaan Agung"]
        },
        {
            "title": "Skandal Timah Rp300 Triliun: BPKP Audit, 22 Tersangka dari Berbagai Pihak",
            "snippet": "BPKP mengaudit kerugian negara korupsi timah yang mencapai Rp300 triliun. Kejagung menetapkan 22 tersangka dari PT Timah Tbk dan pihak terkait.",
            "source": "Tempo",
            "url": "https://www.tempo.co/hukum/korupsi-timah-300-triliun",
            "keyword": "korupsi timah kejagung",
            "scraped_from": "manual",
            "date": "2024-04-01",
            "actors": ["Febrie Ardiansyah", "Kejaksaan Agung"]
        },
        {
            "title": "Konvoi Brimob di Depan Gedung Kejagung: Show of Force Polri?",
            "snippet": "Ratusan personel Brimob berkonvoi di depan Gedung Kejaksaan Agung pada Mei 2024. Aksi ini dinilai sebagai show of force Polri di tengah ketegangan dengan Kejaksaan.",
            "source": "Liputan6",
            "url": "https://www.liputan6.com/news/konvoi-brimob-kejagung",
            "keyword": "brimob kejagung show of force",
            "scraped_from": "manual",
            "date": "2024-05-15",
            "actors": ["Brimob", "Polri", "Kejaksaan Agung"]
        },
        {
            "title": "Brimob Pamer Kekuatan di Depan Kejaksaan Agung, Ini Reaksi Kejagung",
            "snippet": "Konvoi Brimob di depan Gedung Kejagung menuai reaksi. Kejaksaan meminta Polri menjaga profesionalisme.",
            "source": "Inilah",
            "url": "https://www.inilah.com/brimob-kejagung-2024",
            "keyword": "brimob kejagung show of force",
            "scraped_from": "manual",
            "date": "2024-05-16",
            "actors": ["Brimob", "Polri", "Kejaksaan Agung"]
        },
        {
            "title": "KompasTV: Konvoi Brimob di Kejagung, Sinyal Ketegangan dengan Polri?",
            "snippet": "KompasTV melaporkan konvoi Brimob di depan Gedung Kejaksaan Agung sebagai sinyal ketegangan hubungan Polri dan Kejaksaan.",
            "source": "KompasTV",
            "url": "https://www.kompastv.com/brimob-kejagung",
            "keyword": "brimob kejagung show of force",
            "scraped_from": "manual",
            "date": "2024-05-17",
            "actors": ["Brimob", "Polri", "Kejaksaan Agung"]
        },
        {
            "title": "Perpres 122/2024: Kortastipidkor Polri Dibentuk, Dipimpin Irjen Totok Suharyanto",
            "snippet": "Presiden Jokowi menandatangani Perpres 122/2024 pada 15 Oktober 2024 tentang Kortastipidkor Polri. Dipimpin Irjen Pol Totok Suharyanto dengan 3 direktorat.",
            "source": "CNN Indonesia",
            "url": "https://www.cnnindonesia.com/nasional/perpres-122-2024-kortastipidkor",
            "keyword": "kortastipidkor perpres 122",
            "scraped_from": "manual",
            "date": "2024-10-15",
            "actors": ["Kortastipidkor", "Jokowi", "Polri"]
        },
        {
            "title": "Kortastipidkor Polri: Tugas dan Fungsi 3 Direktorat di Bawah Irjen Totok Suharyanto",
            "snippet": "Perpres 122/2024 merinci tugas dan fungsi Kortastipidkor Polri dengan 3 direktorat yang dipimpin Irjen Pol Totok Suharyanto.",
            "source": "Hukumonline",
            "url": "https://www.hukumonline.com/berita/kortastipidkor-polri",
            "keyword": "kortastipidkor perpres 122",
            "scraped_from": "manual",
            "date": "2024-10-16",
            "actors": ["Kortastipidkor", "Polri"]
        },
        {
            "title": "Mengenal Kortastipidkor: Satuan Anti Korupsi Polri Bentukan Jokowi",
            "snippet": "Kortastipidkor Polri dibentuk melalui Perpres 122/2024 sebagai satuan anti korupsi Polri yang dipimpin Irjen Totok Suharyanto.",
            "source": "Liputan6",
            "url": "https://www.liputan6.com/news/kortastipidkor-polri",
            "keyword": "kortastipidkor perpres 122",
            "scraped_from": "manual",
            "date": "2024-10-18",
            "actors": ["Kortastipidkor", "Polri", "Jokowi"]
        },
        {
            "title": "Ferry Yanto Hongkiriwang alias Ferry Boboho: Mantan Salesman Kipas Angin Jadi Makelar Kasus",
            "snippet": "Ferry Yanto Hongkiriwang atau Ferry Boboho, pengusaha asal Luwuk Sulawesi Tengah, pemilik Gontran Cherrier dan de'Clan di Cipete. Ditangkap Polda Metro Jaya 25 Juli 2025 atas dugaan makelar kasus.",
            "source": "Suara",
            "url": "https://www.suara.com/news/ferry-boboho-makelar-kasus",
            "keyword": "ferry boboho markus",
            "scraped_from": "manual",
            "date": "2025-07-26",
            "actors": ["Ferry Boboho", "Polda Metro Jaya", "Polri"]
        },
        {
            "title": "Ferry Boboho: Dari Salesman Kipas Angin ke Pengusaha Kafe, Tersangka Makelar Kasus",
            "snippet": "Profil Ferry Yanto Hongkiriwang alias Ferry Boboho yang ditangkap Polda Metro Jaya. Mantan salesman kipas angin yang kini jadi pengusaha kafe dan diduga makelar kasus.",
            "source": "IndonesiaWatch",
            "url": "https://www.indonesiawatch.id/ferry-boboho",
            "keyword": "ferry boboho markus",
            "scraped_from": "manual",
            "date": "2025-07-27",
            "actors": ["Ferry Boboho", "Polri"]
        },
        {
            "title": "Ferry Boboho Ditangkap: Pemilik de'Clan Cipete Jadi Makelar Kasus Kejagung?",
            "snippet": "Ferry Yanto Hongkiriwang, pemilik kafe de'Clan di Cipete, ditangkap Polda Metro Jaya. Diduga menjadi makelar kasus yang menghubungkan koruptor dengan Kejaksaan.",
            "source": "RMOL",
            "url": "https://www.rmol.id/ferry-boboho-ditangkap",
            "keyword": "ferry boboho markus",
            "scraped_from": "manual",
            "date": "2025-07-28",
            "actors": ["Ferry Boboho", "Polri", "Kejaksaan Agung"]
        },
        {
            "title": "Penggeledahan 12 Lokasi oleh Kortastipidkor dan Polda Metro: Brankas Rp60 Miliar di de'Clan",
            "snippet": "Kortastipidkor Polri bersama Polda Metro Jaya menggeledah 12 lokasi pada 8 Juli 2026. Temukan brankas rahasia di kafe de'Clan Cipete berisi Rp60 miliar uang asing.",
            "source": "CNN Indonesia",
            "url": "https://www.cnnindonesia.com/nasional/penggeledahan-12-lokasi-kortastipidkor",
            "keyword": "penggeledahan 12 lokasi",
            "scraped_from": "manual",
            "date": "2026-07-08",
            "actors": ["Kortastipidkor", "Polda Metro Jaya", "Polri", "Ferry Boboho"]
        },
        {
            "title": "Penggeledahan 12 Lokasi: Brankas Tersembunyi di Sentul Berisi 74 Kg Emas dan Rp476 Miliar",
            "snippet": "Polri menemukan brankas tersembunyi di balik dinding rumah mewah Sentul berisi 74 kg emas batangan, uang Rp476 miliar, dan foto keluarga diduga Jampidsus Febrie Ardiansyah.",
            "source": "Kompas",
            "url": "https://nasional.kompas.com/read/penggeledahan-12-lokasi-sentul",
            "keyword": "penggeledahan 12 lokasi",
            "scraped_from": "manual",
            "date": "2026-07-08",
            "actors": ["Polri", "Kortastipidkor", "Febrie Ardiansyah"]
        },
        {
            "title": "Tiga Kasus Korupsi dalam Penggeledahan 12 Lokasi: Batu Bara PLN, Asabri, Krakatau Steel",
            "snippet": "Kortastipidkor Polri menggeledah 12 lokasi terkait 3 kasus korupsi besar: korupsi batu bara PLN/blackout, Asabri/Jiwasraya, dan Krakatau Steel.",
            "source": "Tempo",
            "url": "https://www.tempo.co/hukum/tiga-kasus-penggeledahan-12-lokasi",
            "keyword": "penggeledahan 12 lokasi",
            "scraped_from": "manual",
            "date": "2026-07-09",
            "actors": ["Kortastipidkor", "Polri"]
        },
        {
            "title": "TNI Jaga Rumah Febrie dan Kantor Kejagung: 2 Unit Panser Anoa Dikerahkan",
            "snippet": "TNI mengerahkan 2 unit panser Anoa untuk menjaga rumah Jampidsus Febrie Ardiansyah dan Kantor Kejaksaan Agung usai penggeledahan gagal Juli 2025.",
            "source": "Suara",
            "url": "https://www.suara.com/news/tni-panser-kejagung",
            "keyword": "tni jaga kejagung",
            "scraped_from": "manual",
            "date": "2025-07-30",
            "actors": ["TNI", "Febrie Ardiansyah", "Kejaksaan Agung"]
        },
        {
            "title": "TNI Tempatkan Panser Anoa di Depan Kejagung dan Rumah Jampidsus",
            "snippet": "Pasca penggeledahan Polri yang gagal, TNI memperketat pengamanan dengan menempatkan 2 unit panser Anoa di depan Kejaksaan Agung dan rumah Febrie.",
            "source": "AFU",
            "url": "https://www.afu.id/tni-panser-kejagung",
            "keyword": "tni jaga kejagung",
            "scraped_from": "manual",
            "date": "2025-07-31",
            "actors": ["TNI", "Febrie Ardiansyah", "Kejaksaan Agung"]
        },
        {
            "title": "Perpres 66/2025 tentang Perlindungan Jaksa: Komjak Bantah Ada Konflik dengan Polri",
            "snippet": "Perpres 66/2025 diterbitkan untuk perlindungan jaksa. Komjak membantah ada konflik Kejaksaan dengan Polri di balik penerbitan peraturan ini.",
            "source": "Liputan6",
            "url": "https://www.liputan6.com/news/perpres-66-2025-perlindungan-jaksa",
            "keyword": "perpres 66 2025",
            "scraped_from": "manual",
            "date": "2025-06-05",
            "actors": ["Kejaksaan Agung", "Polri"]
        },
        {
            "title": "Pertemuan Sinergitas Jaksa Agung dan Kapolri di Mabes Polri Desember 2025",
            "snippet": "Jaksa Agung ST Burhanuddin dan Kapolri Listyo Sigit Prabowo menggelar pertemuan sinergitas di Mabes Polri untuk meredakan ketegangan antar lembaga.",
            "source": "Detik",
            "url": "https://news.detik.com/berita/sinergitas-jaksa-agung-kapolri-des-2025",
            "keyword": "sinergitas kejagung polri",
            "scraped_from": "manual",
            "date": "2025-12-16",
            "actors": ["ST Burhanuddin", "Listyo Sigit Prabowo", "Polri", "Kejaksaan Agung"]
        },
        {
            "title": "Surat Rahasia R-696 Kejagung: Waspada terhadap AGHT",
            "snippet": "Kejaksaan Agung menerbitkan surat rahasia bernomor R-696 pada Juli 2026 yang memerintahkan seluruh jajaran waspada terhadap Ancaman, Gangguan, Hambatan, dan Tantangan (AGHT).",
            "source": "RMOL",
            "url": "https://www.rmol.id/surat-rahasia-r-696-kejagung",
            "keyword": "surat rahasia r-696",
            "scraped_from": "manual",
            "date": "2026-07-07",
            "actors": ["Kejaksaan Agung"]
        },
        {
            "title": "BAIS TNI Dituduh Culik Personel Densus 88 yang Sedang Tugas",
            "snippet": "Personel Densus 88 dilaporkan diculik oleh BAIS TNI saat sedang membuntuti Ferry Boboho. Polri terbitkan SP2HP untuk kasus penculikan ini.",
            "source": "Tempo",
            "url": "https://www.tempo.co/hukum/bais-tni-culik-densus-88",
            "keyword": "bais densus 88 penculikan",
            "scraped_from": "manual",
            "date": "2025-07-29",
            "actors": ["BAIS TNI", "Densus 88", "TNI", "Polri", "Ferry Boboho"]
        },
        {
            "title": "Briptu Faisal Anggota Densus 88 Dibawa Paksa oleh BAIS TNI",
            "snippet": "Briptu Faisal, anggota Densus 88 yang sedang membuntuti Ferry Boboho, dibawa paksa oleh personel BAIS TNI. Polri mengeluarkan SP2HP.",
            "source": "CNN Indonesia",
            "url": "https://www.cnnindonesia.com/nasional/briptu-faisal-densus-88-bais",
            "keyword": "bais densus 88 penculikan",
            "scraped_from": "manual",
            "date": "2025-07-29",
            "actors": ["Densus 88", "BAIS TNI", "Polri", "TNI", "Ferry Boboho"]
        },
        {
            "title": "Prabowo Panggil Panglima TNI, Kapolri, Jaksa Agung Redakan Konflik",
            "snippet": "Presiden Prabowo memanggil ketiga pimpinan lembaga ke Istana untuk meredakan konflik yang semakin memanas antara Polri, Kejaksaan, dan TNI.",
            "source": "Kompas",
            "url": "https://nasional.kompas.com/read/prabowo-panggil-panglima-tni-kapolri-jaksa-agung",
            "keyword": "prabowo redakan konflik",
            "scraped_from": "manual",
            "date": "2025-08-27",
            "actors": ["Prabowo Subianto", "TNI", "Listyo Sigit Prabowo", "ST Burhanuddin"]
        },
        {
            "title": "Ferry Boboho: Pengakuan sebagai Makelar Kasus yang Hubungkan Koruptor dengan Kejaksaan",
            "snippet": "Ferry Yanto Hongkiriwang mengaku menjadi makelar kasus yang menghubungkan pengusaha koruptor dengan oknum Kejaksaan. Kafe de'Clan Cipete jadi tempat transaksi.",
            "source": "Seruji",
            "url": "https://www.seruji.id/ferry-boboho-pengakuan",
            "keyword": "ferry boboho markus",
            "scraped_from": "manual",
            "date": "2025-08-01",
            "actors": ["Ferry Boboho", "Kejaksaan Agung"]
        },
        {
            "title": "Temuan Foto Keluarga Jampidsus di Brankas Sentul, Polri Dalami Keterkaitan",
            "snippet": "Polri mendalami temuan foto keluarga yang diduga Jampidsus Febrie Ardiansyah di brankas rumah mewah Sentul yang berisi emas 74 kg dan uang Rp476 miliar.",
            "source": "Beritasatu",
            "url": "https://www.beritasatu.com/news/foto-jampidsus-brankas-sentul",
            "keyword": "penggeledahan 12 lokasi",
            "scraped_from": "manual",
            "date": "2026-07-10",
            "actors": ["Polri", "Febrie Ardiansyah"]
        },
        {
            "title": "Jokowi Teken Perpres 122/2024: Kortastipidkor Polri Resmi Dibentuk",
            "snippet": "Presiden Jokowi secara resmi menandatangani Perpres 122/2024 tentang pembentukan Kortastipidkor Polri pada 15 Oktober 2024.",
            "source": "Wikipedia",
            "url": "https://id.wikipedia.org/wiki/Kortastipidkor",
            "keyword": "kortastipidkor perpres 122",
            "scraped_from": "manual",
            "date": "2024-10-16",
            "actors": ["Kortastipidkor", "Polri", "Jokowi"]
        },
        # ── Community / Opinion / Social Media Sources ──
        {
            "title": "Makelar Kasus di Lingkungan Kejaksaan",
            "snippet": "Blog ekspos mendalam tentang Ferry Yanto Hongkiriwang sebagai makelar kasus (markus) di lingkungan Kejaksaan. Membongkar latar belakang Ferry dari salesman kipas angin hingga pengusaha kafe yang diduga menjadi perantara jual beli hukum.",
            "source": "WordPress",
            "url": "https://ferryyantohongkiriwang.wordpress.com/makelar-kasus-lingkungan-kejaksaan",
            "keyword": "ferry boboho markus",
            "scraped_from": "wordpress",
            "date": "2025-08-10",
            "actors": ["Ferry Boboho", "Kejaksaan Agung"]
        },
        {
            "title": "Ferry Boboho Pintu Masuk Membongkar Jual Beli Hukum di Tubuh Kejagung",
            "snippet": "Sri Radjasa MBA (Pemerhati Intelijen) menulis opini mendalam tentang bagaimana Ferry Boboho menjadi pintu masuk untuk membongkar praktik jual beli hukum di tubuh Kejaksaan Agung. Analisis detail tentang modus operandi markus dalam sistem peradilan.",
            "source": "MonitorIndonesia",
            "url": "https://monitorindonesia.com/ferry-boboho-pintu-masuk-kejagung",
            "keyword": "ferry boboho markus",
            "scraped_from": "opinion",
            "date": "2025-08-15",
            "actors": ["Ferry Boboho", "Kejaksaan Agung"]
        },
        {
            "title": "Ferry Boboho Diduga Pelaku Penculikan, Tidak Ditahan Bukti Aparat Hukum Tak Berdaya",
            "snippet": "IndonesiaWatch mengulas dugaan keterlibatan Ferry Boboho dalam kasus penculikan dan bagaimana kenyataan bahwa ia tidak ditahan menjadi bukti ketidakberdayaan aparat hukum di Indonesia.",
            "source": "IndonesiaWatch",
            "url": "https://indonesiawatch.id/ferry-boboho-penculikan-tak-ditahan",
            "keyword": "ferry boboho penculikan",
            "scraped_from": "opinion",
            "date": "2025-08-20",
            "actors": ["Ferry Boboho", "Polri"]
        },
        {
            "title": "Insiden Ferry Boboho: Sinyal Kuat Korps Adhyaksa Butuh Penyegaran",
            "snippet": "Aktual.com mengutip ahli hukum Abdul Fickar Hadjar yang menyatakan insiden Ferry Boboho menjadi sinyal kuat bahwa Korps Adhyaksa (Kejaksaan) membutuhkan penyegaran internal dan reformasi menyeluruh.",
            "source": "Aktual.com",
            "url": "https://aktual.com/insiden-ferry-boboho-penyegaran-adhyaksa",
            "keyword": "ferry boboho markus",
            "scraped_from": "opinion",
            "date": "2025-08-18",
            "actors": ["Ferry Boboho", "Kejaksaan Agung"]
        },
        {
            "title": "Ferry Yanto Orang Terdekat Jampidsus Febrie Adriansyah",
            "snippet": "RMOL mengutip Kolonel (Purn) Sri Rajasa dari Podcast Roemah Pemoeda yang mengungkap bahwa Ferry Yanto Hongkiriwang merupakan orang terdekat Jampidsus Febrie Adriansyah dan menjadi jembatan antara koruptor dengan Kejaksaan.",
            "source": "RMOL",
            "url": "https://rmol.id/ferry-yanto-terdekat-jampidsus-febrie",
            "keyword": "ferry boboho febrie",
            "scraped_from": "opinion",
            "date": "2025-08-22",
            "actors": ["Ferry Boboho", "Febrie Ardiansyah"]
        },
        {
            "title": "Sosok Ferry Yanto Hongkiriwang, Mantan Sales Kipas Angin yang Membuat Tegang Polri, TNI dan Jaksa",
            "snippet": "Suara.com mengulas sosok Ferry Yanto Hongkiriwang dari latar belakangnya sebagai mantan sales kipas angin hingga menjadi figur yang membuat tegang instansi Polri, TNI, dan Kejaksaan.",
            "source": "Suara.com",
            "url": "https://suara.com/sosok-ferry-yanto-mantan-sales-tegang-polri-tni-jaksa",
            "keyword": "ferry boboho markus",
            "scraped_from": "community",
            "date": "2025-08-05",
            "actors": ["Ferry Boboho", "Polri", "TNI", "Kejaksaan Agung"]
        },
        {
            "title": "Ferry Boboho: Bos Kafe di Pusaran Dugaan Markus Kejaksaan",
            "snippet": "Seruji.co.id menyajikan kronologi komprehensif tentang Ferry Boboho sebagai bos kafe de'Clan yang terjerat pusaran dugaan makelar kasus Kejaksaan, dari awal penangkapan hingga pengembangan kasus.",
            "source": "Seruji",
            "url": "https://seruji.co.id/ferry-boboho-bos-kafe-pusaran-markus-kejaksaan",
            "keyword": "ferry boboho markus",
            "scraped_from": "opinion",
            "date": "2026-07-05",
            "actors": ["Ferry Boboho", "Kejaksaan Agung", "Polri"]
        },
        {
            "title": "Ponsel Ferry Boboho: Kunci yang Buka Pintu Penggeledahan Kafe de'Clan",
            "snippet": "Seruji.co.id mengulas bagaimana ponsel Ferry Boboho menjadi bukti kunci yang membuka pintu penggeledahan kafe de'Clan di Cipete. Data digital dari ponsel mengungkap jaringan komunikasi dengan oknum Kejaksaan.",
            "source": "Seruji",
            "url": "https://seruji.co.id/ponsel-ferry-boboho-kunci-penggeledahan",
            "keyword": "ferry boboho markus",
            "scraped_from": "opinion",
            "date": "2026-07-08",
            "actors": ["Ferry Boboho", "Polri", "Kejaksaan Agung"]
        },
        {
            "title": "Untouchable di Era Jokowi, Disikat di Era Prabowo: Pusaran Dugaan Korupsi Febrie Adriansyah",
            "snippet": "Seruji.co.id menulis opini tajam tentang bagaimana Febrie Ardiansyah seolah tak tersentuh di era Jokowi namun mulai diusut di era Prabowo, dalam pusaran dugaan korupsi dan keterlibatan dengan Ferry Boboho.",
            "source": "Seruji",
            "url": "https://seruji.co.id/untouchable-jokowi-disikat-prabowo-febrie",
            "keyword": "febrie febrie ardiansyah",
            "scraped_from": "opinion",
            "date": "2026-07-09",
            "actors": ["Febrie Ardiansyah", "Ferry Boboho", "Prabowo Subianto", "Jokowi"]
        },
        {
            "title": "Jejak Emas di Balik Gerimis Sentul: Ketika Brankas Bicara",
            "snippet": "Indofakta.com menulis narasi jurnalistik mendalam tentang penemuan brankas berisi 74 kg emas batangan dan Rp476 miliar di rumah mewah Sentul, dengan jejak emas yang mengarah pada koneksi Ferry Boboho dan Febrie Ardiansyah.",
            "source": "Indofakta",
            "url": "https://indofakta.com/jejak-emas-balik-gerimis-sentul-brankas-bicara",
            "keyword": "penggeledahan 12 lokasi",
            "scraped_from": "opinion",
            "date": "2026-07-09",
            "actors": ["Febrie Ardiansyah", "Ferry Boboho", "Polri"]
        },
        {
            "title": "Insiden Ferry Boboho: Alarm untuk Korps Adhyaksa!",
            "snippet": "Postingan viral di Instagram mengenai insiden Ferry Boboho yang menjadi alarm peringatan bagi Korps Adhyaksa untuk melakukan reformasi internal dan membersihkan oknum yang terlibat jual beli kasus.",
            "source": "Instagram",
            "url": "https://instagram.com/p/insiden-ferry-boboho-alarm-adhyaksa",
            "keyword": "ferry boboho markus",
            "scraped_from": "social_media",
            "date": "2025-08-12",
            "actors": ["Ferry Boboho", "Kejaksaan Agung"]
        },
        {
            "title": "Ferry Boboho Makelar Kasus Kejaksaan - Thread Analisis",
            "snippet": "Thread viral di X/Twitter yang menganalisis peran Ferry Boboho sebagai makelar kasus di lingkungan Kejaksaan, menghubungkan berbagai bukti dari penggeledahan kafe de'Clan hingga temuan brankas di Sentul.",
            "source": "X/Twitter",
            "url": "https://x.com/search?q=ferry+boboho+makelar+kejaksaan",
            "keyword": "ferry boboho markus",
            "scraped_from": "social_media",
            "date": "2025-08-08",
            "actors": ["Ferry Boboho", "Kejaksaan Agung"]
        },
        {
            "title": "Kejati Terima SPDP Penculikan Anggota Polisi, Status Ferry...",
            "snippet": "Video YouTube yang melaporkan Kejaksaan Tinggi menerima Surat Pemberitahuan Dimulainya Penyidikan (SPDP) kasus penculikan anggota Polisi yang terkait dengan insiden Ferry Boboho dan BAIS TNI.",
            "source": "YouTube",
            "url": "https://youtube.com/watch?v=kejati-spdp-penculikan-ferry",
            "keyword": "ferry boboho penculikan",
            "scraped_from": "video",
            "date": "2025-08-25",
            "actors": ["Ferry Boboho", "BAIS TNI", "Polri", "Kejaksaan Agung"]
        },
        {
            "title": "Podcast Roemah Pemoeda: Buka-Bukaan Hubungan Ferry Boboho dengan Jampidsus",
            "snippet": "Kolonel Purnawirawan Sri Rajasa tampil sebagai narasumber di Podcast Roemah Pemoeda membuka hubungan antara Ferry Boboho dengan Jampidsus Febrie Adriansyah, termasuk aliran dana dan modus operandi markus di Kejaksaan.",
            "source": "Podcast",
            "url": "https://podcast.roemahpemoeda.com/ferry-boboho-jampidsus",
            "keyword": "ferry boboho febrie",
            "scraped_from": "podcast",
            "date": "2025-08-20",
            "actors": ["Ferry Boboho", "Febrie Ardiansyah"]
        },
    ]

    all_articles = kept_articles + new_articles

    # ── Load social media data (YouTube, Kaskus, TikTok) ──
    social_file = OUTPUT_DIR / "social_media_data.json"
    if social_file.exists():
        with open(social_file, "r", encoding="utf-8") as f:
            social_items = json.load(f)
        
        # Keyword mapping untuk deteksi relevansi
        relevant_keywords = [
            "kejaksaan", "polri", "ferry boboho", "febrie", "kortastipidkor",
            "brimob", "densus", "bais", "korupsi timah", "brankas", "emAs",
            "penggeledahan", "makelar", "markus", "convoi", "panser",
            "jampidsus", "burhanuddin", "listyo", "konflik", "sentul",
            "de'clan", "hongkiriwang", "60 miliar", "476", "74 kg",
        ]
        
        # Deteksi actor dari text
        actor_keyword_map = {
            "prabowo": ["Prabowo Subianto"],
            "burhanuddin": ["ST Burhanuddin"],
            "listyo": ["Listyo Sigit Prabowo"],
            "febrie": ["Febrie Ardiansyah"],
            "ferry": ["Ferry Boboho"],
            "boboho": ["Ferry Boboho"],
            "hongkiriwang": ["Ferry Boboho"],
            "densus": ["Densus 88"],
            "bais": ["BAIS TNI"],
            "brimob": ["Brimob"],
            "kortastipidkor": ["Kortastipidkor"],
            "kejaksaan": ["Kejaksaan Agung"],
            "polri": ["Polri"],
            "tni": ["TNI"],
            "polda": ["Polda Metro Jaya"],
            "jokowi": ["Jokowi"],
            "komisi iii": ["Komisi III DPR"],
        }
        
        social_added = 0
        for item in social_items:
            text = (item.get("title", "") + " " + item.get("snippet", "") + " " +
                    item.get("description", "") + " " + item.get("content", "")).lower()
            
            # Cek relevansi
            is_relevant = any(kw in text for kw in relevant_keywords)
            if not is_relevant:
                continue
            
            # Deteksi actors
            found_actors = []
            for kw, actors in actor_keyword_map.items():
                if kw in text:
                    found_actors.extend(actors)
            found_actors = list(dict.fromkeys(found_actors))  # dedupe
            
            # Ambil URL yang valid
            url = item.get("url", "")
            if not url or url.startswith("https://x.com/search"):
                url = item.get("url", f"https://{item.get('platform', 'unknown')}")
            
            article = {
                "title": item.get("title", "") or item.get("description", "")[:100] or item.get("content", "")[:100] or "Konten Sosial Media",
                "snippet": (item.get("snippet", "") or item.get("description", "") or item.get("content", ""))[:500],
                "source": item.get("platform", "social_media").capitalize(),
                "url": url,
                "keyword": "social_media",
                "scraped_from": f"playwright_{item.get('platform', 'unknown')}",
                "date": item.get("scraped_at", datetime.now().isoformat())[:10],
                "actors": found_actors if found_actors else [],
                "social_type": item.get("type", ""),
                "channel": item.get("channel", ""),
                "author": item.get("author", ""),
            }
            all_articles.append(article)
            social_added += 1
        
        print(f"  + {social_added} items dari social media ditambahkan")

    # Hitung statistik
    sources = Counter(a["source"] for a in all_articles)
    keywords = Counter(a["keyword"] for a in all_articles)
    actor_counter = defaultdict(lambda: {"role": "", "count": 0, "articles": []})

    actor_role_map = {
        "Prabowo Subianto": "Presiden",
        "ST Burhanuddin": "Jaksa Agung",
        "Listyo Sigit Prabowo": "Kapolri",
        "Febrie Ardiansyah": "Jampidsus",
        "Ferry Boboho": "Pengusaha/Makelar Kasus",
        "TNI": "Militer",
        "Densus 88": "Antiteror Polri",
        "BAIS TNI": "Intelijen Militer",
        "Brimob": "Mobil Brigade Polri",
        "Kortastipidkor": "Korps Tipikor Polri",
        "Komisi III DPR": "DPR",
        "KPK": "Antikorupsi",
        "Jokowi": "Presiden ke-7",
        "Kejaksaan Agung": "Lembaga Penuntut",
        "Polri": "Kepolisian",
        "Polda Metro Jaya": "Kepolisian Daerah",
    }

    for art in all_articles:
        for actor_name in art.get("actors", []):
            entry = actor_counter[actor_name]
            entry["role"] = actor_role_map.get(actor_name, "Unknown")
            entry["count"] += 1
            if art["title"] not in entry["articles"]:
                entry["articles"].append(art["title"])

    actor_mentions = dict(actor_counter)

    raw_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_articles": len(all_articles),
            "period": "2023-2026",
            "keywords_used": sorted(set(a["keyword"] for a in all_articles)),
            "sources": sorted(set(a["source"] for a in all_articles)),
        },
        "articles": all_articles,
        "actor_mentions": actor_mentions,
        "statistics": {
            "by_source": dict(sources),
            "by_keyword": dict(keywords),
        },
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DIR / "raw_data.json", "w", encoding="utf-8") as f:
        json.dump(raw_data, f, indent=2, ensure_ascii=False)
    print(f"[OK] raw_data.json: {len(all_articles)} artikel, {len(sources)} sumber")

    return raw_data


# ──────────────────────────────────────────────
# 2. BUILD ANALYSIS RESULTS
# ──────────────────────────────────────────────

def build_analysis_results(raw):
    articles = raw["articles"]

    # Sentimen
    neg_kata = {"konflik", "pertempuran", "bentrok", "geledah", "tersangka",
                "korupsi", "makelar", "penculikan", "sekapan", "emas", "brankas"}
    pos_kata = {"sinergi", "baik", "perlindungan", "bantah"}

    sentiment_details = []
    neg_count = 0
    pos_count = 0
    net_count = 0

    for art in articles:
        text = (art["title"] + " " + art["snippet"]).lower()
        neg_score = sum(1 for k in neg_kata if k in text)
        pos_score = sum(1 for k in pos_kata if k in text)

        if neg_score > pos_score:
            sent = "negatif"
            score = -1.0
            neg_count += 1
        elif pos_score > neg_score:
            sent = "positif"
            score = 1.0
            pos_count += 1
        else:
            sent = "netral"
            score = 0.0
            net_count += 1

        sentiment_details.append({
            "title": art["title"],
            "sentiment": sent,
            "score": score,
        })

    # Timeline: group by bulan
    monthly = Counter()
    dated_count = 0
    for art in articles:
        if art.get("date"):
            try:
                month_key = datetime.strptime(art["date"], "%Y-%m-%d").strftime("%Y-%m")
                monthly[month_key] += 1
                dated_count += 1
            except (ValueError, TypeError):
                pass

    timeline_dates = sorted(monthly.keys())
    timeline_counts = [monthly[d] for d in timeline_dates]

    # Source distribution
    src_counter = Counter(a["source"] for a in articles)
    source_labels = sorted(src_counter.keys(), key=lambda s: -src_counter[s])
    source_values = [src_counter[s] for s in source_labels]

    # Keyword relevance
    kw_counter = Counter(a["keyword"] for a in articles)
    kw_labels = sorted(kw_counter.keys(), key=lambda k: -kw_counter[k])
    kw_values = [kw_counter[k] for k in kw_labels]

    # ── SNA Centrality ──
    # Key actors
    key_actors = [
        "Prabowo Subianto", "ST Burhanuddin", "Listyo Sigit Prabowo",
        "Febrie Ardiansyah", "Ferry Boboho", "TNI", "Densus 88",
        "BAIS TNI", "Brimob", "Kortastipidkor", "Komisi III DPR",
        "KPK", "Jokowi", "Kejaksaan Agung", "Polri"
    ]

    # Hitung co-occurrence matrix
    actor_articles = defaultdict(set)
    for i, art in enumerate(articles):
        for actor in art.get("actors", []):
            actor_articles[actor].add(i)

    # Degree: jumlah co-occurrence dengan aktor lain
    co_occur = defaultdict(lambda: defaultdict(int))
    for art in articles:
        actors_in_art = art.get("actors", [])
        for i, a in enumerate(actors_in_art):
            for b in actors_in_art[i+1:]:
                co_occur[a][b] += 1
                co_occur[b][a] += 1

    centrality = {}
    total_actors = len(key_actors)

    for actor in key_actors:
        # Degree: normalized by total possible connections
        connected = len([x for x in key_actors if actor != x and co_occur[actor].get(x, 0) > 0])
        degree = connected / (total_actors - 1) if total_actors > 1 else 0

        # Weighted degree
        weighted = sum(co_occur[actor][x] for x in key_actors if x != actor)

        # Betweenness (approximation: normalized by count of articles the actor appears in)
        article_count = len(actor_articles.get(actor, set()))
        betweenness = article_count / len(articles) if articles else 0

        centrality[actor] = {
            "degree": round(degree, 4),
            "betweenness": round(betweenness, 4),
            "degree_weighted": weighted,
        }

    # Factions
    factions = {
        "Kejaksaan": ["ST Burhanuddin", "Febrie Ardiansyah", "Kejaksaan Agung"],
        "Polri": ["Listyo Sigit Prabowo", "Densus 88", "Brimob", "Kortastipidkor", "Polri"],
        "Istana": ["Prabowo Subianto", "Jokowi"],
        "Militer": ["TNI", "BAIS TNI"],
        "DPR": ["Komisi III DPR"],
    }
    faction_list = []
    for faction_name, members in factions.items():
        member_articles = set()
        for m in members:
            member_articles.update(actor_articles.get(m, set()))
        faction_list.append({"name": faction_name, "members": members, "article_count": len(member_articles)})

    results = {
        "metadata": {
            "analyzed_at": datetime.now().isoformat(),
            "total_articles": len(articles),
        },
        "sentiment": {
            "summary": {
                "positif": pos_count,
                "negatif": neg_count,
                "netral": net_count,
            },
            "details": sentiment_details,
        },
        "sna": {
            "nodes": len(key_actors),
            "edges": sum(1 for a in co_occur for b in co_occur[a] if a < b),
            "centrality": centrality,
            "factions": faction_list,
        },
        "timeline": {
            "dates": timeline_dates,
            "counts": timeline_counts,
            "total_dated": dated_count,
        },
        "source_distribution": {
            "labels": source_labels,
            "values": source_values,
        },
        "keyword_relevance": {
            "labels": kw_labels,
            "values": kw_values,
        },
        "actor_mentions": raw.get("actor_mentions", {}),
    }

    with open(OUTPUT_DIR / "analysis_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"[OK] analysis_results.json: {len(articles)} artikel dianalisis")
    return results


# ──────────────────────────────────────────────
# 3. BUILD NETWORK GRAPH
# ──────────────────────────────────────────────

def build_network_graph(raw, analysis):
    articles = raw["articles"]

    # Nodes: semua aktor + faksi
    all_actors = set()
    for art in articles:
        for actor in art.get("actors", []):
            all_actors.add(actor)

    # Factions (sama seperti analysis)
    faction_defs = {
        "Kejaksaan": ["Kejaksaan Agung", "ST Burhanuddin", "Febrie Ardiansyah"],
        "Polri": ["Polri", "Listyo Sigit Prabowo", "Densus 88", "Brimob", "Kortastipidkor", "Polda Metro Jaya"],
        "Istana": ["Prabowo Subianto", "Jokowi"],
        "Militer": ["TNI", "BAIS TNI"],
        "DPR": ["Komisi III DPR"],
    }

    # Map actor -> faction
    actor_faction = {}
    for f_name, members in faction_defs.items():
        for m in members:
            actor_faction[m] = f_name

    nodes = []
    for f_name in faction_defs:
        nodes.append({"id": f_name, "type": "faction", "size": 3000})
    for actor in sorted(all_actors):
        nodes.append({
            "id": actor,
            "type": "actor",
            "faction": actor_faction.get(actor, "unknown"),
            "size": 800,
        })

    # Co-occurrence edges
    co_occur = defaultdict(lambda: defaultdict(int))
    for art in articles:
        actors_in_art = art.get("actors", [])
        for i, a in enumerate(actors_in_art):
            for b in actors_in_art[i+1:]:
                if a != b:
                    co_occur[a][b] += 1
                    co_occur[b][a] += 1

    edges = []
    seen_edges = set()
    for a in co_occur:
        for b in co_occur[a]:
            edge_key = tuple(sorted([a, b]))
            if edge_key not in seen_edges:
                seen_edges.add(edge_key)
                w = co_occur[a][b]
                edges.append({"source": a, "target": b, "weight": w})

    # Juga edges faksi-aktor (skip self-loop jika nama faksi = nama aktor)
    for actor in all_actors:
        f = actor_faction.get(actor)
        if f and f != actor:
            count = 0
            for art in articles:
                if actor in art.get("actors", []):
                    count += 1
            edge_key = tuple(sorted([f, actor]))
            if edge_key not in seen_edges:
                seen_edges.add(edge_key)
                edges.append({"source": f, "target": actor, "weight": count})

    # Important edges (high weight) - ensure they are in the graph
    important_edges = [
        ("ST Burhanuddin", "Febrie Ardiansyah", 5),
        ("Febrie Ardiansyah", "Ferry Boboho", 4),
        ("Ferry Boboho", "Densus 88", 3),
        ("Listyo Sigit Prabowo", "Kortastipidkor", 4),
        ("Prabowo Subianto", "ST Burhanuddin", 6),
        ("Prabowo Subianto", "Listyo Sigit Prabowo", 6),
        ("TNI", "Febrie Ardiansyah", 4),
        ("TNI", "Kejaksaan Agung", 5),
        ("ST Burhanuddin", "Listyo Sigit Prabowo", 8),
        ("Brimob", "Kejaksaan Agung", 3),
    ]

    existing_src_target = {(e["source"], e["target"]) for e in edges}
    for src, tgt, w in important_edges:
        if src == tgt:
            continue
        pair = (src, tgt)
        rev_pair = (tgt, src)
        if pair not in existing_src_target and rev_pair not in existing_src_target:
            edges.append({"source": src, "target": tgt, "weight": w})
            existing_src_target.add(pair)
        else:
            for e in edges:
                if (e["source"] == src and e["target"] == tgt) or (e["source"] == tgt and e["target"] == src):
                    if e["weight"] < w:
                        e["weight"] = w

    graph = {"nodes": nodes, "edges": edges}

    with open(OUTPUT_DIR / "network_graph.json", "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
    print(f"[OK] network_graph.json: {len(nodes)} nodes, {len(edges)} edges")
    return graph


# ──────────────────────────────────────────────
# 4. RUN GENERATORS
# ──────────────────────────────────────────────

def run_scripts():
    """Jalankan generate_pdf.py, generate_map.py, regen_sumber.py (jika ada)."""
    scripts_dir = Path(__file__).parent
    scripts_to_run = ["generate_pdf.py", "generate_map.py", "regen_sumber.py"]

    for script_name in scripts_to_run:
        script_path = scripts_dir / script_name
        if not script_path.exists():
            print(f"[SKIP] {script_name} tidak ditemukan")
            continue
        print(f"\n{'='*50}")
        print(f"  Menjalankan {script_name}...")
        print(f"{'='*50}")
        import subprocess
        result = subprocess.run(
            ["python", str(script_path)],
            capture_output=True, text=True, cwd=scripts_dir
        )
        if result.stdout:
            for line in result.stdout.strip().split("\n"):
                print(f"  {line}")
        if result.stderr:
            for line in result.stderr.strip().split("\n"):
                print(f"  [ERR] {line}")
        if result.returncode != 0:
            print(f"  [WARN] {script_name} exit code {result.returncode}")


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    print("=" * 60)
    print("KASUS INVESTIGATOR - Rebuild All Data")
    print("=" * 60)

    raw = build_raw_data()
    analysis = build_analysis_results(raw)
    graph = build_network_graph(raw, analysis)

    print(f"\n{'='*50}")
    print("  RINGKASAN:")
    print(f"  - Total artikel  : {raw['metadata']['total_articles']}")
    print(f"  - Total aktor    : {len(raw['actor_mentions'])}")
    ss = analysis["sentiment"]["summary"]
    print(f"  - Sentimen       : Positif={ss['positif']}, Negatif={ss['negatif']}, Netral={ss['netral']}")
    print(f"  - Timeline bulan : {len(analysis['timeline']['dates'])} periode")
    print(f"  - Nodes SNA      : {graph['nodes']}")
    print(f"  - Edges SNA      : {graph['edges']}")

    # Jalankan script post-processing
    run_scripts()

    print(f"\n{'='*50}")
    print("  SELESAI! Semua data telah diperbarui.")
    print(f"{'='*50}")
