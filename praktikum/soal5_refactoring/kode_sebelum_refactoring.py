# Soal Praktik 5 - Kode SEBELUM refactoring.
#
# Program memproses data nilai mahasiswa: validasi NIM, konversi
# nilai ke huruf, penentuan status kelulusan, lalu mencetak laporan.
# Kode ini SENGAJA ditulis dengan 5 code smell:
#   1. Magic number   : angka 85/80/70/65/60/50, 60 (batas lulus),
#                       dan kode status 1/2 ditulis langsung tanpa nama.
#   2. Duplikasi      : validasi NIM ditulis dua kali (di proses_semua
#                       dan di cek_nim_untuk_update); tangga konversi
#                       huruf juga ditulis dua kali.
#   3. Long method    : proses_semua mengerjakan semua hal sekaligus.
#   4. Deep nesting   : if bersarang 4 tingkat di dalam proses_semua.
#   5. Dead code      : fungsi hitung_format_lama tidak pernah dipakai.


def proses_semua(data):
    hasil = []
    for mhs in data:
        # duplikasi validasi NIM (salinan 1)
        if mhs["nim"] is not None:
            if len(mhs["nim"]) == 10:
                if mhs["nim"].isdigit():
                    if 0 <= mhs["nilai"] <= 100:
                        if mhs["nilai"] >= 85:
                            huruf = "A"
                        elif mhs["nilai"] >= 80:
                            huruf = "B+"
                        elif mhs["nilai"] >= 70:
                            huruf = "B"
                        elif mhs["nilai"] >= 65:
                            huruf = "C+"
                        elif mhs["nilai"] >= 60:
                            huruf = "C"
                        elif mhs["nilai"] >= 50:
                            huruf = "D"
                        else:
                            huruf = "E"
                        if mhs["nilai"] >= 60:
                            status = 1
                            status_teks = "LULUS"
                        else:
                            status = 2
                            status_teks = "TIDAK LULUS"
                        hasil.append(
                            f"{mhs['nim']} | {mhs['nama']} | "
                            f"{mhs['nilai']} | {huruf} | {status_teks}"
                        )
                    else:
                        hasil.append(
                            f"{mhs['nim']} | {mhs['nama']} | "
                            f"NILAI DI LUAR RENTANG"
                        )
                else:
                    hasil.append(
                        f"{mhs['nim']} | {mhs['nama']} | NIM TIDAK VALID"
                    )
            else:
                hasil.append(
                    f"{mhs['nim']} | {mhs['nama']} | NIM TIDAK VALID"
                )
        else:
            hasil.append("- | - | NIM TIDAK VALID")
    return hasil


def cek_nim_untuk_update(nim):
    # duplikasi validasi NIM (salinan 2, logika yang sama persis)
    if nim is not None:
        if len(nim) == 10:
            if nim.isdigit():
                return True
    return False


def huruf_saja(nilai):
    # duplikasi tangga konversi huruf (salinan 2)
    if nilai >= 85:
        return "A"
    elif nilai >= 80:
        return "B+"
    elif nilai >= 70:
        return "B"
    elif nilai >= 65:
        return "C+"
    elif nilai >= 60:
        return "C"
    elif nilai >= 50:
        return "D"
    else:
        return "E"


def hitung_format_lama(data):
    # DEAD CODE: fungsi versi lama, tidak pernah dipanggil di mana pun
    total = 0
    for d in data:
        total = total + d["nilai"]
    return total


if __name__ == "__main__":
    data_mahasiswa = [
        {"nim": "2024132001", "nama": "Andi Pratama", "nilai": 88},
        {"nim": "2024132002", "nama": "Budi Santoso", "nilai": 74},
        {"nim": "2024132003", "nama": "Citra Lestari", "nilai": 57},
        {"nim": "20241", "nama": "Dodi Firmansyah", "nilai": 90},
    ]
    print("=== Hasil proses (kode SEBELUM refactoring) ===")
    for baris in proses_semua(data_mahasiswa):
        print(baris)
