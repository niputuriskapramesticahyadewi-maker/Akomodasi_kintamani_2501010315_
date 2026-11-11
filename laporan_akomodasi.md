# Laporan Akuisisi Data Akomodasi Kecamatan Kintamani

- **Nama Penyusun:** Ni Putu Riska Pramesti Cahya Dewi  
- **NIM:** 2501010315  
- **Mata Kuliah:** BIFP-243 (INSTIKI)  

---

## 1. Pendahuluan & Latar Belakang
Proyek ini bertujuan untuk melakukan ekstraksi dan analisis data spasial fasilitas akomodasi pariwisata di wilayah Kecamatan Kintamani, Kabupaten Bangli, Bali. Kintamani merupakan kawasan strategis pariwisata berbasis alam dan budaya yang memerlukan pendataan geospasial akurat guna mendukung perencanaan tata ruang pariwisata yang berkelanjutan.

## 2. Metodologi Pengumpulan Data
* **Sumber Data:** OpenStreetMap (OSM) melalui Overpass API.
* **Endpoint URL:** `https://overpass-api.de/api/interpreter`
* **Kriteria Filter Objek:** 
  * Batas Wilayah: Kecamatan Kintamani (`admin_level=6`, `boundary=administrative`)
  * Kategori Pariwisata (`tourism`): Hotel, *guest house*, *hostel*, *motel*, *apartment*, dan *chalet*.
* **Identitas Pengguna / User-Agent:** `INSTIKI-BIFP243-Praktikum/1.0 (2501010315@instiki.ac.id)`

## 3. Hasil Akuisisi & Struktur Data
Proses ekstraksi berhasil menjaring sejumlah elemen fasilitas akomodasi dengan rincian:
* **Format Mentah (*Raw*):** Disimpan dalam format JSON (`data/raw/`) berisikan struktur lengkap respons API.
* **Format Interim (*Tabular*):** Disimpan dalam format CSV (`data/interim/akomodasi_kintamani.csv`) yang memuat kolom: `osm_type`, `osm_id`, `nama`, `jenis`, `lat`, `lon`, `desa`, `bintang`, `jumlah_kamar`, `website`, dan `url_osm`.

## 4. Validasi & Perbandingan dengan Data BPS
* **Jumlah Akomodasi OSM:** 32 titik fasilitas terpetakan secara aktif oleh kontributor komunitas.
* **Data Statistik BPS Kabupaten Bangli:** Tercatat sekitar 35 akomodasi dalam cakupan kecamatan.
* **Analisis Kesenjangan:** Terdapat sedikit selisih karena OpenStreetMap bergantung pada kontribusi berbasis komunitas (*crowdsourced*) secara *real-time*, sedangkan BPS menggunakan metode pendataan sensus resmi berkala.

## 5. Aspek Etika Data
* **Lisensi:** Data bersumber dari OpenStreetMap di bawah lisensi *Open Database License* (ODbL) © kontributor OSM.
* **Privasi:** Data yang dikumpulkan terbatas pada fasilitas publik komersial (akomodasi niaga), tidak melibatkan data pribadi individu.


