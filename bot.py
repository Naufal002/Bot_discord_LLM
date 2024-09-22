# Package here!
import os
import logging
import discord as dc
from discord import Embed
from discord.ext import commands 
from discord.ui import Button, View
from token_1 import *

from langchain_groq import ChatGroq
# from langchain.chains import LLMChain
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
# ==================================
if __name__ == "__main__":
    OperatingSystem = os.name
    match OperatingSystem:
        case "posix" : os.system("clear")
        case "nt" : os.system("cls")
# ===================================
# Initialize Groq Langchain chat object and conversation
model = 'llama3-8b-8192'
groq_chat = ChatGroq(
        groq_api_key= CLIENT_GROQ, 
        model_name=model,
        verbose=False
)

system_prompt = 'You are a friendly conversational chatbot'
conversational_memory_length = 5 # number of previous messages the chatbot will remember during the conversation
memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)
# ===================================
intents = dc.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix='/', intents=intents)
# ===================================
@client.event
async def on_ready():
    print("="*32)
    print("We have logged in as {0.user}".format(client))
    print('='*5,'Bot berada di server','='*5)

    #For check guild
    number = 1
    for guild_list in client.guilds:
        print(f"{number}.{guild_list}")
        number += 1
    print("="*32)

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)

    print(username,": ",user_message)
    print("-"*35)

    if message.author == client.user:
        return
    
    if message.channel.name == 'talkwithkara':
        # Set the system prompt
        user_question = user_message

        # If the user has asked a question,
        if user_question:
            # Construct a chat prompt template using various components
            prompt = ChatPromptTemplate.from_messages(
                [
                    SystemMessage(content=system_prompt),  # Persistent system prompt at the start of the chat.
                    MessagesPlaceholder(variable_name="chat_history"),  # Placeholder for chat history.
                    HumanMessagePromptTemplate.from_template("{human_input}"),  # User's current input.
                ]
            )
            # Create a conversation sequence using a pipeline
            conversation = prompt | groq_chat

            # Generate the chatbot's response by running the conversation sequence
            response = conversation.invoke({
                "chat_history": memory.load_memory_variables({})["chat_history"],  # Retrieve chat history from memory
                "human_input": user_question  # User's question as input
            })
            content = response.content
        await message.reply(content)

        # await message.channel.send(response)
        # print("Chatbot:", response)
        # Print the completion returned by the LLM.
        # print("Assistant:", response.choices[0].message.content)
    
    # Try for check your latency
    if user_message.lower() == '/ping':
        #  Membuat tombol Pong
        button = Button(label="🏓Pong!", style=dc.ButtonStyle.green)
        
        # Membuat view untuk menampilkan tombol
        view = View()
        view.add_item(button)

        # Mengirim pesan dengan tombol
        await message.channel.send("Click the button to get the ping:", view=view)

        # Fungsi ketika tombol diklik
        async def on_button_click(interaction: dc.Interaction):
            if interaction.user == message.author:
                latency = round(client.latency * 1000)  # Menghitung latency dalam ms
                await interaction.response.send_message(f'Latency: {latency} ms', ephemeral=True)
            else:
                await interaction.response.send_message("You can't interact with this button.", ephemeral=True)
        button.callback = on_button_click
    
    # Embed messages
    if user_message.lower() == '/help':
        embed = dc.Embed(
            title='Petunjuk penggunaan 📑',
            description='Saya telah mengembangkan sebuah AI canggih menggunakan kombinasi Python, GROQ API, dan Large Language Model (LLM). AI ini dirancang untuk memanfaatkan kekuatan komputasi tinggi dari GROQ, memungkinkan eksekusi tugas-tugas yang kompleks dengan efisiensi dan kecepatan yang luar biasa. Dengan integrasi LangChain, AI ini mampu mengelola dan memanipulasi rangkaian data dengan fleksibilitas tinggi, memastikan aliran data yang optimal dan responsif. Penggunaan LLM memungkinkan AI ini untuk memahami dan menghasilkan teks dengan presisi tinggi, membuatnya ideal untuk aplikasi seperti analisis data,dan banyak lagi.',
            color=dc.Color.pink()
        )
        embed.add_field(name='/help 🔧', value='Command ini digunakan untuk menampilkan petunjuk penggunaan.', inline=True)
        embed.add_field(name='/ping 📡', value='Kamu bisa menggunakan command ini untuk mendapatkan latncy internet mu.', inline=True)
        embed.add_field(name='# talkwithkara 🤖', value='Untuk bisa menggunakan fitur utama dari AI ini kalian harus membuat channel dengan nama "talkwithkara" dan anda akan bisa menggunakan fitur ini.', inline=True)
        embed.set_footer(text='© 2024 Naufal Rizqi Ilham Gibran🏓')

        try:
            await message.channel.send(embed=embed)
        
        except Exception as e:
            logging.error("Error sending", exc_info=e)

# RUN!
client.run(TOKEN_DC)