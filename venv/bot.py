import random

import aiohttp
import discord


from discord.ext import commands
import uuid
import requests
import shutil
import time
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


def printLanguages():
    s = "You have a total of " + str(len(vocabList)) + " languages in the system! Here they are: \n"
    keys = vocabList.keys()
    for i in keys:
        s += str(i) + ", "
    return s

def printVocabs(vocabs, language):
    s = "You have a total of " + str(len(vocabs)) + " " + language + " words added! Here they are: \n"
    for i in vocabs:
        s += i.getWord() + ", "
    return s

@client.command()
async def addVocab(ctx, language, word, english):
    newVoc = vocab.Vocab(word, english)
    vocabList[str(language)].append(newVoc)
    await ctx.send(printVocabs(vocabList[str(language)], str(language)))

@client.command()
async def test(ctx, language):
    lister = vocabList[language]
    if len(lister) < 1:
        await ctx.send("No vocab words for this language")
    else:
        randomInt = random.randint(0, len(lister)-1)
        vocabWord = lister[randomInt]
        await ctx.send("What is " + vocabWord.getWord() + " in English?")
        time.sleep(10)
        await ctx.send("Answer: " + vocabWord.getEnglish())

@client.command()
async def languages(ctx):
    await ctx.send(printLanguages())

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
                max_tokens=100,
                temperature=0.5
            )

        output = response["choices"][0]["text"]

        print(output)

        await message.channel.send(output)
    else:
        await client.process_commands(message)
