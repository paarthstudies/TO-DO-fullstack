from .repository import TaskRepository
from .task import Task


class TaskManager:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def add_task(self, title: str) -> Task:
        clean_title = title.strip()
        if not clean_title:
            raise ValueError("Task title cannot be empty.")

        return self.repository.create_task(clean_title)

    def get_tasks(self) -> list[Task]:
        return self.repository.get_tasks()

    def get_task(self, task_id: int) -> Task | None:
        return self.repository.get_task(task_id)

    def complete_task(self, task_id: int) -> bool:
        return self.repository.complete_task(task_id) is not None

    def delete_task(self, task_id: int) -> bool:
        return self.repository.delete_task(task_id)