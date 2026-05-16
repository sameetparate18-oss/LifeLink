from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Header,
    status
)

from fastapi.middleware.cors import CORSMiddleware

from pydantic import (
    BaseModel,
    EmailStr
)

from jose import (
    jwt,
    JWTError
)

from passlib.context import CryptContext

from datetime import (
    datetime,
    timedelta
)

from typing import Optional

import sqlite3
import logging

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from app.ai.predictor import (
    predict_disease,
    predictor_health_check
)
# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(
    "lifelink.backend"
)

# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="LifeLink AI",
    version="6.0.0",
    description="AI Emergency Blood & Organ Donation System"
)

# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = "lifelink_ultra_secure_key_2026"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 120

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# =========================================================
# DATABASE
# =========================================================

DATABASE_NAME = "lifelink.db"


def get_db():

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    conn.row_factory = sqlite3.Row

    return conn


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_db():

    conn = get_db()

    cursor = conn.cursor()

    # USERS TABLE

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        role TEXT NOT NULL,

        created_at TEXT
    )
    """)

    # EMERGENCIES TABLE

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emergencies (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_email TEXT,

        location TEXT,

        status TEXT,

        donor TEXT,

        hospital TEXT,

        priority TEXT,

        created_at TEXT
    )
    """)

    conn.commit()

    conn.close()

    logger.info(
        "✅ Database initialized successfully"
    )


init_db()

# =========================================================
# PYDANTIC MODELS
# =========================================================

class RegisterModel(BaseModel):

    email: EmailStr

    password: str

    role: str = "user"


class LoginModel(BaseModel):

    email: EmailStr

    password: str


class EmergencyModel(BaseModel):

    email: EmailStr

    location: str

    priority: str = "medium"


class DiseasePredictionModel(BaseModel):

    symptoms: list[str]


# =========================================================
# PASSWORD HELPERS
# =========================================================

def hash_password(password: str):

    return pwd_context.hash(password)


def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# =========================================================
# JWT TOKEN
# =========================================================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# =========================================================
# AUTH MIDDLEWARE
# =========================================================

def get_current_user(
    authorization: Optional[str] = Header(None)
):

    if not authorization:

        raise HTTPException(

            status_code=401,

            detail="Authorization token missing"
        )

    try:

        token = authorization.split(" ")[1]

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        raise HTTPException(

            status_code=401,

            detail="Invalid token"
        )


# =========================================================
# ROLE CHECK
# =========================================================

def require_role(user, role):

    if user["role"] != role:

        raise HTTPException(

            status_code=403,

            detail=f"{role} access required"
        )


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def home():

    return {

        "system":
            "LifeLink AI Backend",

        "status":
            "ACTIVE",

        "version":
            "6.0.0"
    }


# =========================================================
# REGISTER
# =========================================================

@app.post("/register")
def register(user: RegisterModel):

    conn = get_db()

    cursor = conn.cursor()

    try:

        cursor.execute("""

        INSERT INTO users (

            email,
            password,
            role,
            created_at

        )

        VALUES (?, ?, ?, ?)

        """, (

            user.email,

            hash_password(
                user.password
            ),

            user.role,

            str(datetime.utcnow())
        ))

        conn.commit()

        logger.info(
            f"✅ User registered: {user.email}"
        )

        return {

            "message":
                "User registered successfully",

            "role":
                user.role
        }

    except sqlite3.IntegrityError:

        raise HTTPException(

            status_code=400,

            detail="User already exists"
        )

    finally:

        conn.close()


# =========================================================
# LOGIN
# =========================================================

@app.post("/login")
def login(user: LoginModel):

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM users WHERE email=?",

        (user.email,)
    )

    db_user = cursor.fetchone()

    conn.close()

    if not db_user:

        raise HTTPException(

            status_code=404,

            detail="User not found"
        )

    if not verify_password(

        user.password,

        db_user["password"]
    ):

        raise HTTPException(

            status_code=400,

            detail="Incorrect password"
        )

    token = create_access_token({

        "email":
            db_user["email"],

        "role":
            db_user["role"]
    })

    logger.info(
        f"✅ User logged in: {user.email}"
    )

    return {

        "access_token":
            token,

        "token_type":
            "bearer",

        "role":
            db_user["role"]
    }


