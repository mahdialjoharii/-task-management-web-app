from fastapi import FastAPI

from database.database import Base, engine
from models import user, project, task

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Task Management API is running"}