from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routes import user, task

app = FastAPI()

app.include_router(user.router)
app.include_router(task.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
