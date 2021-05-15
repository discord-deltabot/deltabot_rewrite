import discord
from dotenv import load_dotenv
from discord.ext import commands
import os
import asyncpg
import asyncio
import aiohttp
import typing

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

    async def create_schedule(self, time, message: str, destination: typing.Union[discord.User, discord.TextChannel]):
        if isinstance(destination, discord.User):
            userid, channelid = destination.id, None
        else:
            channelid, userid = destination.id, None
        if userid:
            id = self.db.fetchval("INSERT INTO schedules (time, message,userid) values ($1,$2,$3)", time, message,
                                  userid)
        else:
            id = await self.db.fetchval("INSERT INTO schedules (time, message,channelid) values ($1,$2,$3)", time,
                                        message, channelid)
        map = {}
        map["id"] = id
        map["message"] = message
        map["time"] = time
        map["channelid"] = channelid if channelid else None
        map["userid"] = userid if userid else None
        self.schedules.append(map)

    async def delete_schedule(self, id):
        self.db.execute("DELETE FROM schedules WHERE id = $1", id)
        for i in self.schedules:
            if i["id"] == id:
                self.schedules.remove(i)





bot = MyBot()


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
        "cogs.schedule"
    ]
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(e)


bot.starter()
