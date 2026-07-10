"""
KASUS INVESTIGATOR - Generator Laporan PDF (Versi Orang Awam)
Membuat laporan investigasi yang mudah dipahami siapa saja
Output: output/laporan_investigasi.pdf
"""

import json
from datetime import datetime
from pathlib import Path

from fpdf import FPDF
from PIL import Image

OUTPUT_DIR = Path(__file__).parent.parent / "output"
PHOTOS_DIR = Path(__file__).parent.parent / "photos"


def s(text):
    """Sanitize text untuk fpdf2 latin-1."""
    reps = {
        "\u2014": "-", "\u2013": "-", "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"', "\u2022": "-", "\u2026": "...",
        "\u00a0": " ", "\u200b": "",
    }
    for old, new in reps.items():
        text = text.replace(old, new)
    return text.encode("latin-1", "replace").decode("latin-1")


class LaporanPDF(FPDF):
    """PDF Laporan untuk orang awam."""

    WARNA = {
        "judul": (26, 54, 93),
        "accent": (229, 62, 62),
        "hijau": (56, 161, 105),
        "abu": (113, 128, 150),
        "gelap": (26, 32, 44),
        "terang": (247, 250, 252),
        "putih": (255, 255, 255),
    }

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*self.WARNA["abu"])
        self.cell(0, 5, "KASUS INVESTIGATOR", align="L")
        self.cell(0, 5, "Konflik Kejaksaan vs Polri", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.WARNA["abu"])
        self.cell(0, 10, "Halaman " + str(self.page_no()) + "/{nb}", align="C")

    def cover_page(self):
        """Halaman sampul."""
        self.add_page()
        self.ln(40)

        self.set_fill_color(*self.WARNA["judul"])
        self.rect(0, 0, 210, 8, "F")

        self.set_font("Helvetica", "B", 30)
        self.set_text_color(*self.WARNA["judul"])
        self.multi_cell(0, 14, s("Konflik Kejaksaan\nvs Polri"), align="C")

        self.ln(5)

        self.set_font("Helvetica", "", 16)
        self.set_text_color(*self.WARNA["abu"])
        self.multi_cell(0, 9, s("Apa yang Sebenarnya Terjadi?"), align="C")

        self.ln(10)

        self.set_draw_color(*self.WARNA["accent"])
        self.set_line_width(1.2)
        self.line(70, self.get_y(), 140, self.get_y())

        self.ln(10)

        self.set_font("Helvetica", "", 11)
        self.set_text_color(*self.WARNA["abu"])
        lines = [
            "Laporan Investigasi Berbasis Data Publik",
            "Periode: 2023 - 2026",
            "Tanggal: " + datetime.now().strftime("%d %B %Y"),
            "",
            "62 Artikel Berita  |  10 Sumber Media  |  12 Aktor Teridentifikasi",
        ]
        for line in lines:
            self.cell(0, 7, s(line), align="C", new_x="LMARGIN", new_y="NEXT")

        self.ln(20)

        self.set_fill_color(*self.WARNA["terang"])
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*self.WARNA["abu"])
        y = self.get_y()
        self.rect(20, y, 170, 25, "F")
        self.set_xy(25, y + 3)
        self.multi_cell(160, 5, s(
            "PERINGATAN: Laporan ini dihasilkan dari analisis data berita publik.\n"
            "Bukan merupakan bukti hukum, dakwaan, atau opini resmi.\n"
            "Untuk edukasi dan pemahaman publik saja."
        ), align="C")

    def judul_bagian(self, nomor, judul):
        """Section header yang menarik."""
        self.ln(4)
        self.set_x(10)

        self.set_fill_color(*self.WARNA["judul"])
        self.set_text_color(*self.WARNA["putih"])
        self.set_font("Helvetica", "B", 12)
        self.cell(8, 8, str(nomor), fill=True, align="C")
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*self.WARNA["judul"])
        self.cell(0, 8, "  " + s(judul), new_x="LMARGIN", new_y="NEXT")

        self.set_draw_color(*self.WARNA["accent"])
        self.set_line_width(0.6)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def cerita(self, teks):
        """Teks naratif bahasa manusia."""
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.WARNA["gelap"])
        self.set_x(10)
        self.multi_cell(190, 6, s(teks))
        self.ln(2)

    def highlight_box(self, judul_isi, isi):
        """Kotak highlight yang menarik perhatian."""
        self.ln(2)
        y = self.get_y()
        self.set_fill_color(*self.WARNA["terang"])
        self.rect(10, y, 190, 22, "F")
        self.set_draw_color(*self.WARNA["accent"])
        self.set_line_width(0.8)
        self.line(10, y, 10, y + 22)

        self.set_xy(15, y + 3)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*self.WARNA["accent"])
        self.cell(0, 6, s(judul_isi))
        self.set_xy(15, y + 10)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.WARNA["gelap"])
        self.multi_cell(175, 5, s(isi))
        self.set_y(y + 25)

    def poin(self, teks):
        """Bullet point sederhana."""
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.WARNA["gelap"])
        self.set_x(10)
        self.multi_cell(190, 6, s("  > " + teks))

    def tabel_baris(self, kolom, warna_baris=False):
        """Baris tabel rapi."""
        self.set_font("Helvetica", "", 9)
        if warna_baris:
            self.set_fill_color(240, 244, 248)
        self.set_text_color(*self.WARNA["gelap"])
        x = self.get_x()
        widths = [55, 45, 90]
        for i, (col, w) in enumerate(zip(kolom, widths)):
            self.cell(w, 6, s(str(col)[:40]), fill=warna_baris)
        self.ln()


