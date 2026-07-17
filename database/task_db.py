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
def add_task(
    title,
    date,
    start_time,
    end_time,
    project_id=None,
    system_generated=0,
    planned_minutes=0
    ):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks(
            title,
            date,
            start_time,
            end_time,
            project_id,
            system_generated,
            planned_minutes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        date,
        start_time,
        end_time,
        project_id,
        system_generated,
        planned_minutes
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
    WHERE id=?
    """,(task_id,))

    conn.commit()

    cursor.execute("""
    SELECT completed
    FROM tasks
    WHERE id=?
    """,(task_id,))
    row = cursor.fetchone()

    completed = row[0] if row else 0

    conn.close()

    return completed
    

def get_next_task(today, now):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
        title,
        start_time,
        end_time
        FROM tasks
        WHERE
        date=?
        AND completed=0
        AND end_time>=?
        ORDER BY start_time
        LIMIT 1
    """, (today, now))

    task = cursor.fetchone()

    conn.close()

    return task

def add_project_session(
        project_id,
        project_name, 
        date, 
        start, 
        end,
        planned_minutes
        ):

    add_task(
        title=f"Project Work — {project_name}",
        date=date,
        start_time=start,
        end_time=end,
        project_id=project_id,
        system_generated=1,
        planned_minutes=planned_minutes
    )
def get_project_task(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            project_id,
            planned_minutes,
            system_generated
        FROM tasks
        WHERE id=?
    """,(task_id,))

    row = cursor.fetchone()

    conn.close()

    return row

def has_project_session_today(project_id, today):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM tasks
    WHERE
        project_id=?
        AND date=?
        AND system_generated=1
    """,(project_id, today))

    count = cursor.fetchone()[0]

    conn.close()

    return count > 0

def get_project_minutes_today(project_id, date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(planned_minutes), 0)
        FROM tasks
        WHERE
            project_id = ?
            AND date = ?
            AND system_generated = 1
    """, (
        project_id,
        date
    ))

    total = cursor.fetchone()[0]

    conn.close()

    return total

def routine_exists_today(title, date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE
            title=?
            AND date=?
            AND system_generated=1
    """, (
        title,
        date
    ))

    exists = cursor.fetchone()[0]

    conn.close()

    return exists > 0

def delete_today_routines(today):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE
            date=?
            AND system_generated=1
            AND project_id IS NULL
    """, (today,))

    conn.commit()
    conn.close()