##### **SOCIAL NETWORK ANALYSIS WITH NETWORKX**

##### **DEGREE CENTRALITY ANALYSIS**

**Sumber : Handoko, W. T., Anwar, S. N., Supriyanto, E., \& Lestariningsih, E. (2026). Penerapan Social Network Analysis dengan Network X untuk Melihat Derajat Sentralitas pada Dataset Jaringan Sosial. Jurnal Informatika dan Teknologi Komputer, 6(1), 14–22. https://doi.org/10.55606/jitek.v6i1.8768**



**Anggota Kelompok :**

* Zahida Amanda Rahma (25031554033)
* Thessalonica Alexandra Dominique Rebecca (25031554084)





###### **A. GRAPH UNDIRECTED (Kode 1)**

Graf tidak berarah adalah representasi jaringan di mana setiap hubungan (edge) bersifat simetris dan mutual jika A terhubung ke B, maka B otomatis terhubung ke A. Tidak ada konsep "pengirim" atau "penerima", tidak ada in-degree maupun out-degree. Hanya ada satu nilai degree per node yang merepresentasikan total jumlah koneksi langsung.



Kode program ini secara tepat menggunakan undirected graph karena sesuai dengan asumsi datanya: hubungan antar selebriti/tokoh politik dianggap setara dan timbal balik. Misalnya jika Bush berkolaborasi dengan Obama, maka Obama pun berkolaborasi dengan Bush, tidak ada hierarki arah. Ini sesuai persis dengan yang dijelaskan dalam artikel jurnal Handoko et al. (2026): graf dimodelkan sebagai graf tidak berarah (undirected graph), mengasumsikan bahwa hubungan antara dua peran aktor bersifat timbal balik atau setara dalam konteks edgelist yang diberikan.



Dalam kasus kode ini, tujuan utamanya adalah menerapkan metode Degree Centrality untuk mengukur tingkat konektivitas dan mengidentifikasi aktor paling populer dalam jaringan sosial. Urgensinya sangat nyata: tanpa analisis kuantitatif seperti ini, kita hanya bisa menebak siapa yang paling berpengaruh. Degree Centrality memberikan angka objektif yang bisa dipertanggungjawabkan secara ilmiah.



###### **B. GRAPH DIRECTED (Kode 2)**

Graf Berarah (Directed Graph / DiGraph) adalah representasi di mana setiap edge punya arah — A→B tidak berarti B→A. Koneksi bersifat asimetris. Contoh nyatanya: Twitter/Instagram follow (kamu bisa follow artis tanpa dia follow balik), sitasi jurnal (paper A mengutip paper B), atau aliran data dalam sebuah sistem. Di NetworkX dibuat dengan nx.DiGraph().



Dengan directed graph, kita bisa membedakan influencer yang dikagumi banyak orang (in-degree tinggi) dari influencer yang aktif berinteraksi dengan banyak pihak (out-degree tinggi). Dua profil pengaruh yang sangat berbeda strateginya dalam konteks marketing atau kolaborasi.



###### **C. ALGORITMA YANG DIGUNAKAN**

**Algoritma 1 — Graph Construction (Pembangunan Graf)**

Ini adalah algoritma paling fundamental: mengubah data tabular (CSV) menjadi struktur data graf yang bisa dianalisis.

Cara kerja: nx.from\_pandas\_edgelist() membaca setiap baris CSV dan membangun adjacency list — struktur data dictionary di mana setiap key adalah nama node dan value-nya adalah himpunan (set) node yang terhubung langsung. Proses ini berjalan dengan kompleksitas O(V + E) di mana V = jumlah node dan E = jumlah edge.

Perbedaan antar kode:

* Kode 1 (undirected): menggunakan nx.Graph()
* Kode 2 (directed): menggunakan nx.DiGraph()



**Algoritma 2 — Graph Layout (Penempatan Posisi Node)**

Kedua kode menggunakan dua algoritma layout berbeda untuk dua tujuan berbeda.

