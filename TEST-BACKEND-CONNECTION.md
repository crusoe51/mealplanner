# Backend-Verbindung testen

## Schritt 1: Prüfe ob Backend läuft

```bash
# Container-Status
docker compose ps

# Backend sollte "Up" sein
```

## Schritt 2: Teste Backend direkt

```bash
# Vom Raspberry Pi aus
curl http://localhost:5000/api/health

# Sollte zurückgeben: {"status":"ok"}
```

## Schritt 3: Teste Nginx-Proxy

```bash
# Vom Raspberry Pi aus
curl http://localhost:8086/api/health

# Sollte die gleiche Antwort wie Schritt 2 geben
```

## Schritt 4: Teste vom Frontend-Container aus

```bash
# Backend-Erreichbarkeit im Docker-Netzwerk
docker compose exec frontend wget -O- http://backend:5000/api/health

# Sollte JSON zurückgeben
```

## Schritt 5: Browser-Konsole prüfen

1. Browser öffnen: `http://192.168.178.65:8086`
2. F12 → Console
3. Sollte zeigen: `🔄 Using Nginx proxy API URL: /api`
4. F12 → Network-Tab
5. Request an `/api/health` sollte gehen
6. Status sollte 200 sein (nicht ERR_CONNECTION_REFUSED)

## Falls Nginx-Proxy nicht funktioniert

### Option A: Frontend neu bauen

```bash
docker compose down
docker compose build frontend
docker compose up -d
```

### Option B: Direkte URL verwenden

In `docker-compose.yml` ändern:
```yaml
frontend:
  build:
    args:
      - VITE_API_URL=http://192.168.178.65:5000/api
```

Dann:
```bash
docker compose build frontend
docker compose up -d
```

## Nginx-Logs prüfen

```bash
# Frontend-Logs
docker compose logs frontend

# Sollte keine Fehler zeigen
# Falls "upstream" Fehler: Backend ist nicht erreichbar
```

## Backend-Logs prüfen

```bash
docker compose logs backend

# Sollte Requests zeigen, wenn Frontend versucht zu verbinden
```

