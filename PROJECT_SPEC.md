# 프로젝트 기준/스펙

이 문서는 후속 작업자(사람/AI)가 프로젝트의 목표와 품질 기준을 같은 방식으로 이해하기 위한 기준 문서입니다.

## 1. 프로젝트 목표

이 레포는 **초·중·고 정보 교육을 위한 무료 데이터 과학 교육 자료**를 만든다.

핵심 목표:

- 학생과 교사가 무료 API와 CSV 데이터를 직접 테스트한다.
- GitHub Pages에서 데이터 확인, CSV 로드, 시각화까지 브라우저에서 실행한다.
- Streamlit으로 대시보드를 빠르게 만든다.
- Raspberry Pi **Pico 2 WH + Grove Shield**로 공공/API 데이터를 받아보는 피지컬 컴퓨팅 활동을 한다.
- API 후보는 공식 문서와 실제 테스트를 거쳐 검증된 것만 데이터셋으로 승격한다.

## 2. 기본 사용자

- 초등/중등/고등 정보 교사
- 데이터 과학 수업을 준비하는 시민/교육 활동가
- 학생 프로젝트 지도자
- 후속 기여자와 AI 에이전트

## 3. 데이터셋 승격 기준

후보 API/데이터를 정식 데이터셋으로 추가하려면 아래를 만족해야 한다.

### 필수

1. 공식 문서 URL이 있다.
2. 원천 API 또는 원천 CSV를 직접 테스트할 수 있다.
3. 인증 방식이 명확하다.
   - 키 불필요
   - 무료 키 필요
   - 가입 필요
   - 결제/쿼터 위험 있음
4. 교육적으로 설명 가능한 주제가 있다.
5. 개인정보/민감정보/저작권 문제가 없어야 한다.
6. `scripts/update_datasets.py --scope recent5` 실행 시 CSV가 생성된다.
7. `scripts/generate_pages.py` 실행 시 GitHub Pages용 페이지가 생성된다.
8. `scripts/validate_datasets.py` 검증을 통과한다.

### 권장

- no-auth, HTTPS, JSON 또는 CSV 응답
- 최근 5년치 시계열 또는 수업용 스냅샷
- 숫자 컬럼이 있어 브라우저 시각화 가능
- Pico 2 WH에서 일부 행만 읽어도 의미가 있음

## 4. 기간 정책

### 기본: 최근 5년치

기본 업로드 CSV는 `recent5` 범위로 생성한다.

```bash
python3 scripts/update_datasets.py --scope recent5
```

### 선택: 가능한 전체 기간

가능한 데이터는 `--scope all`을 지원한다.

```bash
python3 scripts/update_datasets.py --scope all
```

단, API 제한/대용량/과거 데이터 부재가 있으면 보수적으로 제한한다. 제한 사유는 데이터 페이지 `note`에 적는다.

예:

- API가 1984년 이후만 지원
- 무료 API가 20년 이하만 안정적
- DEMO_KEY 쿼터 때문에 일부 기간만 제공
- 스냅샷 데이터라 기간 개념이 없음

## 5. GitHub Pages 필수 구성

각 데이터셋 페이지는 아래를 포함해야 한다.

- 데이터 제목
- 카테고리
- 행 수
- 인증 방식
- 원천/API 이름
- 공식 문서 링크
- 원천 API/CSV 직접 테스트 링크
- GitHub Pages CSV 직접 링크
- CSV 미리보기
- 브라우저 직접 테스트 버튼
  - CSV fetch
  - CSV → CSV 로드
  - CSV 표 미리보기 표시
  - 숫자 컬럼 자동 SVG 시각화
- Streamlit 기본 코드
- Pico 2 WH + Grove Shield 기본 코드
- 주의사항/note

## 6. 직접 테스트 기준

“직접 테스트 가능”은 단순히 HTTP 200만 의미하지 않는다.

필수 확인:

1. 원천 API/CSV가 실제 응답한다.
2. CSV 파일이 생성된다.
3. 헤더가 비어 있지 않다.
4. 최소 행 수 기준을 만족한다.
5. `docs/data/`에 Pages용 복사본이 있다.
6. 데이터셋 개별 HTML 페이지가 있다.
7. 페이지 안에 fetch 코드가 있다.
8. 페이지 안에 CSV 직접 로드 코드가 있다.
9. 페이지 안에 브라우저 시각화 코드가 있다.
10. Streamlit/Pico 2 WH 코드가 있다.

검증은 `scripts/validate_datasets.py`에 명시적으로 추가한다.

## 7. Streamlit 코드 기준

각 데이터 페이지의 Streamlit 코드는 최소한 아래를 해야 한다.

- GitHub Pages CSV URL을 읽는다.
- `pandas.read_csv()`로 DataFrame 생성
- 행/열 수 출력
- 상위 100행 표시
- 숫자 컬럼이 있으면 간단한 차트 표시

