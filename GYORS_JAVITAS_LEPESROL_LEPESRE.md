# 🚀 GYORS JAVÍTÁS - Lépésről-Lépésre

## Fontos! Olvasd el először:

Ezt az útmutatót **pontosan ebben a sorrendben** kövesd. **Minden lépés után ellenőrizd** hogy működik-e már a WordPress.com MCP. Ha igen, **megállhatsz**, nem kell a többi lépést végrehajtani.

**Időigény:** ~30 perc
**Szükséges:** Windows admin jogok

---

# 1️⃣ LÉPÉS: OAuth Újra-autorizáció (5 perc)

## Mit csinál?
Törli a régi, hibás WordPress.com tokent és újat kér.

## Hogyan csináld:

### A) WordPress.com oldal tisztítás

1. **Nyisd meg a böngészőt** (Edge/Chrome)

2. **Menj erre a linkre:**
   ```
   https://wordpress.com/me/security/connected-applications
   ```

3. **Várj 10 másodpercet** amíg betölt (ha csak spinner látszik, frissítsd az oldalt F5-tel)

4. **Keresd meg ezt a bejegyzést:**
   ```
   WordPress MCP Connector
   ```

5. **Kattints rá** → **"Disconnect" vagy "Revoke" gomb** → **Megerősítés**

6. **Edge böngészőben:**
   - Nyomd meg: `Ctrl + Shift + Del`
   - Pipáld be: **"Cookies and other site data"**
   - Idő: **"All time"**
   - Kattints: **"Clear now"**

7. **Jelentkezz ki** a WordPress.com-ból:
   - Jobb felső sarokban a profilképed → **"Sign Out"**

8. **Zárd be a böngészőt**

---

### B) Claude Desktop extension újratelepítése

9. **Zárd be teljesen a Claude Desktop-ot**
   - ❌ gomb → **igen, bezárás**

10. **Ellenőrizd a Task Manager-ben** (Ctrl+Shift+Esc):
    - Keress rá: "Claude"
    - Ha látod → jobb klikk → **"End task"**

11. **Indítsd újra a Claude Desktop-ot**

12. **Kattints a bal alsó sarokban:**
    - **Fogaskerék ⚙️ ikon** (Settings)

13. **Bal oldali menüben:**
    - Kattints: **"Extensions"**

14. **Keresd meg:**
    - **"WordPress.com"** extension

15. **Kattints rá** → **"Uninstall"** gomb → **Confirm**

16. **Várj 5 másodpercet**

17. **Keresőbe írd be:**
    ```
    WordPress.com
    ```

18. **Találatban:**
    - **"WordPress.com"** → **"Install"** gomb → kattints

19. **Új böngésző ablak nyílik:**
    - WordPress.com bejelentkezési oldal
    - **Add meg az email + jelszó**
    - VAGY kattints: **"Continue with Google"**

20. **Engedélyezés oldal:**
    - Látod: "WordPress MCP Connector would like to access your account"
    - Kattints: **"Approve"**

21. **Visszatér a böngésző:**
    - Látod: "You can close this window"
    - **Zárd be az ablakot**

22. **Claude Desktop-ban:**
    - Látod: "WordPress.com" extension **Enabled** ✅

23. **TESZT:**
    - Bal oldali menüben kattints: **"Tools"** 🔧 ikon
    - Keress rá: **"WordPress"**
    - Látod a **kapcsolót**?
    - Próbáld **bekapcsolni**

---

### ✅ Működik? (zöld kapcsoló, be lehet kapcsolni)
**Gratulálok! Kész vagy! A többi lépést NEM kell csinálnod!**

### ❌ Még mindig szürke/nem kapcsolható?
**Folytasd a 2. lépéssel.**

---

# 2️⃣ LÉPÉS: ESET/Tűzfal Kivételek (10 perc)

## Mit csinál?
Megengedi a Claude-nak és a Node.js-nek hogy szabadon fussanak.

## Hogyan csináld:

### A) ESET Total Security (ha telepítve van)

1. **Nyisd meg az ESET-et**
   - Tálca ikon (jobb alsó sarok) → dupla klikk az ESET ikonra
   - VAGY Start menü → "ESET"

2. **ESET főablakban:**
   - Kattints: **"Setup"** (Beállítások)

3. **Bal menüben:**
   - Kattints: **"Computer"**

4. **Jobb oldalon:**
   - Keresd meg: **"Exclusions"** (Kivételek)
   - Kattints rá

5. **"Edit" vagy "Add"** gomb:
   - Kattints: **"Add"**

6. **Mappák hozzáadása - egyenként írd be ezeket:**

   **ELSŐ kivétel:**
   ```
   C:\Users\kukla\AppData\Roaming\Claude\
   ```
   - Pipáld be: **"Include subfolders"** (Almappák)
   - Kattints: **"OK"**

   **MÁSODIK kivétel:**
   ```
   C:\Program Files\Claude\
   ```
   - Pipáld be: **"Include subfolders"**
   - Kattints: **"OK"**

