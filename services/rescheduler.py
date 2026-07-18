import database.task_db as task_db

from services.free_time_analyzer import get_free_time_slots

from services.scheduler_engine import time_to_minutes
from services.scheduler_engine import minutes_to_time


def reschedule_unfinished_tasks():

    tasks = task_db.get_unfinished_ai_tasks()

    slots = get_free_time_slots()

    moved = []

    for task in tasks:

        (
            task_id,
            title,
            old_start,
            old_end,
            planned_minutes,
            project_id
        ) = task

        if planned_minutes <= 0:
            continue

        for slot in slots:

            if slot["duration"] < planned_minutes:
                continue

            start = time_to_minutes(
                slot["start"]
            )

            end = start + planned_minutes

            new_start = minutes_to_time(start)
            new_end = minutes_to_time(end)

            task_db.update_task_time(
                task_id,
                new_start,
                new_end
            )

            moved.append({

                "title": title,

                "old_start": old_start,
                "old_end": old_end,

                "new_start": new_start,
                "new_end": new_end

            })

            slot["start"] = new_end
            slot["duration"] -= planned_minutes

            break

    return moved