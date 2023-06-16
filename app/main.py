import configparser
from pathlib import Path
from typing import Union

from fastapi import FastAPI, HTTPException, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

dir_path = Path(__file__).resolve().parent
config = configparser.ConfigParser()
config.read("{}/config.ini".format(dir_path))

# Line Bot config
CHANNEL_SECRET = config.get("Line", "channel_secret")
CHANNEL_ACCESS_TOKEN = config.get("Line", "channel_access_token")

app = FastAPI()

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.post("/")
async def echoBot(request: Request):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameters")
    return "OK"


@handler.add(MessageEvent, message=(TextMessage))
def handling_message(event):
    replyToken = event.reply_token

    if isinstance(event.message, TextMessage):
        messages = event.message.text

        echoMessages = TextSendMessage(text=messages)
        line_bot_api.reply_message(
            reply_token=replyToken, messages=echoMessages
        )


@app.get("/")
def read_root():
    return {"Hello": config.get("Line", "channel_access_token")}
