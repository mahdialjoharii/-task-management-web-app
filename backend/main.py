from fastapi import FastAPI

from database.database import Base, engine
from models import user, project, task
from routers.tasks import router as tasks_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks_router)


@app.get("/")
def root():
    return {"message": "Task Management API is running"}