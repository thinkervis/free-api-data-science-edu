from __future__ import annotations

import csv
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"
DOC_DATA = DOCS / "data"
DATASET_PAGES = DOCS / "datasets"

DATASETS = [
    {
        "id": "open-meteo-weather",
        "title": "서울 5년 일별 기상",
        "category": "기상",
        "csv": "open_meteo_seoul_daily_weather.csv",
        "source": "Open-Meteo Historical Weather API",
        "doc_url": "https://open-meteo.com/en/docs/historical-weather-api",
        "test_url": "https://archive-api.open-meteo.com/v1/archive?latitude=37.5665&longitude=126.9780&start_date=2021-01-01&end_date=2021-01-03&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=Asia%2FSeoul",
        "auth": "불필요",
        "pico": "높음",
        "streamlit": "높음",
        "note": "최근 5년치 CSV 기본 제공, --scope all로 가능한 전체 기간 요청 가능",
    },
    {
        "id": "open-meteo-air-quality",
        "title": "서울 5년 시간별 대기질",
        "category": "기상/환경",
        "csv": "open_meteo_seoul_air_quality_hourly.csv",
        "source": "Open-Meteo Air Quality API",
        "doc_url": "https://open-meteo.com/en/docs/air-quality-api",
        "test_url": "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=37.5665&longitude=126.9780&hourly=pm10,pm2_5&start_date=2021-01-01&end_date=2021-01-03&timezone=Asia%2FSeoul",
        "auth": "불필요",
        "pico": "중간",
        "streamlit": "높음",
        "note": "시간별 데이터라 CSV가 큼. Pico W는 최근 몇 줄만 쓰는 예제로 권장",
    },
    {
        "id": "worldbank-korea",
        "title": "한국 5년 World Bank 지표",
        "category": "인구/경제/교육/보건",
        "csv": "worldbank_korea_indicators.csv",
        "source": "World Bank Indicators API",
        "doc_url": "https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation",
        "test_url": "https://api.worldbank.org/v2/country/KOR/indicator/SP.POP.TOTL?format=json&date=2021:2025",
        "auth": "불필요",
        "pico": "중간",
        "streamlit": "높음",
        "note": "인구/GDP/기대수명/중등교육 등록률 포함",
    },
    {
        "id": "usgs-earthquakes",
        "title": "전세계 규모 6+ 지진 5년",
        "category": "지질/지도",
        "csv": "usgs_major_earthquakes.csv",
        "source": "USGS Earthquake API",
        "doc_url": "https://earthquake.usgs.gov/fdsnws/event/1/",
        "test_url": "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2021-01-01&endtime=2021-01-31&minmagnitude=6",
        "auth": "불필요",
        "pico": "중간",
        "streamlit": "높음",
        "note": "지도 시각화/GeoJSON 수업에 적합",
    },
    {
        "id": "mlb-schedule",
        "title": "MLB 경기 일정/결과 5년",
        "category": "야구/스포츠",
        "csv": "mlb_schedule.csv",
        "source": "MLB Stats API",
        "doc_url": "https://github.com/toddrob99/MLB-StatsAPI/wiki",
        "test_url": "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2024-03-28",
        "auth": "불필요",
        "pico": "중간",
        "streamlit": "높음",
        "note": "스코어보드, 승률, 팀별 득점 분석 가능",
    },
    {
        "id": "fred-fedfunds",
        "title": "미국 기준금리 5년",
        "category": "경제/금융",
        "csv": "fred_fedfunds.csv",
        "source": "FRED CSV",
        "doc_url": "https://fred.stlouisfed.org/docs/api/fred/",
        "test_url": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS&cosd=2021-01-01&coed=2026-05-15",
        "auth": "CSV 다운로드는 불필요 / 정식 API는 키 필요",
        "pico": "중간",
        "streamlit": "높음",
        "note": "CSV 엔드포인트로 금리 시계열을 바로 읽을 수 있음",
    },
    {
        "id": "owid-co2",
        "title": "한국/세계 CO₂ 배출량",
        "category": "환경/에너지",
        "csv": "owid_co2_korea_world.csv",
        "source": "Our World in Data Grapher CSV",
        "doc_url": "https://docs.owid.io/projects/etl/api/",
        "test_url": "https://ourworldindata.org/grapher/annual-co2-emissions-per-country.csv",
        "auth": "불필요",
        "pico": "낮음",
        "streamlit": "높음",
        "note": "기본은 최근 5년, --scope all로 전체 역사 범위 필터 가능",
    },
    {
        "id": "gbif-korea",
        "title": "한국 생물종 관측 샘플",
        "category": "생태/생물다양성",
        "csv": "gbif_korea_occurrences_sample.csv",
        "source": "GBIF Occurrence API",
        "doc_url": "https://techdocs.gbif.org/en/openapi/",
        "test_url": "https://api.gbif.org/v1/occurrence/search?country=KR&limit=3",
        "auth": "불필요",
        "pico": "낮음~중간",
        "streamlit": "높음",
        "note": "위치 기반 생물종 관측 지도 샘플. 기본 300건 제한",
    },
    {
        "id": "artic-artworks",
        "title": "최근 5년 미술 작품 샘플",
        "category": "문화/예술",
        "csv": "artic_recent_artworks_sample.csv",
        "source": "Art Institute of Chicago API",
        "doc_url": "https://api.artic.edu/docs/",
        "test_url": "https://api.artic.edu/api/v1/artworks/search?q=monet&fields=id,title,artist_title,date_display&limit=3",
        "auth": "불필요",
        "pico": "중간",
        "streamlit": "높음",
        "note": "문화 데이터 검색/분류/카드 UI 예제로 적합",
    },
    {
        "id": "seoul-bike",
        "title": "서울 따릉이 샘플",
        "category": "대중교통/도시",
        "csv": "seoul_bike_sample.csv",
        "source": "서울 열린데이터광장",
        "doc_url": "https://data.seoul.go.kr/",
        "test_url": "http://openapi.seoul.go.kr:8088/sample/json/bikeList/1/5/",
        "auth": "샘플키 가능 / 정식은 무료 키 권장",
        "pico": "중간",
        "streamlit": "높음",
        "note": "샘플키는 5건 제한. 정식키로 전체 대여소 자동화 가능",
    },
    {
        "id": "nasa-power-seoul",
        "title": "NASA POWER 서울 일별 기상/에너지",
        "category": "기상/에너지/과학",
        "csv": "nasa_power_seoul_daily.csv",
        "source": "NASA POWER Daily API",
        "doc_url": "https://power.larc.nasa.gov/docs/services/api/",
        "test_url": "https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,PRECTOTCORR&community=RE&longitude=126.9780&latitude=37.5665&start=20210101&end=20210105&format=JSON",
        "auth": "불필요",
        "pico": "중간",
        "streamlit": "높음",
        "note": "public-apis 확장 후보에서 승격. 최근 5년치 기본, --scope all은 NASA POWER 일별 제공 시작 시점부터 요청",
    },
    {
        "id": "bls-us-cpi",
        "title": "미국 소비자물가지수 CPI 월별",
        "category": "경제/통계",
        "csv": "bls_us_cpi_monthly.csv",
        "source": "U.S. Bureau of Labor Statistics Public API",
        "doc_url": "https://www.bls.gov/developers/api_signature_v2.htm",
        "test_url": "https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0?startyear=2021&endyear=2025",
        "auth": "제한 내 불필요 / 대량 사용은 무료 키 권장",
        "pico": "중간",
        "streamlit": "높음",
        "note": "물가/인플레이션 수업용 월별 시계열. --scope all은 공개 API 제한을 고려해 2005년 이후로 제한",
    },
    {
        "id": "nager-korea-holidays",
        "title": "한국 공휴일 5년",
        "category": "달력/사회/문화",
        "csv": "nager_korea_public_holidays.csv",
        "source": "Nager.Date Public Holiday API",
        "doc_url": "https://date.nager.at/Api",
        "test_url": "https://date.nager.at/api/v3/PublicHolidays/2024/KR",
        "auth": "불필요",
        "pico": "높음",
        "streamlit": "높음",
        "note": "날짜/캘린더/지역 문화 수업에 적합. --scope all은 1970년 이후 연도별 조회",
    },
    {
        "id": "spacex-launches",
        "title": "SpaceX 발사 기록",
        "category": "우주/과학",
        "csv": "spacex_launches.csv",
        "source": "SpaceX API v5",
        "doc_url": "https://github.com/r-spacex/SpaceX-API/tree/master/docs",
        "test_url": "https://api.spacexdata.com/v5/launches/latest",
        "auth": "불필요",
        "pico": "중간",
        "streamlit": "높음",
        "note": "최근 5년 발사 기록 기본. POST query로 기간 필터링하며 Pages에서는 CSV→JSON 변환/시각화 제공",
    },
    {
        "id": "frankfurter-usd-krw",
        "title": "USD/KRW 환율 일별",
        "category": "경제/환율",
        "csv": "frankfurter_usd_krw_daily.csv",
        "source": "Frankfurter Exchange Rates API",
        "doc_url": "https://www.frankfurter.app/docs/",
        "test_url": "https://api.frankfurter.app/2021-01-01..2021-01-05?from=USD&to=KRW",
        "auth": "불필요",
        "pico": "중간",
        "streamlit": "높음",
        "note": "환율 시계열/변화율 수업용. --scope all은 API 제공 시작 시점 이후",
    },
    {
        "id": "who-korea-life-expectancy",
        "title": "WHO 한국 기대수명",
        "category": "보건/국제통계",
        "csv": "who_korea_life_expectancy.csv",
        "source": "WHO Global Health Observatory API",
        "doc_url": "https://www.who.int/data/gho/info/gho-odata-api",
        "test_url": "https://ghoapi.azureedge.net/api/WHOSIS_000001?$filter=SpatialDim%20eq%20%27KOR%27&$top=5",
        "auth": "불필요",
        "pico": "중간",
        "streamlit": "높음",
        "note": "보건/인구/국제비교 수업용. 최근 5년 범위에 값이 적을 수 있어 WHO 제공 연도 기준으로 검증",
    },
    {
        "id": "restcountries-world",
        "title": "세계 국가 기본 정보 스냅샷",
        "category": "지리/국가/인구",
        "csv": "restcountries_world_snapshot.csv",
        "source": "REST Countries API",
        "doc_url": "https://restcountries.com/",
        "test_url": "https://restcountries.com/v3.1/all?fields=name,cca3,region,population,area,latlng",
        "auth": "불필요",
        "pico": "중간",
        "streamlit": "높음",
        "note": "시계열이 아닌 현재 스냅샷 데이터. 국가별 인구/면적/지역 비교와 지도 수업용",
    },
    {
        "id": "eia-california-electricity",
        "title": "EIA 캘리포니아 전력 일별",
        "category": "에너지/전력/환경",
        "csv": "eia_california_electricity_daily.csv",
        "source": "U.S. EIA Open Data API",
        "doc_url": "https://www.eia.gov/opendata/documentation.php",
        "test_url": "https://api.eia.gov/v2/electricity/rto/daily-region-data/data/?frequency=daily&data[0]=value&facets[respondent][]=CAL&start=2021-01-01&end=2021-01-05&sort[0][column]=period&sort[0][direction]=asc&api_key=DEMO_KEY",
        "auth": "DEMO_KEY 가능 / 안정 사용은 무료 키 권장",
        "pico": "중간",
        "streamlit": "높음",
        "note": "전력 수요/공급/에너지 데이터 수업용. DEMO_KEY 제한을 명시하고 무료 키 사용 권장",
    },

]

