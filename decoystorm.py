#!/usr/bin/env python3

import os
import platform
import random
import json
import subprocess
from pathlib import Path

ARTIFACT_LOG = "/tmp/decoystorm_artifacts.json" if os.name != "nt" else "C:\\Temp\\decoystorm_artifacts.json"

# Utility Functions

def log_artifact(entry):
    try:
        data = []
        if os.path.exists(ARTIFACT_LOG):
            with open(ARTIFACT_LOG, "r") as f:
                data = json.load(f)

        data.append(entry)

        with open(ARTIFACT_LOG, "w") as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        print(f"[!] Failed to write to artifact log: {e}")


def os_name():
    """Return a simple OS name: windows or linux."""
    if os.name == "nt":
        return "windows"
    return "linux"


# Decoy File Generator

def create_decoy_file(path, content):
    """Create a harmless decoy file."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)

    log_artifact({"type": "file", "path": str(p)})
    print(f"[+] Created decoy file: {p}")


def seed_decoy_files():
    suspicious_names = [
        "payload.enc",
        "data_dump.raw",
        "exfiltration.zip",
        "credentials_backup.txt",
        "system_patch.ps1",
        "sync_module.py",
        "shadow_copy.log",
        "update_temp.bin"
    ]

    base = "C:\\ProgramData\\DecoyStorm" if os_name() == "windows" else "/var/tmp/decoystorm"

    for _ in range(8):
        name = random.choice(suspicious_names)
        path = os.path.join(base, name)
        create_decoy_file(path, "DECOY FILE – SAFE CONTENT\nThis file is intentionally harmless.")


# Decoy Script Generator

def seed_decoy_scripts():
    base = "C:\\ProgramData\\DecoyStorm\\scripts" if os_name() == "windows" else "/var/tmp/decoystorm/scripts"
    Path(base).mkdir(parents=True, exist_ok=True)

    fake_script = """#!/bin/bash
# DecoyStorm benign script
# Looks suspicious, does nothing harmful.
echo "DecoyStorm benign script executed."
"""

    script_path = os.path.join(base, "kworker_sync.sh")
    create_decoy_file(script_path, fake_script)


# Log Noise Generator

def generate_log_noise():
    log_path = "C:\\ProgramData\\DecoyStorm\\activity.log" if os_name() == "windows" else "/var/log/decoystorm.log"

    noise_entries = [
        "Beacon received: status=OK",
        "Sync module initiated...",
        "Scanning subsystem heartbeat...",
        "Exfil attempt: NO DATA FOUND",
        "Worker thread idle...",
        "Module check passed"
    ]

    with open(log_path, "a") as f:
        for _ in range(12):
            f.write(random.choice(noise_entries) + "\n")

    log_artifact({"type": "logfile", "path": log_path})
    print(f"Generated log noise: {log_path}")


# Scheduled Task / Cron Job

def schedule_task_windows():
    task_name = "WindowsUpdateHelper"
    cmd = 'schtasks /create /sc minute /mo 5 /tn {} /tr "cmd.exe /c echo UpdateCheck"'.format(task_name)

    subprocess.call(cmd, shell=True)
    log_artifact({"type": "task", "name": task_name})
    print("Created benign scheduled task.")


def schedule_task_linux():
    cron_line = "* * * * * echo 'DecoyStorm heartbeat' >> /var/tmp/decoystorm_heartbeat.log\n"

    cron_cmd = f'(crontab -l 2>/dev/null; echo "{cron_line}") | crontab -'
    os.system(cron_cmd)

    log_artifact({"type": "cronjob", "entry": cron_line.strip()})
    print("Added benign cron job.")


# Cleanup

def cleanup():
    if not os.path.exists(ARTIFACT_LOG):
        print("No artifact log found.")
        return

    with open(ARTIFACT_LOG, "r") as f:
        artifacts = json.load(f)

    for a in artifacts:
        if "path" in a and os.path.exists(a["path"]):
            print(f"[-] Removing {a['path']}")
            try:
                os.remove(a["path"])
            except:
                pass

    print("Cleanup complete.")
  

def main():
    print("=== DecoyStorm ===")
    system = os_name()
    print(f"[i] Running on: {system}")

    seed_decoy_files()
    seed_decoy_scripts()
    generate_log_noise()

    if system == "windows":
        schedule_task_windows()
    else:
        schedule_task_linux()

    print("DecoyStorm completed successfully.")


if __name__ == "__main__":
    main()
