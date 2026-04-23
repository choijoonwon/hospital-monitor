import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "monitor.db")


def _conn() -> sqlite3.Connection:
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def init():
    with _conn() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                hospital     TEXT NOT NULL,
                keyword      TEXT,
                source       TEXT NOT NULL,
                title        TEXT NOT NULL,
                link         TEXT NOT NULL UNIQUE,
                description  TEXT,
                published_at TEXT,
                collected_at TEXT NOT NULL,
                is_new       INTEGER NOT NULL DEFAULT 1
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at TEXT NOT NULL,
                ended_at   TEXT,
                new_count  INTEGER DEFAULT 0
            )
        """)


def save_articles(items: list) -> int:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    saved = 0
    with _conn() as con:
        for item in items:
            try:
                con.execute(
                    """
                    INSERT INTO articles
                        (hospital, keyword, source, title, link,
                         description, published_at, collected_at, is_new)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
                    """,
                    (
                        item["hospital"], item.get("keyword"),
                        item["source"], item["title"], item["link"],
                        item["description"], item["published_at"], now,
                    ),
                )
                saved += 1
            except sqlite3.IntegrityError:
                pass
    return saved


def start_run() -> int:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with _conn() as con:
        cur = con.execute("INSERT INTO runs (started_at) VALUES (?)", (now,))
        return cur.lastrowid


def finish_run(run_id: int, new_count: int):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with _conn() as con:
        con.execute(
            "UPDATE runs SET ended_at=?, new_count=? WHERE id=?",
            (now, new_count, run_id),
        )


def mark_seen(article_id: int):
    with _conn() as con:
        con.execute("UPDATE articles SET is_new=0 WHERE id=?", (article_id,))

def mark_all_seen():
    with _conn() as con:
        con.execute("UPDATE articles SET is_new=0 WHERE is_new=1")


def get_articles(hospital: str = None, source: str = None,
                 only_new: bool = False, limit: int = 300) -> list:
    wheres, params = [], []
    if hospital:
        wheres.append("hospital=?")
        params.append(hospital)
    if source:
        wheres.append("source=?")
        params.append(source)
    if only_new:
        wheres.append("is_new=1")

    where_sql = ("WHERE " + " AND ".join(wheres)) if wheres else ""
    sql = f"""
        SELECT * FROM articles {where_sql}
        ORDER BY collected_at DESC, id DESC
        LIMIT {limit}
    """
    with _conn() as con:
        return [dict(r) for r in con.execute(sql, params).fetchall()]


def get_hospitals() -> list:
    with _conn() as con:
        rows = con.execute(
            "SELECT DISTINCT hospital FROM articles ORDER BY hospital"
        ).fetchall()
        return [r["hospital"] for r in rows]


def get_stats() -> dict:
    with _conn() as con:
        total = con.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
        new = con.execute("SELECT COUNT(*) FROM articles WHERE is_new=1").fetchone()[0]
        last_run = con.execute(
            "SELECT started_at, new_count FROM runs ORDER BY id DESC LIMIT 1"
        ).fetchone()
    return {
        "total": total,
        "new": new,
        "last_run": dict(last_run) if last_run else None,
    }
