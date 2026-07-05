import sqlite3

DB_NAME = "sira_schedule.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # ================= Projects =================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        deadline TEXT,
        hours_required INTEGER,
        priority TEXT,
        progress INTEGER DEFAULT 0
    )
    """)

    # ================= Tasks =================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date TEXT NOT NULL,
        start_time TEXT,
        end_time TEXT,
        completed INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()