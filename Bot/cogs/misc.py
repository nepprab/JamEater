import discord
import os
import inspect
from discord.ext import commands

class MiscCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command(name="source")
  async def source_code_(self, ctx, command: str=None):
    if command is None:
      embed = discord.Embed(description=f"Click [here](https://youtube.com/watch?v=dQw4w9WgXcQ) for the source code of {self.bot.user.name}", colour=discord.Colour.blurple())
      embed.set_footer
      await ctx.send(embed=embed)
    else:
        source_url = 'https://github.com/ProGamer368/JamEater'
        branch = 'master/Bot'      
        if command == 'help':
            src = type(self.bot.help_command)
            module = src.__module__
            filename = inspect.getsourcefile(src)
        else:
            obj = self.bot.get_command(command.replace('.', ' '))
            if obj is None:
                return await ctx.send("I couldn't find any command with that name.\nThat command is either not open-source or invalid!")
            src = obj.callback.__code__
            module = obj.callback.__module__
            filename = src.co_filename

        lines, firstlineno = inspect.getsourcelines(src)
        if not module.startswith('discord'):
            location = os.path.relpath(filename).replace('\\', '/')
        else:
            location = module.replace('.', '/') + '.py'
            source_url = 'https://github.com/Rapptz/discord.py'
            branch = 'master'

        final_url = f'<{source_url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>'
        source_embed = discord.Embed(description=f"Click [here]({final_url}) for the source code of the `{command}` command.")
        await ctx.send(embed=source_embed)      
  
  @commands.command(name="ping")
  async def ping_(self, ctx):
    msg = await ctx.send("Pinging...")
    await msg.edit(content=f":ping_pong: Pong! `{round(self.bot.latency * 1000)}ms`")

  @commands.command()
  async def invite(self, ctx):
    embed = discord.Embed(description="**Hey, looks like you are interested in adding me!**", colour=0x7289da)
    embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
    embed.add_field(name="Need Support?", value="[`Join my support server`](https://discord.com/invite/CSZdMdAuZt)", inline=False)
    embed.add_field(name="Wanna invite me?", value=f"[`Invite me!`](https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=427158910)", inline=False)
    await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(MiscCog(bot))
  print("MiscCog is ready!")
