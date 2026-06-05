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

    async def start(self):
        self.logger.info("Producer started")
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()
        self.logger.info(f"Producer stopped")

    async def send_message(self, message: dict):
        self.logger.info(f"Sending message: {message}")
        await self.producer.send(settings.topic, message)
        self.logger.info(f"Message sent: {message}")
