import sqlite3

conn = sqlite3.connect("SYRA_schedule.db")

cursor = conn.cursor()

cursor.execute("""
SELECT
title,
monday,
tuesday,
wednesday,
thursday,
friday,
saturday,
sunday
FROM routines
""")

for row in cursor.fetchall():
    print(row)

conn.close()