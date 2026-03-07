# Render Flask Mealplanner (ex-Raspberry Pi)
FROM python:3.12-slim

LABEL maintainer="crusoe51@mealplanner"
LABEL description="Meal Planner Flask App"

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Source
COPY . .

# Render PORT
ENV PORT=10000
EXPOSE 10000

# Healthcheck (curl jetzt installiert)
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:$PORT/api/health || exit 1

# CMD mit korrekter $PORT Expansion (kein $$!)
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --worker-class gthread --timeout 120 app:app"]
