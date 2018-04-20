from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import oil_price

app = Flask(__name__)

line_bot_api = LineBotApi('zsBI+cGhchpR7I998XlgkKsX2bpANDR7PLEwOH3bUsAKnJ7TCY4aUiBTO5PSSb9dEsCXvYCTTqJ2FK9nXtx7OIbSzh7Zkl13avsSbswy8ms7AhiRAXn1Vm+f6FU6hIgGFuGH3ppCGmuxP5tBqeTWLQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('949751303901deead8ebda134e7f7c78')


@app.route("/", methods=['GET'])
def default_action():
    return 'Hello World'


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == 'ราคาน้ำมัน':
        l = oil_price.get_prices()
        s = ""
        for p in l:
            s += "%s %.2f บาท\n"%(p[0],p[1])

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=s))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text + 'จ้า'))


if __name__ == "__main__":
    app.run()