"""
Selenium 보완 수집 모듈 - 네이버 플레이스 리뷰 등 API가 닿지 않는 영역.
undetected-chromedriver 사용으로 기본 봇 탐지 우회.
"""
import time
import random
from datetime import datetime

try:
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


def _random_delay(min_s: float = 2.0, max_s: float = 5.0):
    time.sleep(random.uniform(min_s, max_s))


def _make_driver() -> "uc.Chrome":
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")
    driver = uc.Chrome(options=options, use_subprocess=True)
    return driver


def fetch_place_reviews(keyword: str, max_results: int = 20,
                        delay_min: float = 2.0, delay_max: float = 5.0) -> list:
    """
    네이버 플레이스 검색 → 상위 결과의 최신 리뷰 수집.
    실패 시 빈 리스트 반환 (안전 우선).
    """
    if not SELENIUM_AVAILABLE:
        print("[Selenium] undetected-chromedriver 미설치, 건너뜀")
        return []

    results = []
    driver = None
    try:
        driver = _make_driver()
        search_url = f"https://map.naver.com/v5/search/{keyword}"
        driver.get(search_url)
        _random_delay(delay_min, delay_max)

        # 검색 결과 iframe 진입
        wait = WebDriverWait(driver, 10)
        try:
            frame = wait.until(EC.presence_of_element_located((By.ID, "searchIframe")))
            driver.switch_to.frame(frame)
        except Exception:
            return []

        _random_delay(1.5, 3.0)

        # 첫 번째 병원 결과 클릭
        try:
            items = driver.find_elements(By.CSS_SELECTOR, "li.UEzoS")
            if not items:
                return []
            items[0].click()
            _random_delay(delay_min, delay_max)
        except Exception:
            return []

        # 리뷰 탭으로 이동 (메인 프레임으로 전환 후 상세 iframe)
        driver.switch_to.default_content()
        try:
            detail_frame = wait.until(
                EC.presence_of_element_located((By.ID, "entryIframe"))
            )
            driver.switch_to.frame(detail_frame)
        except Exception:
            return []

        _random_delay(1.5, 3.0)

        # 리뷰 요소 수집
        try:
            review_els = driver.find_elements(By.CSS_SELECTOR, "li.pui__X35jYm")[:max_results]
        except Exception:
            review_els = []

        for el in review_els:
            try:
                text = el.find_element(By.CSS_SELECTOR, "span.pui__xtsQN-").text.strip()
                date_raw = el.find_element(By.CSS_SELECTOR, "span.pui__gfuPNc").text.strip()
            except Exception:
                continue

            results.append({
                "hospital": keyword,
                "source": "place",
                "title": f"[플레이스 리뷰] {keyword}",
                "link": driver.current_url,
                "description": text[:200],
                "published_at": date_raw,
            })

    except Exception as e:
        print(f"[Selenium 오류] {keyword}: {e}")
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

    return results
