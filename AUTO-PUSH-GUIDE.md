# Automatisches Git Push - Anleitung

Es gibt mehrere Möglichkeiten, Commits automatisch zu pushen:

## Option 1: Git Alias (Einfachste Lösung)

### Einrichten
```bash
git config alias.ap '!f() { git add -A && git commit -m "$1" && git push; }; f'
```

### Verwendung
```bash
git ap "Deine Commit-Nachricht"
```

Dies führt automatisch aus:
1. `git add -A` (alle Änderungen hinzufügen)
2. `git commit -m "..."` (committen)
3. `git push` (pushen)

## Option 2: PowerShell-Funktion (Windows)

### Einrichten
Führe das Script aus:
```powershell
.\setup-auto-push-ps.ps1
```

Oder manuell zu deinem PowerShell-Profil hinzufügen:
```powershell
# Profil öffnen
notepad $PROFILE

# Diese Funktion hinzufügen:
function Git-AutoPush {
    param([string]$Message)
    if (-not $Message) {
        $Message = Read-Host "Commit-Nachricht"
    }
    git add -A
    git commit -m "$Message"
    git push
}

Set-Alias -Name gap -Value Git-AutoPush
```

### Verwendung
```powershell
gap "Deine Commit-Nachricht"
# oder
Git-AutoPush "Deine Commit-Nachricht"
```

## Option 3: Git Hook (Post-Commit)

### Einrichten
```bash
# Script ausführen
.\setup-auto-push.ps1

# Oder manuell:
# .git/hooks/post-commit erstellen (siehe Beispiel unten)
```

**Hinweis:** Git Hooks funktionieren auf Windows am besten mit Git Bash.

### Hook-Inhalt (.git/hooks/post-commit)
```bash
#!/bin/sh
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if git remote | grep -q "^origin$"; then
    echo "Auto-pushing to origin/$BRANCH..."
    git push origin "$BRANCH"
fi
```

Hook ausführbar machen:
```bash
chmod +x .git/hooks/post-commit
```

### Verhalten
- Pusht automatisch nach jedem `git commit`
- Funktioniert nur, wenn Remote konfiguriert ist

## Option 4: GitHub Actions / GitLab CI (Cloud)

Für automatische Aktionen nach Push siehe:
- GitHub Actions: `.github/workflows/`
- GitLab CI: `.gitlab-ci.yml`

## Vergleich der Optionen

| Option | Vorteile | Nachteile |
|--------|----------|-----------|
| **Git Alias** | Einfach, funktioniert überall | Manuell aufrufen |
| **PowerShell-Funktion** | Windows-nativ, einfach | Nur PowerShell |
| **Git Hook** | Vollautomatisch | Funktioniert am besten mit Git Bash |
| **CI/CD** | Professionell, erweiterbar | Komplexer Setup |

## Empfehlung

**Für Windows/PowerShell:** Option 2 (PowerShell-Funktion)
- Einfach zu verwenden
- Funktioniert zuverlässig
- Kontrolle über wann gepusht wird

**Für automatisches Pushen:** Option 3 (Git Hook)
- Pusht nach jedem Commit
- Keine manuellen Schritte nötig

## Sicherheitshinweise

⚠️ **Wichtig:**
- Automatisches Pushen kann problematisch sein, wenn du noch nicht bereit bist zu pushen
- Prüfe deine Änderungen vor dem Push
- Verwende `git push --dry-run` zum Testen
- Für wichtige Branches: Deaktiviere Auto-Push

## Deaktivieren

### Git Alias entfernen
```bash
git config --unset alias.ap
```

### PowerShell-Funktion entfernen
```powershell
# Aus Profil entfernen
notepad $PROFILE
# Funktion löschen
```

### Git Hook entfernen
```bash
rm .git/hooks/post-commit
```

## Troubleshooting

### "Remote not found"
```bash
# Remote hinzufügen
git remote add origin <url>
```

### "Permission denied"
- Prüfe deine Git-Credentials
- Bei GitHub: Personal Access Token verwenden

### Hook funktioniert nicht (Windows)
- Verwende Git Bash statt PowerShell
- Oder nutze die PowerShell-Funktion (Option 2)

