# AI 기여 안내 (AI/에이전트 버전)

이 문서는 AI 에이전트가 이 레포에 안전하고 검증 가능한 방식으로 기여하기 위한 규칙입니다.

## 목표

**초·중·고 정보 교육을 위한 무료 데이터 과학 교육 자료**를 만든다. 모든 산출물은 교사와 학생이 GitHub Pages에서 직접 테스트하고, Streamlit/Pico 2 WH + Grove Shield 기본 코드를 바로 복사해 쓸 수 있어야 한다.

## 작업 원칙

1. 추측하지 말고 공식 문서 또는 직접 호출 결과로 확인한다.
2. 데이터/API 추가 시 인증 방식, 공식 문서, 직접 테스트 URL을 반드시 남긴다.
3. 기본 CSV는 최근 5년치로 생성한다.
4. `--scope all`로 가능한 전체 기간을 받을 수 있게 자동화한다.
5. GitHub Pages에 데이터별 페이지를 생성한다.
6. 각 데이터 페이지에는 다음이 있어야 한다.
   - CSV 직접 링크
   - 원천 API/CSV 직접 테스트 링크
   - 공식 문서 링크
   - 브라우저 fetch 테스트 버튼
   - CSV 미리보기
   - Streamlit 기본 코드
   - Pico 2 WH + Grove Shield 기본 코드
   - 인증/라이선스/주의사항
7. 테스트 없이 완료 보고하지 않는다.

## 필수 검증 명령

변경 후 아래를 모두 실행한다.

```bash
python3 scripts/update_datasets.py --scope recent5
python3 scripts/generate_pages.py
python3 scripts/validate_datasets.py
python3 scripts/check_apis.py
```

가능하면 GitHub Actions도 확인한다.

```bash
gh workflow run update-datasets.yml -f scope=recent5
gh run list --limit 5
```

## 데이터 추가 절차

1. 공식 문서 확인
2. 테스트 URL 확인
3. `scripts/update_datasets.py`에 함수 추가
4. `scripts/generate_pages.py`의 `DATASETS`에 페이지 메타데이터 추가
5. `scripts/validate_datasets.py`에 최소 행 수/스키마 검증 추가
6. README/API 문서 업데이트
7. 로컬 검증
8. 커밋/푸시
9. Actions/Pages 확인

## 금지/주의

- 개인 API 키, 토큰, 비밀번호를 커밋하지 않는다.
- 비공식 크롤링을 기본 데이터로 넣지 않는다. 약관 확인 전에는 “후보”로만 기록한다.
- 교육용이므로 주식 데이터에는 투자 조언처럼 보이는 문구를 넣지 않는다.
- 개인정보 또는 재식별 위험이 있는 원자료를 저장하지 않는다.
- 대용량 전체 데이터는 Git LFS 또는 외부 저장소 필요성을 먼저 검토한다.

## 완료 보고 형식

- 변경한 데이터/API 수
- 생성된 CSV 파일과 행 수
- Pages URL
- 실행한 검증 명령과 결과
- 남은 한계/주의사항