# =========================================================
# CREATE EMERGENCY
# =========================================================

@app.post("/emergency")
def create_emergency(

    emergency: EmergencyModel,

    user=Depends(get_current_user)
):

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO emergencies (

        user_email,
        location,
        status,
        donor,
        hospital,
        priority,
        created_at

    )

    VALUES (?, ?, ?, ?, ?, ?, ?)

    """, (

        emergency.email,

        emergency.location,

        "searching_donor",

        None,

        None,

        emergency.priority,

        str(datetime.utcnow())
    ))

    conn.commit()

    conn.close()

    logger.info(
        f"🚨 Emergency created: {emergency.email}"
    )

    return {

        "message":
            "Emergency created successfully",

        "status":
            "searching_donor"
    }


# =========================================================
# GET EMERGENCIES
# =========================================================

@app.get("/emergencies")
def get_emergencies(
    user=Depends(get_current_user)
):

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM emergencies

    ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return {

        "data":

            [dict(row) for row in rows]
    }


# =========================================================
# DONOR CLAIM
# =========================================================

@app.put("/donor/claim/{eid}")
def donor_claim(

    eid: int,

    donor_email: str,

    user=Depends(get_current_user)
):

    require_role(
        user,
        "donor"
    )

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute("""

    UPDATE emergencies

    SET donor=?,
        status=?

    WHERE id=?

    """, (

        donor_email,

        "donor_assigned",

        eid
    ))

    conn.commit()

    conn.close()

    return {

        "message":
            "Donor assigned successfully"
    }


# =========================================================
# HOSPITAL ACCEPT
# =========================================================

@app.put("/hospital/accept/{eid}")
def hospital_accept(

    eid: int,

    hospital: str,

    user=Depends(get_current_user)
):

    require_role(
        user,
        "hospital"
    )

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute("""

    UPDATE emergencies

    SET hospital=?,
        status=?

    WHERE id=?

    """, (

        hospital,

        "hospital_assigned",

        eid
    ))

    conn.commit()

    conn.close()

    return {

        "message":
            "Hospital assigned"
    }


# =========================================================
# COMPLETE EMERGENCY
# =========================================================

@app.put("/emergency/complete/{eid}")
def complete_emergency(

    eid: int,

    user=Depends(get_current_user)
):

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute("""

    UPDATE emergencies

    SET status=?

    WHERE id=?

    """, (

        "completed",

        eid
    ))

    conn.commit()

    conn.close()

    return {

        "message":
            "Emergency completed"
    }


# =========================================================
# DASHBOARD ANALYTICS
# =========================================================

@app.get("/dashboard")
def dashboard(
    user=Depends(get_current_user)
):

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM emergencies"
    )

    total_cases = cursor.fetchone()[0]

    cursor.execute("""

    SELECT COUNT(*)

    FROM emergencies

    WHERE status='searching_donor'

    """)

    searching_donor = cursor.fetchone()[0]

    cursor.execute("""

    SELECT COUNT(*)

    FROM emergencies

    WHERE status='completed'

    """)

    completed_cases = cursor.fetchone()[0]

    conn.close()

    return {

        "total_cases":
            total_cases,

        "searching_donor":
            searching_donor,

        "completed_cases":
            completed_cases,

        "system":
            "LifeLink Active"
    }


# =========================================================
# AI DISEASE PREDICTION
# =========================================================

@app.post("/predict")
def predict_disease_api(
    request: DiseasePredictionModel
):

    result = predict_disease(
        request.symptoms
    )

    return result


# =========================================================
# AI HEALTH CHECK
# =========================================================

@app.get("/ai/health")
def ai_health():

    return predictor_health_check()