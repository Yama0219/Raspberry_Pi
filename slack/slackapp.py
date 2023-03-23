import requests
import time
import datetime
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
import logging
import json

url = r"https://playground-gkh7524.slack.com/archives/D04UBP43RPZ"

with open(r"token.txt", "r", encoding="utf-8") as f:
    txt = f.read().split()
    bottoken = txt[0]
    apptoken = txt[1]
# logging.basicConfig(level=logging.DEBUG)
app = App(token=bottoken)

def get_dm_id(user_id):
    channels = app.client.conversations_list(types="im")["channels"]
    for channel in channels:
        if "user" in channel:
            if channel["user"] == user_id:
                return channel["id"]
    return None

@app.event("reaction_added")
def handle_reaction_added_events(event):
    print(get_dm_id(event["user"]))
    res = app.client.chat_postMessage(channel=get_dm_id(event["user"]), text="今リアクションしましたね！？")
    
@app.event("reaction_removed")
def handle_reaction_removed_events(event):
        res = app.client.chat_postMessage(channel=get_dm_id(event["user"]), text="なんでリアクション外すの？")


@app.message("alarm")
def message_hello(message, say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    tomorrow = datetime.datetime.timestamp(datetime.datetime.strptime((datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d") + " 7:00:00", '%Y-%m-%d %H:%M:%S'))
    print(message)
    say(text="時間を入力してね", 
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

@app.action("time_selected")
def action_button_click(body, ack, say):
    ack()
    time = ""
    message = ""
    parent_message_ts = body["container"]["message_ts"]
    parent_message_channel = body["channel"]["id"]
    for value in body["state"]["values"].values():
        if "plain_text_input-action" in value:
            message = value["plain_text_input-action"]["value"]
    
        if 'datetime_input' in value:
            time = value['datetime_input']['selected_date_time']

    try:
        res = app.client.chat_scheduleMessage(channel=parent_message_channel, post_at=time, text=f"{body['user']['id']}", 
                                        blocks=[
                                                {
                                                    "type": "section",
                                                    "text": {"type": "mrkdwn", "text": f"<@{body['user']['id']}>時間だよ!\n時刻：{datetime.datetime.fromtimestamp(time)}\nメモ：{message}"},
                                                    "accessory": {
                                                        "type": "button",
                                                        "text": {"type": "plain_text", "text":"確認しました"},
                                                        "action_id": "alarm_confirm"
                                                    }
                                                }
                                            ]
                                        )
    except SlackApiError as e: 
        app.client.chat_postMessage(channel=parent_message_channel, thread_ts=parent_message_ts, text=f"<@{body['user']['id']}>エラー：{e.response['error']}")
    else:
        app.client.chat_postMessage(channel=parent_message_channel, thread_ts=parent_message_ts, 
                                    text=f'"scheduled_message_id":"{res["scheduled_message_id"]}", "channel":"{parent_message_channel}", "user":"{res["message"]["text"]}", "thread_ts":{parent_message_ts}' ,
                                    blocks=[
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"<@{body['user']['id']}> {datetime.datetime.fromtimestamp(time)}を入力しました\nメッセージ:{message}"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "キャンセル"
				},
				"action_id": "cancel_alarm"
			}
		}
		
	])

@app.action("alarm_confirm")
def action_alarm_confirm(body, ack, say):
    # アクションを確認したことを即時で応答します
    ack()
    
    # チャンネルにメッセージを投稿します
    parent_message_ts = body["container"]["message_ts"]
    parent_message_channel = body["channel"]["id"]
    for_who = body["message"]["text"]
    who_clicked = body["user"]["id"]
    if (for_who == who_clicked):
        res = app.client.chat_postMessage(channel=parent_message_channel, thread_ts=parent_message_ts, 
                                    text="<@{}> {:02d}:{:02d}に確認されました！".format(body['user']['id'], datetime.datetime.now().hour, datetime.datetime.now().minute))
        print(res)
        app.client.reactions_add(channel=parent_message_channel, timestamp=res["ts"], name="eyes")
    else:
        app.client.chat_postMessage(channel=parent_message_channel, thread_ts=parent_message_ts, text="<@{}> に向けたメッセージだよ！".format(body['user']['id']))

@app.action("cancel_alarm")
def action_alarm_confirm(body, ack, say):
    # アクションを確認したことを即時で応答します
    ack()
    text=body["message"]["text"]
    print(body)
    data=json.loads("{"+text+"}")
    print(data)
    print(app.client.chat_scheduledMessages_list())
    
    try:
        res = app.client.chat_deleteScheduledMessage(channel=data["channel"], scheduled_message_id=data["scheduled_message_id"], as_user=True)
        app.client.chat_postMessage(channel=data["channel"], thread_ts=body["message"]["thread_ts"], text=f"<@{body['user']['id']}>取り消しました")
        app.client.chat_delete(channel=data["channel"], ts=body["message"]["ts"])
        print(res)
    except SlackApiError as e:
        app.client.chat_postMessage(channel=data["channel"], thread_ts=body["message"]["thread_ts"], text=f"<@{body['user']['id']}>操作に失敗しました:{e}")
# アプリを起動します
if __name__ == "__main__":
    handler = SocketModeHandler(app, apptoken)
    handler.start()