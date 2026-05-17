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
        "auth": "키 없음",
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
        "auth": "키 없음",
        "streamlit": "높음",
        "note": "시간별 데이터라 CSV가 커서 최근 일부 기간부터 다루는 예제로 권장",
    },
    {
        "id": "worldbank-korea",
        "title": "한국 5년 World Bank 지표",
        "category": "인구/경제/교육/보건",
        "csv": "worldbank_korea_indicators.csv",
        "source": "World Bank Indicators API",
        "doc_url": "https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation",
        "test_url": "https://api.worldbank.org/v2/country/KOR/indicator/SP.POP.TOTL?format=json&date=2021:2025",
        "auth": "키 없음",
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
        "auth": "키 없음",
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
        "auth": "키 없음",
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
        "auth": "키 없음",
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
        "auth": "키 없음",
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
        "auth": "키 없음",
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
        "auth": "키 없음",
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
        "auth": "샘플키 가능 · 안정 사용은 무료 API 키 권장",
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
        "auth": "키 없음",
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
        "auth": "키 없음",
        "streamlit": "높음",
        "note": "날짜/캘린더/지역 문화 수업에 적합. --scope all은 1970년 이후 연도별 조회",
    },
    {
        "id": "spacex-launches",
        "title": "SpaceX 발사 기록",
        "category": "우주/과학",
        "csv": "spacex_launches.csv",
        "source": "Launch Library 2",
        "doc_url": "https://ll.thespacedevs.com/2.2.0/swagger/",
        "test_url": "https://ll.thespacedevs.com/2.2.0/launch/previous/?search=SpaceX&limit=3",
        "auth": "키 없음",
        "streamlit": "높음",
        "note": "최신 발사를 포함한 최근 6년치 SpaceX 발사 기록. 연도별 발사 빈도·성공 여부·임무 유형 분석에 적합",
    },
    {
        "id": "frankfurter-usd-krw",
        "title": "USD/KRW 환율 일별",
        "category": "경제/환율",
        "csv": "frankfurter_usd_krw_daily.csv",
        "source": "Frankfurter Exchange Rates API",
        "doc_url": "https://www.frankfurter.app/docs/",
        "test_url": "https://api.frankfurter.app/2021-01-01..2021-01-05?from=USD&to=KRW",
        "auth": "키 없음",
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
        "auth": "키 없음",
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
        "auth": "키 없음",
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
        "auth": "DEMO_KEY 가능 · 안정 사용은 무료 API 키 권장",
        "streamlit": "높음",
        "note": "전력 수요/공급/에너지 데이터 수업용. DEMO_KEY 제한을 명시하고 무료 키 사용 권장",
    },
    {
        "id": "noaa-coops-seattle-water-level",
        "title": "NOAA 시애틀 조위 관측",
        "category": "해양/기후/시계열",
        "csv": "noaa_coops_seattle_water_level.csv",
        "source": "NOAA CO-OPS API",
        "doc_url": "https://api.tidesandcurrents.noaa.gov/api/prod/",
        "test_url": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date=20240501&end_date=20240503&station=9447130&product=water_level&datum=MLLW&time_zone=gmt&units=metric&format=json",
        "auth": "키 없음",
        "streamlit": "높음",
        "note": "해수면·조위 변화를 시간축으로 읽고 해안 도시와 기후 적응을 토론하는 수업용 샘플",
    },
    {
        "id": "gb-carbon-intensity",
        "title": "영국 전력 탄소집약도",
        "category": "에너지/탄소/기후",
        "csv": "gb_carbon_intensity.csv",
        "source": "UK Carbon Intensity API",
        "doc_url": "https://carbon-intensity.github.io/api-definitions/",
        "test_url": "https://api.carbonintensity.org.uk/intensity/date/2024-05-01",
        "auth": "키 없음",
        "streamlit": "높음",
        "note": "30분 단위 전력 탄소집약도를 보고 전기 사용 시간대와 탄소 배출의 관계를 탐구",
    },
    {
        "id": "citi-bike-stations",
        "title": "뉴욕 Citi Bike 대여소 스냅샷",
        "category": "대중교통/도시/탄소",
        "csv": "citi_bike_station_snapshot.csv",
        "source": "Citi Bike GBFS",
        "doc_url": "https://www.citibikenyc.com/system-data",
        "test_url": "https://gbfs.citibikenyc.com/gbfs/en/station_status.json",
        "auth": "키 없음",
        "streamlit": "높음",
        "note": "자전거 대여소별 잔여 자전거와 거치대를 지도/막대그래프로 보고 도시 이동을 분석",
    },
    {
        "id": "met-museum-sunflower",
        "title": "Met Museum 해바라기 작품 샘플",
        "category": "문화/예술/메타데이터",
        "csv": "met_museum_sunflower_objects.csv",
        "source": "Metropolitan Museum of Art Collection API",
        "doc_url": "https://metmuseum.github.io/",
        "test_url": "https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&q=sunflower",
        "auth": "키 없음",
        "streamlit": "높음",
        "note": "작품 주제·제작연도·부서 메타데이터로 예술 데이터 검색과 분류 활동을 구성",
    },
    {
        "id": "cdc-places-health",
        "title": "CDC PLACES 지역 건강 지표 샘플",
        "category": "보건/지역/공공데이터",
        "csv": "cdc_places_health_sample.csv",
        "source": "CDC Socrata Open Data API",
        "doc_url": "https://dev.socrata.com/",
        "test_url": "https://data.cdc.gov/resource/cwsq-ngmh.json?$limit=5",
        "auth": "토큰 선택 / 소량 조회 불필요",
        "streamlit": "높음",
        "note": "지역별 건강 지표를 비교하며 보건 격차와 데이터 기반 정책 질문을 만드는 샘플",
    },
    {
        "id": "osm-seoul-hospitals",
        "title": "OpenStreetMap 서울 병원 위치",
        "category": "지도/보건/도시",
        "csv": "osm_seoul_hospitals.csv",
        "source": "OpenStreetMap Overpass API",
        "doc_url": "https://wiki.openstreetmap.org/wiki/Overpass_API",
        "test_url": "https://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%5Btimeout%3A10%5D%3Bnode%5Bamenity%3Dhospital%5D%2837.4%2C126.8%2C37.7%2C127.2%29%3Bout%205%3B",
        "auth": "불필요 / 사용 정책 준수",
        "streamlit": "높음",
        "note": "서울 병원 위치를 지도에 표시하고 의료 접근성·생활권 분석 수업으로 연결",
    },
    {
        "id": "nominatim-seoul-landmarks",
        "title": "Nominatim 서울 주요 장소 지오코딩",
        "category": "지도/지오코딩/위치",
        "csv": "nominatim_seoul_landmarks.csv",
        "source": "OpenStreetMap Nominatim",
        "doc_url": "https://nominatim.org/release-docs/latest/api/Search/",
        "test_url": "https://nominatim.openstreetmap.org/search?q=Seoul%20City%20Hall&format=json&limit=3",
        "auth": "불필요 / 사용 정책 준수",
        "streamlit": "높음",
        "note": "장소 이름을 위도·경도로 바꾸는 과정을 통해 지도 데이터 전처리를 설명",
    },

    {
        "id": "seoul-realtime-citydata",
        "title": "서울 실시간 도시데이터 샘플",
        "category": "도시/혼잡도/안전",
        "csv": "seoul_realtime_citydata_sample.csv",
        "source": "서울 열린데이터광장 실시간 도시데이터",
        "doc_url": "https://data.seoul.go.kr/dataList/OA-21285/S/1/datasetView.do",
        "test_url": "http://openapi.seoul.go.kr:8088/sample/json/citydata/1/5/%EA%B4%91%ED%99%94%EB%AC%B8%C2%B7%EB%8D%95%EC%88%98%EA%B6%81",
        "auth": "샘플키 가능 · 안정 사용은 무료 API 키 권장",
        "streamlit": "높음",
        "note": "서울 주요 장소의 혼잡도와 추정 인구를 비교해 안전한 방문 시간·도시 운영 질문으로 연결",
    },
    {
        "id": "seoul-realtime-air-quality",
        "title": "서울 실시간 대기질 샘플",
        "category": "대기질/건강/환경",
        "csv": "seoul_realtime_air_quality.csv",
        "source": "서울 열린데이터광장 실시간 대기환경",
        "doc_url": "https://data.seoul.go.kr/",
        "test_url": "http://openapi.seoul.go.kr:8088/sample/json/RealtimeCityAir/1/5/",
        "auth": "샘플키 가능 · 안정 사용은 무료 API 키 권장",
        "streamlit": "높음",
        "note": "권역·측정소별 PM10/PM2.5와 통합대기환경지수를 비교해 건강·환경 수업에 활용",
    },


]

TOP_RECOMMENDATIONS = [
    {
        "id": "open-meteo-weather",
        "why": "가장 수업 전환이 쉽고, 학생 생활 경험과 바로 연결되는 입문용 시계열입니다.",
        "perspective": "‘올해가 정말 더웠나?’처럼 체감과 데이터를 비교하는 질문에서 출발합니다.",
        "visualization": "최고·평균·최저기온 선그래프, 월별 평균 막대그래프, 강수량이 많은 날 강조 표시.",
        "use": "CSV를 불러온 뒤 날짜를 월/계절로 변환해 평균·최댓값·극단값을 계산합니다.",
        "analysis": "이동평균, 계절별 비교, 폭염일/강수일 조건 필터링으로 ‘기후’와 ‘날씨’를 구분해 봅니다.",
    },
    {
        "id": "open-meteo-air-quality",
        "why": "행 수가 많아 ‘시간별 데이터’의 장점과 전처리 필요성을 함께 보여 주기 좋습니다.",
        "perspective": "등교 시간, 점심시간, 야외활동 시간대의 미세먼지 차이를 생활 안전 문제로 다룹니다.",
        "visualization": "PM10·PM2.5 시간별 선그래프, 일평균 집계 그래프, 나쁨 기준선을 넣은 위험 구간 표시.",
        "use": "시간별 원자료를 그대로 그리기보다 일/주 단위로 묶어 노이즈를 줄입니다.",
        "analysis": "리샘플링, 기준 초과 횟수 세기, PM10과 PM2.5 상관관계 비교를 추천합니다.",
    },
    {
        "id": "nasa-power-seoul",
        "why": "NASA 공식 데이터라는 신뢰도와 기상·에너지 융합성이 강합니다.",
        "perspective": "태양광 발전, 냉난방 수요, 강수·풍속을 연결해 ‘에너지 계획’ 관점으로 읽습니다.",
        "visualization": "기온·강수·풍속 다중 축 그래프, 월별 일사/기온 비교, 결측값 제외 전후 비교.",
        "use": "날짜별 관측치를 월 단위로 집계하고, 단위가 다른 열은 축을 분리하거나 표준화합니다.",
        "analysis": "상관분석, 계절성 비교, 결측값(-999 계열)을 왜 0으로 처리하면 안 되는지 토론합니다.",
    },
    {
        "id": "frankfurter-usd-krw",
        "why": "경제 뉴스와 연결하기 쉽고, 단일 지표라 시계열 분석 입문에 적합합니다.",
        "perspective": "환율 상승/하락이 해외직구·여행·수입물가에 어떤 의미인지 해석합니다.",
        "visualization": "환율 선그래프, 전일 대비 변화율 막대그래프, 특정 뉴스일 전후 구간 확대.",
        "use": "원 환율뿐 아니라 변화량과 변화율 열을 새로 만들어 분석합니다.",
        "analysis": "최댓값/최솟값 찾기, 변동성 계산, 이동평균으로 단기 흔들림과 추세를 구분합니다.",
    },
    {
        "id": "usgs-earthquakes",
        "why": "지도와 과학 탐구가 결합되어 학생 흥미가 높고 위치 데이터 개념을 설명하기 좋습니다.",
        "perspective": "지진은 무작위로 흩어지는가, 판 경계 주변에 모이는가를 데이터로 확인합니다.",
        "visualization": "위도·경도 지도 산점도, 규모별 점 크기, 깊이별 색상, 지역별 발생 수 막대그래프.",
        "use": "위도·경도·규모·깊이 열을 골라 지도에 표시하고, 규모 기준을 바꿔 결과를 비교합니다.",
        "analysis": "공간 패턴 읽기, 규모와 깊이의 관계, 필터 조건에 따라 결론이 달라지는 점을 다룹니다.",
    },
    {
        "id": "factfulness-global",
        "why": "단순 최신 수치보다 ‘오래된 상식이 데이터와 어떻게 어긋나는가’를 보여 주는 힘이 큽니다.",
        "perspective": "팩트풀니스식 질문으로 세계가 나빠지기만 했다는 직관을 장기 데이터로 검증합니다.",
        "visualization": "국가별 기대수명 장기 선그래프, 지표별 최신값 막대그래프, 첫해=100 변화율 그래프.",
        "use": "국가·지표·연도를 필터링해 같은 질문을 여러 지표로 반복 검증합니다.",
        "analysis": "장기 추세, 국가 간 비교, 기준연도 선택 효과, 결측 연도가 해석에 미치는 영향을 봅니다.",
    },
    {
        "id": "spacex-launches",
        "why": "최신 발사를 포함한 최근 6년치로 갱신하면 우주 산업의 변화 속도를 직접 볼 수 있습니다.",
        "perspective": "SpaceX 발사 횟수가 해마다 어떻게 늘었고, 어떤 임무 유형이 많아졌는지 묻습니다.",
        "visualization": "연도별 발사 횟수 막대그래프, 성공/실패 비율, 로켓·임무 유형별 누적 막대그래프.",
        "use": "Launch Library 2에서 최신 이전 발사를 가져와 날짜·상태·로켓·임무 유형을 CSV로 정리합니다.",
        "analysis": "연도별 빈도, 성공률, 임무 유형 변화, 최신 데이터 출처가 분석 흥미에 미치는 영향을 함께 다룹니다.",
    },
    {
        "id": "gbif-korea",
        "why": "한국 안의 실제 생물 관측 위치라 생태·지역 탐구 프로젝트로 확장하기 좋습니다.",
        "perspective": "우리 지역에는 어떤 생물이 기록되어 있고, 관측은 어디에 집중되는지 질문합니다.",
        "visualization": "한국 지도 산점도, 종별 관측 수 막대그래프, 관측 월/지역 분포 그래프.",
        "use": "좌표가 있는 관측만 사용하고, 종명·지역·날짜 기준으로 필터링합니다.",
        "analysis": "관측 편향, 표본 수 한계, 도시/산림/해안 지역 차이를 데이터 품질 관점에서 해석합니다.",
    },
    {
        "id": "restcountries-world",
        "why": "시계열은 아니지만 국가 단위 비교·지도·산점도 활동의 출발점으로 안정적입니다.",
        "perspective": "‘큰 나라가 항상 인구도 많은가?’처럼 지리 상식을 데이터로 확인합니다.",
        "visualization": "면적-인구 로그 산점도, 대륙별 국가 수 막대그래프, 위치 기반 세계 지도.",
        "use": "인구·면적·지역 열을 골라 로그 축을 적용하고, 극단값을 따로 표시합니다.",
        "analysis": "비율 계산, 로그 스케일의 필요성, 스냅샷 데이터와 시계열 데이터의 차이를 설명합니다.",
    },
]

EXCLUDED_FROM_TOP = [
    {
        "id": "nager-korea-holidays",
        "reason": "초급 날짜 처리 예제로는 좋지만 분석 질문이 얕아 top 추천보다는 보조 예제로 두는 편이 적절합니다.",
    },
    {
        "id": "worldbank-korea",
        "reason": "행 수가 20개라 빠른 비교에는 좋지만, 장기 변화와 수업 질문은 factfulness-global 데이터가 더 강합니다.",
    },
]


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

    "noaa-coops-seattle-water-level": {"kind": "line", "title": "시애틀 조위 변화", "x": "time_utc", "y": ["water_level_m"], "labels": ["수위(m)"], "y_title": "수위(m)"},
    "gb-carbon-intensity": {"kind": "line", "title": "영국 전력 탄소집약도 변화", "x": "from_utc", "y": ["forecast_gco2_kwh", "actual_gco2_kwh"], "labels": ["예측(gCO₂/kWh)", "실측(gCO₂/kWh)"], "y_title": "gCO₂/kWh", "max_points": 1000},
    "citi-bike-stations": {"kind": "scattergeo", "title": "Citi Bike 대여소별 자전거 가용성", "lat": "latitude", "lon": "longitude", "size": "num_bikes_available", "color": "capacity", "hover": "name"},
    "met-museum-sunflower": {"kind": "histogram", "title": "해바라기 관련 작품 제작연도 분포", "x": "objectEndDate"},
    "cdc-places-health": {"kind": "bar", "title": "CDC PLACES 건강 지표 샘플", "x": "state", "y": "data_value"},
    "osm-seoul-hospitals": {"kind": "scattergeo", "title": "서울 병원 위치", "lat": "latitude", "lon": "longitude", "hover": "name", "geo_scope": "korea"},
    "nominatim-seoul-landmarks": {"kind": "scattergeo", "title": "서울 주요 장소 지오코딩 결과", "lat": "latitude", "lon": "longitude", "hover": "query", "geo_scope": "korea"},

    "seoul-realtime-citydata": {"kind": "bar", "title": "서울 주요 장소 추정 인구 상한", "x": "area_name", "y": "max_population"},
    "seoul-realtime-air-quality": {"kind": "bar", "title": "서울 측정소별 통합대기환경지수", "x": "station", "y": "cai_index"},
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
        "auth": "키 없음",
        "activity": "PM10·PM2.5 시간별 변화를 보고 등하교/야외활동 안내 대시보드 만들기",
    },
    {
        "title": "폭염일·열대야와 학교 에너지 사용",
        "sdg": "SDG 7 깨끗한 에너지 · SDG 13 기후행동",
        "data": "NASA POWER 서울 일별 기상/에너지",
        "url": "https://power.larc.nasa.gov/docs/services/api/",
        "auth": "키 없음",
        "activity": "기온·강수·풍속을 분석해 폭염 경보 기준과 냉방 에너지 절약 캠페인 설계",
    },
    {
        "title": "한국과 세계의 CO₂ 배출 변화",
        "sdg": "SDG 12 책임 있는 소비와 생산 · SDG 13 기후행동",
        "data": "Our World in Data CO₂ Grapher CSV",
        "url": "https://docs.owid.io/projects/etl/api/",
        "auth": "키 없음",
        "activity": "한국/세계 CO₂ 배출량을 비교하고 1인당 감축 아이디어를 데이터 근거로 제안",
    },
    {
        "title": "생물다양성 관측으로 보는 우리 주변 생태계",
        "sdg": "SDG 14 해양생태계 · SDG 15 육상생태계",
        "data": "GBIF 한국 생물종 관측",
        "url": "https://techdocs.gbif.org/en/openapi/",
        "auth": "키 없음",
        "activity": "한국 지도 위 관측 위치를 찍고 도시/해안/산림별 생물종 관측 차이 탐구",
    },
    {
        "title": "따릉이와 탄소 줄이는 통학·이동",
        "sdg": "SDG 9 산업·혁신·인프라 · SDG 11 지속가능한 도시",
        "data": "서울 열린데이터광장 따릉이 실시간 대여정보",
        "url": "https://data.seoul.go.kr/",
        "auth": "샘플키 가능 · 안정 사용은 무료 API 키 권장",
        "activity": "대여소별 자전거 수를 시각화하고 짧은 거리 자동차 이동 대체 효과 추정",
    },
    {
        "title": "도시 혼잡도와 안전한 공공공간",
        "sdg": "SDG 10 불평등 감소 · SDG 11 지속가능한 도시",
        "data": "서울 실시간 도시데이터",
        "url": "https://data.seoul.go.kr/dataList/OA-21285/S/1/datasetView.do",
        "auth": "샘플키 가능 · 무료 API 키 권장",
        "activity": "주요 장소 혼잡도를 비교해 안전한 방문 시간 추천 또는 행사 운영 아이디어 만들기",
    },
    {
        "title": "인구·교육·경제 지표로 보는 지속가능한 사회",
        "sdg": "SDG 4 양질의 교육 · SDG 8 양질의 일자리와 경제성장",
        "data": "World Bank 한국 지표",
        "url": "https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation",
        "auth": "키 없음",
        "activity": "인구·GDP·기대수명·교육 지표를 함께 보고 지속가능발전 지표 카드 만들기",
    },
    {
        "title": "팩트풀니스 데이터 최신화: 오래된 상식 검증",
        "sdg": "SDG 1 빈곤 종식 · SDG 3 건강과 웰빙 · SDG 4 양질의 교육 · SDG 7 깨끗한 에너지",
        "data": "World Bank 최신 세계 지표 CSV: 기대수명, 5세 미만 사망률, 전기 접근성, 1인당 GDP, 초등교육 이수율",
        "url": "https://www.gapminder.org/data/",
        "auth": "키 없음",
        "activity": "학생 예상값을 먼저 적고 최신 데이터와 비교해 '세상은 생각보다 어떻게 달라졌나'를 시각화",
    },
    {
        "title": "물 사용량과 가뭄·절수 행동 데이터",
        "sdg": "SDG 6 깨끗한 물과 위생 · SDG 12 책임 있는 소비와 생산",
        "data": "공공데이터포털/지자체 상수도 사용량·수질·가뭄 관련 데이터",
        "url": "https://www.data.go.kr/",
        "auth": "이용 조건은 데이터별 상이 · 일부는 파일 다운로드, 일부는 공공데이터포털 API 키 필요",
        "activity": "지역별 물 사용량·강수량·가뭄 정보를 비교하고 학교/가정 절수 캠페인 근거 만들기",
    },
    {
        "title": "전력 수요와 재생에너지 전환 토론",
        "sdg": "SDG 7 깨끗한 에너지 · SDG 13 기후행동",
        "data": "EIA Open Data 전력 일별 데이터",
        "url": "https://www.eia.gov/opendata/documentation.php",
        "auth": "DEMO_KEY 가능 · 안정 사용은 무료 API 키 권장",
        "activity": "전력 수요·공급 시계열을 보고 태양광/풍력 확대가 필요한 시간대 추론",
    },
]


