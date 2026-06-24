from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI(title="Doable API", version="1.0.0")

# Enable CORS so React frontend can talk to this API locally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Default Vite dev server port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the Task schema matching project specifications
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    priority: str  # high, medium, low
    tag: str       # work, personal, health
    due_date: date
    completed: bool = False

# Temporary in-memory database placeholder
todo_db: List[Task] = []
id_counter = 1

@app.get("/")
def read_root():
    return {"message": "Welcome to the Doable Backend API"}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return todo_db

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: Task):
    global id_counter
    task.id = id_counter
    todo_db.append(task)
    id_counter += 1
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(todo_db):
        if task.id == task_id:
            updated_task.id = task_id
            todo_db[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(todo_db):
        if task.id == task_id:
            todo_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Task not found")