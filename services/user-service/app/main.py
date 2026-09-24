from fastapi import FastAPI
from app.schemas import UserCreate

app = FastAPI(title="User Service")


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "user-service"
    }


@app.post("/users")
def create_user(user: UserCreate):
    return {
        "message": "User created successfully",
        "user": user
    }