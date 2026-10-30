from datetime import date, datetime

from services.free_time_analyzer import get_free_time_slots

import database.project_db as project_db
import database.task_db as task_db

from database.project_db import get_all_projects
from services.day_workload import get_today_workload

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
