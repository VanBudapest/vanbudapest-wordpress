# VanBudapest WordPress - Claude Desktop MCP Diagnosztika

## Gyors áttekintés

Ez a repository a **VanBudapest WordPress.com** site és a **Claude Desktop MCP integráció** hibakeresési dokumentációját tartalmazza.

## Probléma leírás

A WordPress.com MCP extension **megjelenik a Claude Desktop Tools paneljén, de szürke és nem lehet bekapcsolni**.

### Tünetek
- ✅ WordPress.com MCP szerver **fut** (`running` státusz)
- ✅ JSON-RPC kommunikáció **működik**
- ❌ `resources/read` hívások **500-as hibát** adnak
- ❌ Tools panelen a kapcsoló **szürke és nem kapcsolható be**
- ❌ Más MCP-k is hasonló problémát mutatnak (Cloudinary, Filesystem, PDF Tools)

## Dokumentumok

### 📄 [WORDPRESS_MCP_JAVITAS.md](./WORDPRESS_MCP_JAVITAS.md)
**Teljes, lépésről-lépésre javítási útmutató** az alábbi témákban:
1. LOG_FILE beállítása részletes hibakereséshez
2. WordPress.com OAuth újra-autorizáció
3. Windows Tűzfal/Antivirus konfiguráció
4. Claude Desktop cache teljes törlése
5. MCP szerver manuális diagnosztika
6. Átmeneti megoldások (REST API közvetlen használat)

## Gyors javítás (próbáld először!)

### 1. LOG_FILE bekapcsolása
```
Claude Desktop → Settings → Extensions → WordPress.com → ⚙️
Log File Path: C:\Users\kukla\Documents\claude_wp_mcp_debug.log
Save → Disable/Enable extension
```

### 2. OAuth újra-autorizáció
```
1. https://wordpress.com/me/security/connected-applications
2. "WordPress MCP Connector" → Revoke
3. Claude Desktop → Extensions → WordPress.com → Uninstall
4. Géprestart
5. Claude Desktop → Extensions → WordPress.com → Install
6. OAuth flow követése
```

### 3. Tűzfal/AV kivételek
**ESET/Defender**: Add kivételként
```
C:\Users\kukla\AppData\Roaming\Claude\
C:\Program Files\Claude\
```

### 4. Cache törlés (PowerShell Admin)
```powershell
Remove-Item "$env:APPDATA\Claude\Code Cache\" -Recurse -Force
Remove-Item "$env:APPDATA\Claude\Claude Extensions\" -Recurse -Force
```
Géprestart → Claude újratelepítés

## Technikai részletek

### Környezet
- **OS:** Windows 10 Home 22H2 (build 19045.6456)
- **Claude Desktop:** ~1.0.211
- **Node.js (beágyazott):** v22.19.0
- **WordPress site:** vanbudapest.com
- **Jetpack:** Backup & Scan aktív

### Ismert hibák a logból
```
[ERROR] [API] API error response:
{"code":-32603,"message":"Internal error: Failed to read resource ...","data":{"status":500}}
```

### MCP szerver státusz
```
Local MCP servers → WordPress.com: running
Command: node C:\Users\kukla\AppData\Roaming\Claude\Claude Extensions\local.mcpb.automattic.wordpress-com-mcp\dist\index.js
Environment: NODE_ENV=production, LOG_FILE=(üres)
```

## Mit küldjél ha nem sikerült

Ha a javítási útmutató nem segített:

1. **Log fájl**: `C:\Users\kukla\Documents\claude_wp_mcp_debug.log`
2. **Screenshot**: Claude Desktop → Tools panel (szürke kapcsolóval)
3. **Screenshot**: Settings → Developer → Local MCP servers
4. **PowerShell kimenet**: `node .\index.js` (lásd WORDPRESS_MCP_JAVITAS.md 5. LÉPÉS)
5. **Windows Eseménynapló**: Application/System hibák (eventvwr.msc)

## Átmeneti megoldás

**WordPress REST API közvetlen használata:**
```bash
# Token megszerzés: https://wordpress.com/me/security (új alkalmazás)
curl https://public-api.wordpress.com/rest/v1.1/sites/vanbudapest.com/posts \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Vagy használd a **WP Admin** felületet közvetlenül: https://vanbudapest.com/wp-admin

## Linkek

- **WordPress.com MCP GitHub**: https://github.com/Automattic/wordpress.com-mcp
- **Claude Desktop Docs**: https://docs.claude.com/
- **WordPress.com REST API**: https://developer.wordpress.com/docs/api/
- **Connected Applications**: https://wordpress.com/me/security/connected-applications

---

**Utolsó frissítés:** 2025-11-01
**Készítette:** Claude Code Assistant
