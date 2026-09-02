from datetime import datetime


class Habit:
    """Represents one habit with a task, periodicity and creation date."""

    def __init__(self, task, periodicity, created_at=None, habit_id=None):
        if not isinstance(task, str) or not task.strip():
            raise ValueError("Task description cannot be empty.")

        if periodicity not in ("daily", "weekly"):
            raise ValueError("Periodicity must be 'daily' or 'weekly'.")

        self.id = habit_id
        self.task = task.strip()
        self.periodicity = periodicity
        self.created_at = created_at or datetime.now()

    def __str__(self):
        return f"{self.id}: {self.task} ({self.periodicity})"
