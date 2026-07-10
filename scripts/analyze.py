"""
KASUS INVESTIGATOR - Analisis Data + SNA
Load raw_data.json, jalankan analisis SNA, sentimen, timeline
Output: output/analysis_results.json
"""

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import networkx as nx
import pandas as pd
import numpy as np

OUTPUT_DIR = Path(__file__).parent.parent / "output"

# Sentimen lexicon sederhana (Indonesia)
POSITIVE_WORDS = {
    "baik", "berhasil", "dukung", "positif", "sukses", "capai", "menang",
    "unggul", "solid", "komitmen", "perkuat", "sinergi", "harapan", "optimis",
    "setuju", "apresiasi", "puji", "terima kasih", "prestasi", "maju",
}
NEGATIVE_WORDS = {
    "konflik", "krisis", "korupsi", "jahat", "salah", "gagal", "buruk",
    "hancur", "rusak", "tuding", "saling", "serang", "kriminal", "curang",
    "manipulasi", "kekerasan", "ancaman", "bahaya", "terburuk", "skandal",
    "perseteruan", "adu", "bentrok", "pecah", "retak", "gelap", "suram",
    "merugikan", "dugaan", "cacat", "lemah", "bobrok", "dust", "bohong",
    "kontroversi", "polemik", "gesekan", "tarik-menarik", "berebut",
}


def load_data():
    """Load data scraping."""
    json_path = OUTPUT_DIR / "raw_data.json"
    if not json_path.exists():
        print("[ERROR] raw_data.json tidak ditemukan! Jalankan scrape.py dulu.")
        return None
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def analyze_sentiment(text):
    """Analisis sentimen sederhana berbasis lexicon."""
    words = set(re.findall(r"\w+", text.lower()))
    pos = len(words & POSITIVE_WORDS)
    neg = len(words & NEGATIVE_WORDS)
    total = pos + neg
    if total == 0:
        return "netral", 0.0
    score = (pos - neg) / total
    if score > 0.2:
        return "positif", score
    elif score < -0.2:
        return "negatif", score
    return "netral", score


def build_network(data):
    """Bangun jaringan aktor dari data artikel."""
    G = nx.Graph()

    known_actors = {
        "St Burhanuddin": "Kejaksaan",
        "Burhanuddin": "Kejaksaan",
        "Sanitiar Burhanuddin": "Kejaksaan",
        "Listyo Sigit Prabowo": "Polri",
        "Listyo Sigit": "Polri",
        "Kapolri": "Polri",
        "Kabareskrim": "Polri",
        "Prabowo Subianto": "Polri",
        "Prabowo": "Polri",
        "Jokowi": "Istana",
        "Joko Widodo": "Istana",
        "Mahfud MD": "Istana",
        "Komisi III DPR": "DPR",
        "DPR": "DPR",
        "Mahkamah Agung": "Yudikatif",
        "Mahkamah Konstitusi": "Yudikatif",
        "KPK": "Antikorupsi",
        "LPSK": "Antikorupsi",
        "Ombudsman": "Antikorupsi",
    }

    # Tambah node untuk setiap institusi/faksi
    factions = ["Kejaksaan", "Polri", "Istana", "DPR", "Yudikatif", "Antikorupsi"]
    for f in factions:
        G.add_node(f, type="faction", size=3000)

    # Co-mention = edge
    for article in data["articles"]:
        text = f"{article['title']} {article['snippet']}"
        mentioned = []
        for actor, faction in known_actors.items():
            if actor.lower() in text.lower():
                mentioned.append((actor, faction))

        # Tambah edge antar aktor yang muncul bersama
        for i in range(len(mentioned)):
            a1, f1 = mentioned[i]
            G.add_node(a1, type="actor", faction=f1, size=800)
            if not G.has_edge(f1, a1):
                G.add_edge(f1, a1, weight=0)
            G[f1][a1]["weight"] += 1

            for j in range(i + 1, len(mentioned)):
                a2, f2 = mentioned[j]
                G.add_node(a2, type="actor", faction=f2, size=800)
                if a1 != a2:
                    key = tuple(sorted([a1, a2]))
                    if not G.has_edge(a1, a2):
                        G.add_edge(a1, a2, weight=0)
                    G[a1][a2]["weight"] += 1
                    if f1 != f2:
                        if not G.has_edge(f1, f2):
                            G.add_edge(f1, f2, weight=0)
                        G[f1][f2]["weight"] += 1

    return G


