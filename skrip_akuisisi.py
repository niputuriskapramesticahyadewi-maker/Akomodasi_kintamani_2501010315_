import requests
import json
import pandas as pd
from pathlib import Path

URL = "https://overpass-api.de/api/interpreter"
HEADERS = {"User-Agent": "INSTIKI-BIFP243-Praktikum/1.0 (2501010315@instiki.ac.id)"}

QUERY = '''
[out:json][timeout:90];
area["name"="Kintamani"]["boundary"="administrative"]["admin_level"="6"]->.kec;
nwr["tourism"~"^(hotel|guest_house|hostel|motel|apartment|chalet)$"](area.kec);
out center tags;
'''

def ambil_data():
    r = requests.post(URL, data={"data": QUERY}, headers=HEADERS, timeout=120)
    if r.status_code == 200:
        return r.json()
    raise RuntimeError(f"Gagal: {r.status_code}")

if __name__ == "__main__":
    data = ambil_data()
    print(f"Berhasil mengambil {len(data['elements'])} elemen akomodasi Kintamani.")