* Spring Layout (Fruchterman-Reingold) -> Dipakai di Visualisasi 1 pada kedua kode. Prinsipnya meniru fisika pegas: node yang terhubung saling menarik seperti pegas, sedangkan semua node yang tidak terhubung langsung saling mendorong seperti muatan listrik sejenis. Simulasi dijalankan berulang (iterations=50) hingga sistem mencapai keseimbangan energi minimum. Parameter k=1.5 pada Kode 2 mengatur jarak ideal antar node — makin besar nilainya, makin renggang susunan node. Parameter seed=42 memastikan posisi node tidak berubah setiap kali kode dijalankan.
* Kamada-Kawai Layout —> Dipakai untuk Visualisasi 2 dan 3 pada kedua kode. Pendekatannya lebih canggih: algoritma ini menghitung shortest path (jarak terpendek) antar semua pasang node dalam graf, lalu memposisikan node di kanvas sehingga jarak antar node di layar (dalam piksel) seproposional mungkin dengan jarak terpendeknya di dalam graf. Hasilnya secara intuitif: node yang dekat secara struktural (terhubung dalam sedikit langkah) akan terlihat berdekatan secara visual. Jadi algoritma ini lebih lambat tapi menghasilkan layout yang jauh lebih rapi dan informatif.



**Algoritma 3 — Degree Calculation**

* Kode 1 menggunakan nx.degree(G) yang mengembalikan satu nilai per node. Jumlah total edge yang menyentuh node tersebut, tanpa membedakan arah. Ini langsung tersimpan dalam dictionary degree\_map.
* Kode 2 menggunakan tiga fungsi terpisah: G.in\_degree() menghitung edge yang masuk, G.out\_degree() menghitung edge yang keluar, lalu keduanya dijumlahkan secara manual dengan dictionary comprehension untuk mendapat total\_degree\_map. Pemisahan ini penting karena in-degree tinggi bermakna "banyak orang merujuk ke entitas ini" (popularitas/prestise), sedangkan out-degree tinggi bermakna "entitas ini aktif merujuk ke banyak pihak" (keaktifan). Kedua dimensi itu memberikan informasi yang sama sekali berbeda.



**Algoritma 4 — Degree Centrality**

* Kode 1 menggunakan nx.degree\_centrality(G) yang secara internal menghitung degree(v) / (N-1).
* Kode 2 menghitung tiga varian centrality: nx.in\_degree\_centrality(G) untuk in\_degree(v)/(N-1), nx.out\_degree\_centrality(G) untuk out\_degree(v)/(N-1), dan kemudian combined\_dc yang merupakan rata-rata aritmetika keduanya: (in\_dc + out\_dc) / 2. Combined DC ini adalah metrik yang lebih seimbang karena menghargai baik node yang banyak dirujuk maupun node yang aktif merujuk.



**Algoritma 5 — Sorting (Pengurutan / Peringkat)**

Kedua kode menggunakan fungsi sorted() bawaan Python. Dalam konteks kedua kode ini, sorted() dipanggil dengan key=lambda item: item\[1] yang berarti pengurutan dilakukan berdasarkan nilai centrality (elemen kedua dari setiap tuple), dan reverse=True untuk urutan descending (terbesar di atas). Hasilnya adalah most\_influential, daftar node dari yang paling sentral hingga paling pinggiran, yang kemudian digunakan untuk menampilkan Top-5 dan menyimpan ke CSV.



###### **D. POIN PENTING**

"Sentral" ≠ "Paling Banyak Diikuti"

Anggapan bahwa paling banyak diikuti = paling sentral hanya valid dalam satu definisi sempit dari kata "sentral", yaitu popularitas atau prestise. Tetapi konsep sentralitas dalam Social Network Analysis jauh lebih luas dari itu. Sentral dalam konteks SNA berarti: seberapa strategis posisi sebuah node di dalam struktur jaringan secara keseluruhan. Sebuah node yang hanya menerima koneksi tapi tidak pernah mengirim koneksi keluar adalah node yang pasif dia bisa sangat terkenal, tapi tidak berpartisipasi dalam arus informasi. Dalam jaringan yang dinamis, node seperti ini ibarat selebritis yang hanya ditonton tapi tidak pernah berinteraksi balik. Dia populer, tapi bukan pusat jaringan.



Selain data selebriti, kode ini sangat relevan untuk:

Bidang akademik — menganalisis jaringan sitasi ilmiah untuk menemukan paper atau peneliti paling berpengaruh.

Bidang teknologi — memetakan hyperlink antar halaman web (fondasi algoritma PageRank Google).

Bidang keuangan — mendeteksi aliran transaksi mencurigakan atau pola money laundering dalam jaringan transfer uang.

Bidang epidemiologi — memodelkan penyebaran penyakit (siapa menginfeksi siapa).

Bidang organisasi — memetakan alur komunikasi internal perusahaan untuk menemukan "bottleneck" informasi.

Bidang logistik — menganalisis jaringan distribusi barang.