def analyze_timeline(data):
    """Analisis timeline artikel."""
    dated = [a for a in data["articles"] if a.get("date")]
    if not dated:
        return {"dates": [], "counts": []}

    df = pd.DataFrame(dated)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df = df.sort_values("date")

    # Agregasi per bulan
    df["month"] = df["date"].dt.to_period("M")
    monthly = df.groupby("month").size()

    return {
        "dates": [str(d) for d in monthly.index],
        "counts": monthly.values.tolist(),
        "total_dated": len(df),
    }


def analyze_source_distribution(data):
    """Analisis distribusi sumber."""
    source_counts = data["statistics"]["by_source"]
    return {
        "labels": list(source_counts.keys()),
        "values": list(source_counts.values()),
    }


def analyze_keyword_relevance(data):
    """Analisis relevansi keyword."""
    kw_counts = data["statistics"]["by_keyword"]
    sorted_kw = sorted(kw_counts.items(), key=lambda x: -x[1])
    return {
        "labels": [k for k, v in sorted_kw[:10]],
        "values": [v for k, v in sorted_kw[:10]],
    }


def compute_centrality(G):
    """Hitung centrality metrics untuk setiap node."""
    if len(G.nodes()) == 0:
        return {}

    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G, weight="weight")

    centrality = {}
    for node in G.nodes():
        centrality[node] = {
            "degree": round(degree.get(node, 0), 4),
            "betweenness": round(betweenness.get(node, 0), 4),
            "degree_weighted": G.degree(node, weight="weight"),
        }
    return centrality


def main():
    print("=" * 60)
    print("KASUS INVESTIGATOR - Analisis Data")
    print("=" * 60)

    data = load_data()
    if not data:
        return

    print(f"[LOAD] {len(data['articles'])} artikel dimuat")

    # 1. Sentimen Analysis
    print("\n[ANALISIS] Sentimen...")
    sentiments = {"positif": 0, "negatif": 0, "netral": 0}
    sentiment_details = []
    for article in data["articles"]:
        text = f"{article['title']} {article['snippet']}"
        sent, score = analyze_sentiment(text)
        sentiments[sent] += 1
        sentiment_details.append({
            "title": article["title"],
            "sentiment": sent,
            "score": round(score, 3),
        })

    print(f"  Positif: {sentiments['positif']}")
    print(f"  Negatif: {sentiments['negatif']}")
    print(f"  Netral:  {sentiments['netral']}")

    # 2. Network Analysis (SNA)
    print("\n[ANALISIS] Social Network Analysis...")
    G = build_network(data)
    centrality = compute_centrality(G)

    print(f"  Nodes: {G.number_of_nodes()}")
    print(f"  Edges: {G.number_of_edges()}")
    if centrality:
        top_betweenness = sorted(centrality.items(), key=lambda x: -x[1]["betweenness"])[:5]
        print("  Top 5 Betweenness Centrality:")
        for actor, metrics in top_betweenness:
            print(f"    {actor}: {metrics['betweenness']}")

    # 3. Timeline Analysis
    print("\n[ANALISIS] Timeline...")
    timeline = analyze_timeline(data)
    print(f"  Artikel bertanggal: {timeline.get('total_dated', 0)}")

    # 4. Source Distribution
    print("\n[ANALISIS] Distribusi Sumber...")
    source_dist = analyze_source_distribution(data)

    # 5. Keyword Relevance
    print("\n[ANALISIS] Relevansi Keyword...")
    kw_relevance = analyze_keyword_relevance(data)

    # Simpan hasil analisis
    analysis = {
        "metadata": {
            "analyzed_at": datetime.now().isoformat(),
            "total_articles": len(data["articles"]),
        },
        "sentiment": {
            "summary": sentiments,
            "details": sentiment_details,
        },
        "sna": {
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "centrality": centrality,
            "factions": list(set(
                data.get("type") == "faction"
                for _, data in G.nodes(data=True)
            )),
        },
        "timeline": timeline,
        "source_distribution": source_dist,
        "keyword_relevance": kw_relevance,
        "actor_mentions": data.get("actor_mentions", {}),
    }

    json_path = OUTPUT_DIR / "analysis_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    print(f"\n[SAVE] {json_path}")

    # Simpan graph untuk visualisasi
    graph_data = {
        "nodes": [{"id": n, **G.nodes[n]} for n in G.nodes()],
        "edges": [{"source": u, "target": v, "weight": G[u][v].get("weight", 1)} for u, v in G.edges()],
    }
    graph_path = OUTPUT_DIR / "network_graph.json"
    with open(graph_path, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)
    print(f"[SAVE] {graph_path}")

    print("\n[DONE] Analisis selesai!")
    return analysis


if __name__ == "__main__":
    main()
