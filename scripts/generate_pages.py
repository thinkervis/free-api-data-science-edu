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
        "note": "시간별 데이터라 CSV가 큼. Pico 2 WH + Grove Shield에서는 최근 몇 줄만 쓰는 예제로 권장",
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
        "id": "factfulness-global",
        "title": "팩트풀니스 세계 지표 최신화",
        "category": "SDG/세계시민/데이터 리터러시",
        "csv": "factfulness_global_indicators.csv",
        "source": "World Bank Indicators API",
        "doc_url": "https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation",
        "test_url": "https://api.worldbank.org/v2/country/KOR;USA;CHN;IND;BRA;NGA;SWE;WLD/indicator/SP.DYN.LE00.IN?format=json&per_page=20&date=2021:2026",
        "auth": "불필요",
        "pico": "중간",
        "streamlit": "높음",
        "note": "팩트풀니스 수업용: 기대수명, 5세 미만 사망률, 전기 접근성, 1인당 GDP, 초등교육 이수율을 최신 World Bank 데이터로 다시 확인",
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
        "note": "최근 5년 발사 기록 기본. POST query로 기간 필터링하며 Pages에서는 CSV 직접 로드/시각화 제공",
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

RECOMMENDED_CANDIDATE_IDS = [
    "open-meteo-weather", "open-meteo-air-quality", "nasa-power-seoul", "usgs-earthquakes", "frankfurter-usd-krw",
    "worldbank-korea", "restcountries-world", "nager-korea-holidays", "spacex-launches", "gbif-korea",
]

RECOMMENDED_CANDIDATE_REASONS = {
    "open-meteo-weather": "날씨 시계열·그래프·평균/최댓값 비교 수업에 가장 쉽게 활용",
    "open-meteo-air-quality": "미세먼지와 환경 데이터 탐구에 적합",
    "nasa-power-seoul": "NASA 공식 데이터로 기상·에너지·태양광 주제 연결 가능",
    "usgs-earthquakes": "GeoJSON/지도/지구과학 융합 수업에 좋음",
    "frankfurter-usd-krw": "환율 변화와 경제 시계열 분석 입문에 적합",
    "worldbank-korea": "인구·GDP·기대수명·교육 지표를 함께 비교 가능",
    "restcountries-world": "국가별 인구·면적·위치 데이터로 지도/비교 활동 가능",
    "nager-korea-holidays": "날짜·달력·문화 데이터를 다루기 쉬워 초급 수업에 좋음",
    "spacex-launches": "우주/과학 흥미도가 높고 성공 여부·발사 횟수 분석 가능",
    "gbif-korea": "한국 안의 생물다양성·위치 데이터·생태 탐구 프로젝트에 적합",
}

VIZ_CONFIG = {
    "open-meteo-weather": {"kind": "line", "title": "최고·평균·최저 기온 3종 세트", "x": "time", "y": ["temperature_2m_max", "temperature_2m_mean", "temperature_2m_min"], "labels": ["최고기온", "평균기온", "최저기온"], "y_title": "기온(°C)"},
    "open-meteo-air-quality": {"kind": "line", "title": "PM10·PM2.5 시간별 변화", "x": "time", "y": ["pm10", "pm2_5"], "labels": ["PM10", "PM2.5"], "y_title": "㎍/m³", "max_points": 500},
    "nasa-power-seoul": {"kind": "line", "title": "NASA 기온·강수·풍속 비교", "x": "date", "y": ["temperature_2m_c", "precipitation_mm_day", "wind_speed_2m_m_s"], "labels": ["평균기온(°C)", "강수량(mm/day)", "풍속(m/s)"], "axes": ["y", "y2", "y3"], "invalid_below": -900},
    "usgs-earthquakes": {"kind": "scattergeo", "title": "규모 6 이상 지진 위치와 규모", "lat": "latitude", "lon": "longitude", "size": "magnitude", "color": "depth_km", "hover": "place"},
    "frankfurter-usd-krw": {"kind": "line", "title": "USD/KRW 환율 변화", "x": "date", "y": ["rate"], "labels": ["환율(KRW)"]},
    "fred-fedfunds": {"kind": "line", "title": "미국 기준금리 변화", "x": "observation_date", "y": ["FEDFUNDS"], "labels": ["FEDFUNDS(%)"]},
    "bls-us-cpi": {"kind": "line", "title": "미국 CPI 월별 변화", "x": "date", "y": ["cpi_value"], "labels": ["CPI"]},
    "worldbank-korea": {"kind": "multiCategoryLine", "title": "한국 주요 지표 변화율 비교(첫해=100)", "x": "date", "y": "value", "category": "indicator", "indexed": True, "y_title": "첫 관측연도=100"},
    "factfulness-global": {"kind": "factfulnessLong", "title": "팩트풀니스: 기대수명 장기 변화(1960년대~현재)", "indicator_id": "SP.DYN.LE00.IN"},
    "owid-co2": {"kind": "multiCategoryLine", "title": "한국과 세계 CO₂ 배출량 비교(로그 축)", "x": "Year", "y": "Annual CO₂ emissions", "category": "Entity", "log_y": True},
    "gbif-korea": {"kind": "scattergeo", "title": "한국 생물종 관측 위치", "lat": "decimalLatitude", "lon": "decimalLongitude", "hover": "scientificName", "geo_scope": "korea"},
    "artic-artworks": {"kind": "histogram", "title": "작품 제작 연도 분포", "x": "date_end"},
    "seoul-bike": {"kind": "bar", "title": "따릉이 대여소별 주차 자전거 수", "x": "stationName", "y": "parkingBikeTotCnt"},
    "mlb-schedule": {"kind": "barAggregate", "title": "홈팀별 경기 수", "x": "home_team"},
    "nager-korea-holidays": {"kind": "barAggregate", "title": "연도별 한국 공휴일 수", "x_date_year": "date"},
    "spacex-launches": {"kind": "barAggregate", "title": "연도별 SpaceX 발사 횟수", "x_date_year": "date_utc"},
    "who-korea-life-expectancy": {"kind": "bar", "title": "성별 기대수명 비교", "x": "sex", "y": "value"},
    "restcountries-world": {"kind": "scatter", "title": "국가별 면적과 인구 관계", "x": "area", "y": "population", "text": "name", "x_title": "면적", "y_title": "인구"},
    "eia-california-electricity": {"kind": "multiCategoryLine", "title": "캘리포니아 전력 데이터 유형별 변화", "x": "date", "y": "value", "category": "type_name", "max_points": 1000},
}

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

