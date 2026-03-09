# Setup für Raspberry Pi (192.168.178.65)

## Aktuelle Konfiguration

- **Frontend**: http://192.168.178.65:8086
- **Backend**: http://192.168.178.65:5000

## Installation

### 1. Code auf Raspberry Pi

```bash
# Via Git
git clone <dein-repo-url> mealplanner
cd mealplanner

# Oder Code manuell kopieren
```

### 2. Container bauen und starten

**Option A: Automatische URL-Erkennung (empfohlen)**

```bash
# Standard docker-compose.yml verwenden
docker compose build
docker compose up -d
```

Die App erkennt automatisch die IP-Adresse aus der Browser-URL.

**Option B: Explizite IP-Konfiguration**

```bash
# Lokale Konfiguration verwenden
docker compose -f docker-compose.local.yml build
docker compose -f docker-compose.local.yml up -d
```

### 3. Prüfen

```bash
# Container-Status
docker compose ps

# Logs
docker compose logs -f backend
docker compose logs -f frontend

# Backend-Health prüfen
curl http://192.168.178.65:5000/api/health
```

### 4. App öffnen

Im Browser: **http://192.168.178.65:8086**

## Troubleshooting

### Backend nicht erreichbar

1. **Browser-Konsole prüfen (F12)**
   - Network-Tab: Welche URL wird verwendet?
   - Console: Gibt es CORS-Fehler?

2. **API-URL prüfen**
   - Sollte sein: `http://192.168.178.65:5000/api`
   - Falls nicht: Frontend neu bauen mit expliziter URL

3. **Frontend neu bauen mit expliziter URL**

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

### CORS-Fehler

CORS ist bereits aktiviert in `backend/app.py`:
```python
CORS(app)
```

Falls weiterhin Probleme:
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### Ports prüfen

```bash
# Welche Ports sind offen?
sudo netstat -tulpn | grep -E ':(5000|8086)'

# Firewall-Regeln (falls nötig)
sudo ufw allow 5000/tcp
sudo ufw allow 8086/tcp
```

## Automatische URL-Erkennung

Die App erkennt automatisch die Backend-URL:
- Wenn auf `http://192.168.178.65:8086` → Backend: `http://192.168.178.65:5000/api`
- Wenn auf `localhost:8086` → Backend: `http://localhost:5000/api`

Falls die automatische Erkennung nicht funktioniert, verwende `docker-compose.local.yml` mit expliziter URL.

## Update

```bash
# Code aktualisieren
git pull

# Container neu bauen
docker compose build

# Container neu starten
docker compose up -d
```

