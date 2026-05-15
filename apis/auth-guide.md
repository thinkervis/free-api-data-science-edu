# Authentication / Signup Guide

API를 수업에 쓰기 전 “가입 필요 여부”와 “API 키 필요 여부”를 먼저 구분합니다.

## 1. 가입도 키도 불필요
바로 테스트 가능합니다. 단, 공개 서버 정책과 호출 빈도를 지켜야 합니다.

- Open-Meteo: 날씨 JSON
- World Bank Indicators: 국가 통계 JSON
- USGS Earthquake: GeoJSON
- REST Countries: 국가 정보 JSON
- OpenStreetMap Nominatim: 지오코딩. User-Agent와 낮은 호출 빈도 권장
- Stooq Quote CSV: 주식 CSV

수업 운영 팁:
- 학생 실습에는 이 그룹을 먼저 사용
- 네트워크 장애 대비로 샘플 JSON/CSV를 `raw/samples/`에 저장 가능
- 반복 호출은 Streamlit `st.cache_data` 사용

## 2. 가입 없이 API 키만 신청하거나 이메일 인증
서비스에 따라 간단한 폼/이메일 인증으로 키를 받습니다.

- OMDb: 무료 키 신청 후 이메일 인증
- Alpha Vantage: 무료 API 키 신청

수업 운영 팁:
- 교사용 키 하나를 서버 환경변수로 넣고 학생에게 노출하지 않는 방식 권장
- 학생별 키 발급을 시킬 경우, 수업 전날 미리 완료

## 3. 계정 가입 + 앱/API 키 발급 필요
개발자 콘솔에서 앱을 만들고 키를 발급합니다.

- TMDB: 계정 생성 → Settings > API → 약관 동의 → 키 발급
- Kakao 지도/Local: 카카오 개발자 가입 → 앱 생성 → 플랫폼/도메인 등록 → REST/JavaScript 키 사용
- FMP: 회원가입 → 대시보드/API 키 발급
- Finnhub: 회원가입 → API token 발급

수업 운영 팁:
- `.env` 파일 사용. Git에 커밋 금지
- Streamlit Cloud 배포 시 Secrets 사용
- Pico W에서는 코드에 키를 직접 박지 말고 별도 `secrets.py` 사용

## 4. 계정 + 키 + 결제/과금 설정 가능성 있음
무료 크레딧이나 데모 키가 있어도 실수 과금 방지를 위해 교육용으로 신중하게 씁니다.

- Google Maps Platform: Cloud 프로젝트/API 키/제한 설정/보통 결제 설정 필요. Demo Key는 프로토타입 전용

수업 운영 팁:
- 초급반에는 OpenStreetMap/Kakao 중심 추천
- Google Maps는 키 제한, 예산 알림, 과금 차단 정책까지 같이 교육할 때만 권장

## 공통 보안 규칙

`.env.example`만 커밋하고 실제 `.env`는 커밋하지 않습니다.

```bash
TMDB_BEARER_TOKEN=
TMDB_API_KEY=
OMDB_API_KEY=
KAKAO_REST_API_KEY=
KAKAO_JAVASCRIPT_KEY=
ALPHA_VANTAGE_API_KEY=
FMP_API_KEY=
FINNHUB_API_KEY=
DATA_GO_KR_SERVICE_KEY=
```

Python에서는 `python-dotenv` 또는 Streamlit secrets를 사용합니다.
