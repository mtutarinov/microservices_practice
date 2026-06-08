import os
from pydantic import BaseModel

class Settings(BaseModel):
    topic: str = "user.events"
    bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    group_id: str = "logger-group"
    validation_url = os.getenv("VALIDATION_SERVICE_URL", "http://127.0.0.1:8001")


settings = Settings()