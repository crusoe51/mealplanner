#!/bin/sh
set -e

# Data folder (Render /tmp/)
mkdir -p /tmp/data
chmod 755 /tmp/data

# GUNICORN direkt starten (kein su!)
exec gunicorn --bind 0.0.0.0:${PORT:-5000} \
    --workers 1 --threads 8 \
    --worker-class gthread \
    --timeout 120 \
    "app:app"
