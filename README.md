# Latihan Python — Pertemuan ke-7

Tugas Pemrograman Modern Python **Pertemuan 7: Exception Handling,
Debugging, Logging, Unit Testing, Clean Code, dan Code Review**
(Program Studi Sistem Informasi).

**Nama:** Fakhry Ahmad Fauzan
**NPM:** 20241320038

## Isi Repository

```
├── teori/
│   └── Jawaban_Teori.md            # Jawaban tertulis 10 soal teori
├── praktikum/
│   ├── soal1_baca_csv/             # Baca CSV + exception handling
│   ├── soal2_perpustakaan/         # Hierarki custom exception
│   ├── soal3_logging/              # Konfigurasi logging SI
│   ├── soal4_unit_test/            # Unit test unittest
│   ├── soal5_refactoring/          # Identifikasi code smell + refactoring
│   └── soal6_precommit/            # Konfigurasi pre-commit hooks + demo
└── screenshot_hasil_praktikum/     # Screenshot output setiap soal praktik
```

## Ringkasan Soal Praktik

| Soal | Topik | Cara Menjalankan |
|---|---|---|
| 1 | Membaca data mahasiswa dari CSV dengan penanganan `FileNotFoundError`, `csv.Error`, `ValueError`, blok `else` dan `finally` | `cd praktikum/soal1_baca_csv && python3 baca_csv_mahasiswa.py` |
| 2 | Hierarki custom exception Sistem Informasi Perpustakaan (`PerpustakaanError`, `BukuNotFoundError`, `BukuTidakTersediaError`, `AnggotaNotFoundError`) + fungsi `pinjam_buku()` | `cd praktikum/soal2_perpustakaan && python3 perpustakaan.py` |
| 3 | Logging dengan `RotatingFileHandler` (DEBUG ke atas) dan console handler (WARNING ke atas) | `cd praktikum/soal3_logging && python3 logging_si.py` |
| 4 | Unit test `unittest` untuk `hitung_ipk()`, `validasi_nim()`, `konversi_nilai_huruf()` — 23 test, semua lolos | `cd praktikum/soal4_unit_test && python3 -m unittest test_fungsi_akademik -v` |
| 5 | Identifikasi 5 code smell (magic number, duplikasi, long method, deep nesting, dead code) dan refactoring-nya (lihat `PENJELASAN_REFACTORING.md`) | `cd praktikum/soal5_refactoring && python3 kode_sesudah_refactoring.py` |
| 6 | Konfigurasi pre-commit hooks (black, flake8, isort) dan demonstrasinya (lihat `DEMO.md`) | `pre-commit run --all-files` di folder `praktikum/soal6_precommit` |

## Catatan Screenshot

Screenshot hasil praktik tampil di folder `screenshot_hasil_praktikum`
dalam format SVG agar dapat dirender langsung di GitHub. Versi PNG
dengan isi yang sama tersedia pada bundle ZIP yang dibagikan bersama
repository ini.
