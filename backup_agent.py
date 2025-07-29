import shutil
import datetime
from pathlib import Path
import os

# Use your actual project directory path below:
PROJECT_DIR = "F:/code/3dshapesnap-ui2/3dshapesnap-ui2"   # <-- EDIT if your path is different
BACKUP_DIR = "./backups"

def backup():
    # Create backups directory if it doesn't exist
    Path(BACKUP_DIR).mkdir(parents=True, exist_ok=True)

    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = Path(BACKUP_DIR) / f"backup-{dt}"
    try:
        shutil.copytree(PROJECT_DIR, backup_path, dirs_exist_ok=True)
        print(f"Backup created at {backup_path}")
    except Exception as e:
        print(f"Backup failed: {e}")
