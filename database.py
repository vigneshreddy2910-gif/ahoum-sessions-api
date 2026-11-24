
import os
import sqlite3


DATABASE_PATH = os.getenv("DATABASE_PATH", "data/sessions.db")


def get_connection():
    directory = os.path.dirname(DATABASE_PATH)

    if directory:
        os.makedirs(directory, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                duration INTEGER NOT NULL CHECK (duration > 0)
            )
        """)
        connection.commit()


def get_all_sessions():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, title, description, category, duration "
            "FROM sessions ORDER BY id"
        ).fetchall()

        return [dict(row) for row in rows]


def create_session(title, description, category, duration):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO sessions
            (title, description, category, duration)
            VALUES (?, ?, ?, ?)
            """,
            (title, description, category, duration)
        )

        connection.commit()
        return cursor.lastrowid


def check_database():
    with get_connection() as connection:
        connection.execute("SELECT 1")
