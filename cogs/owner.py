import asyncio
import discord
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pull(self, ctx):
        proc = await asyncio.create_subprocess_shell("git pull origin master", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        stdout = f"{stdout.decode()}" if stdout != b"" else ""
        stderr = f"\n{stderr.decode()}" if stderr != b"" else ""
        final = f"```\n{stdout}\n{stderr}\n```"
        embed = discord.Embed(color=self.bot.default_color, title="Pulling from GitHub...",
                              description=final)
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Owner(bot))