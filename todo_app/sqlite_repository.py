import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path

from .task import Task


DEFAULT_DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "tasks.db"


class SQLiteTaskRepository:
    def __init__(self, database_path: Path = DEFAULT_DATABASE_PATH) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.database_path)) as connection:
            with connection:
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        completed INTEGER NOT NULL DEFAULT 0,
                        created_at TEXT NOT NULL
                    )
                    """
                )

    def create_task(self, title: str) -> Task:
        created_at = datetime.now().astimezone().isoformat(timespec="seconds")
        with closing(sqlite3.connect(self.database_path)) as connection:
            with connection:
                cursor = connection.execute(
                    "INSERT INTO tasks (title, completed, created_at) VALUES (?, 0, ?)",
                    (title, created_at),
                )
                task_id = cursor.lastrowid

        return Task(
            task_id=task_id,
            title=title,
            created_at=datetime.fromisoformat(created_at),
        )

    def get_tasks(self) -> list[Task]:
        with closing(sqlite3.connect(self.database_path)) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                "SELECT id, title, completed, created_at FROM tasks ORDER BY id"
            ).fetchall()
        return [self._to_task(row) for row in rows]

    def get_task(self, task_id: int) -> Task | None:
        with closing(sqlite3.connect(self.database_path)) as connection:
            connection.row_factory = sqlite3.Row
            row = connection.execute(
                "SELECT id, title, completed, created_at FROM tasks WHERE id = ?",
                (task_id,),
            ).fetchone()
        return self._to_task(row) if row is not None else None

    def complete_task(self, task_id: int) -> Task | None:
        with closing(sqlite3.connect(self.database_path)) as connection:
            connection.row_factory = sqlite3.Row
            with connection:
                connection.execute(
                    "UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,)
                )
                row = connection.execute(
                    "SELECT id, title, completed, created_at FROM tasks WHERE id = ?",
                    (task_id,),
                ).fetchone()
        return self._to_task(row) if row is not None else None

    def delete_task(self, task_id: int) -> bool:
        with closing(sqlite3.connect(self.database_path)) as connection:
            with connection:
                cursor = connection.execute(
                    "DELETE FROM tasks WHERE id = ?", (task_id,)
                )
                return cursor.rowcount > 0

    @staticmethod
    def _to_task(row: sqlite3.Row) -> Task:
        return Task(
            task_id=row["id"],
            title=row["title"],
            completed=bool(row["completed"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )