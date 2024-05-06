FROM python:3.10-slim

ENV SERVICE_PORT 8080
ENV PYTHONUNBUFFERED 1
ENV UVICORN_OPTS ''

RUN apt-get update && apt-get upgrade -y
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD uvicorn runapp:app ${UVICORN_OPTS} --host 0.0.0.0 --port ${SERVICE_PORT}