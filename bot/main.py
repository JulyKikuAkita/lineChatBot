from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

from bot import wishes, messageHistory

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("FAMILY_LINE_CHANNEL_ACCESS_TOKEN"))
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    user_id = event.source.user_id if hasattr(event.source, "user_id") else "unknown"

    # 📝 記錄訊息（for 每週摘要）
    messageHistory.log_message(user_id, msg)

    # 🎂 處理生日訊息
    birthday_reply = wishes.handle_birthday_message(msg)
    if birthday_reply:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=birthday_reply)
        )
        return

    # 📆 群組說：狗狗週報
    if "狗狗週報" in msg or "汪汪總結" in msg:
        summary = messageHistory.get_weekly_summary()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=summary))
        return

    # 🐶 預設回應（狗狗語氣）
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="汪？我還不太懂這句話，要不要再說一次？🐶"),
    )


# 可加排程：每天早上自動送生日祝賀
def send_daily_birthday_wishes():
    messages = wishes.check_today_birthdays()
    group_id = "你的群組 ID"  # TODO: 替換成你的實際群組 ID
    for msg in messages:
        line_bot_api.push_message(group_id, TextSendMessage(text=msg))


if __name__ == "__main__":
    app.run()