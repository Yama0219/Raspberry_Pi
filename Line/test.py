import requests
import pandas as pd
from matplotlib import pyplot as plt
import my_tools

TOKEN = ""
API = 'https://notify-api.line.me/api/notify'

with open(r"token.txt", "r") as f:
    TOKEN = f.read().replace("\n", "")


def send_message(message):
    headers = {'Authorization': 'Bearer ' + TOKEN}
    data = {'message': message}
    requests.post(API, headers = headers, data = data)


def send_GPA():
    df = pd.read_csv("../GPA/GPA.csv", names = [str(i) for i in range(18)])
    print(df)
    my_tools.TablePlot(df, 1000, 1000, "GPA_table.jpg")
    with open("../GPA/GPA.csv", "r") as f:
        GPA = f.read()
        send_message("成績を送るよ！")
        send_message(GPA)
# message = "raspberry piから送信してるよ！"

send_GPA()