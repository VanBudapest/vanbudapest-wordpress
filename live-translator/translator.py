#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Élő Fordító Alkalmazás Google Meets-hez
Angol-Magyar és Magyar-Angol valós idejű fordítás
"""

import speech_recognition as sr
from googletrans import Translator
import threading
import time
from datetime import datetime
import sys

class LiveTranslator:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        self.is_running = False
        self.source_lang = "hu"  # Kezdeti nyelv: magyar

        # Mikrofon beállítások finomhangolása
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

    def detect_and_translate(self, text):
        """Automatikus nyelvfelismerés és fordítás"""
        try:
            # Nyelv detektálás
            detected = self.translator.detect(text)

            if detected.lang == 'en':
                # Angolról magyarra
                translation = self.translator.translate(text, src='en', dest='hu')
                return f"🇬🇧 EN: {text}\n🇭🇺 HU: {translation.text}"
            elif detected.lang == 'hu':
                # Magyarról angolra
                translation = self.translator.translate(text, src='hu', dest='en')
                return f"🇭🇺 HU: {text}\n🇬🇧 EN: {translation.text}"
            else:
                # Más nyelv esetén angolra fordítunk
                translation = self.translator.translate(text, dest='en')
                return f"🌐 {detected.lang.upper()}: {text}\n🇬🇧 EN: {translation.text}"

        except Exception as e:
            return f"❌ Fordítási hiba: {str(e)}"

    def listen_and_translate(self):
        """Folyamatos hallgatás és fordítás"""
        print("\n" + "="*60)
        print("🎤 ÉLŐ FORDÍTÓ ELINDULT")
        print("="*60)
        print("📢 Beszélj a mikrofonba...")
        print("⌨️  Nyomd meg a Ctrl+C-t a leállításhoz\n")

        with sr.Microphone() as source:
            # Környezeti zaj kalibrálás
            print("🔧 Környezeti zaj kalibrálása...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("✅ Kalibrálás kész! Beszélhetsz.\n")

            while self.is_running:
                try:
                    print("🎧 Hallgatok...", end='\r')
                    # Hangfelvétel
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)

                    print("🔄 Feldolgozás...", end='\r')

                    # Beszédfelismerés - először magyarul próbáljuk
                    text = None
                    try:
                        text = self.recognizer.recognize_google(audio, language="hu-HU")
                    except sr.UnknownValueError:
                        # Ha magyarul nem sikerült, próbáljuk angolul
                        try:
                            text = self.recognizer.recognize_google(audio, language="en-US")
                        except sr.UnknownValueError:
                            print("❓ Nem értettem, próbáld újra...          ")
                            continue

                    if text:
                        # Időbélyeg
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        print(f"\n[{timestamp}]")

                        # Fordítás
                        result = self.detect_and_translate(text)
                        print(result)
                        print("-" * 60)

                except sr.WaitTimeoutError:
                    # Timeout - nincs probléma, folytatjuk
                    continue
                except sr.RequestError as e:
                    print(f"\n❌ Google API hiba: {e}")
                    print("⚠️  Ellenőrizd az internet kapcsolatot!")
                    time.sleep(2)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"\n❌ Hiba: {str(e)}")
                    time.sleep(1)

    def start(self):
        """Fordító indítása"""
        self.is_running = True
        try:
            self.listen_and_translate()
        except KeyboardInterrupt:
            print("\n\n🛑 Leállítás...")
            self.stop()

    def stop(self):
        """Fordító leállítása"""
        self.is_running = False
        print("👋 Viszlát!\n")

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║          ÉLŐ FORDÍTÓ - Google Meets Helper              ║
║                                                          ║
║  🇭🇺 Magyar ↔️ Angol 🇬🇧                                 ║
║                                                          ║
║  Használat:                                              ║
║  1. Indítsd el a Google Meets hívást                    ║
║  2. Futtasd ezt az alkalmazást                          ║
║  3. Beszélj a mikrofonba                                ║
║  4. Az alkalmazás automatikusan felismeri a nyelvet     ║
║     és lefordítja                                        ║
║                                                          ║
║  Ctrl+C = Leállítás                                      ║
╚══════════════════════════════════════════════════════════╝
    """)

    # Ellenőrizzük a mikrofont
    try:
        mics = sr.Microphone.list_microphone_names()
        print(f"📱 Elérhető mikrofonok ({len(mics)} db):")
        for i, mic in enumerate(mics):
            print(f"   {i}: {mic}")
        print()
    except Exception as e:
        print(f"⚠️  Figyelem: Nem sikerült a mikrofonok listázása: {e}\n")

    translator = LiveTranslator()
    translator.start()

if __name__ == "__main__":
    main()
