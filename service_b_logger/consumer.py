import asyncio
import json

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError

from app.settings import settings
from app.logger import get_logger

class ConsumerService:

    def __init__(self):
        self.consumer = AIOKafkaConsumer(
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
                        f" X-Request-Id: {message.value['request_id']}"
                        f"Received UserCreated:"
                        f"  {message.value['id']} -> {message.value['name']}"
                    )
            except asyncio.CancelledError:
                self.logger.info("Consumer canceled.")
                break
            except KafkaError as e:
                self.logger.error(f"Kafka error: {e}, retry after {self.exp ** 2} seconds.")
                await asyncio.sleep(self.exp ** 2)
                self.exp += 1
            finally:
                await self.consumer.stop()
                self.logger.info("Consumer finished.")
