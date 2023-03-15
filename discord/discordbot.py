import discord
from discord import Intents
import pandas as pd
from matplotlib import pyplot as plt
import japanize_matplotlib

TOKEN = ""
with open("token.txt", "r") as f:
    TOKEN = f.read().replace("\n", "")

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')

    if message.content == "/成績表":
            df = pd.read_csv("../GPA/GPA.csv", names = [str(i) for i in range(18)])
            df.fillna("")
            print(df)
            
            with open("../GPA/GPA.csv", "r") as f:
                GPA = f.read()
                await message.channel.send('成績表を送るよ！')
                for txt in GPA:
                    await message.channel.send(txt)


# Botの起動とDiscordサーバーへの接続
client.run(token=TOKEN)