import sys
import json
import random
from datetime import datetime
from pytz import timezone
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

    return None


def check_today_birthdays_custom():
    tz = timezone("Asia/Taipei")
    today = datetime.now(tz).strftime("%m/%d")
    print(f"🐾 [Birthday Debug] 今天是：{today}")
    birthdays = load_birthdays()
    print(f"📦 [Birthday Debug] 載入生日資料：{birthdays}")
    wishes = []

    emoji_styles = [
        ["🐾", "🐶", "🐹", "🐰", "🐻"],
        ["🎁", "💖", "🍰", "🎂", "🧁"],
        ["🎊", "🌟", "🎉", "🎈", "✨"],
        ["🪅", "🎇", "🎆", "🌟", "✨"],
    ]

    mainText = "{name} 生日快樂!"
    templates = [
        "十萬青年十萬肝，但你生日我擋班。願你今年少爆肝，多領紅包不還單。",
        "年年生日都包金。雖然只夠買珍奶，但喝起來就甘心。",
        "今日宜耍廢，宜與外送言歡。願你被奶茶溫柔以待，被狗狗視為主子，被老闆誤認為天才。",
        "願你煩惱像髮量一樣稀少！",
        "今日宜喜，宜緩，宜與歲月言歡。願你眉眼如初，風不驚心，雨不傷身。新歲更懂自己，也更被世界溫柔以待。",
        "汪步輕隨入夢來，君生之日月明開。千帆過盡皆無憾，只願君心樂自懷。",
        "風起時，請記得加件衣；我們未必常在，但惦記從不間斷。",
    ]

    def normalize(date_str):
        parts = date_str.strip().split("/")
        return f"{int(parts[0])}/{int(parts[1])}"

    def build_border(characters, length):
        return "".join(random.choices(characters, k=length))

    for name, date in birthdays.items():
        match = normalize(date) == normalize(today)
        print(f"🔍 檢查 {name} 的生日：{date} 是否等於今天？→ {match}")
        if match:
            message_text = mainText.format(name=name)
            style = random.choice(emoji_styles)
            max_length = 10
            line_length = min(len(message_text), max_length)
            border_line = build_border(style, line_length)
            center = f" {message_text} "
            top = f"{border_line}"
            bottom = f"{border_line}"
            wishes.append(f"{top}\n{center}\n{bottom}\n")
            wishes.append("祝你 " + random.choice(templates))
            print(f"✅ 已加入祝福：{name}")
    return wishes