def load_analysis():
    path = OUTPUT_DIR / "analysis_results.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_raw():
    path = OUTPUT_DIR / "raw_data.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_pdf():
    print("=" * 60)
    print("KASUS INVESTIGATOR - PDF Laporan (Versi Orang Awam)")
    print("=" * 60)

    analysis = load_analysis()
    raw = load_raw()
    if not analysis or not raw:
        return

    pdf = LaporanPDF()
    pdf.alias_nb_pages()
    W = pdf.WARNA

    total = raw["metadata"]["total_articles"]
    sent = analysis["sentiment"]["summary"]
    actors = raw.get("actor_mentions", {})
    centrality = analysis.get("sna", {}).get("centrality", {})
    sn = analysis.get("sna", {})

    # =============================================
    # HALAMAN 1: COVER
    # =============================================
    pdf.cover_page()

    # =============================================
    # HALAMAN 2: JADI GIMANA SIH?
    # =============================================
    pdf.add_page()
    pdf.judul_bagian(1, "Jadi Gimana Sih?")

    pdf.cerita(
        "Dua lembaga penegak hukum terbesar di Indonesia -- Kejaksaan Agung dan "
        "Kepolisian (Polri) -- sedang berkonflik. Bukan soal pertengkaran mulut, "
        "tapi soal siapa yang berhak menangani kasus-kasus korupsi besar."
    )
    pdf.cerita(
        "Konflik ini melibatkan pengusaha bernama Ferry Hongkiriwang yang diduga "
        "menjadi penghubung antara pihak Kejaksaan dan kasus korupsi. Polri "
        "menggeledah kafe miliknya, sementara pihak Kejaksaan merasa urusannya "
        "dicampuri."
    )
    pdf.cerita(
        "Yang bikin makin rumit, TNI (tentara) juga masuk ke tengah konflik ini "
        "dengan mengerahkan pasukan untuk melindungi salah satu pejabat Kejaksaan. "
        "Presiden Prabowo Subianto pun harus turun tangan memanggil semua pihak "
        "ke Istana."
    )

    pdf.highlight_box(
        "KESIMPULAN SINGKAT:",
        "Ini bukan sekadar konflik birokrasi. Ini soal perebutan kuasa antara "
        "lembaga penegak hukum di masa transisi kekuasaan, yang melibatkan "
        "kepentingan politik, korupsi besar, dan intervensi militer."
    )

    pdf.cerita(
        "Laporan ini menyajikan fakta-fakta dari 62 artikel berita publik. "
        "Semua data tercantum di bagian lampiran. Anda bisa langsung cek "
        "sumbernya sendiri."
    )

    # =============================================
    # HALAMAN 3: SIAPA SIH MEREKA?
    # =============================================
    pdf.add_page()
    pdf.judul_bagian(2, "Siapa Sih Mereka?")

    pdf.cerita(
        "Berikut adalah tokoh-tokoh utama yang terlibat dalam konflik ini. "
        "Anda tidak perlu hafal semua -- yang penting tahu peran masing-masing."
    )

    # Profil dengan foto untuk aktor utama
    profil_foto = [
        ("Prabowo Subianto", "Presiden RI", "Panggil semua pihak ke Istana untuk redakan konflik", "prabowo.jpg"),
        ("ST Burhanuddin", "Jaksa Agung", "Pimpinan Kejaksaan -- posisinya di tengah pusaran konflik", "burhanuddin.jpg"),
        ("Listyo Sigit Prabowo", "Kapolri", "Pimpinan Polri -- aktif geledah kafe linked ke Kejaksaan", "listyo_sigit.jpg"),
    ]

    for nama, jabatan, peran, foto in profil_foto:
        y_start = pdf.get_y()
        if y_start > 240:
            pdf.add_page()
            y_start = pdf.get_y()

        # Foto (40x40)
        foto_path = PHOTOS_DIR / foto
        if foto_path.exists():
            try:
                pdf.image(str(foto_path), x=12, y=y_start, w=20, h=25)
            except Exception:
                pass

        # Teks di sebelah foto
        x_text = 35
        pdf.set_xy(x_text, y_start)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*W["gelap"])
        pdf.cell(0, 6, s(nama))

        pdf.set_xy(x_text, y_start + 7)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(*W["abu"])
        pdf.cell(0, 5, s(jabatan))

        pdf.set_xy(x_text, y_start + 14)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*W["gelap"])
        pdf.multi_cell(155, 5, s(peran))

        pdf.set_y(y_start + 28)

    pdf.ln(3)

    # Tabel untuk aktor pendukung
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*W["judul"])
    pdf.set_x(10)
    pdf.cell(0, 7, s("Aktor Pendukung:"), new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(*W["judul"])
    pdf.set_text_color(*W["putih"])
    pdf.cell(55, 7, "  NAMA", fill=True)
    pdf.cell(45, 7, "  JABATAN", fill=True)
    pdf.cell(90, 7, "  PERAN DALAM KONFLIK", fill=True)
    pdf.ln()

    profil = [
        ("Febrie Adriansyah", "Jampidsus Kejagung", "Jaksa yang rumahnya dijaga TNI saat konflik"),
        ("Ferry Hongkiriwang", "Pengusaha", "Operator kafe -- diduga jadi penghubung korupsi"),
        ("TNI / Militer", "Tentara", "Mengerahkan pasukan ke rumah pejabat Kejaksaan"),
        ("Densus 88", "Antiteror Polri", "Personelnya menguntit orang Kejaksaan"),
        ("Komisi III DPR", "DPR", "Minta TNI-Polri solid dan saling bantu"),
    ]

    for i, (nama, jabatan, peran) in enumerate(profil):
        pdf.tabel_baris([nama, jabatan, peran], warna_baris=(i % 2 == 0))

    pdf.ln(5)
    pdf.highlight_box(
        "YANG PERLU ANDA INGAT:",
        "Presiden Prabowo = Pemain kunci yang bisa hentikan konflik. "
        "Burhanuddin vs Listyo Sigit = Dua pimpinan yang berseteru. "
        "Ferry Hongkiriwang = Benang merah yang menghubungkan semuanya."
    )

    # =============================================
    # HALAMAN 4-5: KRONOLOGI KONFLIK
    # =============================================
    pdf.add_page()
    pdf.judul_bagian(3, "Bagaimana Konfliknya Berkembang?")

    pdf.cerita(
        "Konflik ini bukan terjadi tiba-tiba. Berikut adalah rangkaian peristiwa "
        "penting yang membentuk konflik dari awal sampai sekarang:"
    )

    kronologi = [
        ("MEI 2024", "Densus 88 menguntit",
         "Anggota Densus 88 tertangkap kamera Polisi Militer sedang menguntit "
         "Febrie Adriansyah (Jampidsus) di sebuah kafe VIP. Ini pertanda sudah ada "
         "ketidakpercayaan antar lembaga."),
        ("OKT 2024", "Prabowo lantik Jaksa Agung",
         "Presiden Prabowo resmi melantik ST Burhanuddin sebagai Jaksa Agung "
         "periode 2024-2029. Posisi ini krusial karena terkait penanganan "
         "kasus korupsi besar."),
        ("JUN 2025", "Perpres Perlindungan Jaksa",
         "Terbit Perpres 66/2025 tentang perlindungan jaksa. Komjak membantah "
         "ada konflik, tapi timing-nya memicu spekulasi publik."),
        ("JUL 2025", "Polri geledah kafe Ferry",
         "Polri menggeledah kafe milik Ferry Hongkiriwang di Cilandak. Ditemukan "
         "mobil dinas Kejaksaan di lokasi. Kortastipidkor Polri menemukan indikasi "
         "Ferry sebagai operator pemerasan korupsi."),
        ("JUL 2025", "TNI lindungi pejabat Kejaksaan",
         "TNI mengerahkan puluhan prajurit ke rumah Febrie Adriansyah. Bais TNI "
         "menangkap Briptu Faisal (Densus 88) yang membuntuti Ferry. Polri terbitkan "
         "SP2HP untuk kasus penculikan."),
        ("JUL 2025", "Prabowo panggil ke Istana",
         "Presiden Prabowo memanggil Panglima TNI, Kapolri, dan Jaksa Agung ke "
         "Istana. Memerintahkan menjaga situasi kondusif. Ini sinyal bahwa "
         "konflik sudah di level presiden."),
        ("AGU 2025", "Kejagung: Hubungan baik saja",
         "Kejaksaan Agung mengklaim hubungan dengan Polri baik-baik saja. Tapi "
         "di saat yang sama, Tempo melaporkan politisasi perkara korupsi "
         "antara Kejaksaan dan Polri."),
        ("OKT 2025", "Prabowo tak ganti pejabat",
         "Prabowo belum mengganti Kapolri dan Jaksa Agung karena dianggap "
         "\"berjasa\". Keduanya direncanakan diganti Januari 2026."),
        ("DES 2025", "Jaksa Agung & Kapolri sepakat",
         "Pertemuan sinergitas di Mabes Polri untuk hadapi KUHP baru. "
         "Ketua Komisi III DPR hadir. Sinyal upaya normalisasi."),
        ("JUL 2026", "Kejaksaan terbit surat rahasia",
         "Kejaksaan Agung keluarkan surat rahasia R-696 memerintahkan "
         "seluruh jajaran waspada terhadap \"Ancaman, Gangguan, Hambatan, "
         "dan Tantangan\". Konflik belum selesai."),
    ]

    for i, (waktu, judul_peristiwa, deskripsi) in enumerate(kronologi):
        y = pdf.get_y()
        if y > 250:
            pdf.add_page()
            y = pdf.get_y()

        # Timeline marker
        pdf.set_fill_color(*W["accent"])
        pdf.rect(12, y + 2, 3, 3, "F")

        # Waktu
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*W["accent"])
        pdf.set_xy(18, y)
        pdf.cell(30, 5, s(waktu))

        # Judul
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*W["gelap"])
        pdf.set_xy(50, y)
        pdf.cell(0, 5, s(judul_peristiwa), new_x="LMARGIN", new_y="NEXT")

        # Deskripsi
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*W["abu"])
        pdf.set_x(50)
        pdf.multi_cell(145, 5, s(deskripsi))
        pdf.ln(3)

    # =============================================
    # HALAMAN 6: APA KATA MEDIA?
    # =============================================
    pdf.add_page()
    pdf.judul_bagian(4, "Apa Kata Media?")

    pdf.cerita(
        "Kami menganalisis 62 artikel berita dari 10 sumber media. Berikut "
        "bagaimana media meliput konflik ini:"
    )

    # Sentimen visual
    y = pdf.get_y()
    pdf.set_xy(10, y)

    # Negatif
    pdf.set_fill_color(229, 62, 62)
    pdf.rect(10, y, 60, 25, "F")
    pdf.set_xy(10, y + 5)
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*W["putih"])
    pdf.cell(60, 10, str(sent["negatif"]), align="C")
    pdf.set_xy(10, y + 15)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(60, 6, "BERITA NEGATIF", align="C")

    # Netral
    pdf.set_fill_color(237, 183, 60)
    pdf.rect(75, y, 60, 25, "F")
    pdf.set_xy(75, y + 5)
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*W["gelap"])
    pdf.cell(60, 10, str(sent["netral"]), align="C")
    pdf.set_xy(75, y + 15)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(60, 6, "BERITA NETRAL", align="C")

    # Positif
    pdf.set_fill_color(56, 161, 105)
    pdf.rect(140, y, 60, 25, "F")
    pdf.set_xy(140, y + 5)
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*W["putih"])
    pdf.cell(60, 10, str(sent["positif"]), align="C")
    pdf.set_xy(140, y + 15)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(60, 6, "BERITA POSITIF", align="C")

    pdf.set_y(y + 32)

    pdf.highlight_box(
        "APA ARTINYA?",
        "Sebagian besar berita (50 dari 62) bersifat netral -- artinya media "
        "lebih banyak melaporkan fakta daripada berpihak. Tapi 9 berita "
        "negatif menunjukkan ada framing konflik yang cukup kuat di media."
    )

    # Sumber media
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*W["judul"])
    pdf.set_x(10)
    pdf.cell(0, 8, s("Dari Mana Berita Datang?"), new_x="LMARGIN", new_y="NEXT")

    source_dist = analysis.get("source_distribution", {})
    if source_dist.get("labels"):
        sorted_src = sorted(zip(source_dist["values"], source_dist["labels"]), reverse=True)
        max_val = sorted_src[0][0] if sorted_src else 1
        for i, (val, label) in enumerate(sorted_src[:8]):
            y_bar = pdf.get_y()
            bar_width = (val / max_val) * 100
            pdf.set_fill_color(*W["judul"])
            pdf.rect(60, y_bar + 1, bar_width, 6, "F")
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(*W["gelap"])
            pdf.set_x(10)
            pdf.cell(48, 8, s(label), align="R")
            pdf.set_xy(62, y_bar)
            pdf.set_text_color(*W["putih"])
            pdf.set_font("Helvetica", "B", 7)
            pdf.cell(bar_width, 8, str(val))
            pdf.ln()

    # =============================================
    # HALAMAN 7: SIAPA PALING BERPENGARUH?
    # =============================================
    pdf.add_page()
    pdf.judul_bagian(5, "Siapa yang Paling Berpengaruh?")

    pdf.cerita(
        "Dalam setiap konflik, selalu ada orang-orang kunci yang posisinya "
        "paling sentral. Berikut siapa yang paling berpengaruh berdasarkan "
        "analisis jaringan dari 62 berita:"
    )

    if centrality:
        top_bn = sorted(centrality.items(), key=lambda x: -x[1]["betweenness"])[:7]
        for i, (actor, m) in enumerate(top_bn):
            bar_w = int(m["betweenness"] * 500)
            y_bar = pdf.get_y()

            # Rank
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(*W["accent"])
            pdf.set_xy(10, y_bar)
            pdf.cell(8, 8, str(i + 1) + ".")

            # Nama
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(*W["gelap"])
            pdf.set_xy(20, y_bar)
            pdf.cell(55, 8, s(actor))

            # Bar
            pdf.set_fill_color(*W["judul"])
            pdf.rect(78, y_bar + 2, max(bar_w, 5), 5, "F")

            # Angka
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(*W["abu"])
            pdf.set_xy(78 + max(bar_w, 5) + 3, y_bar)
            pdf.cell(30, 8, str(m["betweenness"]))

            pdf.ln()

    pdf.ln(5)
    pdf.highlight_box(
        "CARA BACA:",
        "Angka betweenness semakin tinggi = semakin sering orang itu muncul "
        "sebagai penghubung dalam konflik. Prabowo paling tinggi karena dia "
        "presiden yang memanggil semua pihak. Burhanuddin dan Listyo Sigit "
        "tinggi karena mereka dua pimpinan yang berseteru."
    )

    # Kutipan penting
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*W["judul"])
    pdf.set_x(10)
    pdf.cell(0, 8, s("Kutipan Penting dari Berita:"), new_x="LMARGIN", new_y="NEXT")

    kutipan = [
        '"Hubungan Kejaksaan dengan Polri baik-baik saja." - Kejagung (Agustus 2025)',
        '"Prabowo panggil semua ke Istana, perintahkan jaga kondusifitas." - CNN (Agustus 2025)',
        '"Ini pergeseran tektonik relasi kuasa antar-lembaga penegak hukum." - Sindikatpost (Juli 2026)',
        '"Kami tak mencampuri penangkapan Ferry Hongkiriwang." - Kejagung (Agustus 2025)',
    ]

    for k in kutipan:
        pdf.poin(k)

    # =============================================
    # HALAMAN 8: KESIMPULAN
    # =============================================
    pdf.add_page()
    pdf.judul_bagian(6, "Kesimpulan")

    pdf.cerita(
        "Setelah menganalisis 62 artikel berita dari 10 sumber media, "
        "berikut adalah yang bisa kami simpulkan:"
    )

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*W["judul"])
    pdf.set_x(10)
    pdf.cell(0, 8, s("Yang Sudah Jelas:"), new_x="LMARGIN", new_y="NEXT")

    poin_jelas = [
        "Konflik antara Kejaksaan dan Polri itu NYATA, bukan sekadar rumor.",
        "Ferry Hongkiriwang adalah benang merah -- pengusaha yang diduga "
        "menjadi operator pemerasan kasus korupsi.",
        "TNI turut campur dengan mengerahkan pasukan untuk melindungi "
        "pejabat Kejaksaan -- ini anomali serius.",
        "Presiden Prabowo sudah turun tangan memanggil semua pihak ke Istana.",
        "Konflik ini sudah berlangsung sejak Mei 2024 dan masih berlanjut "
        "sampai Juli 2026.",
    ]
    for p in poin_jelas:
        pdf.poin(p)

    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*W["accent"])
    pdf.set_x(10)
    pdf.cell(0, 8, s("Yang Perlu Diperhatikan:"), new_x="LMARGIN", new_y="NEXT")

    poin_catatan = [
        "Analisis ini hanya berdasarkan berita PUBLIK. Sumber classified "
        "atau dokumen hukum resmi tidak termasuk.",
        "Sebagian besar berita bersifat netral (50 dari 62), artinya "
        "framing media relatif seimbang.",
        "Confidence level: MEDIUM -- cukup untuk gambaran umum, tapi "
        "belum cukup untuk kesimpulan hukum.",
    ]
    for p in poin_catatan:
        pdf.poin(p)

    # =============================================
    # HALAMAN 9: MAU TAHU LEBIH?
    # =============================================
    pdf.add_page()
    pdf.judul_bagian(7, "Mau Tahu Lebih?")

    pdf.cerita(
        "Jika Anda ingin menelusuri lebih dalam, berikut sumber-sumber "
        "yang bisa diakses:"
    )

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*W["judul"])
    pdf.set_x(10)
    pdf.cell(0, 8, s("Berita Utama:"), new_x="LMARGIN", new_y="NEXT")

    sumber_utama = [
        'Tempo: "Konflik Polisi-Jaksa Berebut Perkara" (23 Agustus 2025)',
        'Infonews: "Konflik Polri vs Kejaksaan dan Intervensi Militer" (9 Juli 2026)',
        'Tempo: "Mengapa Prabowo Tak Ganti Kapolri dan Jaksa Agung" (30 Oktober 2025)',
        'Kompas: "Komjak Bantah Ada Konflik Kejaksaan dengan Polri" (6 Juni 2025)',
        'CNN: "Prabowo Panggil Panglima, Kapolri, Jaksa Agung ke Istana" (27 Agustus 2025)',
    ]
    for su in sumber_utama:
        pdf.poin(su)

    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*W["judul"])
    pdf.set_x(10)
    pdf.cell(0, 8, s("Saran Pelacakan Lanjutan:"), new_x="LMARGIN", new_y="NEXT")

    saran = [
        "Pantau perkembangan penggantian Kapolri dan Jaksa Agung.",
        "Cek dokumen resmi di JDIH Kejaksaan (jdih.kejaksaan.go.id).",
        "Ikuti putusan pengadilan terkait kasus Ferry Hongkiriwang.",
        "Perhatikan sikap DPR (Komisi III) terhadap konflik ini.",
        "Bandungkan dengan konflik serupa pada era sebelumnya.",
    ]
    for sa in saran:
        pdf.poin(sa)

    # =============================================
    # HALAMAN 10: LAMPIRAN
    # =============================================
    pdf.add_page()
    pdf.judul_bagian(8, "Lampiran: Data & Metodologi")

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*W["judul"])
    pdf.set_x(10)
    pdf.cell(0, 8, s("Sumber Data:"), new_x="LMARGIN", new_y="NEXT")

    sumber_list = [
        "Detik (50 artikel), Tempo (2), Infonews (2), Badiklat Kejaksaan (2),",
        "Sindikatpost (1), Kompas (1), CNN Indonesia (1), Sindonews (1),",
        "MetroTV (1), iNews (1)",
        "Total: 62 artikel unik",
    ]
    for sl in sumber_list:
        pdf.poin(sl)

    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*W["judul"])
    pdf.set_x(10)
    pdf.cell(0, 8, s("Metodologi:"), new_x="LMARGIN", new_y="NEXT")

    metode = [
        "1. Web scraping dari 6 portal berita + 1 websearch manual",
        "2. 14 keyword pencarian terkait konflik Kejaksaan vs Polri",
        "3. Deduplikasi berdasarkan judul artikel",
        "4. Analisis sentimen: lexicon-based (kata positif/negatif)",
        "5. SNA: NetworkX centrality metrics (betweenness, degree)",
        "6. Semua data dari sumber publik, tidak termasuk classified",
    ]
    for m in metode:
        pdf.poin(m)

    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*W["judul"])
    pdf.set_x(10)
    pdf.cell(0, 8, s("Keyword Pencarian:"), new_x="LMARGIN", new_y="NEXT")

    for kw in raw["metadata"]["keywords_used"][:7]:
        pdf.poin(kw)

    pdf.ln(8)
    pdf.set_fill_color(*W["terang"])
    y = pdf.get_y()
    pdf.rect(10, y, 190, 20, "F")
    pdf.set_xy(15, y + 3)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*W["abu"])
    pdf.multi_cell(180, 5, s(
        "Laporan ini dihasilkan oleh Kasus Investigator -- skill AI untuk "
        "analisis kasus berbasis data publik. Seluruh data dan kode tersedia "
        "di: github.com/InitialJawa/kasus-investigator"
    ), align="C")

    # Simpan
    pdf_path = OUTPUT_DIR / "laporan_investigasi.pdf"
    pdf.output(str(pdf_path))
    print(f"\n[SAVE] {pdf_path}")
    print(f"[DONE] PDF laporan selesai! {pdf.page_no()} halaman")
    return pdf_path


if __name__ == "__main__":
    generate_pdf()
