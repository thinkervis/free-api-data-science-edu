# Free API Data Science Education Catalog

무료 API로 데이터 과학 수업, Streamlit 대시보드, Raspberry Pi Pico W 프로젝트를 만들기 위한 API 기록 레포입니다.

기준:
- 무료로 시작 가능
- 직접 테스트 가능한 엔드포인트 또는 공식 문서 확인 가능
- JSON/CSV 등 교육용으로 다루기 쉬운 형식 우선
- Pico W에서는 HTTPS, 응답 크기, 인증키 저장 난이도를 별도 표시

## 빠른 시작

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/check_apis.py
streamlit run examples/streamlit_app/app.py
```

## API 목록

| 구분 | API | 주제 | 인증 | 검증 |
|---|---|---|---|---|
| 글로벌 | Open-Meteo Forecast | 날씨/시계열 | 불필요 | 직접 테스트 가능 |
| 글로벌 | World Bank Indicators | 인구/경제/국가통계 | 불필요 | 직접 테스트 가능 |
| 글로벌 | USGS Earthquake API | 지진/지도/실시간 | 불필요 | 직접 테스트 가능 |
| 글로벌 | REST Countries | 국가/인구/언어/통화 | 불필요 | 직접 테스트 가능 |
| 한국 | 서울 열린데이터광장 따릉이 | 도시/교통/위치 | 샘플키 가능, 정식키 무료 신청 | 직접 테스트 가능 |
| 한국 | 공공데이터포털 기상청 단기예보 | 한국 날씨 | 무료 인증키 필요 | 공식 문서 확인 |
| 한국 | 한국은행 ECOS | 거시경제/금리/환율 | 무료 인증키, sample 호출 가능 | 문서/샘플 확인 |

## 수업 아이디어

- JSON → pandas DataFrame 변환
- 시간별 날씨 시계열 시각화
- 국가별 인구 변화 비교
- 지진 발생 위치 지도 시각화
- 서울 따릉이 대여소별 잔여 자전거 지도
- Pico W로 현재 날씨/공공 데이터 받아 OLED 또는 시리얼 출력

## 레포 상태

초안입니다. GitHub 공개 레포 생성/푸시는 별도 확인 후 진행하세요.
