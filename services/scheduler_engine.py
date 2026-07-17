from datetime import date, datetime

from services.free_time_analyzer import get_free_time_slots

import database.project_db as project_db

from database.project_db import get_all_projects

MAX_FOCUS_SESSION = 90

TIME_FORMAT = "%H:%M"


def time_to_minutes(t):

    dt = datetime.strptime(t, TIME_FORMAT)

    return dt.hour * 60 + dt.minute


def minutes_to_time(minutes):

    hour = minutes // 60

    minute = minutes % 60

    return f"{hour:02}:{minute:02}"

def get_sorted_projects():

    projects = get_all_projects()

    scored = []

    for project in projects:

        if project[7] != "Active":
            continue

        scored.append(
            calculate_project_score(project)
        )

    scored.sort(
        key=lambda p: p["score"],
        reverse=True
    )

    return scored


def allocate_projects():

    slots = get_free_time_slots()

    projects = get_sorted_projects()

    allocation = []

    project_index = 0

    for slot in slots:

        if project_index >= len(projects):
            break

        project = projects[project_index]

        allocation.append({

            "project": project["name"],

            "start": slot["start"],

            "end": slot["end"],

            "minutes": slot["duration"]

        })

        project_index += 1

    return allocation

def preview_schedule():

    allocation = allocate_projects()

    print("\nToday's AI Schedule\n")

    for item in allocation:

        print(
            f'{item["start"]} - {item["end"]}'
        )

        print(item["project"])

        print()

def calculate_project_score(project):

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


    today = date.today()


    deadline_date = datetime.strptime(
        deadline,
        "%Y-%m-%d"
    ).date()


    remaining_days = (
        deadline_date - today
    ).days


    if remaining_days <= 0:
        remaining_days = 1


    remaining_hours = max(
        0,
        estimated - worked
    )


    daily_hours = (
        remaining_hours /
        remaining_days
    )


    multiplier = {
        "High":1.5,
        "Medium":1.2,
        "Low":1.0
    }.get(priority,1)


    score = round(
        daily_hours * multiplier,
        2
    )


    return {

        "project_id":project_id,

        "name":name,

        "remaining_hours":remaining_hours,

        "remaining_minutes": int(remaining_hours * 60),

        "remaining_days":remaining_days,

        "daily_hours":round(
            daily_hours,
            2
        ),

        "priority":priority,

        "score":score

    }



def calculate_project_risk(project):

    pass



def generate_daily_schedule():

    slots = get_free_time_slots()

    projects = project_db.get_active_projects()

    if not projects:
        return []

    scored = []

    for project in projects:

        scored.append(
            calculate_project_score(project)
        )

    scored.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    generated = []

    for project in scored:

        remaining = project["remaining_minutes"]

        slot_index = 0

        while remaining > 0 and slot_index < len(slots):

            slot = slots[slot_index]

            available = slot["duration"]

            if available < 30:

                slot_index += 1
                continue

            work = min(
                available,
                remaining,
                MAX_FOCUS_SESSION
            )

            start_minutes = time_to_minutes(
                slot["start"]
            )

            end_minutes = start_minutes + work

            generated.append({

                "project_id": project["project_id"],

                "title": f"Work on {project['name']}",

                "start": minutes_to_time(start_minutes),

                "end": minutes_to_time(end_minutes),

                "minutes": work

            })

            remaining -= work

            available -= work

            if available <= 0:

                slots.pop(slot_index)

            else:

                slot["start"] = minutes_to_time(end_minutes)

                slot["duration"] = available

                slot_index += 1

    return generated


def find_available_slots():

    return get_free_time_slots()



def reschedule_task(task):

    pass
