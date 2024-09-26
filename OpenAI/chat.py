# Package here!
import os
import discord as dc
import openai
from discord.ext import commands
import datetime as dt
from token_1 import *

if __name__ == "__main__":
    OperatingSystem = os.name
    match OperatingSystem:
        case "posix" : os.system("clear")
        case "nt" : os.system("cls")
# ===================================
TOKEN = TOKEN_DC
openai.api_key = TOKEN_OPENAI
intents = dc.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    # channel = str(message.channel.name)
    # today = dt.datetime.today()

    print(username,": ",user_message)

    if message.author == client.user:
        return
    
    if message.channel.name == 'talkwithkara':
    
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Menggunakan model yang tersedia dan valid
            messages=[
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7,
            n=1,
            stop=None
        )
        
        # response = openai.Completion.create(
        #     model="text-davinci-003",
        #     prompt=user_message,
        #     max_tokens=3000,
        #     temperature=0.7
        # )

        output = response["choices"] [0] ["text"]
        print(output)
        await message.channel.send(output)
    
client.run(TOKEN)