# To-Do List

A beginner-friendly to-do application with a command-line interface and a
FastAPI REST API. Both use the same `TaskManager` and SQLite repository.

## Setup

From the project directory, create and activate a virtual environment, then
install the dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The SQLite database is created automatically at `data/tasks.db`.

## Run the CLI

```powershell
python -m todo_app
```

The menu supports adding, viewing, completing, and deleting tasks.

## Run the API

```powershell
uvicorn todo_app.api:app --reload
```

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

Available endpoints:

- `GET /tasks`
- `GET /tasks/{task_id}`
- `POST /tasks`
- `PATCH /tasks/{task_id}/complete`
- `DELETE /tasks/{task_id}`