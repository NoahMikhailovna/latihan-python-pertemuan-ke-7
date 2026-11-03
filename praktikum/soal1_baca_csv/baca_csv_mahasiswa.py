"""Soal Praktik 1 — Membaca data mahasiswa dari file CSV.

Program membaca file CSV berisi data mahasiswa (nim, nama, ipk) dengan
penanganan exception lengkap:
- FileNotFoundError : file tidak ditemukan
- csv.Error         : format CSV rusak
- ValueError        : nilai IPK tidak dapat dikonversi ke float

Blok else menampilkan ringkasan data jika pembacaan berhasil, dan blok
finally memastikan file selalu ditutup.
"""

import csv


def baca_data_mahasiswa(path):
    """Baca data mahasiswa dari file CSV pada path yang diberikan.

    Baris dengan IPK tidak valid dilewati dan dilaporkan (ValueError
    ditangani per baris). Mengembalikan list dict mahasiswa yang valid.
    """
    file_csv = None
    mahasiswa = []
    try:
        file_csv = open(path, newline="", encoding="utf-8")
        reader = csv.DictReader(file_csv, strict=True)
        for baris in reader:
            try:
                ipk = float(baris["ipk"])
            except ValueError:
                print(f"  [ValueError] Baris dilewati, IPK tidak valid: "
                      f"{baris}")
                continue
            mahasiswa.append({
                "nim": baris["nim"],
                "nama": baris["nama"],
                "ipk": ipk,
            })
    except FileNotFoundError:
        print(f"[FileNotFoundError] File '{path}' tidak ditemukan.")
    except csv.Error as e:
        print(f"[csv.Error] Format CSV rusak pada '{path}': {e}")
    else:
        total_ipk = sum(m["ipk"] for m in mahasiswa)
        rata_rata = total_ipk / len(mahasiswa) if mahasiswa else 0.0
        print(f"Pembacaan '{path}' berhasil (blok else):")
        for m in mahasiswa:
            print(f"  - {m['nim']} | {m['nama']} | IPK {m['ipk']:.2f}")
        print(f"Ringkasan: {len(mahasiswa)} mahasiswa valid, "
              f"rata-rata IPK = {rata_rata:.2f}")
    finally:
        if file_csv is not None:
            file_csv.close()
            print(f"  (finally) File '{path}' ditutup.")
    return mahasiswa


if __name__ == "__main__":
    print("=== Skenario 1: File CSV valid ===")
    baca_data_mahasiswa("data_mahasiswa.csv")
    print()
    print("=== Skenario 2: File tidak ditemukan ===")
    baca_data_mahasiswa("data_tidak_ada.csv")
    print()
    print("=== Skenario 3: Format CSV rusak ===")
    baca_data_mahasiswa("data_rusak.csv")
