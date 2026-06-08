# service_b_logger/Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app ./app
COPY service_b_logger ./service_b_logger
COPY service_b_logger/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Запуск consumer.py (основная функция)
CMD ["python", "-m", "service_b_logger.main"]