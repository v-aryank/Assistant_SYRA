import sqlite3

conn = sqlite3.connect("sira_schedule.db")
cursor = conn.cursor()

# Projects table
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
# Tasks table
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