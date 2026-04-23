import json
import os
import sys
import webbrowser
import threading
from flask import Flask, render_template, jsonify, request

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import app.db as db
from app.collector import naver_api
from app.collector import naver_selenium

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

flask_app = Flask(__name__)
flask_app.config['TEMPLATES_AUTO_RELOAD'] = True


def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def run_collection():
    cfg = load_config()
    run_id = db.start_run()
    total_new = 0

    hospitals = cfg.get("hospitals", [])
    client_id = cfg["naver_client_id"]
    client_secret = cfg["naver_client_secret"]
    targets = cfg.get("search_targets", ["cafe", "blog"])
    max_results = cfg.get("max_results_per_keyword", 30)
    delay_min = cfg.get("delay_min", 2)
    delay_max = cfg.get("delay_max", 5)

    for hospital in hospitals:
        name = hospital["name"] if isinstance(hospital, dict) else hospital
        print(f"\n[수집] {name}")

        # 1차: 네이버 Open API
        items = naver_api.fetch_hospital(
            hospital=hospital if isinstance(hospital, dict) else {"name": hospital, "keywords": [hospital]},
            client_id=client_id,
            client_secret=client_secret,
            targets=targets,
            target_cafes=cfg.get("target_cafes", []),
            max_results=max_results,
            delay_min=delay_min,
            delay_max=delay_max,
        )

        # 2차: 플레이스 Selenium (선택)
        place_items = naver_selenium.fetch_place_reviews(
            keyword=name,
            max_results=20,
            delay_min=delay_min,
            delay_max=delay_max,
        )
        items.extend(place_items)

        saved = db.save_articles(items)
        total_new += saved
        print(f"  → 신규 저장: {saved}건")

    db.finish_run(run_id, total_new)
    print(f"\n[완료] 신규 {total_new}건 저장")
    return total_new


# ── Flask 라우트 ────────────────────────────────────────────

@flask_app.route("/")
def index():
    return render_template("index.html")


@flask_app.route("/api/stats")
def api_stats():
    return jsonify(db.get_stats())


@flask_app.route("/api/hospitals")
def api_hospitals():
    cfg = load_config()
    # config의 병원 목록 + DB에 수집된 병원 병합
    config_names = [
        h["name"] if isinstance(h, dict) else h
        for h in cfg.get("hospitals", [])
    ]
    db_names = db.get_hospitals()
    merged = list(dict.fromkeys(config_names + db_names))
    return jsonify(merged)


@flask_app.route("/api/articles")
def api_articles():
    hospital = request.args.get("hospital")
    source = request.args.get("source")
    only_new = request.args.get("only_new") == "1"
    articles = db.get_articles(hospital=hospital, source=source, only_new=only_new)
    return jsonify(articles)


@flask_app.route("/api/collect", methods=["POST"])
def api_collect():
    def _run():
        run_collection()
    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return jsonify({"status": "started"})


@flask_app.route("/api/mark_seen", methods=["POST"])
def api_mark_seen():
    data = request.get_json(silent=True) or {}
    article_id = data.get("id")
    if article_id:
        db.mark_seen(article_id)
    else:
        db.mark_all_seen()
    return jsonify({"status": "ok"})


@flask_app.route("/api/config/hospitals", methods=["GET"])
def api_get_hospitals_config():
    cfg = load_config()
    hospitals = cfg.get("hospitals", [])
    normalized = [
        h if isinstance(h, dict) else {"name": h, "keywords": [h]}
        for h in hospitals
    ]
    return jsonify(normalized)


@flask_app.route("/api/config/hospitals", methods=["POST"])
def api_save_hospitals_config():
    data = request.get_json()
    hospitals = data.get("hospitals", [])
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    cfg["hospitals"] = hospitals
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    return jsonify({"status": "ok"})


# ── 진입점 ──────────────────────────────────────────────────

def main():
    db.init()

    if "--collect" in sys.argv:
        run_collection()
        return

    print("대시보드 시작: http://localhost:8080")
    threading.Timer(1.2, lambda: webbrowser.open("http://localhost:8080")).start()
    flask_app.run(host="0.0.0.0", port=8080, debug=False)


if __name__ == "__main__":
    main()
