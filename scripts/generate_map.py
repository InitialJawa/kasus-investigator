"""
KASUS INVESTIGATOR - Visual Mapping Generator
Membuat visualisasi: Network Graph, Timeline, Sentiment, Source Distribution
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

# Warna
COLORS = {
    "Kejaksaan": "#e74c3c",
    "Polri": "#3498db",
    "Istana": "#f39c12",
    "DPR": "#2ecc71",
    "Yudikatif": "#9b59b6",
    "Antikorupsi": "#1abc9c",
    "unknown": "#95a5a6",
    "bg": "#0d0d0d",
    "text": "#e0e0e0",
    "accent": "#00ff88",
    "grid": "#333333",
}


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


def load_graph():
    path = OUTPUT_DIR / "network_graph.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_networkx_graph(graph_data):
    """Rebuild NetworkX graph from JSON data."""
    G = nx.Graph()
    for node in graph_data["nodes"]:
        G.add_node(node["id"], **{k: v for k, v in node.items() if k != "id"})
    for edge in graph_data["edges"]:
        G.add_edge(edge["source"], edge["target"], weight=edge.get("weight", 1))
    return G


def plot_network_panel(ax, G, centrality):
    """Panel 1: Network Graph."""
    ax.set_facecolor(COLORS["bg"])
    ax.set_title("SOCIAL NETWORK ANALYSIS", color=COLORS["accent"], fontsize=12, fontweight="bold", pad=10)

    if G.number_of_nodes() == 0:
        ax.text(0.5, 0.5, "Tidak ada data jaringan", ha="center", va="center",
                color=COLORS["text"], fontsize=10, transform=ax.transAxes)
        return

    # Layout
    try:
        pos = nx.spring_layout(G, k=2.5, iterations=50, seed=42)
    except Exception:
        pos = nx.random_layout(G, seed=42)

    # Node colors berdasarkan faction
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        faction = G.nodes[node].get("faction", G.nodes[node].get("id", "unknown"))
        if faction in COLORS:
            node_colors.append(COLORS[faction])
        elif node in COLORS:
            node_colors.append(COLORS[node])
        else:
            node_colors.append(COLORS["unknown"])

        if G.nodes[node].get("type") == "faction":
            node_sizes.append(2000)
        else:
            node_sizes.append(800)

    # Edge widths
    edge_weights = [G[u][v].get("weight", 1) for u, v in G.edges()]
    max_w = max(edge_weights) if edge_weights else 1
    edge_widths = [0.5 + (w / max_w) * 3 for w in edge_weights]

    # Draw
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#555555",
                           width=edge_widths, alpha=0.6)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                           node_size=node_sizes, alpha=0.9, edgecolors="#ffffff",
                           linewidths=0.5)

    # Labels
    labels = {}
    for node in G.nodes():
        name = str(node)
        if len(name) > 15:
            name = name[:12] + "..."
        labels[node] = name

    nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=6,
                            font_color=COLORS["text"], font_weight="bold")

    # Legend
    legend_items = [
        mpatches.Patch(color=COLORS["Kejaksaan"], label="Kejaksaan"),
        mpatches.Patch(color=COLORS["Polri"], label="Polri"),
        mpatches.Patch(color=COLORS["Istana"], label="Istana"),
        mpatches.Patch(color=COLORS["DPR"], label="DPR"),
        mpatches.Patch(color=COLORS["Yudikatif"], label="Yudikatif"),
        mpatches.Patch(color=COLORS["Antikorupsi"], label="Antikorupsi"),
    ]
    ax.legend(handles=legend_items, loc="lower left", fontsize=5,
              facecolor=COLORS["bg"], edgecolor=COLORS["grid"],
              labelcolor=COLORS["text"])


def plot_timeline_panel(ax, timeline):
    """Panel 2: Timeline Chart."""
    ax.set_facecolor(COLORS["bg"])
    ax.set_title("TIMELINE PUBLIKASI", color=COLORS["accent"], fontsize=12, fontweight="bold", pad=10)

    if not timeline.get("dates"):
        ax.text(0.5, 0.5, "Data timeline tidak tersedia", ha="center", va="center",
                color=COLORS["text"], fontsize=10, transform=ax.transAxes)
        return

    dates = timeline["dates"]
    counts = timeline["counts"]

    # Ambil 20 terakhir
    if len(dates) > 20:
        dates = dates[-20:]
        counts = counts[-20:]

    x = range(len(dates))
    bars = ax.bar(x, counts, color=COLORS["accent"], alpha=0.7, width=0.6)

    ax.set_xticks(x)
    ax.set_xticklabels(dates, rotation=45, ha="right", fontsize=5, color=COLORS["text"])
    ax.tick_params(axis="y", colors=COLORS["text"], labelsize=6)
    ax.set_ylabel("Jumlah Artikel", color=COLORS["text"], fontsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLORS["grid"])
    ax.spines["bottom"].set_color(COLORS["grid"])
    ax.yaxis.grid(True, alpha=0.2, color=COLORS["grid"])


def plot_sentiment_panel(ax, sentiment):
    """Panel 3: Sentiment Pie Chart."""
    ax.set_facecolor(COLORS["bg"])
    ax.set_title("DISTRIBUSI SENTIMEN", color=COLORS["accent"], fontsize=12, fontweight="bold", pad=10)

    summary = sentiment.get("summary", {})
    labels = ["Negatif", "Netral", "Positif"]
    values = [summary.get("negatif", 0), summary.get("netral", 0), summary.get("positif", 0)]
    colors_pie = ["#e74c3c", "#f39c12", "#2ecc71"]

    if sum(values) == 0:
        ax.text(0.5, 0.5, "Data sentimen tidak tersedia", ha="center", va="center",
                color=COLORS["text"], fontsize=10, transform=ax.transAxes)
        return

    wedges, texts, autotexts = ax.pie(
        values, labels=labels, colors=colors_pie,
        autopct=lambda pct: f"{pct:.1f}%\n({int(round(pct/100.*sum(values)))})",
        startangle=90, textprops={"color": COLORS["text"], "fontsize": 7}
    )
    for at in autotexts:
        at.set_fontsize(6)


def plot_source_panel(ax, source_dist):
    """Panel 4: Source Distribution Bar Chart."""
    ax.set_facecolor(COLORS["bg"])
    ax.set_title("DISTRIBUSI SUMBER", color=COLORS["accent"], fontsize=12, fontweight="bold", pad=10)

    labels = source_dist.get("labels", [])
    values = source_dist.get("values", [])

    if not labels:
        ax.text(0.5, 0.5, "Data sumber tidak tersedia", ha="center", va="center",
                color=COLORS["text"], fontsize=10, transform=ax.transAxes)
        return

    # Sort by value
    sorted_data = sorted(zip(values, labels), reverse=True)
    values = [v for v, l in sorted_data]
    labels = [l for v, l in sorted_data]

    y = range(len(labels))
    colors_bar = plt.cm.viridis(np.linspace(0.3, 0.9, len(labels)))

    bars = ax.barh(y, values, color=colors_bar, alpha=0.8, height=0.6)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7, color=COLORS["text"])
    ax.tick_params(axis="x", colors=COLORS["text"], labelsize=6)
    ax.set_xlabel("Jumlah Artikel", color=COLORS["text"], fontsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLORS["grid"])
    ax.spines["bottom"].set_color(COLORS["grid"])
    ax.xaxis.grid(True, alpha=0.2, color=COLORS["grid"])
    ax.invert_yaxis()

    # Value labels
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                str(val), va="center", fontsize=6, color=COLORS["text"])


def generate_mapping():
    """Generate visual mapping PNG (4-panel)."""
    print("=" * 60)
    print("KASUS INVESTIGATOR - Visual Mapping Generator")
    print("=" * 60)

    analysis = load_analysis()
    graph_data = load_graph()
    if not analysis:
        print("[ERROR] analysis_results.json tidak ditemukan!")
        return

    # Build NetworkX graph
    G = nx.Graph()
    if graph_data:
        G = build_networkx_graph(graph_data)
    centrality = analysis.get("sna", {}).get("centrality", {})

    # Create 2x2 figure
    fig, axes = plt.subplots(2, 2, figsize=(20, 16), facecolor=COLORS["bg"])
    fig.suptitle(
        "KASUS INVESTIGASI: Kejaksaan Agung vs Polri (2023-2026)",
        color=COLORS["accent"], fontsize=16, fontweight="bold", y=0.98
    )

    # Panel 1: Network Graph
    plot_network_panel(axes[0, 0], G, centrality)

    # Panel 2: Timeline
    plot_timeline_panel(axes[0, 1], analysis.get("timeline", {}))

    # Panel 3: Sentiment
    plot_sentiment_panel(axes[1, 0], analysis.get("sentiment", {}))

    # Panel 4: Source Distribution
    plot_source_panel(axes[1, 1], analysis.get("source_distribution", {}))

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Simpan
    map_path = OUTPUT_DIR / "mapping_kasus.png"
    fig.savefig(str(map_path), dpi=150, bbox_inches="tight",
                facecolor=COLORS["bg"], edgecolor="none")
    plt.close(fig)
    print(f"\n[SAVE] {map_path}")
    print("[DONE] Visual mapping selesai!")

    # Generate centrality ranking chart
    if centrality:
        fig2, ax2 = plt.subplots(figsize=(14, 8), facecolor=COLORS["bg"])
        ax2.set_facecolor(COLORS["bg"])

        # Top 15 by betweenness
        sorted_c = sorted(centrality.items(), key=lambda x: -x[1]["betweenness"])[:15]
        actors = [a for a, _ in sorted_c]
        bn_vals = [m["betweenness"] for _, m in sorted_c]
        deg_vals = [m["degree"] for _, m in sorted_c]

        x = np.arange(len(actors))
        width = 0.35

        bars1 = ax2.bar(x - width/2, bn_vals, width, label="Betweenness",
                        color=COLORS["accent"], alpha=0.8)
        bars2 = ax2.bar(x + width/2, deg_vals, width, label="Degree",
                        color="#3498db", alpha=0.8)

        ax2.set_xlabel("Aktor", color=COLORS["text"], fontsize=10)
        ax2.set_ylabel("Centrality Score", color=COLORS["text"], fontsize=10)
        ax2.set_title("CENTRALITY RANKING - TOP 15 AKTOR",
                       color=COLORS["accent"], fontsize=14, fontweight="bold", pad=15)
        ax2.set_xticks(x)
        ax2.set_xticklabels(actors, rotation=45, ha="right", fontsize=7, color=COLORS["text"])
        ax2.tick_params(axis="y", colors=COLORS["text"], labelsize=8)
        ax2.legend(facecolor=COLORS["bg"], edgecolor=COLORS["grid"],
                   labelcolor=COLORS["text"], fontsize=9)
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.spines["left"].set_color(COLORS["grid"])
        ax2.spines["bottom"].set_color(COLORS["grid"])
        ax2.yaxis.grid(True, alpha=0.2, color=COLORS["grid"])

        plt.tight_layout()
        centrality_path = OUTPUT_DIR / "centrality_ranking.png"
        fig2.savefig(str(centrality_path), dpi=150, bbox_inches="tight",
                     facecolor=COLORS["bg"], edgecolor="none")
        plt.close(fig2)
        print(f"[SAVE] {centrality_path}")


if __name__ == "__main__":
    generate_mapping()
