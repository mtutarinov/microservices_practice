from pydantic import BaseModel


class Settings(BaseModel):

    topic: str = "user.events"
    bootstrap_servers: str = 'localhost:9092'
    group_id: str = "logger-group"


settings = Settings()