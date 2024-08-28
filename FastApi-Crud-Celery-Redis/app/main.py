from fastapi import FastAPI
from app.api.crud import router as todo_router

app = FastAPI()

app.include_router(todo_router, prefix="/todos", tags=["todos"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the TodoApp API"}
