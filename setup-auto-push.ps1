# PowerShell Script zum Aktivieren von Auto-Push
# Führe aus: .\setup-auto-push.ps1

Write-Host "Git Auto-Push Setup" -ForegroundColor Green
Write-Host "====================" -ForegroundColor Green
Write-Host ""

# Prüfe ob Git-Repository existiert
if (-not (Test-Path .git)) {
    Write-Host "Fehler: Kein Git-Repository gefunden!" -ForegroundColor Red
    exit 1
}

# Prüfe ob Remote existiert
$remote = git remote get-url origin 2>$null
if (-not $remote) {
    Write-Host "Warnung: Kein Remote 'origin' konfiguriert!" -ForegroundColor Yellow
    Write-Host "Bitte zuerst Remote hinzufügen:" -ForegroundColor Yellow
    Write-Host "  git remote add origin <url>" -ForegroundColor Yellow
    exit 1
}

Write-Host "Remote gefunden: $remote" -ForegroundColor Green
Write-Host ""

# Optionen anzeigen
Write-Host "Wähle eine Option:" -ForegroundColor Cyan
Write-Host "1. Post-Commit Hook (pusht nach jedem Commit)" -ForegroundColor White
Write-Host "2. Pre-Push Hook (pusht vor jedem manuellen Push)" -ForegroundColor White
Write-Host "3. Beide" -ForegroundColor White
Write-Host "4. Abbrechen" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Deine Wahl (1-4)"

switch ($choice) {
    "1" {
        # Post-Commit Hook erstellen
        $hookContent = @"
#!/bin/sh
# Automatisches Pushen nach jedem Commit
BRANCH=`$(git rev-parse --abbrev-ref HEAD)
if git remote | grep -q "^origin`$"; then
    echo "Auto-pushing to origin/`$BRANCH..."
    git push origin "`$BRANCH"
fi
"@
        $hookContent | Out-File -FilePath .git/hooks/post-commit -Encoding UTF8 -NoNewline
        Write-Host "Post-Commit Hook erstellt!" -ForegroundColor Green
    }
    "2" {
        # Pre-Push Hook erstellen (wird automatisch ausgeführt)
        Write-Host "Pre-Push Hook wird automatisch ausgeführt, wenn du 'git push' verwendest." -ForegroundColor Yellow
        Write-Host "Keine zusätzliche Konfiguration nötig." -ForegroundColor Yellow
    }
    "3" {
        # Beide erstellen
        $hookContent = @"
#!/bin/sh
# Automatisches Pushen nach jedem Commit
BRANCH=`$(git rev-parse --abbrev-ref HEAD)
if git remote | grep -q "^origin`$"; then
    echo "Auto-pushing to origin/`$BRANCH..."
    git push origin "`$BRANCH"
fi
"@
        $hookContent | Out-File -FilePath .git/hooks/post-commit -Encoding UTF8 -NoNewline
        Write-Host "Post-Commit Hook erstellt!" -ForegroundColor Green
    }
    "4" {
        Write-Host "Abgebrochen." -ForegroundColor Yellow
        exit 0
    }
    default {
        Write-Host "Ungültige Auswahl!" -ForegroundColor Red
        exit 1
    }
}

# Hook ausführbar machen (für Git Bash)
if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host ""
    Write-Host "Hinweis: Auf Windows funktioniert der Hook nur mit Git Bash." -ForegroundColor Yellow
    Write-Host "Für PowerShell siehe: setup-auto-push-ps.ps1" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setup abgeschlossen!" -ForegroundColor Green

