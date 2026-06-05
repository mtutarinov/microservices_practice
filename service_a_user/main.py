import asyncio

from fastapi import FastAPI

from app.logger import get_logger
from service_a_user.schemas import UserCreated
from service_a_user.producer import ProducerService

app = FastAPI()
logger = get_logger(__name__)


@app.post("/")
async def create_user(user: UserCreated):
    message = user.model_dump()
    producer = ProducerService()
    try:
        await producer.send_message(message)
        return {"status": 200}
    except Exception as e:
        logger.error(e)
        return {"status": 503}



