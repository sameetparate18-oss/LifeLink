from fastapi import APIRouter
from app.services.ai_matching_service import find_best_donors

router = APIRouter()

@router.get("/match")

def match(

    blood_group: str,
    latitude: float,
    longitude: float,
    emergency: str

):

    results = find_best_donors(

        blood_group,
        latitude,
        longitude,
        emergency

    )

    return {

        "matches": results

    }