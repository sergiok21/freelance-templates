FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV PYTHONPATH="/app"

RUN chmod +x ./init.sh
CMD ["sh", "-c", "./init.sh"]
