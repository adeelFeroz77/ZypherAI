from pydantic import BaseModel

class SynchronousPredictionResponse(BaseModel):
    input: str
    result: str

class PredictionRequest(BaseModel):
    input: str

class AsynchronousPredictResponse(BaseModel):
    message: str
    prediction_id: str

class PredictionResponse(BaseModel):
    prediction_id: str
    output: SynchronousPredictionResponse

class QueuePredictionRequest(BaseModel):
    prediction_id: str
    input: str