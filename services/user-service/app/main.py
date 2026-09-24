from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import User
from app.schemas import UserCreate, UserUpdate

app = FastAPI(title="User Service")


Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "user-service"
    }


@app.post("/users")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = User(
        name=user.name,
        email=user.email
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "message": "User created successfully",
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email
     
        }
    }

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return {
        "users": [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
            for user in users
        ]
    }

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }

@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db_user.name = user.name
    db_user.email = user.email

    db.commit()
    db.refresh(db_user)

    return {
        "message": "User updated successfully",
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email
        }
    }

@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(db_user)
    db.commit()

    return {
        "message": "User deleted successfully",
        "user_id": user_id
    }
