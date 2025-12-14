# Datenbank-Berechtigungen beheben

## Problem
`sqlite3.OperationalError: unable to open database file`

Dieser Fehler tritt auf, wenn:
- Das `data` Verzeichnis nicht existiert
- Falsche Berechtigungen auf dem Verzeichnis
- Volume-Mount-Probleme

## Lösung

### Option 1: Verzeichnis manuell erstellen (Schnellste Lösung)

Auf dem Raspberry Pi:

```bash
# Im Projektverzeichnis
cd mealplanner

# Data-Verzeichnis erstellen
mkdir -p backend/data

# Berechtigungen setzen
chmod 755 backend/data
chown -R $USER:$USER backend/data

# Container neu starten
docker compose down
docker compose up -d
```

### Option 2: Container mit Root-Rechten starten (Temporär)

In `docker-compose.yml` temporär ändern:

```yaml
backend:
  user: root  # Temporär für ersten Start
  volumes:
    - ./backend/data:/app/data
```

Nach dem ersten Start wieder entfernen.

### Option 3: Volume-Berechtigungen im Container setzen

```bash
# Container mit Root-Rechten starten
docker compose exec -u root backend bash

# Im Container:
mkdir -p /app/data
chown -R appuser:appuser /app/data
chmod 755 /app/data
exit

# Container neu starten
docker compose restart backend
```

### Option 4: Dockerfile wurde bereits angepasst

Das Dockerfile wurde bereits angepasst mit:
- Entrypoint-Script, das das Verzeichnis erstellt
- Korrekte Berechtigungen

**Neu bauen:**
```bash
docker compose build backend
docker compose up -d
```

## Prüfen

```bash
# Container-Logs prüfen
docker compose logs backend

# Im Container prüfen
docker compose exec backend ls -la /app/data
docker compose exec backend whoami
```

## Dauerhafte Lösung

Das aktualisierte Dockerfile mit Entrypoint-Script sollte das Problem automatisch beheben. Stelle sicher, dass:

1. Das lokale `backend/data` Verzeichnis existiert
2. Der Container neu gebaut wurde: `docker compose build backend`
3. Container neu gestartet wurde: `docker compose up -d`

