import pytest

import task_manager


@pytest.fixture
def temporary_storage(tmp_path, monkeypatch):
    """Use isolated JSON storage for every test."""

    test_file = tmp_path / "test_tasks.json"
    monkeypatch.setattr(task_manager, "TASKS_FILE", test_file)

    return test_file


def test_add_task(temporary_storage):
    task = task_manager.add_task("Complete Python project")

    assert task["id"] == 1
    assert task["description"] == "Complete Python project"
    assert task["completed"] is False
    assert task["priority"] == "medium"


def test_add_task_with_priority(temporary_storage):
    task = task_manager.add_task(
        "Study Python",
        priority="high",
    )

    assert task["priority"] == "high"


def test_add_task_with_due_date(temporary_storage):
    task = task_manager.add_task(
        "Submit assignment",
        due_date="2026-12-01",
    )

    assert task["due_date"] == "2026-12-01"


def test_reject_empty_description(temporary_storage):
    with pytest.raises(ValueError):
        task_manager.add_task("   ")


def test_reject_invalid_priority(temporary_storage):
    with pytest.raises(ValueError):
        task_manager.add_task(
            "Test task",
            priority="urgent",
        )


def test_reject_invalid_due_date(temporary_storage):
    with pytest.raises(ValueError):
        task_manager.add_task(
            "Test task",
            due_date="December 1",
        )


def test_incremental_task_ids(temporary_storage):
    first = task_manager.add_task("First task")
    second = task_manager.add_task("Second task")

    assert first["id"] == 1
    assert second["id"] == 2


def test_list_tasks(temporary_storage):
    task_manager.add_task("First task")
    task_manager.add_task("Second task")

    tasks = task_manager.list_tasks()

    assert len(tasks) == 2


def test_complete_task(temporary_storage):
    task = task_manager.add_task("Finish testing")

    completed = task_manager.complete_task(task["id"])

    assert completed["completed"] is True
    assert completed["completed_at"] is not None


def test_complete_task_preserves_timestamp(temporary_storage):
    task = task_manager.add_task("Finish testing")

    first = task_manager.complete_task(task["id"])
    original_timestamp = first["completed_at"]

    second = task_manager.complete_task(task["id"])

    assert second["completed_at"] == original_timestamp


def test_update_task(temporary_storage):
    task = task_manager.add_task("Old description")

    updated = task_manager.update_task(
        task["id"],
        description="New description",
        priority="high",
    )

    assert updated["description"] == "New description"
    assert updated["priority"] == "high"


def test_delete_task(temporary_storage):
    task = task_manager.add_task("Delete me")

    result = task_manager.delete_task(task["id"])

    assert result is True
    assert task_manager.list_tasks() == []


def test_delete_missing_task(temporary_storage):
    assert task_manager.delete_task(999) is False


def test_corrupted_storage_raises_error(temporary_storage):
    temporary_storage.write_text("{invalid json")

    with pytest.raises(ValueError):
        task_manager.load_tasks()


def test_clear_task_due_date(temporary_storage):
    task = task_manager.add_task(
        "Complete assignment",
        due_date="2026-12-01",
    )

    updated = task_manager.update_task(
        task["id"],
        due_date=None,
    )

    assert updated["due_date"] is None


def test_update_task_preserves_due_date_when_not_provided(
    temporary_storage,
):
    task = task_manager.add_task(
        "Complete assignment",
        due_date="2026-12-01",
    )

    updated = task_manager.update_task(
        task["id"],
        priority="high",
    )

    assert updated["due_date"] == "2026-12-01"


def test_update_task_changes_due_date(temporary_storage):
    task = task_manager.add_task(
        "Complete assignment",
        due_date="2026-12-01",
    )

    updated = task_manager.update_task(
        task["id"],
        due_date="2026-12-15",
    )

    assert updated["due_date"] == "2026-12-15"
