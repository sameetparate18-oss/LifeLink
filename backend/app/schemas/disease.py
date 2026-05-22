from pydantic import BaseModel

class DiseaseInput(BaseModel):

    symptoms: str