SDG_TOPICS = [
    {
        "title": "우리 동네 미세먼지와 건강한 생활권",
        "sdg": "SDG 3 건강과 웰빙 · SDG 11 지속가능한 도시",
        "data": "Open-Meteo Air Quality / 서울 시간별 대기질",
        "url": "https://open-meteo.com/en/docs/air-quality-api",
        "auth": "불필요",
        "activity": "PM10·PM2.5 시간별 변화를 보고 등하교/야외활동 안내 대시보드 만들기",
    },
    {
        "title": "폭염일·열대야와 학교 에너지 사용",
        "sdg": "SDG 7 깨끗한 에너지 · SDG 13 기후행동",
        "data": "NASA POWER 서울 일별 기상/에너지",
        "url": "https://power.larc.nasa.gov/docs/services/api/",
        "auth": "불필요",
        "activity": "기온·강수·풍속을 분석해 폭염 경보 기준과 냉방 에너지 절약 캠페인 설계",
    },
    {
        "title": "한국과 세계의 CO₂ 배출 변화",
        "sdg": "SDG 12 책임 있는 소비와 생산 · SDG 13 기후행동",
        "data": "Our World in Data CO₂ Grapher CSV",
        "url": "https://docs.owid.io/projects/etl/api/",
        "auth": "불필요",
        "activity": "한국/세계 CO₂ 배출량을 비교하고 1인당 감축 아이디어를 데이터 근거로 제안",
    },
    {
        "title": "생물다양성 관측으로 보는 우리 주변 생태계",
        "sdg": "SDG 14 해양생태계 · SDG 15 육상생태계",
        "data": "GBIF 한국 생물종 관측",
        "url": "https://techdocs.gbif.org/en/openapi/",
        "auth": "불필요",
        "activity": "한국 지도 위 관측 위치를 찍고 도시/해안/산림별 생물종 관측 차이 탐구",
    },
    {
        "title": "따릉이와 탄소 줄이는 통학·이동",
        "sdg": "SDG 9 산업·혁신·인프라 · SDG 11 지속가능한 도시",
        "data": "서울 열린데이터광장 따릉이 실시간 대여정보",
        "url": "https://data.seoul.go.kr/",
        "auth": "샘플키 가능 / 정식은 무료 키 권장",
        "activity": "대여소별 자전거 수를 시각화하고 짧은 거리 자동차 이동 대체 효과 추정",
    },
    {
        "title": "도시 혼잡도와 안전한 공공공간",
        "sdg": "SDG 10 불평등 감소 · SDG 11 지속가능한 도시",
        "data": "서울 실시간 도시데이터",
        "url": "https://data.seoul.go.kr/dataList/OA-21285/S/1/datasetView.do",
        "auth": "샘플키/무료키",
        "activity": "주요 장소 혼잡도를 비교해 안전한 방문 시간 추천 또는 행사 운영 아이디어 만들기",
    },
    {
        "title": "인구·교육·경제 지표로 보는 지속가능한 사회",
        "sdg": "SDG 4 양질의 교육 · SDG 8 양질의 일자리와 경제성장",
        "data": "World Bank 한국 지표",
        "url": "https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation",
        "auth": "불필요",
        "activity": "인구·GDP·기대수명·교육 지표를 함께 보고 지속가능발전 지표 카드 만들기",
    },
    {
        "title": "팩트풀니스 데이터 최신화: 오래된 상식 검증",
        "sdg": "SDG 1 빈곤 종식 · SDG 3 건강과 웰빙 · SDG 4 양질의 교육 · SDG 7 깨끗한 에너지",
        "data": "World Bank 최신 세계 지표 CSV: 기대수명, 5세 미만 사망률, 전기 접근성, 1인당 GDP, 초등교육 이수율",
        "url": "https://www.gapminder.org/data/",
        "auth": "불필요",
        "activity": "학생 예상값을 먼저 적고 최신 데이터와 비교해 '세상은 생각보다 어떻게 달라졌나'를 시각화",
    },
    {
        "title": "물 사용량과 가뭄·절수 행동 데이터",
        "sdg": "SDG 6 깨끗한 물과 위생 · SDG 12 책임 있는 소비와 생산",
        "data": "공공데이터포털/지자체 상수도 사용량·수질·가뭄 관련 데이터",
        "url": "https://www.data.go.kr/",
        "auth": "데이터별 상이: 파일 다운로드 또는 공공데이터포털 키",
        "activity": "지역별 물 사용량·강수량·가뭄 정보를 비교하고 학교/가정 절수 캠페인 근거 만들기",
    },
    {
        "title": "전력 수요와 재생에너지 전환 토론",
        "sdg": "SDG 7 깨끗한 에너지 · SDG 13 기후행동",
        "data": "EIA Open Data 전력 일별 데이터",
        "url": "https://www.eia.gov/opendata/documentation.php",
        "auth": "DEMO_KEY 가능 / 안정 사용은 무료 키 권장",
        "activity": "전력 수요·공급 시계열을 보고 태양광/풍력 확대가 필요한 시간대 추론",
    },
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
    return f'''# Raspberry Pi Pico 2 WH + Grove Shield / MicroPython basic CSV fetch
# 기본 출력: USB 시리얼. 선택 출력: Grove I2C OLED/LCD(SDA=GP4, SCL=GP5 예시).
import network, urequests, time
from machine import Pin

SSID = "YOUR_WIFI"
PASSWORD = "YOUR_PASSWORD"
URL = "https://thinkervis.github.io/free-api-data-science-edu/data/{csv_name}"

led = Pin("LED", Pin.OUT)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    led.toggle()
    time.sleep(0.5)
led.on()

r = urequests.get(URL)
text = r.text
r.close()

# Pico 메모리 보호: 큰 CSV는 앞부분만 확인
lines = text.split("\\n")[:6]
for line in lines:
    print(line)

# 선택: Grove I2C OLED/LCD 표시
# from machine import I2C
# import ssd1306
# i2c = I2C(0, scl=Pin(5), sda=Pin(4))
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)
# for i, line in enumerate(lines[:4]):
#     oled.text(line[:16], 0, i * 12)
# oled.show()
'''


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
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
</head>
<body>
{body}
</body>
</html>'''


def dataset_script(ds: dict[str, str]) -> str:
    viz_config = json.dumps(VIZ_CONFIG.get(ds["id"], {}), ensure_ascii=False)
    script = r'''
<script>
const VIZ_CONFIG = __VIZ_CONFIG__;
function parseCsvRows(text) {
  const rows = [];
  let row = [];
  let cell = '';
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    const next = text[i + 1];
    if (ch === '"') {
      if (inQuotes && next === '"') { cell += '"'; i++; }
      else { inQuotes = !inQuotes; }
    } else if (ch === ',' && !inQuotes) {
      row.push(cell); cell = '';
    } else if ((ch === '\n' || ch === '\r') && !inQuotes) {
      if (ch === '\r' && next === '\n') i++;
      row.push(cell); cell = '';
      if (row.some(v => v !== '')) rows.push(row);
      row = [];
    } else {
      cell += ch;
    }
  }
  row.push(cell);
  if (row.some(v => v !== '')) rows.push(row);
  return rows;
}
function escapeHtml(value) { return String(value).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch])); }
const LABEL_KO = {
  time:'시간', date:'연도/날짜', Year:'연도', value:'값', count:'개수', latitude:'위도', longitude:'경도', depth_km:'깊이(km)', magnitude:'규모',
  temperature_2m_max:'최고기온', temperature_2m_mean:'평균기온', temperature_2m_min:'최저기온', temperature_2m_c:'평균기온', precipitation_mm_day:'강수량(mm/일)', wind_speed_2m_m_s:'풍속(m/s)',
  rate:'환율', FEDFUNDS:'미국 기준금리(%)', cpi_value:'소비자물가지수(CPI)', parkingBikeTotCnt:'주차 자전거 수', stationName:'대여소', home_team:'홈팀', date_utc:'발사일', date_end:'제작연도', sex:'성별', area:'면적', population:'인구', type_name:'전력 데이터 유형', Entity:'지역',
  'Annual CO₂ emissions':'연간 CO₂ 배출량',
  'GDP (current US$)':'GDP(현재 US$)', 'Life expectancy at birth, total (years)':'기대수명(년)', 'Population, total':'총인구', 'School enrollment, secondary (% gross)':'중등교육 등록률(%)',
  'Access to electricity (% of population)':'전기 접근성(인구 %)', 'GDP per capita (current US$)':'1인당 GDP(현재 US$)', 'Mortality rate, under-5 (per 1,000 live births)':'5세 미만 사망률(1,000명당)', 'Primary completion rate, total (% of relevant age group)':'초등교육 이수율(%)',
  'South Korea':'한국', World:'세계', 'Day-ahead demand forecast':'하루 전 수요 예측', Demand:'전력 수요', 'Net generation':'순발전량', 'Total interchange':'총 전력 교환량', SEX_BTSX:'전체', SEX_FMLE:'여성', SEX_MLE:'남성'
};
function koLabel(value) { return LABEL_KO[value] || value; }
function column(rows, name) { const headers = rows[0] || []; const idx = headers.indexOf(name); if (idx < 0) return []; return rows.slice(1).map(row => row[idx] ?? ''); }
function numericColumn(rows, name, cfg={}) {
  return column(rows, name).map(v => Number(v)).map(v => {
    if (!Number.isFinite(v)) return null;
    if (cfg.invalid_below !== undefined && v <= cfg.invalid_below) return null;
    return v;
  });
}
function limitedRows(rows, maxPoints) { if (!maxPoints || rows.length <= maxPoints + 1) return rows; return [rows[0]].concat(rows.slice(-maxPoints)); }
function sortedDataRows(rows, xName) {
  const headers = rows[0] || []; const xIdx = headers.indexOf(xName);
  if (xIdx < 0) return rows;
  return [headers].concat(rows.slice(1).sort((a,b)=>String(a[xIdx]||'').localeCompare(String(b[xIdx]||''))));
}
function indexedSeries(y) {
  const base = y.find(v => v !== null && v !== 0);
  return y.map(v => (v === null || !base) ? null : (v / base) * 100);
}
function renderPreview(rows) {
  const target = document.getElementById('browser-preview');
  const headers = rows[0] || [];
  const bodyRows = rows.slice(1, 6);
  const head = headers.map(h => `<th>${escapeHtml(h)}</th>`).join('');
  const body = bodyRows.map(r => '<tr>' + headers.map((_, i) => `<td>${escapeHtml(r[i] ?? '')}</td>`).join('') + '</tr>').join('');
  target.innerHTML = `<h3>브라우저에서 방금 읽은 CSV 표 미리보기</h3><table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`;
}
function drawCsvChart(rows) {
  const chart = document.getElementById('chart');
  if (typeof Plotly === 'undefined') { chart.innerHTML = '<p>Plotly 라이브러리를 불러오지 못했습니다. 인터넷 연결 또는 CDN 차단 여부를 확인하세요.</p>'; return; }
  const cfg = VIZ_CONFIG || {};
  const dataRows = sortedDataRows(limitedRows(rows, cfg.max_points || 1200), cfg.x);
  let traces = [];
  let layout = {title: cfg.title || '데이터셋 맞춤 시각화', margin: {t: 50, r: 20, b: 60, l: 60}, hovermode: 'closest'};
  if (cfg.kind === 'line') {
    const x = column(dataRows, cfg.x);
    traces = (cfg.y || []).map((yName, i) => ({x, y: numericColumn(dataRows, yName, cfg), mode: 'lines', type: 'scatter', name: (cfg.labels || [])[i] || yName, yaxis: (cfg.axes || [])[i] || 'y'}));
    layout.xaxis = {title: koLabel(cfg.x)}; layout.yaxis = {title: (cfg.labels || [])[0] || cfg.y_title || ''};
    if (cfg.axes && cfg.axes.includes('y2')) layout.yaxis2 = {title: (cfg.labels || [])[1] || '', overlaying: 'y', side: 'right', showgrid: false};
    if (cfg.axes && cfg.axes.includes('y3')) layout.yaxis3 = {title: (cfg.labels || [])[2] || '', overlaying: 'y', side: 'right', anchor: 'free', position: 0.97, showgrid: false};
  } else if (cfg.kind === 'multiCategoryLine') {
    const headers = dataRows[0] || []; const catIdx = headers.indexOf(cfg.category), xIdx = headers.indexOf(cfg.x), yIdx = headers.indexOf(cfg.y); const groups = {};
    dataRows.slice(1).forEach(row => { const cat = row[catIdx] || '(blank)'; if (!groups[cat]) groups[cat] = {x: [], y: []}; groups[cat].x.push(row[xIdx]); const y = Number(row[yIdx]); groups[cat].y.push(Number.isFinite(y) ? y : null); });
    traces = Object.entries(groups).map(([name, g]) => ({x: g.x, y: cfg.indexed ? indexedSeries(g.y) : g.y, mode: 'lines+markers', type: 'scatter', name: koLabel(name)}));
    layout.xaxis = {title: koLabel(cfg.x)}; layout.yaxis = {title: cfg.y_title || koLabel(cfg.y), type: cfg.log_y ? 'log' : undefined};
  } else if (cfg.kind === 'factfulnessLong') {
    const headers = dataRows[0] || []; const indIdx=headers.indexOf('indicator_id'), countryIdx=headers.indexOf('countryiso3code'), dateIdx=headers.indexOf('date'), valueIdx=headers.indexOf('value'), countryNameIdx=headers.indexOf('country');
    const groups = {};
    dataRows.slice(1).forEach(row => {
      if (row[indIdx] !== cfg.indicator_id) return;
      const country = row[countryIdx] || row[countryNameIdx] || '(blank)';
      if (!groups[country]) groups[country] = {x: [], y: [], label: row[countryNameIdx] || country};
      const y = Number(row[valueIdx]); if (Number.isFinite(y)) { groups[country].x.push(row[dateIdx]); groups[country].y.push(y); }
    });
    traces = Object.entries(groups).map(([code, g]) => ({type:'scatter',mode:'lines+markers',name:koLabel(g.label || code),x:g.x,y:g.y}));
    layout.xaxis = {title:'연도'}; layout.yaxis = {title:'기대수명(년)'};
  } else if (cfg.kind === 'scattergeo') {
    const lonRaw = numericColumn(dataRows, cfg.lon, cfg); const latRaw = numericColumn(dataRows, cfg.lat, cfg); const text = cfg.hover ? column(dataRows, cfg.hover) : []; const sizeRaw = cfg.size ? numericColumn(dataRows, cfg.size, cfg) : []; const colorRaw = cfg.color ? numericColumn(dataRows, cfg.color, cfg) : [];
    const lon = [], lat = [], text2 = [], sizes = [], colors = [];
    dataRows.slice(1).forEach((_, i) => { const la = latRaw[i], lo = lonRaw[i]; if (la !== null && lo !== null) { lon.push(lo); lat.push(la); text2.push(text[i] || ''); sizes.push(cfg.size ? Math.max(6, (sizeRaw[i] || 1) * 3) : 7); colors.push(cfg.color ? colorRaw[i] : null); } });
    traces = [{type: 'scattergeo', mode: 'markers', lat, lon, text: text2, marker: {size: sizes, color: cfg.color ? colors : '#0969da', colorscale: 'Viridis', showscale: !!cfg.color, opacity: 0.75}}];
    if (cfg.geo_scope === 'korea') {
      layout.geo = {scope: 'asia', projection: {type: 'mercator'}, lonaxis: {range: [124, 132]}, lataxis: {range: [33, 39.5]}, showland: true, landcolor: '#f6f8fa', showcountries: true, countrycolor: '#8c959f', showsubunits: true, subunitcolor: '#d0d7de'};
    } else {
      layout.geo = {scope: 'world', projection: {type: 'natural earth'}, showland: true, landcolor: '#f6f8fa'};
    }
  } else if (cfg.kind === 'bar') {
    traces = [{type: 'bar', x: column(dataRows, cfg.x).map(koLabel), y: numericColumn(dataRows, cfg.y, cfg), name: koLabel(cfg.y)}]; layout.xaxis = {title: koLabel(cfg.x)}; layout.yaxis = {title: koLabel(cfg.y)};
  } else if (cfg.kind === 'barAggregate') {
    const headers = dataRows[0] || []; const idx = cfg.x_date_year ? headers.indexOf(cfg.x_date_year) : headers.indexOf(cfg.x); const counts = {};
    dataRows.slice(1).forEach(row => { const raw = row[idx] || '(blank)'; const key = cfg.x_date_year ? String(raw).slice(0, 4) : raw; counts[key] = (counts[key] || 0) + 1; });
    const entries = Object.entries(counts).sort((a, b) => String(a[0]).localeCompare(String(b[0]))).slice(0, 30);
    traces = [{type: 'bar', x: entries.map(e => koLabel(e[0])), y: entries.map(e => e[1]), name: '개수'}]; layout.yaxis = {title: '개수'};
  } else if (cfg.kind === 'histogram') {
    traces = [{type: 'histogram', x: numericColumn(dataRows, cfg.x, cfg), name: koLabel(cfg.x)}];
  } else if (cfg.kind === 'scatter') {
    const xs = numericColumn(dataRows, cfg.x, cfg), ys = numericColumn(dataRows, cfg.y, cfg), texts = cfg.text ? column(dataRows, cfg.text) : [];
    const clean = xs.map((x,i)=>({x,y:ys[i],text:texts[i]})).filter(p=>p.x !== null && p.y !== null && p.x > 0 && p.y > 0);
    traces = [{type: 'scatter', mode: 'markers', x: clean.map(p=>p.x), y: clean.map(p=>p.y), text: clean.map(p=>p.text), marker: {size: 8, opacity: 0.7}}];
    layout.xaxis = {title: cfg.x_title || koLabel(cfg.x), type: 'log'}; layout.yaxis = {title: cfg.y_title || koLabel(cfg.y), type: 'log'};
  }
  if (!traces.length) { chart.innerHTML = '<p>이 데이터셋의 맞춤 시각화 설정을 찾지 못했습니다.</p>'; return; }
  Plotly.newPlot(chart, traces, layout, {responsive: true, displaylogo: false});
}
async function testCsvAndChart(url) {
  const out = document.getElementById('test-output');
  try {
    const r = await fetch(url); if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const text = await r.text(); const rows = parseCsvRows(text); renderPreview(rows); drawCsvChart(rows);
    out.textContent = `status=${r.status} bytes=${text.length} csv_rows≈${Math.max(0, rows.length - 1)} columns=${(rows[0] || []).length}`;
  } catch (e) { out.textContent = 'ERROR: ' + e; }
}
</script>
'''
    return script.replace("__VIZ_CONFIG__", viz_config)


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
  <button onclick="testCsvAndChart('{html.escape(csv_url)}')">GitHub Pages에서 CSV 로드 + 맞춤형 Plotly 시각화 테스트</button>
  <pre id="test-output">버튼을 누르면 이 페이지에서 CSV를 직접 fetch하고, 데이터셋별 교육용 맞춤 시각화를 표시합니다.</pre>
  <div id="browser-preview"></div>
  <div id="chart" aria-label="브라우저 직접 시각화 결과"></div>
</div>
<h2>CSV 미리보기</h2>
{preview}
<h2>Streamlit 기본 코드</h2>
<pre>{html.escape(streamlit_code(ds['csv']))}</pre>
<h2>Pico 2 WH + Grove Shield 기본 코드</h2>
<pre>{html.escape(pico_code(ds['csv']))}</pre>
{dataset_script(ds)}
'''
    return layout(ds["title"], body)


