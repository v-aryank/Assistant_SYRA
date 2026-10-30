from datetime import date

import database.routine_db as routine_db
import database.task_db as task_db


def inject_today_routines():

    today = date.today().strftime("%Y-%m-%d")

    routines = routine_db.get_today_routines()

    task_db.delete_today_routines(today)



    for routine in routines:

        (
            routine_id,
            title,
            category,
            visible_in_schedule,
            start,
            end
        ) = routine

        if routine_db.is_routine_skipped(routine_id):
            continue

        if not visible_in_schedule:
            continue

        task_title = f"Routine — {title}"

        if task_db.routine_exists_today(
            task_title,
            today,
            start,
            end
        ):
            continue

        task_db.add_task(
            title=task_title,
            date=today,
            start_time=start,
            end_time=end,
            project_id=-routine_id,
            system_generated=1,
            planned_minutes=0
        )