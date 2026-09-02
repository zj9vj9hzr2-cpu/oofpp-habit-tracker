from datetime import timedelta


def get_all_habits(habits):
    """Return all currently tracked habits."""
    return list(habits)


def filter_by_periodicity(habits, periodicity):
    """Return habits that have the requested periodicity."""
    return [
        habit
        for habit in habits
        if habit.periodicity == periodicity
    ]


def get_period_start(completion, periodicity):
    """Convert a completion timestamp into its daily or weekly period."""
    completion_date = completion.date()

    if periodicity == "daily":
        return completion_date

    if periodicity == "weekly":
        return completion_date - timedelta(days=completion_date.weekday())

    raise ValueError("Periodicity must be 'daily' or 'weekly'.")


def calculate_longest_streak(completions, periodicity):
    """Calculate the longest run of consecutive completed periods."""
    if not completions:
        return 0

    periods = set()

    for completion in completions:
        periods.add(get_period_start(completion, periodicity))

    periods = sorted(periods)

    if periodicity == "daily":
        step = timedelta(days=1)
    elif periodicity == "weekly":
        step = timedelta(days=7)
    else:
        raise ValueError("Periodicity must be 'daily' or 'weekly'.")

    longest_streak = 1
    current_streak = 1

    for index in range(1, len(periods)):
        difference = periods[index] - periods[index - 1]

        if difference == step:
            current_streak += 1

            if current_streak > longest_streak:
                longest_streak = current_streak
        else:
            current_streak = 1

    return longest_streak


def longest_streak_for_habit(habit, completions):
    """Return the longest streak for one selected habit."""
    return calculate_longest_streak(
        completions,
        habit.periodicity
    )


def longest_streak_all(habits, completions_by_habit):
    """Return the habit with the longest streak and the streak length."""
    longest_habit = None
    longest_streak = 0

    for habit in habits:
        completions = completions_by_habit.get(habit.id, [])
        streak = longest_streak_for_habit(habit, completions)

        if streak > longest_streak:
            longest_streak = streak
            longest_habit = habit

    return longest_habit, longest_streak
