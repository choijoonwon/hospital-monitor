"""
데모용 샘플 데이터 DB 삽입 스크립트.
실제 네이버 API 없이 대시보드 동작을 확인할 때 사용.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import app.db as db

SAMPLES = [
    {
        "hospital": "리팅성형외과",
        "keyword": "ㄹㅌ",
        "source": "cafe",
        "title": "리팅 후기 진짜 별로임 솔직리뷰",
        "link": "https://cafe.naver.com/demo/1",
        "description": "수술 후 붓기가 너무 오래가고 상담이 불친절했어요. 원장님도 바뀐 것 같고 예전만 못한 것 같습니다. 다른 곳 알아보세요.",
        "published_at": "2026-04-21 10:00",
    },
    {
        "hospital": "리팅성형외과",
        "keyword": "리팅성형외과",
        "source": "cafe",
        "title": "리팅성형외과 상담 후기 (성예사)",
        "link": "https://cafe.naver.com/demo/2",
        "description": "상담은 친절했는데 견적이 너무 높게 나왔어요. 비슷한 시술 다른 데서 훨씬 저렴하게 했다는 글 봤는데 좀 실망이에요.",
        "published_at": "2026-04-20 14:30",
    },
    {
        "hospital": "강남피부과",
        "keyword": "ㄱㄴ피부",
        "source": "blog",
        "title": "강남피부과 레이저 시술 부작용 경험담",
        "link": "https://blog.naver.com/demo/3",
        "description": "시술 받고 나서 색소침착이 심하게 왔어요. 병원에서는 일시적이라고 했는데 3개월째 그대로입니다. 주의하세요.",
        "published_at": "2026-04-19 09:15",
    },
    {
        "hospital": "압구정클리닉",
        "keyword": "압구정클리닉",
        "source": "cafe",
        "title": "압구정클리닉 환불 거부 당함 주의",
        "link": "https://cafe.naver.com/demo/4",
        "description": "패키지 구매 후 환불 요청했더니 계속 미루고 있습니다. 소비자원 신고 예정입니다. 다들 조심하세요.",
        "published_at": "2026-04-18 11:00",
    },
    {
        "hospital": "리팅성형외과",
        "keyword": "000원장",
        "source": "cafe",
        "title": "000원장 실력 논란 여우야 펌",
        "link": "https://cafe.naver.com/demo/5",
        "description": "여우야에서 퍼온 글인데 원장 바뀐 이후로 결과가 들쭉날쭉하다는 얘기가 많네요. 참고하세요.",
        "published_at": "2026-04-17 16:45",
    },
    {
        "hospital": "강남피부과",
        "keyword": "강남피부과",
        "source": "place",
        "title": "[플레이스 리뷰] 강남피부과",
        "link": "https://map.naver.com/demo/6",
        "description": "직원이 너무 불친절하고 대기시간이 너무 길어요. 예약하고 갔는데도 1시간 기다렸습니다.",
        "published_at": "2026-04-16 13:20",
    },
    {
        "hospital": "압구정클리닉",
        "keyword": "압구정",
        "source": "blog",
        "title": "압구정클리닉 쌍꺼풀 재수술 후기",
        "link": "https://blog.naver.com/demo/7",
        "description": "처음 수술이 비대칭으로 나와서 재수술 요청했는데 추가 비용을 요구해서 황당했습니다.",
        "published_at": "2026-04-15 10:00",
    },
]


def insert_demo():
    db.init()
    saved = db.save_articles(SAMPLES)
    print(f"[데모] 샘플 데이터 {saved}건 삽입 완료 (이미 있는 항목은 건너뜀)")


if __name__ == "__main__":
    insert_demo()
