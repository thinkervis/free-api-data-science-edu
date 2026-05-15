import requests

APIS = [
    ("Open-Meteo", "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current=temperature_2m,relative_humidity_2m,wind_speed_10m&timezone=Asia%2FSeoul"),
    ("World Bank", "https://api.worldbank.org/v2/country/KOR/indicator/SP.POP.TOTL?format=json&per_page=5"),
    ("USGS Earthquake", "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&limit=1&orderby=time"),
    ("REST Countries", "https://restcountries.com/v3.1/name/korea?fields=name,capital,population,region,currencies,languages"),
    ("Seoul Bike sample", "http://openapi.seoul.go.kr:8088/sample/json/bikeList/1/5/"),
]

for name, url in APIS:
    try:
        r = requests.get(url, timeout=10)
        content_type = r.headers.get("content-type", "")
        print(f"{name:18} status={r.status_code} content-type={content_type} bytes={len(r.content)}")
        r.raise_for_status()
    except Exception as exc:
        print(f"{name:18} ERROR {exc}")
