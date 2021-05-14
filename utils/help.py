import discord
from discord.ext import commands


class MyHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, color=self.context.bot.default_color)
            await destination.send(embed=emby)
