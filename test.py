import requests

TOKEN = input("token:")
API = 'https://notify-api.line.me/api/notify'

message = "test"

headers = {'Authorization': 'Bearer ' + TOKEN}
data = {'message': message}
requests.post(API, headers = headers, data = data)