"""Soal Praktik 4 — Unit test untuk fungsi akademik.

Menguji hitung_ipk(), validasi_nim(), dan konversi_nilai_huruf()
dengan unittest, mencakup happy path, edge case, dan input
tidak valid.

Jalankan: python -m unittest test_fungsi_akademik -v
"""

import unittest

from fungsi_akademik import (hitung_ipk, konversi_nilai_huruf,
                             validasi_nim)


class TestHitungIPK(unittest.TestCase):
    """Test untuk fungsi hitung_ipk()."""

    def setUp(self):
        self.nilai_normal = [
            {"bobot": 4.0, "sks": 3},
            {"bobot": 3.0, "sks": 2},
            {"bobot": 3.7, "sks": 3},
        ]

    def test_hitung_ipk_normal(self):
        # (4.0*3 + 3.0*2 + 3.7*3) / 8 = 29.1 / 8 = 3.6375
        self.assertAlmostEqual(hitung_ipk(self.nilai_normal), 3.6375)

    def test_hitung_ipk_satu_nilai(self):
        self.assertAlmostEqual(hitung_ipk([{"bobot": 3.5, "sks": 3}]), 3.5)

    def test_hitung_ipk_kosong(self):
        # Edge case: list kosong menghasilkan 0.0
        self.assertEqual(hitung_ipk([]), 0.0)

    def test_hitung_ipk_sks_nol(self):
        # Edge case: total SKS nol menghasilkan 0.0
        self.assertEqual(hitung_ipk([{"bobot": 4.0, "sks": 0}]), 0.0)


class TestValidasiNIM(unittest.TestCase):
    """Test untuk fungsi validasi_nim()."""

    def test_nim_benar(self):
        self.assertTrue(validasi_nim("2024132003"))

    def test_nim_mengandung_huruf(self):
        self.assertFalse(validasi_nim("2024AB2003"))

    def test_nim_kurang_digit(self):
        # Edge case: hanya 9 digit
        self.assertFalse(validasi_nim("202413200"))

    def test_nim_lebih_digit(self):
        # Edge case: 11 digit
        self.assertFalse(validasi_nim("20241320030"))

    def test_nim_kosong(self):
        self.assertFalse(validasi_nim(""))

    def test_nim_bukan_string(self):
        # Input tidak valid: tipe data bukan string
        self.assertFalse(validasi_nim(2024132003))


class TestKonversiNilaiHuruf(unittest.TestCase):
    """Test untuk fungsi konversi_nilai_huruf()."""

    def test_nilai_a(self):
        self.assertEqual(konversi_nilai_huruf(90), "A")

    def test_nilai_batas_a(self):
        # Edge case: batas bawah A
        self.assertEqual(konversi_nilai_huruf(85), "A")

    def test_nilai_b_plus(self):
        self.assertEqual(konversi_nilai_huruf(82), "B+")

    def test_nilai_b(self):
        self.assertEqual(konversi_nilai_huruf(72), "B")

    def test_nilai_c_plus(self):
        self.assertEqual(konversi_nilai_huruf(66), "C+")

    def test_nilai_c(self):
        self.assertEqual(konversi_nilai_huruf(60), "C")

    def test_nilai_d(self):
        self.assertEqual(konversi_nilai_huruf(55), "D")

    def test_nilai_e(self):
        self.assertEqual(konversi_nilai_huruf(40), "E")

    def test_nilai_nol(self):
        # Edge case: nilai minimum
        self.assertEqual(konversi_nilai_huruf(0), "E")

    def test_nilai_seratus(self):
        # Edge case: nilai maksimum
        self.assertEqual(konversi_nilai_huruf(100), "A")

    def test_nilai_negatif(self):
        # Input tidak valid: di bawah rentang
        with self.assertRaises(ValueError):
            konversi_nilai_huruf(-5)

    def test_nilai_di_atas_seratus(self):
        # Input tidak valid: di atas rentang
        with self.assertRaises(ValueError):
            konversi_nilai_huruf(101)

    def test_nilai_bukan_angka(self):
        # Input tidak valid: tipe data salah
        with self.assertRaises(TypeError):
            konversi_nilai_huruf("delapan puluh")


if __name__ == "__main__":
    unittest.main()
