from __future__ import annotations

import argparse
import csv
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlencode

import requests
from requests import RequestException

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
HEADERS = {"User-Agent": "free-api-data-science-edu/0.2 dataset-updater"}


def add_years(d: date, years: int) -> date:
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return d.replace(month=2, day=28, year=d.year + years)


def range_for_scope(scope: str) -> tuple[date, date]:
    today = date.today()
    end = today - timedelta(days=1)
    if scope == "all":
        # Conservative all-period default for APIs where truly full history may be huge.
        return date(1940, 1, 1), end
    return add_years(today, -5), end


def fetch(url: str, timeouts: tuple[int, ...] = (45, 90, 150)) -> requests.Response:
    last_error: Exception | None = None
    for timeout in timeouts:
        try:
            r = requests.get(url, timeout=timeout, headers=HEADERS)
            r.raise_for_status()
            return r
        except RequestException as exc:
            last_error = exc
            print(f"retryable fetch error timeout={timeout}: {exc}")
    assert last_error is not None
    raise last_error


def get_json(url: str) -> Any:
    return fetch(url).json()


def get_text(url: str, timeouts: tuple[int, ...] = (45, 90, 150)) -> str:
    r = fetch(url, timeouts=timeouts)
    try:
        return r.content.decode("utf-8")
    except UnicodeDecodeError:
        return r.text


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        keys: list[str] = []
        for row in rows:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def rows_from_series(data: dict[str, Any], key: str, static: dict[str, Any]) -> list[dict[str, Any]]:
    series = data[key]
    times = series["time"]
    rows: list[dict[str, Any]] = []
    for i, t in enumerate(times):
        row = {**static, "time": t}
        for field, values in series.items():
            if field != "time":
                row[field] = values[i]
        rows.append(row)
    return rows


def update_open_meteo_seoul_daily(scope: str) -> dict[str, Any]:
    start, end = range_for_scope(scope)
    params = {
        "latitude": 37.5665,
        "longitude": 126.9780,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,wind_speed_10m_max",
        "timezone": "Asia/Seoul",
    }
    url = "https://archive-api.open-meteo.com/v1/archive?" + urlencode(params)
    data = get_json(url)
    rows = rows_from_series(data, "daily", {"location": "Seoul", "latitude": data["latitude"], "longitude": data["longitude"]})
    path = DATA / "open_meteo_seoul_daily_weather.csv"
    write_csv(path, rows)
    return {"file": str(path.relative_to(ROOT)), "rows": len(rows), "scope": scope, "source": url}


def update_open_meteo_seoul_air_quality(scope: str) -> dict[str, Any]:
    start, end = range_for_scope(scope)
    if scope == "all":
        start = max(start, date(2020, 1, 1))
    params = {
        "latitude": 37.5665,
        "longitude": 126.9780,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "hourly": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone",
        "timezone": "Asia/Seoul",
    }
    url = "https://air-quality-api.open-meteo.com/v1/air-quality?" + urlencode(params)
    data = get_json(url)
    rows = rows_from_series(data, "hourly", {"location": "Seoul", "latitude": data["latitude"], "longitude": data["longitude"]})
    path = DATA / "open_meteo_seoul_air_quality_hourly.csv"
    write_csv(path, rows)
    return {"file": str(path.relative_to(ROOT)), "rows": len(rows), "scope": scope, "source": url}


def update_worldbank_korea_indicators(scope: str) -> dict[str, Any]:
    start, end = range_for_scope(scope)
    date_param = "1960:2030" if scope == "all" else f"{start.year}:{end.year}"
    indicators = {
        "SP.POP.TOTL": "Population, total",
        "NY.GDP.MKTP.CD": "GDP (current US$)",
        "SP.DYN.LE00.IN": "Life expectancy at birth, total (years)",
        "SE.SEC.ENRR": "School enrollment, secondary (% gross)",
    }
    rows: list[dict[str, Any]] = []
    for indicator in indicators:
        url = f"https://api.worldbank.org/v2/country/KOR/indicator/{indicator}?format=json&per_page=20000&date={date_param}"
        data = get_json(url)
        if not isinstance(data, list) or len(data) < 2 or data[1] is None:
            continue
        for item in data[1]:
            rows.append(
                {
                    "country": item["country"]["value"],
                    "countryiso3code": item["countryiso3code"],
                    "indicator_id": item["indicator"]["id"],
                    "indicator": item["indicator"]["value"],
                    "date": item["date"],
                    "value": item["value"],
                }
            )
    rows.sort(key=lambda r: (r["indicator_id"], r["date"]))
    path = DATA / "worldbank_korea_indicators.csv"
    write_csv(path, rows)
    return {"file": str(path.relative_to(ROOT)), "rows": len(rows), "scope": scope, "source": "https://api.worldbank.org/v2/"}


