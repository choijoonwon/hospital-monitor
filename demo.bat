@echo off
chcp 65001 > nul
echo ================================================
echo  병원 모니터링 시스템 - 데모 모드
echo  (샘플 데이터로 대시보드를 미리 확인합니다)
echo ================================================
echo.

python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [오류] Python을 찾을 수 없습니다. setup.bat 을 먼저 실행하세요.
    pause
    exit /b 1
)

echo 샘플 데이터 삽입 중...
python app/demo_data.py
echo.
echo 대시보드를 시작합니다... (http://localhost:5000)
echo [종료하려면 이 창을 닫으세요]
echo.

python app/main.py
pause
