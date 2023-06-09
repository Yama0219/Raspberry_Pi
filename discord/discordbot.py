import discord
from discord import Intents
import pandas as pd
import os
import sys
import subprocess

TOKEN = ""

with open("token.txt", "r") as f:
    TOKEN = f.read().replace("\n", "")

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    for channel in client.get_all_channels():
        if channel.name == "general":
            await channel.send("起動しました")

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    
    if message.author.guild_permissions.administrator:
        if message.content == "/stop":
            await message.channel.send('see you')
            await client.close()

        if message.content.startswith("/command"):
            command = message.content.split()[1:]
            await message.channel.send(f"{' '.join(command)}を実行するよ")

            if "shutdown" in message.content:
                await message.channel.send("シャットダウンはできません")
            else:   
                output = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                await message.channel.send(output.communicate()[0].decode())

    if message.content == '/hello':
        await message.channel.send('やあ，{}さん'.format(message.author.mention))

    if message.content == '/neko':
        await message.channel.send('にゃーん')
        await message.channel.send(':smirk_cat:')

    if message.content == "/GPA":
        await message.channel.send('成績表を送信するよ')
        await message.channel.send(file=discord.File("../GPA/GPA.csv"))
    
    if message.content == "/updateGPA":
        await message.channel.send('成績表を更新するよ．しばらく待ってね')
        output = subprocess.Popen("python /home/kenke/Desktop/myfolder/Raspberry_Pi/GPA/GPA.py".split())
        





# Botの起動とDiscordサーバーへの接続
client.run(token=TOKEN)