def update_usgs_major_earthquakes(scope: str) -> dict[str, Any]:
    start, end = range_for_scope(scope)
    if scope == "all":
        start = max(start, date(1900, 1, 1))
    params = {
        "format": "geojson",
        "starttime": start.isoformat(),
        "endtime": end.isoformat(),
        "minmagnitude": 6,
        "orderby": "time-asc",
        "limit": 20000,
    }
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query?" + urlencode(params)
    data = get_json(url)
    rows = []
    for feature in data.get("features", []):
        props = feature.get("properties", {})
        coords = feature.get("geometry", {}).get("coordinates", [None, None, None])
        rows.append(
            {
                "id": feature.get("id"),
                "time_utc": datetime.fromtimestamp(props.get("time", 0) / 1000, tz=timezone.utc).isoformat() if props.get("time") else None,
                "magnitude": props.get("mag"),
                "place": props.get("place"),
                "longitude": coords[0],
                "latitude": coords[1],
                "depth_km": coords[2] if len(coords) > 2 else None,
                "type": props.get("type"),
                "url": props.get("url"),
            }
        )
    path = DATA / "usgs_major_earthquakes.csv"
    write_csv(path, rows)
    return {"file": str(path.relative_to(ROOT)), "rows": len(rows), "scope": scope, "source": url}


def update_mlb_schedule(scope: str) -> dict[str, Any]:
    start, end = range_for_scope(scope)
    if scope == "all":
        start = max(start, date(2015, 1, 1))
    params = {"sportId": 1, "startDate": start.isoformat(), "endDate": end.isoformat()}
    url = "https://statsapi.mlb.com/api/v1/schedule?" + urlencode(params)
    data = get_json(url)
    rows = []
    for date_item in data.get("dates", []):
        for game in date_item.get("games", []):
            teams = game.get("teams", {})
            rows.append(
                {
                    "date": date_item.get("date"),
                    "gamePk": game.get("gamePk"),
                    "gameDate": game.get("gameDate"),
                    "season": game.get("season"),
                    "gameType": game.get("gameType"),
                    "status": game.get("status", {}).get("detailedState"),
                    "away_team": teams.get("away", {}).get("team", {}).get("name"),
                    "home_team": teams.get("home", {}).get("team", {}).get("name"),
                    "away_score": teams.get("away", {}).get("score"),
                    "home_score": teams.get("home", {}).get("score"),
                }
            )
    path = DATA / "mlb_schedule.csv"
    write_csv(path, rows)
    return {"file": str(path.relative_to(ROOT)), "rows": len(rows), "scope": scope, "source": url}


def update_fred_fedfunds(scope: str) -> dict[str, Any]:
    start, end = range_for_scope(scope)
    if scope == "all":
        start = date(1954, 7, 1)
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?" + urlencode({"id": "FEDFUNDS", "cosd": start.isoformat(), "coed": end.isoformat()})
    path = DATA / "fred_fedfunds.csv"
    try:
        text = get_text(url, timeouts=(10, 20, 30))
        path.write_text(text, encoding="utf-8")
        source = url
    except RequestException as exc:
        if not path.exists():
            raise
        print(f"FRED fetch failed; keeping existing checked-in CSV: {exc}")
        text = path.read_text(encoding="utf-8")
        source = f"{url} (fallback: existing checked-in CSV)"
    rows = max(0, len(text.splitlines()) - 1)
    return {"file": str(path.relative_to(ROOT)), "rows": rows, "scope": scope, "source": source}


