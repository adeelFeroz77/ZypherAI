from pydantic import BaseModel

class SynchronousPredictionResponse(BaseModel):
    input: str
    result: str

class PredictionRequest(BaseModel):
    input: str