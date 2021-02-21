import discord
from discord.ext import commands

class MiscCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.Cog.listener()
  async def on_ready(self):
    print("Misc stuff are ready!")
    
  @commands.command(name="source")
  async def source_code_(self, ctx, command: str):
    embed = discord.Embed(title="Source code", description=f"Click [here](https://youtube.com/watch?v=dQw4w9WgXcQ) for the source code of {self.bot.user.name}")
    await ctx.send(embed=embed)
  
  @commands.command(name="ping")
  async def ping_(self, ctx):
    msg = await ctx.send("Pinging...")
    await msg.edit(content=f":ping_pong: Pong! `{round(self.bot.latency * 1000)}`")
  
def setup(bot):
  bot.add_cog(MiscCog(bot))
