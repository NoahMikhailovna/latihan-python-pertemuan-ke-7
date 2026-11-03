# Jawaban Teori — Pertemuan 7
## Exception Handling, Debugging, Logging, Unit Testing, Clean Code, dan Code Review

**Nama:** Fakhry Ahmad Fauzan
**NPM:** 20241320038
**Mata Kuliah:** Pemrograman Modern Python — Program Studi Sistem Informasi

---

### 1. Perbedaan Syntax Error dan Exception

**Syntax error** adalah kesalahan yang terdeteksi oleh parser Python *sebelum* program dijalankan. Kode yang mengandung syntax error tidak dapat dieksekusi sama sekali karena melanggar aturan tata bahasa (grammar) Python. Kesalahan ini harus diperbaiki terlebih dahulu agar program bisa berjalan.

Contoh syntax error:
- Kurung tutup yang hilang: `print("Halo"` → `SyntaxError: '(' was never closed`
- Indentasi yang salah: blok `if` tanpa indentasi pada baris berikutnya → `IndentationError: expected an indented block`

**Exception** adalah kesalahan yang terjadi *saat program berjalan* (runtime), meskipun sintaks kode sudah benar. Python membuat objek exception dan mencari handler yang sesuai; jika tidak ada handler, program berhenti dan menampilkan traceback. Exception dapat ditangani dengan blok `try-except` agar program tetap berjalan.

Contoh exception:
- `hasil = 10 / 0` → `ZeroDivisionError: division by zero`
- `nilai = int("abc")` → `ValueError: invalid literal for int() with base 10: 'abc'`

Singkatnya: syntax error terjadi pada tahap parsing (program tidak bisa mulai), sedangkan exception terjadi pada tahap eksekusi (program sudah berjalan, lalu menemui kondisi yang tidak diharapkan).

---

### 2. Perbedaan Blok else dan Blok finally

Keduanya adalah bagian opsional dari struktur `try-except-else-finally`, tetapi waktu dan syarat jalannya berbeda:

- **Blok else** dijalankan *hanya jika tidak ada exception* yang terjadi di dalam blok `try`. Blok ini cocok untuk kode lanjutan yang hanya boleh berjalan apabila operasi di `try` berhasil, misalnya menampilkan ringkasan data setelah file berhasil dibaca seluruhnya. Jika terjadi exception (dan ditangani oleh `except`), blok `else` dilewati.
- **Blok finally** dijalankan *selalu*, baik ada exception maupun tidak, baik exception ditangani maupun merambat ke luar. Blok ini ideal untuk pembersihan sumber daya (resource cleanup), seperti menutup file, menutup koneksi database, atau melepaskan lock, agar sumber daya tidak bocor (resource leak).

Urutan alur eksekusi: `try` → (jika sukses) `else` → `finally`; atau `try` → (jika error) `except` → `finally`.

---

### 3. Mengapa Urutan Blok except Penting

Exception dalam Python membentuk hierarki pewarisan: misalnya `ZeroDivisionError` adalah subclass dari `ArithmeticError`, dan `ArithmeticError` adalah subclass dari `Exception`. Python memeriksa blok `except` dari atas ke bawah dan menggunakan blok *pertama* yang cocok dengan tipe exception (termasuk superclass-nya).

Jika exception yang lebih umum ditulis sebelum yang lebih spesifik, misalnya:

```python
try:
    hasil = 10 / 0
except Exception:
    print("Error umum")
except ZeroDivisionError:
    print("Pembagian dengan nol")
```

maka blok `except Exception` akan selalu menangkap `ZeroDivisionError` terlebih dahulu, sehingga blok `except ZeroDivisionError` tidak akan pernah tercapai (unreachable code) dan penanganan spesifik tidak pernah berjalan. Akibatnya, pesan dan logika pemulihan yang seharusnya khusus untuk pembagian-nol hilang, dan bug menjadi lebih sulit dilacak.

Aturannya: **tangani exception yang paling spesifik terlebih dahulu, baru kemudian exception yang lebih umum** sebagai penangkap terakhir (fallback).

---

### 4. Keuntungan Hierarki Custom Exception

Menggunakan exception bawaan secara langsung (misalnya melempar `ValueError` untuk semua jenis kesalahan) membuat penanganan error menjadi kabur: pemanggil tidak bisa membedakan apakah kesalahan berasal dari format data, aturan bisnis, atau kegagalan teknis, dan pesan error tidak membawa konteks domain.

Keuntungan membuat hierarki custom exception:
1. **Semantik domain yang jelas** — nama exception langsung menjelaskan kondisi bisnis yang gagal, misalnya `NIMDuplikatError` lebih bermakna daripada `ValueError`.
2. **Penanganan berjenjang** — handler dapat menangkap exception spesifik untuk pemulihan khusus, atau menangkap superclass-nya untuk penanganan umum, mengikuti tingkat abstraksi setiap lapisan aplikasi.
3. **Informasi diagnostik yang kaya** — custom exception dapat membawa atribut tambahan (NIM yang bermasalah, kode error, saran perbaikan), bukan hanya string pesan.
4. **Stabilitas arsitektur** — hierarki yang mencerminkan domain bisnis tidak berubah ketika implementasi teknis (database, library) berganti.

