# Lösung: Backend-Verbindung beheben

## Problem
- Backend per curl erreichbar ✅
- Browser zeigt ERR_CONNECTION_REFUSED ❌
- Frontend verwendet wahrscheinlich falsche URL

## Lösung: Explizite API-URL setzen

### Schritt 1: docker-compose.yml anpassen

**Öffne `docker-compose.yml` und ändere:**

```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
    args:
      VITE_API_URL: http://192.168.178.65:5000/api
```

### Schritt 2: Frontend neu bauen (OHNE Cache)

```bash
# Container stoppen
docker compose down

# Frontend neu bauen (ohne Cache, um sicherzustellen dass alles neu ist)
docker compose build frontend --no-cache

# Container starten
docker compose up -d
```

### Schritt 3: Prüfen

1. **Browser öffnen**: `http://192.168.178.65:8086`
2. **F12 → Console**: Sollte zeigen:
   ```
   📦 Using build-time API URL: http://192.168.178.65:5000/api
   🔗 API URL: http://192.168.178.65:5000/api
   ```
3. **F12 → Network-Tab**: 
   - Requests sollten an `http://192.168.178.65:5000/api/health` gehen
   - Status sollte 200 sein (nicht ERR_CONNECTION_REFUSED)

## Alternative: Nginx-Proxy testen

Falls du den Nginx-Proxy verwenden möchtest:

### Schritt 1: Prüfe ob Backend vom Frontend-Container erreichbar ist

```bash
docker compose exec frontend wget -O- http://backend:5000/api/health
```

**Falls das funktioniert**, sollte der Nginx-Proxy auch funktionieren.

### Schritt 2: Nginx-Proxy testen

```bash
# Vom Raspberry Pi aus
curl http://localhost:8086/api/health

# Sollte die gleiche Antwort geben wie:
curl http://localhost:5000/api/health
```

### Schritt 3: Frontend neu bauen

```bash
# Entferne args aus docker-compose.yml (damit /api verwendet wird)
docker compose build frontend --no-cache
docker compose up -d
```

## Warum funktioniert es nicht?

Mögliche Ursachen:
1. **Frontend wurde nicht neu gebaut** → Lösung: `--no-cache` verwenden
2. **Nginx-Proxy funktioniert nicht** → Lösung: Explizite URL verwenden
3. **Browser-Cache** → Lösung: Hard Reload (Strg+Shift+R)

## Debugging

```bash
# 1. Welche URL verwendet das Frontend?
#    Browser Console: Suche nach "🔗 API URL"

# 2. Geht der Request raus?
#    Browser Network-Tab: Welche URL wird verwendet?

# 3. Kommt er beim Backend an?
#    docker compose logs backend | tail -20

# 4. Kommt er beim Nginx an?
#    docker compose logs frontend | tail -20
```

