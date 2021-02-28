import discord
import asyncio
import random
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, has_permissions, cooldown, BucketType
import json

with open("bot-config//bot-emojis.json") as f:
  bot_emojis = json.load(f)

class UtilityCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=["av"])
  @cooldown(1, 1, BucketType.user)
  async def avatar(self, ctx, member: discord.Member = None):

        if member == None:
            member = ctx.author
        embed = discord.Embed(
            title=f"{member.name}'s avatar",
            colour=discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        embed.set_image(url=member.avatar_url)
        embed.set_footer(
            text=
            f'Requested by {ctx.author}',
            icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

  @avatar.error
  async def avatar_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      em = discord.Embed(title=random.choice(["Take a chill pill", "Slow it down, C'mon", "Hold your horses"]), colour=discord.Colour.blurple())
      em.description = f"You'll be able to use the `{ctx.command.name}` command again in **{error.retry_after:.2f} second(s)**\nThe default cooldown is **`1s`**"
      await ctx.message.reply(embed=em)
    else:
      await ctx.send(f"**An Unknown Error Occurred**\n\nAn unknown error occured in the `{ctx.command.name}` command, please consider joining our support server and reporting this bug. (<https://discord.gg/CSZdMdAuZt>)")

  @commands.command(aliases=["whois"])
  @cooldown(1, 3, BucketType.user)
  async def userinfo(self, ctx, *,member: discord.Member=None):
        if not member:
          member = ctx.author
        roles = member.roles
        embed = discord.Embed(
            title=f"{member}", colour=discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255),random.randint(0, 255)))
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(
            name="Created at:",
            value=member.created_at.strftime(
                '%a, %#d %B %Y, %I:%M %p GMT'),
            inline=True)
        embed.add_field(
            name="Joined server at:",
            value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p GMT'),
            inline=True)
        embed.add_field(name="Activity", value=f"{member.activity}", inline=False)       
        if member.status == discord.Status.online:
          embed.add_field(name="Status:", value=bot_emojis['online'], inline=True) 
        elif member.status == discord.Status.dnd:
          embed.add_field(name="Status:", value=bot_emojis['dnd'], inline=True)
        elif member.status == discord.Status.offline:
          embed.add_field(name="Status:", value=bot_emojis['invisible'], inline=True)
        elif member.status == discord.Status.idle:
          embed.add_field(name="Status:", value=bot_emojis['idle'])
        embed.add_field(name="Bot?", value=f"{member.bot}", inline=True) 
        embed.add_field(name="User ID:", value=member.id, inline=False)          
        if len(roles) == 1:
            embed.add_field(name=f'Roles ({len(roles) - 1})', value='No Roles.')
        elif len(roles) > 25:
            embed.add_field(name=f"Roles ({len(roles) - 1})",value="Too many roles to show here!")
        else:
            embed.add_field(name=f'Roles ({len(roles) - 1})', value=' '.join([role.mention for role in roles if role.name != '@everyone']))
        if member.top_role.name == "@everyone":
          embed.add_field(name="Top role", value="No Roles.")
        else:
          embed.add_field(name="Top role", value=member.top_role.mention)
        await ctx.send(embed=embed)

  @userinfo.error
  async def userinfo_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      em = discord.Embed(title=random.choice(["Take a chill pill", "Slow it down, C'mon", "Hold your horses"]), colour=discord.Colour.blurple())
      em.description = f"You'll be able to use the `{ctx.command.name}` command again in **{round(error.retry_after)} second(s)**\nThe default cooldown is `3s`"
      await ctx.message.reply(embed=em)
    else:
      await ctx.send(f"**An Unknown Error Occurred**\n\nAn unknown error occured in the `{ctx.command.name}` command, please consider joining our support server and reporting this bug. (<https://discord.gg/CSZdMdAuZt>)")

  @commands.Cog.listener()
  async def on_message_delete(self, msg):
     file = json.load(open(r"json//snipe-dict.json", "r"))
     if not msg.author.bot:
      if not str(msg.guild.id) in file:
          file[str(msg.guild.id)] = {}
      file[str(msg.guild.id)]["user-id"] = msg.author.id
      file[str(msg.guild.id)]["content"] = msg.content
      json.dump(file, open(r"json//snipe-dict.json", "w"), indent=4)

  @commands.command()
  @cooldown(1, 5, BucketType.user)
  async def snipe(self, ctx):
     file = json.load(open(r"json//snipe-dict.json", "r"))
     if not str(ctx.guild.id) in file:
         return await ctx.send("There's nothing to snipe!")
    
     user_id = file[str(ctx.guild.id)]["user-id"]
     content = file[str(ctx.guild.id)]["content"]
     user = await self.bot.fetch_user(user_id)    
     embed = discord.Embed(color=discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), timestamp=ctx.message.created_at)
     embed.set_author(name=user, icon_url=user.avatar_url)
     embed.description = f"{content}"
     embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
     await ctx.send(embed=embed)

  @snipe.error
  async def snipe_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      em = discord.Embed(title=random.choice(["Take a chill pill", "Slow it down, C'mon", "Hold your horses"]), colour=discord.Colour.blurple())
      em.description = f"You'll be able to use the `{ctx.command.name}` command again in **{round(error.retry_after)} second(s)**\nThe default cooldown is `5s`"
      await ctx.message.reply(embed=em)
    else:
      await ctx.send(f"**An Unknown Error Occurred**\n\nAn unknown error occured in the `{ctx.command.name}` command, please consider joining our support server and reporting this bug. (<https://discord.gg/CSZdMdAuZt>)")

  @commands.Cog.listener()
  async def on_message_edit(self, msg_before, msg_after):
     file = json.load(open(r"json//editsnipe-dict.json", "r"))
     if not msg_before.author.bot:
      if not str(msg_before.guild.id) in file:
          file[str(msg_before.guild.id)] = {}
      file[str(msg_before.guild.id)]["user-id"] = msg_before.author.id
      file[str(msg_after.guild.id)]["before-content"] = msg_before.content
      file[str(msg_after.guild.id)]["after-content"] = msg_after.content
      json.dump(file, open(r"json//editsnipe-dict.json", "w"), indent=4)

  @commands.command()
  @cooldown(1, 5, BucketType.user)
  async def editsnipe(self, ctx):
      file = json.load(open(r"json//editsnipe-dict.json", "r"))
      if not str(ctx.guild.id) in file:
          return await ctx.send("There's nothing to snipe!")
    
      user_id = file[str(ctx.guild.id)]["user-id"]
      before_content = file[str(ctx.guild.id)]["before-content"]
      after_content = file[str(ctx.guild.id)]["after-content"]
      user = await self.bot.fetch_user(user_id)    
      embed = discord.Embed(colour=discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),timestamp=ctx.message.created_at)
      embed.set_author(name=user, icon_url=user.avatar_url)
      embed.description = f"**Before**:\n{before_content}\n\n**After**:\n{after_content}"
      embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)

  @editsnipe.error
  async def editsnipe_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      em = discord.Embed(title=random.choice(["Take a chill pill", "Slow it down, C'mon", "Hold your horses"]), colour=discord.Colour.blurple())
      em.description = f"You'll be able to use the `{ctx.command.name}` command again in **{round(error.retry_after)} second(s)**\nThe default cooldown is `5s`"
      await ctx.message.reply(embed=em)
    else:
      await ctx.send(f"**An Unknown Error Occurred**\n\nAn unknown error occured in the `{ctx.command.name}` command, please consider joining our support server and reporting this bug. (<https://discord.gg/CSZdMdAuZt>)")

  @commands.group(aliases=["welc"],invoke_without_command=True)
  async def welcome(self,ctx):
      await ctx.invoke(self.bot.get_command("help"), entity="welcome")

  @welcome.command(name="channel")
  async def welchannel(self,ctx,channel:discord.TextChannel):
      data = await self.bot.welcomes.find(ctx.guild.id)
      if data is None:
          data = {"_id": ctx.guild.id, "channel": channel.id, "message": "{member} Welcome to **{server}**! Have a great time here!"}
      data["channel"] = channel.id
      await self.bot.welcomes.upsert(data)
      await ctx.send("The welcome channel has been set as {}".format(channel.mention))

  @welcome.command(name="message", usage = "[message (or args for args)]")
  async def welmessage(self,ctx,*,message:commands.clean_content):
      data = await self.bot.welcomes.find(ctx.guild.id)
      if message == "args":
          return await ctx.send("The args for the welcome message are:\n```{member}: Mentions the member\n{server}: sends the server name```")
      if data is None:
          return await ctx.send("Set up a channel first then set a welcome message")
      data["message"] = message
      await self.bot.welcomes.upsert(data)
      await ctx.send("The welcome message has been set as\n\n{}".format(message))

  @welcome.command(name="role")
  async def welrole(self,ctx,role:discord.Role):
      data = await self.bot.welcomes.find(ctx.guild.id)
      if data is None and "role" not in data:
          return await ctx.send("Set up a channel first then set a welcome message")
      data["role"] = role.id
      await self.bot.welcomes.upsert(data)
      await ctx.send("The welcome role has been set as `{}`".format(role.name))
      
def setup(bot):
  bot.add_cog(UtilityCog(bot))
  print("UtilityCog is ready!")
