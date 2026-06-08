from datetime import timedelta
from contextlib import asynccontextmanager
from uuid import uuid4

import aiobreaker
import aiohttp
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from aiobreaker import CircuitBreaker

from app.logger import get_logger
from app.settings import settings
from service_a_user.schemas import UserCreated
from service_a_user.producer import ProducerService

circuit_breaker = CircuitBreaker(
    fail_max=2,
    timeout_duration=timedelta(seconds=10),
)

@circuit_breaker
async def check_user(name: str, request_id: str):
    uri = f"{settings.validation_url}/{name}"
    headers = {"request_id": request_id}
    timeout = aiohttp.ClientTimeout(total=2)
    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        response = await session.get(uri)
        response.raise_for_status()
        return await response.json()

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
    message["id"] = str(uuid4())
    request_id = str(uuid4())
    producer = app.state.producer
    try:
        result = await check_user(message["name"], request_id)
    except aiobreaker.CircuitBreakerError as e:
        logger.error(f"CircuitBreakerError: {e}")
        return JSONResponse(
            status_code=503,
            content={"error": str(e)}
        )
    except Exception as e:
        logger.error(f"Exception: {e}")
        return JSONResponse(
            status_code=503,
            content={"error": "Internal Server Error"}
        )
    if result.get("exists") is False:
        try:
            message["request_id"] = request_id
            await producer.send_message(message)
            return {"status": 200}
        except Exception as e:
            logger.exception(e)
            return JSONResponse(
                status_code=503,
                content={"error": "Internal Server Error"}
            )
    return JSONResponse(
        status_code=409,
        content={"error": "User already exists"}
    )



