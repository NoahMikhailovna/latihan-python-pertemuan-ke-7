"""Soal Praktik 3 — Konfigurasi logging untuk aplikasi Sistem Informasi.

Konfigurasi:
(a) File handler (RotatingFileHandler) mencatat level DEBUG ke atas.
(b) Console handler mencatat level WARNING ke atas.
(c) Formatter menyertakan timestamp, level, nama logger, dan pesan.

Program menulis pesan pada berbagai level, lalu memverifikasi output
pada kedua handler: konsol hanya menampilkan WARNING ke atas,
sedangkan file log memuat semua level termasuk DEBUG dan INFO.
"""

import logging
from logging.handlers import RotatingFileHandler

FILE_LOG = "si_akademik.log"
FORMAT_LOG = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def buat_logger():
    """Buat dan konfigurasi logger 'si_akademik' dengan dua handler."""
    logger = logging.getLogger("si_akademik")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    if logger.handlers:
        return logger

    formatter = logging.Formatter(FORMAT_LOG, datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = RotatingFileHandler(
        FILE_LOG, maxBytes=5 * 1024 * 1024, backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":
    logger = buat_logger()

    print("Menulis pesan log ke semua level...")
    print("(Di konsol di bawah ini hanya WARNING ke atas yang tampil;")
    print(" DEBUG dan INFO hanya masuk ke file log.)")
    logger.debug("Query SQL: SELECT * FROM mahasiswa WHERE nim="
                 "'2024132003'")
    logger.info("User admin berhasil login dari 192.168.1.10")
    logger.warning("Penggunaan memori mencapai 85%")
    logger.error("Gagal mengirim notifikasi email ke dosen@univ.ac.id")
    logger.critical("Koneksi database utama terputus!")

    for handler in logger.handlers:
        handler.flush()
        handler.close()

    print(f"\n=== Verifikasi isi file {FILE_LOG} "
          f"(semua level DEBUG ke atas) ===")
    with open(FILE_LOG, encoding="utf-8") as f:
        print(f.read(), end="")
