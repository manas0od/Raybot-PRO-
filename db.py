import sqlite3
from datetime import datetime
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            name TEXT,
            created_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            session_id INTEGER,
            role TEXT,
            content TEXT,
            ts TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY,
            session_id INTEGER,
            key TEXT,
            value TEXT,
            ts TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

def create_session(name="default"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    ts = datetime.utcnow().isoformat()

    c.execute("INSERT INTO sessions (name, created_at) VALUES (?,?)", (name, ts))

    sid = c.lastrowid
    conn.commit()
    conn.close()
    return sid

def append_event(session_id, role, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    ts = datetime.utcnow().isoformat()

    c.execute(
        "INSERT INTO events (session_id, role, content, ts) VALUES (?,?,?,?)",
        (session_id, role, content, ts)
    )

    conn.commit()
    conn.close()

def get_recent_events(session_id, limit=50):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "SELECT role, content, ts FROM events WHERE session_id=? ORDER BY id DESC LIMIT ?",
        (session_id, limit)
    )

    rows = c.fetchall()
    conn.close()
    return rows[::-1]

def remember(session_id, key, value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    ts = datetime.utcnow().isoformat()

    c.execute(
        "INSERT INTO memory (session_id, key, value, ts) VALUES (?,?,?,?)",
        (session_id, key, value, ts)
    )

    conn.commit()
    conn.close()

def recall(session_id, key):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "SELECT value FROM memory WHERE session_id=? AND key=? ORDER BY id DESC LIMIT 1",
        (session_id, key)
    )

    r = c.fetchone()
    conn.close()

    return r[0] if r else None