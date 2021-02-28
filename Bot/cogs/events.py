import discord
from discord.ext import commands
import asyncio

class Events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member):
        data = await self.bot.welcomes.find(member.guild.id)
        if data is None:
            return
        welchannel = data["channel"]
        welmessage = data["message"]
        channel = self.bot.get_channel(int(welchannel))
        welmessage = welmessage.replace("{member}", member.mention)
        welmessage = welmessage.replace("{server}", member.guild.name)
        if "role" in data:
            await member.add_roles(member.guild.get_role(data["role"]))
        await channel.send(welmessage)

def setup(bot):
    bot.add_cog(Events(bot))