def update_owid_co2(scope: str) -> dict[str, Any]:
    start, end = range_for_scope(scope)
    start_year = 1750 if scope == "all" else start.year
    url = "https://ourworldindata.org/grapher/annual-co2-emissions-per-country.csv"
    text = get_text(url)
    reader = csv.DictReader(text.splitlines())
    rows = [row for row in reader if row.get("Code") in {"KOR", "OWID_WRL"} and int(row.get("Year", "0")) >= start_year and int(row.get("Year", "0")) <= end.year]
    path = DATA / "owid_co2_korea_world.csv"
    write_csv(path, rows, fieldnames=reader.fieldnames)
    return {"file": str(path.relative_to(ROOT)), "rows": len(rows), "scope": scope, "source": url}


def update_gbif_korea_occurrences(scope: str) -> dict[str, Any]:
    start, end = range_for_scope(scope)
    year_param = f"{start.year},{end.year}"
    params = {"country": "KR", "year": year_param, "limit": 300}
    url = "https://api.gbif.org/v1/occurrence/search?" + urlencode(params)
    data = get_json(url)
    rows = []
    for item in data.get("results", []):
        rows.append(
            {
                "key": item.get("key"),
                "scientificName": item.get("scientificName"),
                "vernacularName": item.get("vernacularName"),
                "eventDate": item.get("eventDate"),
                "year": item.get("year"),
                "country": item.get("country"),
                "locality": item.get("locality"),
                "decimalLatitude": item.get("decimalLatitude"),
                "decimalLongitude": item.get("decimalLongitude"),
                "basisOfRecord": item.get("basisOfRecord"),
            }
        )
    path = DATA / "gbif_korea_occurrences_sample.csv"
    write_csv(path, rows)
    return {"file": str(path.relative_to(ROOT)), "rows": len(rows), "scope": scope, "source": url}


def update_artic_recent_artworks(scope: str) -> dict[str, Any]:
    start, end = range_for_scope(scope)
    start_year = 0 if scope == "all" else start.year
    rows = []
    # The API supports Elasticsearch-style range filters. Keep this as a compact teaching sample.
    params = {
        "query[range][date_end][gte]": start_year,
        "query[range][date_end][lte]": end.year,
        "fields": "id,title,artist_title,date_start,date_end,medium_display,place_of_origin",
        "limit": 100,
    }
    url = "https://api.artic.edu/api/v1/artworks/search?" + urlencode(params)
    data = get_json(url)
    for item in data.get("data", []):
        rows.append(item)
    path = DATA / "artic_recent_artworks_sample.csv"
    write_csv(path, rows)
    return {"file": str(path.relative_to(ROOT)), "rows": len(rows), "scope": scope, "source": url}


def update_seoul_bike_sample(_: str) -> dict[str, Any]:
    url = "http://openapi.seoul.go.kr:8088/sample/json/bikeList/1/5/"
    data = get_json(url)
    rows = data["rentBikeStatus"]["row"]
    path = DATA / "seoul_bike_sample.csv"
    write_csv(path, rows)
    return {"file": str(path.relative_to(ROOT)), "rows": len(rows), "scope": "sample", "source": url}

def update_nasa_power_seoul_daily(scope: str) -> dict[str, Any]:
    start, end = range_for_scope(scope)
    if scope == "all":
        start = max(start, date(1984, 1, 1))
    params = {
        "parameters": "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,WS2M",
        "community": "RE",
        "longitude": 126.9780,
        "latitude": 37.5665,
        "start": start.strftime("%Y%m%d"),
        "end": end.strftime("%Y%m%d"),
        "format": "JSON",
    }
    url = "https://power.larc.nasa.gov/api/temporal/daily/point?" + urlencode(params)
    data = get_json(url)
    params_data = data.get("properties", {}).get("parameter", {})
    dates = sorted(next(iter(params_data.values())).keys()) if params_data else []
    rows = []
    for ymd in dates:
        rows.append({
            "location": "Seoul",
            "date": f"{ymd[:4]}-{ymd[4:6]}-{ymd[6:]}",
            "temperature_2m_c": params_data.get("T2M", {}).get(ymd),
            "temperature_max_c": params_data.get("T2M_MAX", {}).get(ymd),
            "temperature_min_c": params_data.get("T2M_MIN", {}).get(ymd),
            "precipitation_mm_day": params_data.get("PRECTOTCORR", {}).get(ymd),
            "wind_speed_2m_m_s": params_data.get("WS2M", {}).get(ymd),
        })
    path = DATA / "nasa_power_seoul_daily.csv"
    write_csv(path, rows)
    return {"file": str(path.relative_to(ROOT)), "rows": len(rows), "scope": scope, "source": url}


