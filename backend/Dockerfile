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
RUN useradd -m -u 1000 appuser

# Dependencies vom builder kopieren
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

# App-Code kopieren
COPY app.py database.py ./

# Data-Verzeichnis erstellen und Berechtigungen setzen
# Wird auch benötigt, wenn Volume gemountet wird
RUN mkdir -p /app/data && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app/data

# Entrypoint-Script kopieren und ausführbar machen
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# su ist bereits in python:slim enthalten, keine zusätzliche Installation nötig

# Als root starten, Entrypoint wechselt zu appuser
# USER appuser wird nicht gesetzt, damit Entrypoint als root Berechtigungen setzen kann

# Port freigeben
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/health')"

# Entrypoint und CMD
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["python", "app.py"]


