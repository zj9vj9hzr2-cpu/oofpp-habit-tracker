from datetime import datetime, timedelta

from habit import Habit
from database import (
    DATABASE_NAME,
    add_completion,
    add_habit,
    habit_count
)


def seed_predefined_data(db_name=DATABASE_NAME):
    """Insert five predefined habits and four weeks of example data."""
    if habit_count(db_name) > 0:
        return False

    start = datetime(2026, 7, 6, 9, 0)

    habits = [
        Habit("Study Python for 30 minutes", "daily", start),
        Habit("Review university notes", "daily", start),
        Habit("Complete one cycling training session", "weekly", start),
        Habit("Plan the upcoming study week", "weekly", start),
        Habit("Review household and family tasks", "weekly", start)
    ]

    for habit in habits:
        add_habit(habit, db_name)

    study_days = [
        0, 1, 2, 3, 4,
        6, 7, 8, 9, 10,
        13, 14, 15, 16, 17, 18, 19, 20,
        22, 23, 24, 25, 26, 27
    ]

    review_days = [
        0, 2, 3, 4,
        7, 8, 10, 11,
        14, 15, 16, 18,
        21, 22, 24, 25, 27
    ]

    for day in study_days:
        add_completion(
            habits[0].id,
            start + timedelta(days=day, hours=9),
            db_name
        )

    for day in review_days:
        add_completion(
            habits[1].id,
            start + timedelta(days=day, hours=10),
            db_name
        )

    cycling_days = [1, 3, 8, 15, 22, 24]
    planning_days = [0, 7, 21]
    household_days = [3, 10, 17, 24]

    for day in cycling_days:
        add_completion(
            habits[2].id,
            start + timedelta(days=day, hours=8),
            db_name
        )

    for day in planning_days:
        add_completion(
            habits[3].id,
            start + timedelta(days=day, hours=11),
            db_name
        )

    for day in household_days:
        add_completion(
            habits[4].id,
            start + timedelta(days=day, hours=12),
            db_name
        )

    return True
