import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

NOTES_FILE = Path(__file__).resolve().parent / "resources" / "notes.json"


def debug(msg):
    print(f"[🐾 note debug] {msg}", flush=True)


def load_notes():
    if not NOTES_FILE.exists():
        return []
    with open(NOTES_FILE, "r") as f:
        return json.load(f)


def save_notes(notes):
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


def handle_note_message(user_text, user_id="unknown"):
    notes = load_notes()

    # ➕ 新增筆記
    if "記住筆記" in user_text:
        try:
            if "：" in user_text:
                content = user_text.split("記住筆記：")[-1].strip()
            else:
                return "汪～你要記什麼筆記呢？請用『記住筆記：內容』的格式來教我！🐾"
            if not content:
                return "汪？筆記內容好像是空的耶，要不要再說一次？"

            notes.append(
                {"user": user_id, "text": content, "timestamp": datetime.now().isoformat()}
            )
            save_notes(notes)
            return f"🐶 筆記我記下來了喔：『{content}』"
        except Exception as e:
            debug(f"記筆記時錯誤: {e}")
            return "嗚嗚，我記筆記時出錯了…可以再試一次嗎？"

    # 📋 分類顯示所有筆記
    if "有哪些筆記" in user_text or "列出筆記" in user_text or "/筆記清單" in user_text:
        if not notes:
            return "🐶 我目前腦袋空空的，沒有記下任何筆記喔～"

        grouped = defaultdict(list)
        for note in notes:
            grouped[note["user"]].append(note["text"])

        lines = []
        for user, items in grouped.items():
            lines.append(f"🐾 {user} 的筆記：")
            for i, text in enumerate(items):
                lines.append(f"  {i+1}. {text}")

        return "📝 狗狗記事本整理如下\n" + "".join(lines)

    # 🗑 刪除筆記 by 編號（整體 index）
    if "刪除筆記" in user_text:
        try:
            index = int(user_text.split("刪除筆記")[-1].strip()) - 1
            if 0 <= index < len(notes):
                deleted = notes.pop(index)
                save_notes(notes)
                return f"🗑 汪～我已經刪除了這則筆記：『{deleted['text']}』"
            else:
                return f"汪？我找不到第 {index+1} 筆筆記耶，可以再確認一下嗎？"
        except Exception as e:
            debug(f"刪除筆記時錯誤: {e}")
            return "嗚嗚，我沒刪成功耶…請確認格式是『刪除筆記 2』這樣。"

    return None
