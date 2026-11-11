# Akuisisi Data Akomodasi Kecamatan Kintamani

**Nama:** Ni Putu Riska Pramesti Cahya Dewi  
**NIM:** 2501010315  
**Mata kuliah:** BIFP-243 Akuisisi dan Manajemen Data  
**Program studi:** Informatika – INSTIKI

## Tujuan
Mengakuisisi data akomodasi publik di Kecamatan Kintamani melalui OpenStreetMap (OSM) menggunakan Overpass API, menyimpan respons mentah, mengubahnya menjadi CSV, dan mendokumentasikan provenance serta etika data.

## Sumber data
- OpenStreetMap melalui Overpass API: https://overpass-api.de/api/interpreter
- Publikasi pembanding yang perlu diperiksa: BPS Kabupaten Bangli, *Kecamatan Kintamani Dalam Angka 2025*: https://banglikab.bps.go.id/id/publication/2025/09/26/8bd335021722e75f43dae2ad/kecamatan-kintamani-dalam-angka-2025.html
- Atribusi wajib: **© OpenStreetMap contributors**. Data OSM tersedia di bawah Open Database License (ODbL).

## Tanggal akses
Tanggal akuisisi aktual dicatat otomatis di `docs/provenance.json` dalam UTC saat skrip dijalankan. Jangan mengisi tanggal perkiraan secara manual.

## Metode akuisisi
1. Buka `docs/query_overpass.txt` di https://overpass-turbo.eu/.
2. Pastikan batas `Kintamani` yang dipilih benar-benar Kecamatan Kintamani, bukan Desa Kintamani. Query awal memakai `admin_level=6` sesuai contoh pada instruksi tugas; tingkat administratif wajib diperiksa di peta.
3. Jalankan `python skrip_akuisisi.py` dari root repository.
4. Skrip menyimpan JSON mentah di `data/raw/`, CSV di `data/interim/`, provenance dan pemeriksaan kualitas di `docs/`.
5. Isi hasil verifikasi manual 10 sampel pada `docs/sampel_verifikasi_10.csv`.
6. Lengkapi pembanding BPS pada `docs/perbandingan_bps.csv` berdasarkan tabel dan tahun yang benar-benar ditemukan.

## Cara menjalankan
Pastikan Python 3.10+ tersedia. Instal dependensi:
```bash
pip install requests pandas jupyter matplotlib
```
Kemudian:
```bash
python skrip_akuisisi.py
```
Notebook `notebooks/akuisisi_akomodasi.ipynb` dapat dijalankan dari awal sampai akhir setelah akuisisi berhasil.

## Batasan dan etika
- OSM merupakan data kolaboratif berbasis kontribusi sukarela sehingga tidak boleh dianggap sebagai daftar lengkap seluruh akomodasi.
- Jangan mengirim request berulang-ulang. Jalankan satu atau dua kali sesuai instruksi dosen dan tunggu jika server sibuk.
- Tidak mengambil nomor telepon, email, atau akun media sosial pemilik.
- Tidak menggunakan scraping OTA (Booking.com, Agoda, Traveloka, tiket.com, Airbnb, Tripadvisor) maupun halaman Google Maps.
- File JSON mentah tidak boleh diedit atau ditimpa. Pengolahan dilakukan ke file baru.
- Hasil verifikasi 10 sampel harus dilakukan manual, bukan dianggap selesai hanya karena sampel sudah dipilih.

## Struktur repository
```text
akomodasi_kintamani_2501010315/
├── data/
│   ├── raw/
│   └── interim/
├── notebooks/akuisisi_akomodasi.ipynb
├── docs/
│   ├── query_overpass.txt
│   ├── provenance.json
│   ├── data_dictionary.csv
│   ├── data_ethics_checklist.csv
│   ├── perbandingan_bps.csv
│   ├── hasil_pemeriksaan_kualitas.json
│   └── sampel_verifikasi_10.csv
├── reports/laporan_akomodasi_kintamani.pdf
├── skrip_akuisisi.py
└── README.md
```

**Status sebelum pengumpulan:** jalankan skrip dan notebook, pastikan file JSON/CSV terbentuk, verifikasi 10 sampel, lengkapi angka BPS atau jelaskan jika data tingkat kecamatan tidak tersedia, lalu perbarui laporan PDF.
