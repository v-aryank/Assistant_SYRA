import database.routine_db as routine_db


def build_today_blocks():

    routines = routine_db.get_today_routines()

    if not routines:
        return []

    blocks = []

    current = None

    for routine in routines:

        (
            routine_id,
            title,
            category,
            visible,
            start,
            end
        ) = routine

        if current is None:

            current = {
                "category": category,
                "start": start,
                "end": end,
                "tasks": [title]
            }

            continue

        if (
            category == current["category"]
            and start == current["end"]
        ):

            current["end"] = end
            current["tasks"].append(title)

        else:

            blocks.append(current)

            current = {
                "category": category,
                "start": start,
                "end": end,
                "tasks": [title]
            }

    if current:

        blocks.append(current)

    return blocks