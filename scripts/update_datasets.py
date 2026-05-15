from __future__ import annotations

import argparse
import csv
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlencode

import requests

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


def get_json(url: str) -> Any:
    r = requests.get(url, timeout=45, headers=HEADERS)
    r.raise_for_status()
    return r.json()


def get_text(url: str) -> str:
    r = requests.get(url, timeout=45, headers=HEADERS)
    r.raise_for_status()
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
    text = get_text(url)
    path = DATA / "fred_fedfunds.csv"
    path.write_text(text, encoding="utf-8")
    rows = max(0, len(text.splitlines()) - 1)
    return {"file": str(path.relative_to(ROOT)), "rows": rows, "scope": scope, "source": url}


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
