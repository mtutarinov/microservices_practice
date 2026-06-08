# service_a_user/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Копируем общие модули (app) и код сервиса A
COPY app ./app
COPY service_a_user ./service_a_user

# Копируем requirements (можно общий, или отдельный)
COPY service_a_user/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Запуск через uvicorn (FastAPI)
CMD ["uvicorn", "service_a_user.main:app", "--host", "0.0.0.0", "--port", "8000"]