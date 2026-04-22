@echo off
chcp 65001 > nul
echo ================================================
echo  병원 모니터링 시스템 시작
echo ================================================
echo.

:: Python 확인
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [오류] Python을 찾을 수 없습니다. setup.bat 을 먼저 실행하세요.
    pause
    exit /b 1
)

:: config.json API 키 확인
python -c "import json; c=json.load(open('config.json',encoding='utf-8')); exit(0 if c.get('naver_client_id','').strip() not in ('','YOUR_NAVER_CLIENT_ID') else 1)" 2>nul
if %errorlevel% neq 0 (
    echo [!] config.json 에 네이버 API 키가 입력되지 않았습니다.
    echo     config.json 파일을 열어 naver_client_id / naver_client_secret 을 입력해주세요.
    echo.
    echo     API 키 발급: https://developers.naver.com/apps/#/register
    pause
    exit /b 1
)

echo 대시보드를 시작합니다...
echo 브라우저에서 http://localhost:5000 으로 자동으로 열립니다.
echo.
echo [종료하려면 이 창을 닫으세요]
echo.

python app/main.py
pause
