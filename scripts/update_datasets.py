from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
HEADERS = {"User-Agent": "free-api-data-science-edu/0.1 dataset-updater"}


def get_json(url: str) -> Any:
    r = requests.get(url, timeout=20, headers=HEADERS)
    r.raise_for_status()
    return r.json()


def get_text(url: str) -> str:
    r = requests.get(url, timeout=20, headers=HEADERS)
    r.raise_for_status()
    return r.text


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
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


def update_stooq_quote() -> None:
    url = "https://stooq.com/q/l/?s=aapl.us&f=sd2t2ohlcv&h&e=csv"
    text = get_text(url)
    (DATA / "stooq_aapl_quote.csv").write_text(text, encoding="utf-8")


def update_worldbank_population() -> None:
    url = "https://api.worldbank.org/v2/country/KOR/indicator/SP.POP.TOTL?format=json&per_page=100"
    data = get_json(url)
    rows = []
    for item in data[1]:
        rows.append(
            {
                "country": item["country"]["value"],
                "countryiso3code": item["countryiso3code"],
                "indicator": item["indicator"]["id"],
                "date": item["date"],
                "value": item["value"],
            }
        )
    rows.sort(key=lambda r: r["date"])
    write_csv(DATA / "worldbank_korea_population.csv", rows)


def update_open_meteo_current() -> None:
    url = "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current=temperature_2m,relative_humidity_2m,wind_speed_10m&timezone=Asia%2FSeoul"
    data = get_json(url)
    current = data["current"]
    rows = [
        {
            "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
            "location": "Seoul",
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "time": current["time"],
            "temperature_2m": current["temperature_2m"],
            "relative_humidity_2m": current["relative_humidity_2m"],
            "wind_speed_10m": current["wind_speed_10m"],
        }
    ]
    write_csv(DATA / "open_meteo_seoul_current.csv", rows)


def update_mlb_schedule_sample() -> None:
    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2024-03-28"
    data = get_json(url)
    rows = []
    for date in data.get("dates", []):
        for game in date.get("games", []):
            teams = game.get("teams", {})
            rows.append(
                {
                    "date": date.get("date"),
                    "gamePk": game.get("gamePk"),
                    "gameDate": game.get("gameDate"),
                    "status": game.get("status", {}).get("detailedState"),
                    "away_team": teams.get("away", {}).get("team", {}).get("name"),
                    "home_team": teams.get("home", {}).get("team", {}).get("name"),
                    "away_score": teams.get("away", {}).get("score"),
                    "home_score": teams.get("home", {}).get("score"),
                }
            )
    write_csv(DATA / "mlb_schedule_sample.csv", rows)


def update_seoul_bike_sample() -> None:
    url = "http://openapi.seoul.go.kr:8088/sample/json/bikeList/1/5/"
    data = get_json(url)
    rows = data["rentBikeStatus"]["row"]
    write_csv(DATA / "seoul_bike_sample.csv", rows)


def main() -> None:
    jobs = [
        update_stooq_quote,
        update_worldbank_population,
        update_open_meteo_current,
        update_mlb_schedule_sample,
        update_seoul_bike_sample,
    ]
    for job in jobs:
        print(f"running {job.__name__}")
        job()
    manifest = {
        "updated_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": sorted(str(p.relative_to(ROOT)) for p in DATA.glob("*.csv")),
    }
    (DATA / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
