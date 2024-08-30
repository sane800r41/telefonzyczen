import subprocess
import re
import time
import pygame
from datetime import datetime
import RPi.GPIO as GPIO
import os

button_pin = 23
led_pin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW)
current_dir = os.path.dirname(os.path.abspath(__file__))
def read_config_file(filename):
    config_dict = {}
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    config_dict[key.strip()] = value.strip()
    except Exception as e:
        print("Error:", e)
    return config_dict

def write_log(log):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_path = os.path.join(current_dir, 'log.txt')
    with open(log_path, 'a') as file:
        file.write(f'{timestamp}: {log}\n')

config_file_path = os.path.join(current_dir, 'config.txt')
config = read_config_file(config_file_path)
welcome_record_path = os.path.join(current_dir, config.get('welcome_record_path'))
signal_record_path = os.path.join(current_dir, config.get('signal_record_path'))
record_timeout = config.get('record_timeout')

card_pattern = r"card (\d+):"
subdevice_pattern = r"Subdevice #(\d+):"
output = subprocess.check_output(["arecord", "-l"])
card_match = re.search(card_pattern, output.decode('utf-8'))
subdevice_match = re.search(subdevice_pattern, output.decode('utf-8'))

if card_match and subdevice_match:
    card = int(card_match.group(1))
    subdevice = int(subdevice_match.group(1))

    print("Card:", card)
    print("Subdevice:", subdevice)
else:
    write_log("Unable to extract card and subdevice values.")

while True:
    GPIO.output(led_pin, GPIO.LOW)
    GPIO.wait_for_edge(button_pin, GPIO.RISING)
    time.sleep(2)
    if GPIO.input(button_pin) == GPIO.HIGH:
        pygame.init()
        try:
            pygame.mixer.music.load(welcome_record_path)
        except:
            write_log("incorrect path to the welcome record")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        try:
            pygame.mixer.music.load(signal_record_path)
        except:
            write_log("incorrect path to the signal record")
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
