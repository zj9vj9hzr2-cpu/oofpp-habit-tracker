from habit import Habit
from database import (
    add_completion,
    add_habit,
    delete_habit,
    initialize_database,
    load_all_habits,
    load_completions,
    load_habit
)
from analytics import (
    filter_by_periodicity,
    get_all_habits,
    longest_streak_all,
    longest_streak_for_habit
)
from seed_data import seed_predefined_data


def print_habits(habits):
    """Display habits in a simple readable format."""
    if not habits:
        print("No habits found.")
        return

    for habit in habits:
        print(
            f"{habit.id}: {habit.task} "
            f"({habit.periodicity})"
        )


def view_habits():
    """Load and display all currently tracked habits."""
    habits = get_all_habits(load_all_habits())
    print_habits(habits)
    

def create_habit():
    """Create and store a new daily or weekly habit from user input."""
    task = input("Task description: ").strip()
    periodicity = input(  
        "Periodicity (daily/weekly): "
    ).strip().lower()
    try:
        habit = Habit(task, periodicity)
        add_habit(habit)
        print(f"Habit created with ID {habit.id}.")
    except ValueError as error:
        print("Error:", error)


def check_off_habit():
    """Record a completion timestamp for a selected habit."""
    try:
        habit_id = int(input("Habit ID: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    habit = load_habit(habit_id)

    if habit is None:
        print("Habit not found.")
        return

    add_completion(habit.id)
    print(f"Checked off: {habit.task}")


def remove_habit():
    """Remove a habit from the database."""
    try:
        habit_id = int(input("Habit ID to delete: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    if delete_habit(habit_id):
        print("Habit deleted.")
    else:
        print("Habit not found.")


def view_by_periodicity():
    """Display habits filtered by daily or weekly periodicity."""
    periodicity = input(
        "Periodicity (daily/weekly): "
    ).strip().lower()

    if periodicity not in ("daily", "weekly"):
        print("Periodicity must be 'daily' or 'weekly'.")
        return

    habits = load_all_habits()
    filtered = filter_by_periodicity(habits, periodicity)
    print_habits(filtered)


def view_longest_streak():
    """Display the longest streak across all stored habits."""
    habits = load_all_habits()
    completions_by_habit = {}

    for habit in habits:
        completions_by_habit[habit.id] = load_completions(habit.id)

    habit, streak = longest_streak_all(
        habits,
        completions_by_habit
    )

    if habit is None:
        print("No completed habits found.")
        return

    print(
        f"Longest streak: {habit.task} "
        f"with {streak} consecutive period(s)."
    )


def view_habit_streak():
    """Display the longest streak for one selected habit."""
    try:
        habit_id = int(input("Habit ID: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    habit = load_habit(habit_id)

    if habit is None:
        print("Habit not found.")
        return

    completions = load_completions(habit.id)
    streak = longest_streak_for_habit(habit, completions)

    print(
        f"Longest streak for '{habit.task}': "
        f"{streak} consecutive period(s)."
    )


def main():
    """Initialize the application and run the command-line menu."""
    initialize_database()
    seed_predefined_data()

    while True:
        print("""
Habit Tracker

1 - View all habits
2 - Create habit
3 - Check off habit
4 - Delete habit
5 - Filter habits by periodicity
6 - Show longest streak overall
7 - Show longest streak for one habit
0 - Exit
""")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_habits()
        elif choice == "2":
            create_habit()
        elif choice == "3":
            check_off_habit()
        elif choice == "4":
            remove_habit()
        elif choice == "5":
            view_by_periodicity()
        elif choice == "6":
            view_longest_streak()
        elif choice == "7":
            view_habit_streak()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Unknown option. Please try again.")


if __name__ == "__main__":
    main()
