"""Soal Praktik 5 — Kode SESUDAH refactoring.

Hasil refactoring dari kode_sebelum_refactoring.py. Perilaku program
sama persis (output identik), tetapi lima code smell sudah
dihilangkan:

1. Magic number  -> diganti konstanta bernama (BATAS_LULUS, SKALA_NILAI,
                    STATUS_LULUS, STATUS_TIDAK_LULUS, PANJANG_NIM).
2. Duplikasi     -> validasi NIM dan konversi huruf dipusatkan menjadi
                    satu fungsi validasi_nim() dan konversi_huruf().
3. Long method   -> proses_semua() dipecah menjadi fungsi-fungsi kecil
                    (Extract Method): validasi_nim, konversi_huruf,
                    tentukan_status, proses_mahasiswa.
4. Deep nesting  -> diganti guard clause: kondisi tidak valid ditangani
                    di awal fungsi dengan return dini.
5. Dead code     -> fungsi hitung_format_lama() yang tidak terpakai
                    dihapus.

Seluruh fungsi dilengkapi docstring dan type hints sesuai PEP 8.
"""

from typing import Optional

PANJANG_NIM = 10
BATAS_LULUS = 60
STATUS_LULUS = 1
STATUS_TIDAK_LULUS = 2
NILAI_MINIMUM = 0
NILAI_MAKSIMUM = 100

# Tangga konversi nilai: (batas bawah, huruf), diurutkan dari tertinggi.
SKALA_NILAI = [(85, "A"), (80, "B+"), (70, "B"), (65, "C+"),
               (60, "C"), (50, "D")]


def validasi_nim(nim: Optional[str]) -> bool:
    """Periksa apakah NIM berupa string 10 digit angka."""
    return nim is not None and len(nim) == PANJANG_NIM and nim.isdigit()


def konversi_huruf(nilai: float) -> str:
    """Konversi nilai angka ke huruf berdasarkan SKALA_NILAI."""
    for batas_bawah, huruf in SKALA_NILAI:
        if nilai >= batas_bawah:
            return huruf
    return "E"


def tentukan_status(nilai: float) -> tuple[int, str]:
    """Tentukan (kode status, teks status) kelulusan dari nilai."""
    if nilai >= BATAS_LULUS:
        return STATUS_LULUS, "LULUS"
    return STATUS_TIDAK_LULUS, "TIDAK LULUS"


def proses_mahasiswa(mhs: dict) -> str:
    """Proses satu data mahasiswa menjadi satu baris laporan.

    Kondisi tidak valid ditangani dengan guard clause (return dini),
    sehingga alur utama tidak bersarang.
    """
    if not validasi_nim(mhs["nim"]):
        return f"{mhs['nim']} | {mhs['nama']} | NIM TIDAK VALID"
    if not NILAI_MINIMUM <= mhs["nilai"] <= NILAI_MAKSIMUM:
        return f"{mhs['nim']} | {mhs['nama']} | NILAI DI LUAR RENTANG"
    huruf = konversi_huruf(mhs["nilai"])
    _, status_teks = tentukan_status(mhs["nilai"])
    return (f"{mhs['nim']} | {mhs['nama']} | {mhs['nilai']} | "
            f"{huruf} | {status_teks}")


def proses_semua(data: list[dict]) -> list[str]:
    """Proses seluruh data mahasiswa menjadi daftar baris laporan."""
    return [proses_mahasiswa(mhs) for mhs in data]


if __name__ == "__main__":
    data_mahasiswa = [
        {"nim": "2024132001", "nama": "Andi Pratama", "nilai": 88},
        {"nim": "2024132002", "nama": "Budi Santoso", "nilai": 74},
        {"nim": "2024132003", "nama": "Citra Lestari", "nilai": 57},
        {"nim": "20241", "nama": "Dodi Firmansyah", "nilai": 90},
    ]
    print("=== Hasil proses (kode SESUDAH refactoring) ===")
    for baris in proses_semua(data_mahasiswa):
        print(baris)
