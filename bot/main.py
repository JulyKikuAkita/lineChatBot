from flask import Flask, request, abort, jsonify
from linebot.v3.webhook import WebhookHandler, MessageEvent
from linebot.v3.webhooks import TextMessageContent
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi
from linebot.v3.exceptions import InvalidSignatureError
from pytz import timezone
from datetime import datetime
import logging
import os
import wishes
import messageHistory
import notes
import memo
from quick_reply_helper import make_quick_reply
from poetry_api import get_random_poem, get_short_poem, get_sonnet
from line_helpers import make_text_reply, build_birthday_push_requests
from sent_wishes import has_already_sent_today, mark_sent_today

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HELP_TEXT = (
    "📚 狗狗可以幫你做這些事情喔～\n\n"
    "📝 記事本功能：\n"
    "・記住筆記：xxx\n"
    "・記筆記請用格式：記住筆記：明天買菜\n"
    "・/筆記清單 → 查看筆記（分類顯示）\n"
    "・刪除筆記 N → 刪除第 N 筆\n\n"
    "🎂 生日紀錄：\n"
    "・記住 8月9日 是媽媽生日\n"
    "・媽媽生日是幾號？\n"
    "・你記得誰的生日\n\n"
    "🔑 常用的機密：\n"
    "・記住 wifi 是 12345678\n"
    "・wifi 是什麼？\n"
    "・地址是什麼？\n\n"
    "📅 週報功能：\n"
    "・狗狗週報 / 汪汪總結 → 查看這週摘要\n\n"
    "📜 詩詞功能：\n"
    "・/詩 或 來一首詩 → 從英文詩庫讀出一首\n\n"
    "🐾 其他：\n"
    "・/幫助 或 狗狗指令 → 顯示這份教學"
)

app = Flask(__name__)

configuration = Configuration(access_token=os.getenv("FAMILY_LINE_CHANNEL_ACCESS_TOKEN"))
api_client = ApiClient(configuration=configuration)
line_bot_api = MessagingApi(api_client)
handler = WebhookHandler(os.getenv("FAMILY_LINE_CHANNEL_SECRET"))


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


# we need to handle the message event with HEAD ping
@app.route("/trigger-birthday", methods=["GET", "HEAD"])
def trigger_birthday():
    send_daily_birthday_wishes()
    if request.method == "HEAD":
        return "", 200  # For UptimeRobot ping

    return jsonify(
        {
            "status": "ok",
            "timestamp": datetime.now(timezone("Asia/Taipei")).isoformat(),
        }
    )


# @handler.default()
# def default_handler(event):
#     print(f"⚠️ Received unhandled event: {type(event)}", flush=True)


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    msg = event.message.text
    user_id = event.source.user_id if hasattr(event.source, "user_id") else "unknown"
    print(event.source)

    logger.info(f"[RECEIVED] From {user_id}: {msg}")
    # 📝 記錄訊息（for 每週摘要）
    messageHistory.log_message(user_id, msg)
    # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # debug_reply = f"🐶 收到囉！你說的是：『{msg}』\n時間是：{timestamp}"
    # reply = make_text_reply(event.reply_token, debug_reply)
    # line_bot_api.reply_message(reply)

    # 📜 詩詞觸發 （使用 poetrydb）
    if msg.startswith("/詩") or "來一首詩" in msg or "random poem" in msg.lower():
        poem = get_random_poem()
        reply = make_text_reply(event.reply_token, poem)
        line_bot_api.reply_message(reply)
        return

    if msg.startswith("/短詩") or "/poem" in msg.lower():
        poem = get_short_poem()
        reply = make_text_reply(event.reply_token, poem)
        line_bot_api.reply_message(reply)
        return

    if msg.startswith("/十四行詩") or "/sonnet" in msg.lower():
        poem = get_sonnet()
        reply = make_text_reply(event.reply_token, poem)
        line_bot_api.reply_message(reply)
        return

    # 📆 群組說：狗狗週報
    if "狗狗週報" in msg or "汪汪總結" in msg:
        summary = messageHistory.get_weekly_summary()
        reply = make_text_reply(event.reply_token, summary)
        line_bot_api.reply_message(reply)
        return

    # 📖 教學指令
    if "/幫助" in msg or "狗狗指令" in msg or "/help" in msg.lower():
        fallback = "汪？我只會下面這些指令跟亂尿尿？🐶\n" "👇以下是我會的指令：\n" f"{HELP_TEXT}"
        reply = make_quick_reply(event.reply_token, fallback + "\n" + HELP_TEXT)
        line_bot_api.reply_message(reply)
        return

    # 🎂 處理生日訊息
    birthday_reply = wishes.handle_birthday_message(msg)
    if birthday_reply:
        reply = make_text_reply(event.reply_token, birthday_reply)
        line_bot_api.reply_message(reply)
        return

    # 🔑 機密
    memory_reply = memo.handle_memory_message(msg)
    if memory_reply:
        reply = make_text_reply(event.reply_token, memory_reply)
        line_bot_api.reply_message(reply)
        return

    # 📝 處理狗狗記事本：新增、列出、刪除
    note_reply = notes.handle_note_message(msg, user_id)
    if note_reply:
        reply = make_text_reply(event.reply_token, note_reply)
        line_bot_api.reply_message(reply)
        return


# 可加排程：每天早上自動送生日祝賀
def send_daily_birthday_wishes():
    if has_already_sent_today():
        print("🎂 今天已經送過生日祝福了，不再重複推播")
        return
        
    messages = wishes.check_today_birthdays_custom()
    group_id = os.getenv("FAMILY_LINE_CHANNEL_GROUPID")

    if not group_id:
        return "❗未設定 DEFAULT_GROUP_ID", 400

    print(f"🎂 生日推播觸發，共送出 {len(messages)} 則")
    push_requests = build_birthday_push_requests(messages, group_id)
    for item in push_requests:
        line_bot_api.push_message(item)
    mark_sent_today()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
