from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.logger import get_logger
from service_a_user.schemas import UserCreated
from service_a_user.producer import ProducerService

@asynccontextmanager
async def lifespan(app: FastAPI):
    producer_service = ProducerService()
    await producer_service.start()
    app.state.producer = producer_service
    yield
    await producer_service.stop()

app = FastAPI(lifespan=lifespan)
logger = get_logger(__name__)


@app.post("/")
async def create_user(user_created: UserCreated):
    message = user_created.model_dump(mode="json")
    producer = app.state.producer
    try:
        await producer.send_message(message)
        return {"status": 200}
    except Exception as e:
        logger.exception(e)
        return {"status": 503}



