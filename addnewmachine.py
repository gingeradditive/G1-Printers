#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
import argparse

# ========================
#  Utility Functions
# ========================

def load_config(config_file="config.json"):
    """Carica il file di configurazione JSON."""
    if not os.path.exists(config_file):
        sys.exit(f"❌ File di configurazione '{config_file}' non trovato.")
    with open(config_file, "r") as f:
        return json.load(f)


def ask_machine_type(config):
    """Permette di selezionare il tipo di macchina."""
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
    """Suggerisce il prossimo seriale disponibile, ignorando quelli >9000."""
    dirs = [d for d in os.listdir(".") if os.path.isdir(d) and d.startswith(prefix + "-")]
    serial_numbers = []
    for d in dirs:
        try:
            parts = d.split("-")
            if len(parts) >= 3 and parts[0] == prefix:
                num = int(parts[1])
                if num < 9000:  # ignora macchine di test
                    serial_numbers.append(num)
        except ValueError:
            continue

    next_serial = max(serial_numbers, default=0) + 1
    year = datetime.now().year % 100  # ultime due cifre
    return f"{prefix}-{next_serial:04d}-{year:02d}"


def copy_template(template_folder, new_folder, dry_run=False):
    """Copia la cartella template nella nuova cartella."""
    if not os.path.exists(template_folder):
        sys.exit(f"❌ La cartella template '{template_folder}' non esiste.")
    if os.path.exists(new_folder):
        sys.exit(f"❌ La cartella di destinazione '{new_folder}' esiste già.")
    if dry_run:
        print(f"[DRY-RUN] Copierei la cartella da {template_folder} a {new_folder}")
    else:
        shutil.copytree(template_folder, new_folder)
        print(f"✅ Copiata cartella da {template_folder} a {new_folder}")


def git_commit_and_push(new_folder, dry_run=False):
    """Esegue add, commit e push Git."""
    commit_message = f"robot: add machine number {new_folder}"

    if dry_run:
        print(f"[DRY-RUN] Eseguirei: git add {new_folder}")
        print(f"[DRY-RUN] Eseguirei: git commit -m \"{commit_message}\"")
        print(f"[DRY-RUN] Eseguirei: git push")
        return

    subprocess.run(["git", "add", new_folder], check=True)
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    print("✅ Commit creato.")

    try:
        subprocess.run(["git", "push"], check=True)
        print("✅ Push completato.")
    except subprocess.CalledProcessError:
        print("⚠️ Push fallito. Controlla connessione o permessi Git.")


# ========================
#  Main Script
# ========================

def main():
    parser = argparse.ArgumentParser(
        description="Script per creare una nuova configurazione macchina (G1, G1 Rev2, ecc.)"
    )
    parser.add_argument("--dry-run", action="store_true", help="Simula le operazioni senza modificare nulla")
    parser.add_argument("--no-commit", action="store_true", help="Crea solo la cartella, senza fare commit o push Git")
    parser.add_argument("--type", type=int, help="Indice del tipo di macchina (1 = primo nel config.json)")
    parser.add_argument("--serial", type=str, help="Seriale macchina, es. G1-0025-25")

    args = parser.parse_args()

    print("=== Creazione nuova configurazione macchina ===")
    if args.dry_run:
        print("⚙️ Modalità DRY-RUN attiva (nessuna modifica effettiva).")
    if args.no_commit:
        print("⚙️ Modalità NO-COMMIT attiva (niente Git commit/push).")

    config = load_config()

    # --- Se specificato da CLI, salta wizard ---
    if args.type is not None:
        keys = list(config.keys())
        if args.type < 1 or args.type > len(keys):
            sys.exit(f"❌ Tipo macchina non valido. Usa un numero tra 1 e {len(keys)}.")
        model_name = keys[args.type - 1]
        model_conf = config[model_name]
        print(f"➡️  Selezionato tipo macchina: {model_name}")
    else:
        model_name, model_conf = ask_machine_type(config)

    # --- Serial ---
    if args.serial:
        serial = args.serial
    else:
        suggested_serial = suggest_serial(model_conf["prefix"])
        serial = input(f"Inserisci seriale [{suggested_serial}]: ").strip() or suggested_serial

    new_folder = serial

    copy_template(model_conf["template"], new_folder, dry_run=args.dry_run)

    if not args.no_commit:
        git_commit_and_push(new_folder, dry_run=args.dry_run)
    else:
        print("ℹ️ Commit e push saltati (--no-commit).")

    print(f"\n✅ Macchina '{serial}' pronta ({'simulazione' if args.dry_run else 'reale'})!\n")


if __name__ == "__main__":
    main()
