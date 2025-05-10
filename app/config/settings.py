from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "ZypherAI"
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_QUEUE: str = "predictionqueue"
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    API_PORT: int = 8080
    API_HOST: str = "0.0.0.0"

settings = Settings()