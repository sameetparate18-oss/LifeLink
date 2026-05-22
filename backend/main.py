from fastapi import FastAPI

from app.routes.disease_routes import (
    router as disease_router
)

app = FastAPI()

# ================= ROUTES =================

app.include_router(disease_router)

# ================= HOME =================

@app.get("/")

def home():

    return {

        "message": "LifeLink AI Backend Running"

    }