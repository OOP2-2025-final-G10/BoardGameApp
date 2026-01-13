import sqlite3

DB_PATH = "game.db"

def get_db():
    conn = sqlite3.connect(
        "game.db",
        timeout=10,
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row

    # ★ ロック対策（必須）
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")

    return conn