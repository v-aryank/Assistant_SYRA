from services.scheduler_engine import get_sorted_projects
from services.free_time_analyzer import get_free_time_slots


def recommend_next_project():

    projects = get_sorted_projects()

    slots = get_free_time_slots()

    if not projects:
        return None

    if not slots:
        return None

    project = projects[0]
    slot = slots[0]

    return {

        "project_id": project["project_id"],

        "project_name": project["name"],

        "priority": project["priority"],

        "required_minutes": project["remaining_minutes"],

        "slot_start": slot["start"],

        "slot_end": slot["end"],

        "slot_duration": slot["duration"]

    }