import sys
import json
from datetime import datetime
from pathlib import Path

BIRTHDAY_FILE = Path(__file__).resolve().parent / "resources" / "birthdays.json"


def debug(msg):
    print(f"[🐾 birthday debug] {msg}", file=sys.stdout, flush=True)


def load_birthdays():
    try:
        with open(BIRTHDAY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_birthdays(birthdays):
    with open(BIRTHDAY_FILE, "w") as f:
        json.dump(birthdays, f, ensure_ascii=False, indent=2)


def handle_birthday_message(user_text):
    debug(f"Handling: {user_text}")
    birthdays = load_birthdays()

    if "記住" in user_text and "是" in user_text and "生日" in user_text:
        try:
            parts = user_text.split("記住")[1].strip()
            debug(f"After '記住': {parts}")

            date_part, name_part = parts.split("是")
            debug(f"Split date/name: {date_part.strip()} / {name_part.strip()}")

            # Try normalizing
            date_str = (
                date_part.strip()
                .replace("月", "/")
                .replace("日", "")
                .replace("號", "")
                .replace(" ", "")
            )
            name = name_part.replace("生日", "").strip()

            debug(f"Parsed date: {date_str}, name: {name}")

            # Simple validation
            if "/" not in date_str:
                debug("⚠️ Invalid date format")
                return "汪？我不太懂這個日期，可以像『記住 3月29日 是媽媽生日』這樣嗎？"

            birthdays[name] = date_str
            save_birthdays(birthdays)
            return f"🐶 嗷嗚～我記住啦！{name} 的生日是 {date_str}，到時我會送上狗狗的祝福喔！"
        except Exception as e:
            debug(f"❌ Exception while parsing: {e}")
            return "汪？我有點聽不懂…可以像這樣說『記住 3月29日 是媽媽生日』嗎？"

    if "生日" in user_text and "是幾號" in user_text:
        for name, date in birthdays.items():
            if name in user_text:
                return f"🐾 汪！{name} 的生日是 {date}，我有記在狗狗腦袋裡喔～"
        return "嗚…我找不到那個生日耶，要不要再幫我記一次？"

    if "你記得誰的生日" in user_text or "誰的生日" in user_text:
        if not birthdays:
            return "嗚…我還沒有記下任何生日耶～可以教我嗎？🐶"

        lines = [f"{name}：{date}" for name, date in birthdays.items()]
        return "🐶 我記得這些人的生日喔～\n" + "\n".join(lines)

    return "汪？我聽不懂這句話呢，可以問我記得誰的生日？"


def check_today_birthdays():
    today = datetime.now().strftime("%m/%d")
    birthdays = load_birthdays()
    messages = []
    for name, date in birthdays.items():
        if date == today:
            messages.append(f"🎉 汪汪！今天是 {name} 的生日～祝你骨頭吃到飽、玩具永不壞！🎂")
    return messages
