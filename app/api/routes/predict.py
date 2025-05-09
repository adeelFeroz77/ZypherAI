from fastapi import APIRouter, HTTPException, Header
from app.services.prediction_service import PredictionService
from app.models import SynchronousPredictionResponse, PredictionRequest

router = APIRouter(prefix="/api")
prediction_service = PredictionService()

@router.post("/predict", response_model=SynchronousPredictionResponse)
def predict(request: PredictionRequest):

    response = prediction_service.predict_sync(request.input)
    return response