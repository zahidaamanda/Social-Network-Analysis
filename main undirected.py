# ============================================
# SOCIAL NETWORK ANALYSIS WITH NETWORKX
# DEGREE CENTRALITY ANALYSIS (UNDIRECTED)
# ============================================
# Program ini mengimplementasikan Social Network Analysis (SNA)
# menggunakan graf TIDAK BERARAH (undirected graph).
# Tujuan utama: mengukur Degree Centrality tiap node untuk
# menemukan aktor paling aktif/sentral dalam jaringan sosial.
# Referensi: Jurnal JITEK vol.6 no.1, Handoko et al. (2026)

import pandas as pd                 # untuk membaca dan memanipulasi data tabular (CSV)
import networkx as nx               # library utama analisis dan pemodelan graf/jaringan
import matplotlib.pyplot as plt     # untuk visualisasi/plotting graf
import matplotlib.patheffects as pe # untuk efek outline pada teks label

# ─────────────────────────────────────────
# HELPER: gambar label dengan outline tipis
# ─────────────────────────────────────────

def draw_labels_with_outline(G, pos, labels=None, font_size=9,
                              font_color='black', outline_color='white',
                              outline_width=3, ax=None):
    # Fungsi custom untuk menggambar label node dengan outline putih di sekeliling
    # teks agar label tetap terbaca meski node/edge saling berdekatan atau bertumpuk.
    if ax is None:
        ax = plt.gca()  # ambil axes aktif jika tidak disediakan

    if labels is None:
        labels = {node: str(node) for node in G.nodes()}
        # Default: gunakan nama node itu sendiri sebagai label

    for node, label in labels.items():
        x, y = pos[node]  # ambil koordinat posisi node di canvas
        ax.text(
            x, y, label,
            fontsize=font_size,
            ha='center', va='center',
            color=font_color,
            path_effects=[
                pe.withStroke(linewidth=outline_width, foreground=outline_color)
                # withStroke menambahkan lapisan outline di balik teks
                # sehingga teks lebih mudah dibaca di atas latar apapun
            ]
        )


# A. LOAD DATA

df = pd.read_csv("celeb_edgelist.csv")
# Membaca edge list dari file CSV ke dalam DataFrame pandas.
# Edge list adalah format data paling umum dalam SNA:
# setiap baris merepresentasikan SATU hubungan (edge) antara dua entitas.
# Contoh isi file: kolom "From" berisi nama node asal, "To" berisi node tujuan.

print("=== DATASET ===")
print(df.head())  # tampilkan 5 baris pertama untuk memvalidasi data sudah terbaca benar

# GRAPH CONSTRUCTION

G = nx.from_pandas_edgelist(
    df,
    source='From',   # kolom yang menjadi satu ujung hubungan
    target='To'      # kolom yang menjadi ujung lain hubungan
)
# Default NetworkX adalah nx.Graph() = graf TIDAK BERARAH.
# Artinya: hubungan A-B otomatis berarti B-A juga ada (simetris/timbal balik).
# Tidak ada parameter create_using=nx.DiGraph() seperti pada directed graph.

print("\n=== INFORMASI GRAPH ===")
print(f"Jumlah node : {G.number_of_nodes()}")  # berapa banyak aktor
print(f"Jumlah edge : {G.number_of_edges()}")  # berapa banyak hubungan unik
print(f"Tipe graph  : {type(G).__name__}")      # pastikan bertipe Graph (undirected)


# B. PERHITUNGAN DEGREE

degree_map = dict(nx.degree(G))
# nx.degree(G) mengembalikan DegreeView: pasangan (node, degree) untuk semua node.
# Untuk UNDIRECTED graph, degree = jumlah total edge yang terhubung ke node tersebut.
# Tidak ada pembedaan in/out degree seperti pada directed graph.
# dict() mengubahnya menjadi dictionary Python biasa: {nama_node: nilai_degree}

print("\n=== DEGREE TIAP NODE ===")
print(f"{'Node':<20} {'Degree':>8}")
print("-" * 30)

