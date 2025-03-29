from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

from birthday import handle_birthday_message, check_today_birthdays

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

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

    # 優先處理生日指令
    birthday_reply = handle_birthday_message(msg)
    if birthday_reply:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=birthday_reply))
        return

    # 其他預設回應
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="黛玉不懂此語，汝可再細說？🌿"))

# 可加排程：每天早上發生日祝賀
def send_daily_birthday_wishes():
    messages = check_today_birthdays()
    group_id = "你的群組 ID"  # 可替換成你群組的 ID 或從事件中存起來
    for msg in messages:
        line_bot_api.push_message(group_id, TextSendMessage(text=msg))

if __name__ == "__main__":
    app.run()