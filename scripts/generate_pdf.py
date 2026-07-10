"""
KASUS INVESTIGATOR - Generator Laporan PDF
Membuat laporan investigasi lengkap dalam format PDF
Output: output/laporan_investigasi.pdf
"""

import json
import os
from datetime import datetime
from pathlib import Path

from fpdf import FPDF

OUTPUT_DIR = Path(__file__).parent.parent / "output"


def sanitize(text):
    """Replace non-latin-1 characters for fpdf2."""
    replacements = {
        "\u2014": "-", "\u2013": "-", "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"', "\u2022": "-", "\u2026": "...",
        "\u00a0": " ", "\u200b": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode("latin-1", "replace").decode("latin-1")


class LaporanPDF(FPDF):
    """Custom PDF class untuk laporan investigasi."""

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 6, "KASUS INVESTIGATOR - LAPORAN INVESTIGASI", align="L")
        self.cell(0, 6, "CONFIDENTIAL", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Halaman {self.page_no()}/{{nb}}", align="C")

    def cover_page(self, title, subtitle, date):
        self.add_page()
        self.ln(50)

        # Judul besar
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(0, 51, 102)
        self.multi_cell(0, 15, title, align="C")

        self.ln(10)

        # Subtitle
        self.set_font("Helvetica", "", 14)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 8, subtitle, align="C")

        self.ln(15)

        # Garis pemisah
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.8)
        self.line(60, self.get_y(), 150, self.get_y())

        self.ln(15)

        # Info
        self.set_font("Helvetica", "", 11)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, f"Tanggal: {date}", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 8, "Klasifikasi: MIXED (OSINT + SNA + DATA)", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 8, "Confidence Level: MEDIUM", align="C", new_x="LMARGIN", new_y="NEXT")

        self.ln(30)

        # Disclaimer
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(150, 150, 150)
        self.multi_cell(0, 5,
            "LAPORAN INI DIHASILKAN SECARA OTOMATIS MENGGUNAKAN ANALISIS DATA PUBLIK.\n"
            "TIDAK MERUPAKAN BUKTI HUKUM ATAU OPINI RESMI MANA PUN.",
            align="C"
        )

    def section_title(self, title):
        self.ln(5)
        self.set_x(10)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, sanitize(title), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def sub_title(self, title):
        self.ln(3)
        self.set_x(10)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, sanitize(title), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.set_x(10)
        self.multi_cell(190, 6, sanitize(text))
        self.ln(2)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.set_x(10)
        self.multi_cell(190, 6, "  - " + sanitize(text))

    def stat_box(self, label, value):
        self.set_fill_color(240, 245, 255)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(0, 51, 102)
        x = self.get_x()
        y = self.get_y()
        self.rect(x, y, 55, 20, "F")
        self.set_xy(x + 3, y + 3)
        self.cell(50, 6, sanitize(str(label)))
        self.set_font("Helvetica", "B", 14)
        self.set_xy(x + 3, y + 10)
        self.cell(50, 8, sanitize(str(value)))
        self.set_xy(x + 60, y)


