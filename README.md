
# Task Tracker CLI

A Python command-line task management application that supports task creation, editing, completion, deletion, priorities, and due-date tracking.

Tasks are stored locally in JSON, making the application lightweight and easy to run without a database.

## Features

- Create tasks with descriptions and optional priorities.
- Assign due dates using `YYYY-MM-DD` format.
- View all tasks or filter by status, priority, and overdue status.
- Edit task descriptions, priorities, and due dates.
- Clear existing due dates.
- Mark tasks as completed.
- Record creation and completion timestamps.
- Delete tasks by ID.
- Automatically assign incremental task IDs.
- Validate user input and handle invalid commands.
- Persist task data locally in JSON.
- Run automated tests with pytest.

## Technology Stack

- Python 3.12+
- JSON for local data persistence
- argparse for command-line argument handling
- pytest for automated testing
- Black for code formatting
- isort for import organization
- Flake8 for linting

## Project Structure

```text
Task-Tracker-CLI/
│
├── main.py
├── task_manager.py
├── requirements.txt
├── .gitignore
├── .flake8
├── README.md
│
└── tests/
    ├── test_cli.py
    └── test_task_manager.py
```

The application creates `tasks.json` locally when task data is saved. This file is excluded from version control so personal task records are not published.

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Task-Tracker-CLI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS / WSL:

```bash
source .venv/bin/activate
```

### 4. Install development dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run commands from the project directory.

### Add a task

```bash
python main.py add "Study Python"
```

Add a task with priority and due date:

```bash
python main.py add "Complete project" --priority high --due 2026-12-01
```

### List tasks

```bash
python main.py list
```

Filter by status:

```bash
python main.py list pending
python main.py list completed
```

Filter overdue tasks:

```bash
python main.py list overdue
```

Filter by priority:

```bash
python main.py list high
python main.py list medium
python main.py list low
```

### Complete a task

```bash
python main.py complete 1
```

### Edit a task

Change its description:

```bash
python main.py edit 1 --description "Study Python fundamentals"
```

Change its priority:

```bash
python main.py edit 1 --priority high
```

Change its due date:

```bash
python main.py edit 1 --due 2026-12-15
```

Remove its due date:

```bash
python main.py edit 1 --clear-due
```

### Delete a task

```bash
python main.py delete 1
```

## Task Data

Each task is stored as a JSON object with fields for:

- `id`: Unique task identifier.
- `description`: Task description.
- `completed`: Completion status.
- `priority`: Task priority.
- `due_date`: Optional due date.
- `created_at`: Task creation timestamp.
- `completed_at`: Completion timestamp, when applicable.

The JSON file is stored locally and is not included in the public repository.

## Testing

The project includes automated tests for task management and command-line functionality.

Run the complete test suite:

```bash
python -m pytest -v
```

The tests cover:

- Task creation and deletion.
- Task editing and due-date updates.
- Priority and date validation.
- Completion timestamps.
- Task filtering.
- Invalid CLI arguments.
- Overdue task behavior.
- JSON storage error handling.

## Code Quality

Format the project:

```bash
black .
```

Organize imports:

```bash
isort .
```

Run lint checks:

```bash
python -m flake8 .
```


## Project Screenshots

The following screenshots demonstrate the Task Tracker CLI's main features and automated testing.

### Task Management

**Task List**

![Task List](screenshots/task%20list.png)

**Adding a Task**

![Adding a Task](screenshots/add%20task.png)

**Editing a Task**

![Editing a Task](screenshots/edit%20task.png)

**Completing a Task**

![Completing a Task](screenshots/complete%20task.png)

### Task Filtering

**Overdue Tasks**

![Overdue Tasks](screenshots/overdue%20task.png)

**High-Priority Tasks**

![High Priority Tasks](screenshots/high%20priority%20tasks.png)

### Automated Testing

**Test Results**

![Test Results](screenshots/test%20results.png)

## Development Notes

This project uses Python's standard library for its application functionality. External packages are used for testing and development quality checks.

Task data is stored locally in JSON, and automated tests use temporary storage to avoid modifying personal task records.

## License

MIT License
