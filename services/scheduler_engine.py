from datetime import date, datetime, timedelta


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

    pass



def find_available_slots(tasks):

    pass



def reschedule_task(task):

    pass
