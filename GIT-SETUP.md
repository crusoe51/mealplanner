# Git Repository Setup

## Repository auf GitHub/GitLab erstellen

### Option 1: GitHub

1. Gehe zu [github.com](https://github.com) und logge dich ein
2. Klicke auf "New repository" (oder "+" → "New repository")
3. Repository-Name: z.B. `mealplanner`
4. Beschreibung: "Wochenplaner für Mahlzeiten"
5. Wähle **Public** oder **Private**
6. **WICHTIG**: Lasse "Initialize this repository with a README" **NICHT** angehakt
7. Klicke auf "Create repository"

### Option 2: GitLab

1. Gehe zu [gitlab.com](https://gitlab.com) und logge dich ein
2. Klicke auf "New project" → "Create blank project"
3. Projektname: z.B. `mealplanner`
4. Wähle **Public** oder **Private**
5. **WICHTIG**: Lasse "Initialize repository with a README" **NICHT** angehakt
6. Klicke auf "Create project"

## Lokales Repository mit Remote verbinden

### 1. Ersten Commit erstellen

```bash
# Im Projektverzeichnis
cd C:\Users\mikra\MK\prog\mealplanner

# Ersten Commit erstellen
git commit -m "Initial commit: Mealplanner App"
```

### 2. Remote Repository hinzufügen

**Für GitHub:**
```bash
# Ersetze <dein-username> und <repository-name>
git remote add origin https://github.com/<dein-username>/<repository-name>.git

# Beispiel:
# git remote add origin https://github.com/mikra/mealplanner.git
```

**Für GitLab:**
```bash
# Ersetze <dein-username> und <repository-name>
git remote add origin https://gitlab.com/<dein-username>/<repository-name>.git

# Beispiel:
# git remote add origin https://gitlab.com/mikra/mealplanner.git
```

### 3. Code hochladen

```bash
# Branch umbenennen (optional, aber empfohlen)
git branch -M main

# Code hochladen
git push -u origin main
```

## Authentifizierung

### GitHub

**Option 1: Personal Access Token (empfohlen)**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token" → "Generate new token (classic)"
3. Scopes: `repo` auswählen
4. Token kopieren
5. Beim `git push` wird nach Username und Password gefragt:
   - Username: dein GitHub-Username
   - Password: der generierte Token

**Option 2: GitHub CLI**
```bash
# GitHub CLI installieren
winget install GitHub.cli

# Authentifizieren
gh auth login

# Dann normal pushen
git push -u origin main
```

**Option 3: SSH (für fortgeschrittene)**
```bash
# SSH Key generieren (falls noch nicht vorhanden)
ssh-keygen -t ed25519 -C "deine-email@example.com"

# Public Key zu GitHub hinzufügen
# GitHub → Settings → SSH and GPG keys → New SSH key

# Remote URL ändern
git remote set-url origin git@github.com:<username>/<repository>.git
```

### GitLab

Ähnlich wie GitHub, Personal Access Token oder SSH verwenden.

## Nächste Schritte

### Weitere Commits

```bash
# Änderungen hinzufügen
git add .

# Commit erstellen
git commit -m "Beschreibung der Änderungen"

# Hochladen
git push
```

### Branch erstellen

```bash
# Neuen Branch erstellen
git checkout -b feature/neue-funktion

# Änderungen committen
git add .
git commit -m "Neue Funktion hinzugefügt"

# Branch hochladen
git push -u origin feature/neue-funktion
```

### Status prüfen

```bash
# Status anzeigen
git status

# Änderungen anzeigen
git diff

# Commit-Historie
git log
```

## Wichtige Dateien

Die folgenden Dateien werden **NICHT** ins Repository hochgeladen (dank .gitignore):

- `venv/` - Python Virtual Environment
- `node_modules/` - Node.js Dependencies
- `*.db` - Datenbankdateien
- `__pycache__/` - Python Cache
- `.env` - Environment Variables

## Troubleshooting

### "Repository not found"
- Prüfe, ob der Repository-Name korrekt ist
- Prüfe, ob du Zugriff auf das Repository hast

### "Authentication failed"
- Prüfe deine Credentials
- Bei GitHub: Verwende Personal Access Token statt Passwort

### "Permission denied"
- Prüfe, ob du Schreibrechte auf das Repository hast
- Bei privaten Repositories: Prüfe die Zugriffsrechte

### Dateien werden nicht ignoriert
```bash
# .gitignore prüfen
cat .gitignore

# Bereits getrackte Dateien entfernen
git rm -r --cached venv/
git rm -r --cached node_modules/
git commit -m "Remove ignored files"
```


