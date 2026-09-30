import sqlite3

from .sqlite_repository import DEFAULT_DATABASE_PATH, SQLiteTaskRepository
from .task_manager import TaskManager


def display_tasks(manager: TaskManager) -> None:
    tasks = manager.get_tasks()
    if not tasks:
        print("\nNo tasks yet.")
        return

    print("\nYour tasks:")
    for task in tasks:
        status = "done" if task.completed else "pending"
        print(f"{task.task_id}. [{status}] {task.title}")


def read_task_id() -> int | None:
    try:
        return int(input("Task ID: ").strip())
    except ValueError:
        print("Please enter a valid number.")
        return None


def run_cli(manager: TaskManager) -> None:
    while True:
        print("\nTo-Do List")
        print("1. Add a task")
        print("2. View all tasks")
        print("3. Mark a task as completed")
        print("4. Delete a task")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            title = input("Task title: ")
            try:
                task = manager.add_task(title)
            except ValueError as error:
                print(error)
            else:
                print(f"Added task {task.task_id}: {task.title}")
        elif choice == "2":
            display_tasks(manager)
        elif choice == "3":
            task_id = read_task_id()
            if task_id is not None:
                if manager.complete_task(task_id):
                    print("Task marked as completed.")
                else:
                    print("No task found with that ID.")
        elif choice == "4":
            task_id = read_task_id()
            if task_id is not None:
                if manager.delete_task(task_id):
                    print("Task deleted.")
                else:
                    print("No task found with that ID.")
        elif choice == "5":
            print("Goodbye!")
            return
        else:
            print("Please choose a number from 1 to 5.")


def main() -> None:
    try:
        manager = TaskManager(SQLiteTaskRepository(DEFAULT_DATABASE_PATH))
    except (OSError, sqlite3.Error) as error:
        print(f"Could not open the task database: {error}")
        return

    run_cli(manager)