COLUMN_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "open_meteo_seoul_daily_weather.csv": {
        "location": "이 저장소에서 붙인 관측 위치 이름입니다.",
        "latitude": "요청 지점의 위도입니다.",
        "longitude": "요청 지점의 경도입니다.",
        "time": "일별 관측 날짜입니다.",
        "temperature_2m_max": "지상 2m 기준 일 최고기온입니다.",
        "temperature_2m_min": "지상 2m 기준 일 최저기온입니다.",
        "temperature_2m_mean": "지상 2m 기준 일 평균기온입니다.",
        "precipitation_sum": "하루 동안의 강수량 합계입니다.",
        "wind_speed_10m_max": "지상 10m 기준 일 최대 풍속입니다.",
    },
    "open_meteo_seoul_air_quality_hourly.csv": {
        "location": "이 저장소에서 붙인 측정 위치 이름입니다.",
        "latitude": "요청 지점의 위도입니다.",
        "longitude": "요청 지점의 경도입니다.",
        "time": "시간별 대기질 데이터의 기준 시각입니다.",
        "pm10": "PM10 미세먼지 농도입니다.",
        "pm2_5": "PM2.5 초미세먼지 농도입니다.",
        "carbon_monoxide": "일산화탄소 농도입니다.",
        "nitrogen_dioxide": "이산화질소 농도입니다.",
        "ozone": "오존 농도입니다.",
    },
    "worldbank_korea_indicators.csv": {
        "country": "World Bank가 제공하는 국가 이름입니다.",
        "countryiso3code": "국가 ISO 3자리 코드입니다.",
        "indicator_id": "World Bank 지표 코드입니다.",
        "indicator": "World Bank 지표 이름입니다.",
        "date": "지표 값의 기준 연도입니다.",
        "value": "해당 국가·연도·지표의 값입니다.",
    },
    "factfulness_global_indicators.csv": {
        "country": "World Bank가 제공하는 국가/지역 이름입니다.",
        "countryiso3code": "국가/지역 ISO 3자리 코드입니다.",
        "indicator_id": "World Bank 지표 코드입니다.",
        "indicator": "World Bank 지표 이름입니다.",
        "date": "지표 값의 기준 연도입니다.",
        "value": "해당 국가/지역·연도·지표의 값입니다.",
        "factfulness_question": "이 저장소에서 수업 질문과 연결하기 위해 붙인 분류 문구입니다.",
    },
    "usgs_major_earthquakes.csv": {
        "id": "USGS 지진 이벤트 식별자입니다.",
        "time_utc": "지진 발생 시각입니다(UTC).",
        "magnitude": "USGS가 제공하는 지진 규모 값입니다.",
        "place": "USGS가 제공하는 발생 위치 설명입니다.",
        "longitude": "지진 위치의 경도입니다.",
        "latitude": "지진 위치의 위도입니다.",
        "depth_km": "진원 깊이입니다(km).",
        "type": "USGS 이벤트 유형입니다.",
        "url": "USGS 상세 페이지 URL입니다.",
    },
    "mlb_schedule.csv": {
        "date": "경기 일정의 날짜입니다.",
        "gamePk": "MLB Stats API의 경기 고유 식별자입니다.",
        "gameDate": "경기 시작 일시입니다.",
        "season": "경기가 속한 시즌 연도입니다.",
        "gameType": "MLB Stats API의 경기 유형 코드입니다.",
        "status": "경기 진행 상태입니다.",
        "away_team": "원정 팀 이름입니다.",
        "home_team": "홈 팀 이름입니다.",
        "away_score": "원정 팀 점수입니다.",
        "home_score": "홈 팀 점수입니다.",
    },
    "fred_fedfunds.csv": {
        "observation_date": "FRED 관측 날짜입니다.",
        "FEDFUNDS": "FRED의 Effective Federal Funds Rate 계열 값입니다.",
    },
    "owid_co2_korea_world.csv": {
        "Entity": "Our World in Data의 국가/지역 이름입니다.",
        "Code": "국가/지역 코드입니다.",
        "Year": "자료의 기준 연도입니다.",
        "Annual CO₂ emissions": "연간 이산화탄소 배출량 값입니다.",
    },
    "gbif_korea_occurrences_sample.csv": {
        "key": "GBIF occurrence 고유 키입니다.",
        "scientificName": "학명입니다.",
        "vernacularName": "일반명/국명입니다. 원천에 값이 없을 수 있습니다.",
        "eventDate": "관측 또는 채집 이벤트 날짜입니다.",
        "year": "관측 또는 채집 이벤트 연도입니다.",
        "country": "관측 국가입니다.",
        "locality": "관측 지역 설명입니다.",
        "decimalLatitude": "십진수 위도입니다.",
        "decimalLongitude": "십진수 경도입니다.",
        "basisOfRecord": "GBIF 기록 근거 유형입니다.",
    },
    "artic_recent_artworks_sample.csv": {
        "_score": "Art Institute of Chicago API 검색 결과의 관련도 점수입니다.",
        "id": "작품 고유 식별자입니다.",
        "title": "작품 제목입니다.",
        "date_start": "작품 제작 시작 연도입니다.",
        "date_end": "작품 제작 종료 연도입니다.",
        "medium_display": "작품 재료/기법 설명입니다.",
        "artist_title": "작가 이름입니다.",
        "place_of_origin": "작품의 출처/제작 지역입니다.",
    },
    "seoul_bike_sample.csv": {
        "rackTotCnt": "대여소의 전체 거치대 수입니다.",
        "stationName": "따릉이 대여소 이름입니다.",
        "parkingBikeTotCnt": "현재 대여 가능한 자전거 수입니다.",
        "shared": "서울 열린데이터광장 응답의 shared 필드 값입니다.",
        "stationLatitude": "대여소 위도입니다.",
        "stationLongitude": "대여소 경도입니다.",
        "stationId": "대여소 식별자입니다.",
    },
    "nasa_power_seoul_daily.csv": {
        "location": "이 저장소에서 붙인 관측 위치 이름입니다.",
        "date": "일별 자료의 기준 날짜입니다.",
        "temperature_2m_c": "NASA POWER T2M 값을 섭씨로 저장한 일 평균 기온입니다.",
        "temperature_max_c": "NASA POWER T2M_MAX 값을 섭씨로 저장한 일 최고기온입니다.",
        "temperature_min_c": "NASA POWER T2M_MIN 값을 섭씨로 저장한 일 최저기온입니다.",
        "precipitation_mm_day": "NASA POWER PRECTOTCORR 값을 mm/day 단위로 저장한 강수량입니다.",
        "wind_speed_2m_m_s": "NASA POWER WS2M 값을 m/s 단위로 저장한 2m 풍속입니다.",
    },
    "bls_us_cpi_monthly.csv": {
        "series_id": "BLS 시계열 식별자입니다.",
        "year": "자료의 기준 연도입니다.",
        "month": "자료의 기준 월 코드입니다.",
        "date": "이 저장소에서 year와 month로 만든 월별 날짜입니다.",
        "cpi_value": "소비자물가지수(CPI) 값입니다.",
        "footnotes": "BLS 응답에 포함된 주석/각주입니다.",
    },
    "nager_korea_public_holidays.csv": {
        "date": "공휴일 날짜입니다.",
        "localName": "현지 언어 공휴일 이름입니다.",
        "name": "영문 공휴일 이름입니다.",
        "countryCode": "국가 코드입니다.",
        "global": "전국 공휴일 여부입니다.",
        "types": "Nager.Date API가 제공하는 공휴일 유형 목록입니다.",
    },
    "spacex_launches.csv": {
        "flight_number": "발사 번호입니다.",
        "name": "발사 임무 이름입니다.",
        "date_utc": "발사 예정/실제 일시입니다(UTC).",
        "success": "발사 성공 여부입니다. 값이 비어 있으면 원천에서 확정되지 않은 상태일 수 있습니다.",
        "status": "Launch Library 2가 제공하는 발사 상태 이름입니다.",
        "rocket": "로켓 이름입니다.",
        "mission_type": "임무 유형입니다.",
        "orbit": "목표 궤도 이름입니다.",
        "pad": "발사대 이름입니다.",
        "location": "발사 장소 이름입니다.",
        "details": "임무 설명입니다.",
        "wikipedia": "관련 Wikipedia URL입니다.",
        "webcast": "관련 영상/중계 URL입니다.",
    },
    "frankfurter_usd_krw_daily.csv": {
        "date": "환율 기준 날짜입니다.",
        "base": "기준 통화입니다.",
        "quote": "상대 통화입니다.",
        "rate": "기준 통화 1단위에 대한 상대 통화 환율입니다.",
    },
    "who_korea_life_expectancy.csv": {
        "indicator": "WHO GHO 지표 코드입니다.",
        "year": "자료의 기준 연도입니다.",
        "country": "국가 코드 또는 국가 식별 값입니다.",
        "sex": "성별 구분입니다.",
        "value": "지표의 수치 값입니다.",
        "display": "WHO API가 제공하는 표시용 값입니다.",
    },
    "restcountries_world_snapshot.csv": {
        "name": "국가의 일반 이름입니다.",
        "official_name": "국가의 공식 이름입니다.",
        "cca3": "ISO 3166-1 alpha-3 국가 코드입니다.",
        "region": "대륙/권역 분류입니다.",
        "subregion": "세부 권역 분류입니다.",
        "population": "REST Countries가 제공하는 인구 값입니다.",
        "area": "국가 면적입니다.",
        "latitude": "국가 대표 좌표의 위도입니다.",
        "longitude": "국가 대표 좌표의 경도입니다.",
    },
    "eia_california_electricity_daily.csv": {
        "date": "전력 데이터의 기준 날짜입니다.",
        "respondent": "EIA respondent 코드입니다.",
        "respondent_name": "EIA respondent 이름입니다.",
        "type": "EIA 전력 데이터 유형 코드입니다.",
        "type_name": "EIA 전력 데이터 유형 이름입니다.",
        "value": "해당 날짜·유형의 전력 데이터 값입니다.",
        "unit": "값의 단위입니다.",
    },
    "noaa_coops_seattle_water_level.csv": {
        "station_id": "NOAA CO-OPS 관측소 ID입니다.",
        "station_name": "이 저장소에서 붙인 관측소 이름입니다.",
        "time_utc": "관측 시각입니다(UTC).",
        "water_level_m": "수위 관측값입니다(m).",
        "sigma": "NOAA 응답의 sigma 값입니다.",
        "quality": "NOAA 응답의 품질 플래그입니다.",
    },
    "gb_carbon_intensity.csv": {
        "from_utc": "탄소집약도 구간 시작 시각입니다.",
        "to_utc": "탄소집약도 구간 종료 시각입니다.",
        "forecast_gco2_kwh": "예측 전력 탄소집약도입니다(gCO₂/kWh).",
        "actual_gco2_kwh": "실측 전력 탄소집약도입니다(gCO₂/kWh).",
        "index": "Carbon Intensity API가 제공하는 등급 문자열입니다.",
    },
    "citi_bike_station_snapshot.csv": {
        "station_id": "GBFS 대여소 식별자입니다.",
        "name": "대여소 이름입니다.",
        "latitude": "대여소 위도입니다.",
        "longitude": "대여소 경도입니다.",
        "capacity": "대여소 총 거치 용량입니다.",
        "num_bikes_available": "현재 이용 가능한 자전거 수입니다.",
        "num_docks_available": "현재 비어 있는 거치대 수입니다.",
        "is_renting": "현재 대여 가능 여부를 나타내는 GBFS 상태 값입니다.",
    },
    "met_museum_sunflower_objects.csv": {
        "objectID": "Met Collection API의 작품 고유 식별자입니다.",
        "title": "작품 제목입니다.",
        "artistDisplayName": "작가 표시 이름입니다.",
        "objectDate": "작품 제작 시기 표시 문자열입니다.",
        "objectBeginDate": "작품 제작 시작 연도입니다.",
        "objectEndDate": "작품 제작 종료 연도입니다.",
        "department": "소장 부서입니다.",
        "culture": "문화권/문화 분류입니다.",
        "repository": "소장 기관 정보입니다.",
        "objectURL": "Met 작품 상세 페이지 URL입니다.",
    },
    "cdc_places_health_sample.csv": {
        "year": "자료의 기준 연도입니다.",
        "stateabbr": "미국 주 약어입니다.",
        "state": "미국 주 이름입니다.",
        "county": "카운티 이름입니다.",
        "measure": "CDC PLACES 건강 지표 이름입니다.",
        "data_value": "해당 지표의 값입니다.",
        "low_confidence_limit": "신뢰구간 하한입니다.",
        "high_confidence_limit": "신뢰구간 상한입니다.",
    },
    "osm_seoul_hospitals.csv": {
        "osm_id": "OpenStreetMap 객체 식별자입니다.",
        "name": "시설 이름입니다.",
        "amenity": "OpenStreetMap amenity 태그 값입니다.",
        "emergency": "OpenStreetMap emergency 태그 값입니다.",
        "latitude": "시설 위도입니다.",
        "longitude": "시설 경도입니다.",
    },
    "nominatim_seoul_landmarks.csv": {
        "query": "이 저장소가 Nominatim에 보낸 검색어입니다.",
        "display_name": "Nominatim이 반환한 표시용 장소 이름입니다.",
        "latitude": "검색 결과의 위도입니다.",
        "longitude": "검색 결과의 경도입니다.",
        "type": "Nominatim이 반환한 장소 유형입니다.",
        "importance": "Nominatim 검색 결과의 중요도 점수입니다.",
    },
    "seoul_realtime_citydata_sample.csv": {
        "area_name": "서울 실시간 도시데이터의 장소 이름입니다.",
        "area_code": "서울 실시간 도시데이터의 장소 코드입니다.",
        "congestion_level": "장소의 혼잡도 단계입니다.",
        "congestion_message": "혼잡도에 대한 설명 문구입니다.",
        "min_population": "추정 인구 최솟값입니다.",
        "max_population": "추정 인구 최댓값입니다.",
        "male_rate": "남성 비율입니다.",
        "female_rate": "여성 비율입니다.",
        "updated_at": "데이터 갱신 시각입니다.",
    },
    "seoul_realtime_air_quality.csv": {
        "measured_at": "대기질 측정 시각입니다.",
        "area": "측정 권역/지역 이름입니다.",
        "station": "측정소 이름입니다.",
        "pm10": "미세먼지(PM10) 농도입니다.",
        "pm25": "초미세먼지(PM2.5) 농도입니다.",
        "ozone": "오존 농도입니다.",
        "no2": "이산화질소 농도입니다.",
        "co": "일산화탄소 농도입니다.",
        "so2": "아황산가스 농도입니다.",
        "cai_grade": "통합대기환경지수 등급입니다.",
        "cai_index": "통합대기환경지수 값입니다.",
    },
}



