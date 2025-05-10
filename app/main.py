import uvicorn

from fastapi import FastAPI
from app.api.routes.predict import router
from app.config.settings import settings
from app.services.queue_service import QueueService
from app.services.prediction_service import PredictionService
from app.models import QueuePredictionRequest
from threading import Thread

app = FastAPI(title=settings.APP_NAME)

app.include_router(router)

queue_service = QueueService()
prediction_service = PredictionService()

def start_consumer():
    """Background process for consumer"""
    def callback(ch, method, properties, body):
        """
            Process prediction from consumer
        """
        try:
            request = QueuePredictionRequest.model_validate_json(body)

            result = prediction_service.predict_sync(request.input)

            #store result in temporary memory
            prediction_service.store_async_prediction_result(request.prediction_id, result)

        except Exception as ex:
            print(str(ex))
            
    while True:
        try:
            queue_service.consume_prediction_request(callback)
        except Exception as ex:
            print(str(ex))


@app.on_event("startup")
def start_consumer_thread():
    """Start RabbitMQ on FastAPI startup"""
    Thread(target=start_consumer, daemon=True).start()

if __name__ == '__main__':
    uvicorn.run (
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )