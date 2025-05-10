from fastapi import APIRouter, HTTPException, Header
from app.services.prediction_service import PredictionService
from app.models import SynchronousPredictionResponse, PredictionRequest, AsynchronousPredictResponse, PredictionResponse
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api")
prediction_service = PredictionService()

@router.post("/predict", response_model=SynchronousPredictionResponse | AsynchronousPredictResponse)
def predict(
    request: PredictionRequest,
    async_mode: bool = Header(False, alias="Async-Mode")
    ):

    if not async_mode:
        response = prediction_service.predict_sync(request.input)
        return response
    
    prediction_id = prediction_service.predict_async(request.input)
    
    response = AsynchronousPredictResponse (
        message = "Request received. Processing asynchronously.",
        prediction_id= prediction_id
    )
    return JSONResponse(
        status_code=202,
        content=response.model_dump()
    )

@router.get("/predict/{prediction_id}", response_model=PredictionResponse)
def get_prediction(prediction_id: str):

    if prediction_service.is_processing_by_id(prediction_id):
        raise HTTPException(
            status_code=400,
            detail="Prediction is still being processed." 
        )
    
    result = prediction_service.get_prediction_by_id(prediction_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Prediction ID not found."
        )
    
    prediction_response = PredictionResponse(
        prediction_id= prediction_id,
        output= result
    )

    return prediction_response
