from app.models import SynchronousPredictionResponse, QueuePredictionRequest
from app.services.queue_service import QueueService
from app.core.predictor import mock_model_predict
import uuid

queue_service = QueueService()

class PredictionService:
    """Service to handle Predictions"""
    _instance = None

    # Singleton instance to use same attributes on all threads
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # temporary memory
            cls._instance.async_prediction_map = {}
            cls._instance.currently_processing = set()
        return cls._instance

    def predict_sync(self, input_text: str) -> SynchronousPredictionResponse:
        """
            Function to execute synchronous prediction
        """

        return mock_model_predict(input_text)
    
    def predict_async(self, input_text: str) -> str:
        """
            Function to execute Asynchronous Prediction
        """

        id = str(uuid.uuid4())
        self.currently_processing.add(id)

        request = QueuePredictionRequest(
            prediction_id=id,
            input=input_text
        )

        #call to rabbitMQ
        queue_service.publish_prediction(request)

        return id
    
    def get_prediction_by_id(self, prediction_id: str) -> SynchronousPredictionResponse:
        """
            Function to fetch completed asynchronous
            prediction stored in temporary memory
            against unique id
        """

        return self.async_prediction_map.get(prediction_id, None)

    def is_processing_by_id(self, prediction_id: str) -> bool:
        """
            Function to check if asynchronous prediciton
            is still in progress
        """

        return prediction_id in self.currently_processing
    
    def store_async_prediction_result(self, prediction_id: str, result: SynchronousPredictionResponse) -> None:
        """
            Function to store result of async prediction
            in temporary storage
        """

        self.async_prediction_map[prediction_id] = result
        self.currently_processing.discard(prediction_id)