sorted_degree = sorted(
    degree_map.items(),
    key=lambda item: item[1],
    reverse=True   # descending: degree terbesar di atas
)

for node, degree in sorted_degree:
    print(f"{node:<20} {degree:>8}")


# LAYOUT UTAMA (dipakai visualisasi 1 & 2)

pos = nx.kamada_kawai_layout(G)
# kamada_kawai_layout: algoritma layout berbasis minimisasi energi (spring model).
# Menghasilkan tata letak yang lebih "rapi" dan proporsional dibanding spring_layout,
# karena mempertimbangkan jarak terpendek antar semua pasang node (all-pairs shortest path).
# Lebih lambat tapi lebih estetis untuk visualisasi akademik.


# C. VISUALISASI 1: DEGREE (HEATMAP YlOrRd)

max_degree = max(degree_map.values()) or 1
# Nilai degree terbesar, digunakan sebagai pembagi normalisasi.
# "or 1" mencegah pembagian dengan nol jika semua node tidak punya koneksi.

node_colors = [degree_map[n] / max_degree for n in G.nodes()]
# Normalisasi degree ke rentang [0,1] untuk dipakai sebagai skala warna colormap.
# Node dengan degree tertinggi → warna paling pekat (merah).
# Contoh: Node A punya 5 koneksi, max_degree=10 → 5/10 = 0.5 (warna sedang/oranye).

node_sizes = [degree_map[n] * 400 + 300 for n in G.nodes()]
# Ukuran node proporsional terhadap degree.
# +300 = ukuran minimum agar node tidak terlalu kecil meski degree rendah.
# *400 = faktor skala agar perbedaan ukuran terlihat jelas.

fig, ax = plt.subplots(figsize=(13, 13))

fig.suptitle(
    "Visualisasi Undirected Graph – Degree\n"
    "(ukuran = degree, warna = degree ternormalisasi)",
    fontsize=13, fontweight='bold', y=0.95
)

# 1. Gambar node
nodes_drawn = nx.draw_networkx_nodes(
    G, pos,
    node_size=node_sizes,
    node_color=node_colors,
    cmap=plt.cm.YlOrRd,
    # YlOrRd = colormap Yellow-Orange-Red
    # Node dengan degree rendah = kuning, tinggi = merah
    alpha=0.9,
    ax=ax
)

# 2. Gambar edge
nx.draw_networkx_edges(
    G, pos,
    edge_color='gray',
    alpha=0.6,
    ax=ax
    # Pada undirected graph, edge digambar sebagai garis lurus tanpa panah,
    # mencerminkan hubungan simetris (tidak ada arah).
    # Tidak perlu parameter arrowstyle/arrowsize/connectionstyle.
)

# Nama node
draw_labels_with_outline(
    G, pos,
    font_size=9,
    font_color='black',
    outline_color='white',
    outline_width=1,
    ax=ax
)

# Sub-label degree
degree_labels = {
    node: f"deg:{degree_map[node]}"
    for node in G.nodes()
    # Buat label tambahan di bawah nama node yang menampilkan nilai degree
}
label_pos = {k: (v[0], v[1] - 0.055) for k, v in pos.items()}
# Geser posisi label ke bawah sebesar 0.055 unit agar tidak menimpa nama node

draw_labels_with_outline(
    G, label_pos,
    labels=degree_labels,
    font_size=7,
    font_color='blue',   # warna biru untuk membedakan dari nama node
    outline_color='white',
    outline_width=1,
    ax=ax
)

plt.colorbar(nodes_drawn, ax=ax, label="Degree (normalized)")
# Tampilkan gradient warna (colorbar) di sisi kanan gambar
# sehingga pembaca tahu makna warna kuning vs merah

ax.axis('off')
plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.show()
plt.close()


# D. DEGREE CENTRALITY

