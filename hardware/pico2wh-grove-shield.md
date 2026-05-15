# Raspberry Pi Pico 2 WH + Grove Shield 기준

이 레포의 Pico 예제는 **Raspberry Pi Pico 2 WH**와 **Grove Shield 사용**을 기본 전제로 합니다.

## 기본 전제

- 보드: Raspberry Pi Pico 2 WH
- 네트워크: 내장 Wi-Fi 사용
- 배선: 납땜/브레드보드 대신 Grove Shield 커넥터 사용
- 기본 출력: USB 시리얼 `print()`
- 선택 출력: Grove I2C OLED/LCD 등 I2C 표시 장치

## 권장 Grove 포트

Grove Shield 제품/리비전에 따라 표기가 다를 수 있으므로 실물 실크 인쇄를 우선합니다.

- I2C Grove: 보통 `SDA=GP4`, `SCL=GP5` 조합을 우선 안내
- 디지털 Grove: 버튼/LED/릴레이 등 단순 입출력
- 아날로그 Grove: 센서값 읽기 수업에 사용 가능

## 수업 운영 팁

1. 처음에는 USB 시리얼 출력으로 API 연결과 CSV/JSON 파싱을 확인합니다.
2. 그 다음 Grove OLED/LCD에 한두 줄만 표시합니다.
3. Pico 메모리를 고려해 큰 CSV는 앞부분 몇 줄만 읽습니다.
4. API 키가 필요한 데이터는 학생 코드에 키를 직접 넣지 않고 교사용 환경에서 별도 관리합니다.

## 예제 구조

각 데이터셋 페이지의 Pico 2 WH 코드는 다음을 포함합니다.

- Wi-Fi 연결
- GitHub Pages CSV 다운로드
- CSV 앞부분 파싱
- USB 시리얼 출력
- Grove I2C OLED가 있을 경우 표시할 수 있는 선택 코드 주석
