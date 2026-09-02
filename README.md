# Study and Routine Habit Tracker

A small local command-line habit tracker written in Python.

The application allows one user to create daily or weekly habits, check them off,
store completion events and analyse habit streaks.

## Requirements

- Python 3.7 or newer
- No external Python packages are required
- SQLite is included in Python through the built-in `sqlite3` module

## Download

Download or clone this repository and open the project folder in a terminal.

No additional installation is required.

## Run the application

Run:

```bash
python3 main.py
```

On the first run, the application automatically creates a local SQLite database
named `habit_tracker.db`.

If the database is empty, five predefined habits and four weeks of example
completion data are inserted automatically.

## Available functions

The command-line interface allows the user to:

- view all habits
- create a daily or weekly habit
- check off a habit
- delete a habit
- filter habits by periodicity
- show the longest streak across all habits
- show the longest streak for a selected habit

The application is controlled through the numbered menu displayed in the terminal.

## Project structure

- `habit.py` - Habit class and validation
- `database.py` - SQLite storage and database operations
- `analytics.py` - functional analytics and streak calculations
- `seed_data.py` - predefined habits and four weeks of example data
- `main.py` - command-line interface and application flow
- `tests/` - automated unit tests

## Run the tests

From the project folder, run:

```bash
python3 -m unittest discover tests
```

The test suite covers habit validation, database operations and daily and weekly
streak calculations.

## Data storage

The project uses SQLite for persistent local storage.

Habits and completion events are stored in separate tables. Each completion
record is linked to one habit through its habit ID.

The database is stored locally as `habit_tracker.db`.

## Reset the application

To start again with a fresh database, close the application and delete:

```text
habit_tracker.db
```

The next time `main.py` is started, the database will be created again and the
five predefined habits with their example data will be inserted automatically.

## User interface

The project uses a simple command-line interface because the focus of the
assignment is the Python backend and its object-oriented and functional
programming components.

Because user interaction, storage and analytics are separated into different
modules, another interface such as a graphical or web-based frontend could be
added later without rewriting the core logic.