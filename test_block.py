from services.scheduler_engine import generate_daily_schedule

schedule = generate_daily_schedule()

print("\n========== TODAY'S AI SCHEDULE ==========\n")

for task in schedule:

    print(
        f'{task["start"]} -> {task["end"]}'
    )

    print(task["title"])

    print(
        f'Duration : {task["minutes"]} minutes'
    )

    print("--------------------------------------")