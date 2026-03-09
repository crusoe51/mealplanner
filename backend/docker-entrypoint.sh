#!/bin/sh
set -e

# DB erstellen
mkdir -p /tmp/data
chmod 755 /tmp/data

# PORT fix (Render setzt es)
export PORT=${PORT:-10000}
echo "Starting on PORT $PORT"

# Gunicorn mit Shell Expansion
exec gunicorn --bind "0.0.0.0:$PORT" \
    --workers 1 --threads 8 \
    --worker-class gthread \
    --timeout 120 \
    app:app
