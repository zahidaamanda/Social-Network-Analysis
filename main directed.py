# ============================================
# SOCIAL NETWORK ANALYSIS WITH NETWORKX
# DIRECTED GRAPH - DEGREE CENTRALITY ANALYSIS
# ============================================
# Program ini menganalisis jaringan sosial selebriti menggunakan
# directed graph (graf berarah). Kita mengukur siapa yang paling
# berpengaruh berdasarkan seberapa banyak koneksi yang dimiliki.

import pandas as pd                 # untuk membaca dan memanipulasi data CSV
import networkx as nx               # library utama untuk analisis graf dan jaringan
import matplotlib.pyplot as plt     # untuk visualisasi/plot graf
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
# Membaca edge list dari file CSV.
# Edge list = daftar pasangan (From, To) yang merepresentasikan koneksi antar node.
# Contoh isi: "BTS,BLACKPINK" artinya BTS mengikuti / terhubung ke BLACKPINK.

print("=== DATASET ===")
print(df.head())  # tampilkan 5 baris pertama untuk validasi data

# GRAPH CONSTRUCTION (DiGraph = berarah)

G = nx.from_pandas_edgelist(
    df,
    source='From',   # kolom yang menjadi asal edge (siapa yang "mengirim" koneksi)
    target='To',     # kolom yang menjadi tujuan edge (siapa yang "menerima" koneksi)
    create_using=nx.DiGraph()
    # DiGraph = Directed Graph (graf berarah)
    # Berbeda dengan Graph() biasa, DiGraph menyimpan arah tiap koneksi.
    # A→B tidak sama dengan B→A.
)

print("\n=== INFORMASI GRAPH ===")
print(f"Jumlah node  : {G.number_of_nodes()}")  # berapa banyak entitas (selebriti)
print(f"Jumlah edge  : {G.number_of_edges()}")  # berapa banyak koneksi/hubungan
print(f"Tipe graph   : {type(G).__name__}")     # pastikan bertipe DiGraph

# B. VISUALISASI 1: GRAPH DASAR

fig, ax = plt.subplots(figsize=(10, 10))
# Buat figure ukuran 10x10 inci

fig.suptitle(
    "Visualisasi Directed Graph",
    fontsize=14, fontweight='bold', y=0.95
)

pos_basic = nx.spring_layout(G, k=1.5, iterations=50, seed=42)
# spring_layout: algoritma force-directed layout (Fruchterman-Reingold), bertugas menghitung posisi terbaik agar graf tersebut rapi dan mudah dibaca manusia.
# Node yang terhubung saling "menarik", node yang tidak terhubung saling "mendorong".
# k=1.5 → jarak ideal antar node (semakin besar, semakin renggang)
# iterations=50 → jumlah iterasi simulasi fisika. Menentukan berapa kali algoritma mengulang perhitungan gaya tarik dan tolak sebelum berhenti.
# seed=42 → agar posisi node konsisten setiap kali dijalankan

# 1. Gambar node terlebih dahulu
nx.draw_networkx_nodes(
    G, pos_basic,
    node_color='yellow',
    node_size=1000,   # ukuran lingkaran node dalam satuan area (pixel^2)
    alpha=0.9,        # transparansi: 0=transparan penuh, 1=solid penuh
    ax=ax
)

# 2. Gambar edge dengan menyertakan node_size agar panah berhenti di luar lingkaran
nx.draw_networkx_edges(
    G, pos_basic,
    edge_color='gray',
    alpha=0.6,
    node_size=1000,
    arrowstyle='-|>',
    arrowsize=20,
    # ukuran kepala panah dalam poin
    connectionstyle='arc3,rad=0.1',
    # arc3 = edge melengkung; rad=0.1 = sedikit melengkung
    # kelengkungan mencegah dua panah saling bertumpuk dan tidak terbaca
    ax=ax
)

#3. Outline label atau nama aktor node supaya mudah dibaca
draw_labels_with_outline(
    G, pos_basic,
    font_size=9,
    font_color='black',
    outline_color='white',
    outline_width=1,
    ax=ax
)

ax.axis('off')                          # sembunyikan sumbu x dan y (tidak diperlukan)
plt.tight_layout(rect=[0, 0, 1, 0.93]) # atur margin agar title tidak tertutup plot
plt.show()
plt.close()  # tutup figure agar memori tidak bocor saat program lanjut


# C. PERHITUNGAN IN-DEGREE & OUT-DEGREE

in_degree_map    = dict(G.in_degree())
# in_degree = jumlah edge MASUK ke node 

