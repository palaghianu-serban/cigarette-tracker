import os
import time

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP_DIR = os.path.join(PROJECT_DIR, "backups")

def cleanup_old_backups():
    if not os.path.exists(BACKUP_DIR):
        print("No backup directory found.")
        return

    backups = [os.path.join(BACKUP_DIR, f) for f in os.listdir(BACKUP_DIR) if f.endswith(".db")]
    backups.sort(key=os.path.getmtime)  # Oldest first

    # Only delete if there are more than 10 backups
    if len(backups) <= 10:
        print("10 or fewer backups found, nothing deleted.")
        return

    one_week_ago = time.time() - 7 * 24 * 60 * 60
    to_delete = [f for f in backups if os.path.getmtime(f) < one_week_ago]

    # Only delete enough to keep 10 backups
    if len(backups) - len(to_delete) < 10:
        to_delete = backups[:len(backups) - 10]

    for f in to_delete:
        try:
            os.remove(f)
            print(f"Deleted old backup: {f}")
        except Exception as e:
            print(f"Error deleting {f}: {e}")

if __name__ == "__main__":
    cleanup_old_backups()