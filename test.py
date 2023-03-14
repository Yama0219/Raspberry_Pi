import requests

TOKEN = ""
with open("token.txt", "r") as f:
    TOKEN = f.read()
    
API = 'https://notify-api.line.me/api/notify'

message = "test"

headers = {'Authorization': 'Bearer ' + TOKEN}
data = {'message': message}
requests.post(API, headers = headers, data = data)