def update_bls_us_cpi(scope: str) -> dict[str, Any]:
    start, end = range_for_scope(scope)
    start_year = max(2005, start.year) if scope == "all" else start.year
    url = f"https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0?startyear={start_year}&endyear={end.year}"
    data = get_json(url)
    rows = []
    for item in data.get("Results", {}).get("series", [{}])[0].get("data", []):
        period = item.get("period", "")
        if not period.startswith("M"):
            continue
        rows.append({
            "series_id": "CUUR0000SA0",
            "year": item.get("year"),
            "month": period,
            "date": f"{item.get('year')}-{period[1:]}-01",
            "cpi_value": item.get("value"),
            "footnotes": "; ".join(f.get("text", "") for f in item.get("footnotes", []) if f.get("text")),
        })
    rows.sort(key=lambda r: r["date"])
    path = DATA / "bls_us_cpi_monthly.csv"
    write_csv(path, rows)
    return {"file": str(path.relative_to(ROOT)), "rows": len(rows), "scope": scope, "source": url}


def update_nager_korea_holidays(scope: str) -> dict[str, Any]:
    start, end = range_for_scope(scope)
    start_year = 1970 if scope == "all" else start.year
    rows = []
    source_urls = []
    for year in range(start_year, end.year + 1):
        url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/KR"
        source_urls.append(url)
        for item in get_json(url):
            rows.append({
                "date": item.get("date"),
                "localName": item.get("localName"),
                "name": item.get("name"),
                "countryCode": item.get("countryCode"),
                "global": item.get("global"),
                "types": ",".join(item.get("types", [])),
            })
    rows.sort(key=lambda r: r["date"])
    path = DATA / "nager_korea_public_holidays.csv"
    write_csv(path, rows)
    return {"file": str(path.relative_to(ROOT)), "rows": len(rows), "scope": scope, "source": source_urls[0] if source_urls else "https://date.nager.at/"}


def update_spacex_launches(scope: str) -> dict[str, Any]:
    start, end = range_for_scope(scope)
    if scope == "all":
        start = date(2006, 1, 1)
    url = "https://api.spacexdata.com/v5/launches/query"
    payload = {
        "query": {"date_utc": {"$gte": f"{start.isoformat()}T00:00:00.000Z", "$lte": f"{end.isoformat()}T23:59:59.999Z"}},
        "options": {"limit": 500, "sort": {"date_utc": "asc"}, "select": ["name", "date_utc", "success", "flight_number", "details", "links"]},
    }
    r = requests.post(url, json=payload, timeout=45, headers=HEADERS)
    r.raise_for_status()
    data = r.json()
    rows = []
    for item in data.get("docs", []):
        rows.append({
            "flight_number": item.get("flight_number"),
            "name": item.get("name"),
            "date_utc": item.get("date_utc"),
            "success": item.get("success"),
            "details": item.get("details"),
            "wikipedia": item.get("links", {}).get("wikipedia"),
            "webcast": item.get("links", {}).get("webcast"),
        })
    path = DATA / "spacex_launches.csv"
    write_csv(path, rows)
    return {"file": str(path.relative_to(ROOT)), "rows": len(rows), "scope": scope, "source": url}


def update_frankfurter_usd_krw(scope: str) -> dict[str, Any]:
    start, end = range_for_scope(scope)
    if scope == "all":
        start = max(start, date(1999, 1, 4))
    url = f"https://api.frankfurter.app/{start.isoformat()}..{end.isoformat()}?from=USD&to=KRW"
    data = get_json(url)
    rows = []
    for day, rates in data.get("rates", {}).items():
        rows.append({"date": day, "base": data.get("base"), "quote": "KRW", "rate": rates.get("KRW")})
    rows.sort(key=lambda r: r["date"])
    path = DATA / "frankfurter_usd_krw_daily.csv"
    write_csv(path, rows)
    return {"file": str(path.relative_to(ROOT)), "rows": len(rows), "scope": scope, "source": url}


