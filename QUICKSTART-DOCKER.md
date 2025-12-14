# Quick Start - Docker auf Raspberry Pi

## Schnellstart

```bash
# 1. Docker installieren (falls noch nicht vorhanden)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt-get install docker-compose-plugin

# 2. Projektverzeichnis
cd mealplanner

# 3. Build und Start
docker compose build
docker compose up -d

# 4. App öffnen
# Frontend: http://raspberry-pi-ip
# Backend: http://raspberry-pi-ip:5000/api
```

## Wichtige Befehle

```bash
# Status prüfen
docker compose ps

# Logs anzeigen
docker compose logs -f

# Stoppen
docker compose down

# Neu starten
docker compose restart

# Aktualisieren
git pull
docker compose build
docker compose up -d
```

## API URL anpassen

Wenn Frontend und Backend auf verschiedenen Geräten laufen:

1. In `docker-compose.yml` die `VITE_API_URL` anpassen
2. Frontend neu bauen: `docker compose build frontend`
3. Container neu starten: `docker compose up -d`

## Datenbank-Backup

```bash
# Backup
cp backend/data/meals.db backend/data/meals.db.backup

# Restore
cp backend/data/meals.db.backup backend/data/meals.db
```

