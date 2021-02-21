import discord
from discord.ext import commands
import os
import random

intents = discord.Intents.all()
intents.members = True
intents.bans = True
intents.typing = True
bot = commands.Bot(command_prefix="jm ", case_insensitive=True, intents=intents)

@bot.event
async def on_ready():
  print("Ready to eat jam!")
  
bot.run(token)
