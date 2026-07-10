"""
KASUS INVESTIGATOR - Visual Mapping Generator (Clean White Style)
Membuat visualisasi profesional: Network Graph, Timeline, Sentiment, Sumber
Output: output/mapping_kasus.png (multi-panel)
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np

OUTPUT_DIR = Path(__file__).parent.parent / "output"

# Warna bersih profesional
COLORS = {
    "Kejaksaan": "#c0392b",
    "Polri": "#2980b9",
    "Istana": "#f39c12",
    "DPR": "#27ae60",
    "Yudikatif": "#8e44ad",
    "Antikorupsi": "#16a085",
    "unknown": "#95a5a6",
    "bg": "#ffffff",
    "text": "#2c3e50",
    "accent": "#2c3e50",
    "grid": "#ecf0f1",
    "bar": "#34495e",
}


def load_analysis():
    path = OUTPUT_DIR / "analysis_results.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_graph():
    path = OUTPUT_DIR / "network_graph.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_networkx_graph(graph_data):
    G = nx.Graph()
    for node in graph_data["nodes"]:
        G.add_node(node["id"], **{k: v for k, v in node.items() if k != "id"})
    for edge in graph_data["edges"]:
        G.add_edge(edge["source"], edge["target"], weight=edge.get("weight", 1))
    return G


def plot_network_panel(ax, G, centrality):
    ax.set_facecolor(COLORS["bg"])
    ax.set_title("Social Network Analysis\nSiapa Terhubung dengan Siapa?",
                 color=COLORS["text"], fontsize=11, fontweight="bold", pad=12, loc="left")

    if G.number_of_nodes() == 0:
        ax.text(0.5, 0.5, "Tidak ada data", ha="center", va="center",
                color=COLORS["text"], fontsize=10, transform=ax.transAxes)
        return

    try:
        pos = nx.spring_layout(G, k=2.8, iterations=50, seed=42)
    except Exception:
        pos = nx.random_layout(G, seed=42)

    node_colors = []
    node_sizes = []
    for node in G.nodes():
        faction = G.nodes[node].get("faction", "unknown")
        node_colors.append(COLORS.get(faction, COLORS["unknown"]))
        if G.nodes[node].get("type") == "faction":
            node_sizes.append(2500)
        else:
            node_sizes.append(1000)

    edge_weights = [G[u][v].get("weight", 1) for u, v in G.edges()]
    max_w = max(edge_weights) if edge_weights else 1
    edge_widths = [0.5 + (w / max_w) * 3 for w in edge_weights]

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#bdc3c7",
                           width=edge_widths, alpha=0.5)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                           node_size=node_sizes, alpha=0.85, edgecolors="#ffffff",
                           linewidths=1.5)

    labels = {}
    for node in G.nodes():
        name = str(node)
        if len(name) > 14:
            name = name[:11] + "..."
        labels[node] = name

    nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=7,
                            font_color=COLORS["text"], font_weight="bold")

    legend_items = [
        mpatches.Patch(color=COLORS["Kejaksaan"], label="Kejaksaan"),
        mpatches.Patch(color=COLORS["Polri"], label="Polri"),
        mpatches.Patch(color=COLORS["Istana"], label="Istana"),
        mpatches.Patch(color=COLORS["DPR"], label="DPR"),
        mpatches.Patch(color=COLORS["Yudikatif"], label="Yudikatif"),
        mpatches.Patch(color=COLORS["Antikorupsi"], label="Antikorupsi"),
    ]
    ax.legend(handles=legend_items, loc="lower left", fontsize=6,
              facecolor="white", edgecolor="#bdc3c7", framealpha=0.9)
    ax.set_axis_off()


def plot_timeline_panel(ax, timeline):
    ax.set_facecolor(COLORS["bg"])
    ax.set_title("Kapan Berita Muncul?\nJumlah Artikel per Periode",
                 color=COLORS["text"], fontsize=11, fontweight="bold", pad=12, loc="left")

    if not timeline.get("dates"):
        ax.text(0.5, 0.5, "Data tidak tersedia", ha="center", va="center",
                color=COLORS["text"], fontsize=10, transform=ax.transAxes)
        return

    dates = timeline["dates"]
    counts = timeline["counts"]

    if len(dates) > 20:
        dates = dates[-20:]
        counts = counts[-20:]

    x = range(len(dates))
    ax.bar(x, counts, color="#3498db", alpha=0.8, width=0.6, edgecolor="white", linewidth=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels(dates, rotation=45, ha="right", fontsize=6, color=COLORS["text"])
    ax.tick_params(axis="y", colors=COLORS["text"], labelsize=7)
    ax.set_ylabel("Jumlah Artikel", color=COLORS["text"], fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#ddd")
    ax.spines["bottom"].set_color("#ddd")
    ax.yaxis.grid(True, alpha=0.3, color="#ecf0f1")
    ax.set_axisbelow(True)


def plot_sentiment_panel(ax, sentiment):
    ax.set_facecolor(COLORS["bg"])
    ax.set_title("Bagaimana Media Meliput?\nDistribusi Sentimen Berita",
                 color=COLORS["text"], fontsize=11, fontweight="bold", pad=12, loc="left")

    summary = sentiment.get("summary", {})
    labels = ["Negatif", "Netral", "Positif"]
    values = [summary.get("negatif", 0), summary.get("netral", 0), summary.get("positif", 0)]
    colors_pie = ["#e74c3c", "#f1c40f", "#27ae60"]

    if sum(values) == 0:
        ax.text(0.5, 0.5, "Data tidak tersedia", ha="center", va="center",
                color=COLORS["text"], fontsize=10, transform=ax.transAxes)
        return

    wedges, texts, autotexts = ax.pie(
        values, labels=labels, colors=colors_pie,
        autopct=lambda pct: f"{pct:.0f}%\n({int(round(pct/100.*sum(values)))})",
        startangle=90, textprops={"color": COLORS["text"], "fontsize": 8},
        wedgeprops={"edgecolor": "white", "linewidth": 2}
    )
    for at in autotexts:
        at.set_fontsize(7)
        at.set_fontweight("bold")


def plot_source_panel(ax, source_dist):
    ax.set_facecolor(COLORS["bg"])
    ax.set_title("Dari Mana Berita Datang?\nSumber Media Terbanyak",
                 color=COLORS["text"], fontsize=11, fontweight="bold", pad=12, loc="left")

    labels = source_dist.get("labels", [])
    values = source_dist.get("values", [])

    if not labels:
        ax.text(0.5, 0.5, "Data tidak tersedia", ha="center", va="center",
                color=COLORS["text"], fontsize=10, transform=ax.transAxes)
        return

    sorted_data = sorted(zip(values, labels), reverse=True)
    values = [v for v, l in sorted_data]
    labels = [l for v, l in sorted_data]

    y = range(len(labels))
    colors_bar = plt.cm.Blues(np.linspace(0.35, 0.85, len(labels)))

    bars = ax.barh(y, values, color=colors_bar, alpha=0.9, height=0.6, edgecolor="white", linewidth=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7, color=COLORS["text"])
    ax.tick_params(axis="x", colors=COLORS["text"], labelsize=7)
    ax.set_xlabel("Jumlah Artikel", color=COLORS["text"], fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#ddd")
    ax.spines["bottom"].set_color("#ddd")
    ax.xaxis.grid(True, alpha=0.3, color="#ecf0f1")
    ax.set_axisbelow(True)
    ax.invert_yaxis()

    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                str(val), va="center", fontsize=7, color=COLORS["text"], fontweight="bold")


def generate_mapping():
    print("=" * 60)
    print("KASUS INVESTIGATOR - Visual Mapping (Clean White)")
    print("=" * 60)

    analysis = load_analysis()
    graph_data = load_graph()
    if not analysis:
        print("[ERROR] analysis_results.json tidak ditemukan!")
        return

    G = nx.Graph()
    if graph_data:
        G = build_networkx_graph(graph_data)
    centrality = analysis.get("sna", {}).get("centrality", {})

    fig, axes = plt.subplots(2, 2, figsize=(18, 14), facecolor=COLORS["bg"])
    fig.suptitle(
        "KASUS: Konflik Kejaksaan Agung vs Polri (2023-2026)\n"
        "Analisis Berbasis 62 Artikel Berita Publik",
        color=COLORS["text"], fontsize=14, fontweight="bold", y=0.98
    )

    plot_network_panel(axes[0, 0], G, centrality)
    plot_timeline_panel(axes[0, 1], analysis.get("timeline", {}))
    plot_sentiment_panel(axes[1, 0], analysis.get("sentiment", {}))
    plot_source_panel(axes[1, 1], analysis.get("source_distribution", {}))

    plt.tight_layout(rect=[0, 0.02, 1, 0.94])

    map_path = OUTPUT_DIR / "mapping_kasus.png"
    fig.savefig(str(map_path), dpi=150, bbox_inches="tight",
                facecolor=COLORS["bg"], edgecolor="none")
    plt.close(fig)
    print(f"\n[SAVE] {map_path}")

    # Centrality ranking chart
    if centrality:
        fig2, ax2 = plt.subplots(figsize=(14, 8), facecolor=COLORS["bg"])
        ax2.set_facecolor(COLORS["bg"])

        sorted_c = sorted(centrality.items(), key=lambda x: -x[1]["betweenness"])[:15]
        actors = [a for a, _ in sorted_c]
        bn_vals = [m["betweenness"] for _, m in sorted_c]
        deg_vals = [m["degree"] for _, m in sorted_c]

        x = np.arange(len(actors))
        width = 0.35

        ax2.bar(x - width/2, bn_vals, width, label="Betweenness (Pengaruh Jaringan)",
                color="#2c3e50", alpha=0.85)
        ax2.bar(x + width/2, deg_vals, width, label="Degree (Jumlah Koneksi)",
                color="#3498db", alpha=0.85)

        ax2.set_xlabel("Aktor", color=COLORS["text"], fontsize=10)
        ax2.set_ylabel("Skor Centrality", color=COLORS["text"], fontsize=10)
        ax2.set_title("Siapa Paling Berpengaruh? - Top 15 Aktor",
                       color=COLORS["text"], fontsize=13, fontweight="bold", pad=15)
        ax2.set_xticks(x)
        ax2.set_xticklabels(actors, rotation=45, ha="right", fontsize=8, color=COLORS["text"])
        ax2.tick_params(axis="y", colors=COLORS["text"], labelsize=8)
        ax2.legend(facecolor="white", edgecolor="#ddd", fontsize=9)
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.spines["left"].set_color("#ddd")
        ax2.spines["bottom"].set_color("#ddd")
        ax2.yaxis.grid(True, alpha=0.3, color="#ecf0f1")
        ax2.set_axisbelow(True)

        plt.tight_layout()
        centrality_path = OUTPUT_DIR / "centrality_ranking.png"
        fig2.savefig(str(centrality_path), dpi=150, bbox_inches="tight",
                     facecolor=COLORS["bg"], edgecolor="none")
        plt.close(fig2)
        print(f"[SAVE] {centrality_path}")

    print("[DONE] Visual mapping selesai!")


if __name__ == "__main__":
    generate_mapping()
