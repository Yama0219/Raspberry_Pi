import datetime
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
import logging

url = r"https://playground-gkh7524.slack.com/archives/D04UBP43RPZ"

with open(r"C:\Users\kenke\Desktop\programming\python\slack\token.txt", "r") as f:
    txt = f.read().split()
    bottoken = txt[0]
    apptoken = txt[1]
logging.basicConfig(level=logging.DEBUG)
app = App(token=bottoken)

app.client.chat_postMessage(channel="C04UUMG1WSG" , text="<!here>皆さん今日も1日お疲れさまでした！\n明日は何時に起きますか？")
tomorrow = datetime.datetime.timestamp(datetime.datetime.strptime((datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d") + " 7:00:00", '%Y-%m-%d %H:%M:%S'))
app.client.chat_postMessage(channel="C04UUMG1WSG" , text="時間を入力してね", 
blocks = [
    {
        "type": "input",
        "element": {
            "type": "datetimepicker",
            "action_id": "datetime_input",
            "initial_date_time": int(tomorrow)
        },
        "label": {
            "type": "plain_text",
            "text": "Pick a date & time"
        }
    },
    {
        "type": "input",
        "element": {
            "type": "plain_text_input",
            "action_id": "plain_text_input-action"
        },
        "label": {
            "type": "plain_text",
            "text": "MEMO",
            "emoji": True
        }
    },
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "確認",
                    "emoji": True
                },
                "value": "click_me_123",
                "action_id": "time_selected"
            }
        ]
    }

]
)
