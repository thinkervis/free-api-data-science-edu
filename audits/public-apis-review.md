# public-apis 검토 기록

원본: https://raw.githubusercontent.com/public-apis/public-apis/master/README.md
전체 항목: 1529개
카테고리: 51개
교육 후보 1차 필터: 514개

## 산출물

- `audits/public_apis_catalog.csv`: public-apis 전체 항목을 한 줄씩 파싱한 목록
- `audits/public_apis_education_candidates.csv`: 초·중·고 정보/데이터 과학 수업 후보 1차 필터

## 1차 필터 기준

- 과학/환경/보건/우주/지리/교통/경제/통계/공공데이터 키워드
- 인증 불필요 또는 낮은 인증 부담
- HTTPS 지원

## 다음 단계

1. 후보를 공식 문서/테스트 URL 기준으로 하나씩 확인
2. no-auth + JSON/CORS 가능 + 교육 적합 후보 우선 반영
3. 최근 5년치 CSV 자동화가 가능한 후보는 `scripts/update_datasets.py`에 추가
4. GitHub Pages에 JSON 변환 + 시각화 + Streamlit/Pico 2 WH + Grove Shield 예제 제공

## 상위 후보 예시

- FreeForexAPI (Currency Exchange, score=8, auth=No) — https://freeforexapi.com/Home/Api
- National Grid ESO (Environment, score=8, auth=No) — https://data.nationalgrideso.com/
- ADS-B Exchange (Transportation, score=8, auth=No) — https://www.adsbexchange.com/data/
- CoinCap (Cryptocurrency, score=6, auth=No) — https://docs.coincap.io/
- Solana JSON RPC (Cryptocurrency, score=6, auth=No) — https://docs.solana.com/developing/clients/jsonrpc-api
- ZMOK (Cryptocurrency, score=6, auth=No) — https://zmok.io
- Frankfurter (Currency Exchange, score=6, auth=No) — https://www.frankfurter.app/docs
- National Bank of Poland (Currency Exchange, score=6, auth=No) — http://api.nbp.pl/en.html
- Cloudflare Trace (Development, score=6, auth=No) — https://github.com/fawazahmed0/cloudflare-trace-api
- PM2.5 Open Data Portal (Environment, score=6, auth=No) — https://pm25.lass-net.org/#apis
- Bank Negara Malaysia Open Data (Government, score=6, auth=No) — https://apikijangportal.bnm.gov.my/
- Brazil (Government, score=6, auth=No) — https://brasilapi.com.br/
- Brazil Central Bank Open Data (Government, score=6, auth=No) — https://dadosabertos.bcb.gov.br/
- Brazilian Chamber of Deputies Open Data (Government, score=6, auth=No) — https://dadosabertos.camara.leg.br/swagger/api.html
- City, Berlin (Government, score=6, auth=No) — https://daten.berlin.de/
- City, Gdańsk (Government, score=6, auth=No) — https://ckan.multimediagdansk.pl/en
- City, Helsinki (Government, score=6, auth=No) — https://hri.fi/en_gb/
- City, Lviv (Government, score=6, auth=No) — https://opendata.city-adm.lviv.ua/
- City, New York Open Data (Government, score=6, auth=No) — https://opendata.cityofnewyork.us/
- City, Toronto Open Data (Government, score=6, auth=No) — https://open.toronto.ca/
- Colorado Information Marketplace (Government, score=6, auth=No) — https://data.colorado.gov/
- Data USA (Government, score=6, auth=No) — https://datausa.io/about/api/
- District of Columbia Open Data (Government, score=6, auth=No) — http://opendata.dc.gov/pages/using-apis
- EPA (Government, score=6, auth=No) — https://www.epa.gov/developers/data-data-products#apis
- Istanbul (İBB) Open Data (Government, score=6, auth=No) — https://data.ibb.gov.tr
- Open Government, ACT (Government, score=6, auth=No) — https://www.data.act.gov.au/
- Open Government, Argentina (Government, score=6, auth=No) — https://datos.gob.ar/
- Open Government, Australia (Government, score=6, auth=No) — https://www.data.gov.au/
- Open Government, Austria (Government, score=6, auth=No) — https://www.data.gv.at/
- Open Government, Belgium (Government, score=6, auth=No) — https://data.gov.be/
