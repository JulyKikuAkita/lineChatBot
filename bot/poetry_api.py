# bot/poetry_english.py
import requests
import random
import sys

MAX_LENGTH = 600


def debug(msg):
    print(f"[🐾 poetry debug] {msg}", file=sys.stdout, flush=True)


def get_random_poem():
    try:
        res = requests.get("https://poetrydb.org/random")
        res.raise_for_status()
        poem = res.json()[0]
        return format_poem(poem)
    except Exception as e:
        return f"🐶 嗷嗚～我找詩的時候出錯了：{e}"


def get_short_poem(max_lines=12):
    try:
        for _ in range(5):  # Try a few times to find a short one
            res = requests.get("https://poetrydb.org/random")
            res.raise_for_status()
            poem = res.json()[0]
            if len(poem["lines"]) <= max_lines:
                return format_poem(poem)
        return "🐶 今天找不到短詩耶～要不要換個主題？"
    except Exception as e:
        return f"🐶 嗷嗚～我找詩的時候出錯了：{e}"


def get_sonnet():
    try:
        res = requests.get("https://poetrydb.org/author/Shakespeare")
        res.raise_for_status()
        all_poems = res.json()
        sonnets = [p for p in all_poems if "sonnet" in p["title"].lower()]
        if not sonnets:
            return "🐶 沒找到莎士比亞十四行詩呢～"

        poem = random.choice(sonnets)
        return format_poem(poem)
    except Exception as e:
        return f"🐶 嗷嗚～我找詩的時候出錯了：{e}"


def format_poem(poem):
    title = poem["title"]
    author = poem["author"]
    lines = "\n".join(poem["lines"])
    full_text = f"📜 *{title}* by {author}\n\n{lines}"
    return full_text[:MAX_LENGTH]
