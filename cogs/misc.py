import discord
from discord.ext import commands
import time

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remind(self,ctx, seconds, *, reason:str=None):
        await ctx.reply(f"Ok! I will remind you for {reason} in {seconds} second(s)",mention_author=False)
        await self.bot.create_user_schedule(time=time.time()+float(seconds), message=f"Hey you just asked me to remind you for `{reason}` now", user=ctx.author)


def setup(bot):
    bot.add_cog(Misc(bot))