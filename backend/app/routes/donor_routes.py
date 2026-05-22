from fastapi import APIRouter
from app.schemas.donor import Donor
from app.core.database import conn

router = APIRouter()

@router.post("/register_donor")

def register_donor(donor: Donor):

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO donors (

        name,
        blood_group,
        city,
        latitude,
        longitude,
        organ,
        available

    )

    VALUES (?, ?, ?, ?, ?, ?, ?)

    """, (

        donor.name,
        donor.blood_group,
        donor.city,

        donor.latitude,
        donor.longitude,

        donor.organ,

        int(donor.available)

    ))

    conn.commit()

    return {

        "message": "Donor Registered"

    }