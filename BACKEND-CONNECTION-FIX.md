# Backend-Verbindungsproblem beheben

## Problem
Frontend meldet "Backend nicht erreichbar", obwohl Backend läuft.

## Ursache
Das Frontend versucht, `http://localhost:5000/api` zu erreichen. Im Browser ist `localhost` der Computer des Benutzers, nicht der Raspberry Pi.

## Lösung

Die API-URL wird jetzt automatisch aus der Browser-URL abgeleitet:
- Wenn die App auf `http://raspberry-pi-ip:8086` läuft, wird die API auf `http://raspberry-pi-ip:5000/api` verwendet
- Bei `localhost` wird `http://localhost:5000/api` verwendet

## Frontend neu bauen

Nach der Änderung muss das Frontend neu gebaut werden:

```bash
# Auf dem Raspberry Pi
cd mealplanner

# Frontend neu bauen
docker compose build frontend

# Container neu starten
docker compose up -d
```

## Alternative: Manuelle API-URL setzen

Falls die automatische Erkennung nicht funktioniert, kann die API-URL manuell gesetzt werden:

1. In `docker-compose.yml` die `VITE_API_URL` setzen:
   ```yaml
   frontend:
     build:
       args:
         - VITE_API_URL=http://raspberry-pi-ip:5000/api
   ```

2. Frontend neu bauen:
   ```bash
   docker compose build frontend
   docker compose up -d
   ```

## Prüfen

1. Browser öffnen: `http://raspberry-pi-ip:8086`
2. Browser-Konsole öffnen (F12)
3. Network-Tab prüfen: Sollten Requests an `http://raspberry-pi-ip:5000/api` gehen
4. Console prüfen: Keine CORS-Fehler

## CORS-Probleme

Falls CORS-Fehler auftreten, prüfe `backend/app.py`:
```python
CORS(app)  # Sollte vorhanden sein
```

Oder spezifischer:
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

