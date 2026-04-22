@echo off
chcp 65001 > nul
echo ================================================
echo  병원 모니터링 시스템 - 초기 설치
echo ================================================
echo.

:: Python 확인
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python이 설치되어 있지 않습니다.
    echo     아래 링크에서 Python 3.11 이상을 설치해주세요:
    echo     https://www.python.org/downloads/
    echo.
    echo     설치 시 "Add Python to PATH" 체크박스를 반드시 선택하세요!
    pause
    exit /b 1
)

echo [1/3] Python 확인 완료
python --version
echo.

:: pip 패키지 설치
echo [2/3] 필요한 패키지 설치 중...
python -m pip install --upgrade pip -q
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [오류] 패키지 설치 실패. 인터넷 연결을 확인해주세요.
    pause
    exit /b 1
)
echo.

:: config.json 안내
echo [3/3] 설정 파일 확인...
if not exist config.json (
    echo [!] config.json 파일이 없습니다.
) else (
    echo     config.json 파일이 있습니다.
    echo.
    echo ================================================
    echo  [중요] 실행 전 config.json 수정 필요:
    echo  1. 네이버 개발자 API 키 입력
    echo     발급: https://developers.naver.com/apps/#/register
    echo     (검색 API - 카페, 블로그 체크)
    echo  2. hospitals 항목에 병원명과 키워드 목록 입력
    echo ================================================
)
echo.

echo 설치 완료! run.bat 을 실행하면 시작됩니다.
echo.
pause
