import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "app/db/users.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # access columns by name
    return conn


def init_db():
    """Create the users table if it doesn't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            email     TEXT    UNIQUE NOT NULL,
            password  TEXT    NOT NULL,
            created_at TEXT   DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


# ── User helpers ────────────────────────────────────────────────────────────

def create_user(email: str, hashed_password: str):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, hashed_password)
        )
        conn.commit()
    finally:
        conn.close()


def get_user_by_email(email: str):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def email_exists(email: str) -> bool:
    return get_user_by_email(email) is not None