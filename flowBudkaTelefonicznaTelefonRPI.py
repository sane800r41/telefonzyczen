import sounddevice as sd
import numpy as np
import wave
import pygame
import time
import RPi.GPIO as GPIO

# Initialize pygame mixer module
pygame.mixer.init()

# Ustawienia GPIO
BUTTON_PIN = 18  # Numer pinu GPIO do przycisku
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Ustawienia nagrywania
SAMPLERATE = 44100  # Częstotliwość próbkowania
CHANNELS = 2  # Liczba kanałów (stereo)
FILENAME = "/home/pi/wishes/recording_"  # Ścieżka do zapisywania plików

# Set up sound files
SOUND_FILES = [
    "./uploads/music.mp3",
    "./uploads/recording.mp3",
    "./uploads/beep.mp3"
]

# Play sound files in sequence
def play_sounds():
    for sound_file in SOUND_FILES:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

# Funkcja nagrywania
def record_wish():
    print("Nagrywanie rozpoczęte...")

    # Tworzenie pliku WAV
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filepath = FILENAME + timestamp + ".wav"
    
    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # Szerokość próbek w bajtach (2 bajty dla 16-bitowego audio)
        wf.setframerate(SAMPLERATE)

        # Funkcja callback do zapisu danych audio
        def callback(indata, frames, time, status):
            wf.writeframes(indata.tobytes())

        # Nagrywanie
        with sd.InputStream(samplerate=SAMPLERATE, channels=CHANNELS, callback=callback):
            sd.sleep(100)
    
    print(f"Nagrywanie zakończone. Plik zapisany jako {filepath}")

# Główna pętla programu
print("Telefon życzeń jest gotowy do użycia.")
try:
    while True:
        if GPIO.input(BUTTON_PIN) == False:
            play_sounds()
            record_wish()
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Zamykanie programu...")

finally:
    pygame.mixer.quit()
    GPIO.cleanup()
    print('what a shitstorm :skull:')