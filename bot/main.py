from flask import Flask, request, abort
from linebot.v3.webhook import WebhookHandler, MessageEvent
from linebot.v3.webhooks import TextMessageContent
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, TextMessage
from linebot.v3.exceptions import InvalidSignatureError
from datetime import datetime
import sys
import os
import wishes
import messageHistory
from line_helpers import make_text_reply
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# @handler.default()
# def default_handler(event):
#     print(f"⚠️ Received unhandled event: {type(event)}", flush=True)
    
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    msg = event.message.text
    user_id = event.source.user_id if hasattr(event.source, "user_id") else "unknown"

    logger.info(f"[RECEIVED] From {user_id}: {msg}")
    # 📝 記錄訊息（for 每週摘要）
    messageHistory.log_message(user_id, msg)
    print(f"[RECEIVED] From {user_id}: {msg}")
    # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # debug_reply = f"🐶 收到囉！你說的是：『{msg}』\n時間是：{timestamp}"
    # reply = make_text_reply(event.reply_token, debug_reply)
    # line_bot_api.reply_message(reply)

    # 🎂 處理生日訊息
    birthday_reply = wishes.handle_birthday_message(msg)
    if birthday_reply:
        reply = make_text_reply(event.reply_token, birthday_reply)
        line_bot_api.reply_message(reply)
        return

    # 📆 群組說：狗狗週報
    if "狗狗週報" in msg or "汪汪總結" in msg:
        summary = messageHistory.get_weekly_summary()
        reply = make_text_reply(event.reply_token, summary)
        line_bot_api.reply_message(reply)
        return

    # 🐶 預設回應（狗狗語氣）
    defaultMessage = "汪？我還不太懂這句話，要不要再說一次？🐶"
    reply = make_text_reply(event.reply_token, defaultMessage)
    line_bot_api.reply_message(reply)

# 可加排程：每天早上自動送生日祝賀
# def send_daily_birthday_wishes():
#     messages = wishes.check_today_birthdays()
#     group_id = "你的群組 ID"  # TODO: 替換成你的實際群組 ID
#     for msg in messages:
#         line_bot_api.push_message(group_id, TextSendMessage(text=msg))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)