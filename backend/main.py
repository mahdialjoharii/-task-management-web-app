from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Task Management API is running !"}