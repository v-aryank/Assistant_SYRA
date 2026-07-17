from datetime import datetime

from services.routine_analyzer import build_today_blocks


DAY_START = "00:00"
DAY_END = "23:59"


def to_minutes(time_string):
    hour, minute = map(int, time_string.split(":"))
    return hour * 60 + minute


def to_time(minutes):
    hour = minutes // 60
    minute = minutes % 60
    return f"{hour:02d}:{minute:02d}"


def get_free_time_slots():

    busy_blocks = build_today_blocks()

    if not busy_blocks:

        return [{
            "start": DAY_START,
            "end": DAY_END,
            "duration": 1439
        }]

    free_blocks = []

    current = to_minutes(DAY_START)

    for block in busy_blocks:

        start = to_minutes(block["start"])
        end = to_minutes(block["end"])

        if start > current:

            free_blocks.append({

                "start": to_time(current),

                "end": to_time(start),

                "duration": start-current

            })

        current = end

    day_end = to_minutes(DAY_END)

    if current < day_end:

        free_blocks.append({

            "start": to_time(current),

            "end": DAY_END,

            "duration": day_end-current

        })

    return free_blocks