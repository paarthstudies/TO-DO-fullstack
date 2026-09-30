from dataclasses import dataclass


@dataclass
class Task:
    task_id: int
    title: str
    completed: bool = False

    def to_dict(self) -> dict[str, int | str | bool]:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict[str, int | str | bool]) -> "Task":
        return cls(
            task_id=int(data["task_id"]),
            title=str(data["title"]),
            completed=bool(data["completed"]),
        )