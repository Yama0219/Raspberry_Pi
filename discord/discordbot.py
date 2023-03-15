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
        await message.channel.send("../GPA/GPA.csv")


# Botの起動とDiscordサーバーへの接続
client.run(token=TOKEN)