def read_preview(csv_name: str, max_rows: int = 5) -> tuple[list[str], list[list[str]], list[list[str]], int]:
    path = DATA / csv_name
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return [], [], [], 0
    data_rows = rows[1:]
    return rows[0], data_rows[:max_rows], data_rows[-max_rows:] if len(data_rows) > max_rows else [], len(data_rows)


def streamlit_code(csv_name: str) -> str:
    return f'''import pandas as pd\nimport streamlit as st\n\nURL = "https://thinkervis.github.io/free-api-data-science-edu/data/{csv_name}"\n\nst.title("{csv_name}")\ndf = pd.read_csv(URL)\nst.write(df.shape)\nst.dataframe(df.head(100))\n\n# 숫자 컬럼이 있으면 빠르게 차트 확인\nnum_cols = df.select_dtypes("number").columns.tolist()\nif num_cols:\n    st.line_chart(df[num_cols[:3]])\n'''



def html_table(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in row) + "</tr>" for row in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def column_descriptions_table(ds: dict[str, str], headers: list[str]) -> str:
    descriptions = COLUMN_DESCRIPTIONS.get(ds["csv"], {})
    missing = [h for h in headers if h not in descriptions]
    if missing:
        raise ValueError(f"missing column descriptions for {ds['csv']}: {', '.join(missing)}")
    rows = "".join(
        f"<tr><td><code>{html.escape(h)}</code></td><td>{html.escape(descriptions[h])}</td></tr>"
        for h in headers
    )
    return f'''<div class="card">
  <h2>열 설명</h2>
  <p class="small-muted">공식 문서와 이 저장소의 데이터 생성 스크립트(<code>scripts/update_datasets.py</code>)에서 확인한 필드만 설명했습니다. 원천별 단위·코드 체계는 위의 공식 문서 링크를 함께 확인하세요.</p>
  <table><thead><tr><th>열</th><th>의미</th></tr></thead><tbody>{rows}</tbody></table>
</div>'''


def supabase_config_script() -> str:
    return '''<script>
// Optional public config for shared likes.
// To enable shared ranking, create docs/likes-config.js with:
// window.DATASET_LIKES_SUPABASE = { url: "https://YOUR_PROJECT.supabase.co", anonKey: "YOUR_PUBLIC_ANON_KEY" };
window.DATASET_LIKES_SUPABASE = window.DATASET_LIKES_SUPABASE || null;
</script>
<script src="likes-config.js"></script>'''


def likes_script() -> str:
    datasets = [
        {"id": ds["id"], "title": ds["title"], "category": ds["category"], "rows": read_preview(ds["csv"])[3]}
        for ds in DATASETS
    ]
    payload = json.dumps(datasets, ensure_ascii=False)
    return f'''<script>
const DATASETS_FOR_LIKES = {payload};
const LIKE_STORE_KEY = 'free-api-data-science-edu-liked-v1';
const LOCAL_COUNT_KEY = 'free-api-data-science-edu-local-counts-v1';
function readJson(key, fallback) {{ try {{ return JSON.parse(localStorage.getItem(key) || 'null') ?? fallback; }} catch (_) {{ return fallback; }} }}
function writeJson(key, value) {{ localStorage.setItem(key, JSON.stringify(value)); }}
function likedSet() {{ return new Set(readJson(LIKE_STORE_KEY, [])); }}
function localCounts() {{ return readJson(LOCAL_COUNT_KEY, {{}}); }}
function isSupabaseReady() {{ const c = window.DATASET_LIKES_SUPABASE; return !!(c && c.url && c.anonKey); }}
async function supabaseRequest(path, options={{}}) {{
  const c = window.DATASET_LIKES_SUPABASE;
  const headers = Object.assign({{apikey:c.anonKey, Authorization:'Bearer '+c.anonKey, 'Content-Type':'application/json'}}, options.headers || {{}});
  const r = await fetch(c.url.replace(/\/$/,'') + '/rest/v1/' + path, Object.assign({{}}, options, {{headers}}));
  if (!r.ok) throw new Error('Supabase HTTP ' + r.status);
  if (r.status === 204) return null;
  return r.json();
}}
async function fetchSharedCounts() {{
  if (!isSupabaseReady()) return null;
  const rows = await supabaseRequest('dataset_likes?select=dataset_id,likes');
  return Object.fromEntries(rows.map(r => [r.dataset_id, Number(r.likes) || 0]));
}}
async function incrementSharedCount(datasetId) {{
  if (!isSupabaseReady()) return null;
  const c = window.DATASET_LIKES_SUPABASE;
  const r = await fetch(c.url.replace(/\/$/,'') + '/rest/v1/rpc/increment_dataset_like', {{
    method:'POST', headers:{{apikey:c.anonKey, Authorization:'Bearer '+c.anonKey, 'Content-Type':'application/json'}}, body:JSON.stringify({{p_dataset_id:datasetId}})
  }});
  if (!r.ok) throw new Error('Supabase RPC HTTP ' + r.status);
  return r.json();
}}
function renderDatasetCards(counts={{}}, sortMode='default') {{
  const liked = likedSet();
  const list = DATASETS_FOR_LIKES.map((d, i) => Object.assign({{rank:i+1, likes:Number(counts[d.id])||0, liked:liked.has(d.id)}}, d));
  if (sortMode === 'likes') list.sort((a,b)=>(b.likes-a.likes)||a.title.localeCompare(b.title,'ko'));
  const wrap = document.getElementById('dataset-cards'); if (!wrap) return;
  wrap.innerHTML = list.map((d, i) => `
    <div class="card dataset-card" data-dataset-id="${{d.id}}" data-likes="${{d.likes}}">
      <h2>${{sortMode==='likes' ? `<span class="badge">#${{i+1}}</span> ` : ''}}<a href="datasets/${{d.id}}.html">${{d.title}}</a></h2>
      <p><span class="badge">${{d.category}}</span><span class="badge">${{d.rows}} rows</span></p>
      <p><button class="like-button" data-like-id="${{d.id}}" aria-pressed="${{d.liked ? 'true':'false'}}">${{d.liked ? '♥':'♡'}} 좋아요</button> <span class="like-count">${{d.likes}}명 관심</span></p>
    </div>`).join('');
}}
async function bootLikes() {{
  let shared = null;
  try {{ shared = await fetchSharedCounts(); }} catch (e) {{ console.warn('shared likes unavailable; local mode', e); }}
  let counts = shared || localCounts();
  renderDatasetCards(counts, document.getElementById('sort-mode')?.value || 'default');
  const status = document.getElementById('likes-status');
  if (status) status.textContent = isSupabaseReady() && shared ? '공용 좋아요 집계 사용 중' : '로컬 좋아요 모드: 이 브라우저 기준으로 저장됩니다';
  document.getElementById('sort-mode')?.addEventListener('change', e => renderDatasetCards(counts, e.target.value));
  document.getElementById('dataset-cards')?.addEventListener('click', async e => {{
    const btn = e.target.closest('[data-like-id]'); if (!btn) return;
    const id = btn.dataset.likeId; const liked = likedSet();
    if (liked.has(id)) return;
    liked.add(id); writeJson(LIKE_STORE_KEY, [...liked]);
    const local = localCounts(); local[id] = (Number(local[id]) || 0) + 1; writeJson(LOCAL_COUNT_KEY, local);
    counts[id] = (Number(counts[id]) || 0) + 1;
    renderDatasetCards(counts, document.getElementById('sort-mode')?.value || 'default');
    try {{
      const updated = await incrementSharedCount(id);
      if (updated && typeof updated === 'object') {{ counts[id] = Number(updated.likes) || counts[id]; renderDatasetCards(counts, document.getElementById('sort-mode')?.value || 'default'); }}
    }} catch (err) {{ console.warn('shared like failed; kept local like', err); }}
  }});
}}
document.addEventListener('DOMContentLoaded', bootLikes);
</script>'''


