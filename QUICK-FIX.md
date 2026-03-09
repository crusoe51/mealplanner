# Schnelle Lösung für Datenbank-Berechtigungen

## Problem beheben (auf Raspberry Pi)

```bash
# 1. Container stoppen
docker compose down

# 2. Data-Verzeichnis erstellen und Berechtigungen setzen
mkdir -p backend/data
chmod 777 backend/data  # Temporär für ersten Start

# 3. Container neu bauen (mit aktualisiertem Dockerfile)
docker compose build backend

# 4. Container starten
docker compose up -d

# 5. Berechtigungen wieder sicherer machen (optional)
chmod 755 backend/data
```

## Alternative: Ohne Neu-Build

```bash
# Container stoppen
docker compose down

# Verzeichnis erstellen
mkdir -p backend/data
chmod 777 backend/data

# Container mit temporären Root-Rechten starten
# In docker-compose.yml ändern:
#   user: root  # Temporär hinzufügen

docker compose up -d

# Nach erfolgreichem Start wieder entfernen und neu starten
```

## Prüfen ob es funktioniert

```bash
# Logs prüfen
docker compose logs backend

# Sollte keine "unable to open database file" Fehler mehr zeigen
```

