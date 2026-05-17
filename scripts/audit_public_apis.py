from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Any

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw" / "public-apis"
AUDITS = ROOT / "audits"
SOURCE_URL = "https://raw.githubusercontent.com/public-apis/public-apis/master/README.md"

EDU_KEYWORDS = {
    "science": ["weather", "earth", "space", "nasa", "climate", "air", "water", "ocean", "environment", "biology", "species", "health", "disease", "covid", "chemistry", "physics"],
    "social": ["population", "country", "census", "transport", "traffic", "city", "school", "education", "economy", "bank", "currency", "government"],
    "data": ["csv", "json", "time", "historical", "statistics", "open data", "public data", "dataset"],
}


def download() -> str:
    RAW.mkdir(parents=True, exist_ok=True)
    r = requests.get(SOURCE_URL, timeout=60, headers={"User-Agent": "free-api-data-science-edu-audit/0.1"})
    r.raise_for_status()
    path = RAW / "README.md"
    path.write_text(r.text, encoding="utf-8")
    return r.text


def parse_public_apis(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    category = ""
    for line in text.splitlines():
        m = re.match(r"^###\s+(.+)", line)
        if m:
            category = m.group(1).strip()
            continue
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 5 or cells[0].lower() in {"api", "apis"}:
            continue
        api, desc, auth, https, cors = cells[:5]
        link_match = re.search(r"\[([^\]]+)\]\(([^)]+)\)", api)
        name = link_match.group(1).strip() if link_match else re.sub(r"<[^>]+>", "", api).strip()
        url = link_match.group(2).strip() if link_match else ""
        rows.append({
            "category": category,
            "name": name,
            "url": url,
            "description": re.sub(r"<[^>]+>", "", desc).strip(),
            "auth": auth,
            "https": https,
            "cors": cors,
        })
    return rows


def score(row: dict[str, str]) -> int:
    hay = " ".join([row["category"], row["name"], row["description"]]).lower()
    total = 0
    for words in EDU_KEYWORDS.values():
        if any(w in hay for w in words):
            total += 2
    if row["auth"].lower() in {"no", ""} or "no" in row["auth"].lower():
        total += 1
    if "yes" in row["https"].lower():
        total += 1
    return total


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--use-cache", action="store_true", help="Use raw/public-apis/README.md if present")
    args = parser.parse_args()

    cached = RAW / "README.md"
    text = cached.read_text(encoding="utf-8") if args.use_cache and cached.exists() else download()
    rows = parse_public_apis(text)
    candidates = sorted(({**r, "education_score": score(r)} for r in rows if score(r) >= 3), key=lambda r: (-r["education_score"], r["category"], r["name"]))

    write_csv(AUDITS / "public_apis_catalog.csv", rows, ["category", "name", "url", "description", "auth", "https", "cors"])
    write_csv(AUDITS / "public_apis_education_candidates.csv", candidates, ["education_score", "category", "name", "url", "description", "auth", "https", "cors"])

    categories = sorted({r["category"] for r in rows})
    summary = [
        "# public-apis 검토 기록",
        "",
        f"원본: {SOURCE_URL}",
        f"전체 항목: {len(rows)}개",
        f"카테고리: {len(categories)}개",
        f"교육 후보 1차 필터: {len(candidates)}개",
        "",
        "## 산출물",
        "",
        "- `audits/public_apis_catalog.csv`: public-apis 전체 항목을 한 줄씩 파싱한 목록",
        "- `audits/public_apis_education_candidates.csv`: 초·중·고 정보/데이터 과학 수업 후보 1차 필터",
        "",
        "## 1차 필터 기준",
        "",
        "- 과학/환경/보건/우주/지리/교통/경제/통계/공공데이터 키워드",
        "- 인증 불필요 또는 낮은 인증 부담",
        "- HTTPS 지원",
        "",
        "## 다음 단계",
        "",
        "1. 후보를 공식 문서/테스트 URL 기준으로 하나씩 확인",
        "2. no-auth + JSON/CORS 가능 + 교육 적합 후보 우선 반영",
        "3. 최근 5년치 CSV 자동화가 가능한 후보는 `scripts/update_datasets.py`에 추가",
        "4. GitHub Pages에 CSV 직접 로드 + 시각화 + Streamlit 예제 제공",
        "",
        "## 상위 후보 예시",
        "",
    ]
    for r in candidates[:30]:
        summary.append(f"- {r['name']} ({r['category']}, score={r['education_score']}, auth={r['auth']}) — {r['url']}")
    (AUDITS / "public-apis-review.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print({"total": len(rows), "categories": len(categories), "education_candidates": len(candidates)})


if __name__ == "__main__":
    main()
