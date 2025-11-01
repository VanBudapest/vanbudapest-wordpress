# WordPress.com MCP Javítási Útmutató

## Probléma
A WordPress.com MCP megjelenik a Claude Desktop Tools paneljén, de **szürke és nem lehet bekapcsolni**.

---

## GYORS JAVÍTÁS (Ezeket próbáld először, sorrendben!)

### 1. LÉPÉS: LOG_FILE beállítása (hibakereséshez)

**FONTOS:** Mielőtt bármit csinálsz, kapcsold be a részletes naplózást!

1. **Nyisd meg a Claude Desktop-ot**
2. Kattints a **Settings** (fogaskerék) ikonra
3. **Extensions** → **WordPress.com** mellett kattints a **⚙️ (Settings)** gombra
4. **Log File Path** mezőbe írd be:
   ```
   C:\Users\kukla\Documents\claude_wp_mcp_debug.log
   ```
5. Kattints **Save**
6. **Disable** majd **Enable** az extension-t
7. Próbáld **bekapcsolni a Tools panelen**
8. **Nézd meg a log fájlt** (`C:\Users\kukla\Documents\claude_wp_mcp_debug.log`)

**Mit keress a logban:**
- `ERROR` sorok
- `resources/read` körüli 500-as hibák
- `authorization` vagy `token` hibák

---

### 2. LÉPÉS: WordPress.com OAuth újra-autorizáció

**A probléma lehet, hogy az OAuth token elévült vagy hibás.**

#### A) WordPress.com oldal tisztítás

1. Nyisd meg: https://wordpress.com/me/security/connected-applications
2. Keresd meg: **"WordPress MCP Connector"**
3. Ha megtalálod → **Revoke** (visszavonás)
4. Töröld a böngésző **cookie-jait és site data-ját** (Ctrl+Shift+Del → Cookies and site data)
5. **Jelentkezz ki** a WordPress.com-ból
6. **Géprestart** (fontos!)

#### B) Claude Desktop extension újratelepítése

1. **Zárd be teljesen a Claude Desktop-ot** (Task Manager-ben is ellenőrizd, nincs futó folyamat)
2. Nyisd meg újra a Claude-ot
3. **Extensions** → **WordPress.com** → **Uninstall**
4. **Várj 10 másodpercet**
5. **Extensions** → Keresd meg újra a **WordPress.com**-ot → **Install**
6. Kövesd az **OAuth bejelentkezési folyamatot** (böngésző ablak nyílik)
7. **Engedélyezd a hozzáférést**
8. Amikor visszatér a Claude-hoz → **Tools** panelen próbáld **bekapcsolni**

---

### 3. LÉPÉS: Windows Tűzfal / Antivirus ellenőrzés

**A log szerint ESET/G DATA/Defender lehet telepítve. Ezek blokkolhatják az MCP szervert.**

#### ESET Total Security / NOD32

1. Nyisd meg az ESET-et
2. **Setup** → **Computer**
3. **Filtering** → **Exclusions**
4. Add hozzá:
   ```
   C:\Users\kukla\AppData\Roaming\Claude\
   C:\Users\kukla\AppData\Roaming\Claude\Claude Extensions\
   C:\Program Files\Claude\
   ```
5. **Network Protection** → **Firewall** → **Rules**
6. **Add Rule** → Allow:
   - **Claude.exe** (C:\Program Files\Claude\Claude.exe)
   - **node.exe** (keresés: C:\Users\kukla\AppData\...)

#### Windows Defender

1. **Windows Security** → **Virus & threat protection**
2. **Manage settings** → **Exclusions** → **Add an exclusion** → **Folder**
3. Add hozzá:
   ```
   C:\Users\kukla\AppData\Roaming\Claude
   ```

#### Windows Tűzfal

1. **Control Panel** → **Windows Defender Firewall** → **Advanced settings**
2. **Inbound Rules** → **New Rule...**
3. **Program** → Browse → `C:\Program Files\Claude\Claude.exe`
4. **Allow the connection**
5. Ugyanez **Outbound Rules**-ra is

---

### 4. LÉPÉS: Claude Desktop cache teljes törlése

**Ha az előzőek nem segítettek, teljes "clean slate" kell.**

1. **Zárd be a Claude Desktop-ot** (Task Manager ellenőrzés!)
2. **Nyisd meg a PowerShell-t** (Windows + X → Windows PowerShell)
3. Futtasd:

```powershell
# Backup készítése (elővigyázatosság)
Copy-Item "$env:APPDATA\Claude" "$env:USERPROFILE\Desktop\Claude_Backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')" -Recurse

# Cache törlés
Remove-Item "$env:APPDATA\Claude\Code Cache\" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:APPDATA\Claude\GPUCache\" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:APPDATA\Claude\DawnWebGPUCache\" -Recurse -Force -ErrorAction SilentlyContinue

# Extensions törlés (FIGYELEM: Ez törli az ÖSSZES extension-t!)
Remove-Item "$env:APPDATA\Claude\Claude Extensions\" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:APPDATA\Claude\extensions-installations.json" -Force -ErrorAction SilentlyContinue
```

