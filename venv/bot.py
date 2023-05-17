import discord


from discord.ext import commands
import uuid
import requests
import shutil
import tokenAbstractor

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='$', intents=intents)
images = []


def run_discord_bot():


    @client.event
    async def on_ready():
        print(f'{client.user} is now running!!')



    client.run(str(tokenAbstractor.getKey()))
