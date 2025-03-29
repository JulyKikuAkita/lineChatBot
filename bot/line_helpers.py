# bot/line_helpers.py
from linebot.v3.messaging.models import ReplyMessageRequest, PushMessageRequest, TextMessage
import wishes

def make_text_reply(reply_token: str, text: str, disable_notification=False) -> ReplyMessageRequest:
    return ReplyMessageRequest(
        replyToken=reply_token,
        messages=[
            TextMessage(
                type="text",
                text=text,
                quickReply=None,
                quoteToken=None
            )
        ],
        notificationDisabled=disable_notification
    )

def build_birthday_push_requests(group_id: str) -> list[PushMessageRequest]:
    messages = wishes.check_today_birthdays()
    push_requests = []

    for msg in messages:
        push_requests.append(
            PushMessageRequest(
                to=group_id,
                messages=[
                    TextMessage(
                        type="text",
                        text=msg,
                        quickReply=None,
                        quoteToken=None
                    )
                ],
                notificationDisabled=False,
                customAggregationUnits=None
            )
        )

    return push_requests