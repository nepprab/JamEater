import discord
from discord.ext import commands
import os
import random
import json

with open("bot_config/config.json") as f:
   config = json.load(f)

# defining a few stuff...
intents = discord.Intents.all()
intents.members = True
intents.bans = True
intents.typing = True
bot = commands.Bot(command_prefix="jm ", case_insensitive=True, intents=intents)
token = config['bot-token']
bot.owner_ids = config['bot-owner-ids']

@bot.event
async def on_ready():
  print("Ready to eat jam!")
  
bot.run(token)
