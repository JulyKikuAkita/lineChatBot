import json
from datetime import datetime, timedelta
from collections import Counter
import os
import sys

LOG_FILE = "message_log.json"


def debug(msg):
    print(f"[🐾 birthday debug] {msg}", file=sys.stdout, flush=True)


def log_message(user, text):
    log = load_log()
    log.append({"user": user, "text": text, "timestamp": datetime.now().isoformat()})
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def load_log():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        return json.load(f)


def is_noise(text: str) -> bool:
    command_keywords = ["記住", "狗狗週報", "你記得誰的生日", "生日是幾號", "汪汪總結"]
    return any(keyword in text for keyword in command_keywords)


def get_weekly_summary():
    log = load_log()
    now = datetime.now()
    week_ago = now - timedelta(days=7)

    recent_msgs = [
        entry
        for entry in log
        if datetime.fromisoformat(entry["timestamp"]) >= week_ago and not is_noise(entry["text"])
    ]

    # Remove duplicates
    seen = set()
    unique_msgs = []
    for entry in recent_msgs:
        key = (entry["user"], entry["text"].strip())
        if key not in seen:
            seen.add(key)
            unique_msgs.append(entry)

    if not unique_msgs:
        return "🐶 嗷嗚～這週大家都很安靜耶，狗狗也沒聽到什麼事呢。"

    # Statistics
    user_counts = Counter(entry["user"] for entry in unique_msgs)
    total_msgs = len(unique_msgs)
    top_user, top_count = user_counts.most_common(1)[0]

    lines = []
    for entry in unique_msgs:
        lines.append(f"- 🗣️ {entry['user']}：{entry['text']}")

    summary = f"""🐾 狗狗一週大總結 🐾

📊 訊息統計：
- 總共有 {total_msgs} 則訊息被記錄下來
- 最活躍的是：{top_user}（發了 {top_count} 則訊息）🎉

📅 精選內容：
{chr(10).join(lines)}

🐶 下週也請多多指教汪～記得要餵狗狗罐罐～
"""

    return summary
