"""Soal Praktik 2 — Hierarki custom exception Sistem Informasi Perpustakaan.

Hierarki exception:
    PerpustakaanError (base)
    ├── BukuNotFoundError       : buku tidak ada di katalog
    ├── BukuTidakTersediaError  : buku ada, tetapi stok tersedia habis
    └── AnggotaNotFoundError    : anggota tidak terdaftar

Fungsi pinjam_buku() melempar exception di atas sesuai kondisi, dan
program utama mendemonstrasikan penanganan setiap jenis exception.
"""


class PerpustakaanError(Exception):
    """Base exception untuk seluruh error Sistem Informasi Perpustakaan."""


class BukuNotFoundError(PerpustakaanError):
    """Buku dengan ID yang diminta tidak ada di katalog."""

    def __init__(self, id_buku):
        self.id_buku = id_buku
        super().__init__(f"Buku dengan ID '{id_buku}' tidak ditemukan "
                         f"di katalog")


class BukuTidakTersediaError(PerpustakaanError):
    """Buku ada di katalog, tetapi semua eksemplar sedang dipinjam."""

    def __init__(self, id_buku, judul):
        self.id_buku = id_buku
        self.judul = judul
        super().__init__(f"Buku '{judul}' (ID {id_buku}) sedang habis "
                         f"dipinjam, tidak ada eksemplar tersedia")


class AnggotaNotFoundError(PerpustakaanError):
    """Anggota dengan ID yang diminta tidak terdaftar."""

    def __init__(self, id_anggota):
        self.id_anggota = id_anggota
        super().__init__(f"Anggota dengan ID '{id_anggota}' tidak "
                         f"terdaftar di perpustakaan")


def pinjam_buku(katalog, daftar_anggota, id_anggota, id_buku):
    """Pinjam satu eksemplar buku untuk seorang anggota.

    Mengembalikan pesan sukses. Melempar AnggotaNotFoundError,
    BukuNotFoundError, atau BukuTidakTersediaError jika syarat
    peminjaman tidak terpenuhi.
    """
    if id_anggota not in daftar_anggota:
        raise AnggotaNotFoundError(id_anggota)
    if id_buku not in katalog:
        raise BukuNotFoundError(id_buku)
    buku = katalog[id_buku]
    if buku["tersedia"] <= 0:
        raise BukuTidakTersediaError(id_buku, buku["judul"])
    buku["tersedia"] -= 1
    return (f"SUKSES: {daftar_anggota[id_anggota]} meminjam "
            f"'{buku['judul']}' (sisa tersedia: {buku['tersedia']})")


def coba_pinjam(katalog, daftar_anggota, id_anggota, id_buku):
    """Coba satu skenario peminjaman dan tangani exception-nya."""
    try:
        pesan = pinjam_buku(katalog, daftar_anggota, id_anggota, id_buku)
    except AnggotaNotFoundError as e:
        print(f"[AnggotaNotFoundError] {e}")
    except BukuNotFoundError as e:
        print(f"[BukuNotFoundError] {e}")
    except BukuTidakTersediaError as e:
        print(f"[BukuTidakTersediaError] {e}")
    except PerpustakaanError as e:
        print(f"[PerpustakaanError lain] {e}")
    else:
        print(pesan)


if __name__ == "__main__":
    katalog = {
        "BK001": {"judul": "Pemrograman Python", "tersedia": 2},
        "BK002": {"judul": "Basis Data", "tersedia": 0},
        "BK003": {"judul": "Jaringan Komputer", "tersedia": 1},
    }
    daftar_anggota = {
        "AG001": "Fakhry Ahmad Fauzan",
        "AG002": "Siti Rahmawati",
    }

    print("=== Skenario 1: Peminjaman berhasil ===")
    coba_pinjam(katalog, daftar_anggota, "AG001", "BK001")
    print("\n=== Skenario 2: Buku tidak ditemukan ===")
    coba_pinjam(katalog, daftar_anggota, "AG001", "BK999")
    print("\n=== Skenario 3: Buku tidak tersedia ===")
    coba_pinjam(katalog, daftar_anggota, "AG002", "BK002")
    print("\n=== Skenario 4: Anggota tidak terdaftar ===")
    coba_pinjam(katalog, daftar_anggota, "AG999", "BK003")
