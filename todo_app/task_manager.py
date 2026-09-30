from .storage import JsonTaskStorage
from .task import Task


class TaskManager:
    def __init__(self, storage: JsonTaskStorage) -> None:
        self.storage = storage
        self.tasks = storage.load_tasks()

    def add_task(self, title: str) -> Task:
        clean_title = title.strip()
        if not clean_title:
            raise ValueError("Task title cannot be empty.")

        next_id = max((task.task_id for task in self.tasks), default=0) + 1
        task = Task(task_id=next_id, title=clean_title)
        self.tasks.append(task)
        self.storage.save_tasks(self.tasks)
        return task

    def get_tasks(self) -> list[Task]:
        return list(self.tasks)

    def complete_task(self, task_id: int) -> bool:
        for task in self.tasks:
            if task.task_id == task_id:
                if not task.completed:
                    task.completed = True
                    self.storage.save_tasks(self.tasks)
                return True
        return False

    def delete_task(self, task_id: int) -> bool:
        for index, task in enumerate(self.tasks):
            if task.task_id == task_id:
                del self.tasks[index]
                self.storage.save_tasks(self.tasks)
                return True
        return False