out_degree_map   = dict(G.out_degree())
# out_degree = jumlah edge KELUAR dari node

total_degree_map = {
    node: in_degree_map[node] + out_degree_map[node]
    for node in G.nodes()
    # total_degree = in + out → ukuran aktivitas keseluruhan node
}

print("\n=== DEGREE TIAP NODE (DIRECTED) ===")
print(f"{'Node':<20} {'In-Degree':>10} {'Out-Degree':>11} {'Total':>7}")
print("-" * 52)

sorted_total = sorted(total_degree_map.items(), key=lambda x: x[1], reverse=True)
# Urutkan node berdasarkan total degree, dari terbesar ke terkecil

for node, total in sorted_total:
    print(f"{node:<20} {in_degree_map[node]:>10} {out_degree_map[node]:>11} {total:>7}")

# LAYOUT UTAMA (dipakai visualisasi 2 & 3)

pos = nx.kamada_kawai_layout(G)
# kamada_kawai_layout: algoritma layout berbasis minimisasi energi (spring model).
# Menghasilkan tata letak yang lebih "rapi" dan proporsional dibanding spring_layout,
# karena mempertimbangkan jarak terpendek antar semua pasang node (all-pairs shortest path).
# Lebih lambat tapi lebih estetis untuk visualisasi akademik.


# D. VISUALISASI 2: IN / OUT DEGREE 

max_in      = max(in_degree_map.values()) or 1
# Nilai in-degree terbesar, digunakan sebagai pembagi normalisasi.
# "or 1" mencegah pembagian dengan nol jika semua node tidak punya in-degree.

node_colors = [in_degree_map[n] / max_in for n in G.nodes()] 
# Normalisasi in-degree ke rentang [0,1] untuk dipakai sebagai skala warna colormap.
# Node dengan in-degree tertinggi → warna paling pekat.
# Contoh : Node B punya 5 panah masuk, 5 / 10 (misal max_in=10)= 0.5 (Mendapat warna sedang/transisi).

node_sizes  = [total_degree_map[n] * 400 + 300 for n in G.nodes()]
# Ukuran node proporsional terhadap total degree.
# +300 = ukuran minimum agar node tidak terlalu kecil meski total degree rendah.
# *400 = faktor skala agar perbedaan ukuran terlihat jelas.

fig, ax = plt.subplots(figsize=(13, 13))
# Buat figure ukuran 13x13 inci

fig.suptitle(
    "Visualisasi Directed Graph – In/Out Degree\n"
    "(ukuran = total degree, warna = in-degree)",
    fontsize=13, fontweight='bold', y=0.95
)

# 1. Gambar node
nodes_drawn = nx.draw_networkx_nodes(
    G, pos,
    node_size=node_sizes,
    node_color=node_colors,
    cmap=plt.cm.YlOrRd,
    # YlOrRd = colormap Yellow-Orange-Red
    # Node dengan in-degree rendah = kuning, tinggi = merah
    alpha=0.9,
    ax=ax
)

