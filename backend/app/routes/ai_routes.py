from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.user import UserCreate, UserLogin
from services.auth_service import register_user, login_user
from core.database import get_db

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    result = register_user(db, user)

    if not result:
        raise HTTPException(status_code=400, detail="User already exists")

    return {"message": "User registered successfully"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    result = login_user(db, user.email, user.password)

    if not result:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {
        "message": "Login successful",
        "token": result["token"],
        "user": {
            "id": result["user"].id,
            "name": result["user"].name,
            "email": result["user"].email
        }
    }