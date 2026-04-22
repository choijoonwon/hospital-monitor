# 병원 부정글 모니터링 시스템

병원명 키워드로 네이버 카페·블로그·플레이스의 부정 게시글을 자동 수집하고 대시보드로 확인하는 도구입니다.

---

## 현장 세팅 순서 (5단계)

### 1단계 — Python 설치 (없는 경우)
https://www.python.org/downloads/ 에서 Python 3.11 이상 다운로드  
⚠️ 설치 시 **"Add Python to PATH"** 반드시 체크

### 2단계 — 파일 다운로드
```
git clone https://github.com/YOUR_GITHUB_ID/hospital-monitor.git
```
또는 GitHub에서 **Code → Download ZIP** 후 압축 해제

### 3단계 — 네이버 API 키 발급 (5분)
1. https://developers.naver.com/apps/#/register 접속 (네이버 로그인)
2. **애플리케이션 이름** 아무거나 입력
3. **사용 API** → **검색** 선택
4. **WEB 설정 → 서비스 URL**: `http://localhost` 입력
5. 등록 후 **Client ID / Client Secret** 복사

### 4단계 — config.json 수정
`config.json` 파일을 메모장으로 열어서 수정:

```json
{
  "naver_client_id": "발급받은_Client_ID",
  "naver_client_secret": "발급받은_Client_Secret",
  "hospitals": [
    {
      "name": "리팅성형외과",
      "keywords": ["리팅성형외과", "ㄹㅌ", "리팅", "김원장"]
    },
    {
      "name": "강남피부과",
      "keywords": ["강남피부과", "ㄱㄴ피부", "강남 피부"]
    }
  ],
  "search_targets": ["cafe", "blog"],
  "max_results_per_keyword": 30,
  "delay_min": 2,
  "delay_max": 5
}
```

- `name`: 병원 표시명 (대시보드에 표시됨)
- `keywords`: 검색할 키워드 목록 (축약어, 원장명 등 모두 추가)
- `max_results_per_keyword`: 키워드당 최대 수집 건수 (30 권장)

### 5단계 — 실행
```
setup.bat  ← 최초 1회만
run.bat    ← 매번 실행
```
브라우저가 자동으로 `http://localhost:5000` 으로 열립니다.

---

## 대시보드 사용법

| 기능 | 설명 |
|------|------|
| **지금 수집하기** | 모든 병원 키워드 검색 실행 |
| **신규만 보기** | 아직 확인하지 않은 NEW 항목만 필터 |
| **보고 복사** | 클릭 시 카카오톡/메신저용 보고 문자 클립보드에 복사 |
| **전체 확인 처리** | NEW 배지 일괄 제거 |

---

## 주의사항

- 네이버 Open API는 하루 **25,000건** 무료 (키워드 × 수집건수로 차감)
- 키워드가 많으면 요청당 자동으로 2~5초 딜레이가 걸림 (계정 보호)
- 플레이스 수집(Selenium)은 Chrome 브라우저가 설치되어 있어야 함

---

## 파일 구조

```
hospital-monitor/
├── setup.bat           # 초기 설치 (1회)
├── run.bat             # 실행
├── config.json         # 병원 목록 및 API 키 설정
├── requirements.txt    # Python 패키지 목록
├── app/
│   ├── main.py         # Flask 서버 + 수집 실행
│   ├── db.py           # SQLite 데이터 저장
│   ├── collector/
│   │   ├── naver_api.py      # 네이버 Open API 수집
│   │   └── naver_selenium.py # 플레이스 Selenium 수집
│   └── templates/
│       └── index.html  # 대시보드 UI
└── data/
    └── monitor.db      # 수집 데이터 (자동 생성)
```
