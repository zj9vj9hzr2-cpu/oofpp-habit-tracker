import unittest
from datetime import datetime

from habit import Habit
from analytics import (
    calculate_longest_streak,
    filter_by_periodicity,
    longest_streak_all
)


class TestAnalytics(unittest.TestCase):

    def test_filter_by_periodicity(self):
        habits = [
            Habit("Study", "daily"),
            Habit("Notes", "daily"),
            Habit("Cycling", "weekly")
        ]

        result = filter_by_periodicity(habits, "daily")

        self.assertEqual(len(result), 2)

    def test_daily_streak(self):
        completions = [
            datetime(2026, 8, 20, 10, 0),
            datetime(2026, 8, 21, 11, 0),
            datetime(2026, 8, 21, 18, 0),
            datetime(2026, 8, 22, 9, 0),
            datetime(2026, 8, 24, 10, 0)
        ]

        result = calculate_longest_streak(
            completions,
            "daily"
        )

        self.assertEqual(result, 3)

    def test_weekly_streak(self):
        completions = [
            datetime(2026, 8, 3, 10, 0),
            datetime(2026, 8, 5, 18, 0),
            datetime(2026, 8, 10, 9, 0),
            datetime(2026, 8, 17, 12, 0),
            datetime(2026, 8, 31, 11, 0)
        ]

        result = calculate_longest_streak(
            completions,
            "weekly"
        )

        self.assertEqual(result, 3)

    def test_longest_streak_all(self):
        daily = Habit("Study", "daily", habit_id=1)
        weekly = Habit("Cycling", "weekly", habit_id=2)

        completions = {
            1: [
                datetime(2026, 8, 1),
                datetime(2026, 8, 2),
                datetime(2026, 8, 3)
            ],
            2: [
                datetime(2026, 8, 3),
                datetime(2026, 8, 10)
            ]
        }

        habit, streak = longest_streak_all(
            [daily, weekly],
            completions
        )

        self.assertEqual(habit.id, 1)
        self.assertEqual(streak, 3)


if __name__ == "__main__":
    unittest.main()
