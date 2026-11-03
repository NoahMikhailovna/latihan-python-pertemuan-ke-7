# Soal Praktik 5 — Identifikasi Code Smell dan Refactoring

Program yang dianalisis memproses data nilai mahasiswa (validasi NIM,
konversi nilai ke huruf, status kelulusan, laporan). File
`kode_sebelum_refactoring.py` mengandung lima code smell; file
`kode_sesudah_refactoring.py` adalah hasil refactoring-nya dengan
perilaku dan output yang **identik**.

| # | Code Smell | Lokasi di Kode Sebelum | Masalah | Refactoring yang Diterapkan |
|---|---|---|---|---|
| 1 | **Magic Number** | Ambang huruf 85/80/70/65/60/50, batas lulus 60, dan kode status 1/2 ditulis langsung di banyak tempat | Pembaca tidak tahu makna angka tersebut; jika batas lulus berubah, semua kemunculan angka 60 harus dicari dan diganti satu per satu, rawan terlewat | **Replace Magic Number with Symbolic Constant** — semua angka bermakna diganti konstanta bernama: `BATAS_LULUS`, `STATUS_LULUS`, `STATUS_TIDAK_LULUS`, `PANJANG_NIM`, dan tabel `SKALA_NILAI` |
| 2 | **Duplicate Code** | Validasi NIM ditulis dua kali (`proses_semua` dan `cek_nim_untuk_update`); tangga konversi huruf ditulis dua kali (`proses_semua` dan `huruf_saja`) | Perubahan aturan validasi/konversi harus dilakukan di dua tempat; satu tempat yang terlewat menimbulkan perilaku tidak konsisten (pelanggaran prinsip DRY) | **Extract Method** — validasi dipusatkan ke satu fungsi `validasi_nim()` dan konversi ke satu fungsi `konversi_huruf()` yang dipakai semua pemanggil |
| 3 | **Long Method** | Fungsi `proses_semua` mengerjakan validasi, konversi, penentuan status, dan pembuatan laporan sekaligus dalam puluhan baris | Sulit dibaca, sulit diuji per bagian, dan sulit dipakai ulang sebagian logikanya | **Extract Method** — dipecah menjadi fungsi-fungsi kecil berfokus tunggal: `validasi_nim()`, `konversi_huruf()`, `tentukan_status()`, dan `proses_mahasiswa()`; `proses_semua()` tinggal memetakan daftar |
| 4 | **Deep Nesting** | `if` bersarang empat tingkat di dalam `proses_semua` (nim tidak None → panjang 10 → isdigit → nilai dalam rentang) | Alur utama tenggelam ke sisi kanan; pembaca harus mengingat tumpukan kondisi untuk memahami satu baris, rawan salah kurung/logika | **Guard Clause** — kondisi tidak valid ditangani di awal fungsi dengan `return` dini, sehingga alur utama berjalan lurus tanpa sarang |
| 5 | **Dead Code** | Fungsi `hitung_format_lama()` tidak pernah dipanggil di mana pun | Membingungkan pembaca (dikira masih dipakai), menambah beban pemeliharaan, dan menyembunyikan fungsi mana yang benar-benar aktif | **Remove Dead Code** — fungsi yang tidak terpakai dihapus (riwayatnya tetap aman di version control) |

Tambahan sesuai tuntutan soal: seluruh fungsi pada kode sesudah
refactoring dilengkapi **docstring** dan **type hints** (parameter dan
nilai balik), serta mengikuti konvensi penamaan **PEP 8**.

## Verifikasi

Kedua file dijalankan dengan data contoh yang sama dan menghasilkan
output yang sama untuk setiap mahasiswa:

- `2024132001 | Andi Pratama | 88 | A | LULUS`
- `2024132002 | Budi Santoso | 74 | B | LULUS`
- `2024132003 | Citra Lestari | 57 | D | TIDAK LULUS`
- `20241 | Dodi Firmansyah | NIM TIDAK VALID`

Ini membuktikan refactoring mengubah *struktur* kode tanpa mengubah
*perilaku* program.
