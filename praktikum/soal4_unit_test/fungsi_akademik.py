"""Fungsi akademik yang menjadi objek pengujian pada Soal Praktik 4."""


def hitung_ipk(nilai_list):
    """Hitung IPK dari list dict nilai {'bobot': float, 'sks': int}.

    Mengembalikan 0.0 untuk list kosong atau total SKS nol.
    """
    if not nilai_list:
        return 0.0
    total_bobot = sum(n["bobot"] * n["sks"] for n in nilai_list)
    total_sks = sum(n["sks"] for n in nilai_list)
    if total_sks == 0:
        return 0.0
    return total_bobot / total_sks


def validasi_nim(nim):
    """Validasi format NIM: string 10 digit angka. Mengembalikan bool."""
    return isinstance(nim, str) and len(nim) == 10 and nim.isdigit()


def konversi_nilai_huruf(angka):
    """Konversi nilai angka 0-100 ke nilai huruf.

    Skala: A (85-100), B+ (80-84), B (70-79), C+ (65-69),
    C (60-64), D (50-59), E (0-49).

    Melempar TypeError jika masukan bukan angka, dan ValueError
    jika angka di luar rentang 0-100.
    """
    if isinstance(angka, bool) or not isinstance(angka, (int, float)):
        raise TypeError("Nilai harus berupa angka (int atau float)")
    if angka < 0 or angka > 100:
        raise ValueError(f"Nilai {angka} di luar rentang 0-100")
    if angka >= 85:
        return "A"
    if angka >= 80:
        return "B+"
    if angka >= 70:
        return "B"
    if angka >= 65:
        return "C+"
    if angka >= 60:
        return "C"
    if angka >= 50:
        return "D"
    return "E"
