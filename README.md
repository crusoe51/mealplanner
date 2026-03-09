# Mealplanner

Eine moderne Web-Anwendung zur Planung von Mahlzeiten für die Woche.

## Features

- 📅 Wochenplan-Ansicht mit Drag & Drop
- 🍽️ Gerichte-Verwaltung mit Farbzuordnung
- 🔄 Mehrere Wochen gleichzeitig anzeigen
- 📱 Responsive Design
- 🐳 Docker-Support für Raspberry Pi

## Tech Stack

- **Backend**: Python 3.11, Flask, SQLite
- **Frontend**: Vue.js 3, Vite, Tailwind CSS
- **Deployment**: Docker, Docker Compose

## Installation

### Lokale Entwicklung

#### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app.py
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker (Raspberry Pi)

Siehe [README-DOCKER.md](README-DOCKER.md) für detaillierte Anleitung.

```bash
docker compose build
docker compose up -d
```

## Verwendung

1. **Gerichte verwalten**: Klicke auf "Gerichte" in der Navigation
2. **Gericht erstellen**: Klicke auf "+ Neues Gericht"
3. **Wochenplan füllen**: Ziehe Gerichte aus dem Pool in die Tageszellen
4. **Gericht verschieben**: Ziehe ein Gericht von einem Tag zu einem anderen
5. **Gericht löschen**: Hover über ein Gericht und klicke auf das X

## Projektstruktur

```
mealplanner/
├── backend/          # Flask API
│   ├── app.py       # Hauptanwendung
│   ├── database.py  # Datenbanklogik
│   └── data/        # SQLite Datenbank
├── frontend/         # Vue.js Frontend
│   ├── src/
│   │   ├── components/  # Vue Komponenten
│   │   ├── views/      # Views
│   │   └── api/        # API Client
│   └── package.json
└── docker-compose.yml
```

## API Endpunkte

- `GET /api/meals` - Alle Gerichte abrufen
- `POST /api/meals` - Neues Gericht erstellen
- `PUT /api/meals/<id>` - Gericht aktualisieren
- `DELETE /api/meals/<id>` - Gericht löschen
- `GET /api/plan/<year>/<week>` - Wochenplan abrufen
- `PUT /api/plan/<year>/<week>/<day>` - Gericht für Tag setzen
- `DELETE /api/plan/<year>/<week>/<day>` - Gericht für Tag löschen

## Entwicklung

### Backend starten
```bash
cd backend
python app.py
# Läuft auf http://localhost:5000
```

### Frontend starten
```bash
cd frontend
npm run dev
# Läuft auf http://localhost:5173
```

## Lizenz

MIT


