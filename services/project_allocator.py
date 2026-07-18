from services.scheduler_engine import get_sorted_projects


def calculate_daily_targets():

    projects = get_sorted_projects()

    targets = []

    for project in projects:

        minutes = int(
            project["daily_hours"] * 60
        )

        targets.append({

            "project_id": project["project_id"],

            "name": project["name"],

            "required_today": minutes,

            "remaining": minutes

        })

    return targets