import aiohttp
import discord


from discord.ext import commands
import uuid
import requests
import shutil
import json
import tokenAbstractor
import vocab
from collections import defaultdict
import aiohttp
import openai


intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

vocabList = defaultdict(list)
openai.api_key = tokenAbstractor.apiStr

def run_discord_bot():


    @client.event
    async def on_ready():
        print(f'{client.user} is now running!!')

    client.run(str(tokenAbstractor.getKey()))

@client.event
async def on_message(message):

    if message.author == client.user:
        return
    if message.content.startswith("hey"):
        await message.channel.send('hey')
    if message.content.startswith("max is"):
        await message.channel.send('a bit of a beast')
    else:
        await client.process_commands(message)


def printVocabs(vocabs, language):
    s = "You have a total of " + str(len(vocabs)) + " " + language + " words added! Here they are: \n"
    for i in vocabs:
        s += i.getWord() + ", "
    return s

@client.command()
async def addVocab(ctx, language, word, english, meaning):
    newVoc = vocab.Vocab(word, english, meaning)
    vocabList[str(language)].append(newVoc)
    await ctx.send(printVocabs(vocabList[str(language)], str(language)))

@client.command()
async def languages(ctx, language, word, english, meaning):
    newVoc = vocab.Vocab(word, english, meaning)
    vocabList[str(language)].append(newVoc)
    await ctx.send(printVocabs(vocabList[str(language)], str(language)))

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)

    print(username + " said " + user_message.lower() + " in " + channel)

    if message.channel.name == client.user:
        return

    if message.channel.name == 'discord_bot':
        response = openai.Completion.create(
                model="text-davinci-003",
                prompt=user_message,
                max_tokens=50,
                temperature=0.5
            )

        output = response["choices"][0]["text"]

        print(output)
        await message.channel.send(output)
