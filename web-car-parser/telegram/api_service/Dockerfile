FROM python:3.10-slim

WORKDIR /app

COPY api_service/ ./api_service
COPY shared/ ./shared

RUN pip install -r ./api_service/requirements.txt

ENV PYTHONPATH="/app"

RUN chmod +x ./api_service/init.sh

ENTRYPOINT ["/app/api_service/init.sh"]
