# Render Flask Mealplanner (ex-Raspberry Pi)
FROM python:3.12-slim

# Labels für Render Dashboard
LABEL maintainer="crusoe51@mealplanner"
LABEL description="Meal Planner Flask App"

WORKDIR /app

# System deps (falls Pi-spezifisch: gcc, lib etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python deps (cache-optimiert)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Source
COPY . .

# Render PORT (10000-65535)
ENV PORT=${PORT:-5000}
EXPOSE $PORT

# Healthcheck (Render liebt das)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s \
  CMD curl -f http://localhost:${PORT}/health || exit 1

# Shell CMD für $PORT Expansion
CMD sh -c "gunicorn --bind 0.0.0.0:$${PORT:-10000} \
    --workers 1 --threads 8 \
    --worker-class gthread \
    --timeout 120 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    app:app"

