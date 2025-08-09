FROM python:3.10-slim

WORKDIR /app

COPY bot_service/ ./bot_service
COPY shared/ ./shared

RUN pip install -r ./bot_service/requirements.txt

ENV PYTHONPATH="/app"

CMD ["python", "./bot_service/main.py"]
