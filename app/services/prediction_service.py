from app.models import SynchronousPredictionResponse
from app.core.predictor import mock_model_predict

class PredictionService:
    """Service to handle Predictions"""

    def predict_sync(self, input_text: str) -> SynchronousPredictionResponse:
        """
            Function to execute synchronous prediction
        """

        return mock_model_predict(input_text)
