# WordPress.com MCP Diagnosztikai Szkript
# Futtatás: PowerShell-ből (Admin jogokkal ajánlott)
# .\diagnose_claude_mcp.ps1

Write-Host "=== WordPress.com MCP Diagnosztika ===" -ForegroundColor Cyan
Write-Host ""

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$outputDir = "$env:USERPROFILE\Desktop\Claude_MCP_Diagnostics_$timestamp"
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

Write-Host "[1/8] Környezet információk gyűjtése..." -ForegroundColor Yellow

# Rendszer info
$sysInfo = @{
    "OS" = (Get-WmiObject Win32_OperatingSystem).Caption
    "Build" = (Get-WmiObject Win32_OperatingSystem).BuildNumber
    "CPU" = (Get-WmiObject Win32_Processor).Name
    "RAM_GB" = [math]::Round((Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)
    "PowerShell_Version" = $PSVersionTable.PSVersion.ToString()
    "Node_Version" = (node --version 2>&1)
    "Timestamp" = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
}
$sysInfo | ConvertTo-Json | Out-File "$outputDir\system_info.json"
Write-Host "  ✓ system_info.json" -ForegroundColor Green

# Claude Desktop verzió
Write-Host "[2/8] Claude Desktop verzió ellenőrzése..." -ForegroundColor Yellow
$claudeExe = "C:\Program Files\Claude\Claude.exe"
if (Test-Path $claudeExe) {
    $claudeVersion = (Get-Item $claudeExe).VersionInfo.FileVersion
    Write-Host "  ✓ Claude Desktop verzió: $claudeVersion" -ForegroundColor Green
    $sysInfo.Claude_Version = $claudeVersion
} else {
    Write-Host "  ✗ Claude.exe nem található!" -ForegroundColor Red
}

# Claude futó folyamatok
Write-Host "[3/8] Claude folyamatok ellenőrzése..." -ForegroundColor Yellow
$claudeProcesses = Get-Process -Name "Claude" -ErrorAction SilentlyContinue
if ($claudeProcesses) {
    $claudeProcesses | Select-Object Id, ProcessName, StartTime, @{Name="Memory_MB";Expression={[math]::Round($_.WorkingSet64 / 1MB, 2)}} |
        Format-Table | Out-File "$outputDir\claude_processes.txt"
    Write-Host "  ✓ Claude futó folyamatok: $($claudeProcesses.Count)" -ForegroundColor Green
} else {
    Write-Host "  ✗ Nincs futó Claude folyamat" -ForegroundColor Red
}

# Claude config és log fájlok
Write-Host "[4/8] Claude konfigurációs fájlok keresése..." -ForegroundColor Yellow
$claudeAppData = "$env:APPDATA\Claude"

if (Test-Path $claudeAppData) {
    # Config fájlok listázása
    Get-ChildItem -Path $claudeAppData -Recurse -Include "*.json","*.log" -ErrorAction SilentlyContinue |
        Select-Object FullName, Length, LastWriteTime |
        Export-Csv "$outputDir\claude_config_files.csv" -NoTypeInformation

    # Extensions installations
    $extInstallFile = "$claudeAppData\extensions-installations.json"
    if (Test-Path $extInstallFile) {
        Copy-Item $extInstallFile "$outputDir\extensions-installations.json"
        Write-Host "  ✓ extensions-installations.json" -ForegroundColor Green
    }

    # MCP servers config (ha van)
    $mcpConfigFile = "$claudeAppData\claude_desktop_config.json"
    if (Test-Path $mcpConfigFile) {
        Copy-Item $mcpConfigFile "$outputDir\claude_desktop_config.json"
        Write-Host "  ✓ claude_desktop_config.json" -ForegroundColor Green
    }

    # WordPress MCP extension fájlok
    $wpMcpPath = "$claudeAppData\Claude Extensions\local.mcpb.automattic.wordpress-com-mcp"
    if (Test-Path $wpMcpPath) {
        Write-Host "  ✓ WordPress MCP extension megtalálva" -ForegroundColor Green
        Get-ChildItem -Path $wpMcpPath -Recurse -File |
            Select-Object FullName, Length, LastWriteTime |
            Export-Csv "$outputDir\wordpress_mcp_files.csv" -NoTypeInformation
    } else {
        Write-Host "  ✗ WordPress MCP extension NINCS telepítve!" -ForegroundColor Red
    }

    # Logs könyvtár
    $logsPath = "$claudeAppData\logs"
    if (Test-Path $logsPath) {
        $latestLogs = Get-ChildItem -Path $logsPath -Filter "*.log" | Sort-Object LastWriteTime -Descending | Select-Object -First 5
        foreach ($log in $latestLogs) {
            Copy-Item $log.FullName "$outputDir\$($log.Name)"
        }
        Write-Host "  ✓ Utolsó 5 log fájl másolva" -ForegroundColor Green
    }

} else {
    Write-Host "  ✗ Claude AppData mappa nem található!" -ForegroundColor Red
}

# WordPress MCP log (ha be van állítva)
Write-Host "[5/8] WordPress MCP specifikus log keresése..." -ForegroundColor Yellow
$wpMcpLog = "$env:USERPROFILE\Documents\claude_wp_mcp_debug.log"
if (Test-Path $wpMcpLog) {
    Copy-Item $wpMcpLog "$outputDir\claude_wp_mcp_debug.log"
    Write-Host "  ✓ WordPress MCP debug log megtalálva" -ForegroundColor Green
} else {
    Write-Host "  ! WordPress MCP debug log nincs beállítva (LOG_FILE)" -ForegroundColor Yellow
    Write-Host "    Állítsd be: Claude → Settings → Extensions → WordPress.com → Log File Path" -ForegroundColor Gray
}

# Tűzfal szabályok
Write-Host "[6/8] Windows Tűzfal szabályok ellenőrzése..." -ForegroundColor Yellow
try {
    $firewallRules = Get-NetFirewallRule -DisplayName "*Claude*" -ErrorAction SilentlyContinue
    if ($firewallRules) {
        $firewallRules | Select-Object DisplayName, Direction, Action, Enabled |
            Format-Table | Out-File "$outputDir\firewall_rules.txt"
        Write-Host "  ✓ Tűzfal szabályok exportálva" -ForegroundColor Green
    } else {
        Write-Host "  ! Nincs Claude-ra vonatkozó tűzfal szabály" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ! Tűzfal lekérdezés nem sikerült (Admin jogok kellenek)" -ForegroundColor Yellow
}

# Antivirus info (ha lehet)
Write-Host "[7/8] Antivirus szoftverek keresése..." -ForegroundColor Yellow
$avProducts = Get-WmiObject -Namespace "root\SecurityCenter2" -Class AntiVirusProduct -ErrorAction SilentlyContinue
if ($avProducts) {
    $avProducts | Select-Object displayName, productState, pathToSignedProductExe |
        ConvertTo-Json | Out-File "$outputDir\antivirus_products.json"
    Write-Host "  ✓ Telepített AV szoftverek: $($avProducts.displayName -join ', ')" -ForegroundColor Green
} else {
    Write-Host "  ! Nem sikerült lekérdezni az AV szoftvereket" -ForegroundColor Yellow
}

# WordPress.com kapcsolat teszt
Write-Host "[8/8] WordPress.com API kapcsolat tesztelése..." -ForegroundColor Yellow
try {
    $wpApiTest = Invoke-RestMethod -Uri "https://public-api.wordpress.com/rest/v1.1/sites/vanbudapest.com" -Method Get -ErrorAction Stop
    Write-Host "  ✓ WordPress.com API elérhető" -ForegroundColor Green
    $wpApiTest | ConvertTo-Json -Depth 3 | Out-File "$outputDir\wordpress_api_test.json"
} catch {
    Write-Host "  ✗ WordPress.com API hiba: $($_.Exception.Message)" -ForegroundColor Red
    $_.Exception | Out-File "$outputDir\wordpress_api_error.txt"
}

# Node.js PATH és verzió
Write-Host ""
Write-Host "=== Egyéb ellenőrzések ===" -ForegroundColor Cyan
$nodePath = (Get-Command node -ErrorAction SilentlyContinue).Path
if ($nodePath) {
    Write-Host "  ✓ Node.js: $(node --version) [$nodePath]" -ForegroundColor Green
} else {
    Write-Host "  ✗ Node.js NINCS a PATH-ban!" -ForegroundColor Red
}

# MCP szerver manuális teszt ajánlás
Write-Host ""
Write-Host "=== Következő lépések ===" -ForegroundColor Cyan
Write-Host "1. Nézd át a diagnosztikai fájlokat: $outputDir" -ForegroundColor White
Write-Host "2. Ha WordPress MCP extension telepítve van, próbáld manuálisan futtatni:" -ForegroundColor White
Write-Host "   cd `"$env:APPDATA\Claude\Claude Extensions\local.mcpb.automattic.wordpress-com-mcp\dist`"" -ForegroundColor Gray
Write-Host "   node .\index.js" -ForegroundColor Gray
Write-Host "3. Ellenőrizd a README.md és WORDPRESS_MCP_JAVITAS.md fájlokat" -ForegroundColor White
Write-Host ""

# Összefoglaló jelentés
$summary = @"
=== DIAGNOSZTIKAI ÖSSZEFOGLALÓ ===

Diagnosztika időpontja: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Diagnosztikai fájlok helye: $outputDir

Rendszer:
- OS: $($sysInfo.OS) (Build $($sysInfo.Build))
- CPU: $($sysInfo.CPU)
- RAM: $($sysInfo.RAM_GB) GB

Claude Desktop:
- Verzió: $($sysInfo.Claude_Version)
- Futó folyamatok: $($claudeProcesses.Count)
- AppData létezik: $(Test-Path $claudeAppData)

WordPress MCP:
- Extension telepítve: $(Test-Path "$claudeAppData\Claude Extensions\local.mcpb.automattic.wordpress-com-mcp")
- Debug log beállítva: $(Test-Path $wpMcpLog)

Következő lépések:
1. Ha WordPress MCP nincs telepítve → Claude Desktop → Extensions → Install
2. Ha debug log nincs beállítva → Settings → Extensions → WordPress.com → Log File Path
3. Ha Tűzfal/AV blokkolja → Kivételek hozzáadása (lásd WORDPRESS_MCP_JAVITAS.md)
4. Ha OAuth hiba → Uninstall/Install extension + WordPress.com Connected Apps revoke

Részletes útmutató: README.md és WORDPRESS_MCP_JAVITAS.md
"@

$summary | Out-File "$outputDir\SUMMARY.txt"

Write-Host "✓ Diagnosztika befejezve!" -ForegroundColor Green
Write-Host "Fájlok helye: $outputDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "Nyomj ENTER-t a mappa megnyitásához..." -ForegroundColor Yellow
Read-Host
Start-Process $outputDir
