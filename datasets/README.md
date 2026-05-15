# Auto-updated CSV Datasets

이 폴더는 API와 별도로, 규칙적으로 CSV를 내려받거나 생성해 최신 상태를 유지할 수 있는 데이터셋 목록입니다.

목표:
- 학생은 `data/*.csv`만 읽어도 pandas 수업 가능
- 교사는 `scripts/update_datasets.py` 또는 GitHub Actions로 최신 데이터 유지
- API 키가 필요한 데이터는 기본 자동 갱신에서 제외하거나 GitHub Secrets로 관리

## 포함 데이터셋

| 파일 | 원천 | 주제 | 인증 | 갱신 주기 | 상태 |
|---|---|---|---|---|---|
| `data/stooq_aapl_quote.csv` | Stooq Quote CSV | 주식 현재/지연 시세 | 불필요 | 매일/수업 전 | 자동화 가능 |
| `data/worldbank_korea_population.csv` | World Bank API | 한국 인구 장기 시계열 | 불필요 | 월 1회 | 자동화 가능 |
| `data/open_meteo_seoul_current.csv` | Open-Meteo API | 서울 현재 기상 | 불필요 | 시간 단위 | 자동화 가능 |
| `data/mlb_schedule_sample.csv` | MLB Stats API | MLB 경기 일정 샘플 | 불필요 | 매일 시즌 중 | 자동화 가능 |
| `data/seoul_bike_sample.csv` | 서울 열린데이터광장 | 따릉이 샘플 | 샘플키 가능 | 시간 단위 | 자동화 가능 |

## 추가 후보

### 대중교통 CSV
- GTFS 정적 교통 데이터: 정류소/노선/시간표 CSV 묶음. 지역별 제공처 확인 필요
- 서울/공공데이터포털 버스 정류소·노선 파일 데이터: API보다 CSV 수업에 적합

### 인구 CSV
- KOSIS/행안부 인구 파일 데이터: 지역별 인구/연령 구조 분석에 좋음
- World Bank 전체 국가 인구: API에서 CSV로 변환 가능

### 야구 CSV
- Lahman Baseball Database: 선수/팀/시즌 통계 CSV. 역사 데이터 분석에 적합
- Retrosheet: 경기 이벤트 데이터. 고급반용
- MLB Stats API에서 날짜별 경기일정을 CSV로 변환

### 유동인구 CSV
- 서울 생활인구/상권 데이터: 용량이 클 수 있어 원본 다운로드 자동화는 별도 확인 필요
- 수업용으로는 “구/동/시간대별 집계 샘플 CSV”를 만들어 쓰는 방식 추천

### 기상 CSV
- Open-Meteo forecast/archive 응답을 CSV로 저장
- 기상청 단기예보는 서비스키 필요. GitHub Secrets `DATA_GO_KR_SERVICE_KEY`로 자동화 가능

## 운영 방식

로컬 실행:

```bash
python3 scripts/update_datasets.py
```

GitHub Actions:
- `.github/workflows/update-datasets.yml`에서 매일 07:00 KST 근처에 실행
- 변경된 CSV가 있으면 자동 커밋
- 키 필요한 데이터는 GitHub Secrets를 설정한 뒤 스크립트에 추가
