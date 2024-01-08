from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction,
)

app = Flask(__name__)

line_bot_api = LineBotApi('0K8z0A+v+xpOwM8NgqqxdTzSmC+Rz2T09khsQadPEnkIkg0SC782CTER3DCZXXcFnMjfeyjIGfJ8yneMk1zIx2CVRY0JuQZfrpV0v/LkphvMxv2npCslguHHlmtaEyHQFHRN9PpuIgwhfREQmbMKvwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('70c86cb84be67babf7164dee4ebcab28')

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
    if(event.message.text=="語音模型"):
        line_bot_api.reply_message(event.reply_token,
            TemplateSendMessage(
                alt_text='ButtonsTemplate',
                template=ButtonsTemplate(
                    # thumbnail_image_url='',
                    title='語音模型',
                    text='選擇動作',
                    actions=[
                        PostbackAction(
                            label='測試模型準確度',
                            data='發送 postback'
                        ),
                        MessageAction(
                            label='訓練新模型',
                            text='hello'
                        )
                    ]
                )
            )
        )
    if(event.message.text=="使用飲水機"):
        line_bot_api.reply_message(event.reply_token,
            TemplateSendMessage(
                alt_text='ButtonsTemplate',
                template=ButtonsTemplate(
                    # thumbnail_image_url='',
                    title='飲水機',
                    text='選擇動作',
                    actions=[
                        PostbackAction(
                            label='出水',
                            data='發送 postback'
                        ),
                        MessageAction(
                            label='停止',
                            text='hello'
                        )
                    ]
                )
            )
        )
    if(event.message.text=="查詢今日飲水量"):
        message=TextSendMessage("回覆3")
        line_bot_api.reply_message(
        event.reply_token,
            message)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5566)