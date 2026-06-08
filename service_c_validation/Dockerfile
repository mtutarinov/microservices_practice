# service_c_validation/Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app ./app
COPY service_c_validation ./service_c_validation
COPY service_c_validation/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

CMD ["uvicorn", "service_c_validation.main:app", "--host", "0.0.0.0", "--port", "8001"]