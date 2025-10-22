# Ginger Additive Machine Configurations

This repository contains the configuration files and directories for all machines produced by **Ginger Additive**.  
Each machine configuration is stored in its own folder, named according to its serial number, e.g.:

```
G1-0020-25/
G1R2-0042-25/
G1R2-0105-25/
```

The serial number format follows the pattern:
```
[prefix]-[incremental_serial]-[year]
```
For example: `G1R2-0042-25` → model **G1 Rev2**, serial number **42**, year **2025**.

---

## 🧰 Adding a New Machine Configuration

A helper script called `addnewmachine.py` automates the creation of new machine configuration folders.  
It copies the correct template, assigns or accepts a serial number, and can optionally commit and push the changes to Git.

---

### 🧩 Requirements

- Python **3.7** or higher  
- Git repository access with push permissions  
- A valid `config.json` file describing machine models and templates  

Example `config.json`:

```json
{
  "G1 Rev1": {
    "template": "G1-TEMPLATE",
    "prefix": "G1"
  },
  "G1 Rev2": {
    "template": "G1R2-TEMPLATE",
    "prefix": "G1R2"
  },
  "G1 Rev2 (Servo)": {
    "template": "G1R2-TEMPLATESERVO",
    "prefix": "G1R2"
  }
}
```

---

## 🚀 Usage

Run the script from the root of the repository:

```bash
python3 new_machine.py
```

You will be prompted to:
1. Select the machine type (e.g. G1 Rev1, G1 Rev2, etc.)
2. Confirm or override the suggested serial number
3. The script will copy the appropriate template and create a new folder
4. Optionally, it will commit and push the new configuration to Git

---

## ⚙️ Command-Line Options

| Option | Description |
|---------|-------------|
| `--type <N>` | Select the machine type by index (1 = first entry in `config.json`) |
| `--serial <SERIAL>` | Specify the serial directly (e.g. `G1-0025-25`) |
| `--dry-run` | Simulate all actions without making any changes |
| `--no-commit` | Create the folder only, skip Git add/commit/push |
| `--help` | Show all available options |

---

### 🧠 Examples

**Interactive mode (default):**
```bash
python3 new_machine.py
```

**Fully automated (non-interactive):**
```bash
python3 new_machine.py --type 2 --serial G1R2-0042-25
```

**Simulate actions without writing anything:**
```bash
python3 new_machine.py --type 1 --serial G1-0100-25 --dry-run
```

**Skip Git operations:**
```bash
python3 new_machine.py --type 3 --serial G1R2-0075-25 --no-commit
```

---

## 🧩 Notes

- Machines with serial numbers above **9000** are considered **test machines** and are ignored when generating the next available serial.
- The script prevents overwriting existing folders.
- Ensure you have Git commit and push permissions before running the script.
- The year suffix in the serial number is automatically derived from the current year.

---

## 📄 License

© **Ginger Additive**.  
All rights reserved.  
This repository and its contents are proprietary and intended for internal use only.
