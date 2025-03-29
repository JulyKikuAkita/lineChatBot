import json
from datetime import datetime, timedelta
import os

LOG_FILE = "message_log.json"

def log_message(user, text):
    log = load_log()
    log.append({
        "user": user,
        "text": text,
        "timestamp": datetime.now().isoformat()
    })
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

def load_log():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        return json.load(f)

def get_weekly_summary():
    log = load_log()
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    recent_msgs = [
        entry for entry in log
        if datetime.fromisoformat(entry["timestamp"]) >= week_ago
    ]

    if not recent_msgs:
        return "🐶 嗷嗚～這週大家都很安靜耶，狗狗也沒聽到什麼事呢。"

    lines = []
    for entry in recent_msgs:
        lines.append(f"- {entry['user']} 說：{entry['text']}")

    return f"""🐾 狗狗一週大總結 🐾

📅 本週有這些汪汪紀錄：
{chr(10).join(lines)}

🔔 下週提醒：
- 有生日我也會汪汪提醒！

汪！我會持續關注群組的風聲草動～下週見！🐶
"""
