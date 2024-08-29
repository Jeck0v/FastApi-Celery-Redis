from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.schema_todo import TodoCreate, TodoUpdate, TodoResponse
from app.auth.firebase_auth import get_current_user
from app.db.firebase import db
from app.worker import celery_app
from celery.result import AsyncResult

router = APIRouter()

def get_todo_collection():
    return db.collection('todos')

@celery_app.task
def create_todo_task(todo_data: dict):
    todo_ref = get_todo_collection().document()
    todo_id = todo_ref.id
    new_todo = {**todo_data, "id": todo_id, "completed": False}
    todo_ref.set(new_todo)
    return new_todo

@router.post("/", response_model=TodoResponse)
async def create_todo(todo: TodoCreate, user: dict = Depends(get_current_user)):
    task = create_todo_task.apply_async(args=[todo.dict()])
    result = AsyncResult(task.id)
    new_todo = result.get()
    return new_todo

@celery_app.task
def get_todo_task(todo_id: str):
    todo_ref = get_todo_collection().document(todo_id)
    todo = todo_ref.get()
    if not todo.exists:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo.to_dict()

@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: str, user: dict = Depends(get_current_user)):
    task = get_todo_task.apply_async(args=[todo_id])
    result = AsyncResult(task.id)
    todo = result.get()
    return todo

@celery_app.task
def get_all_todos_task():
    todos = get_todo_collection().stream()
    todo_list = [todo.to_dict() for todo in todos]
    return todo_list

@router.get("/", response_model=List[TodoResponse])
async def get_all_todos(user: dict = Depends(get_current_user)):
    task = get_all_todos_task.apply_async()
    result = AsyncResult(task.id)
    todos = result.get()
    return todos

@celery_app.task
def update_todo_task(todo_id: str, todo_data: dict):
    todo_ref = get_todo_collection().document(todo_id)
    todo = todo_ref.get()
    if not todo.exists:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_ref.update(todo_data)
    updated_todo = todo_ref.get().to_dict()
    return updated_todo

@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: str, todo_update: TodoUpdate, user: dict = Depends(get_current_user)):
    task = update_todo_task.apply_async(args=[todo_id, todo_update.dict(exclude_unset=True)])
    result = AsyncResult(task.id)
    updated_todo = result.get()
    return updated_todo

@celery_app.task
def delete_todo_task(todo_id: str):
    todo_ref = get_todo_collection().document(todo_id)
    todo = todo_ref.get()
    if not todo.exists:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_ref.delete()
    return {"message": "Todo deleted"}

@router.delete("/{todo_id}")
async def delete_todo(todo_id: str, user: dict = Depends(get_current_user)):
    task = delete_todo_task.apply_async(args=[todo_id])
    result = AsyncResult(task.id)
    message = result.get()
    return message
