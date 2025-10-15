import json
import os
import shutil
import subprocess
from datetime import datetime

def load_config(config_file="config.json"):
    with open(config_file, "r") as f:
        return json.load(f)

def ask_machine_type(config):
    print("Seleziona il tipo di macchina:")
    for i, key in enumerate(config.keys(), start=1):
        print(f"{i}) {key}")
    while True:
        choice = input("Scelta (1-3): ").strip()
        if choice in [str(i) for i in range(1, len(config) + 1)]:
            key = list(config.keys())[int(choice) - 1]
            return key, config[key]
        else:
            print("Scelta non valida, riprova.")

def suggest_serial(prefix):
    dirs = [d for d in os.listdir(".") if os.path.isdir(d) and d.startswith(prefix + "-")]
    serial_numbers = []
    for d in dirs:
        try:
            parts = d.split("-")
            if len(parts) >= 3 and parts[0] == prefix:
                serial_numbers.append(int(parts[1]))
        except ValueError:
            continue

    next_serial = max(serial_numbers, default=0) + 1
    year = datetime.now().year % 100  # solo le ultime due cifre
    return f"{prefix}-{next_serial:04d}-{year:02d}"

def copy_template(template_folder, new_folder):
    if not os.path.exists(template_folder):
        raise FileNotFoundError(f"La cartella template '{template_folder}' non esiste.")
    shutil.copytree(template_folder, new_folder)
    print(f"✅ Copiata cartella da {template_folder} a {new_folder}")

def git_commit_and_push(new_folder):
    subprocess.run(["git", "add", new_folder], check=True)
    commit_message = f"robot: add machine number {new_folder}"
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    print("✅ Commit creato.")
    try:
        subprocess.run(["git", "push"], check=True)
        print("✅ Push completato.")
    except subprocess.CalledProcessError:
        print("⚠️ Push fallito. Controlla la connessione o i permessi Git.")

def main():
    print("=== Creazione nuova configurazione macchina ===")
    config = load_config()
    model_name, model_conf = ask_machine_type(config)

    suggested_serial = suggest_serial(model_conf["prefix"])
    serial = input(f"Inserisci seriale [{suggested_serial}]: ").strip() or suggested_serial

    new_folder = serial
    copy_template(model_conf["template"], new_folder)

    git_commit_and_push(new_folder)
    print(f"\n✅ Macchina '{serial}' creata e pushata con successo!\n")

if __name__ == "__main__":
    main()
