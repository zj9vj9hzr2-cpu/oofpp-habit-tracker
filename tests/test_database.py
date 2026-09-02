import os
import tempfile
import unittest
from datetime import datetime

from habit import Habit
from database import (
    add_completion,
    add_habit,
    delete_habit,
    initialize_database,
    load_completions,
    load_habit
)


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.db_name = os.path.join(
            self.temp_directory.name,
            "test_habits.db"
        )
        initialize_database(self.db_name)

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_add_and_load_habit(self):
        habit = Habit("Study Python", "daily")
        add_habit(habit, self.db_name)

        loaded = load_habit(habit.id, self.db_name)

        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.task, "Study Python")
        self.assertEqual(loaded.periodicity, "daily")

    def test_add_and_load_completion(self):
        habit = Habit("Cycling", "weekly")
        add_habit(habit, self.db_name)

        completed_at = datetime(2026, 8, 20, 10, 0)
        add_completion(habit.id, completed_at, self.db_name)

        completions = load_completions(habit.id, self.db_name)

        self.assertEqual(len(completions), 1)
        self.assertEqual(completions[0], completed_at)

    def test_delete_habit(self):
        habit = Habit("Study Python", "daily")
        add_habit(habit, self.db_name)
        add_completion(habit.id, db_name=self.db_name)

        deleted = delete_habit(habit.id, self.db_name)

        self.assertTrue(deleted)
        self.assertIsNone(load_habit(habit.id, self.db_name))
        self.assertEqual(load_completions(habit.id, self.db_name), [])


if __name__ == "__main__":
    unittest.main()
