#!/bin/bash
echo "================================================"
echo " 병원 모니터링 - 데모 모드 (Mac)"
echo "================================================"
echo ""

cd "$(dirname "$0")"

# 패키지 설치
echo "[1/2] 패키지 설치 중..."
pip3 install -r requirements.txt -q

# 데모 데이터 삽입 후 서버 실행
echo "[2/2] 샘플 데이터 삽입 및 서버 시작..."
python3 app/demo_data.py
python3 app/main.py