def svg_map_examples_page() -> str:
    body = '''
<p><a href="../index.html">← 전체 목록</a></p>
<h1>SVG 지도 이미지 시각화 예제</h1>
<p>수업용으로 바로 이해하기 쉬운 SVG 지도/카토그램 예제입니다. 실제 보고서용 경계는 국토교통부 행정구역 경계 SHP, 서울 열린데이터광장/주소기반산업지원서비스 경계, 또는 행정동 GeoJSON을 SVG로 변환해 같은 방식으로 칠하면 됩니다.</p>
<div class="card">
  <h2>1) 한국 광역시도별 시각화</h2>
  <div class="map-grid">
    <svg id="korea-sido-map" viewBox="0 0 360 520" role="img" aria-label="한국 광역시도별 SVG 지도 예제">
      <style>.region{stroke:#fff;stroke-width:3;cursor:pointer}.label{font-size:13px;font-weight:700;fill:#24292f;pointer-events:none}.island{stroke:#fff;stroke-width:3}</style>
      <path id="KR-11" class="region" d="M145 78 L197 80 L210 112 L190 142 L144 137 L126 108 Z"/><text class="label" x="158" y="112">서울</text>
      <path id="KR-28" class="region" d="M113 92 L141 78 L126 108 L141 140 L108 151 L83 124 Z"/><text class="label" x="96" y="125">인천</text>
      <path id="KR-41" class="region" d="M126 46 L222 55 L254 111 L231 172 L165 183 L108 151 L141 140 L190 142 L210 112 L197 80 L145 78 L126 108 L113 92 Z"/><text class="label" x="205" y="133">경기</text>
      <path id="KR-42" class="region" d="M197 25 L302 47 L323 128 L281 198 L231 172 L254 111 L222 55 Z"/><text class="label" x="264" y="102">강원</text>
      <path id="KR-43" class="region" d="M165 183 L231 172 L281 198 L264 260 L198 260 L151 224 Z"/><text class="label" x="206" y="221">충북</text>
      <path id="KR-44" class="region" d="M82 181 L151 224 L198 260 L174 313 L94 296 L52 239 Z"/><text class="label" x="107" y="254">충남</text>
      <path id="KR-30" class="region" d="M152 229 L188 242 L177 275 L139 267 Z"/><text class="label" x="146" y="257">대전</text>
      <path id="KR-36" class="region" d="M127 176 L160 184 L151 224 L112 208 Z"/><text class="label" x="121" y="202">세종</text>
      <path id="KR-45" class="region" d="M94 296 L174 313 L186 376 L127 419 L57 372 Z"/><text class="label" x="102" y="353">전북</text>
      <path id="KR-46" class="region" d="M57 372 L127 419 L152 466 L93 499 L31 454 Z"/><text class="label" x="73" y="438">전남</text>
      <path id="KR-47" class="region" d="M198 260 L264 260 L315 309 L297 389 L227 405 L186 376 L174 313 Z"/><text class="label" x="232" y="336">경북</text>
      <path id="KR-27" class="region" d="M222 291 L260 297 L255 333 L216 329 Z"/><text class="label" x="226" y="318">대구</text>
      <path id="KR-48" class="region" d="M186 376 L227 405 L297 389 L325 430 L273 478 L198 459 L152 466 L127 419 Z"/><text class="label" x="210" y="436">경남</text>
      <path id="KR-31" class="region" d="M287 386 L326 397 L315 430 L282 418 Z"/><text class="label" x="288" y="411">울산</text>
      <path id="KR-26" class="region" d="M273 478 L325 430 L337 468 L306 500 Z"/><text class="label" x="295" y="468">부산</text>
      <path id="KR-29" class="region" d="M82 389 L121 406 L101 438 L64 421 Z"/><text class="label" x="76" y="416">광주</text>
      <ellipse id="KR-50" class="region island" cx="152" cy="505" rx="48" ry="20"/><text class="label" x="139" y="510">제주</text>
    </svg>
    <div><pre id="sido-output">시도를 클릭해 보세요.</pre><p>아이디어: 인구, 미세먼지 평균, 학교 수, 지역 축제 수, 생물종 관측 수 등을 시도별로 합산해 색으로 표현합니다.</p></div>
  </div>
</div>
<div class="card"><h2>2) 서울 구별 시각화</h2><p>서울 25개 구를 SVG 느낌의 카토그램 타일로 표현했습니다. 실제 구 경계 SVG를 써도 id와 fill을 바꾸는 구조는 같습니다.</p><div id="seoul-gu-map" class="tile-map"></div><pre id="gu-output">구를 클릭해 보세요.</pre></div>
<div class="card"><h2>3) 서울 동별 시각화</h2><p>동 단위는 행정동 수가 많으므로 한 구를 골라 시작하는 편이 좋습니다. 아래는 성동구 동별 예제입니다.</p><div id="seoul-dong-map" class="tile-map dong"></div><pre id="dong-output">동을 클릭해 보세요.</pre></div>
<style>.map-grid{display:grid;grid-template-columns:minmax(280px,420px) 1fr;gap:1rem;align-items:start}svg{max-width:100%;height:auto}.tile-map{display:grid;grid-template-columns:repeat(7,minmax(76px,1fr));gap:6px;max-width:760px}.tile{border:1px solid #fff;border-radius:10px;min-height:52px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;color:#24292f;cursor:pointer}.dong{grid-template-columns:repeat(5,minmax(82px,1fr))}@media(max-width:760px){.map-grid{grid-template-columns:1fr}.tile-map{grid-template-columns:repeat(4,1fr)}}</style>
<script>
const palette=['#eff6ff','#bfdbfe','#93c5fd','#60a5fa','#3b82f6','#1d4ed8'];function color(v,max){return palette[Math.min(palette.length-1,Math.floor((v/max)*(palette.length-1)))]}
const sidoData={'KR-11':91,'KR-28':55,'KR-41':100,'KR-42':42,'KR-43':36,'KR-44':50,'KR-30':44,'KR-36':31,'KR-45':39,'KR-46':34,'KR-47':46,'KR-27':49,'KR-48':53,'KR-31':38,'KR-26':62,'KR-29':41,'KR-50':47};const sidoNames={'KR-11':'서울','KR-28':'인천','KR-41':'경기','KR-42':'강원','KR-43':'충북','KR-44':'충남','KR-30':'대전','KR-36':'세종','KR-45':'전북','KR-46':'전남','KR-47':'경북','KR-27':'대구','KR-48':'경남','KR-31':'울산','KR-26':'부산','KR-29':'광주','KR-50':'제주'};Object.entries(sidoData).forEach(([id,v])=>{const el=document.getElementById(id);el.style.fill=color(v,100);el.addEventListener('click',()=>document.getElementById('sido-output').textContent=`${sidoNames[id]}: 예제 지표 ${v}`)});
const guLayout=[['은평','서대문','종로','성북','강북','도봉','노원'],['마포','용산','중구','동대문','중랑','광진',''],['강서','양천','영등포','동작','서초','강남','송파'],['구로','금천','관악','','성동','강동','']];const guValues={'종로':72,'중구':64,'용산':58,'성동':83,'광진':51,'동대문':44,'중랑':39,'성북':48,'강북':35,'도봉':31,'노원':46,'은평':49,'서대문':53,'마포':78,'양천':55,'강서':61,'구로':47,'금천':42,'영등포':70,'동작':57,'관악':66,'서초':75,'강남':96,'송파':88,'강동':59};
function renderTiles(targetId,rows,values,suffix){const target=document.getElementById(targetId);const max=Math.max(...Object.values(values));rows.flat().forEach(name=>{const d=document.createElement('div');d.className='tile';if(!name){d.style.visibility='hidden';target.appendChild(d);return}const v=values[name]??0;d.style.background=color(v,max);d.textContent=name;d.title=`${name}: ${v}`;d.onclick=()=>document.getElementById(`${suffix}-output`).textContent=`${name}: 예제 지표 ${v}`;target.appendChild(d)})}
renderTiles('seoul-gu-map',guLayout,guValues,'gu');const dongLayout=[['왕십리도선동','왕십리2동','마장동','사근동','행당1동'],['행당2동','응봉동','금호1가동','금호2·3가동','금호4가동'],['옥수동','성수1가1동','성수1가2동','성수2가1동','성수2가3동'],['송정동','용답동','','','']];const dongValues={'왕십리도선동':41,'왕십리2동':37,'마장동':35,'사근동':29,'행당1동':44,'행당2동':39,'응봉동':31,'금호1가동':33,'금호2·3가동':36,'금호4가동':28,'옥수동':45,'성수1가1동':77,'성수1가2동':69,'성수2가1동':81,'성수2가3동':74,'송정동':40,'용답동':34};renderTiles('seoul-dong-map',dongLayout,dongValues,'dong');
</script>
'''
    return layout("SVG 지도 이미지 시각화 예제", body)


