#!/bin/sh
set -e

# Stelle sicher, dass das data-Verzeichnis existiert
mkdir -p /app/data

# Wenn als root ausgeführt, Berechtigungen setzen und zu appuser wechseln
if [ "$(id -u)" = "0" ]; then
    chown -R appuser:appuser /app/data
    chmod 755 /app/data
    # Zu appuser wechseln und App starten (mit su)
    exec su appuser -c "$*"
else
    # Bereits als appuser, nur Verzeichnis erstellen
    exec "$@"
fi

