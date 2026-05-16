# Free API Data Science Education Catalog

**초·중·고 정보 교육을 위한 무료 데이터 과학 교육 자료**입니다.

무료 API와 자동 갱신 CSV 데이터로 데이터 과학 수업, Streamlit 대시보드, Raspberry Pi Pico 2 WH + Grove Shield 프로젝트를 만들기 위한 레포입니다.

기준:
- 무료로 시작 가능
- 직접 테스트 가능한 엔드포인트 또는 공식 문서 확인 가능
- JSON/CSV 등 교육용으로 다루기 쉬운 형식 우선
- 가입 필요 / API 키 필요 / 결제 가능성 여부를 구분
- Pico 2 WH + Grove Shield에서는 HTTPS, 응답 크기, 인증키 저장 난이도를 별도 표시

## GitHub Pages에서 바로 테스트

- Pages: https://thinkervis.github.io/free-api-data-science-edu/
- 각 데이터 페이지에서 CSV 직접 열기, 원천 API 테스트, 브라우저 fetch 테스트, Streamlit/Pico 2 WH + Grove Shield 기본 코드를 확인할 수 있습니다.

## 빠른 시작

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 scripts/check_apis.py
streamlit run examples/streamlit_app/app.py
```


## 추천 데이터 10가지

처음 방문한 선생님과 학생이 바로 써 보기 좋은 데이터부터 골랐습니다.

1. 서울 5년 일별 기상 — 날씨 시계열/그래프 수업 입문
2. 서울 5년 시간별 대기질 — 미세먼지/환경 탐구
3. NASA POWER 서울 일별 기상/에너지 — NASA 공식 과학 데이터
4. 전세계 규모 6+ 지진 — 지도/지구과학 융합
5. USD/KRW 환율 일별 — 경제 시계열 분석
6. 한국 World Bank 지표 — 인구/경제/교육/보건 지표
7. 세계 국가 기본 정보 — 국가별 인구/면적/위치 비교
8. 한국 공휴일 — 날짜/달력/문화 데이터 초급 활동
9. SpaceX 발사 기록 — 우주/과학 흥미 기반 분석
10. 한국 생물종 관측 샘플 — 생태/위치 데이터 탐구

## API 목록

| 구분 | API | 주제 | 인증 | 검증 |
|---|---|---|---|---|
| 글로벌 | Open-Meteo Forecast | 날씨/시계열 | 불필요 | 직접 테스트 가능 |
| 글로벌 | World Bank Indicators | 인구/경제/국가통계 | 불필요 | 직접 테스트 가능 |
| 글로벌 | USGS Earthquake API | 지진/지도/실시간 | 불필요 | 직접 테스트 가능 |
| 글로벌 | REST Countries | 국가/인구/언어/통화 | 불필요 | 직접 테스트 가능 |
| 영화 | TMDB | 영화/TV/인물/이미지 | 회원가입 + API 키 | 공식 문서 확인 |
| 영화 | OMDb | 영화 상세/평점 | API 키 | 공식 문서 확인 |
| 지도 | OpenStreetMap Nominatim | 지오코딩/역지오코딩 | 불필요 | 직접 테스트 가능 |
| 지도 | Kakao 지도/Local | 한국 지도/주소/장소 | 회원가입 + 앱 키 | 공식 문서 확인 |
| 지도 | Google Maps Platform | 지도/장소/경로 | 계정 + 키 + 결제 가능성 | 공식 문서 확인 |
| 주식 | Stooq CSV | 주식/지수 CSV | 불필요 | 직접 테스트 가능 |
| 주식 | Alpha Vantage | 주식/기술지표/환율 | API 키 | 공식 문서 확인 |
| 주식 | FMP/Finnhub | 주식/재무/현재가 | 회원가입 + API 키 | 공식 문서 확인 |
| 한국 | 서울 열린데이터광장 따릉이 | 도시/교통/위치 | 샘플키 가능, 정식키 무료 신청 | 직접 테스트 가능 |
| 한국 | 공공데이터포털 기상청 단기예보 | 한국 날씨 | 무료 인증키 필요 | 공식 문서 확인 |
| 한국 | 한국은행 ECOS | 거시경제/금리/환율 | 무료 인증키, sample 호출 가능 | 문서/샘플 확인 |
| 한국 | 공공데이터포털 금융위원회 주식시세 | 한국 주식 | 무료 활용신청 + 서비스키 | 공식 문서 확인 |
| 대중교통 | 서울 버스도착정보 | 버스 도착/혼잡도 | 무료 활용신청 + 서비스키 | 공식 문서 확인 |
| 인구 | KOSIS/행안부 후보 | 한국 인구/지역통계 | 확인 필요 | 공식 포털 확인 |
| 야구 | MLB Stats API | 경기 일정/결과 | 불필요 | 직접 테스트 가능 |
| 유동인구 | 서울 생활인구/상권 후보 | 시간대별 유동인구 | 확인 필요 | 공식 포털 확인 |

## CSV 데이터 범위

날씨·대기질처럼 최근성이 중요한 데이터는 최근 5년을 기본으로 제공합니다. 팩트풀니스처럼 장기 변화가 핵심인 데이터는 가능한 한 1960년대부터 현재까지의 흐름을 제공합니다. 개발자는 `--scope all` 옵션으로 더 넓은 기간을 다시 생성할 수 있습니다.

```bash
python3 scripts/update_datasets.py --scope recent5
python3 scripts/update_datasets.py --scope all
python3 scripts/generate_pages.py
python3 scripts/validate_datasets.py
```

## 세부 문서

- `apis/auth-guide.md` — 가입/키 발급 유형별 정리
- `apis/global.md` — 글로벌 무료 API
- `apis/korea.md` — 한국 공공/민간 API
- `apis/movies.md` — 영화 API
- `apis/maps.md` — 지도/지오코딩 API
- `apis/stocks.md` — 주식/금융 API
- `apis/use-cases.md` — Streamlit/Pico 2 WH + Grove Shield 프로젝트 아이디어
- `apis/brainstorm.md` — 수업 주제 브레인스토밍
- `apis/transit.md` — 대중교통 API
- `apis/population.md` — 인구 API
- `apis/baseball.md` — 야구 API
- `apis/foot-traffic.md` — 유동인구 API
- `CONTRIBUTING.md` — 기여하고 싶은 선생님/시민을 위한 안내
- `CONTRIBUTORS.md` — 기여자 표기
- `hardware/pico2wh-grove-shield.md` — Pico 2 WH + Grove Shield 기준

## 수업 아이디어

- JSON → pandas DataFrame 변환
- 시간별 날씨 시계열 시각화
- 국가별 인구 변화 비교
- 지진 발생 위치 지도 시각화
- 서울 따릉이 대여소별 잔여 자전거 지도
- 영화 검색/추천 미니앱
- 주식 이동평균/수익률 대시보드
- 주소 검색 후 지도 표시/거리 계산
- 버스 도착/야구 스코어보드/유동인구 히트맵
- Pico 2 WH + Grove Shield로 현재 날씨/공공 데이터 받아 Grove OLED/LCD 또는 USB 시리얼 출력



## 기여 안내

선생님, 학생, 개발자, 시민 누구나 기여할 수 있습니다.

- 사람용 안내: `CONTRIBUTING.md`
- 기여자 표기: `CONTRIBUTORS.md`

기여는 데이터 추천, 공식 문서 확인, CSV 자동화, Streamlit/Pico 2 WH + Grove Shield 예제, 수업 활동지, 현장 적용 후기까지 모두 환영합니다.

## 레포 상태

GitHub Pages, CSV 데이터, 수업 예제, Streamlit/Pico 2 WH + Grove Shield 시작 코드를 포함합니다. 공식 문서와 직접 테스트 가능한 데이터 출처를 기준으로 계속 확장합니다.