def sdg_topics_page() -> str:
    cards = []
    for i, item in enumerate(SDG_TOPICS, start=1):
        cards.append(f'''
<div class="card sdg-card">
  <h2>{i}. {html.escape(item['title'])}</h2>
  <p><span class="badge">{html.escape(item['sdg'])}</span><span class="badge">인증: {html.escape(item['auth'])}</span></p>
  <p><b>데이터:</b> {html.escape(item['data'])}</p>
  <p><b>수업 아이디어:</b> {html.escape(item['activity'])}</p>
  <p><a href="{html.escape(item['url'])}">공식 문서/데이터 출처</a></p>
  <div id="sdg-chart-{i-1}" class="sdg-chart"></div>
</div>''')
    script = r'''
<style>.sdg-chart{height:380px;margin-top:1rem}.sdg-card{break-inside:avoid}</style>
<script>
function parseCsvRows(text) {
  const rows = []; let row = [], cell = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i], n = text[i + 1];
    if (ch === '"') { if (q && n === '"') { cell += '"'; i++; } else q = !q; }
    else if (ch === ',' && !q) { row.push(cell); cell = ''; }
    else if ((ch === '\n' || ch === '\r') && !q) { if (ch === '\r' && n === '\n') i++; row.push(cell); cell = ''; if (row.some(v => v !== '')) rows.push(row); row = []; }
    else cell += ch;
  }
  row.push(cell); if (row.some(v => v !== '')) rows.push(row); return rows;
}
function toObjects(rows) { const h = rows[0] || []; return rows.slice(1).map(r => Object.fromEntries(h.map((k,i)=>[k,r[i] ?? '']))); }
async function csv(path) { return toObjects(parseCsvRows(await fetch(path).then(r => { if (!r.ok) throw new Error(path + ' HTTP ' + r.status); return r.text(); }))); }
function num(v) { const n = Number(v); return Number.isFinite(n) ? n : null; }
const LABEL_KO = {
  'South Korea':'한국', World:'세계', 'GDP (current US$)':'GDP(현재 US$)', 'Life expectancy at birth, total (years)':'기대수명(년)', 'Population, total':'총인구', 'School enrollment, secondary (% gross)':'중등교육 등록률(%)',
  'Day-ahead demand forecast':'하루 전 수요 예측', Demand:'전력 수요', 'Net generation':'순발전량', 'Total interchange':'총 전력 교환량'
};
function koLabel(value){ return LABEL_KO[value] || value; }
const PLOT_CONFIG = {responsive:true, displaylogo:false, displayModeBar:false};
function validRows(rows, valueField) { return rows.filter(r => num(r[valueField]) !== null); }
function indexRows(rows, valueField) {
  const clean = validRows(rows, valueField);
  const base = clean.length ? num(clean[0][valueField]) : null;
  if (!base) return [];
  return clean.map(r => ({...r, indexValue: num(r[valueField]) / base * 100}));
}
function latestBy(rows, group, value) { const out = {}; rows.forEach(r => { const k = r[group]; if (!out[k] || String(r.date || r.time || r.Year) > String(out[k].date || out[k].time || out[k].Year)) out[k] = r; }); return Object.values(out).filter(r => num(r[value]) !== null); }
async function drawSdgCharts() {
  try {
    const air = await csv('../data/open_meteo_seoul_air_quality_hourly.csv');
    const airRecent = air.slice(-240);
    Plotly.newPlot('sdg-chart-0', [
      {type:'scatter',mode:'lines',name:'PM10',x:airRecent.map(r=>r.time),y:airRecent.map(r=>num(r.pm10))},
      {type:'scatter',mode:'lines',name:'PM2.5',x:airRecent.map(r=>r.time),y:airRecent.map(r=>num(r.pm2_5))}
    ], {title:'최근 시간대 서울 대기질 변화', margin:{t:50,r:20,b:80,l:55}, yaxis:{title:'㎍/m³'}}, PLOT_CONFIG);

    const nasa = await csv('../data/nasa_power_seoul_daily.csv');
    const nasaRecent = nasa.slice(-365);
    Plotly.newPlot('sdg-chart-1', [
      {type:'scatter',mode:'lines',name:'평균기온',x:nasaRecent.map(r=>r.date),y:nasaRecent.map(r=>num(r.temperature_2m_c))},
      {type:'bar',name:'강수량',x:nasaRecent.map(r=>r.date),y:nasaRecent.map(r=>num(r.precipitation_mm_day)),yaxis:'y2',opacity:.35}
    ], {title:'최근 1년 서울 기온·강수', margin:{t:50,r:50,b:80,l:55}, yaxis:{title:'°C'}, yaxis2:{title:'mm/day',overlaying:'y',side:'right'}}, PLOT_CONFIG);

    const co2 = await csv('../data/owid_co2_korea_world.csv');
    const co2Groups = [...new Set(co2.map(r=>r.Entity))];
    Plotly.newPlot('sdg-chart-2', co2Groups.map(g => {
      const rows = indexRows(co2.filter(r=>r.Entity===g).sort((a,b)=>Number(a.Year)-Number(b.Year)), 'Annual CO₂ emissions');
      return {type:'scatter',mode:'lines+markers',name:koLabel(g),x:rows.map(r=>r.Year),y:rows.map(r=>r.indexValue),customdata:rows.map(r=>(num(r['Annual CO₂ emissions'])/1e9).toFixed(2)),hovertemplate:'%{fullData.name}<br>연도: %{x}<br>변화: %{y:.1f} (첫해=100)<br>실제 배출량: %{customdata} GtCO₂<extra></extra>'};
    }), {title:'한국과 세계 CO₂ 배출량 변화(첫해=100)', margin:{t:70,r:20,b:60,l:70}, yaxis:{title:'첫해=100 지수'}}, PLOT_CONFIG);

    const gbif = await csv('../data/gbif_korea_occurrences_sample.csv');
    Plotly.newPlot('sdg-chart-3', [{type:'scattergeo',mode:'markers',lat:gbif.map(r=>num(r.decimalLatitude)),lon:gbif.map(r=>num(r.decimalLongitude)),text:gbif.map(r=>'학명: '+r.scientificName),marker:{size:7,opacity:.65,color:'#16a34a'}}], {title:'한국 생물종 관측 위치', margin:{t:50,r:20,b:20,l:20}, geo:{scope:'asia',projection:{type:'mercator'},lonaxis:{range:[124,132]},lataxis:{range:[33,39.5]},showland:true,landcolor:'#f6f8fa',showcountries:true}}, PLOT_CONFIG);

    const bike = await csv('../data/seoul_bike_sample.csv');
    Plotly.newPlot('sdg-chart-4', [{type:'bar',x:bike.map(r=>r.stationName),y:bike.map(r=>num(r.parkingBikeTotCnt)),marker:{color:'#0ea5e9'}}], {title:'따릉이 대여소별 현재 자전거 수', margin:{t:50,r:20,b:120,l:55}, yaxis:{title:'대수'}}, PLOT_CONFIG);

    const countries = await csv('../data/restcountries_world_snapshot.csv');
    Plotly.newPlot('sdg-chart-5', [{type:'scatter',mode:'markers',x:countries.map(r=>num(r.area)),y:countries.map(r=>num(r.population)),text:countries.map(r=>r.name),marker:{size:8,opacity:.6,color:'#6366f1'}}], {title:'국가별 면적·인구 비교로 보는 도시·인프라 압력', margin:{t:50,r:20,b:65,l:70}, xaxis:{title:'면적',type:'log'}, yaxis:{title:'인구',type:'log'}}, PLOT_CONFIG);

    const wb = await csv('../data/worldbank_korea_indicators.csv');
    const inds = [...new Set(wb.map(r=>r.indicator))];
    Plotly.newPlot('sdg-chart-6', inds.map(ind => {
      const rows = indexRows(wb.filter(r=>r.indicator===ind).sort((a,b)=>Number(a.date)-Number(b.date)), 'value');
      return {type:'scatter',mode:'lines+markers',name:koLabel(ind),x:rows.map(r=>r.date),y:rows.map(r=>r.indexValue),customdata:rows.map(r=>num(r.value)),hovertemplate:'%{fullData.name}<br>연도: %{x}<br>변화: %{y:.1f} (첫해=100)<br>원값: %{customdata}<extra></extra>'};
    }), {title:'한국 주요 발전 지표 변화(첫해=100)', margin:{t:70,r:20,b:70,l:70}, yaxis:{title:'첫해=100 지수'}}, PLOT_CONFIG);

    const fact = await csv('../data/factfulness_global_indicators.csv');
    const life = latestBy(fact.filter(r=>r.indicator_id==='SP.DYN.LE00.IN'), 'countryiso3code', 'value');
    Plotly.newPlot('sdg-chart-7', [{type:'bar',x:life.map(r=>koLabel(r.country)),y:life.map(r=>num(r.value)),text:life.map(r=>r.date),marker:{color:'#f97316'}}], {title:'팩트풀니스: 최신 기대수명 비교', margin:{t:50,r:20,b:110,l:55}, yaxis:{title:'년'}}, PLOT_CONFIG);

    Plotly.newPlot('sdg-chart-8', [{type:'bar',x:nasaRecent.map(r=>r.date),y:nasaRecent.map(r=>num(r.precipitation_mm_day)),marker:{color:'#38bdf8'}}], {title:'물·가뭄 수업용: 서울 일별 강수량', margin:{t:50,r:20,b:80,l:55}, yaxis:{title:'mm/일'}}, PLOT_CONFIG);

    const eia = await csv('../data/eia_california_electricity_daily.csv');
    const recentEia = eia.slice(-600); const types = [...new Set(recentEia.map(r=>r.type_name))].slice(0,5);
    Plotly.newPlot('sdg-chart-9', types.map(t => { const rows = recentEia.filter(r=>r.type_name===t); return {type:'scatter',mode:'lines',name:koLabel(t),x:rows.map(r=>r.date),y:rows.map(r=>num(r.value))}; }), {title:'전력 수요·공급 유형별 변화', margin:{t:50,r:20,b:80,l:70}, yaxis:{title:'MWh'}}, PLOT_CONFIG);
  } catch (err) {
    document.querySelectorAll('.sdg-chart').forEach(el => { if (!el.innerHTML) el.innerHTML = '<p>시각화 로드 실패: ' + err.message + '</p>'; });
  }
}
drawSdgCharts();
</script>
'''
    body = f'''
<p><a href="../index.html">← 전체 목록</a></p>
<h1>지속가능발전(SDG) 주제 데이터 10가지</h1>
<p>지속가능발전 수업에 바로 연결하기 쉬운 주제·데이터·활동을 모았습니다. 각 주제는 “무엇을 질문할지 → 어떤 데이터를 볼지 → 어떻게 시각화할지”가 드러나도록 구성했습니다.</p>
{''.join(cards)}
{script}
'''
    return layout("지속가능발전(SDG) 주제 데이터 10가지", body)


