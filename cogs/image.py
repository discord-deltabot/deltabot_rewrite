import discord
from discord.ext import commands
from utils import image_helper
import functools
import asyncpg


class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invert(self, ctx, image:str=None):
        if image is None:
            image_url = ctx.author.avatar_url()
            async with self.bot.session.get(str(image_url)) as r:
                img_bytes = await r.content()
        try:
            member = await commands.MemberConverter().convert(ctx=ctx, argument=image)
            image_url = member.avatar_url()
            async with self.bot.session.get(str(image_url)) as r:
                img_bytes = await r.content()
        except:
            return await ctx.send("Emoji inverting coming soon")

        partial_function = functools.partial(image_helper.get_inverted_bytes, img_bytes)
        inverted_bytes = await self.bot.loop.run_in_executor(None, partial_function)
        await ctx.send(file=discord.File(fp=inverted_bytes, filename="inverted.png"))


def setup(bot):
    bot.add_cog(Image(bot))
