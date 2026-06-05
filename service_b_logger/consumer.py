import asyncio
import json

from aiokafka.errors import KafkaError

from app.settings import settings
from app.logger import get_logger

class ConsumerService:

    def __init__(self):
        self.consumer = settings.consumer(
            settings.topic,
            bootstrap_servers=settings.bootstrap_servers,
            group_id=settings.group_id,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
        self.logger = get_logger(__name__)
        self.exp = 1

    async def consume(self):
        while True:
            try:
                await self.consumer.start()
                self.logger.info("Consumer started.")
                async for message in self.consumer:
                    self.logger.info(
                        f"Received UserCreated: {message.value['id']} -> {message.value['name']}"
                    )
            except KafkaError as e:
                self.logger.error(f"Kafka error: {e}, retry after {self.exp ** 2} seconds.")
                await asyncio.sleep(self.exp ** 2)
                self.exp += 1
            finally:
                self.consumer.stop()
                self.logger.info("Consumer finished.")
