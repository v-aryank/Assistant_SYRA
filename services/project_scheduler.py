from datetime import date, datetime, timedelta

import database.project_db as project_db
import database.task_db as task_db


def generate_project_recommendation():

    today = date.today()

    projects = project_db.get_active_projects()

    if not projects:
        return None

    recommendations = []

    for project in projects:

        (
            project_id,
            name,
            deadline,
            estimated,
            worked,
            priority,
            progress,
            status
        ) = project

        if task_db.has_project_session_today(
            project_id,
            today.strftime("%Y-%m-%d")
        ):
            continue

        deadline_date = datetime.strptime(
            deadline,
            "%Y-%m-%d"
        ).date()

        remaining_days = (deadline_date - today).days

        if remaining_days <= 0:
            continue

        remaining_hours = max(0, estimated - worked)

        if remaining_hours == 0:
            continue
        
        daily_hours = remaining_hours / remaining_days

        priority_multiplier = {
            "High": 1.5,
            "Medium": 1.2,
            "Low": 1.0
        }.get(priority, 1.0)

        urgency_score = round(
            daily_hours * priority_multiplier,
            2
        )

        recommendations.append({

            "project_id": project_id,

            "name": name,

            "remaining_hours": remaining_hours,

            "remaining_days": remaining_days,

            "daily_hours": round(daily_hours, 2),

            "priority": priority,

            "urgency_score": urgency_score

        })
    #find free slots
    tasks = task_db.get_tasks(
        "Today",
        today.strftime("%Y-%m-%d"),
        None,
        None
    )

    free_slots = find_free_time(tasks)

    
    recommendations.sort(
        key=lambda p: p["urgency_score"],
        reverse=True
    )
    if not recommendations:
     return None

    best_project = recommendations[0]

    slot = choose_best_slot(
        free_slots,
        best_project["daily_hours"]
    )

    best_project["recommended_slot"] = slot

    return best_project

# --------------- Find free time ---------------

def find_free_time(tasks):

    now = datetime.now()

    day_start = datetime.strptime(
        now.strftime("%H:%M"),
        "%H:%M"
    )
    day_end = datetime.strptime("23:59", "%H:%M")

    free_slots = []

    current = day_start

    for task in tasks:

        _, _, _, start, end, _ = task

        start_time = datetime.strptime(start, "%H:%M")
        end_time = datetime.strptime(end, "%H:%M")

        if start_time > current:

            free_slots.append(
                (
                    current.strftime("%H:%M"),
                    start_time.strftime("%H:%M")
                )
            )

        if end_time > current:
            current = end_time

    if current < day_end:

        free_slots.append(
            (
                current.strftime("%H:%M"),
                day_end.strftime("%H:%M")
            )
        )

    return free_slots

#----------Choose Best Slot---------------

def choose_best_slot(free_slots, required_hours):

    required_minutes = int(required_hours * 60)

    for start, end in free_slots:

        start_time = datetime.strptime(
            start,
            "%H:%M"
        )

        end_time = datetime.strptime(
            end,
            "%H:%M"
        )

        available = int(
            (end_time - start_time).total_seconds() / 60
        )

        if available >= required_minutes:

            finish = start_time + timedelta(
                minutes=required_minutes
            )

            return (
                start,
                finish.strftime("%H:%M")
            )

    return None