from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse
)

from app.services.auth_service import (
    register_user,
    login_user
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


# REGISTER
@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

  try:
        user = register_user(db, request)

        return {
            "message": "User registered successfully",
            "user_id": user.id
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# LOGIN
@router.post(
    "/login",
    response_model=TokenResponse
)

def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    token = login_user(
        db,
        request.email,
        request.password
    )

     if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    } 