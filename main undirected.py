# ============================================
# SOCIAL NETWORK ANALYSIS WITH NETWORKX
# DEGREE CENTRALITY ANALYSIS
# ============================================
# Program ini mengimplementasikan Social Network Analysis (SNA)
# menggunakan graf TIDAK BERARAH (undirected graph).
# Tujuan utama: mengukur Degree Centrality tiap node untuk
# menemukan aktor paling aktif/sentral dalam jaringan sosial.
# Referensi: Jurnal JITEK vol.6 no.1, Handoko et al. (2026)

import pandas as pd        # untuk membaca dan memanipulasi data tabular (CSV)
import networkx as nx      # library utama analisis dan pemodelan graf/jaringan
import matplotlib.pyplot as plt  # untuk visualisasi/plotting graf

# A. LOAD DATA
# Membaca file CSV yang berisi hubungan antar node
df = pd.read_csv("celeb_edgelist.csv")
# Membaca edge list dari file CSV ke dalam DataFrame pandas.
# Edge list adalah format data paling umum dalam SNA:
# setiap baris merepresentasikan SATU hubungan (edge) antara dua entitas.
# Contoh isi file: kolom "From" berisi nama node asal, "To" berisi node tujuan.

print("=== DATASET ===")
print(df.head())  # tampilkan 5 baris pertama untuk memvalidasi data sudah terbaca benar

# GRAPH CONSTRUCTION
# Mengubah data edge list menjadi graph NetworkX

# Membuat graph dari edgelist
G = nx.from_pandas_edgelist(
    df,
    source='From',   # kolom yang menjadi satu ujung hubungan
    target='To'      # kolom yang menjadi ujung lain hubungan
)
# PERBEDAAN DENGAN DIRECTED GRAPH:
# Tidak ada parameter create_using=nx.DiGraph().
# Default NetworkX adalah nx.Graph() = graf TIDAK BERARAH.
# Artinya: hubungan A-B otomatis berarti B-A juga ada (simetris/timbal balik).
# Sesuai dengan asumsi artikel: hubungan antar aktor bersifat setara/mutual.

print("\n=== INFORMASI GRAPH ===")
print(f"Jumlah node: {G.number_of_nodes()}")  # berapa banyak aktor
print(f"Jumlah edge: {G.number_of_edges()}")  # berapa banyak hubungan unik


# B. VISUALISASI GRAPH DASAR

# Menampilkan bentuk jaringan secara umum
plt.figure(figsize=(10, 10))
# Buat canvas gambar 10x10 inci

nx.draw(
    G,
    pos=nx.spring_layout(G, seed=42),
    with_labels=True,    # tampilkan nama/label tiap node
    node_color='yellow', # warna node kuning (sesuai artikel: node_color='y')
    edge_color='gray',   # warna garis penghubung abu-abu
    node_size=1000,      # ukuran semua node sama (belum berdasarkan centrality)
    font_size=10         # ukuran font label node
)

plt.title("Visualisasi Graph")
plt.show()
plt.close()  # tutup figure agar memori tidak terus terpakai


# C. PERHITUNGAN DEGREE

# Menghitung jumlah koneksi pada tiap node
degree_map = dict(nx.degree(G))
# nx.degree(G) mengembalikan DegreeView: pasangan (node, degree) untuk semua node.
# Untuk UNDIRECTED graph, degree = jumlah total edge yang terhubung ke node tersebut.
# Tidak ada pembedaan in/out degree seperti pada directed graph.
# dict() mengubahnya menjadi dictionary Python biasa: {nama_node: nilai_degree}

print("\n=== DEGREE TIAP NODE ===")

sorted_degree = sorted(
    degree_map.items(),        # ambil semua pasangan (node, degree)
    key=lambda item: item[1],  # urutkan berdasarkan nilai degree (item[1])
    reverse=True               # descending: degree terbesar di atas
)
# sorted() mengurutkan list of tuples.
# Hasilnya: node paling banyak koneksi muncul pertama.
# Ini memberi gambaran awal siapa aktor paling "ramai" dalam jaringan.

