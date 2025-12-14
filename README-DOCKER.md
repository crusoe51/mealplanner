# Mealplanner - Docker Installation für Raspberry Pi 4

Diese Anleitung beschreibt, wie du die Mealplanner-App auf einem Raspberry Pi 4 mit Docker installierst.

## Voraussetzungen

- Raspberry Pi 4 (empfohlen: 4GB RAM oder mehr)
- Raspberry Pi OS (64-bit empfohlen) oder Ubuntu
- Docker und Docker Compose installiert

## Docker Installation auf Raspberry Pi

### 1. Docker installieren

```bash
# Docker installieren
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Docker Compose installieren
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Benutzer zur docker-Gruppe hinzufügen (optional, um sudo zu vermeiden)
sudo usermod -aG docker $USER
# Danach neu einloggen oder: newgrp docker
```

### 2. Projekt auf Raspberry Pi kopieren

```bash
# Via Git (wenn Repository vorhanden)
git clone <dein-repo-url> mealplanner
cd mealplanner

# Oder via SCP von deinem PC:
# scp -r mealplanner pi@raspberry-pi-ip:/home/pi/
```

### 3. Installation starten

```bash
# Im Projektverzeichnis
cd mealplanner

# Docker Images bauen (kann bei Raspberry Pi etwas länger dauern)
docker compose build

# Container starten
docker compose up -d

# Logs anzeigen
docker compose logs -f
```

### 4. App aufrufen

- **Frontend**: `http://raspberry-pi-ip` oder `http://localhost`
- **Backend API**: `http://raspberry-pi-ip:5000/api`

## Konfiguration

### API URL anpassen

Wenn das Frontend auf einem anderen Gerät läuft als das Backend, musst du die API URL anpassen:

1. **Zur Build-Zeit** (empfohlen für Production):
   ```bash
   # In docker-compose.yml die VITE_API_URL anpassen
   # Dann neu bauen:
   docker compose build frontend
   docker compose up -d
   ```

2. **Zur Laufzeit** (für Entwicklung):
   - Die API URL wird aus `import.meta.env.VITE_API_URL` gelesen
   - Standard: `http://localhost:5000/api`

### Datenbank persistieren

Die SQLite-Datenbank wird automatisch im `backend/data/` Verzeichnis gespeichert und bleibt auch nach Container-Neustarts erhalten.

## Wartung

### Container stoppen
```bash
docker compose down
```

### Container neu starten
```bash
docker compose restart
```

### Logs anzeigen
```bash
# Alle Logs
docker compose logs

# Nur Backend
docker compose logs backend

# Nur Frontend
docker compose logs frontend

# Live-Logs
docker compose logs -f
```

### Container aktualisieren
```bash
# Code aktualisieren (z.B. via git pull)
git pull

# Neu bauen und starten
docker compose build
docker compose up -d
```

### Datenbank-Backup
```bash
# Backup erstellen
cp backend/data/meals.db backend/data/meals.db.backup

# Oder mit Docker
docker compose exec backend cp /app/data/meals.db /app/data/meals.db.backup
```

## Troubleshooting

### Container startet nicht
```bash
# Logs prüfen
docker compose logs

# Container-Status prüfen
docker compose ps

# Images prüfen
docker images
```

### Port bereits belegt
```bash
# Ports prüfen
sudo netstat -tulpn | grep :5000
sudo netstat -tulpn | grep :80

# In docker-compose.yml Ports ändern, z.B.:
# ports:
#   - "5001:5000"  # Backend auf Port 5001
#   - "8080:80"    # Frontend auf Port 8080
```

### ARM64 Kompatibilität
Die Dockerfiles sind für ARM64 (Raspberry Pi 4) optimiert. Falls Probleme auftreten:

```bash
# Platform explizit setzen
docker compose build --platform linux/arm64
```

### Performance-Optimierungen

Für bessere Performance auf Raspberry Pi:

1. **Docker Build Cache nutzen**:
   ```bash
   docker compose build --parallel
   ```

2. **Ressourcen begrenzen** (in docker-compose.yml):
   ```yaml
   services:
     backend:
       deploy:
         resources:
           limits:
             cpus: '1.0'
             memory: 512M
   ```

## Automatischer Start beim Booten

Docker Compose startet Container standardmäßig mit `restart: unless-stopped` automatisch neu.

Für systemd Service (optional):

```bash
# Service-Datei erstellen
sudo nano /etc/systemd/system/mealplanner.service
```

Inhalt:
```ini
[Unit]
Description=Mealplanner Docker Compose
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/pi/mealplanner
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Aktivieren:
```bash
sudo systemctl enable mealplanner.service
sudo systemctl start mealplanner.service
```

## Sicherheit

- Die App läuft standardmäßig nur im lokalen Netzwerk
- Für Internet-Zugriff: Reverse Proxy (z.B. Nginx) mit SSL/TLS einrichten
- Firewall-Regeln setzen
- Regelmäßige Updates durchführen

## Support

Bei Problemen:
1. Logs prüfen: `docker compose logs`
2. Container-Status: `docker compose ps`
3. Docker-Version: `docker --version`
4. System-Info: `uname -a`

