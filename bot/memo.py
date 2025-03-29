import json
from pathlib import Path

MEMORY_FILE = Path(__file__).resolve().parent / "resources" / "memory.json"


def debug(msg):
    print(f"[🐾 memory debug] {msg}", flush=True)


def load_memory():
    if not MEMORY_FILE.exists():
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(data):
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def handle_memory_message(user_text):
    memory = load_memory()

    # ➕ 儲存：記住 [key] 是 [value]
    if user_text.startswith("記住") and "是" in user_text:
        try:
            stripped = user_text.replace("記住", "", 1).strip()
            key, value = stripped.split("是", 1)
            key = key.strip()
            value = value.strip()
            if not key or not value:
                return "汪？你要記什麼是什麼？格式是『記住 xxx 是 yyy』喔！"
            memory[key] = value
            save_memory(memory)
            return f"🐶 好的，我會記得 {key} 是 {value}！"
        except Exception as e:
            debug(f"記憶處理失敗: {e}")
            return "汪？我沒記起來耶，可以再說一次嗎？格式是『記住 xxx 是 yyy』"

    # 🔍 查詢：[key] 是什麼
    if user_text.endswith("是什麼") or user_text.endswith("是什麼？"):
        key = user_text.replace("是什麼", "").replace("？", "").strip()
        if key in memory:
            return f"🐾 {key} 是 {memory[key]}"
        else:
            return f"汪～我沒有記得 {key} 是什麼耶，要不要現在告訴我？"

    # ✨ 查詢所有記憶
    if user_text in ["我記得什麼", "/機密", "/secret"]:
        if not memory:
            return "🐶 我現在腦袋空空的，沒有記下任何小知識喔～"
        lines = [f"・{key}：{value}" for key, value in memory.items()]
        return "✨ 我記得這些機密喔：\n" + "\n".join(lines)

    return None
