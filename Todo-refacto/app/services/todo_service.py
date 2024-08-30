from app.db.firebase import db
from app.schemas.schema_todo import TodoCreate, TodoUpdate

class TodoService:
    @staticmethod
    def get_todo_collection():
        return db.collection('todos')

    @classmethod
    def create_todo(cls, todo_data: TodoCreate):
        todo_ref = cls.get_todo_collection().document()
        todo_id = todo_ref.id
        new_todo = {**todo_data.dict(), "id": todo_id, "completed": False}
        todo_ref.set(new_todo)
        return new_todo

    @classmethod
    def get_todo(cls, todo_id: str):
        todo_ref = cls.get_todo_collection().document(todo_id)
        todo = todo_ref.get()
        if not todo.exists:
            return None
        return todo.to_dict()

    @classmethod
    def get_all_todos(cls):
        todos = cls.get_todo_collection().stream()
        return [todo.to_dict() for todo in todos]

    @classmethod
    def update_todo(cls, todo_id: str, todo_data: TodoUpdate):
        todo_ref = cls.get_todo_collection().document(todo_id)
        todo = todo_ref.get()
        if not todo.exists:
            return None
        todo_ref.update(todo_data.dict(exclude_unset=True))
        return todo_ref.get().to_dict()

    @classmethod
    def delete_todo(cls, todo_id: str):
        todo_ref = cls.get_todo_collection().document(todo_id)
        todo = todo_ref.get()
        if not todo.exists:
            return None
        todo_ref.delete()
        return {"message": "Todo deleted"}
