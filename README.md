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

A helper script called `new_machine.py` is provided to automate the creation of new machine configurations.  
It creates a new folder from the correct template, assigns the next available serial number, and optionally commits and pushes the changes to Git.

### Requirements
- Python 3.7 or higher  
- Git repository access with push permissions  
- A valid `config.json` file describing the machine models and templates

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
4. It will then commit and push the new configuration to Git

---

## ⚙️ Command-Line Options

| Option | Description |
|---------|--------------|
| `--dry-run` | Simulate all actions without making changes |
| `--no-commit` | Create the folder only, skip Git add/commit/push |
| `--help` | Show available options |

Example usage:
```bash
python3 new_machine.py --dry-run
python3 new_machine.py --no-commit
```

---

## 🧩 Notes
- Machines with serial numbers above **9000** are considered **test machines** and are ignored when generating the next available serial number.
- The script automatically prevents overwriting existing folders.
- Ensure you have write access to the repository before committing changes.

---

## 📄 License

© Ginger Additive.  
All rights reserved.  
This repository and its contents are proprietary and intended for internal use only.
