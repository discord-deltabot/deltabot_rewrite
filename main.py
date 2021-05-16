import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
import os
import asyncpg
import asyncio
# import aiohttp # will reimport later
import typing
import time

from utils.help import MyHelp

load_dotenv()


class MyBot(commands.Bot):
    def __init__(self):
        self.default_prefix = os.environ.get("BOT_PREFIX")
        self.default_color = discord.Color.dark_purple()
        database_credentials = {
            "host": os.environ.get("DATABASE_HOST"),
            "user": os.environ.get("DATABASE_USER"),
            "password": os.environ.get("DATABASE_PASSWORD"),
            "database": os.environ.get("DATABASE_NAME")
        }
        self.db = asyncio.get_event_loop().run_until_complete(asyncpg.create_pool(**database_credentials))
        self.schedules = []
        self.prefixes = {}
        super(MyBot, self).__init__(command_prefix=self.get_prefix, help_command=MyHelp())

    def starter(self):
        self.run(os.environ.get("BOT_TOKEN"))

    async def get_prefix(self, message):
        if message.guild is None:
            return self.default_prefix
        if message.guild.id in self.prefixes.keys():
            return self.prefixes.get(message.guild.id)

        prefix = await self.db.fetchval("SELECT prefix FROM prefixes WHERE serverid = $1", message.guild.id)
        if prefix is None:
            self.prefixes[message.guild.id] = self.default_prefix
            return self.default_prefix
        self.prefixes[message.guild.id] = prefix
        return prefix

    async def create_channel_schedule(self, time, message: str, channel):
        id = await self.db.fetchval("INSERT INTO schedules (time, message,channelid) values ($1,$2,$3)", time,
                                        message, channel.id)
        map = {}
        map["id"] = id
        map["message"] = message
        map["time"] = time
        map["channelid"] = channel.id
        self.schedules.append(map)

    async def create_user_schedule(self, time, message: str, user):
        id = await self.db.fetchval("INSERT INTO schedules (time, message,userid) values ($1,$2,$3)", time,
                                        message, user.id)
        map = {}
        map["id"] = id
        map["message"] = message
        map["time"] = time
        map["userid"] = user.id
        self.schedules.append(map)

    async def delete_schedule(self, id):
        await self.db.execute("DELETE FROM schedules WHERE id = $1", id)
        for i in self.schedules:
            if i["id"] == id:
                self.schedules.remove(i)


bot = MyBot()


@tasks.loop(seconds=1)
async def schedule_loop():
    for i in bot.schedules:
        # print(i["time"], time.time())
        if i["time"] <= time.time():
            # print("test")
            try:
                await bot.delete_schedule(i["id"])
                destination = await bot.fetch_user(i["userid"]) if i["userid"] else bot.get_channel(i["channelid"])
                embed = discord.Embed(title="Notification", description=i["message"], color=bot.default_color)
                await destination.send(embed=embed)
            except Exception as e:
                print(e)


@bot.event
async def on_ready():
    print("bot is online")
    cogs = [
        "cogs.prefix",
        "cogs.moderation",
        "cogs.economy",
        "cogs.image",
        "jishaku",
        "cogs.owner",
        "cogs.misc"
    ]
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(e)
    results = await bot.db.fetch("SELECT * FROM schedules;")
    for result in results:
        bot.schedules.append(dict(result))

    schedule_loop.start()


bot.starter()
