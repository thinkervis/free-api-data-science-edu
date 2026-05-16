#!/usr/bin/env python3
"""Generate a polished SVG map for the SDG biodiversity card.

The map uses the same population-data boundary source as the population
visualization example: skorea_provinces_geo_simple.json plus
korea_sido_wikidata_population.csv. GBIF occurrence points are overlaid.
"""

from __future__ import annotations

import csv
import html
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GEO_PATH = ROOT / "docs/assets/skorea_provinces_geo_simple.json"
POP_PATH = ROOT / "docs/data/korea_sido_wikidata_population.csv"
GBIF_PATH = ROOT / "docs/data/gbif_korea_occurrences_sample.csv"
OUT_PATH = ROOT / "docs/assets/gbif-korea-pop-density-map.svg"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(value: Any) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        n = float(value)
    except ValueError:
        return None
    return n if math.isfinite(n) and n > -900 else None


def walk_coords(coords: Any) -> list[list[float]]:
    if not coords:
        return []
    if isinstance(coords[0], (int, float)):
        return [coords]
    pts: list[list[float]] = []
    for child in coords:
        pts.extend(walk_coords(child))
    return pts


def bounds(features: list[dict[str, Any]]) -> dict[str, float]:
    pts: list[list[float]] = []
    for f in features:
        pts.extend(walk_coords(f.get("geometry", {}).get("coordinates")))
    lons = [p[0] for p in pts]
    lats = [p[1] for p in pts]
    return {"min_lon": min(lons), "max_lon": max(lons), "min_lat": min(lats), "max_lat": max(lats)}


def project(lon: float, lat: float, b: dict[str, float], w: int, h: int, pad: int = 34) -> tuple[float, float]:
    x = pad + (lon - b["min_lon"]) / (b["max_lon"] - b["min_lon"]) * (w - pad * 2)
    y = pad + (b["max_lat"] - lat) / (b["max_lat"] - b["min_lat"]) * (h - pad * 2)
    return x, y


def ring_path(ring: list[list[float]], b: dict[str, float], w: int, h: int) -> str:
    parts = []
    for i, point in enumerate(ring):
        x, y = project(point[0], point[1], b, w, h)
        parts.append(("M" if i == 0 else "L") + f"{x:.2f} {y:.2f}")
    return " ".join(parts) + " Z"


def feature_path(feature: dict[str, Any], b: dict[str, float], w: int, h: int) -> str:
    geom = feature.get("geometry") or {}
    coords = geom.get("coordinates") or []
    if geom.get("type") == "Polygon":
        return " ".join(ring_path(ring, b, w, h) for ring in coords)
    if geom.get("type") == "MultiPolygon":
        return " ".join(ring_path(ring, b, w, h) for poly in coords for ring in poly)
    return ""


def mean_point(coords: Any) -> tuple[float, float] | None:
    pts = walk_coords(coords)
    if not pts:
        return None
    return sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)


def short_name(name: str) -> str:
    return (
        name.replace("특별자치도", "")
        .replace("특별자치시", "")
        .replace("광역시", "")
        .replace("특별시", "")
        .replace("자치도", "")
        .replace("도", "")
    )


def label_offset(name: str) -> tuple[int, int]:
    # 수도권·충청권처럼 면적이 작거나 중심점이 가까운 지역은 라벨이 겹쳐
    # “서울기”처럼 보일 수 있어 수업용 정적 SVG에서는 직접 보정한다.
    return {
        "서울특별시": (-54, -16),
        "인천광역시": (-70, 22),
        "경기도": (44, -10),
        "세종특별자치시": (-42, 14),
        "대전광역시": (34, 18),
        "충청남도": (-42, -12),
        "충청북도": (44, -12),
        "대구광역시": (42, 8),
        "울산광역시": (46, 14),
        "부산광역시": (38, 30),
        "광주광역시": (-44, 16),
    }.get(name, (0, 0))


def blue_scale(value: float | None, min_value: float, max_value: float) -> str:
    if value is None:
        return "#e5e7eb"
    stops = [(240, 249, 255), (186, 230, 253), (96, 165, 250), (37, 99, 235), (30, 64, 175)]
    t = 0.65 if max_value == min_value else (value - min_value) / (max_value - min_value)
    scaled = max(0, min(len(stops) - 1, t * (len(stops) - 1)))
    i = min(len(stops) - 2, int(math.floor(scaled)))
    f = scaled - i
    rgb = [round(stops[i][j] + (stops[i + 1][j] - stops[i][j]) * f) for j in range(3)]
    return f"rgb({rgb[0]},{rgb[1]},{rgb[2]})"


