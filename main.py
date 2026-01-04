import json
from contextlib import asynccontextmanager
from enum import IntEnum
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from redis import Redis
from starlette import status
import httpx

@asynccontextmanager
def lifespan(app: FastAPI):
    app.state.redis = Redis(host="localhost", port=6379)
    app.state.http_client = httpx.AsyncClient()
    yield # signal server that the application is ready to start serving request.
    app.state.redis.close()

class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=100, description="Name of the todo")
    todo_description: str = Field(..., description="Description of the todo")
    priority: Priority = Field(default=Priority.LOW, description="Priority of the todo")


class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    todo_id: int = Field(..., description="Unique identifier of the todo")

class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=100, description="Name of the todo")
    todo_description: Optional[str] = Field(None, description="Description of the todo")
    priority: Optional[Priority] = Field(None, description="Priority of the todo")
api = FastAPI(lifespan=lifespan)

all_todos = [
    Todo(todo_id=1, todo_name='sports', todo_description='Go to Gym', priority=Priority.MEDIUM),
    Todo(todo_id=2, todo_name='Grocery', todo_description='Get grocery', priority=Priority.HIGH),
]

@api.get("/")
async def root():
    return {"message": "Hello World"}

@api.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not found.")


@api.get("/todos", response_model=List[Todo])
def get_todos(first_n:int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos

@api.post(
    "/todos" , response_model=Todo)
def create_todo(todo:TodoCreate):
    new_todo_id = max(todo.todo_id for todo in all_todos) + 1
    new_todo = Todo(todo_id=new_todo_id, todo_name=todo.todo_name, todo_description=todo.todo_description, priority=todo.priority)
    all_todos.append(new_todo)
    return new_todo_id


@api.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id:int, updated_todo:TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            if updated_todo.todo_name is not None:
                todo.todo_name = updated_todo.todo_name
            if updated_todo.todo_description is not None:
                todo.todo_description = updated_todo.todo_description
            if updated_todo.priority is not None:
                todo.priority = updated_todo.priority
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not found.")

@api.delete("/todos/{todo_id}", response_model=Todo)
def delete_todo(todo_id:int):
    for index, todo in enumerate(all_todos):
        if todo.todo_id == todo_id:
            deleted_todo = all_todos.pop(index)
            return deleted_todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not found.")


@api.get("/entries")
async def get_entries():
    value = api.state.redis.get("entries")
    if value is None:
        response = await api.state.http_client.get("https://api.publicapis.org/entries")
        value = response.json()
        data_str = json.dumps(value)
        api.state.redis.set("entries", data_str)
    return json.loads(value)