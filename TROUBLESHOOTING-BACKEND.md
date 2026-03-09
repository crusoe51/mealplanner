# Troubleshooting: Backend nicht erreichbar

## Problem: ERR_CONNECTION_REFUSED

### Schritt 1: Prüfe ob Backend läuft

```bash
# Container-Status
docker compose ps

# Backend-Logs
docker compose logs backend

# Backend sollte laufen und Health-Checks zeigen
```

### Schritt 2: Prüfe ob Backend vom Host erreichbar ist

```bash
# Vom Raspberry Pi aus
curl http://localhost:5000/api/health

# Oder mit IP
curl http://192.168.178.65:5000/api/health
```

### Schritt 3: Prüfe ob Backend vom Frontend-Container erreichbar ist

```bash
# Im Frontend-Container
docker compose exec frontend wget -O- http://backend:5000/api/health

# Sollte eine JSON-Antwort zurückgeben
```

### Schritt 4: Prüfe Nginx-Proxy

```bash
# Nginx-Logs im Frontend-Container
docker compose logs frontend | grep -i error

# Nginx-Konfiguration prüfen
docker compose exec frontend cat /etc/nginx/conf.d/default.conf
```

### Schritt 5: Browser-Konsole prüfen

1. Browser öffnen: `http://192.168.178.65:8086`
2. F12 → Console
3. Sollte zeigen: `🔄 Using Nginx proxy API URL: /api`
4. Network-Tab: Welche URL wird verwendet?
   - Sollte sein: `http://192.168.178.65:8086/api/health`
   - NICHT: `http://192.168.178.65:5000/api/health`

## Lösung: Frontend neu bauen

```bash
# Container stoppen
docker compose down

# Frontend neu bauen (mit neuer API-URL-Logik)
docker compose build frontend

# Container starten
docker compose up -d

# Logs prüfen
docker compose logs -f
```

## Alternative: Explizite API-URL setzen

Falls der Nginx-Proxy nicht funktioniert:

1. In `docker-compose.yml`:
```yaml
frontend:
  build:
    args:
      - VITE_API_URL=http://192.168.178.65:5000/api
```

2. Frontend neu bauen:
```bash
docker compose build frontend
docker compose up -d
```

## Nginx-Proxy testen

```bash
# Vom Host aus
curl http://192.168.178.65:8086/api/health

# Sollte die gleiche Antwort wie direktes Backend geben
curl http://192.168.178.65:5000/api/health
```

## CORS prüfen

Falls direkte Verbindung verwendet wird, CORS muss aktiviert sein:

```python
# backend/app.py
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

## Firewall prüfen

```bash
# Ports prüfen
sudo netstat -tulpn | grep -E ':(5000|8086)'

# Firewall-Regeln (falls nötig)
sudo ufw allow 5000/tcp
sudo ufw allow 8086/tcp
```

