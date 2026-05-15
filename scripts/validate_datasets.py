from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"

MIN_ROWS = {
    "open_meteo_seoul_daily_weather.csv": 365 * 4,
    "open_meteo_seoul_air_quality_hourly.csv": 24 * 365 * 4,
    "worldbank_korea_indicators.csv": 10,
    "usgs_major_earthquakes.csv": 100,
    "mlb_schedule.csv": 1000,
    "fred_fedfunds.csv": 48,
    "owid_co2_korea_world.csv": 5,
    "gbif_korea_occurrences_sample.csv": 100,
    "artic_recent_artworks_sample.csv": 50,
    "seoul_bike_sample.csv": 5,
}


def count_rows(path: Path) -> tuple[int, list[str]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return 0, []
    return max(0, len(rows) - 1), rows[0]


def main() -> None:
    failures: list[str] = []
    report = []

    for filename, min_rows in MIN_ROWS.items():
        path = DATA / filename
        if not path.exists():
            failures.append(f"missing data file: {filename}")
            continue
        rows, columns = count_rows(path)
        report.append({"file": filename, "rows": rows, "columns": columns})
        if rows < min_rows:
            failures.append(f"{filename}: rows {rows} < minimum {min_rows}")
        if not columns:
            failures.append(f"{filename}: empty header")

        docs_copy = DOCS / "data" / filename
        if docs_copy.exists():
            docs_rows, docs_columns = count_rows(docs_copy)
            if docs_rows != rows or docs_columns != columns:
                failures.append(f"docs copy mismatch: {filename}")

    required_pages = [DOCS / "index.html", DOCS / "datasets.json"]
    required_pages += list((DOCS / "datasets").glob("*.html"))
    if len(list((DOCS / "datasets").glob("*.html"))) < 10:
        failures.append("expected at least 10 dataset pages")
    for page in required_pages:
        if not page.exists():
            failures.append(f"missing page: {page.relative_to(ROOT)}")
        elif page.name not in {"datasets.json", "index.html"}:
            text = page.read_text(encoding="utf-8")
            checks = {
                "direct fetch test code": "fetch(" in text,
                "CSV to JSON test code": "parseCsv" in text and "JSON sample" in text,
                "browser visualization code": "drawChart" in text and "<svg" in text,
                "Streamlit code": "streamlit" in text.lower(),
                "Pico W code": "Pico W" in text or "MicroPython" in text,
            }
            for label, ok in checks.items():
                if not ok:
                    failures.append(f"page lacks {label}: {page.relative_to(ROOT)}")

    manifest = DATA / "manifest.json"
    if manifest.exists():
        json.loads(manifest.read_text(encoding="utf-8"))
    else:
        failures.append("missing data/manifest.json")

    print(json.dumps({"datasets": report, "failures": failures}, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
