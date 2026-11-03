# Soal Praktik 6 — Demonstrasi Pre-commit Hooks

File `.pre-commit-config.yaml` di folder ini memasang tiga hooks yang
berjalan **otomatis sebelum setiap commit**:

| Hook | Fungsi |
|---|---|
| black | Auto-format kode ke satu gaya yang konsisten |
| flake8 | Linting: pelanggaran PEP 8, variabel tidak terpakai, dll. |
| isort | Mengurutkan dan mengelompokkan import (dengan `--profile black`) |

## Cara Mengaktifkan (satu kali per repo)

```bash
pip install pre-commit
pre-commit install
```

Setelah itu setiap `git commit` akan menjalankan hooks terlebih
dahulu. Jika ada hook yang gagal, **commit dibatalkan** sampai kode
diperbaiki — inilah cara hooks mencegah kode di bawah standar masuk
ke repository.

## Demonstrasi

Sebagai bahan uji digunakan file `contoh_kode_buruk.py` yang sengaja
ditulis tidak rapi (spasi berantakan, import tidak urut, ada variabel
yang tidak terpakai):

```python
import sys
import os
import json


data = '{"nama": "Fakhry", "nilai": 88}'
mahasiswa=json.loads(data)


def tampil( m ):
    x = 5
    print( 'Nama:',m["nama"] )
    print( "Nilai:", m['nilai'] )


tampil(mahasiswa)
print(sys.version_info.major, os.name)
```

### Percobaan 1 — hooks menolak kode yang buruk

```text
$ pre-commit run --all-files
black....................................................................Failed
- hook id: black
- files were modified by this hook

reformatted contoh_kode_buruk.py
1 file reformatted.

flake8...................................................................Failed
- hook id: flake8
- exit code: 1

contoh_kode_buruk.py:11:5: F841 local variable 'x' is assigned to but never used

isort....................................................................Failed
- hook id: isort
- files were modified by this hook

Fixing contoh_kode_buruk.py
```

Hasil: exit code 1 — commit **ditolak**. black sudah otomatis
merapikan format (spasi, tanda kutip) dan isort mengurutkan import
menjadi `json`, `os`, `sys`. Satu-satunya masalah yang tidak bisa
diperbaiki otomatis adalah temuan flake8: variabel `x` tidak terpakai
(F841), yang harus dihapus manual oleh programmer.

Isi file setelah diperbaiki otomatis oleh black + isort dan manual
untuk F841 (keadaan akhir file ini di repository):

```python
import json
import os
import sys

data = '{"nama": "Fakhry", "nilai": 88}'
mahasiswa = json.loads(data)


def tampil(m):
    print("Nama:", m["nama"])
    print("Nilai:", m["nilai"])


tampil(mahasiswa)
print(sys.version_info.major, os.name)
```

### Percobaan 2 — setelah perbaikan, semua hooks lolos

```text
$ pre-commit run --all-files
black....................................................................Passed
flake8...................................................................Passed
isort...................................................................Passed
```

Hasil: exit code 0 — commit diizinkan. Terbukti hooks bekerja sebagai
gerbang kualitas: kode yang belum terformat, import yang tidak urut,
dan kode bermasalah (variabel tidak terpakai) tidak dapat masuk ke
repository.
