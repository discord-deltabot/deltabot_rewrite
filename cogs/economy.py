import discord
from discord.ext import commands
import random


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["bal", "wallet", "bank"], brief="See how much money is left in bank and wallet")
    async def balance(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        result = await self.bot.db.fetchrow("SELECT wallet, bank FROM economy WHERE userid = $1", member.id)

        wallet = result["wallet"] if result else 0
        bank = result["bank"] if result else 0

        embed = discord.Embed(title=f"{member.name}'s balance",
                              description=f"*Wallet*: `{str(wallet)}`\n*bank*: `{str(bank)}`",
                              color=self.bot.default_color
                              )
        await ctx.send(embed=embed)

    @commands.cooldown(1, 300, commands.cooldowns.BucketType.user)
    @commands.command(brief="Beg me for dome trash?")
    async def beg(self, ctx):
        money = random.randint(20, 200)
        is_exist = bool(await self.bot.db.fetchval("SELECT COUNT(*) FROM economy WHERE userid = $1", ctx.author.id))
        if is_exist:
            sql = "UPDATE economy SET wallet = wallet + $1"
            await self.bot.db.execute(sql, money)
        else:
            sql = "INSERT INTO economy (userid, wallet, bank) VALUES ($1,$2,$3)"
            await self.bot.db.execute(sql, ctx.author.id, money, 0)
        await ctx.send("Here you go buddy. I am giving you {} coins!!".format(str(money)))

    @beg.error
    async def on_beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f"Dude I am not Elon wait {error.retry_after.round()}s before asking again!")

    @commands.command(brief="Deposit money to bank", aliases=["dep"])
    async def deposit(self, ctx, money: int):
        data = await self.bot.db.fetchrow("SELECT wallet, bank FROM economy WHERE userid = $1", ctx.author.id)
        wallet = data["wallet"] if data else 0
        # bank = data["bank"] if data else 0
        if wallet < money:
            return await ctx.send("You don't seem to have enough money to deposit into bank")
        sql = "UPDATE economy SET wallet=wallet - $1, bank = bank + $1 where userid = $2"
        await self.bot.db.execute(sql, money, ctx.author.id)
        await ctx.send("You have deposited {} coins to your bank".format(str(money)))

    @commands.command(brief="Withdraw money from bank", aliases=["wit", "with"])
    async def withdraw(self, ctx, money: int):
        data = await self.bot.db.fetchrow("SELECT wallet, bank FROM economy WHERE userid = $1", ctx.author.id)
        # wallet = data["wallet"] if data else 0
        bank = data["bank"] if data else 0
        if bank < money:
            return await ctx.send("You don't have enough money to be withdrawn from bank")
        sql = "UPDATE economy SET bank=bank - $1, wallet = wallet + $1 where userid = $2"
        await self.bot.db.execute(sql, money, ctx.author.id)
        await ctx.send("You have deposited {} coins to your bank".format(str(money)))

    @commands.command(brief="Check store to buy useful items")
    async def store(self, ctx):
        embed = discord.Embed(title="`Store`", color=self.bot.default_color)
        items = await self.bot.db.fetch("SELECT * FROM store;")
        for item in items:
            embed.add_field(name=f"{item['emoji']} {item['name']}", value=f"💰 {item['price']}")
        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(Economy(bot))
