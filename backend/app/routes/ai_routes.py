from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.predictor import predict_disease

router = APIRouter()

class SymptomRequest(BaseModel):
    symptoms: list

@router.post("/predict")
def predict(req: SymptomRequest):

    result = predict_disease(req.symptoms)

    return {
        "prediction": result
    }