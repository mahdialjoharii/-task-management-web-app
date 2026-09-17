from fastapi import FastAPI
from database.database import Base, engine
from models import user, project, task, comment
from routers.tasks import router as tasks_router
from routers.users import router as users_router
from routers.projects import router as projects_router
from routers.comments import router as comments_router
from fastapi.middleware.cors import CORSMiddleware
 
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(tasks_router)
app.include_router(users_router)
app.include_router(projects_router)
app.include_router(comments_router)

@app.get("/")
def root():
    return {"message": "Task Management API is running"}