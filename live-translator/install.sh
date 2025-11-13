#!/bin/bash

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║          ÉLŐ FORDÍTÓ - Telepítő                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

echo "[1/3] Python verzió ellenőrzése..."
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "❌ HIBA: Python3 nincs telepítve!"
    echo ""
    echo "Ubuntu/Debian:"
    echo "  sudo apt update"
    echo "  sudo apt install python3 python3-pip portaudio19-dev"
    echo ""
    echo "macOS:"
    echo "  brew install python3 portaudio"
    echo ""
    exit 1
fi

python3 --version

echo ""
echo "[2/3] Rendszerfüggőségek telepítése..."

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Linux detected - PortAudio telepítése..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y portaudio19-dev python3-pyaudio
    elif command -v yum &> /dev/null; then
        sudo yum install -y portaudio-devel
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS detected - PortAudio telepítése..."
    if command -v brew &> /dev/null; then
        brew install portaudio
    else
        echo "⚠️  Homebrew nincs telepítve. Telepítsd: https://brew.sh"
    fi
fi

echo ""
echo "[3/3] Python csomagok telepítése..."
pip3 install -r requirements.txt

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                   ✅ TELEPÍTÉS KÉSZ!                     ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Használat:"
echo "   python3 translator.py"
echo ""
