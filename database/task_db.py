from database.database import get_connection


def get_tasks(view, today=None, tomorrow=None, end_week=None):

    conn = get_connection()
    cursor = conn.cursor()

    # ================= TODAY =================

    if view == "Today":

        cursor.execute("""
            SELECT id, title, date,
                   start_time, end_time,
                   completed
            FROM tasks
            WHERE date=?
            ORDER BY start_time
        """, (today,))

    # ================= TOMORROW =================

    elif view == "Tomorrow":

        cursor.execute("""
            SELECT id, title, date,
                   start_time, end_time,
                   completed
            FROM tasks
            WHERE date=?
            ORDER BY start_time
        """, (tomorrow,))

    # ================= WEEK =================

    elif view == "This Week":

        cursor.execute("""
            SELECT id,title,date,
                   start_time,end_time,
                   completed
            FROM tasks
            WHERE date BETWEEN ? AND ?
            ORDER BY date,start_time
        """, (today, end_week))

    # ================= ALL =================

    else:

        cursor.execute("""
            SELECT id,title,date,
                   start_time,end_time,
                   completed
            FROM tasks
            ORDER BY date,start_time
        """)

    tasks = cursor.fetchall()

    conn.close()

    return tasks

#================= Get a specific task =================
def get_task(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title,
               date,
               start_time,
               end_time
        FROM tasks
        WHERE id = ?
    """, (task_id,))

    task = cursor.fetchone()

    conn.close()

    return task

#================= Tasks =================
def add_task(title, date, start_time, end_time):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks(
            title,
            date,
            start_time,
            end_time
        )
        VALUES (?, ?, ?, ?)
    """, (
        title,
        date,
        start_time,
        end_time
    ))

    conn.commit()
    conn.close()


#================= Update a task =================
def update_task(
    task_id,
    title,
    date,
    start_time,
    end_time
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET
            title=?,
            date=?,
            start_time=?,
            end_time=?
        WHERE id=?
    """, (
        title,
        date,
        start_time,
        end_time,
        task_id
    ))

    conn.commit()
    conn.close()


#================= Delete a task =================
def delete_task(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()


#================= Toggle task completion =================

def toggle_task_completion(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET completed =
            CASE completed
                WHEN 0 THEN 1
                ELSE 0
            END
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()

def get_next_task(today):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title,
               start_time,
               end_time
        FROM tasks
        WHERE date = ?
          AND completed = 0
        ORDER BY start_time
        LIMIT 1
    """, (today,))

    task = cursor.fetchone()

    conn.close()

    return task