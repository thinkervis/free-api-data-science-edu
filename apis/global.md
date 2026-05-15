# Global Free APIs

## Open-Meteo Forecast API
- 주제: 날씨, 기온, 습도, 풍속, 강수, 일사량 등 시계열
- 인증: 불필요
- 문서: https://open-meteo.com/en/docs
- 테스트 URL: https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current=temperature_2m,relative_humidity_2m,wind_speed_10m&timezone=Asia%2FSeoul
- 교육 포인트: 시계열, 단위, 좌표, 결측/예보 데이터
- Streamlit 적합도: 높음
- Pico W 적합도: 높음. 인증키 없이 HTTPS JSON 호출 가능

## World Bank Indicators API
- 주제: 인구, GDP, 교육, 보건, 개발 지표
- 인증: 불필요
- 문서: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation
- 테스트 URL: https://api.worldbank.org/v2/country/KOR/indicator/SP.POP.TOTL?format=json&per_page=5
- 교육 포인트: 국가코드, 장기 시계열, 지표 선택, 결측치 처리
- Streamlit 적합도: 높음
- Pico W 적합도: 중간. 응답 구조가 배열 중첩이라 파싱 예제를 단순화하는 편이 좋음

## USGS Earthquake API
- 주제: 지진, 지리 좌표, GeoJSON, 실시간 이벤트
- 인증: 불필요
- 문서: https://earthquake.usgs.gov/fdsnws/event/1/
- 테스트 URL: https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&limit=1&orderby=time
- 교육 포인트: GeoJSON, 지도 시각화, 필터링, 실시간 데이터
- Streamlit 적합도: 높음
- Pico W 적합도: 중간. GeoJSON 응답이 클 수 있어 limit/필드 최소화 권장

## REST Countries
- 주제: 국가, 수도, 인구, 통화, 언어
- 인증: 불필요
- 문서: https://restcountries.com/
- 테스트 URL: https://restcountries.com/v3.1/name/korea?fields=name,capital,population,region,currencies,languages
- 교육 포인트: 리스트/딕셔너리 JSON 구조, 카테고리형 데이터
- Streamlit 적합도: 높음
- Pico W 적합도: 높음. fields 파라미터로 응답 축소 가능
