# Port-Konfiguration

## Standard-Ports

- **Frontend**: Port `8080` (Host) → Port `80` (Container)
- **Backend**: Port `5000` (Host) → Port `5000` (Container)

## Ports ändern

### Frontend-Port ändern

In `docker-compose.yml`:

```yaml
frontend:
  ports:
    - "9000:80"  # Ändere 9000 zu deinem gewünschten Port
```

**Wichtig:** Der Container-interne Port bleibt `80` (Nginx läuft intern auf Port 80).

### Backend-Port ändern

In `docker-compose.yml`:

```yaml
backend:
  ports:
    - "5001:5000"  # Ändere 5001 zu deinem gewünschten Port
```

**Wichtig:** Wenn du den Backend-Port änderst, musst du auch die API-URL im Frontend anpassen:

1. In `docker-compose.yml` die `VITE_API_URL` anpassen:
   ```yaml
   frontend:
     build:
       args:
         - VITE_API_URL=http://localhost:5001/api  # Neuer Port
   ```

2. Frontend neu bauen:
   ```bash
   docker compose build frontend
   docker compose up -d
   ```

## Port-Format

Das Format ist: `"HOST_PORT:CONTAINER_PORT"`

- **HOST_PORT**: Port auf dem Raspberry Pi (kann frei gewählt werden)
- **CONTAINER_PORT**: Port im Container (sollte nicht geändert werden)

## Beispiel: Beide Ports ändern

```yaml
services:
  backend:
    ports:
      - "5001:5000"  # Backend auf Port 5001
      
  frontend:
    build:
      args:
        - VITE_API_URL=http://localhost:5001/api  # Angepasst!
    ports:
      - "9000:80"  # Frontend auf Port 9000
```

Dann neu bauen:
```bash
docker compose build
docker compose up -d
```

App aufrufen:
- Frontend: `http://raspberry-pi-ip:9000`
- Backend: `http://raspberry-pi-ip:5001/api`

## Ports prüfen

```bash
# Welche Ports sind belegt?
sudo netstat -tulpn | grep LISTEN

# Oder mit ss:
ss -tulpn | grep LISTEN

# Docker-Container Ports anzeigen
docker compose ps
docker port mealplanner-frontend
docker port mealplanner-backend
```

## Firewall-Regeln (falls nötig)

```bash
# UFW (Ubuntu/Raspberry Pi OS)
sudo ufw allow 8080/tcp  # Frontend
sudo ufw allow 5000/tcp  # Backend

# Oder für andere Ports:
sudo ufw allow 9000/tcp  # Beispiel: Frontend auf 9000
```

## Troubleshooting

### "Port already in use"
- Port ist bereits belegt
- Lösung: Anderen Port wählen oder andere Anwendung beenden

### "Connection refused"
- Port ist nicht geöffnet
- Lösung: Firewall-Regel hinzufügen oder Port prüfen

### Frontend kann Backend nicht erreichen
- API-URL ist falsch
- Lösung: `VITE_API_URL` in docker-compose.yml anpassen und Frontend neu bauen

