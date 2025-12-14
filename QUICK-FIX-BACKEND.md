# Schnelle Lösung: Backend-Verbindung

## Problem: ERR_CONNECTION_REFUSED

### Lösung 1: Frontend mit expliziter API-URL neu bauen

```bash
# 1. docker-compose.yml öffnen und ändern:
#    frontend:
#      build:
#        args:
#          - VITE_API_URL=http://192.168.178.65:5000/api

# 2. Frontend neu bauen
docker compose build frontend

# 3. Container neu starten
docker compose up -d
```

### Lösung 2: Nginx-Proxy testen

```bash
# Prüfe ob Proxy funktioniert
curl http://192.168.178.65:8086/api/health

# Falls Fehler: Backend-Name im Docker-Netzwerk prüfen
docker compose exec frontend ping backend
```

### Lösung 3: Container-Netzwerk prüfen

```bash
# Beide Container sollten im gleichen Netzwerk sein
docker network inspect mealplanner-mealplanner-network

# Sollte beide Container zeigen: backend und frontend
```

### Lösung 4: Nginx-Konfiguration neu laden

```bash
# Frontend-Container neu starten
docker compose restart frontend

# Oder Nginx-Konfiguration testen
docker compose exec frontend nginx -t
```

## Debugging

```bash
# 1. Welche URL verwendet das Frontend?
#    Browser-Konsole: Sollte "/api" zeigen

# 2. Geht der Request raus?
#    Browser Network-Tab: Request an /api/health

# 3. Kommt er beim Backend an?
#    docker compose logs backend

# 4. Kommt er beim Nginx an?
#    docker compose logs frontend
```

