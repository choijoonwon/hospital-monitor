import requests
import time
import random
import html
import re
from datetime import datetime


SEARCH_URLS = {
    "cafe": "https://openapi.naver.com/v1/search/cafearticle.json",
    "blog": "https://openapi.naver.com/v1/search/blog.json",
}


def _strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", html.unescape(text)).strip()


def _parse_date(raw: str) -> str:
    for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%Y%m%d"):
        try:
            dt = datetime.strptime(raw, fmt)
            return dt.strftime("%Y-%m-%d %H:%M")
        except Exception:
            continue
    return raw


def _fetch_keyword(keyword: str, hospital_name: str, client_id: str,
                   client_secret: str, targets: list,
                   max_results: int, delay_min: float, delay_max: float) -> list:
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }
    results = []

    for target in targets:
        url = SEARCH_URLS.get(target)
        if not url:
            continue

        params = {
            "query": keyword,
            "display": min(max_results, 100),
            "sort": "date",
        }

        try:
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            items = resp.json().get("items", [])
        except Exception as e:
            print(f"[API 오류] {keyword} / {target}: {e}")
            items = []

        for item in items:
            results.append({
                "hospital": hospital_name,
                "keyword": keyword,
                "source": target,
                "title": _strip_tags(item.get("title", "")),
                "link": item.get("link", item.get("url", "")),
                "description": _strip_tags(item.get("description", ""))[:300],
                "published_at": _parse_date(
                    item.get("postdate", item.get("pubDate", ""))
                ),
            })

        time.sleep(random.uniform(delay_min, delay_max))

    return results


def fetch_hospital(hospital: dict, client_id: str, client_secret: str,
                   targets: list, max_results: int = 30,
                   delay_min: float = 2.0, delay_max: float = 5.0) -> list:
    """
    hospital = {"name": str, "keywords": [str, ...]}
    병원의 모든 키워드 변형으로 검색 후 합산 결과 반환.
    """
    all_results = []
    for kw in hospital.get("keywords", [hospital.get("name", "")]):
        results = _fetch_keyword(
            keyword=kw,
            hospital_name=hospital["name"],
            client_id=client_id,
            client_secret=client_secret,
            targets=targets,
            max_results=max_results,
            delay_min=delay_min,
            delay_max=delay_max,
        )
        all_results.extend(results)
        print(f"  키워드 '{kw}': {len(results)}건 수집")
    return all_results
