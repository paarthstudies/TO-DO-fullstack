from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Task:
    task_id: int
    title: str
    completed: bool = False
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @property
    def id(self) -> int:
        return self.task_id