MORE_CANDIDATES = [
    ["NASA POWER", "기상/태양광/에너지", "불필요", "https://power.larc.nasa.gov/docs/services/api/"],
    ["NOAA CO-OPS", "해양/조위/기상", "불필요", "https://api.tidesandcurrents.noaa.gov/api/prod/"],
    ["U.S. Census ACS 5-Year", "인구/교육/소득", "키 선택", "https://www.census.gov/data/developers/data-sets/acs-5year.html"],
    ["BLS Public Data", "노동/물가", "제한 내 불필요", "https://www.bls.gov/developers/api_signature_v2.htm"],
    ["WHO GHO", "보건", "불필요", "https://ghoapi.azureedge.net/api"],
    ["CDC/Socrata", "보건/공공데이터", "토큰 선택", "https://dev.socrata.com/"],
    ["GB Carbon Intensity", "에너지/탄소", "불필요", "https://carbon-intensity.github.io/api-definitions/"],
    ["EIA Open Data", "에너지", "무료 키", "https://www.eia.gov/opendata/documentation.php"],
    ["서울 실시간 도시데이터", "유동인구/도시", "샘플키/무료키", "https://data.seoul.go.kr/dataList/OA-21285/S/1/datasetView.do"],
    ["서울 생활인구", "유동인구", "파일 다운로드", "https://data.seoul.go.kr/dataList/OA-14991/S/1/datasetView.do"],
    ["서울 지하철 승하차", "대중교통", "파일 다운로드", "https://data.seoul.go.kr/dataList/OA-12914/S/1/datasetView.do"],
    ["서울 시간별 대기질", "대기질", "샘플키/무료키", "https://data.seoul.go.kr/"],
    ["Korea TourAPI", "관광/문화", "공공데이터 키", "https://api.visitkorea.or.kr/"],
    ["KOSIS", "한국 인구통계", "무료 키", "https://kosis.kr/openapi/index/index.jsp"],
    ["한국은행 ECOS", "경제/금융", "무료 키", "https://ecos.bok.or.kr/api/#/"],
    ["TMDB", "영화", "회원가입+키", "https://developer.themoviedb.org/docs/getting-started"],
    ["OMDb", "영화", "키", "https://www.omdbapi.com/"],
    ["IMDb Non-Commercial Datasets", "영화", "불필요/비상업 약관", "https://developer.imdb.com/non-commercial-datasets/"],
    ["Met Museum Collection", "문화/예술", "불필요", "https://metmuseum.github.io/"],
    ["Nominatim", "지도", "불필요/정책 준수", "https://nominatim.org/release-docs/latest/api/Overview/"],
    ["Overpass API", "지도/POI", "불필요/정책 준수", "https://wiki.openstreetmap.org/wiki/Overpass_API"],
    ["Kakao Local", "한국 지도", "회원가입+키", "https://developers.kakao.com/docs/latest/ko/local/dev-guide"],
    ["Google Maps", "지도", "키+결제 가능성", "https://developers.google.com/maps/documentation/javascript/get-api-key"],
    ["Citi Bike System Data", "자전거/대중교통", "불필요", "https://www.citibikenyc.com/system-data"],
    ["Alpha Vantage", "주식", "키", "https://www.alphavantage.co/documentation/"],
    ["FMP", "주식/재무", "회원가입+키", "https://site.financialmodelingprep.com/developer/docs"],
    ["Finnhub", "주식", "회원가입+키", "https://finnhub.io/docs/api"],
    ["금융위원회 주식시세", "한국 주식", "공공데이터포털 키", "https://www.data.go.kr/data/15094808/openapi.do"],
    ["기상청 단기예보", "한국 기상", "공공데이터포털 키", "https://www.data.go.kr/data/15084084/openapi.do"],
    ["Retrosheet", "야구", "불필요", "https://www.retrosheet.org/game.htm"],
]