def load_analysis():
    """Load data analisis."""
    path = OUTPUT_DIR / "analysis_results.json"
    if not path.exists():
        print("[ERROR] analysis_results.json tidak ditemukan!")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_raw():
    """Load data mentah."""
    path = OUTPUT_DIR / "raw_data.json"
    if not path.exists():
        print("[ERROR] raw_data.json tidak ditemukan!")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_pdf():
    """Generate laporan PDF lengkap."""
    print("=" * 60)
    print("KASUS INVESTIGATOR - Generator Laporan PDF")
    print("=" * 60)

    analysis = load_analysis()
    raw = load_raw()
    if not analysis or not raw:
        return

    pdf = LaporanPDF()
    pdf.alias_nb_pages()

    # 1. COVER PAGE
    pdf.cover_page(
        "LAPORAN INVESTIGASI",
        "Konflik Kejaksaan Agung vs Polri\nMasa Transisi Kekuasaan 2023-2026",
        datetime.now().strftime("%d %B %Y")
    )

    # 2. RINGKASAN EKSEKUTIF
    pdf.add_page()
    pdf.section_title("1. RINGKASAN EKSEKUTIF")
    total = raw["metadata"]["total_articles"]
    sources = len(raw["metadata"]["sources"])
    actors = len(raw.get("actor_mentions", {}))
    sent = analysis["sentiment"]["summary"]

    pdf.body_text(
        f"Laporan ini merupakan hasil analisis investigasi terhadap konflik antara "
        f"Kejaksaan Agung dan Kepolisian Republik Indonesia dalam periode 2023-2026. "
        f"Analisis dilakukan berdasarkan {total} artikel berita dari {sources} sumber "
        f"media daring yang dikumpulkan menggunakan {len(raw['metadata']['keywords_used'])} "
        f"keyword pencarian."
    )
    pdf.body_text(
        f"Temuan utama menunjukkan bahwa konflik ini melibatkan {actors} aktor/entitas "
        f"yang signifikan, dengan sentimen negatif mendominasi ({sent['negatif']} artikel) "
        f"dibandingkan positif ({sent['positif']}) dan netral ({sent['netral']})."
    )
    pdf.body_text(
        f"Analisis jaringan sosial (SNA) mengidentifikasi beberapa node sentral yang "
        f"menghubungkan kedua kubu, menunjukkan adanya pola interaksi lintas institusi "
        f"yang kompleks."
    )

    # 3. STATISTIK UMUM
    pdf.add_page()
    pdf.section_title("2. STATISTIK UMUM")

    pdf.sub_title("Distribusi Data")
    y_start = pdf.get_y()
    pdf.stat_box("Total Artikel", total)
    pdf.stat_box("Sumber Media", sources)
    pdf.stat_box("Aktors", actors)
    pdf.ln(25)

    # Sentimen
    pdf.sub_title("Distribusi Sentimen")
    y_start = pdf.get_y()
    pdf.stat_box("Negatif", sent["negatif"])
    pdf.stat_box("Netral", sent["netral"])
    pdf.stat_box("Positif", sent["positif"])
    pdf.ln(25)

    # Per sumber
    pdf.sub_title("Artikel per Sumber")
    for src, count in sorted(analysis["source_distribution"]["labels"] and
                             zip(analysis["source_distribution"]["labels"],
                                 analysis["source_distribution"]["values"]),
                             key=lambda x: -x[1]):
        pdf.bullet(f"{src}: {count} artikel")

    # 4. ANALISIS AKTOR
    pdf.add_page()
    pdf.section_title("3. ANALISIS AKTOR & JARINGAN")

    actor_mentions = raw.get("actor_mentions", {})
    if actor_mentions:
        pdf.body_text(
            "Berikut adalah aktor-aktor yang paling banyak disebut dalam liputan media "
            "terkait konflik Kejaksaan Agung vs Polri:"
        )
        for actor, info in sorted(actor_mentions.items(), key=lambda x: -x[1]["count"]):
            pdf.sub_title(f"{actor} ({info['role']})")
            pdf.body_text(f"Disebut {info['count']} kali dalam {len(info['articles'])} artikel.")
            for art in info["articles"][:3]:
                pdf.bullet(art[:100])
    else:
        pdf.body_text("Tidak ada data aktor yang signifikan ditemukan.")

    # 5. CENTRALITY (SNA)
    centrality = analysis.get("sna", {}).get("centrality", {})
    if centrality:
        pdf.add_page()
        pdf.section_title("4. SOCIAL NETWORK ANALYSIS (SNA)")
        pdf.body_text(
            f"Jaringan terdiri dari {analysis['sna']['nodes']} nodes dan "
            f"{analysis['sna']['edges']} edges. Berikut adalah centrality metrics:"
        )

        # Top betweenness
        top_bn = sorted(centrality.items(), key=lambda x: -x[1]["betweenness"])[:10]
        pdf.sub_title("Betweenness Centrality (Top 10)")
        pdf.body_text(
            "Betweenness centrality mengukur seberapa sering suatu node berada "
            "di jalur terpendek antara node lain. Node dengan betweenness tinggi "
            "adalah 'jembatan' atau penghubung antar kelompok."
        )
        for actor, metrics in top_bn:
            pdf.bullet(f"{actor}: {metrics['betweenness']} (degree: {metrics['degree']})")

    # 6. TIMELINE
    pdf.add_page()
    pdf.section_title("5. TIMELINE KEJADIAN")
    timeline = analysis.get("timeline", {})
    if timeline.get("dates"):
        pdf.body_text(
            f"Total artikel bertanggal yang dianalisis: {timeline.get('total_dated', 'N/A')}"
        )
        pdf.sub_title("Distribusi Bulanan")
        dates = timeline["dates"]
        counts = timeline["counts"]
        # Tampilkan 10 terakhir
        for d, c in zip(dates[-15:], counts[-15:]):
            bar = "#" * min(c, 50)
            pdf.set_font("Courier", "", 9)
            pdf.set_text_color(40, 40, 40)
            pdf.cell(30, 5, d)
            pdf.cell(0, 5, f" {c:3d} | {bar}", new_x="LMARGIN", new_y="NEXT")
    else:
        pdf.body_text("Data tanggal tidak cukup untuk membuat timeline.")

    # 7. KESIMPULAN
    pdf.add_page()
    pdf.section_title("6. KESIMPULAN")
    pdf.body_text(
        f"Berdasarkan analisis {total} artikel dari {sources} sumber media, "
        f"berikut adalah kesimpulan investigasi:"
    )
    pdf.ln(2)

    pdf.bullet(
        f"Konflik antara Kejaksaan Agung dan Polri teridentifikasi dalam {total} "
        f"liputan media selama periode 2023-2026."
    )
    pdf.bullet(
        f"Sentimen negatif mendominasi ({sent['negatif']} dari {total} artikel), "
        f"menunjukkan framing media yang cenderung negatif terhadap konflik ini."
    )
    if actor_mentions:
        top_actor = max(actor_mentions.items(), key=lambda x: x[1]["count"])
        pdf.bullet(
            f"Aktor paling dominan adalah {top_actor[0]} ({top_actor[1]['role']}) "
            f"dengan {top_actor[1]['count']} penyebutan."
        )
    pdf.bullet(
        f"Jaringan analisis menunjukkan {analysis['sna']['nodes']} nodes dan "
        f"{analysis['sna']['edges']} edges, mengindikasikan kompleksitas "
        f"relasi antar aktor."
    )
    pdf.bullet(
        "Confidence level: MEDIUM — dikarenakan analisis berbasis data publik, "
        "belum termasuk sumber classified atau dokumen hukum resmi."
    )

    # 8. REKOMENDASI
    pdf.section_title("7. REKOMENDASI TINDAK LANJUT")
    pdf.bullet("Lakukan analisis lebih dalam pada aspek keuangan (anggaran institusi).")
    pdf.bullet("Perluas sumber data ke dokumen resmi (JDIH, putusan pengadilan).")
    pdf.bullet("Lakukan wawancara dengan pengamat hukum untuk validasi.")
    pdf.bullet("Update monitoring secara berkala untuk deteksi eskalasi.")
    pdf.bullet("Bandingkan dengan data historis konflik serupa sebelumnya.")

    # 9. LAMPIRAN
    pdf.add_page()
    pdf.section_title("8. LAMPIRAN")

    pdf.sub_title("A. Daftar Keyword Pencarian")
    for kw in raw["metadata"]["keywords_used"]:
        pdf.bullet(kw)

    pdf.sub_title("B. Daftar Sumber")
    for src in raw["metadata"]["sources"]:
        pdf.bullet(src)

    pdf.sub_title("C. Metodologi")
    pdf.body_text(
        "1. Pengumpulan data menggunakan web scraping dari 6 portal berita Indonesia\n"
        "2. Pencarian dilakukan dengan 14 keyword berbeda\n"
        "3. Deduplikasi berdasarkan hash judul artikel\n"
        "4. Analisis sentimen menggunakan lexicon-based approach\n"
        "5. SNA menggunakan NetworkX dengan centrality metrics\n"
        "6. Semua data adalah publik dan tidak termasuk sumber classified"
    )

    # Simpan
    pdf_path = OUTPUT_DIR / "laporan_investigasi.pdf"
    pdf.output(str(pdf_path))
    print(f"\n[SAVE] {pdf_path}")
    print(f"[DONE] PDF laporan selesai! {pdf.page_no()} halaman")
    return pdf_path


if __name__ == "__main__":
    generate_pdf()
