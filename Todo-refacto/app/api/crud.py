from typing import List
from fastapi import APIRouter, Depends, HTTPException
from celery.result import AsyncResult
from app.auth.firebase_auth import get_current_user
from app.schemas.schema_todo import TodoCreate, TodoUpdate, TodoResponse
from app.tasks.todo_tasks import (
    create_todo_task,
    get_todo_task,
    get_all_todos_task,
    update_todo_task,
    delete_todo_task,
)

router = APIRouter()

@router.post("/", response_model=TodoResponse)
async def create_todo(todo: TodoCreate, user: dict = Depends(get_current_user)):
    task = create_todo_task.apply_async(args=[todo.dict()])
    result = AsyncResult(task.id).get()
    return result

@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: str, user: dict = Depends(get_current_user)):
    try:
        task = get_todo_task.apply_async(args=[todo_id])
        result = AsyncResult(task.id).get()
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Todo not found")

@router.get("/", response_model=List[TodoResponse])
async def get_all_todos(user: dict = Depends(get_current_user)):
    task = get_all_todos_task.apply_async()
    result = AsyncResult(task.id).get()
    return result

@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: str, todo_update: TodoUpdate, user: dict = Depends(get_current_user)):
    try:
        task = update_todo_task.apply_async(args=[todo_id, todo_update.dict(exclude_unset=True)])
        result = AsyncResult(task.id).get()
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Todo not found")

@router.delete("/{todo_id}")
async def delete_todo(todo_id: str, user: dict = Depends(get_current_user)):
    try:
        task = delete_todo_task.apply_async(args=[todo_id])
        result = AsyncResult(task.id).get()
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Todo not found")
