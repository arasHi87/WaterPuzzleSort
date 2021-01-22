import os
import subprocess
from utils import *
from dotenv import load_dotenv
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

load_dotenv()
app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


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


@handler.add(MessageEvent)
def handle_message(event):
    if event.message.type == 'image':
        img = line_bot_api.get_message_content(event.message.id)
        user_id = event.source.user_id

        with open('imgs/{}.jpg'.format(user_id), 'wb+') as fp:
            for chunk in img.iter_content():
                fp.write(chunk)

        tubes = label_color('imgs/{}.jpg'.format(user_id))
        tubes = format_color(merge_color(tubes))
        case = list()

        for tube in tubes:
            for block in tube:
                case.append("{} {}".format(block[0], block[1]))
       
        output = subprocess.run('./sol',
                input="\n".join(case),
                universal_newlines = True,
		stdout = subprocess.PIPE).stdout.splitlines()
        ans = "Total have {} steps\n".format(len(output))
        idx = 1

        for step in output:
            ans += "Step {}. {}\n".format(idx, step)
            idx += 1

        os.remove('imgs/{}.jpg'.format(user_id))
    
        line_bot_api.reply_message(
	    event.reply_token,
	    TextSendMessage(text=ans))

if __name__ == "__main__":
    app.run()
