FROM python:3.10-slim

WORKDIR /app

COPY tasks/ ./tasks
COPY shared/ ./shared

RUN pip install -r ./tasks/requirements.txt

ENV PYTHONPATH="/app"

CMD ["rq", "worker", "--config", "tasks.worker"]
