FROM python:3.11-slim

WORKDIR /code

# System deps
RUN apt-get update && apt-get install -y \
    curl gcc g++ && \
    rm -rf /var/lib/apt/lists/*

# Python deps (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app/ ./app/

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000 || exit 1

# Production server
EXPOSE 8000
CMD ["gunicorn", "app.app:app", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "--worker-class", "uvicorn.workers.UvicornWorker"]