def read_preview(csv_name: str, max_rows: int = 5) -> tuple[list[str], list[list[str]], int]:
    path = DATA / csv_name
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return [], [], 0
    return rows[0], rows[1 : max_rows + 1], max(0, len(rows) - 1)


def streamlit_code(csv_name: str) -> str:
    return f'''import pandas as pd\nimport streamlit as st\n\nURL = "https://thinkervis.github.io/free-api-data-science-edu/data/{csv_name}"\n\nst.title("{csv_name}")\ndf = pd.read_csv(URL)\nst.write(df.shape)\nst.dataframe(df.head(100))\n\n# 숫자 컬럼이 있으면 빠르게 차트 확인\nnum_cols = df.select_dtypes("number").columns.tolist()\nif num_cols:\n    st.line_chart(df[num_cols[:3]])\n'''


def pico_code(csv_name: str) -> str:
    return f'''# Raspberry Pi Pico W / MicroPython basic CSV fetch\nimport network, urequests, time\n\nSSID = "YOUR_WIFI"\nPASSWORD = "YOUR_PASSWORD"\nURL = "https://thinkervis.github.io/free-api-data-science-edu/data/{csv_name}"\n\nwlan = network.WLAN(network.STA_IF)\nwlan.active(True)\nwlan.connect(SSID, PASSWORD)\nwhile not wlan.isconnected():\n    time.sleep(1)\n\nr = urequests.get(URL)\ntext = r.text\nr.close()\n\n# 메모리 보호: 앞부분만 확인\nlines = text.split("\\n")[:6]\nfor line in lines:\n    print(line)\n'''


