# PowerShell-basiertes Auto-Push (funktioniert auch auf Windows)
# Führe aus: .\setup-auto-push-ps.ps1

Write-Host "Git Auto-Push Setup (PowerShell)" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
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

# Git Alias für Auto-Push erstellen
Write-Host "Erstelle Git-Alias 'ap' (auto-push)..." -ForegroundColor Cyan
git config alias.ap '!f() { git add -A && git commit -m "$1" && git push; }; f'

Write-Host ""
Write-Host "Git-Alias erstellt!" -ForegroundColor Green
Write-Host ""
Write-Host "Verwendung:" -ForegroundColor Cyan
Write-Host "  git ap 'Commit-Nachricht'" -ForegroundColor White
Write-Host ""
Write-Host "Beispiel:" -ForegroundColor Cyan
Write-Host "  git ap 'Update README'" -ForegroundColor White
Write-Host ""
Write-Host "Dies führt automatisch aus:" -ForegroundColor Yellow
Write-Host "  1. git add -A" -ForegroundColor Gray
Write-Host "  2. git commit -m 'Commit-Nachricht'" -ForegroundColor Gray
Write-Host "  3. git push" -ForegroundColor Gray
Write-Host ""

# PowerShell-Funktion für Profile
$profileFunction = @"

# Git Auto-Push Funktion
function Git-AutoPush {
    param([string]`$Message)
    if (-not `$Message) {
        `$Message = Read-Host "Commit-Nachricht"
    }
    git add -A
    git commit -m "`$Message"
    git push
}

Set-Alias -Name gap -Value Git-AutoPush
"@

Write-Host "Möchtest du eine PowerShell-Funktion zu deinem Profil hinzufügen? (j/n)" -ForegroundColor Cyan
$addToProfile = Read-Host

if ($addToProfile -eq "j" -or $addToProfile -eq "J" -or $addToProfile -eq "y" -or $addToProfile -eq "Y") {
    $profilePath = $PROFILE
    if (-not (Test-Path $profilePath)) {
        New-Item -Path $profilePath -ItemType File -Force | Out-Null
    }
    Add-Content -Path $profilePath -Value $profileFunction
    Write-Host ""
    Write-Host "PowerShell-Funktion zum Profil hinzugefügt!" -ForegroundColor Green
    Write-Host "Verwendung: gap 'Commit-Nachricht'" -ForegroundColor Cyan
    Write-Host "Oder: Git-AutoPush 'Commit-Nachricht'" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Setup abgeschlossen!" -ForegroundColor Green

