from linebot.v3.messaging.models import (
    ReplyMessageRequest,
    TextMessage,
    QuickReply,
    QuickReplyItem,
    MessageAction
)

def make_quick_reply(reply_token: str, text: str) -> ReplyMessageRequest:
    return ReplyMessageRequest(
        replyToken=reply_token,
        messages=[
            TextMessage(
                type="text",
                text=text,
                quickReply=QuickReply(
                    items=[
                        QuickReplyItem(
                            imageUrl=None,
                            action=MessageAction(label="📋 筆記清單", text="/筆記清單"),
                            type=None
                        ),
                        QuickReplyItem(
                            imageUrl=None,
                            action=MessageAction(label="🎂 誰的生日", text="你記得誰的生日"),
                            type=None
                        ),
                        QuickReplyItem(
                            imageUrl=None,
                            action=MessageAction(label="📅 狗狗週報", text="狗狗週報"),
                            type=None
                        ),
                        QuickReplyItem(
                            imageUrl=None,
                            action=MessageAction(label="❓ 幫助", text="/幫助"),
                            type=None
                        )
                    ]
                ),
                quoteToken=None
            )
        ],
        notificationDisabled=False
    )