def factfulness_literacy_page() -> str:
    body = r"""
<p><a href="../index.html">← 전체 목록</a> · <a href="../datasets/factfulness-global.html">CSV 데이터셋 상세</a></p>
<h1>팩트풀니스 데이터 리터러시 수업</h1>
<p>학생들이 “세상은 점점 나빠지고 있다” 같은 직관을 바로 믿지 않고, 최신 공공데이터로 자신의 상식을 업데이트하는 수업용 전용 페이지입니다.</p>

<div class="hero card">
  <div>
    <h2>수업 핵심 질문</h2>
    <p><b>내가 알고 있는 세계의 모습은 최신 데이터와 얼마나 다를까?</b></p>
    <p>페이지를 열면 최신 CSV를 자동으로 불러와 기본 그래프를 보여 줍니다. 학생은 먼저 예상값을 적고, <b>예상값과 비교하기</b>로 실제값과의 차이를 확인합니다.</p>
  </div>
  <div class="mini-rubric">
    <b>배우는 역량</b>
    <ul>
      <li>예상과 관측값 구분</li>
      <li>출처와 최신성 확인</li>
      <li>국가/세계 평균 비교</li>
      <li>그래프 과장 읽기</li>
      <li>근거 있는 설명 쓰기</li>
    </ul>
  </div>
</div>

<div id="data-status" class="status" role="status">데이터를 불러오는 중입니다…</div>

<div class="card">
  <h2>1단계. 데이터 보기 전 예상하기</h2>
  <p>그래프를 보기 전에 아래 질문에 먼저 답해도 좋고, 빈칸으로 둔 채 실제값만 확인해도 됩니다.</p>
  <div class="quiz-grid">
    <label>한국 사람은 평균적으로 몇 살까지 살 것으로 예상될까요?<span class="field-help">기대수명은 “현재의 사망률이 계속된다고 가정할 때, 한 사람이 평균적으로 살 것으로 기대되는 햇수”입니다.</span><input id="guess-life-kor" type="number" placeholder="숫자로 예상해 보기"></label>
    <label>세계에서 5세 생일 전에 사망하는 어린이는 1,000명 중 몇 명일까요?<span class="field-help">5세 미만 사망률은 보건, 영양, 식수, 의료 접근성을 함께 보여 주는 지표입니다. 낮을수록 아이들이 더 안전하게 자란다는 뜻입니다.</span><input id="guess-mort-world" type="number" placeholder="숫자로 예상해 보기"></label>
    <label>인도에서 전기를 사용할 수 있는 사람은 전체 인구 중 몇 %일까요?<span class="field-help">전기 접근성은 집, 학교, 병원, 일터에서 기본적인 전기를 쓸 수 있는 사람이 얼마나 되는지를 나타냅니다.</span><input id="guess-electricity-ind" type="number" placeholder="숫자로 예상해 보기"></label>
    <label>나이지리아의 1인당 GDP는 한 사람당 연간 몇 달러 정도일까요?<span class="field-help">1인당 GDP는 나라의 총소득을 인구로 나눈 평균값입니다. 개인이 실제로 버는 돈과 같지는 않지만 경제 규모를 비교할 때 자주 씁니다.</span><input id="guess-gdp-nga" type="number" placeholder="숫자로 예상해 보기"></label>
  </div>
  <button id="compare-button" type="button">예상값과 비교하기</button>
  <pre id="guess-result">데이터를 불러온 뒤 예상-실제-차이를 표시합니다.</pre>
</div>

<div class="card">
  <h2>2단계. 최신 지표 비교하기</h2>
  <p>선택한 지표의 국가별 가장 최근 값을 비교합니다. 아래 선택 상자와 최신 비교 그래프·추세 그래프가 함께 바뀝니다.</p>
  <p><select id="indicator-select" aria-label="비교할 지표 선택"></select></p>
  <div id="latest-chart" style="height:460px"></div>
</div>

<div class="card">
  <h2>3단계. 시간에 따른 변화 보기</h2>
  <p>팩트풀니스 수업에서는 “현재 스냅샷”보다 “변화 방향”이 중요합니다. 같은 지표를 시간축으로 보면 오래된 상식이 왜 남아 있는지 토론할 수 있습니다.</p>
  <div id="trend-chart" style="height:460px"></div>
</div>

<div class="card">
  <h2>데이터 출처와 한계</h2>
  <ul>
    <li>출처: World Bank 지표를 갱신 스크립트로 수집해 만든 <code>factfulness_global_indicators.csv</code></li>
    <li>페이지에서 불러오는 경로: <code id="csv-path">../data/factfulness_global_indicators.csv</code></li>
    <li>지표별 최신 연도는 국가마다 다를 수 있습니다. 그래프의 hover/막대 라벨에서 연도를 함께 확인하세요.</li>
    <li>이 페이지는 “정답 맞히기”보다 예상과 데이터가 달라지는 이유를 해석하는 수업용 자료입니다.</li>
  </ul>
</div>

<div class="card">
  <h2>4단계. 토론 질문</h2>
  <ol>
    <li>내 예상과 실제 데이터가 가장 크게 달랐던 지표는 무엇인가?</li>
    <li>나는 왜 그렇게 예상했을까? 뉴스, 교과서, 경험, 편견 중 무엇의 영향이 컸을까?</li>
    <li>세계 평균만 보면 놓치는 차이는 무엇인가? 국가별 비교가 필요한 이유는?</li>
    <li>그래프 축을 바꾸면 인상이 어떻게 달라지는가?</li>
    <li>최신 데이터로 설명문을 다시 쓴다면 어떤 문장이 더 정확한가?</li>
  </ol>
</div>

<div class="card">
  <h2>수업 산출물 예시</h2>
  <ul>
    <li>“내 상식 업데이트 카드” 1장: 예상값, 실제값, 차이, 배운 점</li>
    <li>국가별 지표 비교 인포그래픽</li>
    <li>오래된 통념을 바로잡는 1분 발표</li>
    <li>데이터 출처·연도·한계를 포함한 짧은 보고서</li>
  </ul>
</div>

<style>
.hero{display:grid;grid-template-columns:1.5fr 1fr;gap:1rem}.mini-rubric{background:#f6f8fa;border-radius:12px;padding:1rem}.quiz-grid{display:grid;grid-template-columns:repeat(2,minmax(220px,1fr));gap:1rem;margin:1rem 0}.hint{grid-column:1/-1;margin:0;padding:.75rem .9rem;border-radius:10px;background:#fff7ed;border:1px solid #fed7aa;color:#9a3412}.field-help{display:block;margin:.4rem 0 .2rem;color:#57606a;font-size:.92rem;line-height:1.45;font-weight:400}.status{margin:1rem 0;padding:.8rem 1rem;border-radius:10px;background:#eef6ff;border:1px solid #bfdbfe;color:#1e3a8a}.status.error{background:#fff1f2;border-color:#fecdd3;color:#9f1239}.status.ok{background:#ecfdf5;border-color:#bbf7d0;color:#166534}input,select{width:100%;box-sizing:border-box;padding:.55rem;border:1px solid #d0d7de;border-radius:8px;margin-top:.35rem}button{padding:.65rem 1rem;border:0;border-radius:10px;background:#2563eb;color:white;font-weight:700;cursor:pointer}button:hover{background:#1d4ed8}@media(max-width:760px){.hero,.quiz-grid{grid-template-columns:1fr}#latest-chart,#trend-chart{height:380px!important}}
</style>
<script>
const CSV_URL = '../data/factfulness_global_indicators.csv';
const COUNTRIES = ['KOR','WLD','IND','NGA','SWE'];
const COUNTRY_LABELS = {KOR:'한국', WLD:'세계', IND:'인도', NGA:'나이지리아', SWE:'스웨덴'};
const PLOT_CONFIG = {responsive:true, displaylogo:false, displayModeBar:false};
const INDICATOR_LABELS = {
  'Access to electricity (% of population)':'전기 접근성(인구 %)',
  'GDP per capita (current US$)':'1인당 GDP(현재 US$)',
  'Life expectancy at birth, total (years)':'기대수명(년)',
  'Mortality rate, under-5 (per 1,000 live births)':'5세 미만 사망률(1,000명당)',
  'Primary completion rate, total (% of relevant age group)':'초등교육 이수율(%)'
};
function koIndicator(name){ return INDICATOR_LABELS[name] || name; }
let factRows = [];
let headers = [];

function setStatus(message, type='') {
  const el = document.getElementById('data-status');
  el.textContent = message;
  el.className = `status ${type}`.trim();
}
function ensurePlotly() {
  if (typeof Plotly === 'undefined') throw new Error('Plotly 라이브러리를 불러오지 못했습니다. 인터넷 연결 또는 CDN 차단 여부를 확인하세요.');
}
function parseCsvRows(text){const rows=[];let row=[],cell='',q=false;for(let i=0;i<text.length;i++){const ch=text[i],n=text[i+1];if(ch==='"'){if(q&&n==='"'){cell+='"';i++}else q=!q}else if(ch===','&&!q){row.push(cell);cell=''}else if((ch==='\n'||ch==='\r')&&!q){if(ch==='\r'&&n==='\n')i++;row.push(cell);cell='';if(row.some(v=>v!==''))rows.push(row);row=[]}else cell+=ch}row.push(cell);if(row.some(v=>v!==''))rows.push(row);return rows}
function toObjects(rows){headers=rows[0]||[];return rows.slice(1).map(r=>Object.fromEntries(headers.map((h,i)=>[h,r[i]??''])))}
function latestBy(indicator,country){const rows=factRows.filter(r=>r.indicator_id===indicator&&r.countryiso3code===country).sort((a,b)=>Number(b.date)-Number(a.date));return rows[0]}
function fmt(v){const n=Number(v);return Number.isFinite(n)?n.toLocaleString(undefined,{maximumFractionDigits:1}):'데이터 없음'}
function selectedIndicator(){return document.getElementById('indicator-select').value || 'SP.DYN.LE00.IN'}

async function loadFactfulness({compare=false}={}){
  try {
    ensurePlotly();
    if(!factRows.length){
      setStatus(`CSV를 불러오는 중입니다: ${new URL(CSV_URL, location.href).href}`);
      const response = await fetch(CSV_URL, {cache:'no-cache'});
      if(!response.ok) throw new Error(`CSV 로드 실패: ${response.status} ${response.statusText} (${response.url})`);
      const text = await response.text();
      factRows = toObjects(parseCsvRows(text)).filter(r=>r.indicator_id && r.countryiso3code && r.date);
      if(!factRows.length) throw new Error('CSV는 열렸지만 읽을 수 있는 데이터 행이 없습니다.');
      setupIndicatorSelect();
      const years = factRows.map(r=>Number(r.date)).filter(Number.isFinite);
      setStatus(`데이터 ${factRows.length.toLocaleString()}행 로드 완료 · 수록 연도 ${Math.min(...years)}–${Math.max(...years)}`, 'ok');
    }
    drawLatest();
    drawTrend();
    if(compare) compareGuesses();
  } catch (err) {
    console.error(err);
    setStatus(err.message || String(err), 'error');
    document.getElementById('guess-result').textContent = '데이터를 불러오지 못했습니다. 위 오류 메시지와 CSV 경로를 확인하세요.';
  }
}
function compareGuesses(){
  if(!factRows.length){ loadFactfulness({compare:true}); return; }
  const checks=[['한국 기대수명','guess-life-kor','SP.DYN.LE00.IN','KOR','년'],['세계 5세 미만 사망률','guess-mort-world','SH.DYN.MORT','WLD','명/1,000명'],['인도 전기 접근성','guess-electricity-ind','EG.ELC.ACCS.ZS','IND','%'],['나이지리아 1인당 GDP','guess-gdp-nga','NY.GDP.PCAP.CD','NGA','달러']];
  const lines=[];
  for(const [label,input,ind,country,unit] of checks){
    const actual=latestBy(ind,country);
    const raw=document.getElementById(input).value;
    const guess=Number(raw);
    const actualVal=actual?Number(actual.value):NaN;
    const diff=raw!==''&&Number.isFinite(guess)&&Number.isFinite(actualVal)?` / 차이: ${fmt(Math.abs(guess-actualVal))}${unit}`:'';
    lines.push(`${label}: 예상 ${raw||'미입력'}${unit} → 실제 ${fmt(actualVal)}${unit} (${actual?.date||'연도 없음'})${diff}`);
  }
  document.getElementById('guess-result').textContent=lines.join('\n');
}
function setupIndicatorSelect(){
  const select=document.getElementById('indicator-select');
  const inds=[...new Map(factRows.map(r=>[r.indicator_id,r.indicator])).entries()];
  select.innerHTML=inds.map(([id,name])=>`<option value="${id}">${koIndicator(name)}</option>`).join('');
  select.value = inds.some(([id])=>id==='SP.DYN.LE00.IN') ? 'SP.DYN.LE00.IN' : (inds[0]?.[0] || '');
}
function latestRowsForIndicator(ind){
  const latest={};
  for(const r of factRows.filter(row=>row.indicator_id===ind)){
    const k=r.countryiso3code;
    if(!latest[k]||Number(r.date)>Number(latest[k].date)) latest[k]=r;
  }
  return COUNTRIES.map(c=>latest[c]).filter(Boolean);
}
function drawLatest(){
  ensurePlotly();
  if(!factRows.length) return;
  const ind=selectedIndicator();
  const rows=latestRowsForIndicator(ind);
  const name=koIndicator(factRows.find(r=>r.indicator_id===ind)?.indicator||ind);
  Plotly.newPlot('latest-chart',[{type:'bar',x:rows.map(r=>COUNTRY_LABELS[r.countryiso3code]||r.country),y:rows.map(r=>Number(r.value)),text:rows.map(r=>r.date),customdata:rows.map(r=>r.countryiso3code),hovertemplate:'국가: %{x} (%{customdata})<br>값: %{y:.1f}<br>연도: %{text}<extra></extra>',marker:{color:'#2563eb'}}],{title:`최신값 비교: ${name}`,yaxis:{title:'값'},margin:{t:60,r:20,b:100,l:60}},PLOT_CONFIG);
}
function drawTrend(){
  ensurePlotly();
  if(!factRows.length) return;
  const ind=selectedIndicator();
  const traces=COUNTRIES.map(c=>{const rows=factRows.filter(r=>r.indicator_id===ind&&r.countryiso3code===c).sort((a,b)=>Number(a.date)-Number(b.date));return {type:'scatter',mode:'lines+markers',name:COUNTRY_LABELS[c]||c,x:rows.map(r=>r.date),y:rows.map(r=>Number(r.value)),hovertemplate:'국가: %{fullData.name}<br>연도: %{x}<br>값: %{y:.1f}<extra></extra>'}}).filter(t=>t.x.length);
  const name=koIndicator(factRows.find(r=>r.indicator_id===ind)?.indicator||ind);
  Plotly.newPlot('trend-chart',traces,{title:`추세: ${name}`,xaxis:{title:'연도'},yaxis:{title:'값'},margin:{t:60,r:20,b:60,l:70}},PLOT_CONFIG);
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('csv-path').textContent = CSV_URL;
  document.getElementById('compare-button').addEventListener('click', () => loadFactfulness({compare:true}));
  document.getElementById('indicator-select').addEventListener('change', () => { drawLatest(); drawTrend(); });
  loadFactfulness();
});
</script>
"""
    return layout("팩트풀니스 데이터 리터러시 수업", body)