dc = nx.degree_centrality(G)
# Fungsi inti analisis ini.
# Menghitung Degree Centrality TERNORMALISASI untuk setiap node.
# Formula yang digunakan NetworkX:
#   DC(v) = degree(v) / (N - 1)
#   N = jumlah total node dalam graf
#   N-1 = jumlah maksimum koneksi yang MUNGKIN dimiliki satu node
# Hasil: nilai antara 0 (tidak ada koneksi) dan 1 (terhubung ke semua node lain).
# Normalisasi ini penting agar nilai bisa dibandingkan lintas jaringan
# yang memiliki ukuran (N) berbeda-beda.

print("\n=== DEGREE CENTRALITY ===")
print(f"{'Node':<20} {'DC':>8}")
print("-" * 30)

most_influential = sorted(
    dc.items(),
    key=lambda item: item[1],
    reverse=True   # descending: DC tertinggi di atas
)

for node, centrality in most_influential:
    print(f"{node:<20} {centrality:>8.4f}")


# E. VISUALISASI 2: DEGREE CENTRALITY (HEATMAP PLASMA)

centrality_sizes  = [dc[n] * 6000 + 200 for n in G.nodes()]
# Ukuran node proporsional terhadap DC.
# *6000 = faktor skala besar agar perbedaan centrality terlihat dramatis secara visual.
# +200 = ukuran minimum agar node tetap terlihat.

centrality_colors = [dc[n] for n in G.nodes()]
# Warna mengikuti nilai degree centrality,
# sehingga warna dan ukuran keduanya mengkodekan besarnya centrality.

fig, ax = plt.subplots(figsize=(13, 13))

fig.suptitle(
    "Visualisasi Undirected Graph – Degree Centrality\n"
    "(ukuran = DC, warna = DC)",
    fontsize=13, fontweight='bold', y=0.95
)

# 1. Gambar node
nodes_drawn2 = nx.draw_networkx_nodes(
    G, pos,
    node_size=centrality_sizes,
    node_color=centrality_colors,
    cmap=plt.cm.plasma,
    # plasma = colormap ungu-kuning; lebih kontras dari YlOrRd
    # Node dengan DC rendah = ungu gelap; tinggi = kuning cerah
    alpha=0.85,
    ax=ax
)

# 2. Gambar edge
nx.draw_networkx_edges(
    G, pos,
    edge_color='gray',
    alpha=0.5,
    ax=ax
    # Undirected: tidak ada panah, tidak perlu arrowstyle/connectionstyle
)

# Nama node
draw_labels_with_outline(
    G, pos,
    font_size=9,
    font_color='white',   # putih agar kontras di atas node yang berwarna gelap (plasma)
    outline_color='black',
    outline_width=1,
    ax=ax
)

# Sub-label degree dan centrality
centrality_labels = {
    node: f"deg:{degree_map[node]}\nDC:{dc[node]:.2f}"
    for node in G.nodes()
    # Menampilkan Degree dan Degree Centrality di bawah nama node
}

centrality_label_pos = {
    k: (v[0], v[1] - 0.08)
    for k, v in pos.items()
}
# Geser posisi 0.08 unit ke bawah

draw_labels_with_outline(
    G,
    centrality_label_pos,
    labels=centrality_labels,
    font_size=6,
    font_color='cyan',
    outline_color='black',
    outline_width=1,
    ax=ax
)

plt.colorbar(nodes_drawn2, ax=ax, label="Degree Centrality")
ax.axis('off')
plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.show()
plt.close()


# TOP 5 NODE PALING SENTRAL

print("\n=== TOP 5 NODE PALING SENTRAL (Degree Centrality) ===")
for i, (node, centrality) in enumerate(most_influential[:5], start=1):
    print(f"{i}. {node:<20} DC: {centrality:.4f} | Degree: {degree_map[node]}")


# SIMPAN HASIL KE CSV

result_df = pd.DataFrame([
    {
        'Node'             : node,
        'Degree'           : degree_map[node],
        'Degree_Centrality': dc[node],
    }
    for node, _ in most_influential  # urutan: dari node paling sentral
])

result_df.to_csv("hasil_degree_centrality.csv", index=False)
# Simpan ke CSV tanpa kolom index bawaan pandas
print("\nHasil berhasil disimpan ke hasil_degree_centrality.csv")
