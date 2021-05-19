import discord
from discord.ext import commands
import time
import aiohttp
import random

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        websocket_latency = self.bot.latency * 1000
        dbt1 = time.time()
        await self.bot.db.fetchval("SELECT 1")
        database_latency = (time.time() - dbt1) * 1000
        embed = discord.Embed(title="PIng", color=self.bot.default_color)
        embed.add_field(name="websocket Latency", value=f"```js\n{str(round(websocket_latency))} ms```", inline=False)
        embed.add_field(name="database latency", value=f"```js\n{str(round(database_latency))} ms```", inline=False)
        mest1 = time.time()
        mes = await ctx.send(embed=embed)
        message_latency = (time.time() - mest1) * 1000
        embed.add_field(name="Typing", value=f"```js\n{str(round(message_latency))} ms```")
        await mes.edit(embed=embed)



    @commands.command()
    async def remind(self,ctx, seconds, *, reason:str=None):
        await ctx.reply(f"Ok! I will remind you for {reason} in {seconds} second(s)",mention_author=False)
        await self.bot.create_user_schedule(time=time.time()+float(seconds), message=f"Hey you just asked me to remind you for `{reason}` now", user=ctx.author)

    @commands.command()
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://www.reddit.com/r/memes.json") as r:
                result = await r.json()
        index = random.randint(0,len(result["data"]["children"]))
        image_url = result["data"]["children"][index]["data"]["url"]
        title = result["data"]["children"][index]["data"]["title"]
        embed = discord.Embed(title=title, color=self.bot.default_color)
        embed.set_image(url=image_url)
        await ctx.reply(embed=embed, mention_author=False)


def setup(bot):
    bot.add_cog(Misc(bot))