"""
Task Tracker CLI
Command-line interface for managing tasks.
"""

import argparse
from datetime import date

from task_manager import (add_task, complete_task, delete_task, list_tasks,
                          update_task)

# Terminal colors
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"


def positive_int(value):
    """Validate that an ID is a positive integer."""

    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Task ID must be a number.") from error

    if number <= 0:
        raise argparse.ArgumentTypeError("Task ID must be greater than zero.")

    return number


def build_parser():
    """Build the command-line argument parser."""

    parser = argparse.ArgumentParser(
        description="A command-line task tracker.",
        epilog=(
            "Example: python main.py add " '"Complete Python project" --priority high'
        ),
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # ADD
    add_parser = subparsers.add_parser(
        "add",
        help="Add a new task.",
    )
    add_parser.add_argument(
        "description",
        help="Description of the task.",
    )
    add_parser.add_argument(
        "--priority",
        choices=["low", "medium", "high"],
        default="medium",
        help="Task priority (default: medium).",
    )
    add_parser.add_argument(
        "--due",
        help="Due date in YYYY-MM-DD format.",
    )

    # LIST
    list_parser = subparsers.add_parser(
        "list",
        help="Display tasks.",
    )
    list_parser.add_argument(
        "filter",
        nargs="?",
        choices=[
            "all",
            "pending",
            "completed",
            "overdue",
            "low",
            "medium",
            "high",
        ],
        default="all",
        help="Optional task filter.",
    )

    # COMPLETE
    complete_parser = subparsers.add_parser(
        "complete",
        help="Mark a task as completed.",
    )
    complete_parser.add_argument(
        "task_id",
        type=positive_int,
        help="ID of the task.",
    )

    # DELETE
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a task.",
    )
    delete_parser.add_argument(
        "task_id",
        type=positive_int,
        help="ID of the task.",
    )

    # EDIT
    edit_parser = subparsers.add_parser(
        "edit",
        help="Update an existing task.",
    )
    edit_parser.add_argument(
        "task_id",
        type=positive_int,
        help="ID of the task.",
    )
    edit_parser.add_argument(
        "--description",
        help="New task description.",
    )
    edit_parser.add_argument(
        "--priority",
        choices=["low", "medium", "high"],
        help="New task priority.",
    )
    edit_parser.add_argument(
        "--due",
        help="New due date in YYYY-MM-DD format.",
    )
    edit_parser.add_argument(
        "--clear-due",
        action="store_true",
        help="Remove the existing due date.",
    )

    return parser


def display_task(task):
    """Display an individual task."""

    if task["completed"]:
        status = f"{GREEN}Completed{RESET}"
    else:
        status = f"{YELLOW}Pending{RESET}"

    priority = task.get("priority", "medium").capitalize()
    due_date = task.get("due_date") or "Not set"

    print(f"{BOLD}{task['id']}. {task['description']}{RESET}")
    print(f"   Status:   {status}")
    print(f"   Priority: {priority}")
    print(f"   Due date: {due_date}")
    print(f"   Created:  {task['created_at']}")

    if task.get("completed_at"):
        print(f"   Completed: {task['completed_at']}")

    print()


def filter_tasks(tasks, filter_type):
    """Filter tasks by status, priority, or due date."""

    if filter_type == "pending":
        return [task for task in tasks if not task["completed"]]

    if filter_type == "completed":
        return [task for task in tasks if task["completed"]]

    if filter_type == "overdue":
        today = date.today()

        return [
            task
            for task in tasks
            if not task["completed"]
            and task.get("due_date")
            and date.fromisoformat(task["due_date"]) < today
        ]

    if filter_type in {"low", "medium", "high"}:
        return [task for task in tasks if task.get("priority", "medium") == filter_type]

    return tasks


def handle_add(args):
    """Create a new task."""

    task = add_task(
        args.description,
        priority=args.priority,
        due_date=args.due,
    )

    print(f"{GREEN}Task added successfully!{RESET}")
    display_task(task)


def handle_list(args):
    """Display tasks, optionally filtered."""

    tasks = list_tasks()
    tasks = filter_tasks(tasks, args.filter)

    if not tasks:
        print(f"{YELLOW}No tasks found.{RESET}")
        return

    print(f"\n{BOLD}{CYAN}Your Tasks ({args.filter}):{RESET}\n")

    for task in tasks:
        display_task(task)

    print(f"{CYAN}Total tasks displayed: {len(tasks)}{RESET}")


def handle_complete(args):
    """Mark a task as completed."""

    task = complete_task(args.task_id)

    if task is None:
        print(f"{RED}Error: Task not found.{RESET}")
        return

    print(f"{GREEN}Task {args.task_id} marked as completed!{RESET}")


def handle_delete(args):
    """Delete a task."""

    success = delete_task(args.task_id)

    if success:
        print(f"{YELLOW}Task {args.task_id} deleted.{RESET}")
    else:
        print(f"{RED}Error: Task not found.{RESET}")


def handle_edit(args):
    """Update an existing task."""

    if (
        args.description is None
        and args.priority is None
        and args.due is None
        and not args.clear_due
    ):
        print(f"{RED}Error: Provide at least one field to update.{RESET}")
        return

    if args.clear_due and args.due is not None:
        print(f"{RED}Error: Use either --due or --clear-due, not both.{RESET}")
        return

    due_date = None if args.clear_due else args.due

    if not args.clear_due and args.due is None:
        from task_manager import UNSET

        due_date = UNSET

    task = update_task(
        args.task_id,
        description=args.description,
        priority=args.priority,
        due_date=due_date,
    )

    if task is None:
        print(f"{RED}Error: Task not found.{RESET}")
        return

    print(f"{GREEN}Task {args.task_id} updated successfully!{RESET}")
    display_task(task)


def main(argv=None):
    """Run the Task Tracker CLI."""

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "add":
            handle_add(args)

        elif args.command == "list":
            handle_list(args)

        elif args.command == "complete":
            handle_complete(args)

        elif args.command == "delete":
            handle_delete(args)

        elif args.command == "edit":
            handle_edit(args)

    except (ValueError, OSError) as error:
        print(f"{RED}Error: {error}{RESET}")


if __name__ == "__main__":
    main()
