import requests

TOKEN = ""
with open(r"token.txt", "r") as f:
    TOKEN = f.read().replace("\n", "")

API = 'https://notify-api.line.me/api/notify'

with open("../GPA/GPA.csv", "r") as f:
    message = f.read()

# message = "raspberry piから送信してるよ！"

headers = {'Authorization': 'Bearer ' + TOKEN}
data = {'message': message}
requests.post(API, headers = headers, data = data)