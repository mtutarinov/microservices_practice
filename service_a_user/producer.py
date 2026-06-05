import json

from aiokafka import AIOKafkaProducer

from app.settings import settings
from app.logger import get_logger

class ProducerService:

    def __init__(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        self.logger = get_logger(__name__)

    async def send_message(self, message: dict):
        await self.producer.start()
        self.logger.info(f"Sending message: {message}")
        await self.producer.send(settings.topic, message)
        self.logger.info(f"Message sent: {message}")
        await self.producer.stop()
        self.logger.info(f"Producer stopped")
