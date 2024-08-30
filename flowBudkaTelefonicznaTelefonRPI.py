import subprocess
import re
import time
import pygame
from datetime import datetime
import RPi.GPIO as GPIO
import os
import colorama

# Numery pinów pod przycisk i led.
button_pin = 23
led_pin = 24

# Definiuje czytanie logów:
def write_log(log):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_path = os.path.join(current_dir, 'log.txt')
    with open(log_path, 'a') as file:
        file.write(f'{timestamp}: {log}\n')


# Set up GPIO mode and pin configurations
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW)

# Dostaję cd
current_dir = os.path.dirname(os.path.abspath(__file__))
write_log(f"[info] W skrypcie telefonu zapisałem cd: {current_dir}")    

# Define constants for record paths and timeout
music_record_path = current_dir + fr"\uploads\music.wav"
welcome_record_path = current_dir + fr"\uploads\recording.wav"
signal_record_path = current_dir + fr"\uploads\beep.wav"
record_timeout = 10  # seconds

def extract_card_and_subdevice():
    output = subprocess.check_output(["arecord", "-l"])
    card_pattern = r"card (\d+):"
    subdevice_pattern = r"Subdevice #(\d+):"
    card_match = re.search(card_pattern, output.decode('utf-8'))
    subdevice_match = re.search(subdevice_pattern, output.decode('utf-8'))
    if card_match and subdevice_match:
        card = int(card_match.group(1))
        subdevice = int(subdevice_match.group(1))
        print(colorama.Fore.BLUE + "[i] Karta:" + colorama.Fore.MAGENTA + card + colorama.Fore.RESET) 
        write_log("[info] Karta: " + card)
        print(colorama.Fore.GREEN + "[i] Podurządzenie:" + colorama.Fore.MAGENTA + subdevice + colorama.Fore.RESET)  
        write_log("[info] Podurządzenie: " + subdevice)
        return card, subdevice
    else:
        write_log("[error] Nie można wyodrębnić wartości karty i podurządzenia.")  # Nie można wyodrębnić means "Unable to extract" in Polish
    return None

card, subdevice = extract_card_and_subdevice()
if card is None or subdevice is None:
    exit(1)

while True:
    GPIO.output(led_pin, GPIO.LOW)
    GPIO.wait_for_edge(button_pin, GPIO.RISING)
    time.sleep(2)
    if GPIO.input(button_pin) == GPIO.HIGH:
        pygame.init()
        try:
            pygame.mixer.music.load(music_record_path)
        except:
            write_log("Nieprawidłowa ścieka do nagrania muzyki ")
        try:
            pygame.mixer.music.load(welcome_record_path)
        except:
            write_log("Nieprawidłowa ścieżka do nagrania powitania")  
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        try:
            pygame.mixer.music.load(signal_record_path)
        except:
            write_log("Nieprawidłowa ścieżka do nagrania sygnału")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.quit()
        GPIO.output(led_pin, GPIO.HIGH)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = timestamp + ".wav"
        file_path = os.path.join(current_dir, 'records', file_name)
        plughw_string = f"plughw:{card},{subdevice}"
        process = subprocess.Popen([
            "arecord",
            "-D",
            plughw_string,
            "--duration=" + str(record_timeout),
            "--format=cd",
            file_path
        ])
        GPIO.wait_for_edge(button_pin, GPIO.FALLING)
        process.terminate()