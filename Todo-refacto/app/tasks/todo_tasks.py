from app.worker import celery_app
from app.services.todo_service import TodoService

@celery_app.task
def create_todo_task(todo_data: dict):
    return TodoService.create_todo(todo_data)

@celery_app.task
def get_todo_task(todo_id: str):
    todo = TodoService.get_todo(todo_id)
    if todo is None:
        raise ValueError("Todo not found")
    return todo

@celery_app.task
def get_all_todos_task():
    return TodoService.get_all_todos()

@celery_app.task
def update_todo_task(todo_id: str, todo_data: dict):
    updated_todo = TodoService.update_todo(todo_id, todo_data)
    if updated_todo is None:
        raise ValueError("Todo not found")
    return updated_todo

@celery_app.task
def delete_todo_task(todo_id: str):
    result = TodoService.delete_todo(todo_id)
    if result is None:
        raise ValueError("Todo not found")
    return result
