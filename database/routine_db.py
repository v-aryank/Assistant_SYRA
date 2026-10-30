from database.database import get_connection
from datetime import datetime, date


def add_routine(
    title,
    category,
    visible_in_schedule,
    start_time,
    end_time,
    sunday,
    monday,
    tuesday,
    wednesday,
    thursday,
    friday,
    saturday,
    enabled=1
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO routines(
            title,
            category,
            visible_in_schedule,
            start_time,
            end_time,
            sunday,
            monday,
            tuesday,
            wednesday,
            thursday,
            friday,
            saturday,
            enabled
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        category,
        visible_in_schedule,
        start_time,
        end_time,
        sunday,
        monday,
        tuesday,
        wednesday,
        thursday,
        friday,
        saturday,
        enabled
    ))

    conn.commit()
    conn.close()


def update_routine(
    routine_id,
    title,
    category,
    visible_in_schedule,
    start_time,
    end_time,
    sunday,
    monday,
    tuesday,
    wednesday,
    thursday,
    friday,
    saturday,
    enabled
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE routines
        SET
            title=?,
            category=?,
            visible_in_schedule=?,
            start_time=?,
            end_time=?,
            sunday=?,
            monday=?,
            tuesday=?,
            wednesday=?,
            thursday=?,
            friday=?,
            saturday=?,
            enabled=?
        WHERE id=?
    """, (
        title,
        category,
        visible_in_schedule,
        start_time,
        end_time,
        sunday,
        monday,
        tuesday,
        wednesday,
        thursday,
        friday,
        saturday,
        enabled,
        routine_id
    ))

    conn.commit()
    conn.close()

def delete_routine(routine_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM routines
        WHERE id=?
    """, (routine_id,))

    conn.commit()
    conn.close()



def get_all_routines():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            category,
            visible_in_schedule,
            start_time,
            end_time,
            sunday,
            monday,
            tuesday,
            wednesday,
            thursday,
            friday,
            saturday,
            enabled
        FROM routines
        ORDER BY start_time
    """)

    routines = cursor.fetchall()

    conn.close()

    return routines


def get_routine(routine_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            title,
            category,
            visible_in_schedule,
            start_time,
            end_time,
            sunday,
            monday,
            tuesday,
            wednesday,
            thursday,
            friday,
            saturday,
            enabled
        FROM routines
        WHERE id=?
    """, (routine_id,))

    routine = cursor.fetchone()

    conn.close()

    return routine


def get_today_routines():

    weekday = date.today().strftime("%A").lower()

    conn = get_connection()
    cursor = conn.cursor()

    query = f"""
        SELECT
            id,
            title,
            category,
            visible_in_schedule,
            start_time,
            end_time
        FROM routines
        WHERE
            {weekday}=1
            AND enabled=1
        ORDER BY start_time
    """

    cursor.execute(query)

    routines = cursor.fetchall()

    conn.close()

    return routines


def get_hidden_routines_for_today():

    weekday = date.today().strftime("%A").lower()

    conn = get_connection()
    cursor = conn.cursor()

    query = f"""
        SELECT
            start_time,
            end_time
        FROM routines
        WHERE
            {weekday}=1
            AND enabled=1
            AND visible_in_schedule=0
        ORDER BY start_time
    """

    cursor.execute(query)

    routines = cursor.fetchall()

    conn.close()

    return routines


def skip_routine_for_today(routine_id):

    today = date.today().strftime("%Y-%m-%d")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO skipped_routines(
            routine_id,
            skip_date
        )
        VALUES (?,?)
    """,(routine_id,today))

    conn.commit()
    conn.close()


def is_routine_skipped(routine_id):

    today = date.today().strftime("%Y-%m-%d")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM skipped_routines
        WHERE
            routine_id=?
            AND skip_date=?
    """,(routine_id,today))

    skipped = cursor.fetchone()[0]

    conn.close()

    return skipped > 0