for node, degree in sorted_degree:
    print(f"Node: {node} -> Degree: {degree}")
    # Cetak setiap node beserta jumlah koneksi langsungnya


# D. VISUALISASI BERDASARKAN DEGREE
# Ukuran node diperbesar sesuai jumlah degree

# ukuran node berdasarkan degree
node_sizes = [v * 500 for v in degree_map.values()]
# List comprehension: setiap node mendapat ukuran = degree × 500.
# Node dengan degree 5 → ukuran 2500; degree 1 → ukuran 500.
# Faktor 500 adalah skala visual agar perbedaan ukuran terlihat jelas.

# layout graph
# Mengatur posisi node agar visual lebih rapi
pos = nx.kamada_kawai_layout(G)
# kamada_kawai_layout: algoritma tata letak berbasis minimisasi energi.
# Prinsip: jarak antar node di layar proporsional dengan jarak terpendek
# (shortest path) antar node di dalam graf.
# Hasil: node yang saling terhubung cenderung berdekatan secara visual,
# kluster terlihat jelas, dan jaringan terlihat lebih "rapi" dibanding spring_layout.
# Lebih lambat dari spring_layout tapi lebih estetis untuk presentasi akademik.

plt.figure(figsize=(12, 12))

# gambar node
nx.draw_networkx_nodes(
    G,
    pos,              # posisi node hasil kamada_kawai_layout
    node_size=node_sizes,   # ukuran variabel sesuai degree
    node_color='skyblue',   # warna biru muda untuk semua node
    alpha=0.8         # sedikit transparan agar edge di baliknya tetap terlihat
)

# gambar edge
nx.draw_networkx_edges(
    G,
    pos,
    edge_color='gray',  # garis penghubung warna abu-abu
    alpha=0.6           # lebih transparan dari node agar tidak mendominasi visual
)
# CATATAN: pada undirected graph, edge digambar sebagai garis lurus tanpa panah,
# mencerminkan hubungan simetris (tidak ada arah).

# label node
nx.draw_networkx_labels(
    G,
    pos,
    font_size=10,       # ukuran font nama node
    font_color='black'  # warna teks nama node
)

# label degree
# Menampilkan nilai degree di bawah node
degree_labels = {
    node: f"({degree})"          # format: "(5)" untuk degree 5
    for node, degree in degree_map.items()
    # Buat dictionary label tambahan: {nama_node: "(nilai_degree)"}
}

label_pos = {
    k: (v[0], v[1] - 0.04)   # geser posisi y ke bawah 0.04 unit
    for k, v in pos.items()
    # Agar label degree tidak menimpa nama node di atasnya
}

nx.draw_networkx_labels(
    G,
    label_pos,             # posisi label yang sudah digeser ke bawah
    labels=degree_labels,  # dictionary label degree yang akan ditampilkan
    font_color='red',      # merah agar mudah dibedakan dari nama node (hitam)
    font_size=8            # lebih kecil dari nama node
)

plt.title("Visualisasi Degree")
plt.axis('off')  # sembunyikan sumbu x dan y (tidak relevan untuk graf)
plt.show()
plt.close()

# DEGREE CENTRALITY

dc = nx.degree_centrality(G)
# Fungsi inti analisis ini.
# Menghitung Degree Centrality TERNORMALISASI untuk setiap node.
# Formula yang digunakan NetworkX:
#   DC(v) = degree(v) / (N - 1)
#   N = jumlah total node dalam graf
#   N-1 = jumlah maksimum koneksi yang MUNGKIN dimiliki satu node
#         (sebuah node bisa terhubung ke semua node lain kecuali dirinya sendiri)
# Hasil: nilai antara 0 (tidak ada koneksi) dan 1 (terhubung ke semua node lain).
# Normalisasi ini penting agar nilai bisa dibandingkan lintas jaringan
# yang memiliki ukuran (N) berbeda-beda.

print("\n=== DEGREE CENTRALITY ===")

most_influential = sorted(
    dc.items(),                # semua pasangan (node, nilai_DC)
    key=lambda item: item[1],  # urutkan berdasarkan nilai DC
    reverse=True               # descending: DC tertinggi di atas
)
# Hasil pengurutan ini adalah "peringkat pengaruh" semua node dalam jaringan.

