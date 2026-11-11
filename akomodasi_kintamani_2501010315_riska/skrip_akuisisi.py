"""
Akuisisi data akomodasi Kecamatan Kintamani dari OpenStreetMap Overpass API.
Jalankan dari root repository:
    python skrip_akuisisi.py

Catatan:
- Query admin_level=6 mengikuti contoh pada instruksi tugas dosen.
- Sebelum akuisisi, periksa batas wilayah pada https://overpass-turbo.eu/.
- File JSON mentah disimpan sekali dan tidak ditimpa.
- Verifikasi 10 sampel dilakukan MANUAL; script hanya memilih sampel acak.
"""
import json
import time
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent
URL = "https://overpass-api.de/api/interpreter"
HEADERS = {
    "User-Agent": "INSTIKI-BIFP243-Praktikum/1.0 (2501010315@instiki.ac.id)"
}
QUERY_PATH = ROOT / "docs" / "query_overpass.txt"
RAW_DIR = ROOT / "data" / "raw"
INTERIM_DIR = ROOT / "data" / "interim"
DOCS_DIR = ROOT / "docs"

KOLOM = [
    "osm_type", "osm_id", "nama", "jenis", "lat", "lon", "desa",
    "bintang", "jumlah_kamar", "website", "url_osm"
]

def ambil_overpass(query, maks_percobaan=4, jeda=5):
    """Mengambil JSON dari Overpass dengan retry eksponensial."""
    for percobaan in range(1, maks_percobaan + 1):
        try:
            response = requests.post(
                URL, data={"data": query}, headers=HEADERS, timeout=120
            )
            if response.status_code == 200:
                return response.json()
            if response.status_code not in (429, 500, 502, 503, 504):
                response.raise_for_status()
            print(f"[percobaan {percobaan}] HTTP {response.status_code}; tunggu {jeda}s")
        except (requests.Timeout, requests.ConnectionError) as exc:
            print(f"[percobaan {percobaan}] {type(exc).__name__}; tunggu {jeda}s")
        if percobaan < maks_percobaan:
            time.sleep(jeda)
            jeda *= 2
    raise RuntimeError("Gagal mengambil data setelah beberapa percobaan. Coba lagi nanti.")

def ratakan(elements):
    """Mengubah elemen Overpass menjadi tabel sesuai struktur tugas."""
    rows = []
    for e in elements:
        tags = e.get("tags", {})
        center = e.get("center", e)
        lat = center.get("lat")
        lon = center.get("lon")
        rows.append({
            "osm_type": e.get("type"),
            "osm_id": e.get("id"),
            "nama": tags.get("name"),
            "jenis": tags.get("tourism"),
            "lat": lat,
            "lon": lon,
            "desa": tags.get("addr:village"),
            # Sengaja teks sesuai instruksi dosen
            "bintang": tags.get("stars"),
            "jumlah_kamar": tags.get("rooms"),
            "website": tags.get("website") or tags.get("contact:website"),
            "url_osm": f"https://www.openstreetmap.org/{e.get('type')}/{e.get('id')}"
        })
    return pd.DataFrame(rows, columns=KOLOM)

def md5_file(path):
    digest = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def main():
    for folder in (RAW_DIR, INTERIM_DIR, DOCS_DIR):
        folder.mkdir(parents=True, exist_ok=True)

    query = QUERY_PATH.read_text(encoding="utf-8")
    data = ambil_overpass(query)
    elements = data.get("elements", [])

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    raw_path = RAW_DIR / f"osm_akomodasi_kintamani_{stamp}.json"
    # mode x mencegah file mentah tertimpa
    with raw_path.open("x", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    df = ratakan(elements)
    csv_path = INTERIM_DIR / "akomodasi_kintamani.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    # Pemeriksaan kualitas dasar; tidak menghapus data secara diam-diam.
    duplicate_count = int(df.duplicated(subset=["osm_type", "osm_id"]).sum())
    missing_name = int(df["nama"].isna().sum())
    missing_coord = int(df[["lat", "lon"]].isna().any(axis=1).sum())
    missing_type = int(df["jenis"].isna().sum())
    out_of_range = int((~df["lat"].between(-9.0, -8.0) | ~df["lon"].between(114.0, 116.0)).fillna(False).sum())

    qa = {
        "total_elemen_json": len(elements),
        "jumlah_baris_csv": len(df),
        "duplikat_osm_type_id": duplicate_count,
        "tanpa_nama": missing_name,
        "tanpa_koordinat": missing_coord,
        "tanpa_jenis": missing_type,
        "koordinat_di_luar_kotak_pemeriksaan_kasar_bali": out_of_range,
        "catatan": "Pemeriksaan kotak koordinat hanya penyaringan kasar, bukan bukti batas Kecamatan Kintamani."
    }
    (DOCS_DIR / "hasil_pemeriksaan_kualitas.json").write_text(
        json.dumps(qa, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Sampel acak untuk diverifikasi MANUAL oleh mahasiswa.
    sample_n = min(10, len(df))
    sample = df.sample(n=sample_n, random_state=42) if sample_n else df.copy()
    sample = sample.copy()
    sample["hasil_verifikasi_nama"] = ""
    sample["hasil_verifikasi_jenis"] = ""
    sample["hasil_verifikasi_lokasi"] = ""
    sample["sumber_verifikasi_url"] = ""
    sample["catatan_verifikasi"] = ""
    sample.to_csv(DOCS_DIR / "sampel_verifikasi_10.csv", index=False, encoding="utf-8-sig")

    provenance = {
        "endpoint_url": URL,
        "query_file": "docs/query_overpass.txt",
        "acquisition_timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total_elements": len(elements),
        "raw_file": str(raw_path.relative_to(ROOT)).replace("\\\\", "/"),
        "raw_file_md5": md5_file(raw_path),
        "licensing": "Open Database License (ODbL) - © OpenStreetMap contributors",
        "collector_name": "Ni Putu Riska Pramesti Cahya Dewi",
        "collector_nim": "2501010315",
        "note": "Periksa batas administratif query pada peta Overpass Turbo sebelum menggunakan hasil."
    }
    (DOCS_DIR / "provenance.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Jumlah elemen JSON: {len(elements)}")
    print(f"CSV tersimpan: {csv_path}")
    print(f"JSON mentah tersimpan: {raw_path}")
    print(f"MD5 JSON mentah: {provenance['raw_file_md5']}")
    print("Pemeriksaan kualitas:", json.dumps(qa, ensure_ascii=False))
    print(f"Sampel manual: {DOCS_DIR / 'sampel_verifikasi_10.csv'}")
    print("Ingat: isi hasil verifikasi 10 sampel secara manual dan lengkapi pembanding BPS.")

if __name__ == "__main__":
    main()
