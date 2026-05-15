# AI 후속 작업 핸드오프

다른 AI 에이전트가 이 레포를 이어서 작업할 때 반드시 읽어야 하는 요약입니다.

## 먼저 읽기

1. `PROJECT_SPEC.md`
2. `README.md`
3. `AI_CONTRIBUTING.md`
4. `hardware/pico2wh-grove-shield.md`
5. `scripts/validate_datasets.py`

## 절대 잊지 말 것

- 대상은 **초·중·고 정보 교육**이다.
- 기본 CSV는 **최근 5년치**다.
- 가능하면 `--scope all`도 지원한다.
- 모든 정식 데이터셋은 GitHub Pages에서 직접 테스트 가능해야 한다.
- 직접 테스트는 **CSV fetch + CSV 직접 로드 + 브라우저 시각화**까지 포함한다.
- Pico는 **Pico 2 WH + Grove Shield** 전제다.
- 검증 없는 완료 보고 금지.

## 정식 데이터셋 추가 체크리스트

- [ ] 공식 문서 URL 확인
- [ ] 원천 API/CSV 테스트 URL 확인
- [ ] 인증 방식 명시
- [ ] `update_datasets.py` updater 추가
- [ ] `generate_pages.py` DATASETS 메타데이터 추가
- [ ] `validate_datasets.py` 최소 행 수 추가
- [ ] `python3 scripts/update_datasets.py --scope recent5` 통과
- [ ] `python3 scripts/generate_pages.py` 통과
- [ ] `python3 scripts/validate_datasets.py` 통과
- [ ] Pages에서 새 데이터셋 페이지 200 확인
- [ ] GitHub Actions 성공 확인

## public-apis 후보 처리

`public-apis/public-apis`에서 가져온 후보는 이미 아래 파일로 정리되어 있다.

- `audits/public_apis_catalog.csv`
- `audits/public_apis_education_candidates.csv`
- `audits/public-apis-review.md`

후보를 하나씩 확인할 때는 no-auth/HTTPS/JSON/CORS/교육 적합성을 우선한다.

## 커밋 메시지 예시

- `Add NASA POWER teaching dataset`
- `Promote verified API candidates to Pages datasets`
- `Document Pico 2 WH Grove Shield examples`
- `Harden dataset validation for browser tests`

## 완료 보고 템플릿

```md
작업 완료했습니다.

추가 데이터셋:
- 파일명 — 행 수 — 인증 방식 — Pages URL

검증:
- py_compile 통과
- update_datasets recent5 통과
- generate_pages 통과
- validate_datasets 통과
- GitHub Actions 성공

주의사항:
- ...
```