Contoh dalam konteks Sistem Informasi Akademik:

```python
class SIAkademikError(Exception):
    """Base exception untuk seluruh error SI Akademik."""

class MahasiswaError(SIAkademikError):
    """Error terkait data mahasiswa."""

class NIMFormatError(MahasiswaError):
    """Format NIM tidak sesuai."""
    def __init__(self, nim):
        self.nim = nim
        super().__init__(f"NIM '{nim}' tidak sesuai format")

class NIMDuplikatError(MahasiswaError):
    """NIM sudah terdaftar."""
```

Dengan hierarki ini, lapisan bisnis dapat menangani `NIMFormatError` dan `NIMDuplikatError` secara terpisah, sementara lapisan presentasi cukup menangkap `MahasiswaError` atau `SIAkademikError` untuk menampilkan pesan umum kepada pengguna.

---

### 5. Debugging dengan Print Statement vs pdb

**Print statement** adalah teknik menambahkan `print()` pada titik-titik kritis kode untuk memeriksa nilai variabel dan alur eksekusi.

- Kelebihan: sangat cepat dan sederhana, tidak butuh alat tambahan, cocok untuk bug sederhana dan pemeriksaan sesaat.
- Kekurangan: harus mengubah kode setiap kali titik pemeriksaan berubah, output bercampur dengan output program, dan lupa menghapus print debug dapat mengotori kode produksi.

**pdb (Python Debugger)** adalah debugger interaktif bawaan Python. Eksekusi dapat dihentikan pada breakpoint (`breakpoint()` atau `pdb.set_trace()`), lalu programmer dapat memeriksa variabel (`p`), melangkah baris demi baris (`n`, `s`), melihat call stack (`w`), dan melanjutkan eksekusi (`c`) secara interaktif tanpa mengubah logika kode.

- Kelebihan: inspeksi state program secara langsung dan menyeluruh, tidak perlu menebak titik print, efektif untuk bug kompleks yang alurnya sulit diprediksi.
- Kekurangan: lebih lambat untuk masalah sepele, ada kurva belajar perintah, dan tidak boleh dibiarkan di kode produksi karena menghentikan eksekusi aplikasi.

Situasi yang tepat:
- **Print** tepat untuk bug sederhana, skrip kecil, atau pengecekan cepat satu-dua variabel yang lokasinya sudah diketahui.
- **pdb** tepat untuk bug kompleks: nilai variabel berubah di tengah loop panjang, bug hanya muncul pada kondisi data tertentu, atau akar masalah belum diketahui sehingga perlu penelusuran langkah demi langkah.

---

### 6. Lima Level Logging Standar Python

Modul `logging` menyediakan lima level keparahan. Hanya pesan dengan level sama atau lebih tinggi dari threshold logger/handler yang akan direkam.

| Level | Nilai | Kapan Digunakan | Contoh dalam Sistem Informasi |
|---|---|---|---|
| DEBUG | 10 | Informasi diagnostik detail untuk pengembangan | `logger.debug("Query SQL: SELECT * FROM mahasiswa WHERE nim='2024132003'")` |
| INFO | 20 | Konfirmasi bahwa operasi berjalan normal | `logger.info("User admin berhasil login dari 192.168.1.10")` |
| WARNING | 30 | Indikasi kondisi yang berpotensi menjadi masalah, tetapi aplikasi masih berjalan | `logger.warning("Penggunaan memori mencapai 85%")` |
| ERROR | 40 | Terjadi kesalahan sehingga suatu operasi gagal, tetapi aplikasi secara keseluruhan masih berjalan | `logger.error("Gagal mengirim notifikasi email ke dosen@univ.ac.id")` |
| CRITICAL | 50 | Kesalahan fatal yang mengancam kelangsungan sistem | `logger.critical("Koneksi database utama terputus!")` |

---

### 7. Perbedaan setUp dan setUpClass pada unittest

- **`setUp`** adalah method instance yang dijalankan *sebelum setiap* test method. Digunakan untuk menyiapkan kondisi awal yang bersih dan terisolasi bagi setiap test, misalnya mengosongkan tabel test lalu menyisipkan satu baris data contoh. Karena dijalankan berulang kali (sebanyak jumlah test), isinya sebaiknya ringan.
- **`setUpClass`** adalah classmethod (didekorasi `@classmethod`) yang dijalankan *satu kali* sebelum test pertama dalam kelas tersebut. Digunakan untuk persiapan mahal yang dapat dipakai bersama oleh semua test, misalnya membuat koneksi database, membuat tabel, atau memuat file konfigurasi. Pasangannya adalah `tearDownClass` yang dijalankan satu kali setelah test terakhir, misalnya menutup koneksi dan menghapus file database test.

