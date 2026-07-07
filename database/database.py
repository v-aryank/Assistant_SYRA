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

    estimated_hours_required INTEGER,

    worked_hours REAL DEFAULT 0,

    priority TEXT,

    progress INTEGER DEFAULT 0,

    status TEXT DEFAULT 'Active'

    )
    """)

    # ================= Tasks =================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        date TEXT,
        start_time TEXT,
        end_time TEXT,
        completed INTEGER DEFAULT 0,
        project_id INTEGER,
        system_generated INTEGER DEFAULT 0,
        planned_minutes INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()