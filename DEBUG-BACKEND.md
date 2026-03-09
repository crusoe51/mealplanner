# Debug: Backend-Verbindung

## Problem
- Backend ist per curl erreichbar ✅
- Keine Fehler in Frontend-Logs ✅
- Browser zeigt ERR_CONNECTION_REFUSED ❌

## Schritt 1: Welche URL verwendet das Frontend?

**Im Browser:**
1. Öffne: `http://192.168.178.65:8086`
2. F12 → Console
3. Suche nach: `🔗 API URL:` oder `🔄 Using Nginx proxy API URL:`
4. **Welche URL wird angezeigt?**

## Schritt 2: Nginx-Proxy testen

```bash
# Vom Raspberry Pi aus
curl http://localhost:8086/api/health

# Sollte die gleiche Antwort wie geben:
curl http://localhost:5000/api/health
```

## Schritt 3: Browser Network-Tab prüfen

1. F12 → Network-Tab
2. Seite neu laden
3. **Welche URL wird für `/api/health` verwendet?**
   - Sollte sein: `http://192.168.178.65:8086/api/health`
   - NICHT: `http://192.168.178.65:5000/api/health`

## Schritt 4: Frontend wurde neu gebaut?

```bash
# Prüfe ob Frontend mit neuer Konfiguration gebaut wurde
docker compose build frontend --no-cache

# Container neu starten
docker compose up -d frontend
```

## Schritt 5: Nginx-Proxy-Logs prüfen

```bash
# Frontend-Logs
docker compose logs frontend | tail -50

# Suche nach "upstream" oder "backend" Fehlern
```

## Lösung: Explizite API-URL setzen

Falls der Nginx-Proxy nicht funktioniert, setze explizite URL:

**docker-compose.yml:**
```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
    args:
      VITE_API_URL: http://192.168.178.65:5000/api
```

Dann:
```bash
docker compose build frontend --no-cache
docker compose up -d
```

## Prüfe Browser-Console

Die Console sollte zeigen:
- `🔗 API URL: /api` (wenn Nginx-Proxy)
- ODER `📦 Using build-time API URL: http://192.168.178.65:5000/api` (wenn explizit gesetzt)

