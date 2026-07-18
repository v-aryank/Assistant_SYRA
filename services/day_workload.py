from services.free_time_analyzer import get_free_time_slots


def get_today_free_minutes():

    slots = get_free_time_slots()

    total = 0

    for slot in slots:
        total += slot["duration"]

    return total


def get_today_busy_minutes():

    return 1440 - get_today_free_minutes()


def get_today_workload():

    free = get_today_free_minutes()

    busy = get_today_busy_minutes()

    percent = round((busy / 1440) * 100)

    return {

        "free": free,

        "busy": busy,

        "busy_percent": percent

    }