## 8. Pico 2 WH + Grove Shield 코드 기준

Pico 예제는 **Raspberry Pi Pico 2 WH + Grove Shield**를 기본 전제로 한다.

필수:

- MicroPython 기준
- 내장 Wi-Fi 연결
- GitHub Pages CSV URL 요청
- 큰 CSV 전체를 처리하지 않고 앞부분만 확인
- 기본 출력은 USB 시리얼 `print()`
- 온보드 LED로 연결 상태 확인
- Grove I2C OLED/LCD 선택 코드 주석 제공

권장 I2C 안내:

- Grove Shield I2C 포트 사용
- 예시 핀: `SDA=GP4`, `SCL=GP5`
- 단, 실물 Grove Shield 표기를 우선한다.

상세 기준: `hardware/pico2wh-grove-shield.md`

## 9. API 후보 처리 절차

후보는 바로 README에만 넣지 말고 아래 흐름으로 처리한다.

1. 후보 출처 기록
   - 예: `public-apis/public-apis`
2. 공식 문서 확인
3. 인증/쿼터/약관 확인
4. 테스트 URL 확인
5. 실제 호출 테스트
6. 교육 적합성 판단
7. 정식 데이터셋 승격 여부 결정

### 승격 가능

- `scripts/update_datasets.py`에 updater 함수 추가
- `scripts/generate_pages.py`의 `DATASETS`에 메타데이터 추가
- `scripts/validate_datasets.py`에 최소 행 수/페이지 검증 추가
- CSV와 Pages 생성
- 검증 통과 후 커밋

### 승격 보류

아래 이유가 있으면 후보 문서에 남긴다.

- 키 필요
- 결제 설정 위험
- 약관 불명확
- CORS/브라우저 테스트 어려움
- 데이터가 너무 큼
- 최근 5년치 기간 개념이 없음
- 교육용으로 설명이 약함

## 10. 필수 실행 명령

작업 후 최소 아래를 실행한다.

```bash
python3 -m py_compile scripts/update_datasets.py scripts/generate_pages.py scripts/validate_datasets.py
python3 scripts/update_datasets.py --scope recent5
python3 scripts/generate_pages.py
python3 scripts/validate_datasets.py
```

API 목록 점검을 바꿨다면:

```bash
python3 scripts/audit_public_apis.py --use-cache
```

GitHub에 푸시한 뒤 가능하면 Actions도 확인한다.

```bash
gh workflow run update-datasets.yml -f scope=recent5
gh run list --limit 5
```

## 11. 완료 보고 형식

후속 작업자는 완료 보고에 아래를 포함한다.

- 추가/변경한 데이터셋 수
- CSV 파일명과 행 수
- 검증 명령 실행 결과
- GitHub Actions 결과
- Pages URL
- 남은 제한/주의사항

예:

```md
완료:
- NASA POWER 서울 일별 기상: 1,826행
- Frankfurter USD/KRW 환율: 1,282행

검증:
- update_datasets recent5 통과
- generate_pages 통과
- validate_datasets 통과
- GitHub Actions 성공

주의:
- EIA는 DEMO_KEY 제한이 있어 무료 키 권장
```

## 12. 금지사항

- API 키/토큰/비밀번호 커밋 금지
- 공식 문서 없는 출처를 정식 데이터셋으로 승격 금지
- 단순 HTTP 200만 보고 완료 처리 금지
- 검증 실패 상태로 푸시 후 성공 보고 금지
- Pico 예제를 일반 Pico W 기준으로 작성 금지
- 개인정보/민감정보 포함 데이터 저장 금지
- 투자 조언처럼 보이는 금융 문구 금지

## 13. 현재 주요 산출물

- `data/`: 기본 recent5 CSV
- `docs/`: GitHub Pages 산출물
- `docs/datasets/`: 데이터셋별 페이지
- `docs/data/`: Pages에서 직접 읽는 CSV
- `scripts/update_datasets.py`: CSV 갱신
- `scripts/generate_pages.py`: Pages 생성
- `scripts/validate_datasets.py`: 검증
- `scripts/audit_public_apis.py`: public-apis 후보 감사
- `audits/public_apis_catalog.csv`: public-apis 전체 파싱 목록
- `audits/public_apis_education_candidates.csv`: 교육 후보 1차 필터
- `hardware/pico2wh-grove-shield.md`: Pico 2 WH + Grove Shield 기준

## 14. 추천/TOP 10 선정 기준

데이터 추천 목록은 작업자가 임의로 확정하지 않는다.

- 교육적 활용도가 높아 보이는 목록은 “추천 후보”로만 표시한다.
- 최종 “TOP 10” 명칭은 운영자 확인 후 사용한다.
- 애매한 데이터는 Slack/Issue에서 논의한 뒤 확정한다.
- 선정 기준은 수업 활용성, 데이터 안정성, 시각화 품질, Pico 2 WH 활용 가능성, 인증 부담을 함께 본다.
