# Multi-stage build für Raspberry Pi (ARM64)
FROM python:3.11-slim as builder

WORKDIR /app

# Dependencies installieren
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production image
FROM python:3.11-slim

WORKDIR /app

# Python user für Sicherheit
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/data && \
    chown -R appuser:appuser /app

# Dependencies vom builder kopieren
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

# App-Code kopieren
COPY app.py database.py ./
COPY data ./data

# Permissions setzen
RUN chown -R appuser:appuser /app

USER appuser

# Port freigeben
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/health')"

# App starten
CMD ["python", "app.py"]

