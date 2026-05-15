# Movie APIs

영화 데이터는 추천 시스템, 텍스트 검색, 장르 분석, 흥행/평점 시각화 수업에 좋습니다.

## TMDB (The Movie Database) API
- 주제: 영화/TV/인물/이미지/장르/검색
- 인증 유형: 회원가입 + API 키 필요
- 무료 여부: 무료 플랜으로 교육용 시작 가능. 이용 약관과 rate limit 확인 필요
- 공식 문서: https://developer.themoviedb.org/docs/getting-started
- 키 발급 공식 경로: https://www.themoviedb.org/settings/api
- 문서 확인 내용: 계정 설정의 API 링크에서 API 키 등록, 약관 동의 후 발급. 모바일보다 데스크톱 브라우저 권장.
- 테스트 URL 예시: `https://api.themoviedb.org/3/search/movie?query=parasite&language=ko-KR`
- 요청 방식: `Authorization: Bearer <TMDB_READ_ACCESS_TOKEN>` 또는 v3 `api_key` 방식
- 교육 포인트:
  - 검색어와 결과 랭킹
  - 장르/국가/언어 필터링
  - 포스터 이미지 URL 조합
  - 영화 추천/콘텐츠 기반 필터링
- Streamlit 적합도: 높음. 검색 UI, 포스터 카드, 장르 필터 만들기 좋음
- Pico W 적합도: 낮음~중간. 인증 토큰과 응답 크기 때문에 간단 검색/카운트 정도만 권장

### TMDB 가입/키 발급 방법
1. https://www.themoviedb.org/ 에 가입/로그인
2. 프로필 > Settings > API 이동
3. API 이용 약관 동의
4. Developer 용도로 앱 정보 입력
5. 발급된 API Key 또는 Read Access Token을 `.env`에 저장

`.env` 예시:
```bash
TMDB_BEARER_TOKEN=your_token_here
TMDB_API_KEY=your_v3_key_here
```

## OMDb API
- 주제: 영화 제목, 연도, IMDb ID, 평점, 줄거리
- 인증 유형: API 키 필요. 이메일 기반 무료 키 신청 가능
- 공식 문서/신청: https://www.omdbapi.com/
- 테스트 URL 예시: `https://www.omdbapi.com/?t=parasite&apikey=YOUR_KEY`
- 교육 포인트:
  - 단일 영화 상세 조회
  - IMDb 평점/메타스코어 비교
  - 간단한 REST 쿼리 파라미터
- Streamlit 적합도: 높음. 검색 폼과 결과 카드 만들기 쉬움
- Pico W 적합도: 중간. 응답이 비교적 작지만 키 보관 필요

### OMDb 키 발급 방법
1. https://www.omdbapi.com/ 접속
2. API Key 메뉴에서 무료 키 신청
3. 이메일 인증 후 받은 키를 `.env`에 저장
4. 교육용으로는 `t=제목` 또는 `s=검색어`부터 시작

`.env` 예시:
```bash
OMDB_API_KEY=your_key_here
```
