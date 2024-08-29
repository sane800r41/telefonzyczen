import threading
import subprocess

def run_telefon_script():
    subprocess.run(["python", "flowBudkaTelefonicznaTelefon.py"])

def run_ui_script():
    subprocess.run(["python", "flowBudkaTelefonicznaUI.py"])

if __name__ == "__main__":
    # Create threads for each script
    telefon_thread = threading.Thread(target=run_telefon_script)
    ui_thread = threading.Thread(target=run_ui_script)

    # Start the threads
    telefon_thread.start()
    ui_thread.start()

    # Wait for both threads to complete
    telefon_thread.join()
    ui_thread.join()
