import uvicorn

from fastapi import FastAPI
from app.api.routes.predict import router
from app.config.settings import settings
from app.services.consumer_service import ConsumerService
from app.models import QueuePredictionRequest
from threading import Thread

app = FastAPI(title=settings.APP_NAME)

app.include_router(router)

consumer_service = ConsumerService()


@app.on_event("startup")
def start_consumer_thread():
    """Start RabbitMQ on FastAPI startup"""
    Thread(target=consumer_service.start_consumer, daemon=True).start()

if __name__ == '__main__':
    uvicorn.run (
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )