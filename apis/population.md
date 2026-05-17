# Population APIs

## World Bank Indicators API
- 주제: 국가별 인구, GDP, 교육, 보건, 개발 지표
- 인증 유형: 가입/키 불필요
- 문서: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation
- 테스트 URL: https://api.worldbank.org/v2/country/KOR/indicator/SP.POP.TOTL?format=json&per_page=5
- 교육 포인트: 장기 시계열, 국가 비교, 결측치, 지표 코드
- Streamlit 적합도: 높음

## KOSIS 공유서비스
- 주제: 한국 국가통계, 인구/가구/고용/지역 통계
- 인증 유형: KOSIS OpenAPI 이용 절차 및 키 확인 필요
- 공식 포털: https://kosis.kr/openapi/index/index.jsp
- 교육 포인트: 한국 지역 통계, 표/분류 코드, 행정구역 비교
- Streamlit 적합도: 높음

## 행정안전부 주민등록 인구통계 후보
- 주제: 시도/시군구/읍면동별 주민등록 인구
- 인증 유형: 공공데이터포털 또는 통계 파일 제공 형태 확인 필요
- 교육 포인트: 지역별 인구 지도, 고령화 비율, 인구 피라미드
- 비고: 실제 수업 전 공식 API/파일 링크를 추가 검증해야 함
