import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User = None, reason=None):
        """Ban a user from the server"""

        if not user:
            return await ctx.send("You must specify a user")

        try:
            await ctx.guild.ban(user, f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified")
            await ctx.send(f"{user.mention} was Banned from the server for {reason}.")
        except discord.Forbidden:
            return await ctx.send("Are you trying to ban someone higher than the bot")

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, user: discord.User = None, reason=None):
        if not user:
            return await ctx.send("You must specify a user")

        try:
            await ctx.guild.kick(user, f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified")
        except discord.Forbidden:
            return await ctx.send("Are you trying to kick someone higher than the bot?")


    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def purge(self, ctx, limit: int):
        """Bulk deletes messages"""

        await ctx.purge(limit=limit + 1)  # also deletes your own message
        await ctx.send(f"Bulk deleted `{limit}` messages")

def setup(bot):
    bot.add_cog(Moderation(bot))