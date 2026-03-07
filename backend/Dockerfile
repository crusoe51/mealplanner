# Stage 1: Frontend bauen
FROM node:20-slim AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Flask + gebautes Frontend
FROM python:3.12-slim

LABEL maintainer="crusoe51@mealplanner"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Backend Code
COPY backend/ .

# Frontend Build aus Stage 1 (dist oder build)
COPY --from=frontend-builder /frontend/dist ./static

# DB Folder
RUN mkdir -p /tmp/data

ENV PORT=10000
EXPOSE 10000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:$PORT/api/health || exit 1

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --worker-class gthread --timeout 120 app:app"]
