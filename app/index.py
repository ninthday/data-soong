import configparser
from pathlib import Path
from typing import Union

from fastapi import FastAPI, HTTPException, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    StickerMessage,
    TextMessage,
    TextSendMessage,
)

dir_path = Path(__file__).resolve().parent
config = configparser.ConfigParser()
config.read("{}/config.ini".format(dir_path))

# Line Bot config
CHANNEL_SECRET = config.get("Line", "channel_secret")
CHANNEL_ACCESS_TOKEN = config.get("Line", "channel_access_token")

app = FastAPI()

linebot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.post("/")
async def echo_bot(request: Request):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameters")
    return "OK"


# https://github.com/line/line-bot-sdk-python#message


@handler.add(MessageEvent, message=(TextMessage))
def handling_message(event):
    replyToken = event.reply_token

    if isinstance(event.message, TextMessage):
        messages = "嗡~{}".format(event.message.text)
        # print(event)

        echoMessages = TextSendMessage(text=messages)
        linebot_api.reply_message(reply_token=replyToken, messages=echoMessages)


@handler.add(MessageEvent, message=(StickerMessage))
def staiker_message(event):
    replyToken = event.reply_token

    if isinstance(event.message, StickerMessage):
        messages = "嗡~{}".format(event.message.sticker_id)

        echoMessages = TextSendMessage(text=messages)
        linebot_api.reply_message(reply_token=replyToken, messages=echoMessages)


@app.get("/")
def read_root():
    # return {"Hello": config.get("Line", "channel_access_token")}
    return {"Hello": "world!"}
