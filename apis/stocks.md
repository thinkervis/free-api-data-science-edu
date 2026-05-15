# Stock / Finance APIs

주식 데이터는 시계열, 이동평균, 수익률, 변동성, 상관관계 분석 수업에 좋습니다. 투자 조언이 아니라 데이터 분석 교육용으로만 사용하세요.

## Stooq Quote CSV
- 주제: 주식/지수 현재가 또는 지연 시세 CSV
- 인증 유형: 가입/키 불필요
- 공식/데이터 페이지: https://stooq.com/db/h/
- 테스트 URL: https://stooq.com/q/l/?s=aapl.us&f=sd2t2ohlcv&h&e=csv
- 교육 포인트:
  - CSV 읽기
  - OHLCV 컬럼
  - 종목 심볼 체계
- Streamlit 적합도: 높음. 키 없이 빠른 차트 가능
- Pico W 적합도: 중간. CSV 파싱은 가능하지만 HTTPS와 네트워크 예외 처리 필요

## Alpha Vantage
- 주제: 미국/글로벌 주식 시계열, 기술지표, 환율, 암호화폐, 뉴스 감성 등
- 인증 유형: API 키 필요. 무료 키 신청 가능
- 공식 문서: https://www.alphavantage.co/documentation/
- 키 발급: https://www.alphavantage.co/support/#api-key
- 문서 확인 내용: 무료 JSON API, intraday/daily/weekly/monthly 주가와 50개 이상 기술지표 제공
- 테스트 URL 예시: `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=YOUR_KEY`
- 교육 포인트:
  - 일/주/월 시계열 비교
  - 이동평균/RSI 등 기술지표
  - API rate limit 체험과 캐싱
- Streamlit 적합도: 높음
- Pico W 적합도: 낮음~중간. 응답이 커서 `GLOBAL_QUOTE` 같은 작은 엔드포인트 권장

### Alpha Vantage 키 발급 방법
1. https://www.alphavantage.co/support/#api-key 접속
2. 무료 API Key 신청 양식 제출
3. 받은 키를 `.env`에 저장
4. 수업에서는 호출 횟수 제한을 피하려고 응답 캐싱 사용

`.env` 예시:
```bash
ALPHA_VANTAGE_API_KEY=your_key_here
```

## Financial Modeling Prep (FMP)
- 주제: 주가, 재무제표, 기업 검색, 히스토리컬 가격
- 인증 유형: 회원가입 + API 키 필요
- 공식 문서: https://site.financialmodelingprep.com/developer/docs
- 문서 확인 내용: 모든 API 요청은 API 키로 인증. 헤더 `apikey: YOUR_API_KEY` 또는 URL 쿼리 `?apikey=YOUR_API_KEY` 사용
- 테스트 URL 예시: `https://financialmodelingprep.com/api/v3/search?query=Apple&apikey=YOUR_KEY`
- 교육 포인트:
  - 기업명 → 티커 검색
  - 재무제표 기반 기초 분석
  - 가격 데이터와 재무 데이터 결합
- Streamlit 적합도: 높음
- Pico W 적합도: 낮음. 재무 데이터 응답이 커서 데스크톱 Python 권장

## Finnhub
- 주제: 실시간 주식/외환/암호화폐, 기업 기본정보, 경제 데이터
- 인증 유형: 회원가입 + API 키 필요
- 공식 문서: https://finnhub.io/docs/api
- 문서 확인 내용: 무료 API로 realtime stock, forex, crypto, company fundamentals, economic data 제공
- 테스트 URL 예시: `https://finnhub.io/api/v1/quote?symbol=AAPL&token=YOUR_KEY`
- 교육 포인트: 현재가 조회, 종목 검색, 경제지표 결합
- Streamlit 적합도: 높음
- Pico W 적합도: 중간. quote 엔드포인트처럼 작은 응답 위주 권장

## 공공데이터포털 - 금융위원회 주식시세정보
- 주제: 한국거래소 상장 주식 시세, 종가/고가/저가/거래량
- 인증 유형: 공공데이터포털 회원가입 + 무료 활용신청 + 서비스키 필요
- 공식 문서: https://www.data.go.kr/data/15094808/openapi.do
- 문서 확인 내용:
  - REST, JSON+XML
  - 비용 무료
  - 개발계정 트래픽 10,000
  - 개발/운영 자동승인
  - 기준일자 영업일 하루 뒤 오후 1시 이후 업데이트 안내
- 교육 포인트:
  - 한국 주식 일별 데이터 분석
  - 등락률/거래량 순위
  - 공공 API 서비스키와 URL 인코딩
- Streamlit 적합도: 높음
- Pico W 적합도: 낮음~중간. 서비스키 보관과 응답 크기 주의
