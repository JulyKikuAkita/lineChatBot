from datetime import datetime
from pathlib import Path

STATUS_FILE = Path(__file__).resolve().parent / "resources" / "birthday_sent_today.txt"


def has_already_sent_today():
    if STATUS_FILE.exists():
        sent_date = STATUS_FILE.read_text().strip()
        today = datetime.now().strftime("%Y-%m-%d")
        return sent_date == today
    return False


def mark_sent_today():
    today = datetime.now().strftime("%Y-%m-%d")
    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATUS_FILE.write_text(today)
