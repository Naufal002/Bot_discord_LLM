# Package here!
import os
import discord as dc
from discord.ext import commands 
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

    #For check server joined
    guild_list=[]
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
    
    if isinstance(message.channel, dc.DMChannel):
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
        await message.channel.send(content)
        # await message.reply(content)
        
        # await message.channel.send(response)
        # print("Chatbot:", response)
        # Print the completion returned by the LLM.
        # print("Assistant:", response.choices[0].message.content)

# RUN!
client.run(TOKEN_DC)