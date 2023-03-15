import discord
from discord import Intents
import pandas as pd
import os
import sys

sys.path.append(os.pardir)
TOKEN = ""

import GPA

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

    if message.content == "/GPA":
        await message.channel.send('成績表を送信するよ')
        await message.channel.send(file=discord.File("../GPA/GPA.csv"))

    if message.content == "/updateGPA":
        await message.channel.send('成績表を更新するよ')
        await message.channel.send(file=discord.File("../GPA/GPA.csv"))
        GPA.main()
# Botの起動とDiscordサーバーへの接続
client.run(token=TOKEN)