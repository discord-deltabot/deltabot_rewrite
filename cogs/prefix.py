import discord
from discord.ext import commands


class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_guild=True)
    @commands.command(name="changeprefix", brief="Change prefix of the bot in a server")
    async def change_prefix(self, ctx, prefix):
        await self.bot.db.execute(
            "INSERT INTO prefixes (serverid,prefix) VALUES ($1,$2) ON CONFLICT(serverid) DO UPDATE SET prefix = $2",
            ctx.guild.id, prefix)
        self.bot.prefixes[ctx.guild.id] = prefix
        await ctx.send("The prefix for the server has been updated")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == self.bot.user.display_name:
            prefix = self.bot.get_prefix(message)
            await message.channel.send("my prefix for this server is `{}`".format(prefix))


def setup(bot):
    bot.add_cog(Prefix(bot))
