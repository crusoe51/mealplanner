# Sofortige Lösung: Backend-Verbindung beheben

## Problem
Frontend kann Backend nicht erreichen: `ERR_CONNECTION_REFUSED`

## Schnellste Lösung: Explizite API-URL setzen

### Schritt 1: docker-compose.yml anpassen

Öffne `docker-compose.yml` und ändere den Frontend-Build:

```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
    args:
      VITE_API_URL: http://192.168.178.65:5000/api
```

**Wichtig:** `args` muss ein Mapping sein (key: value), nicht eine Liste!

### Schritt 2: Frontend neu bauen

```bash
# Container stoppen
docker compose down

# Frontend neu bauen
docker compose build frontend

# Container starten
docker compose up -d
```

### Schritt 3: Prüfen

1. Browser: `http://192.168.178.65:8086`
2. F12 → Console: Sollte zeigen `📦 Using build-time API URL: http://192.168.178.65:5000/api`
3. Network-Tab: Requests sollten an `http://192.168.178.65:5000/api` gehen

## Alternative: Nginx-Proxy verwenden

Falls du den Nginx-Proxy verwenden möchtest (empfohlen):

### Schritt 1: docker-compose.yml anpassen

```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
    # Keine args - verwendet automatisch /api (Nginx-Proxy)
```

### Schritt 2: Prüfe ob Backend erreichbar ist

```bash
# Vom Frontend-Container aus
docker compose exec frontend wget -O- http://backend:5000/api/health
```

Falls das funktioniert, sollte der Nginx-Proxy auch funktionieren.

### Schritt 3: Frontend neu bauen

```bash
docker compose build frontend
docker compose up -d
```

## Was wurde geändert

1. **Nginx-Proxy**: `/api` → `http://backend:5000/api`
2. **API-URL-Logik**: Verwendet `/api` (relative URL) für Docker
3. **Fallback**: Kann explizite URL via `VITE_API_URL` setzen

## Empfehlung

**Für sofortige Lösung**: Verwende explizite URL (Lösung 1)
**Für langfristig**: Nginx-Proxy (Lösung 2) - funktioniert unabhängig von IP

