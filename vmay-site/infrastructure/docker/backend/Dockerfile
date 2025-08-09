FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./pkg /app/pkg
COPY ./photo /app/photo
COPY ./infrastructure/apps/env_files /app/infrastructure/apps/env_files
COPY ./infrastructure/deployment/entrypoints /app/infrastructure/deployment/entrypoints
COPY ./infrastructure/requirements/app.txt /app/infrastructure/requirements/app.txt

RUN pip install --no-cache-dir -r /app/infrastructure/requirements/app.txt

RUN chmod +x /app/infrastructure/deployment/entrypoints/*.sh

ENTRYPOINT ["./infrastructure/deployment/entrypoints/app_entrypoint.sh"]
