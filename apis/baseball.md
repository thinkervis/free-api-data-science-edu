# Baseball APIs

## MLB Stats API
- 주제: MLB 경기 일정, 결과, 팀, 선수, 박스스코어
- 인증 유형: 가입/키 불필요
- 테스트 URL: https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2024-03-28
- 참고 문서/라이브러리: https://github.com/toddrob99/MLB-StatsAPI/wiki
- 직접 확인 내용: schedule 엔드포인트가 JSON으로 경기 수, gamePk, 경기일, 팀 정보 등을 반환
- 교육 포인트:
  - 경기 일정/결과 데이터
  - 팀별 승패/득점 분포
  - 날짜 필터링과 JSON 중첩 구조
- Streamlit 적합도: 높음. 날짜 선택 → 경기 목록/스코어보드
- Pico W 적합도: 중간. 하루 일정 정도는 가능하지만 응답 크기 제한 필요

## pybaseball / Lahman / Retrosheet 후보
- 주제: 선수 기록, 세이버메트릭스, 장기 역사 데이터
- 인증 유형: 대체로 키 없이 Python 패키지/CSV 기반 사용 가능하나 출처별 라이선스 확인 필요
- 교육 포인트: 선수별 누적 기록, 회귀분석, 순위 예측, 시각화
- 비고: API라기보다 데이터셋/패키지 형태가 많아 별도 `datasets/` 문서로 분리 가능

## KBO 데이터 후보
- 주제: 한국 프로야구 일정/기록
- 인증 유형: 공식 개방 API 존재 여부 추가 확인 필요
- 교육 포인트: 한국 학생 친화적 스포츠 데이터
- 비고: 비공식 크롤링은 약관/robots/저작권 이슈가 있어 기본 카탈로그에는 “후보”로만 둠
