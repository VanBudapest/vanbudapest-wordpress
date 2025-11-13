# ⚡ GYORS START - 5 Perc Alatt

## Windows Felhasználóknak

### 1️⃣ Python telepítés (ha még nincs)
1. Nyisd meg: https://www.python.org/downloads/
2. Töltsd le és telepítsd
3. ✅ **FONTOS:** Pipáld be az **"Add Python to PATH"** opciót!

### 2️⃣ Alkalmazás telepítése
1. Nyiss meg egy **Command Prompt**-ot (cmd)
2. Navigálj a mappába:
   ```cmd
   cd live-translator
   ```
3. Futtasd a telepítőt:
   ```cmd
   install.bat
   ```

### 3️⃣ Indítás
```cmd
python translator.py
```

---

## macOS Felhasználóknak

### 1️⃣ Python telepítés (ha még nincs)
```bash
brew install python3
```

### 2️⃣ Alkalmazás telepítése
```bash
cd live-translator
chmod +x install.sh
./install.sh
```

### 3️⃣ Indítás
```bash
python3 translator.py
```

---

## Linux Felhasználóknak

### 1️⃣ Python telepítés (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip portaudio19-dev
```

### 2️⃣ Alkalmazás telepítése
```bash
cd live-translator
chmod +x install.sh
./install.sh
```

### 3️⃣ Indítás
```bash
python3 translator.py
```

---

## 🎯 Használat Google Meets-szel

### Kétképernyős Setup (AJÁNLOTT):
1. **Bal képernyő:** Google Meets
2. **Jobb képernyő:** Fordító alkalmazás
3. Beszélj a mikrofonba
4. Olvasd a fordításokat a jobb képernyőn

### Egyképernyős Setup:
1. Google Meets - fél képernyő
2. Terminal/CMD - fél képernyő
3. Windows: `Win + ←/→` az ablakok rendezéséhez

---

## 🆘 Problémák?

### "Python nincs megtalálva"
- Windows: Újraindítás telepítés után
- Ellenőrizd: `python --version`

### "PyAudio hiba"
**Windows:**
```cmd
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip3 install pyaudio
```

**Linux:**
```bash
sudo apt-get install python3-pyaudio
```

### "Mikrofon nem működik"
1. Ellenőrizd a mikrofon engedélyeket
2. Windows: Beállítások → Adatvédelem → Mikrofon
3. macOS: Rendszerbeállítások → Biztonság → Mikrofon

### "Nem ismeri fel a beszédet"
- Beszélj hangosabban
- Csökkentsd a háttérzajt
- Várj a kalibrálásra (2-3 mp)

---

## 💡 PRO TIPPEK

1. **Fejhallgató mikrofonnal** - legjobb minőség
2. **Csendes környezet** - jobb felismerés
3. **Internet:** Min. 2-3 Mbps ajánlott
4. **Első használat:** Tesztelj pár percet meetingt előtt!

---

## 📊 Mikrofon Teszt

Ellenőrizd, hogy működik-e:

```python
python -c "import speech_recognition as sr; print('Mikrofonok:'); [print(f'{i}: {m}') for i,m in enumerate(sr.Microphone.list_microphone_names())]"
```

---

**✅ KÉSZ VAGY! Most már használhatod a Google Meets-hez!**

További részletek: `README.md`
