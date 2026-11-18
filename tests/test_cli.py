import json

import pytest

import main


def run_cli(capsys, monkeypatch, args):
    """Run a CLI command and capture its output."""

    monkeypatch.setattr("sys.argv", ["main.py", *args])
    main.main()

    return capsys.readouterr()


def test_add_task_cli(capsys, monkeypatch, tmp_path):
    """Test adding a task through the CLI."""

    import task_manager

    storage = tmp_path / "tasks.json"
    monkeypatch.setattr(task_manager, "TASKS_FILE", storage)

    result = run_cli(
        capsys,
        monkeypatch,
        ["add", "Study Python", "--priority", "high"],
    )

    assert "Task added successfully!" in result.out

    tasks = json.loads(storage.read_text(encoding="utf-8"))

    assert len(tasks) == 1
    assert tasks[0]["description"] == "Study Python"
    assert tasks[0]["priority"] == "high"


def test_list_tasks_cli(capsys, monkeypatch, tmp_path):
    """Test listing tasks through the CLI."""

    import task_manager

    storage = tmp_path / "tasks.json"
    monkeypatch.setattr(task_manager, "TASKS_FILE", storage)

    task_manager.add_task("Complete Python project")

    result = run_cli(capsys, monkeypatch, ["list"])

    assert "Complete Python project" in result.out
    assert "Total tasks displayed: 1" in result.out


def test_complete_task_cli(capsys, monkeypatch, tmp_path):
    """Test completing a task through the CLI."""

    import task_manager

    storage = tmp_path / "tasks.json"
    monkeypatch.setattr(task_manager, "TASKS_FILE", storage)

    task = task_manager.add_task("Finish testing")

    result = run_cli(
        capsys,
        monkeypatch,
        ["complete", str(task["id"])],
    )

    assert "marked as completed" in result.out

    saved_tasks = task_manager.list_tasks()

    assert saved_tasks[0]["completed"] is True


def test_delete_task_cli(capsys, monkeypatch, tmp_path):
    """Test deleting a task through the CLI."""

    import task_manager

    storage = tmp_path / "tasks.json"
    monkeypatch.setattr(task_manager, "TASKS_FILE", storage)

    task = task_manager.add_task("Delete this task")

    result = run_cli(
        capsys,
        monkeypatch,
        ["delete", str(task["id"])],
    )

    assert "deleted" in result.out
    assert task_manager.list_tasks() == []


def test_edit_task_cli(capsys, monkeypatch, tmp_path):
    """Test editing a task through the CLI."""

    import task_manager

    storage = tmp_path / "tasks.json"
    monkeypatch.setattr(task_manager, "TASKS_FILE", storage)

    task = task_manager.add_task("Old description")

    result = run_cli(
        capsys,
        monkeypatch,
        [
            "edit",
            str(task["id"]),
            "--description",
            "Updated description",
        ],
    )

    assert "updated successfully" in result.out

    saved_tasks = task_manager.list_tasks()

    assert saved_tasks[0]["description"] == "Updated description"


def test_list_pending_tasks_cli(capsys, monkeypatch, tmp_path):
    """Test filtering pending tasks through the CLI."""

    import task_manager

    storage = tmp_path / "tasks.json"
    monkeypatch.setattr(task_manager, "TASKS_FILE", storage)

    task_manager.add_task("Pending task")
    completed = task_manager.add_task("Completed task")
    task_manager.complete_task(completed["id"])

    result = run_cli(
        capsys,
        monkeypatch,
        ["list", "pending"],
    )

    assert "Pending task" in result.out
    assert "Completed task" not in result.out


def test_invalid_task_id_cli(capsys, monkeypatch):
    """Test that invalid task IDs are rejected."""

    with pytest.raises(SystemExit) as error:
        run_cli(capsys, monkeypatch, ["complete", "abc"])

    assert error.value.code == 2


def test_invalid_due_date_cli(capsys, monkeypatch, tmp_path):
    """Test that invalid due dates are rejected."""

    import task_manager

    storage = tmp_path / "tasks.json"
    monkeypatch.setattr(task_manager, "TASKS_FILE", storage)

    result = run_cli(
        capsys,
        monkeypatch,
        ["add", "Test task", "--due", "2026-13-40"],
    )

    assert "Due date must use YYYY-MM-DD format" in result.out
    assert task_manager.list_tasks() == []


def test_overdue_filter_excludes_completed_tasks(
    capsys,
    monkeypatch,
    tmp_path,
):
    """Test that completed tasks are excluded from overdue results."""

    import task_manager

    storage = tmp_path / "tasks.json"
    monkeypatch.setattr(task_manager, "TASKS_FILE", storage)

    overdue_task = task_manager.add_task(
        "Overdue pending task",
        due_date="2020-01-01",
    )

    completed_task = task_manager.add_task(
        "Completed overdue task",
        due_date="2020-01-01",
    )

    task_manager.complete_task(completed_task["id"])

    result = run_cli(capsys, monkeypatch, ["list", "overdue"])

    assert overdue_task["description"] in result.out
    assert completed_task["description"] not in result.out


def test_clear_due_date_cli(capsys, monkeypatch, tmp_path):
    """Test clearing a due date through the CLI."""

    import task_manager

    storage = tmp_path / "tasks.json"
    monkeypatch.setattr(task_manager, "TASKS_FILE", storage)

    task = task_manager.add_task(
        "Clear this due date",
        due_date="2026-12-01",
    )

    result = run_cli(
        capsys,
        monkeypatch,
        ["edit", str(task["id"]), "--clear-due"],
    )

    assert "updated successfully" in result.out
    assert task_manager.list_tasks()[0]["due_date"] is None


def test_edit_without_fields_cli(capsys, monkeypatch, tmp_path):
    """Test editing without providing update fields."""

    import task_manager

    storage = tmp_path / "tasks.json"
    monkeypatch.setattr(task_manager, "TASKS_FILE", storage)

    task = task_manager.add_task("Original task")

    result = run_cli(
        capsys,
        monkeypatch,
        ["edit", str(task["id"])],
    )

    assert "Provide at least one field to update" in result.out
