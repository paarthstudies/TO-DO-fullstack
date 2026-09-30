from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .sqlite_repository import DEFAULT_DATABASE_PATH, SQLiteTaskRepository
from .task import Task
from .task_manager import TaskManager


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        clean_title = value.strip()
        if not clean_title:
            raise ValueError("Task title cannot be empty.")
        return clean_title


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    completed: bool
    created_at: datetime


def create_app(manager: TaskManager | None = None) -> FastAPI:
    task_manager = manager or TaskManager(
        SQLiteTaskRepository(DEFAULT_DATABASE_PATH)
    )
    app = FastAPI(title="To-Do List API", version="2.0.0")

    @app.get("/tasks", response_model=list[TaskResponse])
    def list_tasks() -> list[Task]:
        return task_manager.get_tasks()

    @app.get("/tasks/{task_id}", response_model=TaskResponse)
    def get_task(task_id: Annotated[int, Path(gt=0)]) -> Task:
        task = task_manager.get_task(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found.")
        return task

    @app.post(
        "/tasks",
        response_model=TaskResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def create_task(task_data: TaskCreate) -> Task:
        return task_manager.add_task(task_data.title)

    @app.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
    def complete_task(task_id: Annotated[int, Path(gt=0)]) -> Task:
        if not task_manager.complete_task(task_id):
            raise HTTPException(status_code=404, detail="Task not found.")
        task = task_manager.get_task(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found.")
        return task

    @app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_task(task_id: Annotated[int, Path(gt=0)]) -> None:
        if not task_manager.delete_task(task_id):
            raise HTTPException(status_code=404, detail="Task not found.")

    return app


app = create_app()