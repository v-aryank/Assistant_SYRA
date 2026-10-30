import sqlite3

DB_NAME = "FRIDAY_schedule.db"


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
        status TEXT DEFAULT 'Pending',
        project_id INTEGER,
        system_generated INTEGER DEFAULT 0,
        planned_minutes INTEGER DEFAULT 0
    )
    """)

    #================== Routines =====================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS routines(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT NOT NULL,
                   
    category TEXT DEFAULT 'General',
                   
    visible_in_schedule INTEGER DEFAULT 1,

    start_time TEXT NOT NULL,

    end_time TEXT NOT NULL,

    sunday INTEGER DEFAULT 0,
    monday INTEGER DEFAULT 0,
    tuesday INTEGER DEFAULT 0,
    wednesday INTEGER DEFAULT 0,
    thursday INTEGER DEFAULT 0,
    friday INTEGER DEFAULT 0,
    saturday INTEGER DEFAULT 0,
                   
    enabled INTEGER DEFAULT 1
    );
    """)

    # ================= Routine Skip =================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skipped_routines(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        routine_id INTEGER NOT NULL,

        skip_date TEXT NOT NULL,

        UNIQUE(routine_id, skip_date)
    )
    """)

    conn.commit()
    conn.close()