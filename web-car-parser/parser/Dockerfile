FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV PYTHONPATH="/app"

RUN chmod +x init.sh
ENTRYPOINT ["/app/init.sh"]
