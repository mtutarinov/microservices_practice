from typing import Any
from pydantic import BaseModel
from aiokafka import AIOKafkaConsumer

class Settings(BaseModel):

    topic: str = "user.events"
    consumer: Any = AIOKafkaConsumer
    bootstrap_servers: str = 'localhost:9092'
    group_id: str = "logger-group"


settings = Settings()