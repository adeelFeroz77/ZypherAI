from app.models import QueuePredictionRequest
from app.services.prediction_service import PredictionService
from app.services.queue_service import QueueService

prediction_service = PredictionService()
queue_service = QueueService()

class ConsumerService():
        
    def start_consumer(self):
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