def update_who_korea_life_expectancy(scope: str) -> dict[str, Any]:
    start, end = range_for_scope(scope)
    start_year = 2000 if scope == "all" else start.year
    filter_q = f"SpatialDim eq 'KOR' and TimeDim ge {start_year} and TimeDim le {end.year}"
    url = "https://ghoapi.azureedge.net/api/WHOSIS_000001?" + urlencode({"$filter": filter_q, "$top": 1000})
    data = get_json(url)
    rows = []
    for item in data.get("value", []):
        rows.append({
            "indicator": item.get("IndicatorCode"),
            "year": item.get("TimeDim"),
            "country": item.get("SpatialDim"),
            "sex": item.get("Dim1"),
            "value": item.get("NumericValue"),
            "display": item.get("Value"),
        })
    rows.sort(key=lambda r: (str(r.get("sex")), r.get("year") or 0))
    path = DATA / "who_korea_life_expectancy.csv"
    write_csv(path, rows)
    return {"file": str(path.relative_to(ROOT)), "rows": len(rows), "scope": scope, "source": url}


def update_restcountries_world_snapshot(_: str) -> dict[str, Any]:
    url = "https://restcountries.com/v3.1/all?fields=name,cca3,region,subregion,population,area,latlng"
    data = get_json(url)
    rows = []
    for item in data:
        latlng = item.get("latlng") or [None, None]
        rows.append({
            "name": item.get("name", {}).get("common"),
            "official_name": item.get("name", {}).get("official"),
            "cca3": item.get("cca3"),
            "region": item.get("region"),
            "subregion": item.get("subregion"),
            "population": item.get("population"),
            "area": item.get("area"),
            "latitude": latlng[0] if len(latlng) > 0 else None,
            "longitude": latlng[1] if len(latlng) > 1 else None,
        })
    rows.sort(key=lambda r: r.get("name") or "")
    path = DATA / "restcountries_world_snapshot.csv"
    write_csv(path, rows)
    return {"file": str(path.relative_to(ROOT)), "rows": len(rows), "scope": "snapshot", "source": url}


def update_eia_california_electricity(scope: str) -> dict[str, Any]:
    start, end = range_for_scope(scope)
    if scope == "all":
        start = max(start, date(2018, 7, 1))
    params = [
        ("frequency", "daily"),
        ("data[0]", "value"),
        ("facets[respondent][]", "CAL"),
        ("start", start.isoformat()),
        ("end", end.isoformat()),
        ("sort[0][column]", "period"),
        ("sort[0][direction]", "asc"),
        ("offset", "0"),
        ("length", "5000"),
        ("api_key", "DEMO_KEY"),
    ]
    url = "https://api.eia.gov/v2/electricity/rto/daily-region-data/data/?" + urlencode(params)
    data = get_json(url)
    rows = []
    for item in data.get("response", {}).get("data", []):
        rows.append({
            "date": item.get("period"),
            "respondent": item.get("respondent"),
            "respondent_name": item.get("respondent-name"),
            "type": item.get("type"),
            "type_name": item.get("type-name"),
            "value": item.get("value"),
            "unit": item.get("value-units"),
        })
    path = DATA / "eia_california_electricity_daily.csv"
    write_csv(path, rows)
    return {"file": str(path.relative_to(ROOT)), "rows": len(rows), "scope": scope, "source": url}


JOBS = [
    update_open_meteo_seoul_daily,
    update_open_meteo_seoul_air_quality,
    update_worldbank_korea_indicators,
    update_usgs_major_earthquakes,
    update_mlb_schedule,
    update_fred_fedfunds,
    update_owid_co2,
    update_gbif_korea_occurrences,
    update_artic_recent_artworks,
    update_seoul_bike_sample,
    update_nasa_power_seoul_daily,
    update_bls_us_cpi,
    update_nager_korea_holidays,
    update_spacex_launches,
    update_frankfurter_usd_krw,
    update_who_korea_life_expectancy,
    update_restcountries_world_snapshot,
    update_eia_california_electricity,
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Update teaching CSV datasets.")
    parser.add_argument("--scope", choices=["recent5", "all"], default="recent5", help="recent5 uploads recent five years; all requests the broadest safe supported range")
    args = parser.parse_args()

    results = []
    for job in JOBS:
        print(f"running {job.__name__} --scope={args.scope}")
        results.append(job(args.scope))
    manifest = {
        "updated_at_utc": datetime.now(timezone.utc).isoformat(),
        "default_scope": args.scope,
        "files": sorted(str(p.relative_to(ROOT)) for p in DATA.glob("*.csv")),
        "results": results,
    }
    (DATA / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
