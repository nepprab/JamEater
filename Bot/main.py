# da imports

import discord
from discord.ext import commands, ipc
import os
import random
import json
import ast
import asyncio
import datetime
from mymongo import Document
import motor.motor_asyncio

#important stuff

with open("bot_config/credentials.json") as f:
    config = json.load(f)

with open("bot_config/bot-emojis.json") as f:
    bot_emojis = json.load(f)

class Bot(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.ipc = ipc.Server(self,secret_key = "JamEater")

    async def on_ipc_ready(self):
        """Called upon the IPC Server being ready"""
        print("Ipc server is ready.")

    async def on_ipc_error(self, endpoint, error):
        """Called upon an error being raised within an IPC route"""
        print(endpoint, "raised", error)

# defining a few stuff...
intents = discord.Intents.all()
intents.members = True
intents.bans = True
bot = Bot(command_prefix=commands.when_mentioned_or("jm "), case_insensitive=True, intents=intents, allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True))
bot.remove_command("help")
my_bot.connection_url = "mongodb://JamEater:JamEater@cluster0-shard-00-00.zps67.mongodb.net:27017,cluster0-shard-00-01.zps67.mongodb.net:27017,cluster0-shard-00-02.zps67.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-o4zk6d-shard-0&authSource=admin&retryWrites=true&w=majority"
my_bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(my_bot.connection_url))
my_bot.db = my_bot.mongo["JamEater"]
my_bot.prefixes = Document(my_bot.db, "prefixes")
token = config['bot-token']
bot.owner_ids = config['bot-owner-ids']

def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

async def presence():
    await bot.wait_until_ready()
    
    while not bot.is_closed():
        streaming_statuses = ["life", "Never gonna loose this BotJam", "life is a lie", f"with {len(bot.guilds)} servers"]
        streaming_status = random.choice(streaming_statuses)
        await bot.change_presence(activity = discord.Streaming(name = streaming_status, url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
        await asyncio.sleep(5.0)

# global error handeler

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    pass
  elif isinstance(error, commands.MissingPermissions):
    await ctx.send("{}, You can't do that, You need the **{}** perms. to do that!".format(ctx.author.mention,' '.join(error.missing_perms[0].split('_'))), delete_after=3.0)
    await ctx.message.delete()
  elif isinstance(error, commands.BotMissingPermissions):
      if error.missing_perms[0] == 'send_messages':
          return
      embed=discord.Embed(description="I'm missing the **{}** permission!".format(' '.join(error.missing_perms[0].split('_'))), colour=discord.Colour.blurple())
      await ctx.message.reply(embed=embed)
  elif isinstance(error, commands.MemberNotFound):
    await ctx.send(error, delete_after=3.3)
  elif isinstance(error, commands.MissingRole):
    await ctx.send(error)
  elif isinstance(error, commands.ChannelNotFound):
    await ctx.send(error)
  elif isinstance(error, commands.CommandInvokeError):
      await ctx.send(error)
  
# first command

@bot.command(name="eval")
async def eval_(ctx, *, code):
  if ctx.author.id in bot.owner_ids: #making sure only the owners have access to eval
    fn_name = "_eval_expr"
    code = code.replace("```py", "```")
    code = code.strip("` ")
    code = "\n".join(f"    {i}" for i in code.splitlines())
    body = f"async def {fn_name}():\n{code}"
    parsed = ast.parse(body)
    body = parsed.body[0].body
    insert_returns(body)
    env = { # defining important eval stuff
        'bot': bot,
        'discord': discord,
        'commands': commands,
        'ctx': ctx,
        '__import__': __import__,
        'asyncio': asyncio,
        'datetime': datetime,
        'os': os,
        'random': random
    }
    exec(compile(parsed, filename="<ast>", mode="exec"), env)
    result = (await eval(f"{fn_name}()", env))
    try:
      await ctx.send(result)
    except:
      pass


@bot.command()
async def load(ctx, extension):
  if ctx.author.id in bot.owner_ids:
      try:
        bot.load_extension(extension)
        await ctx.send(f"Loaded `{extension}`")
      except Exception as e:
        await ctx.send(e)
  else:
    return False

@bot.command()
async def unload(ctx, extension):
  if ctx.author.id in bot.owner_ids:
      try:
        bot.unload_extension(extension)
        await ctx.send(f"Unloaded `{extension}`")
      except Exception as e:
        await ctx.send(e)
  else:
    return False

@bot.command()
async def reload(ctx, extension):
  if ctx.author.id in bot.owner_ids:
      try:
        bot.unload_extension(extension)
        bot.load_extension(extension)
        await ctx.send(f"Reloaded `{extension}`")
      except Exception as e:
        await ctx.send(e)
  else:
    return False

# eval error handeler

@eval_.error
async def _eval_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    if ctx.author.id in bot.owner_ids:
      await ctx.send("Give me a code to eval")
    else:
      pass
  elif isinstance(error, commands.CommandInvokeError):
    if ctx.author.id in bot.owner_ids:
      embed= discord.embed(colour=discord.Colour.dark_red())
      embed.description = f"**{bot_emojis['error']} Error**\n\n{error}"
      await ctx.send(embed=embed)
    else:
      pass  

# on ready

@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Activity(name=f"{len(bot.guilds)} servers", type=5), status=discord.Status.dnd)
  print("Bot is ready!")
  for file in os.listdir("./cogs"):
    if file.endswith(".py"):
      try:
        bot.load_extension(f"cogs.{file[:-3]}")
      except Exception as e:
	      print("Cogs error: Cannot load cogs")
	      print("\033[5;37;40m\033[1;33;40mWARNING\033[1;33;40m\033[0;37;40m", end=' ')
	      print("Functionality limited!\n")
	      print(f"exception thrown:\n{e}")

# To make the commands work when the message is edited

@bot.event
async def on_message_edit(msg_before, message):
  await bot.process_commands(message)

# IPC Stuff for dashboard

@bot.ipc.route()
async def checkforguild(data):
	try:
		server = bot.get_guild(data.guildid)
	except:
		return None
	else:
		return True

@bot.ipc.route()
async def getnickname(data):
	guild = bot.get_guild(int(data.guildid))
	if guild.me.nick:
		return str(guild.me.nick)
	return bot.user.name

@bot.ipc.route()
async def getprefix(data):
	prefixes = await bot.prefixes.find(data.guildid)
	if not prefixes or "prefix" not in prefixes:
		return bot.command_prefix
	return str(prefixes["prefix"])

@my_bot.ipc.route()
async def changenick(data):
	guild = my_bot.get_guild(data.guildid)
	name = data.name
	await guild.me.edit(nick=str(name).strip('"'))
	return

@my_bot.ipc.route()
async def changeprefix(data):
	prefix = await bot.prefixes.find(int(data.guildid))
	if not prefix or "prefix" not in prefix:
		prefix = {"_id":data.guildid,"prefix":data.newprefix}
	prefix["prefix"] = str(data.newprefix).strip('"')
	await my_bot.prefixes.upsert(prefix)

bot.loop.create_task(presence()) # changing the bot's presence every 5 secs
bot.ipc.start()
bot.run(token) # running the bot lmao