Aturan praktisnya: persiapan yang mahal dan tidak berubah antar-test masuk `setUpClass`; data yang harus segar dan terisolasi untuk tiap test masuk `setUp`.

---

### 8. Prinsip DRY (Don't Repeat Yourself)

Prinsip DRY menyatakan bahwa setiap pengetahuan (logika, aturan, konstanta) dalam sistem harus memiliki satu representasi tunggal yang otoritatif. Duplikasi kode berbahaya karena ketika aturan berubah, semua salinannya harus diubah; satu salinan yang terlewat akan menimbulkan bug dan perilaku yang tidak konsisten.

Contoh pelanggaran DRY — logika validasi NIM ditulis ulang di dua fungsi:

```python
def proses_pendaftaran(data):
    if not data['nim'].isdigit() or len(data['nim']) != 10:
        raise ValueError("NIM tidak valid")
    # ... proses pendaftaran

def update_mahasiswa(data):
    if not data['nim'].isdigit() or len(data['nim']) != 10:
        raise ValueError("NIM tidak valid")  # DUPLIKASI!
    # ... proses update
```

Refactoring yang tepat — ekstrak validasi menjadi satu fungsi (Extract Method) yang dipakai bersama:

```python
def validasi_nim(nim):
    if not nim.isdigit() or len(nim) != 10:
        raise ValueError(f"NIM '{nim}' tidak valid")

def proses_pendaftaran(data):
    validasi_nim(data['nim'])
    # ... proses pendaftaran

def update_mahasiswa(data):
    validasi_nim(data['nim'])
    # ... proses update
```

Sekarang, jika aturan format NIM berubah (misalnya menjadi 12 digit), perubahan cukup dilakukan di satu tempat.

---

### 9. Empat Code Smell Umum dan Teknik Refactoring-nya

| Code Smell | Gejala | Teknik Refactoring |
|---|---|---|
| **Long Method** | Satu fungsi sangat panjang (> 20–30 baris) dan mengerjakan banyak hal sekaligus, sulit dibaca dan diuji | **Extract Method** — pecah fungsi menjadi beberapa fungsi kecil yang namanya menjelaskan maksud setiap tahap |
| **Duplicate Code** | Blok kode yang sama/serupa muncul di beberapa tempat | **Extract Method / Extract Class** — pusatkan logika menjadi satu fungsi atau kelas bersama (sejalan dengan prinsip DRY) |
| **Magic Number** | Angka literal tanpa penjelasan makna, misalnya `if status == 3:` | **Replace Magic Number with Symbolic Constant** — ganti dengan konstanta bernama jelas, misalnya `STATUS_LULUS = 3` |
| **Deep Nesting** | `if` bersarang lebih dari 3 tingkat sehingga alur utama tenggelam di sisi kanan kode | **Guard Clause** — tangani kondisi gagal/keluar di awal fungsi dengan `return` dini, sehingga alur utama tidak bersarang; dapat dikombinasikan dengan Extract Method |

(Code smell lain yang juga umum: **Dead Code** — kode yang tidak pernah dijalankan; diatasi dengan menghapusnya (Remove Dead Code). **God Class** — satu kelas menanggung terlalu banyak tanggung jawab; diatasi dengan Extract Class.)

---

### 10. Peran Static Analysis Tools dalam Code Review

Static analysis tools memeriksa kode *tanpa menjalankannya* untuk mendeteksi potensi bug, pelanggaran style, dan masalah kualitas secara otomatis:

- **pylint** — linting komprehensif: memeriksa error, pelanggaran konvensi PEP 8, code smell, dan memberi skor kualitas kode.
- **flake8** — memeriksa kepatuhan PEP 8, error sintaks/logika sederhana (misalnya variabel tidak terpakai), dan kompleksitas fungsi.
- **black** — auto-formatter yang memformat ulang kode ke satu gaya yang konsisten dan tidak dapat ditawar, sehingga perdebatan soal format hilang.
- **mypy** — type checker yang memverifikasi konsistensi type hints dan menangkap kesalahan tipe sebelum runtime.

Perannya dalam code review: alat-alat ini menangani pemeriksaan mekanis (format, style, kesalahan dangkal) secara otomatis dan objektif, sehingga reviewer manusia dapat fokus pada aspek yang memerlukan pertimbangan manusia — kebenaran logika bisnis, arsitektur, keamanan, dan keterbacaan solusi.

Integrasi ke CI/CD pipeline meningkatkan efektivitas review karena:
1. Setiap pull request otomatis diperiksa; kode yang tidak lolos lint/type check langsung gagal di pipeline *sebelum* dibebani ke reviewer.
2. Standar ditegakkan secara konsisten pada semua kontributor dan semua waktu, tidak bergantung pada ketelitian individu.
3. Masalah terdeteksi sedini mungkin (shift-left), saat biaya perbaikannya paling murah.
4. Dengan pre-commit hook, pemeriksaan yang sama berjalan di mesin pengembang sebelum commit, melengkapi gerbang di CI.
