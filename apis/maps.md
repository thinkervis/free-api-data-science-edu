# Map / Geocoding APIs

지도 API는 좌표, 거리, 경로, 공간 데이터 시각화 수업에 좋습니다.

## OpenStreetMap Nominatim
- 주제: 지오코딩(주소/장소 → 좌표), 역지오코딩(좌표 → 주소)
- 인증 유형: 가입/키 불필요
- 공식 문서: https://nominatim.org/release-docs/latest/api/Overview/
- 테스트 URL: https://nominatim.openstreetmap.org/search?q=Seoul%20City%20Hall&format=json&limit=1
- 중요 정책: 공개 서버는 대량 호출 금지. 수업에서는 캐싱, 낮은 빈도, 명확한 User-Agent 사용 권장
- 교육 포인트:
  - 주소 검색 결과의 모호성
  - 위도/경도와 지도 시각화
  - API 사용 정책과 공공 자원 예절
- Streamlit 적합도: 높음. `st.map`, pydeck, folium과 연결 가능

## Kakao 지도 / Local API
- 주제: 한국 주소 검색, 좌표 변환, 지도 표시, 키워드 검색
- 인증 유형: 카카오 계정 가입 + 앱 생성 + API 키 필요
- 지도 Web API 문서: https://apis.map.kakao.com/web/guide/
- Local REST API 문서: https://developers.kakao.com/docs/latest/ko/local/dev-guide
- 문서 확인 내용:
  - Kakao 지도 JavaScript API는 키 발급과 카카오 계정 필요
  - 개발자 등록 및 앱 생성 후 플랫폼 키에서 JavaScript Key 사용
  - JavaScript SDK 도메인 등록 필요
  - Local API는 `Authorization: KakaoAK ${REST_API_KEY}` 헤더 사용
- 교육 포인트:
  - 한국 주소 → 좌표 변환
  - 장소 검색 결과 페이지네이션
  - 지도 마커/클러스터링
- Streamlit 적합도: 중간~높음. REST Local API는 Python에서 좋고, 지도 렌더링은 folium/HTML 컴포넌트 활용

### Kakao 키 발급 방법
1. https://developers.kakao.com/ 로그인
2. 내 애플리케이션 > 애플리케이션 추가하기
3. 앱 설정 > 플랫폼에서 Web 플랫폼과 도메인 등록 (`http://localhost:8501` 등)
4. 앱 키에서 JavaScript 키 또는 REST API 키 복사
5. `.env`에 저장

`.env` 예시:
```bash
KAKAO_REST_API_KEY=your_rest_key_here
KAKAO_JAVASCRIPT_KEY=your_js_key_here
```

## Google Maps Platform
- 주제: 지도, 지오코딩, 경로, 장소 검색
- 인증 유형: Google 계정 + Cloud 프로젝트 + API 키 + 보통 결제 설정 필요. 일부 데모 키로 프로토타입 가능
- 공식 문서: https://developers.google.com/maps/documentation/javascript/get-api-key
- 문서 확인 내용:
  - API 키는 인증과 과금 연결에 필요
  - Cloud Console 또는 Cloud SDK에서 생성/관리
  - 보안을 위해 앱/웹사이트 제한 권장
  - Maps Demo Key는 결제 정보 없이 일부 기능 프로토타입 가능하나 production 용도 아님
- 교육 포인트: 글로벌 지도, 장소 검색, 경로 최적화
- Streamlit 적합도: 중간. 비용/키 제한 때문에 고급반 또는 데모 중심 권장