7. **Vissza a főoldalra** → **Kattints: "Firewall"** (Tűzfal)

8. **"Rules" vagy "Advanced settings"**:
   - Kattints: **"Rules and zones"** → **"Editor"**

9. **"Add" gomb** (új szabály):

   **ELSŐ szabály:**
   - Name: `Claude Desktop Allow`
   - Direction: **Both** (mindkét irány)
   - Protocol: **TCP + UDP**
   - Application: **Browse...** → válaszd ki:
     ```
     C:\Program Files\Claude\Claude.exe
     ```
   - Action: **Allow**
   - Kattints: **"OK"**

10. **ESET újraindítás** (opcionális):
    - ESET bezárása → géprestart

---

### B) Windows Defender

1. **Start menü** → írd be: **"Windows Security"** → Enter

2. **"Virus & threat protection"** → kattints

3. **Görgess le:**
   - **"Virus & threat protection settings"** → **"Manage settings"**

4. **Görgess le:**
   - **"Exclusions"** → **"Add or remove exclusions"**

5. **"Add an exclusion"** → **"Folder"**

6. **Tallózd be EGYENKÉNT ezeket:**

   ```
   C:\Users\kukla\AppData\Roaming\Claude
   ```

   ```
   C:\Program Files\Claude
   ```

7. **Kattints "Select Folder"** mindegyikhez

---

### C) Windows Tűzfal

1. **Start menü** → írd be: **"Windows Defender Firewall"** → Enter

2. **Bal menüben:**
   - Kattints: **"Advanced settings"**
   - (Kér admin jogot → **"Yes"**)

3. **Bal menüben:**
   - Kattints: **"Inbound Rules"**

4. **Jobb menüben:**
   - Kattints: **"New Rule..."**

5. **Rule Wizard:**
   - **Rule Type:** `Program` → **Next**
   - **This program path:** Browse → válaszd:
     ```
     C:\Program Files\Claude\Claude.exe
     ```
     → **Next**
   - **Action:** `Allow the connection` → **Next**
   - **Profile:** Mind a 3 pipálva (Domain, Private, Public) → **Next**
   - **Name:** `Claude Desktop Inbound` → **Finish**

6. **ISMÉTELD MEG az "Outbound Rules"-ra is:**
   - Bal menü → **"Outbound Rules"**
   - Jobb menü → **"New Rule..."**
   - Ugyanazok a lépések
   - Name: `Claude Desktop Outbound`

---

### ✅ TESZT:

1. **Géprestart** (fontos!)

2. **Claude Desktop indítás**

3. **Tools panel** → WordPress.com kapcsoló → próbáld bekapcsolni

---

### ✅ Működik?
**Gratulálok! Kész vagy!**

### ❌ Még mindig nem?
**Folytasd a 3. lépéssel.**

---

# 3️⃣ LÉPÉS: Cache/Extensions Teljes Törlés (15 perc)

## Mit csinál?
Teljesen "nullázza" a Claude Desktop-ot, mintha most telepítetted volna.

## ⚠️ FIGYELEM:
- Ez törli az **ÖSSZES** extension-ödet (nem csak a WordPress-t)
- Készíts **backup-ot** először!

## Hogyan csináld:

### A) Backup készítés (biztonság)

1. **Nyisd meg a File Explorer-t** (Win + E)

2. **Címsorba másold be:**
   ```
   %APPDATA%\Claude
   ```
   → Enter

3. **Jobb klikk a "Claude" mappán** → **Copy**

4. **Menj az Asztalra** → **Jobb klikk** → **Paste**

5. **Átnevezés:**
   - Jobb klikk a lemásolt mappán → **Rename**
   - Új név: `Claude_Backup_2025_11_01`

---

### B) Automatikus törlés (PowerShell script)

**Könnyebb módszer - HASZNÁLD EZT:**

1. **Nyisd meg a Jegyzettömböt** (Notepad)

2. **Másold be ezt a TELJES szöveget:**

