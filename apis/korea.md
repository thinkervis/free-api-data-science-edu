# Korea Free APIs

## 서울 열린데이터광장 - 따릉이 실시간 대여정보
- 주제: 서울 공공자전거, 위치, 도시 교통
- 인증: 샘플키 `sample`로 일부 테스트 가능. 정식 사용은 무료 API 키 신청 권장
- 문서/포털: https://data.seoul.go.kr/
- 테스트 URL: http://openapi.seoul.go.kr:8088/sample/json/bikeList/1/5/
- 교육 포인트: 지도 시각화, 좌표, 실시간 도시 데이터, 문자열 숫자 변환
- Streamlit 적합도: 높음

## 공공데이터포털 - 기상청 단기예보 조회서비스
- 주제: 한국 날씨, 초단기실황/예보, 격자 좌표
- 인증: 무료 서비스키 필요
- 문서: https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15084084
- 확인 내용: REST, JSON+XML, 무료, 개발계정 트래픽 10,000, 자동승인
- 교육 포인트: 인증키, 날짜/시간 파라미터, 격자좌표 변환, 카테고리 코드 매핑
- Streamlit 적합도: 높음

## 한국은행 ECOS API
- 주제: 기준금리, 통화량, 환율 등 경제통계
- 인증: 무료 인증키 필요. 일부 sample 호출 가능
- 문서/포털: https://ecos.bok.or.kr/
- 샘플 URL: https://ecos.bok.or.kr/api/StatisticSearch/sample/json/kr/1/5/200Y001/A/2020/2024/10101
- 교육 포인트: 경제 시계열, 코드체계, 연/분기/월 주기 비교
- Streamlit 적합도: 높음

## 후보로 추가 조사할 한국 API
- 한국수출입은행 환율 API: 무료 인증키 필요 여부와 샘플 호출 안정성 확인 필요
- KOSIS 국가통계포털 OpenAPI: 인증/샘플 정책 확인 필요
- 관광공사 TourAPI: 무료 인증키, 위치/관광 데이터 수업에 유용
- 국토교통부/서울시 지하철·버스 API: 교통 데이터 수업 후보