def layout(title: str, body: str) -> str:
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>
* {{ box-sizing: border-box; }}
html {{ overflow-x: hidden; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: clamp(1rem, 4vw, 2rem); line-height: 1.6; max-width: 1120px; overflow-x: hidden; padding-bottom: 4rem; }}
a {{ color: #0969da; overflow-wrap: anywhere; word-break: break-word; }}
h1, h2, h3, p, li, div {{ overflow-wrap: anywhere; word-break: normal; }}
.card {{ border: 1px solid #d0d7de; border-radius: 12px; padding: 1rem; margin: 1rem 0; max-width: 100%; min-width: 0; }}
select, button {{ max-width: 100%; }}
label {{ max-width: 100%; }}
table {{ border-collapse: collapse; width: 100%; overflow-x: auto; display: block; }}
th, td {{ border: 1px solid #d0d7de; padding: .4rem .6rem; font-size: .9rem; }}
th {{ background: #f6f8fa; }}
pre {{ background: #f6f8fa; padding: 1rem; overflow-x: auto; border-radius: 8px; max-width: 100%; }} code, pre {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
.badge {{ display: inline-block; background: #eef; border-radius: 12px; padding: .15rem .55rem; margin: 0 .25rem .25rem 0; max-width: 100%; white-space: normal; line-height: 1.35; vertical-align: top; overflow-wrap: anywhere; word-break: break-word; }}
button {{ padding: .5rem .8rem; border-radius: 8px; border: 1px solid #d0d7de; background: white; cursor: pointer; }}
@media (max-width: 760px) {{ body {{ width: auto; max-width: none; margin: .5rem; font-size: 15px; }} h1 {{ font-size:1.45rem; line-height:1.28; }} select, button {{ width: 100%; }} label {{ display: block; margin: .45rem 0; }} .js-plotly-plot, .plot-container, .svg-container {{ max-width: 100% !important; }} }}
.dataset-toolbar {{ display: flex; gap: .5rem; flex-wrap: wrap; align-items: center; margin: 1rem 0; }}
.dataset-card {{ position: relative; }}
.like-button {{ border-color: #ffb3c1; color: #c9184a; font-weight: 700; }}
.like-button[aria-pressed="true"] {{ background: #ffe3ec; border-color: #ff8fab; }}
.like-count, .small-muted {{ color: #6e7781; font-size: .9rem; }}
.recommendation-list {{ list-style: none; padding-left: 0; }}
.recommendation-card {{ border: 1px solid #d0d7de; border-radius: 12px; padding: 1rem; margin: 1rem 0; background: #fff; }}
.recommendation-card h3 {{ margin-top: 0; }}
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
  rate:'환율', FEDFUNDS:'미국 기준금리(%)', cpi_value:'소비자물가지수(CPI)', parkingBikeTotCnt:'주차 자전거 수', stationName:'대여소', home_team:'홈팀', date_utc:'발사일', date_end:'제작연도', sex:'성별', area:'면적', population:'인구', type_name:'전력 데이터 유형', Entity:'지역', water_level_m:'수위(m)', forecast_gco2_kwh:'예측 탄소집약도', actual_gco2_kwh:'실측 탄소집약도', data_value:'지표값', state:'주', max_population:'추정 인구 상한', area_name:'장소', cai_index:'통합대기환경지수', station:'측정소', objectEndDate:'제작연도', capacity:'거치 용량', num_bikes_available:'이용 가능 자전거', Entity:'지역',
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
    if (v <= -900) return null;
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
  Plotly.newPlot(chart, traces, layout, {responsive: true, displaylogo: false, displayModeBar: false});
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
    headers, head_rows, tail_rows, count = read_preview(ds["csv"])
    preview = f"<h3>Head: 처음 5행</h3>{html_table(headers, head_rows)}"
    if tail_rows:
        preview += f"<h3>Tail: 마지막 5행</h3>{html_table(headers, tail_rows)}"
    column_descriptions = column_descriptions_table(ds, headers)
    csv_url = f"../data/{ds['csv']}"
    body = f'''
<p><a href="../index.html">← 전체 목록</a></p>
<h1>{html.escape(ds['title'])}</h1>
<p><span class="badge">{html.escape(ds['category'])}</span><span class="badge">이용 조건: {html.escape(ds['auth'])}</span><span class="badge">행 수: {count}</span></p>
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
{column_descriptions}
<h2>Streamlit 기본 코드</h2>
<pre>{html.escape(streamlit_code(ds['csv']))}</pre>
{dataset_script(ds)}
'''
    return layout(ds["title"], body)


def svg_map_examples_page() -> str:
    body = r'''
<p><a href="../index.html">← 전체 목록</a></p>
<h1>지도 데이터 유형별 샘플</h1>
<p>자료를 검토한 결과, 모든 지도를 SVG 하나로 처리하기보다 데이터 유형별로 맞는 방식을 나누는 것이 가장 정확합니다. 행정구역 단위 데이터는 경계 지도, 위도·경도 데이터는 점 지도로 시각화합니다.</p>
<div class="card">
  <h2>1) 행정구역 단위 데이터: 색칠 지도</h2>
  <p>
    <label>지도 범위 <select id="boundary-map-kind">
      <option value="seoul-gu">서울 구별</option>
      <option value="seoul-dong">서울 동별</option>
      <option value="korea-sido">전국 광역시도별</option>
    </select></label>
    <label>데이터 선택 <select id="svg-metric-select"></select></label>
    <button id="reload-svg-map" type="button">지도 다시 그리기</button>
  </p>
  <p id="svg-map-summary" class="small-muted">데이터를 불러오는 중입니다…</p>
  <div id="svg-map" class="real-svg-map"></div>
  <div id="boundary-plot" style="height:620px;display:none"></div>
  <div id="svg-legend" class="small-muted"></div>
  <p class="small-muted">경계 출처: Wikimedia Commons 행정구역 SVG 및 southkorea/seoul-maps GeoJSON. 데이터 출처: Wikidata SPARQL(P1082 인구, P2046 면적), GeoJSON 속성값. 출처 상세는 assets/*.SOURCE.txt에 기록했습니다.</p>
</div>
<div class="card">
  <h2>2) 위도·경도 위치 데이터: 점 지도</h2>
  <p>
    <select id="point-dataset-select" aria-label="지도에 표시할 좌표 데이터 선택"></select>
    <button id="reload-point-map" type="button">지도 다시 그리기</button>
  </p>
  <p id="point-map-summary" class="small-muted">데이터를 불러오는 중입니다…</p>
  <div id="point-map" style="height:600px"></div>
  <div id="point-preview"></div>
</div>
<div class="card">
  <h2>3) 데이터 출처와 선택 이유</h2>
  <table>
    <thead><tr><th>유형</th><th>사용 자료</th><th>원본/출처</th><th>수업 포인트</th></tr></thead>
    <tbody>
      <tr><td>전국 광역시도 경계</td><td><code>skorea_provinces_geo_simple.json</code></td><td><a href="https://github.com/southkorea/southkorea-maps">southkorea/southkorea-maps</a> · KOSTAT 센서스 경계 기반</td><td>경계 파일의 지역명과 통계 CSV의 지역명을 매칭</td></tr>
      <tr><td>서울 구 경계</td><td><code>seoul_municipalities_geo_simple.json</code></td><td><a href="https://github.com/southkorea/seoul-maps">southkorea/seoul-maps</a> · KOSTAT 2013</td><td>25개 구가 모두 1:1로 매칭되는지 확인</td></tr>
      <tr><td>서울 동 경계</td><td><code>seoul_neighborhoods_geo_simple.json</code></td><td><a href="https://github.com/southkorea/seoul-maps">southkorea/seoul-maps</a> · JUSO 2015</td><td>동 단위는 명칭·개편 이력이 있어 매칭 전처리가 중요</td></tr>
      <tr><td>인구/면적</td><td><code>seoul_district_wikidata_population.csv</code>, <code>korea_sido_wikidata_population.csv</code></td><td><a href="https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service">Wikidata SPARQL</a> P1082/P2046. 공식 인구 수업 확장은 <a href="https://jumin.mois.go.kr/">행정안전부 주민등록 인구통계</a> 권장</td><td>출처별 최신성·공식성·재현성을 비교</td></tr>
      <tr><td>위치점 데이터</td><td>지진, 병원, 자전거, 생물종 등 위경도 CSV</td><td>각 데이터셋 상세 페이지의 공식 API 링크</td><td>경계 데이터가 아니라 좌표 데이터이므로 점 지도가 적합</td></tr>
    </tbody>
  </table>
  <p class="small-muted">주의: 현재 인구 CSV는 키 없이 재현 가능한 공개 지식그래프 샘플입니다. 공식 행정 수업에서는 행정안전부 주민등록 인구통계 CSV를 내려받아 같은 열 이름으로 바꾸면 동일 코드로 교체할 수 있습니다.</p>
</div>
<div class="card">
  <h2>4) 수업용 샘플 코드</h2>
  <h3>Python/pandas: 행정구역 데이터 매칭 확인</h3>
  <pre><code>import pandas as pd

pop = pd.read_csv("https://thinkervis.github.io/free-api-data-science-edu/data/seoul_district_wikidata_population.csv")
print(pop.head())
print("구 개수:", pop["district"].nunique())

# 수업 질문: 인구밀도가 가장 높은 구와 낮은 구는?
print(pop.sort_values("population_density_per_km2", ascending=False)[["district", "population_density_per_km2"]].head())
print(pop.sort_values("population_density_per_km2")[["district", "population_density_per_km2"]].head())</code></pre>
  <h3>Python/Plotly: 간단한 막대그래프로 먼저 읽기</h3>
  <pre><code>import pandas as pd
import plotly.express as px

url = "https://thinkervis.github.io/free-api-data-science-edu/data/korea_sido_wikidata_population.csv"
df = pd.read_csv(url)
fig = px.bar(df.sort_values("population"), x="population", y="region", orientation="h",
             title="전국 광역시도별 인구")
fig.show()</code></pre>
  <h3>JavaScript: CSV를 읽어 지도 색상에 연결하는 핵심 구조</h3>
  <pre><code>const rows = await fetch("../data/seoul_district_wikidata_population.csv")
  .then(r =&gt; r.text())
  .then(parseCsvRows)
  .then(toObjects);

// 핵심: 경계 파일의 properties.name과 CSV의 district가 같아야 색칠 가능
const rowByDistrict = Object.fromEntries(rows.map(r =&gt; [r.district, r]));
const value = Number(rowByDistrict["강남구"].population_density_per_km2);</code></pre>
</div>
<div class="card">
  <h2>5) 수업 활동 예시</h2>
  <ol>
    <li><b>데이터 유형 분류:</b> 이 데이터는 행정구역 통계인가, 위경도 위치점인가?</li>
    <li><b>매칭 검증:</b> 경계 파일의 지역명과 CSV 지역명이 모두 일치하는지 확인한다.</li>
    <li><b>해석:</b> 인구가 많은 지역과 인구밀도가 높은 지역은 왜 다를까?</li>
    <li><b>출처 토론:</b> Wikidata와 행정안전부 주민등록 인구통계 중 어떤 자료가 더 적합한가?</li>
    <li><b>확장 과제:</b> 행정안전부 CSV를 내려받아 같은 지도에 공식 최신 인구로 교체한다.</li>
  </ol>
</div>
<style>
.real-svg-map{border:1px solid #d0d7de;border-radius:12px;padding:clamp(.25rem,1.5vw,.75rem);overflow:hidden;background:#f6f8fa;max-width:100%}.real-svg-map svg{display:block;width:100%;max-width:100%;height:auto}.boundary-svg{touch-action:manipulation}.boundary-region{cursor:pointer}.boundary-region:hover{stroke:#24292f;stroke-width:2}.small-muted{color:#6e7781;font-size:.95rem}#point-map{border:1px solid #d0d7de;border-radius:12px;overflow:hidden}#point-preview table{margin-top:1rem}.map-hit{stroke:#24292f!important;stroke-width:.6!important;cursor:pointer}.map-muted{fill:#eaeef2!important;stroke:#fff!important;stroke-width:.5!important}
@media(max-width:760px){#point-map,#boundary-plot{height:420px!important}.card{padding:.8rem}button{margin-top:.35rem}#svg-legend div{flex-wrap:wrap}#svg-legend span:nth-child(2){width:120px!important}}
</style>
<script>
const SVG_URL = '../assets/administrative-divisions-south-korea.svg';
const SEOUL_DISTRICT_CSV = '../data/seoul_district_wikidata_population.csv';
const KOREA_SIDO_CSV = '../data/korea_sido_wikidata_population.csv';
const SEOUL_GU_GEOJSON = '../assets/seoul_municipalities_geo_simple.json';
const SEOUL_DONG_GEOJSON = '../assets/seoul_neighborhoods_geo_simple.json';
const KOREA_SIDO_GEOJSON = '../assets/skorea_provinces_geo_simple.json';
if(window.Plotly && Plotly.setPlotConfig){Plotly.setPlotConfig({mapboxAccessToken:null});}
const POINT_DATASETS = [
  {id:'usgs-earthquakes', label:'전세계 규모 6+ 지진 위치', csv:'../data/usgs_major_earthquakes.csv', lat:'latitude', lon:'longitude', text:'place', size:'magnitude', color:'depth_km', colorTitle:'깊이(km)', sizeLabel:'규모', zoom:1, center:{lat:20, lon:0}, note:'USGS 지진 API: 규모와 깊이로 전세계 지진 분포를 확인'},
  {id:'gbif-korea', label:'한국 생물종 관측 위치', csv:'../data/gbif_korea_occurrences_sample.csv', lat:'decimalLatitude', lon:'decimalLongitude', text:'scientificName', subtext:'locality', color:'year', colorTitle:'관측연도', zoom:6, center:{lat:36.4, lon:127.8}, note:'GBIF 관측 좌표: 한국 생물다양성 관측 위치'},
  {id:'osm-seoul-hospitals', label:'서울 병원 위치', csv:'../data/osm_seoul_hospitals.csv', lat:'latitude', lon:'longitude', text:'name', color:'emergency', colorTitle:'응급 태그', zoom:10, center:{lat:37.56, lon:126.98}, note:'OpenStreetMap Overpass: 서울 병원 POI 위치'},
  {id:'nominatim-seoul-landmarks', label:'서울 주요 장소 지오코딩', csv:'../data/nominatim_seoul_landmarks.csv', lat:'latitude', lon:'longitude', text:'query', subtext:'display_name', color:'importance', colorTitle:'중요도', zoom:10, center:{lat:37.56, lon:126.98}, note:'Nominatim: 장소명 → 실제 위경도 변환 결과'},
  {id:'citi-bike-stations', label:'뉴욕 Citi Bike 대여소', csv:'../data/citi_bike_station_snapshot.csv', lat:'latitude', lon:'longitude', text:'name', size:'num_bikes_available', color:'capacity', colorTitle:'거치 용량', sizeLabel:'이용 가능 자전거', zoom:10, center:{lat:40.72, lon:-73.98}, note:'GBFS 스냅샷: 대여소별 자전거 수와 거치 용량'},
  {id:'seoul-bike', label:'서울 따릉이 샘플', csv:'../data/seoul_bike_sample.csv', lat:'stationLatitude', lon:'stationLongitude', text:'stationName', size:'parkingBikeTotCnt', color:'parkingBikeTotCnt', colorTitle:'주차 자전거 수', sizeLabel:'자전거 수', zoom:11, center:{lat:37.56, lon:126.98}, note:'서울 열린데이터광장 샘플키 5건: 따릉이 대여소 위치'},
  {id:'restcountries-world', label:'세계 국가 위치와 인구', csv:'../data/restcountries_world_snapshot.csv', lat:'latitude', lon:'longitude', text:'name', size:'population', color:'population', colorTitle:'인구', sizeLabel:'인구', zoom:1, center:{lat:20, lon:0}, note:'REST Countries: 국가 중심 좌표와 인구 스냅샷'}
];
function parseCsvRows(text){const rows=[];let row=[],cell='',q=false;for(let i=0;i<text.length;i++){const ch=text[i],n=text[i+1];if(ch==='"'){if(q&&n==='"'){cell+='"';i++;}else q=!q;}else if(ch===','&&!q){row.push(cell);cell='';}else if((ch==='\n'||ch==='\r')&&!q){if(ch==='\r'&&n==='\n')i++;row.push(cell);cell='';if(row.some(v=>v!==''))rows.push(row);row=[];}else cell+=ch;}row.push(cell);if(row.some(v=>v!==''))rows.push(row);return rows;}
function toObjects(rows){const h=rows[0]||[];return rows.slice(1).map(r=>Object.fromEntries(h.map((k,i)=>[k,r[i]??''])))}
async function csv(path){return toObjects(parseCsvRows(await fetch(path).then(r=>{if(!r.ok)throw new Error(path+' HTTP '+r.status);return r.text();})))}
function num(v){if(v===null||v===undefined||String(v).trim()==='')return null;const n=Number(v);return Number.isFinite(n)&&n>-900?n:null;}
function escapeHtml(v){return String(v??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));}
function colorScale(v,min,max){if(v===null)return '#eaeef2';const t=max===min?.7:(v-min)/(max-min);const r=Math.round(255-(255-9)*t),g=Math.round(245-(245-105)*t),b=Math.round(235-(235-218)*t);return `rgb(${r},${g},${b})`;}
function geoBounds(geo){
  const pts=[];
  function walk(c){ if(typeof c[0]==='number') pts.push(c); else c.forEach(walk); }
  geo.features.forEach(f=>walk(f.geometry.coordinates));
  return {minLon:Math.min(...pts.map(p=>p[0])), maxLon:Math.max(...pts.map(p=>p[0])), minLat:Math.min(...pts.map(p=>p[1])), maxLat:Math.max(...pts.map(p=>p[1]))};
}
function ringPath(ring,b,w,h){return ring.map((p,i)=>{const x=(p[0]-b.minLon)/(b.maxLon-b.minLon)*w; const y=(b.maxLat-p[1])/(b.maxLat-b.minLat)*h; return (i?'L':'M')+x.toFixed(2)+' '+y.toFixed(2);}).join(' ')+' Z';}
function featurePath(f,b,w,h){const g=f.geometry; if(!g)return ''; if(g.type==='Polygon')return g.coordinates.map(r=>ringPath(r,b,w,h)).join(' '); if(g.type==='MultiPolygon')return g.coordinates.flatMap(poly=>poly.map(r=>ringPath(r,b,w,h))).join(' '); return '';}
async function drawSvgMap(){
  const kind=document.getElementById('boundary-map-kind').value;
  const metricSelect=document.getElementById('svg-metric-select');
  const metricOptions={
    'seoul-gu': [['population','인구(명)'],['area_km2','면적(km²)'],['population_density_per_km2','인구밀도(명/km²)']],
    'korea-sido': [['population','인구(명)'],['area_km2','면적(km²)'],['population_density_per_km2','인구밀도(명/km²)']],
    'seoul-dong': [['shape_area','경계 면적(GeoJSON SHAPE_AREA)'],['shape_len','경계 둘레(GeoJSON SHAPE_LEN)']]
  };
  const current=metricSelect.value;
  metricSelect.innerHTML=metricOptions[kind].map(([v,l])=>`<option value="${v}">${l}</option>`).join('');
  if(metricOptions[kind].some(([v])=>v===current)) metricSelect.value=current;
  const metric=metricSelect.value;
  const metricLabel=Object.fromEntries(metricOptions[kind])[metric]||metric;
  const svgBox=document.getElementById('svg-map');
  const boundaryPlot=document.getElementById('boundary-plot');
  boundaryPlot.style.display='none'; svgBox.style.display='block';
  let geo, rows, title, sourceNote;
  if(kind==='seoul-gu'){
    [geo, rows]=await Promise.all([fetch(SEOUL_GU_GEOJSON).then(r=>r.json()), csv(SEOUL_DISTRICT_CSV)]);
    geo.features.forEach(f=>f.id=f.properties.name);
    rows=rows.map(r=>({id:r.district, name:r.district, value:num(r[metric]), population:r.population, area_km2:r.area_km2, wikidata_id:r.wikidata_id})).filter(r=>r.value!==null);
    title='서울 25개 자치구별 '+metricLabel; sourceNote='경계: southkorea/seoul-maps KOSTAT 2013 · 데이터: Wikidata 인구/면적';
  }else if(kind==='korea-sido'){
    [geo, rows]=await Promise.all([fetch(KOREA_SIDO_GEOJSON).then(r=>r.json()), csv(KOREA_SIDO_CSV)]);
    geo.features.forEach(f=>f.id=f.properties.name);
    rows=rows.map(r=>({id:r.svg_id||r.region, name:r.region, value:num(r[metric]), population:r.population, area_km2:r.area_km2, wikidata_id:r.wikidata_id})).filter(r=>r.value!==null);
    title='전국 17개 광역시도별 '+metricLabel; sourceNote='경계: southkorea/southkorea-maps KOSTAT 2013 · 데이터: Wikidata 인구/면적';
  }else{
    geo=await fetch(SEOUL_DONG_GEOJSON).then(r=>r.json());
    rows=geo.features.map((f,i)=>({id:String(i), name:f.properties.EMD_KOR_NM, value:metric==='shape_len'?Number(f.properties.SHAPE_LEN):Number(f.properties.SHAPE_AREA)}));
    geo.features.forEach((f,i)=>f.id=String(i));
    title='서울 467개 동별 '+metricLabel; sourceNote='경계/속성: southkorea/seoul-maps JUSO 2015. 동별 인구 CSV 확보 시 같은 구조로 교체 가능';
  }
  const rowById=Object.fromEntries(rows.map(r=>[String(r.id),r]));
  const values=rows.map(r=>r.value); const min=Math.min(...values), max=Math.max(...values);
  const b=geoBounds(geo); const w=1000; const h=Math.max(520, Math.round((b.maxLat-b.minLat)/(b.maxLon-b.minLon)*w));
  const paths=geo.features.map(f=>{
    const id=String(f.id); const r=rowById[id]; const fill=r?colorScale(r.value,min,max):'#eaeef2';
    const label=r?`${r.name} · ${metricLabel}: ${r.value.toLocaleString()}`:(f.properties.name||f.properties.EMD_KOR_NM||id);
    return `<path class="boundary-region" d="${featurePath(f,b,w,h)}" fill="${fill}" stroke="#fff" stroke-width="1" data-id="${escapeHtml(id)}"><title>${escapeHtml(label)}</title></path>`;
  }).join('');
  svgBox.innerHTML=`<h3>${escapeHtml(title)}</h3><svg class="boundary-svg" viewBox="0 0 ${w} ${h}" role="img" aria-label="${escapeHtml(title)}">${paths}</svg>`;
  svgBox.querySelectorAll('.boundary-region').forEach(el=>el.addEventListener('click',()=>{const r=rowById[el.dataset.id]; if(!r)return; document.getElementById('svg-map-summary').textContent= kind==='seoul-dong' ? `${r.name} · ${metricLabel}: ${r.value}` : `${r.name} · ${metricLabel}: ${r.value.toLocaleString()} · 인구 ${Number(r.population).toLocaleString()}명 · 면적 ${r.area_km2}km² · Wikidata ${r.wikidata_id}`;}));
  const featureIds=new Set(geo.features.map(f=>String(f.id))); const matched=rows.filter(r=>featureIds.has(String(r.id))).length;
  document.getElementById('svg-map-summary').textContent=`${title} · 데이터 ${rows.length}행 중 경계와 매칭 ${matched}개 · ${sourceNote}`;
  document.getElementById('svg-legend').innerHTML=`<div style="display:flex;align-items:center;gap:.5rem;margin-top:.75rem"><span>낮음 ${min.toLocaleString()}</span><span style="display:inline-block;width:180px;height:12px;border-radius:999px;background:linear-gradient(90deg,#fff5eb,#0969da)"></span><span>높음 ${max.toLocaleString()}</span></div>`;
}
function markerSizes(values){const nums=values.filter(v=>v!==null&&v>0);if(!nums.length)return values.map(()=>9);const min=Math.min(...nums),max=Math.max(...nums);return values.map(v=>{if(v===null||v<=0)return 8;if(max===min)return 14;return 8+Math.sqrt((v-min)/(max-min))*24;});}
function colorValues(rows,cfg){if(!cfg.color)return rows.map(()=>null);const raw=rows.map(r=>r[cfg.color]);const nums=raw.map(num);if(nums.some(v=>v!==null))return nums;const cats=[...new Set(raw.filter(Boolean))];return raw.map(v=>cats.indexOf(v)+1);}
function previewTable(rows,cfg){const cols=[cfg.text,cfg.subtext,cfg.lat,cfg.lon,cfg.size,cfg.color].filter(Boolean);const head=cols.map(c=>`<th>${escapeHtml(c)}</th>`).join('');const body=rows.slice(0,5).map(r=>'<tr>'+cols.map(c=>`<td>${escapeHtml(r[c])}</td>`).join('')+'</tr>').join('');document.getElementById('point-preview').innerHTML=`<h3>지도에 사용한 CSV 미리보기</h3><table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`;}
async function drawPointMap(){
  const cfg=POINT_DATASETS.find(d=>d.id===document.getElementById('point-dataset-select').value)||POINT_DATASETS[0];
  const summary=document.getElementById('point-map-summary'); summary.textContent='CSV를 불러오는 중입니다…';
  try{
    const all=await csv(cfg.csv);
    const rows=all.map(r=>({...r,_lat:num(r[cfg.lat]),_lon:num(r[cfg.lon]),_size:cfg.size?num(r[cfg.size]):null})).filter(r=>r._lat!==null&&r._lon!==null);
    const colors=colorValues(rows,cfg); const sizes=markerSizes(rows.map(r=>r._size));
    const hover=rows.map(r=>{const bits=[`<b>${escapeHtml(r[cfg.text]||cfg.label)}</b>`]; if(cfg.subtext&&r[cfg.subtext])bits.push(escapeHtml(r[cfg.subtext])); if(cfg.size)bits.push(`${escapeHtml(cfg.sizeLabel||cfg.size)}: ${escapeHtml(r[cfg.size])}`); if(cfg.color)bits.push(`${escapeHtml(cfg.colorTitle||cfg.color)}: ${escapeHtml(r[cfg.color])}`); bits.push(`좌표: ${r._lat.toFixed(4)}, ${r._lon.toFixed(4)}`); return bits.join('<br>');});
    const trace={type:'scattermapbox',mode:'markers',lat:rows.map(r=>r._lat),lon:rows.map(r=>r._lon),text:hover,hovertemplate:'%{text}<extra></extra>',marker:{size:sizes,color:colors,colorscale:'Viridis',showscale:!!cfg.color,opacity:.72,colorbar:{title:cfg.colorTitle||cfg.color||''}}};
    const layout={title:cfg.label,mapbox:{style:'open-street-map',center:cfg.center,zoom:cfg.zoom},margin:{t:50,r:10,b:10,l:10},showlegend:false};
    Plotly.newPlot('point-map',[trace],layout,{responsive:true,displaylogo:false,displayModeBar:false});
    summary.textContent=`${cfg.note} · 전체 ${all.length.toLocaleString()}행 중 좌표가 있는 ${rows.length.toLocaleString()}행 표시 · 출처 CSV: ${cfg.csv.replace('../data/','')}`;
    previewTable(rows,cfg);
  }catch(err){summary.textContent='지도 로드 실패: '+err.message;document.getElementById('point-map').innerHTML='';}
}
document.addEventListener('DOMContentLoaded',()=>{const sel=document.getElementById('point-dataset-select');sel.innerHTML=POINT_DATASETS.map(d=>`<option value="${d.id}">${d.label}</option>`).join('');sel.addEventListener('change',drawPointMap);document.getElementById('reload-point-map').addEventListener('click',drawPointMap);document.getElementById('boundary-map-kind').addEventListener('change',drawSvgMap);document.getElementById('svg-metric-select').addEventListener('change',drawSvgMap);document.getElementById('reload-svg-map').addEventListener('click',drawSvgMap);drawSvgMap();drawPointMap();});
</script>
'''
    return layout("지도 데이터 유형별 샘플", body)


def sdg_topics_page() -> str:
    cards = []
    for i, item in enumerate(SDG_TOPICS, start=1):
        cards.append(f'''
<div class="card sdg-card">
  <h2>{i}. {html.escape(item['title'])}</h2>
  <p><span class="badge">{html.escape(item['sdg'])}</span><span class="badge">이용 조건: {html.escape(item['auth'])}</span></p>
  <p><b>데이터:</b> {html.escape(item['data'])}</p>
  <p><b>출처 확인:</b> <a href="{html.escape(item['url'])}">{html.escape(item['data'])} 원본/문서</a></p>
  <p><b>수업 아이디어:</b> {html.escape(item['activity'])}</p>
  <p class="small-muted">그래프는 결측값(빈 값, -999/-1000 계열)을 제외하고 그립니다. 학생에게 “왜 결측값을 0으로 그리면 안 되는가?”를 함께 질문해 보세요.</p>
  <div id="sdg-chart-{i-1}" class="sdg-chart"></div>
</div>''')
    script = r'''
<style>.sdg-chart{height:380px;margin-top:1rem}.sdg-svg-map{height:auto;min-height:480px;border:1px solid #d0d7de;border-radius:14px;background:linear-gradient(180deg,#f8fbff,#eef7ff);padding:.75rem;overflow:hidden}.sdg-svg-map svg{display:block;width:100%;height:auto;max-height:none}.sdg-map-boundary{stroke:#ffffff;stroke-width:1.25;vector-effect:non-scaling-stroke}.sdg-map-boundary:hover{stroke:#0f172a;stroke-width:2}.sdg-map-point{fill:#16a34a;fill-opacity:.68;stroke:#064e3b;stroke-width:.6;vector-effect:non-scaling-stroke}.sdg-map-label{font-size:13px;font-weight:700;fill:#1f2937;paint-order:stroke;stroke:#fff;stroke-width:3;stroke-linejoin:round}.sdg-card{break-inside:avoid}.sdg-card .badge{margin-bottom:.25rem}@media(max-width:760px){.sdg-chart{height:340px}.sdg-svg-map{height:auto!important;min-height:0;padding:.45rem}.sdg-svg-map svg{min-height:420px}.sdg-card h2{font-size:1.18rem;line-height:1.35}.sdg-card .badge{font-size:.78rem;display:inline-block;max-width:100%;overflow-wrap:anywhere;word-break:break-word}.sdg-chart .legend{font-size:10px}}</style>
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
async function json(path) { return fetch(path).then(r => { if (!r.ok) throw new Error(path + ' HTTP ' + r.status); return r.json(); }); }
function escapeHtml(value){return String(value ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));}
function num(v) { if (v === null || v === undefined || String(v).trim() === '') return null; const n = Number(v); return Number.isFinite(n) && n > -900 ? n : null; }
const LABEL_KO = {
  'South Korea':'한국', World:'세계', 'GDP (current US$)':'GDP(현재 US$)', 'Life expectancy at birth, total (years)':'기대수명(년)', 'Population, total':'총인구', 'School enrollment, secondary (% gross)':'중등교육 등록률(%)',
  'Day-ahead demand forecast':'하루 전 수요 예측', Demand:'전력 수요', 'Net generation':'순발전량', 'Total interchange':'총 전력 교환량'
};
function koLabel(value){ return LABEL_KO[value] || value; }
const PLOT_CONFIG = {responsive:true, displaylogo:false, displayModeBar:false};
function mobileLayout(extra={}) { const mobile = window.innerWidth < 760; return Object.assign({legend:{orientation: mobile ? 'h' : 'v', x:0, y: mobile ? -0.25 : 1.05}, font:{size: mobile ? 10 : 12}}, extra); }
function timeAxis(nticks=5){ return {nticks, rangeslider:{visible:true, thickness:0.08}, rangeselector:{buttons:[{count:7,label:'7일',step:'day',stepmode:'backward'},{count:1,label:'1달',step:'month',stepmode:'backward'},{count:1,label:'1년',step:'year',stepmode:'backward'},{step:'all',label:'전체'}]}}; }
function validRows(rows, valueField) { return rows.filter(r => num(r[valueField]) !== null); }
function indexRows(rows, valueField) {
  const clean = validRows(rows, valueField);
  const base = clean.length ? num(clean[0][valueField]) : null;
  if (!base) return [];
  return clean.map(r => ({...r, indexValue: num(r[valueField]) / base * 100}));
}
function latestBy(rows, group, value) { const out = {}; rows.forEach(r => { const k = r[group]; if (!out[k] || String(r.date || r.time || r.Year) > String(out[k].date || out[k].time || out[k].Year)) out[k] = r; }); return Object.values(out).filter(r => num(r[value]) !== null); }
function geoBounds(geo){
  const pts=[];
  function walk(c){ if(!c) return; if(typeof c[0]==='number') pts.push(c); else c.forEach(walk); }
  geo.features.forEach(f=>walk(f.geometry && f.geometry.coordinates));
  return {minLon:Math.min(...pts.map(p=>p[0])), maxLon:Math.max(...pts.map(p=>p[0])), minLat:Math.min(...pts.map(p=>p[1])), maxLat:Math.max(...pts.map(p=>p[1]))};
}
function projectLonLat(lon,lat,b,w,h,pad=18){
  const x=pad+(lon-b.minLon)/(b.maxLon-b.minLon)*(w-pad*2);
  const y=pad+(b.maxLat-lat)/(b.maxLat-b.minLat)*(h-pad*2);
  return [x,y];
}
function ringPath(ring,b,w,h){return ring.map((p,i)=>{const [x,y]=projectLonLat(p[0],p[1],b,w,h);return (i?'L':'M')+x.toFixed(2)+' '+y.toFixed(2);}).join(' ')+' Z';}
function featurePath(f,b,w,h){const g=f.geometry;if(!g)return '';if(g.type==='Polygon')return g.coordinates.map(r=>ringPath(r,b,w,h)).join(' ');if(g.type==='MultiPolygon')return g.coordinates.flatMap(poly=>poly.map(r=>ringPath(r,b,w,h))).join(' ');return '';}
function meanPoint(coords){
  const pts=[]; function walk(c){ if(!c)return; if(typeof c[0]==='number') pts.push(c); else c.forEach(walk); } walk(coords);
  if(!pts.length) return null; return [pts.reduce((a,p)=>a+p[0],0)/pts.length, pts.reduce((a,p)=>a+p[1],0)/pts.length];
}
function shortSidoName(name){return String(name||'').replace('특별자치도','').replace('특별자치시','').replace('광역시','').replace('특별시','').replace('자치도','').replace('도','');}
function labelOffset(name){
  return {'서울특별시':[-54,-16],'인천광역시':[-70,22],'경기도':[44,-10],'세종특별자치시':[-42,14],'대전광역시':[34,18],'충청남도':[-42,-12],'충청북도':[44,-12],'대구광역시':[42,8],'울산광역시':[46,14],'부산광역시':[38,30],'광주광역시':[-44,16]}[name] || [0,0];
}
function blueScale(v,min,max){
  if(v===null) return '#e5e7eb';
  const t=max===min?.65:(v-min)/(max-min);
  const stops=[[240,249,255],[186,230,253],[96,165,250],[37,99,235],[30,64,175]];
  const scaled=t*(stops.length-1); const i=Math.min(stops.length-2, Math.max(0, Math.floor(scaled))); const f=scaled-i;
  const c=stops[i].map((x,j)=>Math.round(x+(stops[i+1][j]-x)*f));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
}
function drawGbifSvgMap(geo, rows, popRows=[]){
  const target=document.getElementById('sdg-chart-3');
  target.classList.add('sdg-svg-map');
  const clean=rows.map(r=>({...r,lat:num(r.decimalLatitude),lon:num(r.decimalLongitude)})).filter(r=>r.lat!==null&&r.lon!==null);
  const popById=Object.fromEntries(popRows.map(r=>[r.svg_id||r.region,r]));
  const densities=geo.features.map(f=>num(popById[f.properties?.name]?.population_density_per_km2)).filter(v=>v!==null);
  const minDensity=Math.min(...densities), maxDensity=Math.max(...densities);
  const b=geoBounds(geo); const w=900; const h=Math.round((b.maxLat-b.minLat)/(b.maxLon-b.minLon)*w)+80;
  const boundaries=geo.features.map(f=>{
    const name=f.properties?.name||''; const pop=popById[name]; const density=num(pop?.population_density_per_km2);
    const fill=blueScale(density,minDensity,maxDensity);
    const title=pop ? `${name} · 인구 ${Number(pop.population).toLocaleString()}명 · 인구밀도 ${Number(pop.population_density_per_km2).toLocaleString()}명/km²` : name;
    return `<path class="sdg-map-boundary" d="${featurePath(f,b,w,h)}" fill="${fill}"><title>${escapeHtml(title)}</title></path>`;
  }).join('');
  const labels=geo.features.map(f=>{
    const p=meanPoint(f.geometry?.coordinates); if(!p) return '';
    const [x,y]=projectLonLat(p[0],p[1],b,w,h);
    const [dx,dy]=labelOffset(f.properties?.name||'');
    return `<text class="sdg-map-label" x="${(x+dx).toFixed(1)}" y="${(y+dy).toFixed(1)}" text-anchor="middle">${escapeHtml(shortSidoName(f.properties?.name))}</text>`;
  }).join('');
  const points=clean.map(r=>{const [x,y]=projectLonLat(r.lon,r.lat,b,w,h);return `<circle class="sdg-map-point" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="3.8"><title>${escapeHtml(r.scientificName || '관측')} · ${escapeHtml(r.locality || '')}</title></circle>`;}).join('');
  target.innerHTML=`<h3>한국 생물종 관측 위치 + 광역시도 인구밀도 SVG</h3><svg viewBox="0 0 ${w} ${h}" role="img" aria-label="광역시도 인구밀도로 색칠한 한국 SVG 지도 위 GBIF 생물종 관측 위치"><rect width="${w}" height="${h}" rx="20" fill="#f8fbff"/><g>${boundaries}</g><g>${points}</g><g>${labels}</g><g transform="translate(34 ${h-48})"><text x="0" y="-10" fill="#475569" font-size="13" font-weight="700">배경색: 인구밀도 낮음 → 높음</text><rect x="0" y="0" width="210" height="12" rx="6" fill="url(#densityGradient)"/><text x="0" y="32" fill="#64748b" font-size="12">${Math.round(minDensity).toLocaleString()}</text><text x="210" y="32" text-anchor="end" fill="#64748b" font-size="12">${Math.round(maxDensity).toLocaleString()}명/km²</text><circle cx="286" cy="6" r="4" class="sdg-map-point"/><text x="300" y="10" fill="#475569" font-size="13">GBIF 관측점</text></g><defs><linearGradient id="densityGradient" x1="0" x2="1" y1="0" y2="0"><stop offset="0%" stop-color="#f0f9ff"/><stop offset="35%" stop-color="#bae6fd"/><stop offset="70%" stop-color="#60a5fa"/><stop offset="100%" stop-color="#1e40af"/></linearGradient></defs></svg><p class="small-muted">GBIF 관측 ${clean.length.toLocaleString()}건을 인구 데이터 예제와 같은 광역시도 경계 위에 표시했습니다. 배경은 <code>korea_sido_wikidata_population.csv</code>의 인구밀도, 점은 GBIF 관측 좌표입니다. <a href="../assets/gbif-korea-pop-density-map.svg">정교한 SVG 이미지 파일 열기</a></p>`;
}

async function drawSdgCharts() {
  try {
    const air = await csv('../data/open_meteo_seoul_air_quality_hourly.csv');
    const airRecent = air.slice(-240);
    Plotly.newPlot('sdg-chart-0', [
      {type:'scatter',mode:'lines',name:'PM10',x:airRecent.map(r=>r.time),y:airRecent.map(r=>num(r.pm10))},
      {type:'scatter',mode:'lines',name:'PM2.5',x:airRecent.map(r=>r.time),y:airRecent.map(r=>num(r.pm2_5))}
    ], mobileLayout({title:'최근 시간대 서울 대기질 변화', margin:{t:50,r:20,b:90,l:50}, yaxis:{title:'㎍/m³'}, xaxis:timeAxis(5)}), PLOT_CONFIG);

    const nasa = await csv('../data/nasa_power_seoul_daily.csv');
    const nasaRecent = nasa.slice(-365);
    Plotly.newPlot('sdg-chart-1', [
      {type:'scatter',mode:'lines',name:'평균기온',x:nasaRecent.map(r=>r.date),y:nasaRecent.map(r=>num(r.temperature_2m_c))},
      {type:'bar',name:'강수량',x:nasaRecent.map(r=>r.date),y:nasaRecent.map(r=>num(r.precipitation_mm_day)),yaxis:'y2',opacity:.35}
    ], mobileLayout({title:'최근 1년 서울 기온·강수', margin:{t:50,r:45,b:95,l:45}, yaxis:{title:'°C'}, yaxis2:{title:'mm/day',overlaying:'y',side:'right'}, xaxis:timeAxis(5)}), PLOT_CONFIG);

    const co2 = await csv('../data/owid_co2_korea_world.csv');
    const co2Groups = [...new Set(co2.map(r=>r.Entity))];
    Plotly.newPlot('sdg-chart-2', co2Groups.map(g => {
      const rows = indexRows(co2.filter(r=>r.Entity===g).sort((a,b)=>Number(a.Year)-Number(b.Year)), 'Annual CO₂ emissions');
      return {type:'scatter',mode:'lines+markers',name:koLabel(g),x:rows.map(r=>r.Year),y:rows.map(r=>r.indexValue),customdata:rows.map(r=>(num(r['Annual CO₂ emissions'])/1e9).toFixed(2)),hovertemplate:'%{fullData.name}<br>연도: %{x}<br>변화: %{y:.1f} (첫해=100)<br>실제 배출량: %{customdata} GtCO₂<extra></extra>'};
    }), mobileLayout({title:'한국과 세계 CO₂ 배출량 변화(첫해=100)', margin:{t:70,r:20,b:90,l:70}, yaxis:{title:'첫해=100 지수'}, xaxis:timeAxis(6)}), PLOT_CONFIG);

    const gbif = await csv('../data/gbif_korea_occurrences_sample.csv');
    const [koreaGeo, sidoPopulation] = await Promise.all([json('../assets/skorea_provinces_geo_simple.json'), csv('../data/korea_sido_wikidata_population.csv')]);
    drawGbifSvgMap(koreaGeo, gbif, sidoPopulation);

    const bike = await csv('../data/seoul_bike_sample.csv');
    Plotly.newPlot('sdg-chart-4', [{type:'bar',x:bike.map(r=>r.stationName),y:bike.map(r=>num(r.parkingBikeTotCnt)),marker:{color:'#0ea5e9'}}], {title:'따릉이 대여소별 현재 자전거 수', margin:{t:50,r:20,b:120,l:55}, yaxis:{title:'대수'}}, PLOT_CONFIG);

    const countries = await csv('../data/restcountries_world_snapshot.csv');
    Plotly.newPlot('sdg-chart-5', [{type:'scatter',mode:'markers',x:countries.map(r=>num(r.area)),y:countries.map(r=>num(r.population)),text:countries.map(r=>r.name),marker:{size:8,opacity:.6,color:'#6366f1'}}], {title:'국가별 면적·인구 비교로 보는 도시·인프라 압력', margin:{t:50,r:20,b:65,l:70}, xaxis:{title:'면적',type:'log'}, yaxis:{title:'인구',type:'log'}}, PLOT_CONFIG);

    const wb = await csv('../data/worldbank_korea_indicators.csv');
    const inds = [...new Set(wb.map(r=>r.indicator))];
    Plotly.newPlot('sdg-chart-6', inds.map(ind => {
      const rows = indexRows(wb.filter(r=>r.indicator===ind).sort((a,b)=>Number(a.date)-Number(b.date)), 'value');
      return {type:'scatter',mode:'lines+markers',name:koLabel(ind),x:rows.map(r=>r.date),y:rows.map(r=>r.indexValue),customdata:rows.map(r=>num(r.value)),hovertemplate:'%{fullData.name}<br>연도: %{x}<br>변화: %{y:.1f} (첫해=100)<br>원값: %{customdata}<extra></extra>'};
    }), mobileLayout({title:'한국 주요 발전 지표 변화(첫해=100)', margin:{t:70,r:20,b:95,l:70}, yaxis:{title:'첫해=100 지수'}, xaxis:timeAxis(6)}), PLOT_CONFIG);

    const fact = await csv('../data/factfulness_global_indicators.csv');
    const life = latestBy(fact.filter(r=>r.indicator_id==='SP.DYN.LE00.IN'), 'countryiso3code', 'value');
    Plotly.newPlot('sdg-chart-7', [{type:'bar',x:life.map(r=>koLabel(r.country)),y:life.map(r=>num(r.value)),text:life.map(r=>r.date),marker:{color:'#f97316'}}], {title:'팩트풀니스: 최신 기대수명 비교', margin:{t:50,r:20,b:110,l:55}, yaxis:{title:'년'}}, PLOT_CONFIG);

    Plotly.newPlot('sdg-chart-8', [{type:'bar',x:nasaRecent.map(r=>r.date),y:nasaRecent.map(r=>num(r.precipitation_mm_day)),marker:{color:'#38bdf8'}}], mobileLayout({title:'물·가뭄 수업용: 서울 일별 강수량', margin:{t:50,r:20,b:90,l:50}, yaxis:{title:'mm/일', rangemode:'tozero'}, xaxis:timeAxis(5)}), PLOT_CONFIG);

    const eia = await csv('../data/eia_california_electricity_daily.csv');
    const recentEia = eia.slice(-600); const types = [...new Set(recentEia.map(r=>r.type_name))].slice(0,5);
    Plotly.newPlot('sdg-chart-9', types.map(t => { const rows = recentEia.filter(r=>r.type_name===t); return {type:'scatter',mode:'lines',name:koLabel(t),x:rows.map(r=>r.date),y:rows.map(r=>num(r.value))}; }), mobileLayout({title:'전력 수요·공급 유형별 변화', margin:{t:50,r:20,b:95,l:70}, yaxis:{title:'MWh'}, xaxis:timeAxis(5)}), PLOT_CONFIG);
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
function mobileLayout(extra={}) { const mobile = window.innerWidth < 760; return Object.assign({legend:{orientation: mobile ? 'h' : 'v', x:0, y: mobile ? -0.25 : 1.05}, font:{size: mobile ? 10 : 12}}, extra); }
function timeAxis(nticks=5){ return {nticks, rangeslider:{visible:true, thickness:0.08}, rangeselector:{buttons:[{count:7,label:'7일',step:'day',stepmode:'backward'},{count:1,label:'1달',step:'month',stepmode:'backward'},{count:1,label:'1년',step:'year',stepmode:'backward'},{step:'all',label:'전체'}]}}; }
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

    for ds in DATASETS:
        page_path = DATASET_PAGES / f"{ds['id']}.html"
        page_path.write_text(dataset_page(ds), encoding="utf-8")

    more_rows = "".join(f"<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td><td>{html.escape(c)}</td><td><a href='{html.escape(d)}'>문서</a></td></tr>" for a, b, c, d in MORE_CANDIDATES)
    by_id = {ds["id"]: ds for ds in DATASETS}
    recommended_items = []
    for rank, rec in enumerate(TOP_RECOMMENDATIONS, start=1):
        ds = by_id[rec["id"]]
        _, _, _, count = read_preview(ds["csv"])
        recommended_items.append(f"""
<li class="recommendation-card">
  <h3>{rank}. <a href="datasets/{ds['id']}.html">{html.escape(ds['title'])}</a> <span class="badge">{count} rows</span></h3>
  <p><b>추천 이유:</b> {html.escape(rec['why'])}</p>
  <ul>
    <li><b>교육적 관점:</b> {html.escape(rec['perspective'])}</li>
    <li><b>시각화 예시:</b> {html.escape(rec['visualization'])}</li>
    <li><b>데이터 사용 방법:</b> {html.escape(rec['use'])}</li>
    <li><b>분석 방법:</b> {html.escape(rec['analysis'])}</li>
  </ul>
</li>""")
    excluded_items = []
    for item in EXCLUDED_FROM_TOP:
        ds = by_id[item["id"]]
        excluded_items.append(f"<li><a href='datasets/{ds['id']}.html'>{html.escape(ds['title'])}</a>: {html.escape(item['reason'])}</li>")
    index = f'''
<h1>초·중·고 정보 교육을 위한 무료 데이터 과학 API & CSV</h1>
<p>교육적 가치가 높은 무료 데이터셋을 골라, 바로 열어 보고 시각화하고 수업 예제로 바꿀 수 있게 정리했습니다. 팩트풀니스 수업용 세계 지표처럼 장기 변화가 중요한 자료는 1960년대부터의 긴 흐름을 우선 보여 주고, 날씨·대기질처럼 최근성이 중요한 자료는 최근 데이터 중심으로 제공합니다.</p>
<p>데이터별 페이지에서 CSV 직접 열기, 원천 API 확인, 브라우저 시각화, Streamlit 기본 코드를 확인할 수 있습니다.</p>
<p><a href="examples/factfulness-literacy.html">팩트풀니스 데이터 리터러시 수업</a> · <a href="examples/sdg-topics.html">지속가능발전 주제 데이터 10가지</a> · <a href="examples/svg-map-visualization.html">SVG 지도 시각화 예제</a> · <a href="https://github.com/thinkervis/free-api-data-science-edu">GitHub 저장소</a> · <a href="https://github.com/thinkervis/free-api-data-science-edu/blob/main/CONTRIBUTING.md">기여 안내</a></p>
<h2>수업 추천 데이터 {len(TOP_RECOMMENDATIONS)}가지</h2>
<p>처음 방문한 선생님과 학생이 바로 써 보기 좋은 데이터만 골라, 데이터별 교육적 관점·시각화 예시·사용 방법·분석 방법을 함께 제안했습니다.</p>
<ol class="recommendation-list">{''.join(recommended_items)}</ol>
<h2>추천 목록에서 잠시 낮춘 데이터</h2>
<p>데이터 자체는 유용하지만, 첫 화면 top 추천에는 분석 질문이 더 강한 자료를 우선했습니다.</p>
<ul>{''.join(excluded_items)}</ul>
<h2>지속가능발전(SDG) 주제 데이터 10가지</h2>
<p>기후·대기질·생물다양성·도시 이동·건강 형평성 등 SDG 수업용 주제는 <a href="examples/sdg-topics.html">별도 페이지</a>로 분리했습니다.</p>
<h2>바로 테스트 가능한 데이터셋</h2>
<p class="small-muted">좋아요는 로그인 없이 누를 수 있습니다. Supabase 설정 전에는 이 브라우저 기준으로 저장되고, 설정 후에는 공용 관심도 순위로 집계됩니다.</p>
<div class="dataset-toolbar">
  <label>정렬 <select id="sort-mode"><option value="default">기본 순서</option><option value="likes">좋아요 많은 순</option></select></label>
  <span id="likes-status" class="small-muted">좋아요 상태 확인 중…</span>
</div>
<div id="dataset-cards"></div>
<h2>추가 API 후보</h2>
<table><thead><tr><th>이름</th><th>분야</th><th>이용 조건</th><th>공식 문서</th></tr></thead><tbody>{more_rows}</tbody></table>
'''
    (DOCS / "index.html").write_text(layout("무료 데이터 과학 교육 API & CSV", index + supabase_config_script() + likes_script()), encoding="utf-8")
    (DOCS / "datasets.json").write_text(json.dumps(DATASETS, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"generated {DOCS}")


if __name__ == "__main__":
    main()
