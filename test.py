import requests

TOKEN = ""
API = ''

message = "test"

headers = {'Authorization': 'Bearer ' + TOKEN}
data = {'message': message}
requests.post(API, headers = headers, data = data)