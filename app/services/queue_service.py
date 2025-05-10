import pika

from app.config.settings import settings
from app.models import QueuePredictionRequest
from typing import Callable

class QueueService:
    """
        Service to handle RabbitMQ operations
    """

    def __init__(self):
        self.connection = None
        self.channel = None
    
    def connect(self):
        """
            Function to establish rabbitMQ connection
        """

        # Connect only if connection does not exists or expired
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host = settings.RABBITMQ_HOST,
                    credentials= pika.PlainCredentials(
                        username= settings.RABBITMQ_USER,
                        password= settings.RABBITMQ_PASSWORD
                    )
                )
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=settings.RABBITMQ_QUEUE)
        

    def publish_prediction(self, message: QueuePredictionRequest) -> None:
        """
            Function to publish prediction request in queue
        """

        try:
            self.connect()
            self.channel.basic_publish(
                exchange='',
                routing_key=settings.RABBITMQ_QUEUE,
                body=message.model_dump_json()
            )

        except Exception as ex:
            print(str(ex))
            if self.connection and not self.connection.is_closed:
                self.connection.close()
    
    def consume_prediction_request(self, callback: Callable) -> None:
        """
            Function to consume prediction requests
        """

        try:
            self.connect()
            self.channel.basic_consume(
                queue=settings.RABBITMQ_QUEUE,
                on_message_callback=callback,
                auto_ack=True
            )
            self.channel.start_consuming()
        except Exception as ex:
            print(str(ex))
            if self.connection and not self.connection.is_closed:
                self.connection.close()