def main() -> None:
    geo = json.loads(GEO_PATH.read_text(encoding="utf-8"))
    features = geo["features"]
    pop_by_id = {row.get("svg_id") or row.get("region"): row for row in read_csv(POP_PATH)}
    gbif = read_csv(GBIF_PATH)
    b = bounds(features)
    w = 1100
    h = round((b["max_lat"] - b["min_lat"]) / (b["max_lon"] - b["min_lon"]) * w) + 110
    densities = [num(row.get("population_density_per_km2")) for row in pop_by_id.values()]
    densities = [d for d in densities if d is not None]
    min_density, max_density = min(densities), max(densities)

    boundary_parts = []
    label_parts = []
    for feature in features:
        name = feature.get("properties", {}).get("name", "")
        pop = pop_by_id.get(name, {})
        density = num(pop.get("population_density_per_km2"))
        fill = blue_scale(density, min_density, max_density)
        title = name
        if pop:
            title = f"{name} · 인구 {int(float(pop['population'])):,}명 · 인구밀도 {float(pop['population_density_per_km2']):,.0f}명/km²"
        boundary_parts.append(
            f'<path class="province" d="{feature_path(feature, b, w, h)}" fill="{fill}"><title>{html.escape(title)}</title></path>'
        )
        center = mean_point(feature.get("geometry", {}).get("coordinates"))
        if center:
            x, y = project(center[0], center[1], b, w, h)
            dx, dy = label_offset(name)
            label_parts.append(f'<text class="label" x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="middle">{html.escape(short_name(name))}</text>')

    point_parts = []
    for row in gbif:
        lat, lon = num(row.get("decimalLatitude")), num(row.get("decimalLongitude"))
        if lat is None or lon is None:
            continue
        x, y = project(lon, lat, b, w, h)
        title = f"{row.get('scientificName') or '관측'} · {row.get('locality') or ''}"
        point_parts.append(f'<circle class="gbif-point" cx="{x:.1f}" cy="{y:.1f}" r="4.2"><title>{html.escape(title)}</title></circle>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">한국 생물종 관측 위치와 광역시도 인구밀도</title>
<desc id="desc">광역시도 경계를 인구밀도로 색칠하고, GBIF 생물종 관측 위치를 초록 점으로 표시한 수업용 SVG 지도입니다.</desc>
<style>
  .province{{stroke:#fff;stroke-width:1.6;vector-effect:non-scaling-stroke}}
  .province:hover{{stroke:#111827;stroke-width:2.4}}
  .gbif-point{{fill:#16a34a;fill-opacity:.68;stroke:#064e3b;stroke-width:.75;vector-effect:non-scaling-stroke}}
  .label{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:16px;font-weight:800;fill:#1f2937;paint-order:stroke;stroke:#fff;stroke-width:4;stroke-linejoin:round}}
  .title{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:28px;font-weight:800;fill:#0f172a}}
  .note{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:14px;fill:#475569}}
</style>
<defs>
  <linearGradient id="densityGradient" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0%" stop-color="#f0f9ff"/><stop offset="35%" stop-color="#bae6fd"/><stop offset="70%" stop-color="#60a5fa"/><stop offset="100%" stop-color="#1e40af"/>
  </linearGradient>
</defs>
<rect width="{w}" height="{h}" rx="28" fill="#f8fbff"/>
<text class="title" x="34" y="50">한국 생물종 관측 위치 + 광역시도 인구밀도</text>
<text class="note" x="34" y="78">배경: korea_sido_wikidata_population.csv 인구밀도 · 점: GBIF 관측 {len(point_parts):,}건</text>
<g>{''.join(boundary_parts)}</g>
<g>{''.join(point_parts)}</g>
<g>{''.join(label_parts)}</g>
<g transform="translate(34 {h-56})">
  <text class="note" x="0" y="-12" font-weight="700">인구밀도 낮음 → 높음</text>
  <rect x="0" y="0" width="260" height="16" rx="8" fill="url(#densityGradient)"/>
  <text class="note" x="0" y="38">{round(min_density):,}</text>
  <text class="note" x="260" y="38" text-anchor="end">{round(max_density):,}명/km²</text>
  <circle class="gbif-point" cx="350" cy="8" r="5"/>
  <text class="note" x="368" y="13">GBIF 생물종 관측점</text>
</g>
</svg>
'''
    OUT_PATH.write_text(svg, encoding="utf-8")
    print(OUT_PATH)


if __name__ == "__main__":
    main()
