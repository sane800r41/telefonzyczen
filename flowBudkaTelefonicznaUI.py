from nicegui import events, ui
import os
import colorama
import time
import datetime

colorama.just_fix_windows_console()
infoColor = colorama.Fore.BLUE
errorColor = colorama.Fore.RED
successColor = colorama.Fore.GREEN
print(infoColor + "[i] Startuję skrypt - webUI.py - webUI dostępne będzie na porcie 8080." + colorama.Fore.RESET)

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define constants for record paths and timeout
music_record_path = current_dir + fr"\uploads\music.mp3"
welcome_record_path = current_dir + fr"\uploads\recording.mp3"
signal_record_path = current_dir + fr"\uploads\beep.mp3"
record_timeout = 10  # seconds

def write_log(log):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_path = os.path.join(current_dir, 'log.txt')
    with open(log_path, 'a') as file:
        file.write(f'{timestamp}: {log}\n')

# Check if the 'uploads' folder exists, if not create it
if os.path.isdir('dzwieki'):
    print(infoColor + "[i] Folder dzwieki istnieje, ignoruję." + colorama.Fore.RESET)
    write_log("[info] Folder 'dzwieki' istnieje, ignoruje. ")
    time.sleep(1)
else:
    os.mkdir("dzwieki")
    print(infoColor + "[i] Utworzono folder - dzwieki" + colorama.Fore.RESET)
    write_log("[info] Utworzono folder 'dzwieki'.")

def handle_upload1(e: events.UploadEventArguments):
    print(infoColor + '[i] Dźwigam upload.' + colorama.Fore.RESET)
    write_log("[info] Dźwigam upload.")
    soundEffect = e.content
    print(infoColor + '[i] Próbuję zapisać dźwięk. + colorama.Fore.RESET')
    write_log("[info] Próbuję zapisać dźwięk.")
    with open(r""".\uploads\music.mp3""", "wb") as mainSound:  # Use "wb" to write bytes
        while True:
            chunk = soundEffect.read(4096)
            if not chunk:
                break
            mainSound.write(chunk)

def handle_upload2(e: events.UploadEventArguments):
    print(infoColor + '[i] Dźwigam upload.' + colorama.Fore.RESET)
    write_log("[info] Dźwigam upload.")
    soundEffect = e.content
    print(infoColor + '[i] Próbuję zapisać dźwięk' + colorama.Fore.RESET)
    write_log("[info] Próbuję zapisać dźwięk.")

    with open(r""".\uploads\recording.mp3""", "wb") as mainSound:  # Use "wb" to write bytes
        while True:
            chunk = soundEffect.read(4096)
            if not chunk:
                break
            mainSound.write(chunk)

def handle_upload3(e: events.UploadEventArguments):
    print(infoColor + '[i] Dźwigam upload.'+ colorama.Fore.RESET)
    write_log("[info] Dźwigam upload.")
    soundEffect = e.content
    print(infoColor + '[i] Próbuję zapisać dźwięk' + colorama.Fore.RESET)
    write_log("[info] Próbuję zapisać dźwięk.")

    with open(r""".\uploads\beep.mp3""", "wb") as mainSound:  # Use "wb" to write bytes
        while True:
            chunk = soundEffect.read(4096)
            if not chunk:
                break
            mainSound.write(chunk)

def handle_slider_change(e):
    volume_label.set_text(f"{e.value}%")
    write_log(f"Zmiana głośności na {e.value}%, przez GUI.")
    

# UI layout
# Main title centered at the top of the page
ui.label('Telefon Życzeń Flow Media') \
    .style('font-size: 36px; font-weight: bold; text-align: center; margin-top: 20px; font-family: "Arial", sans-serif; width: 100%;')
# Row for the upload label and upload component
with ui.row().style('align-items: flex-start; margin-top: 20px; padding-left: 10%;'):
    # Left side upload
    with ui.column().style('margin-right: 20px;'):
        ui.label('Tutaj załącz muzyczkę:') \
            .style('font-size: 18px; margin-bottom: 10px;')
        ui.upload(on_upload=handle_upload1,
                  on_rejected=lambda: ui.notify('Nie można było zapisać pliku. Upewnij się że ma mniej niż 1GB i jest .mp3! Jeżeli to nie zadziała, odśwież stronę ;)'),
                  max_file_size=1_000_000) \
            .props('accept=.mp3') \
            .classes('max-w-full')

    # Center upload
    with ui.column().style('margin-right: 20px;'):
        ui.label('Tutaj załącz nagranie pary młodej:') \
            .style('font-size: 18px; margin-bottom: 10px;')
        ui.upload(on_upload=handle_upload2,
                  on_rejected=lambda: ui.notify('Nie można było zapisać pliku. Upewnij się że ma mniej niż 1GB i jest .mp3! Jeżeli to nie zadziała, odśwież stronę ;)'),
                  max_file_size=1_000_000) \
            .props('accept=.mp3') \
            .classes('max-w-full')
        ui.label('Głośność:') \
            .style('font-size: 18px; margin-bottom: -8px;')
        slider = ui.slider(min=0, max=100, on_change=handle_slider_change) \
            .style('margin-top: -5px;')
        volume_label = ui.label('0%') \
            .style('font-size: 18px; text-align: center; margin-bottom: 10px; margin-top: -10px;')

    # Right side upload
    with ui.column():
        ui.label('Tutaj załącz *BIIIIP*:') \
            .style('font-size: 18px; margin-bottom: 10px;')
        ui.upload(on_upload=handle_upload3,
                  on_rejected=lambda: ui.notify('Nie można było zapisać pliku. Upewnij się że ma mniej niż 1GB i jest .mp3! Jeżeli to nie zadziała, odśwież stronę ;)'),
                  max_file_size=1_000_000) \
            .props('accept=.mp3') \
            .classes('max-w-full')

write_log("[info] UI Gotowe do uźytku, port 8080.")
ui.run()