import csv
from io import StringIO
import requests

APIS = [
    ("Open-Meteo", "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current=temperature_2m,relative_humidity_2m,wind_speed_10m&timezone=Asia%2FSeoul"),
    ("World Bank", "https://api.worldbank.org/v2/country/KOR/indicator/SP.POP.TOTL?format=json&per_page=5"),
    ("USGS Earthquake", "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&limit=1&orderby=time"),
    ("REST Countries", "https://restcountries.com/v3.1/name/korea?fields=name,capital,population,region,currencies,languages"),
    ("Seoul Bike sample", "http://openapi.seoul.go.kr:8088/sample/json/bikeList/1/5/"),
    ("Nominatim", "https://nominatim.openstreetmap.org/search?q=Seoul%20City%20Hall&format=json&limit=1"),
    ("Stooq CSV", "https://stooq.com/q/l/?s=aapl.us&f=sd2t2ohlcv&h&e=csv"),
]

HEADERS = {"User-Agent": "free-api-data-science-edu/0.1 educational-test"}

for name, url in APIS:
    try:
        r = requests.get(url, timeout=10, headers=HEADERS)
        content_type = r.headers.get("content-type", "")
        print(f"{name:18} status={r.status_code} content-type={content_type} bytes={len(r.content)}")
        r.raise_for_status()
        if "csv" in content_type:
            rows = list(csv.reader(StringIO(r.text)))
            print(f"{'':18} csv_rows={len(rows)} columns={rows[0] if rows else []}")
    except Exception as exc:
        print(f"{name:18} ERROR {exc}")
