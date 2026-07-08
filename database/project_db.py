from database.database import get_connection


def add_project(name, deadline, estimated_hours_required, priority):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO projects(
            name,
            deadline,
            estimated_hours_required,
            worked_hours,
            priority,
            progress,
            status
        )
        VALUES (?, ?, ?, 0, ?, 0, 'Active')
    """, (
        name,
        deadline,
        estimated_hours_required,
        priority,
    ))

    conn.commit()
    conn.close()


def get_active_projects():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
        id,
        name,
        deadline,
        estimated_hours_required,
        worked_hours,
        priority,
        progress,
        status
        FROM projects
        WHERE status = 'Active'
        ORDER BY deadline
    """)

    projects = cursor.fetchall()

    conn.close()

    return projects

def get_project(project_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            name,
            deadline,
            estimated_hours_required,
            priority
        FROM projects
        WHERE id = ?
    """, (project_id,))

    project = cursor.fetchone()

    conn.close()

    return project

def get_active_project_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM projects
        WHERE status = 'Active'
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count

def get_all_projects():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
        id,
        name,
        deadline,
        estimated_hours_required,
        worked_hours,
        priority,
        progress,
        status

        FROM projects

        ORDER BY 
        CASE 
            WHEN status='Active' THEN 0
            ELSE 1
        END,
        deadline
    """)

    projects = cursor.fetchall()

    conn.close()

    return projects


def delete_project(project_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM projects WHERE id = ?",
        (project_id,)
    )

    conn.commit()
    conn.close()


def update_project_progress(project_id, progress):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE projects
        SET progress = ?
        WHERE id = ?
    """, (
        progress,
        project_id
    ))

    conn.commit()
    conn.close()

def update_project(
    project_id,
    name,
    deadline,
    estimated_hours_required,
    priority
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE projects
        SET
            name = ?,
            deadline = ?,
            estimated_hours_required = ?,
            priority = ?
        WHERE id = ?
    """, (
        name,
        deadline,
        estimated_hours_required,
        priority,
        project_id
    ))

    conn.commit()
    conn.close()


def get_next_deadline():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            name,
            deadline
        FROM projects
        WHERE status = 'Active'
        ORDER BY deadline
        LIMIT 1
    """)

    project = cursor.fetchone()

    conn.close()

    return project

def get_active_project_names():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name
        FROM projects
        WHERE status='Active'
        ORDER BY name
    """)

    projects = cursor.fetchall()

    conn.close()

    return projects

def add_worked_minutes(project_id, minutes):

    conn = get_connection()
    cursor = conn.cursor()

    hours = minutes / 60

    cursor.execute("""
    UPDATE projects
    SET worked_hours = worked_hours + ?
    WHERE id=?
    """,(hours, project_id))

    cursor.execute("""
    SELECT worked_hours,
           estimated_hours_required
    FROM projects
    WHERE id=?
    """,(project_id,))

    worked, estimated = cursor.fetchone()

    if estimated <= 0:
        progress = 0
    else:
        progress = min(
            int((worked / estimated) * 100),
            100
        )

    status = "Completed" if progress >= 100 else "Active"

    cursor.execute("""
    UPDATE projects
    SET
        progress = ?,
        status = ?
    WHERE id = ?
    """, (
        progress,
        status,
        project_id
    ))

    conn.commit()
    conn.close()

def remove_worked_minutes(project_id, minutes):

    conn = get_connection()
    cursor = conn.cursor()

    hours = minutes / 60

    # Reduce worked hours (never below 0)
    cursor.execute("""
        UPDATE projects
        SET worked_hours =
            CASE
                WHEN worked_hours - ? < 0 THEN 0
                ELSE worked_hours - ?
            END
        WHERE id = ?
    """, (
        hours,
        hours,
        project_id
    ))

    # Read updated values
    cursor.execute("""
        SELECT worked_hours,
               estimated_hours_required
        FROM projects
        WHERE id = ?
    """, (project_id,))

    worked, estimated = cursor.fetchone()

    # Recalculate progress
    if estimated <= 0:
        progress = 0
    else:
        progress = min(
            int((worked / estimated) * 100),
            100
        )

    status = "Completed" if progress >= 100 else "Active"

    cursor.execute("""
    UPDATE projects
    SET
        progress = ?,
        status = ?
    WHERE id = ?
    """, (
        progress,
        status,
        project_id
    ))
    conn.commit()
    conn.close()