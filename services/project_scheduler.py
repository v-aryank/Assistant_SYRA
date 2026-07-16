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


        try:
            deadline_date = datetime.strptime(
                deadline,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            continue

        remaining_days = (deadline_date - today).days

        if remaining_days < 0:
            continue

        if remaining_days == 0:
            remaining_days = 1
        
        # Remaining work
        remaining_hours = max(0, estimated - worked)

        if remaining_hours == 0:
            continue
        
        # Today's ideal target
        daily_hours = remaining_hours / remaining_days

        # Round today's target to whole minutes
        daily_minutes = round(daily_hours * 60)
        
        #Already scheduled today
        scheduled_today = task_db.get_project_minutes_today(
            project_id,
            today.strftime("%Y-%m-%d")
        )
        
        # Recommend only the unscheduled part
        daily_minutes = max(
            0,
            daily_minutes - scheduled_today
        )
        
        if daily_minutes == 0:
            continue

        daily_hours = daily_minutes / 60


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

            "daily_minutes": daily_minutes,

            "daily_hours": daily_hours,

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


    return recommendations

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

def choose_best_slot(free_slots, required_minutes):

    best_slot = None
    biggest = 0

    for start, end in free_slots:

        start_time = datetime.strptime(start, "%H:%M")
        end_time = datetime.strptime(end, "%H:%M")

        available = int(
            (end_time - start_time).total_seconds() / 60
        )

        if available >= required_minutes:

            finish = start_time + timedelta(
                minutes=required_minutes
            )

            return {

                "scheduled_start": start,

                "scheduled_end": finish.strftime("%H:%M"),

                "scheduled_minutes": required_minutes,

                "completed": True
            }

        if available > biggest:

            biggest = available

            best_slot = {

                "scheduled_start": start,

                "scheduled_end": end,

                "scheduled_minutes": available,

                "completed": False
            }

    return best_slot



def generate_daily_schedule():

    recommendations = generate_project_recommendation()

    if not recommendations:
        return []

    tasks = task_db.get_tasks(
        "Today",
        date.today().strftime("%Y-%m-%d"),
        None,
        None
    )

    free_slots = find_free_time(tasks)

    result = []

    for project in recommendations:

        slot = choose_best_slot(
            free_slots,
            project["daily_minutes"]
        )

        if slot is None:
            continue

        scheduled = slot["scheduled_minutes"]

        project["recommended_slot"] = slot

        project["target_minutes"] = project["daily_minutes"]

        project["scheduled_minutes"] = scheduled

        project["remaining_minutes"] = (
            project["daily_minutes"] - scheduled
        )

        result.append(project)

    return result