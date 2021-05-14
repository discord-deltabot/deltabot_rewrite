import discord
from discord.ext import commands
from utils import image_helper
import functools
import asyncpg
import aiohttp
import typing
from io import BytesIO
import re


class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="invert an image", description="Invert an image. the source can be an emoji, user or a url pointing the image")
    async def invert(self, ctx, source: typing.Union[discord.PartialEmoji, discord.Member, str] = None):
        async with ctx.typing():
            print(type(source))
            if not source:
                source = ctx.author
                asset = source.avatar_url_as(size=512)
                source = BytesIO(await asset.read())
                source.seek(0)
            elif isinstance(source, discord.PartialEmoji):
                asset = source.url
                source = BytesIO(await asset.read())
                source.seek(0)
            elif isinstance(source, discord.Emoji):
                asset = source.url
                source = BytesIO(await asset.read())
                source.seek(0)
            elif isinstance(source, discord.Member):
                asset = source.avatar_url_as(size=512)
                source = BytesIO(await asset.read())
                source.seek(0)
            else:
                url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s(" \
                            r")<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".," \
                            r"<>?«»“”‘’])) "
                url = re.findall(url_regex, source)
                if len(url) <= 0:
                    return await ctx.send("Url is not valid")
                url = url[0]
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(url) as r:
                        source = BytesIO(await r.read())
                        source.seek(0)
            partial = functools.partial(image_helper.get_inverted_bytes, source)
            output = await self.bot.loop.run_in_executor(None, partial)
            await ctx.reply(file=discord.File(output, "invert.png"), mention_author=False)


def setup(bot):
    bot.add_cog(Image(bot))
