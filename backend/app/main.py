from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

from app.ai.predictor import predict_disease


# ---------------- APP ----------------

app = FastAPI(
    title="LifeLink API"
)


# ---------------- CORS ----------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- SECURITY ----------------

SECRET_KEY = "lifelink_secret_key_123"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

security = HTTPBearer()


# ---------------- USERS DATABASE ----------------
# TEMPORARY IN-MEMORY USERS

users = {
    "admin@lifelink.com": {
        "email": "admin@lifelink.com",
        "name": "Admin",
        "hashed_password": pwd_context.hash("admin123"),
        "role": "admin"
    },

    "hospital@lifelink.com": {
        "email": "hospital@lifelink.com",
        "name": "Hospital",
        "hashed_password": pwd_context.hash("hospital123"),
        "role": "hospital"
    },

    "donor@lifelink.com": {
        "email": "donor@lifelink.com",
        "name": "Donor",
        "hashed_password": pwd_context.hash("donor123"),
        "role": "donor"
    }
}


# ---------------- MODELS ----------------

class LoginRequest(BaseModel):
    email: str
    password: str


class SymptomRequest(BaseModel):
    symptoms: list


# ---------------- TOKEN CREATION ----------------

def create_token(data: dict, expires_delta: timedelta):

    payload = data.copy()

    expire = datetime.utcnow() + expires_delta

    payload.update({
        "exp": expire
    })

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# ---------------- LOGIN ----------------

@app.post("/login")
def login(user: LoginRequest):

    db_user = users.get(user.email)

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    valid_password = pwd_context.verify(
        user.password,
        db_user["hashed_password"]
    )

    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="Wrong password"
        )

    token = create_token(
        {
            "sub": db_user["email"],
            "role": db_user["role"]
        },
        timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": db_user["role"],
        "name": db_user["name"]
    }


# ---------------- GET CURRENT USER ----------------

def get_current_user(token=Depends(security)):

    try:

        payload = jwt.decode(
            token.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return {
            "email": payload.get("sub"),
            "role": payload.get("role")
        }

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


# ---------------- ROLE CHECKER ----------------

def require_role(role: str):

    def checker(user=Depends(get_current_user)):

        if user["role"] != role:

            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return user

    return checker


# ---------------- HOME ----------------

@app.get("/")
def home():

    return {
        "message": "LifeLink backend running 🚀"
    }


# ---------------- ADMIN ----------------

@app.get("/admin")
def admin(user=Depends(require_role("admin"))):

    return {
        "message": f"Welcome Admin {user['email']}"
    }


# ---------------- HOSPITAL ----------------

@app.get("/hospital")
def hospital(user=Depends(require_role("hospital"))):

    return {
        "message": f"Hospital Panel - {user['email']}"
    }


# ---------------- DONOR ----------------

@app.get("/donor")
def donor(user=Depends(require_role("donor"))):

    return {
        "message": f"Donor Panel - {user['email']}"
    }


# ---------------- AI PREDICTION ----------------

@app.post("/predict")
def predict(req: SymptomRequest):

    result = predict_disease(req.symptoms)

    return {
        "prediction": result
    }