@echo off
chcp 65001 > nul
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║          ÉLŐ FORDÍTÓ - Telepítő                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo [1/3] Python verzió ellenőrzése...
python --version
if errorlevel 1 (
    echo.
    echo ❌ HIBA: Python nincs telepítve!
    echo.
    echo Telepítsd a Python-t innen: https://www.python.org/downloads/
    echo FONTOS: Pipáld be az "Add Python to PATH" opciót!
    echo.
    pause
    exit /b 1
)

echo.
echo [2/3] PyAudio telepítése...
echo ⚠️  Ha ez hibát ad, telepítsd kézzel:
echo    pip install pipwin
echo    pipwin install pyaudio
echo.

pip install pipwin
pipwin install pyaudio

echo.
echo [3/3] További csomagok telepítése...
pip install -r requirements.txt

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                   ✅ TELEPÍTÉS KÉSZ!                     ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo Használat:
echo    python translator.py
echo.
pause
