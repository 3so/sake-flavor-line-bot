import os
import sys

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

import reply_messages as rm

app = Flask(__name__)

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    search_condition = rm.search_brand(event)

    # 完全一致の銘柄が見つかり、フレーバー情報を持っている場合
    if search_condition[0] == 0:
        brand_name = search_condition[1]
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=("該当する銘柄が見つかりました。\n\n" + brand_name)),
                ImageSendMessage(
                    original_content_url='https://sake-flavor-line-bot.herokuapp.com/static/flavor_chart.png',
                    preview_image_url='https://sake-flavor-line-bot.herokuapp.com/static/flavor_chart.png'
                )
            ]
        )

    # 完全一致の銘柄が見つかり、フレーバー情報を持っていない場合
    if search_condition[0] == 1:
        brand_name = search_condition[1]
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=("該当する銘柄が見つかりました。\n\n" + brand_name)),
                TextSendMessage(text=("この銘柄のフレーバー情報はありません。"))
            ]
        )

    # 完全一致の銘柄、部分一致の銘柄ともに見つからなかった場合
    elif search_condition[0] == 2:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="一致する銘柄は見つかりませんでした。別の検索ワードをお試しください。")
        )

    # 完全一致の銘柄が見つからず、かつ部分一致の銘柄が31種類以上見つかった場合
    elif search_condition[0] == 3:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="一致する銘柄が見つかりませんでした。また、部分一致となる銘柄が多すぎます。別の検索ワードをお試しください。")
        )

    # 完全一致の銘柄が見つからず、かつ部分一致の銘柄が30種類以下見つかった場合
    elif search_condition[0] == 4:
        brand_list = search_condition[1]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=("該当する銘柄が見つかりませんでした。また、部分一致となる銘柄が複数見つかりました。以下の銘柄をお探しでしょうか？\n\n" + brand_list))
        )


#    line_bot_api.reply_message(
#        event.reply_token,
#        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()