def main() -> None:
    DOCS.mkdir(exist_ok=True)
    DOC_DATA.mkdir(parents=True, exist_ok=True)
    DATASET_PAGES.mkdir(parents=True, exist_ok=True)
    examples_dir = DOCS / "examples"
    examples_dir.mkdir(parents=True, exist_ok=True)
    (examples_dir / "svg-map-visualization.html").write_text(svg_map_examples_page(), encoding="utf-8")
    (examples_dir / "sdg-topics.html").write_text(sdg_topics_page(), encoding="utf-8")
    (examples_dir / "factfulness-literacy.html").write_text(factfulness_literacy_page(), encoding="utf-8")

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
    by_id = {ds["id"]: ds for ds in DATASETS}
    recommended_items = []
    for rank, dataset_id in enumerate(RECOMMENDED_CANDIDATE_IDS, start=1):
        ds = by_id[dataset_id]
        _, _, count = read_preview(ds["csv"])
        recommended_items.append(f"""<li><b>{rank}. <a href="datasets/{ds['id']}.html">{html.escape(ds['title'])}</a></b> <span class="badge">{count} rows</span><br>{html.escape(RECOMMENDED_CANDIDATE_REASONS[dataset_id])}</li>""")
    index = f'''
<h1>초·중·고 정보 교육을 위한 무료 데이터 과학 API & CSV</h1>
<p>교육적 가치가 높은 무료 데이터셋을 골라, 바로 열어 보고 시각화하고 수업 예제로 바꿀 수 있게 정리했습니다. 팩트풀니스처럼 장기 변화가 중요한 자료는 1960년대부터의 긴 흐름을 우선 보여 주고, 날씨·대기질처럼 최근성이 중요한 자료는 최근 데이터 중심으로 제공합니다.</p>
<p>데이터별 페이지에서 CSV 직접 열기, 원천 API 확인, 브라우저 시각화, Streamlit 기본 코드, Pico 2 WH + Grove Shield 기본 코드를 확인할 수 있습니다.</p>
<p><a href="examples/factfulness-literacy.html">팩트풀니스 데이터 리터러시 수업</a> · <a href="examples/sdg-topics.html">지속가능발전 주제 데이터 10가지</a> · <a href="examples/svg-map-visualization.html">SVG 지도 시각화 예제</a> · <a href="https://github.com/thinkervis/free-api-data-science-edu">GitHub 저장소</a> · <a href="https://github.com/thinkervis/free-api-data-science-edu/blob/main/CONTRIBUTING.md">기여 안내</a></p>
<h2>추천 데이터 10가지</h2>
<p>처음 방문한 선생님과 학생이 바로 써 보기 좋은 데이터부터 골랐습니다.</p>
<ol>{''.join(recommended_items)}</ol>
<h2>지속가능발전(SDG) 주제 데이터 10가지</h2>
<p>기후·대기질·생물다양성·도시 이동·건강 형평성 등 SDG 수업용 주제는 <a href="examples/sdg-topics.html">별도 페이지</a>로 분리했습니다.</p>
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
