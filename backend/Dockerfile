FROM python:3.11-slim-buster

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry && poetry install --no-root --only main

COPY app /app

RUN apt-get update && \
    apt-get install -y python3-dev gcc && \
    rm -rf /var/lib/apt/lists/*

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]