for node, centrality in most_influential:
    print(f"Node: {node} -> Degree Centrality: {centrality:.4f}")
    # :.4f = tampilkan 4 angka di belakang koma untuk presisi

# VISUALISASI DEGREE CENTRALITY
# Ukuran node menunjukkan besar centrality

# ukuran node berdasarkan centrality
centrality_sizes = [v * 5000 for v in dc.values()]
# Ukuran node = nilai DC × 5000.
# Nilai DC sudah ternormalisasi [0,1], sehingga faktor pengali 5000 (lebih besar dari 500)
# diperlukan agar perbedaan ukuran antar node tetap terlihat signifikan.
# Node dengan DC = 0.25 → ukuran 1250; DC = 0.05 → ukuran 250.

plt.figure(figsize=(12, 12))

# Menggambar node pada graph
# Ukuran node mengikuti nilai centrality
nx.draw_networkx_nodes(
    G,
    pos,                       # posisi sama dengan visualisasi degree (kamada_kawai)
    node_size=centrality_sizes,  # ukuran berdasarkan DC ternormalisasi
    node_color='orange',         # oranye untuk membedakan secara visual dari skyblue
    alpha=0.8
)

# Menggambar garis penghubung antar node
nx.draw_networkx_edges(
    G,
    pos,
    edge_color='gray',
    alpha=0.6
)

# Menampilkan nama/label tiap node
nx.draw_networkx_labels(
    G,
    pos,
    font_size=10,
    font_color='black'
)

# label centrality
# Menampilkan nilai centrality pada tiap node
centrality_labels = {
    node: f"{centrality:.2f}"  # Format .2f berarti hanya menampilkan 2 angka di belakang koma
    # Contoh: 0.2500 → "0.25"; 0.1500 → "0.15"
    # Lebih ringkas dari 4 desimal agar label tidak terlalu panjang di visualisasi
    for node, centrality in dc.items()
    # Iterasi semua node dan nilai DC-nya dari dictionary dc
}

# Mengatur posisi label centrality sedikit di bawah node
centrality_label_pos = {
    k: (v[0], v[1] - 0.05)   # geser 0.05 unit ke bawah (lebih jauh dari 0.04 sebelumnya)
    for k, v in pos.items()
    # Jarak lebih besar karena node lebih besar (centrality_sizes lebih besar dari node_sizes)
}

# Menampilkan label centrality pada graph
nx.draw_networkx_labels(
    G,
    centrality_label_pos,
    labels=centrality_labels,
    font_color='blue',   # biru untuk membedakan dari nama node (hitam) dan degree (merah)
    font_size=8
)

plt.title("Visualisasi Degree Centrality") # Memberi judul visualisasi
plt.axis('off') # Menghilangkan sumbu koordinat
plt.show() # Menampilkan graph
plt.close() # Menutup plot setelah ditampilkan

# TOP 5 NODE PALING SENTRAL
# Menampilkan 5 node dengan centrality tertinggi

print("\n=== TOP 5 NODE PALING SENTRAL ===")

top_5 = most_influential[:5]
# Ambil 5 elemen pertama dari list most_influential yang sudah terurut descending.
# Ini adalah 5 node dengan Degree Centrality tertinggi = paling berpengaruh.

for i, (node, centrality) in enumerate(top_5, start=1):
    # enumerate dengan start=1 menghasilkan nomor urut 1,2,3,4,5 (bukan 0-indexed)
    print(f"{i}. {node} -> {centrality:.4f}")

# SIMPAN HASIL KE CSV

result_df = pd.DataFrame(
    most_influential,              # data: list of tuples (node, DC)
    columns=['Node', 'Degree Centrality']  # nama kolom di CSV output
)
# Mengubah list hasil analisis menjadi DataFrame pandas
# agar bisa diekspor ke CSV untuk dokumentasi atau analisis lanjutan.

result_df.to_csv(
    "hasil_degree_centrality.csv",  # nama file output
    index=False                      # jangan sertakan kolom index bawaan pandas (0,1,2,...)
)

print("\nHasil berhasil disimpan ke hasil_degree_centrality.csv")