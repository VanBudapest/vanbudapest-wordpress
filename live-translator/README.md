# 🎤 Élő Fordító - Google Meets Helper

Valós idejű **magyar-angol** és **angol-magyar** fordító alkalmazás Google Meets megbeszélésekhez.

## 🌟 Funkciók

- ✅ **Automatikus nyelvfelismerés** - felismeri, hogy magyarul vagy angolul beszélsz
- ✅ **Valós idejű fordítás** - azonnal fordít beszéd közben
- ✅ **Kétirányú fordítás** - magyar ↔️ angol
- ✅ **Egyszerű használat** - csak indítsd el és beszélj
- ✅ **Időbélyegek** - minden fordítás idővel van ellátva

## 📋 Követelmények

### Szoftver követelmények:
- **Python 3.7 vagy újabb**
- **Mikrofon** (beépített vagy külső)
- **Internet kapcsolat** (Google API-hoz)

### Operációs rendszerek:
- ✅ Windows 10/11
- ✅ macOS
- ✅ Linux

## 🚀 Telepítés

### 1. Python telepítése

#### Windows:
1. Töltsd le a Python-t: https://www.python.org/downloads/
2. Telepítés közben pipáld be: **"Add Python to PATH"**
3. Ellenőrzés terminálban:
   ```cmd
   python --version
   ```

#### macOS:
```bash
brew install python3
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip portaudio19-dev
```

### 2. PyAudio telepítése (fontos!)

#### Windows:
```cmd
pip install pipwin
pipwin install pyaudio
```

Vagy töltsd le innen: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

#### macOS:
```bash
brew install portaudio
pip3 install pyaudio
```

#### Linux:
```bash
sudo apt-get install python3-pyaudio
```

### 3. Alkalmazás telepítése

```bash
# Lépj be a mappába
cd live-translator

# Telepítsd a csomagokat
pip install -r requirements.txt
```

## 🎯 Használat

### Google Meets-hez:

1. **Indítsd el a Google Meets hívást**
2. **Nyiss meg egy terminált/parancssort**
3. **Futtasd az alkalmazást:**

   ```bash
   cd live-translator
   python translator.py
   ```

4. **Várd meg a kalibrálást** (2-3 másodperc)
5. **Beszélj a mikrofonba:**
   - Ha magyarul beszélsz → angolra fordít
   - Ha angolul beszélsz → magyarra fordít

6. **Leállítás:** `Ctrl+C`

### Példa használat:

```
╔══════════════════════════════════════════════════════════╗
║          ÉLŐ FORDÍTÓ - Google Meets Helper              ║
╚══════════════════════════════════════════════════════════╝

🔧 Környezeti zaj kalibrálása...
✅ Kalibrálás kész! Beszélhetsz.

🎧 Hallgatok...

[14:32:15]
🇭🇺 HU: Szia, hogy vagy?
🇬🇧 EN: Hi, how are you?
------------------------------------------------------------

[14:32:28]
🇬🇧 EN: I'm doing great, thanks!
🇭🇺 HU: Nagyon jól vagyok, köszönöm!
------------------------------------------------------------
```

## ⚙️ Beállítások

### Mikrofon kiválasztása

Ha több mikrofonod van, szerkeszd a `translator.py` fájlt:

```python
# Adott mikrofon használata (lista alapján)
with sr.Microphone(device_index=0) as source:
```

### Érzékenység módosítása

```python
# Zajszint küszöb (alacsonyabb = érzékenyebb)
self.recognizer.energy_threshold = 3000  # Alapértelmezett: 4000

# Szünet hossza mondatok között (másodperc)
self.recognizer.pause_threshold = 0.5  # Alapértelmezett: 0.8
```

## 🔧 Hibaelhárítás

### "No module named 'speech_recognition'"
```bash
pip install SpeechRecognition
```

### "PyAudio nincs telepítve" hiba
Lásd a telepítési útmutatót fentebb (PyAudio külön telepítése szükséges)

### "Could not find PyAudio" Windows-on
1. Töltsd le a megfelelő `.whl` fájlt: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. Telepítsd: `pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl`

### Mikrofon nem működik
```bash
# Ellenőrizd a mikrofonokat
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

### "Google API hiba"
- Ellenőrizd az internet kapcsolatot
- Lehet, hogy túl sok kérés (várj 1-2 percet)

### Lassú fordítás
- Ellenőrizd a hálózati sebességet
- Google Translate API lehet túlterhelt (próbáld később)

## 💡 Tippek

1. **Használj jó minőségű mikrofont** - jobb felismerés
2. **Csökkentsd a háttérzajt** - tisztább hang
3. **Beszélj világosan** - lassabban és érthetően
4. **Várj a kalibrálásra** - az első 2-3 másodperc fontos
5. **Használj füles mikrofont** - kevesebb visszacsatolás

## 📱 Google Meets Best Practices

### Kétképernyős setup:
1. **Első képernyő:** Google Meets hívás
2. **Második képernyő:** Fordító alkalmazás

### Egyképernyős setup:
1. Nyisd meg a Google Meets-et böngészőben
2. Nyisd meg a terminált fél képernyőn mellette
3. Így mindkettőt látod egyszerre

### Mikrofon használat:
- **Opció 1:** Külön mikrofon a fordítónak
- **Opció 2:** Ugyanaz a mikrofon (lehet visszhangos!)
- **Ajánlott:** Push-to-talk gomb használata a Meets-ben

## 🆘 Gyakori kérdések

**K: Tudja fordítani más nyelveket is?**
V: Igen! A kód automatikusan észleli a nyelvet, de elsősorban magyar-angol párosra van optimalizálva.

**K: Működik offline?**
V: Nem, internet kapcsolat szükséges a Google API-hoz.

**K: Menthető a fordítások története?**
V: Jelenleg nem, de hozzáadható log fájl írással.

**K: Lehet egyidejűleg használni a Meets mikrofonnal?**
V: Igen, de ajánlott külön mikrofon vagy push-to-talk.

## 🔐 Adatvédelem

- A hang a Google Speech Recognition API-n megy keresztül
- A szöveg fordítása a Google Translate API-t használja
- Nincs helyi tárolás
- Minden valós időben történik

## 📝 Licensz

MIT License - Szabadon használható és módosítható.

## 🤝 Közreműködés

Találtál hibát? Van ötleted? Nyiss egy issue-t vagy pull request-et!

## 📞 Támogatás

Ha problémád van:
1. Olvasd el a hibaelhárítási szekciót
2. Ellenőrizd a mikrofonod és internetkapcsolatot
3. Nézd meg a GitHub Issues-t

---

**Készítve ❤️ -vel, hogy megkönnyítse a nemzetközi kommunikációt!**
