# Claude Desktop Cache Törlő Script
# Használat: Jobb klikk ezen a fájlon → "Run with PowerShell"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Claude Desktop Cache Törlő" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "FIGYELEM: Ez törli az ÖSSZES extension-t!" -ForegroundColor Yellow
Write-Host "Backup helye: C:\Users\kukla\Desktop\Claude_Backup_*" -ForegroundColor Yellow
Write-Host ""
Write-Host "Folytatod? (I/N): " -ForegroundColor White -NoNewline
$confirm = Read-Host

if ($confirm -ne "I" -and $confirm -ne "i") {
    Write-Host "Megszakítva." -ForegroundColor Red
    Start-Sleep -Seconds 2
    exit
}

Write-Host ""
Write-Host "Backup készítése..." -ForegroundColor Yellow

# Backup készítés
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupPath = "$env:USERPROFILE\Desktop\Claude_Backup_$timestamp"

try {
    if (Test-Path "$env:APPDATA\Claude") {
        Copy-Item "$env:APPDATA\Claude" $backupPath -Recurse -Force -ErrorAction Stop
        Write-Host "  Backup kész: $backupPath" -ForegroundColor Green
    } else {
        Write-Host "  Nincs mit backup-olni (Claude mappa nem létezik)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  HIBA a backup készítéskor: $_" -ForegroundColor Red
    Write-Host "  Folytatod ettől függetlenül? (I/N): " -ForegroundColor White -NoNewline
    $continueAnyway = Read-Host
    if ($continueAnyway -ne "I" -and $continueAnyway -ne "i") {
        exit
    }
}

Write-Host ""
Write-Host "Claude Desktop törlése folyamatban..." -ForegroundColor Cyan
Write-Host ""

# Claude bezárása
Write-Host "[1/7] Claude folyamatok leállítása..." -ForegroundColor Cyan
$claudeProcesses = Get-Process -Name "Claude" -ErrorAction SilentlyContinue
if ($claudeProcesses) {
    $claudeProcesses | Stop-Process -Force
    Write-Host "  $($claudeProcesses.Count) folyamat leállítva" -ForegroundColor Green
} else {
    Write-Host "  Nincs futó Claude folyamat" -ForegroundColor Gray
}
Start-Sleep -Seconds 2

# Cache könyvtárak törlése
Write-Host "[2/7] Code Cache törlése..." -ForegroundColor Cyan
try {
    Remove-Item "$env:APPDATA\Claude\Code Cache\" -Recurse -Force -ErrorAction Stop
    Write-Host "  Törölve" -ForegroundColor Green
} catch {
    Write-Host "  Már törölve vagy nem létezik" -ForegroundColor Gray
}

Write-Host "[3/7] GPU Cache törlése..." -ForegroundColor Cyan
try {
    Remove-Item "$env:APPDATA\Claude\GPUCache\" -Recurse -Force -ErrorAction Stop
    Write-Host "  Törölve" -ForegroundColor Green
} catch {
    Write-Host "  Már törölve vagy nem létezik" -ForegroundColor Gray
}

Write-Host "[4/7] WebGPU Cache törlése..." -ForegroundColor Cyan
try {
    Remove-Item "$env:APPDATA\Claude\DawnWebGPUCache\" -Recurse -Force -ErrorAction Stop
    Write-Host "  Törölve" -ForegroundColor Green
} catch {
    Write-Host "  Már törölve vagy nem létezik" -ForegroundColor Gray
}

# Extensions törlése
Write-Host "[5/7] Extensions törlése..." -ForegroundColor Cyan
try {
    Remove-Item "$env:APPDATA\Claude\Claude Extensions\" -Recurse -Force -ErrorAction Stop
    Write-Host "  Törölve" -ForegroundColor Green
} catch {
    Write-Host "  Már törölve vagy nem létezik" -ForegroundColor Gray
}

Write-Host "[6/7] Extension installations config törlése..." -ForegroundColor Cyan
try {
    Remove-Item "$env:APPDATA\Claude\extensions-installations.json" -Force -ErrorAction Stop
    Write-Host "  Törölve" -ForegroundColor Green
} catch {
    Write-Host "  Már törölve vagy nem létezik" -ForegroundColor Gray
}

# Session Storage törlése
Write-Host "[7/7] Session Storage törlése..." -ForegroundColor Cyan
try {
    Remove-Item "$env:APPDATA\Claude\Session Storage\" -Recurse -Force -ErrorAction Stop
    Write-Host "  Törölve" -ForegroundColor Green
} catch {
    Write-Host "  Már törölve vagy nem létezik" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  KÉSZ!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Következő lépések:" -ForegroundColor Yellow
Write-Host "1. Indítsd újra a gépet (FONTOS!)" -ForegroundColor White
Write-Host "2. Indítsd el a Claude Desktop-ot" -ForegroundColor White
Write-Host "3. Settings → Extensions → WordPress.com → Install" -ForegroundColor White
Write-Host "4. Kövesd az OAuth bejelentkezési folyamatot" -ForegroundColor White
Write-Host ""
Write-Host "Ha probléma lenne, a backup itt van:" -ForegroundColor Yellow
Write-Host "  $backupPath" -ForegroundColor Gray
Write-Host ""
Write-Host "Nyomj ENTER-t a bezáráshoz..." -ForegroundColor Cyan
Read-Host
