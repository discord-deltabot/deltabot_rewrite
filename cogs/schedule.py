import discord
from discord.ext import commands, tasks
import time


class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        results = self.bot.db.fetch("SELECT * FROM schedules;")
        for result in results:
            self.bot.schedules.append(dict(result))

    @tasks.loop(seconds=1)
    async def schedule_loop(self):
        for i in self.bot.schedules:
            if i["time"] <= time.time():
                self.bot.delete_schedule(i["id"])
                destination = self.bot.fetch_user(i["userid"]) if i["userid"] else self.bot.get_channel(i["channelid"])
                await destination.send(i["message"])

def setup(bot):
    bot.add_cog(Schedule(bot))