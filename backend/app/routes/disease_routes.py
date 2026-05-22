from fastapi import APIRouter

from app.ai.disease_engine import (
    process_disease_prediction
)

router = APIRouter()

# ================= DISEASE PREDICTION =================

@router.get("/predict")

def predict(symptoms: str):

    result = process_disease_prediction(
        symptoms
    )

    return result