# 2. Gambar edge dengan melewatkan list node_sizes
nx.draw_networkx_edges(
    G, pos,
    edge_color='gray',
    alpha=0.6,
    node_size=node_sizes,
    # Karena ukuran node berbeda-beda (variabel),
    # kita harus meneruskan list node_sizes agar panah
    # berhenti di tepi masing-masing node dengan tepat.
    arrowstyle='-|>',
    arrowsize=20,
    connectionstyle='arc3,rad=0.1',
    ax=ax
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

# Sub-label in/out degree
degree_labels = {
    node: f"in:{in_degree_map[node]} out:{out_degree_map[node]}"
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

plt.colorbar(nodes_drawn, ax=ax, label="In-Degree (normalized)")
# Tampilkan gradient warna (colorbar) di sisi kanan gambar
# sehingga pembaca tahu makna warna kuning vs merah

ax.axis('off')
plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.show()
plt.close()


# E. DEGREE CENTRALITY (IN, OUT, COMBINED)

in_dc       = nx.in_degree_centrality(G)
# In-degree centrality = in_degree(v) / (N-1)
# N = jumlah node total. N-1 = jumlah node lain (maksimum edge yang mungkin masuk).
# Mengukur seberapa banyak node lain yang "menunjuk" ke node ini.

out_dc      = nx.out_degree_centrality(G)
# Out-degree centrality = out_degree(v) / (N-1)
# Mengukur seberapa aktif node ini dalam "menunjuk" node lain.

combined_dc = {
    node: (in_dc[node] + out_dc[node]) / 2
    for node in G.nodes()
    # Rata-rata in-DC dan out-DC sebagai ukuran pengaruh gabungan.
    # Node yang banyak ditunjuk DAN banyak menunjuk = paling sentral.
}

print("\n=== DEGREE CENTRALITY (DIRECTED) ===")
print(f"{'Node':<20} {'In-DC':>8} {'Out-DC':>8} {'Combined':>10}")
print("-" * 50)

most_influential = sorted(combined_dc.items(), key=lambda x: x[1], reverse=True)
# Urutkan node berdasarkan combined DC, dari paling sentral ke paling pinggir

for node, comb in most_influential:
    print(f"{node:<20} {in_dc[node]:>8.4f} {out_dc[node]:>8.4f} {comb:>10.4f}")


# F. VISUALISASI 3: DEGREE CENTRALITY

centrality_sizes  = [in_dc[n] * 6000 + 200 for n in G.nodes()]
# Ukuran node proporsional terhadap in DC.
# *6000 = faktor skala besar agar perbedaan centrality terlihat dramatis secara visual.
# +200 = ukuran minimum agar node tetap terlihat.

centrality_colors = [in_dc[n] for n in G.nodes()]
# Warna mengikuti in-degree centrality saja (bukan combined),
# sehingga warna dan ukuran mengkodekan dua dimensi berbeda sekaligus.

fig, ax = plt.subplots(figsize=(13, 13))

fig.suptitle(
    "Visualisasi Directed Graph – Degree Centrality\n"
    "(ukuran = in-degree DC, warna = in-degree DC)",
    fontsize=13, fontweight='bold', y=0.95
)

# 1. Gambar node
nodes_drawn2 = nx.draw_networkx_nodes(
    G, pos,
    node_size=centrality_sizes,
    node_color=centrality_colors,
    cmap=plt.cm.plasma,
    # plasma = colormap ungu-kuning; lebih kontras dari YlOrRd
    # Node with low in-DC = ungu gelap; tinggi = kuning cerah
    alpha=0.85,
    ax=ax
)

# 2. Gambar edge dengan melewatkan list centrality_sizes
nx.draw_networkx_edges(
    G, pos,
    edge_color='gray',
    alpha=0.5,
    node_size=centrality_sizes,  # ukuran variabel = panah harus menyesuaikan tiap node
    arrowstyle='-|>',
    arrowsize=20,
    connectionstyle='arc3,rad=0.1',
    ax=ax
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

# Sub-label nilai in DC
centrality_labels = {
    node: f"{in_dc[node]:.2f}"
    for node in G.nodes()
    # Tampilkan nilai combined DC dibulatkan 2 desimal di bawah nama node
}
centrality_label_pos = {k: (v[0], v[1] - 0.06) for k, v in pos.items()}
# Geser posisi 0.06 unit ke bawah

draw_labels_with_outline(
    G, centrality_label_pos,
    labels=centrality_labels,
    font_size=7,
    font_color='cyan',    # cyan kontras dengan warna plasma (ungu/kuning)
    outline_color='black',
    outline_width=1,
    ax=ax
)

plt.colorbar(nodes_drawn2, ax=ax, label="In-Degree Centrality")
ax.axis('off')
plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.show()
plt.close()

# TOP 5 NODE PALING SENTRAL

print("\n=== TOP 5 NODE PALING SENTRAL (Combined DC) ===")
for i, (node, score) in enumerate(most_influential[:5], start=1):
    # Cetak 5 besar selebriti paling berpengaruh berdasarkan combined degree centrality
    print(f"{i}. {node:<20} Combined DC: {score:.4f} "
          f"| In-DC: {in_dc[node]:.4f} | Out-DC: {out_dc[node]:.4f}")

# SIMPAN HASIL KE CSV

result_df = pd.DataFrame([
    {
        'Node'                   : node,
        'In_Degree'              : in_degree_map[node],
        'Out_Degree'             : out_degree_map[node],
        'Total_Degree'           : total_degree_map[node],
        'In_Degree_Centrality'   : in_dc[node],
        'Out_Degree_Centrality'  : out_dc[node],
        'Combined_DC'            : combined_dc[node],
        # Semua metrik dikumpulkan dalam satu baris per node
    }
    for node, _ in most_influential  # urutan: dari node paling sentral
])

result_df.to_csv("hasil_degree_centrality_directed.csv", index=False)
# Simpan ke CSV tanpa kolom index bawaan pandas
print("\nHasil berhasil disimpan ke hasil_degree_centrality_directed.csv")

