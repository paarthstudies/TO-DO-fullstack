import json
from pathlib import Path

from .task import Task


class JsonTaskStorage:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def load_tasks(self) -> list[Task]:
        if not self.file_path.exists():
            return []

        with self.file_path.open("r", encoding="utf-8") as file:
            task_data = json.load(file)

        if not isinstance(task_data, list):
            raise ValueError("The task file must contain a JSON list.")

        return [Task.from_dict(item) for item in task_data]

    def save_tasks(self, tasks: list[Task]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in tasks], file, indent=2)