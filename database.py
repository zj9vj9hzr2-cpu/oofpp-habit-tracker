import sqlite3
from datetime import datetime

from habit import Habit


DATABASE_NAME = "habit_tracker.db"


def get_connection(db_name=DATABASE_NAME):
    """Open a SQLite connection and enable foreign-key support."""
    connection = sqlite3.connect(db_name)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(db_name=DATABASE_NAME):
    """Create the required database tables if they do not yet exist."""
    connection = get_connection(db_name)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            periodicity TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completed_at TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
        )
    """)

    connection.commit()
    connection.close()


def add_habit(habit, db_name=DATABASE_NAME):
    """Store a Habit object and return its database ID."""
    connection = get_connection(db_name)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO habits (task, periodicity, created_at)
        VALUES (?, ?, ?)
    """, (
        habit.task,
        habit.periodicity,
        habit.created_at.isoformat()
    ))

    habit.id = cursor.lastrowid

    connection.commit()
    connection.close()

    return habit.id


def load_all_habits(db_name=DATABASE_NAME):
    """Load all stored habits as Habit objects."""
    connection = get_connection(db_name)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, task, periodicity, created_at
        FROM habits
        ORDER BY id
    """)

    rows = cursor.fetchall()
    connection.close()

    habits = []

    for row in rows:
        habit = Habit(
            task=row[1],
            periodicity=row[2],
            created_at=datetime.fromisoformat(row[3]),
            habit_id=row[0]
        )
        habits.append(habit)

    return habits


def load_habit(habit_id, db_name=DATABASE_NAME):
    """Load one habit by its ID. Return None if it does not exist."""
    connection = get_connection(db_name)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, task, periodicity, created_at
        FROM habits
        WHERE id = ?
    """, (habit_id,))

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return None

    return Habit(
        task=row[1],
        periodicity=row[2],
        created_at=datetime.fromisoformat(row[3]),
        habit_id=row[0]
    )


def delete_habit(habit_id, db_name=DATABASE_NAME):
    """Delete a habit and its completion records."""
    connection = get_connection(db_name)
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM habits
        WHERE id = ?
    """, (habit_id,))

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted


def add_completion(habit_id, completed_at=None, db_name=DATABASE_NAME):
    """Store one completion timestamp for a habit."""
    completed_at = completed_at or datetime.now()

    connection = get_connection(db_name)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO completions (habit_id, completed_at)
        VALUES (?, ?)
    """, (
        habit_id,
        completed_at.isoformat()
    ))

    completion_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return completion_id


def load_completions(habit_id, db_name=DATABASE_NAME):
    """Load all completion timestamps for one habit."""
    connection = get_connection(db_name)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT completed_at
        FROM completions
        WHERE habit_id = ?
        ORDER BY completed_at
    """, (habit_id,))

    rows = cursor.fetchall()
    connection.close()

    completions = []

    for row in rows:
        completions.append(datetime.fromisoformat(row[0]))

    return completions


def habit_count(db_name=DATABASE_NAME):
    """Return the number of stored habits."""
    connection = get_connection(db_name)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM habits")
    count = cursor.fetchone()[0]

    connection.close()
    return count
