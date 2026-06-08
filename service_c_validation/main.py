from app.logger import get_logger

from fastapi import FastAPI, Request

app = FastAPI()
logger = get_logger(__name__)

@app.get("/check_user/{name}")
async def check_user(name: str, request: Request):
    logger.info(f"X-Request-Id: {request.headers.get('X-Request-Id')}")
    return {"exists": False}