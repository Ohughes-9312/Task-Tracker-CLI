"""
Task Manager
Handles task creation, storage, updates, completion, and deletion.
"""

import json
from datetime import date, datetime
from pathlib import Path

# Store task data alongside this Python file.
TASKS_FILE = Path(__file__).with_name("tasks.json")

VALID_PRIORITIES = {"low", "medium", "high"}
UNSET = object()


def load_tasks():
    """Load tasks from JSON storage."""

    if not TASKS_FILE.exists():
        return []

    try:
        with TASKS_FILE.open("r", encoding="utf-8") as file:
            tasks = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            "Task storage contains invalid JSON. "
            "Restore your backup before continuing."
        ) from error

    if not isinstance(tasks, list):
        raise ValueError("Task storage must contain a JSON list.")

    return tasks


def save_tasks(tasks):
    """Save tasks safely using an atomic file replacement."""

    temporary_file = TASKS_FILE.with_suffix(".tmp")

    try:
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)

        temporary_file.replace(TASKS_FILE)

    except OSError:
        if temporary_file.exists():
            temporary_file.unlink()
        raise


def get_next_id(tasks):
    """Generate the next incremental task ID."""

    if not tasks:
        return 1

    return max(task["id"] for task in tasks) + 1


def validate_description(description):
    """Validate task descriptions."""

    if not isinstance(description, str) or not description.strip():
        raise ValueError("Task description cannot be empty.")

    return description.strip()


def validate_priority(priority):
    """Validate task priority."""

    priority = priority.lower().strip()

    if priority not in VALID_PRIORITIES:
        raise ValueError("Priority must be low, medium, or high.")

    return priority


def validate_due_date(due_date):
    """Validate optional due dates in YYYY-MM-DD format."""

    if due_date is None:
        return None

    try:
        return date.fromisoformat(due_date).isoformat()
    except (ValueError, TypeError) as error:
        raise ValueError("Due date must use YYYY-MM-DD format.") from error


def add_task(description, priority="medium", due_date=None):
    """Create and save a new task."""

    description = validate_description(description)
    priority = validate_priority(priority)
    due_date = validate_due_date(due_date)

    tasks = load_tasks()

    new_task = {
        "id": get_next_id(tasks),
        "description": description,
        "completed": False,
        "priority": priority,
        "due_date": due_date,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "completed_at": None,
    }

    tasks.append(new_task)
    save_tasks(tasks)

    return new_task


def list_tasks():
    """Return all saved tasks."""

    return load_tasks()


def get_task(task_id):
    """Find a task by ID."""

    return next(
        (task for task in load_tasks() if task["id"] == task_id),
        None,
    )


def update_task(task_id, description=None, priority=None, due_date=UNSET):
    """Update an existing task."""

    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:

            if description is not None:
                task["description"] = validate_description(description)

            if priority is not None:
                task["priority"] = validate_priority(priority)

            if due_date is not UNSET:
                task["due_date"] = validate_due_date(due_date)

            save_tasks(tasks)
            return task

    return None


def complete_task(task_id):
    """Mark a task as completed."""

    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:

            if not task["completed"]:
                task["completed"] = True
                task["completed_at"] = datetime.now().isoformat(timespec="seconds")
                save_tasks(tasks)

            return task

    return None


def delete_task(task_id):
    """Delete a task by ID."""

    tasks = load_tasks()

    updated_tasks = [task for task in tasks if task["id"] != task_id]

    if len(updated_tasks) == len(tasks):
        return False

    save_tasks(updated_tasks)
    return True