```powershell
# Claude Desktop Cache Törlő Script
Write-Host "Claude Desktop Cache Törlése..." -ForegroundColor Yellow
Write-Host ""

# Claude bezárása
Write-Host "[1/6] Claude folyamatok leállítása..." -ForegroundColor Cyan
Get-Process -Name "Claude" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2
Write-Host "  OK" -ForegroundColor Green

# Cache könyvtárak törlése
Write-Host "[2/6] Code Cache törlése..." -ForegroundColor Cyan
Remove-Item "$env:APPDATA\Claude\Code Cache\" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  OK" -ForegroundColor Green

Write-Host "[3/6] GPU Cache törlése..." -ForegroundColor Cyan
Remove-Item "$env:APPDATA\Claude\GPUCache\" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  OK" -ForegroundColor Green

Write-Host "[4/6] WebGPU Cache törlése..." -ForegroundColor Cyan
Remove-Item "$env:APPDATA\Claude\DawnWebGPUCache\" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  OK" -ForegroundColor Green

# Extensions törlése
Write-Host "[5/6] Extensions törlése..." -ForegroundColor Cyan
Remove-Item "$env:APPDATA\Claude\Claude Extensions\" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:APPDATA\Claude\extensions-installations.json" -Force -ErrorAction SilentlyContinue
Write-Host "  OK" -ForegroundColor Green

# Session Storage törlése (opcionális)
Write-Host "[6/6] Session Storage törlése..." -ForegroundColor Cyan
Remove-Item "$env:APPDATA\Claude\Session Storage\" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  OK" -ForegroundColor Green

Write-Host ""
Write-Host "KÉSZ! Most indítsd újra a gépet." -ForegroundColor Green
Write-Host "Géprestart után telepítsd újra a Claude Desktop-ot." -ForegroundColor Yellow
Write-Host ""
Write-Host "Nyomj ENTER-t a bezáráshoz..."
Read-Host
```

3. **Mentsd el:**
   - File → Save As
   - Hely: **Desktop** (Asztal)
   - Fájlnév: `claude_cleanup.ps1`
   - **FONTOS:** "Save as type" → válaszd: **"All Files (*.*)"**
   - Kattints: **Save**

4. **Bezárás** (Jegyzettömb)

---

### C) Script futtatása

5. **Keresd meg az Asztalon:**
   - `claude_cleanup.ps1` fájl

6. **Jobb klikk rá** → **"Run with PowerShell"**

7. **Ha kérdez valamilyen policy-t:**
   - Írd be: `Y` → Enter
   - VAGY nyisd meg **PowerShell Admin**-ként:
     - Start → írd: "PowerShell"
     - Jobb klikk: **"Run as administrator"**
     - Írd be:
       ```powershell
       Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
       ```
       → Enter
     - Aztán:
       ```powershell
       cd C:\Users\kukla\Desktop
       .\claude_cleanup.ps1
       ```
       → Enter

8. **Látod a kimenetet:**
   ```
   [1/6] Claude folyamatok leállítása...
     OK
   [2/6] Code Cache törlése...
     OK
   ...
   KÉSZ! Most indítsd újra a gépet.
   ```

---

### D) Géprestart

9. **Start menü** → **Power** → **Restart**

---

### E) Claude Desktop újratelepítése

10. **Indítsd újra a gépet**

11. **Töröld a Claude Desktop-ot:**
    - Start → Settings → Apps → "Claude" → **Uninstall**

12. **Töltsd le újra:**
    - https://claude.ai/download
    - Telepítsd

13. **Indítsd el**

14. **Bejelentkezés** (Google/email)

15. **Extensions telepítése:**
    - Settings → Extensions → **"WordPress.com"** → **Install**
    - OAuth folyamat (1. LÉPÉS B része szerint)

---

### ✅ VÉGSŐ TESZT:

1. **Tools panel** → WordPress.com → kapcsoló **BE**

2. **Chat-ben írd be:**
   ```
   List all recent posts from my WordPress.com site
   ```

3. **Látod a posztokat?**
   - **IGEN** → ✅ **MŰKÖDIK! KÉSZ!**
   - **NEM** → 😞 Küldd el a diagnosztikát (lásd alább)

---

# 🆘 Ha még mindig nem működik

## Futtasd a diagnosztikai szkriptet:

1. **Töltsd le:** https://github.com/VanBudapest/vanbudapest-wordpress/blob/claude/check-desktop-settings-011CUhwmJgzYy8owzwKbeJrJ/diagnose_claude_mcp.ps1

2. **Jobb klikk** → **Save Link As** → Desktop → `diagnose_claude_mcp.ps1`

3. **Jobb klikk** → **"Run with PowerShell"**

4. **Várj amíg végez** → megnyílik egy mappa az Asztalon

5. **Küldd el nekem:**
   - A teljes **diagnosztikai mappát** (Desktop-on)
   - **Screenshot** a Claude → Tools panelről
   - **Screenshot** a Claude → Settings → Developer → Local MCP servers-ről

---

# 📞 Hol kérj segítséget

- **GitHub Issue:** https://github.com/VanBudapest/vanbudapest-wordpress/issues
- **Claude Support:** https://support.anthropic.com/
- **WordPress.com MCP:** https://github.com/Automattic/wordpress.com-mcp/issues

---

**Készítette:** Claude Code Assistant
**Verzió:** 1.0
**Utolsó frissítés:** 2025-11-01

**Sok sikert! 🚀**
