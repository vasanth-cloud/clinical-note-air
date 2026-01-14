FROM python:3.11-slim

WORKDIR /code

# System dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /code
USER appuser

EXPOSE 8000

# FIXED: Use uvicorn directly (Render compatible)
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
