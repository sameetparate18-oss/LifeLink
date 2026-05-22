from pydantic import BaseModel

class Donor(BaseModel):

    name: str
    blood_group: str
    city: str

    latitude: float
    longitude: float

    organ: str

    available: bool