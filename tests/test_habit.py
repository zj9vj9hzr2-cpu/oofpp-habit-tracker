import unittest

from habit import Habit


class TestHabit(unittest.TestCase):

    def test_valid_habit(self):
        habit = Habit("Study Python", "daily")

        self.assertEqual(habit.task, "Study Python")
        self.assertEqual(habit.periodicity, "daily")

    def test_invalid_periodicity(self):
        with self.assertRaises(ValueError):
            Habit("Study Python", "monthly")

    def test_empty_task(self):
        with self.assertRaises(ValueError):
            Habit("", "daily")


if __name__ == "__main__":
    unittest.main()
