import requests

TOKEN = ""
API = 'https://notify-api.line.me/api/notify'

with open(r"token.txt", "r") as f:
    TOKEN = f.read().replace("\n", "")


def send_message(message):
    headers = {'Authorization': 'Bearer ' + TOKEN}
    data = {'message': message}
    requests.post(API, headers = headers, data = data)

with open("../GPA/GPA.csv", "r") as f:
    GPA = f.read().split()
    send_message("成績を送るよ！")
    for message in GPA:
        send_message(message)
# message = "raspberry piから送信してるよ！"