4. **Géprestart**
5. **Claude Desktop indítása**
6. **WordPress.com extension újratelepítése** (2. LÉPÉS B pontja szerint)

---

### 5. LÉPÉS: MCP szerver manuális futtatás (diagnosztika)

**Ha még mindig nem megy, próbáld meg közvetlenül futtatni a szervert.**

1. **Nyisd meg a PowerShell-t**
2. Navigálj a szerver mappába:

```powershell
cd "$env:APPDATA\Claude\Claude Extensions\local.mcpb.automattic.wordpress-com-mcp\dist"
```

3. Futtasd:

```powershell
node .\index.js
```

4. **Nézd a konzol kimenetet:**
   - Ha `[INFO] [WPCOM-PROXY] WordPress Remote proxy launched successfully` → **jó**
   - Ha `[ERROR]` vagy `ENOENT`, `EACCES` → **permission/fájl hiba**
   - Ha `authorization_required` → **OAuth token hiba**

5. **Ctrl+C** a leállításhoz
6. **Másold be ide a teljes kimenetet** (screenshot vagy szöveg)

---

## Mit küldjél nekem ha nem sikerült

Ha mindez nem segített, kérlek küldd el:

1. **Screenshot** a Claude Desktop → **Settings → Developer → Local MCP servers** panelről
2. **Screenshot** a **Tools** panelről (ahol szürke a WordPress.com)
3. **Log fájl tartalma**: `C:\Users\kukla\Documents\claude_wp_mcp_debug.log`
4. **PowerShell manuális futtatás** teljes kimenete (5. LÉPÉS)
5. **Windows Eseménynapló**:
   - `eventvwr.msc` → **Application** → keresés: "Claude" vagy "Node"
   - Exportáld a hibákat (jobb klikk → Save Selected Events)

---

## Átmeneti megoldás (ha sürgős)

**Ha most azonnal kell dolgozni és az MCP nem működik:**

### WordPress REST API közvetlen használat

1. Menj: https://wordpress.com/me/security
2. **Applications** → **Create New Application**
3. **Application Name**: "Temporary Access Token"
4. **Redirect URLs**: `http://localhost`
5. Kattints **Create**
6. Másold ki a **Client ID** és **Client Secret**-et

**Token megszerzés:**

1. Böngészőben:
   ```
   https://public-api.wordpress.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost&response_type=token
   ```
2. Engedélyezd → az URL-ben lesz egy `access_token=...`
3. Ezt a tokent használd **Postman** vagy **curl**-lel:

```bash
curl https://public-api.wordpress.com/rest/v1.1/sites/vanbudapest.com/posts \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**VAGY használd a WordPress Admin felületet közvetlenül:**
- https://vanbudapest.com/wp-admin

---

## Gyakori hibák és megoldásaik

| Hiba | Ok | Megoldás |
|------|-----|----------|
| **"Server disconnected"** banner | MCP szerver nem indul vagy crash-el | Cache törlés (4. LÉPÉS) |
| **Szürke kapcsoló a Tools-ban** | OAuth token hibás vagy hiányzik | 2. LÉPÉS teljes végrehajtása |
| **"Unable to connect to extension server"** | Firewall/AV blokkolja | 3. LÉPÉS |
| **resources/read 500 error** | WordPress.com API oldali hiba VAGY cache probléma | Cache törlés + OAuth újra |
| **"authorization_required"** REST API-nál | Böngésző cookie lejárt | WordPress.com kijelentkezés/bejelentkezés |

---

## Következő lépések ha MINDEN működik

1. **Teszteld a Tools-t:**
   - "List all recent posts from my WordPress.com site"
   - "Show me the site statistics"
   - "Create a draft post titled 'Test'"

2. **Nézd a log fájlt** hogy nincs-e ERROR

3. **Készíts backup-ot** a működő konfigról:
   ```powershell
   Copy-Item "$env:APPDATA\Claude\Claude Extensions\local.mcpb.automattic.wordpress-com-mcp" `
             "$env:USERPROFILE\Desktop\WordPress_MCP_WORKING_BACKUP" -Recurse
   ```

---

## Support linkek

- **Claude Desktop dokumentáció**: https://docs.claude.com/
- **WordPress.com MCP**: https://github.com/Automattic/wordpress.com-mcp
- **WordPress.com REST API**: https://developer.wordpress.com/docs/api/

---

**Készítette:** Claude Code Assistant
**Verzió:** 1.0
**Dátum:** 2025-11-01