def html_table(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in row) + "</tr>" for row in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def layout(title: str, body: str) -> str:
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 2rem; line-height: 1.6; max-width: 1120px; }}
a {{ color: #0969da; }}
.card {{ border: 1px solid #d0d7de; border-radius: 12px; padding: 1rem; margin: 1rem 0; }}
table {{ border-collapse: collapse; width: 100%; overflow-x: auto; display: block; }}
th, td {{ border: 1px solid #d0d7de; padding: .4rem .6rem; font-size: .9rem; }}
th {{ background: #f6f8fa; }}
pre {{ background: #f6f8fa; padding: 1rem; overflow-x: auto; border-radius: 8px; }}
.badge {{ display: inline-block; background: #eef; border-radius: 999px; padding: .15rem .55rem; margin-right: .25rem; }}
button {{ padding: .5rem .8rem; border-radius: 8px; border: 1px solid #d0d7de; background: white; cursor: pointer; }}
</style>
</head>
<body>
{body}
</body>
</html>'''


def dataset_page(ds: dict[str, str]) -> str:
    headers, rows, count = read_preview(ds["csv"])
    preview = html_table(headers, rows)
    csv_url = f"../data/{ds['csv']}"
    body = f'''
<p><a href="../index.html">← 전체 목록</a></p>
<h1>{html.escape(ds['title'])}</h1>
<p><span class="badge">{html.escape(ds['category'])}</span><span class="badge">인증: {html.escape(ds['auth'])}</span><span class="badge">행 수: {count}</span></p>
<div class="card">
  <p><b>원천:</b> {html.escape(ds['source'])}</p>
  <p><b>설명:</b> {html.escape(ds['note'])}</p>
  <p><a href="{html.escape(csv_url)}">CSV 직접 열기</a> · <a href="{html.escape(ds['test_url'])}">원천 API/CSV 직접 테스트</a> · <a href="{html.escape(ds['doc_url'])}">공식 문서</a></p>
  <button onclick="testCsvJsonAndChart('{html.escape(csv_url)}')">GitHub Pages에서 JSON 변환 + 시각화 테스트</button>
  <pre id="test-output">버튼을 누르면 이 페이지에서 CSV를 fetch한 뒤 JSON으로 변환하고, 숫자 컬럼을 자동 시각화합니다.</pre>
  <div id="chart" aria-label="브라우저 직접 시각화 결과"></div>
</div>
<h2>CSV 미리보기</h2>
{preview}
<h2>Streamlit 기본 코드</h2>
<pre>{html.escape(streamlit_code(ds['csv']))}</pre>
<h2>Pico W 기본 코드</h2>
<pre>{html.escape(pico_code(ds['csv']))}</pre>
<script>
function parseCsv(text) {{
  const rows = text.trim().split(/\r?\n/).map(line => line.split(','));
  const headers = rows.shift() || [];
  return rows.filter(r => r.length).map(row => Object.fromEntries(headers.map((h, i) => [h, row[i] ?? ''])));
}}

function drawChart(data) {{
  const chart = document.getElementById('chart');
  const keys = Object.keys(data[0] || {{}});
  const numericKey = keys.find(k => data.some(row => Number.isFinite(Number(row[k]))));
  if (!numericKey) {{
    chart.innerHTML = '<p>숫자 컬럼을 찾지 못해 시각화를 생략했습니다.</p>';
    return;
  }}
  const values = data.slice(0, 80).map(row => Number(row[numericKey])).filter(Number.isFinite);
  const width = 760, height = 260, pad = 30;
  const min = Math.min(...values), max = Math.max(...values);
  const range = max - min || 1;
  const points = values.map((v, i) => {{
    const x = pad + i * ((width - pad * 2) / Math.max(1, values.length - 1));
    const y = height - pad - ((v - min) / range) * (height - pad * 2);
    return `${{x.toFixed(1)}},${{y.toFixed(1)}}`;
  }}).join(' ');
  chart.innerHTML = `<h3>브라우저 직접 시각화: ${{numericKey}}</h3>
  <svg viewBox="0 0 ${{width}} ${{height}}" role="img" aria-label="${{numericKey}} line chart" style="max-width:100%;border:1px solid #d0d7de;border-radius:8px;background:#fff">
    <line x1="${{pad}}" y1="${{height-pad}}" x2="${{width-pad}}" y2="${{height-pad}}" stroke="#888"/>
    <line x1="${{pad}}" y1="${{pad}}" x2="${{pad}}" y2="${{height-pad}}" stroke="#888"/>
    <polyline fill="none" stroke="#0969da" stroke-width="2" points="${{points}}"/>
    <text x="${{pad}}" y="18" font-size="12">max=${{max}}</text>
    <text x="${{pad}}" y="${{height-8}}" font-size="12">min=${{min}}</text>
  </svg>`;
}}

async function testCsvJsonAndChart(url) {{
  const out = document.getElementById('test-output');
  try {{
    const r = await fetch(url);
    const text = await r.text();
    const jsonRows = parseCsv(text);
    drawChart(jsonRows);
    out.textContent = `status=${{r.status}} bytes=${{text.length}} json_rows=${{jsonRows.length}}\nJSON sample:\n` + JSON.stringify(jsonRows.slice(0, 3), null, 2);
  }} catch (e) {{
    out.textContent = 'ERROR: ' + e;
  }}
}}
</script>
'''
    return layout(ds["title"], body)


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    DOC_DATA.mkdir(parents=True, exist_ok=True)
    DATASET_PAGES.mkdir(parents=True, exist_ok=True)

    for csv_file in DATA.glob("*.csv"):
        shutil.copy2(csv_file, DOC_DATA / csv_file.name)
    if (DATA / "manifest.json").exists():
        shutil.copy2(DATA / "manifest.json", DOC_DATA / "manifest.json")

    cards = []
    for ds in DATASETS:
        headers, _, count = read_preview(ds["csv"])
        page_path = DATASET_PAGES / f"{ds['id']}.html"
        page_path.write_text(dataset_page(ds), encoding="utf-8")
        cards.append(f'''
<div class="card">
  <h2><a href="datasets/{ds['id']}.html">{html.escape(ds['title'])}</a></h2>
  <p><span class="badge">{html.escape(ds['category'])}</span><span class="badge">{html.escape(ds['auth'])}</span><span class="badge">{count} rows</span></p>
  <p>{html.escape(ds['note'])}</p>
  <p><a href="data/{html.escape(ds['csv'])}">CSV</a> · <a href="{html.escape(ds['test_url'])}">직접 테스트</a> · <a href="{html.escape(ds['doc_url'])}">공식 문서</a></p>
</div>''')

    more_rows = "".join(f"<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td><td>{html.escape(c)}</td><td><a href='{html.escape(d)}'>문서</a></td></tr>" for a, b, c, d in MORE_CANDIDATES)
    index = f'''
<h1>초·중·고 정보 교육을 위한 무료 데이터 과학 API & CSV</h1>
<p>모든 기본 CSV는 최근 5년치 중심으로 생성되며, <code>python3 scripts/update_datasets.py --scope all</code>로 가능한 전체 기간을 받을 수 있습니다.</p>
<p>데이터별 페이지에서 CSV→JSON 직접 테스트, 원천 API 테스트, 브라우저 시각화, Streamlit 기본 코드, Pico W 기본 코드를 제공합니다.</p>
<p><a href="data/manifest.json">갱신 manifest</a> · <a href="https://github.com/thinkervis/free-api-data-science-edu">GitHub repo</a> · <a href="https://github.com/thinkervis/free-api-data-science-edu/blob/main/CONTRIBUTING.md">사람용 기여 안내</a> · <a href="https://github.com/thinkervis/free-api-data-science-edu/blob/main/AI_CONTRIBUTING.md">AI용 기여 안내</a> · <a href="https://github.com/thinkervis/free-api-data-science-edu/blob/main/REWARDS.md">리워드 설계</a></p>
<h2>바로 테스트 가능한 데이터셋</h2>
{''.join(cards)}
<h2>추가 API 후보</h2>
<table><thead><tr><th>이름</th><th>분야</th><th>인증</th><th>공식 문서</th></tr></thead><tbody>{more_rows}</tbody></table>
'''
    (DOCS / "index.html").write_text(layout("무료 데이터 과학 교육 API & CSV", index), encoding="utf-8")
    (DOCS / "datasets.json").write_text(json.dumps(DATASETS, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"generated {DOCS}")


if __name__ == "__main__":
    main()
