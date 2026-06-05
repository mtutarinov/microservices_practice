import asyncio

from fastapi import FastAPI

from service_b_logger.consumer import ConsumerService

app = FastAPI()

async def main():
    consumer = ConsumerService()
    await consumer.consume()

if __name__ == '__main__':
    asyncio.run(main())