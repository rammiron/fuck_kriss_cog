import os
import discord
from discord.ext import commands

path = "counter.txt"
mats = {
    "хуй", "охуел", "хер", "пизд", "еба", "бля",
    "сука"
}


class FuckKrissCog(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id != 1203158269556822049:
            return
        mats_in_message = 0
        for mat in mats:
            if mat in message.content.lower():
                mats_in_message += 1
        if mats_in_message > 0:
            if os.path.exists(path):
                count: int
                with open(path, "r") as file:
                    count = int(file.read()) + mats_in_message
                with open(path, "w+") as file:
                    file.write(str(count))
                return
            else:
                with open(path, "w+") as file:
                    file.write(str(mats_in_message))

    @commands.slash_command(name="show_kriss_mats_count", description="Отображает"
                                                                      " количество матов сказанных "
                                                                      "Криссом.")
    async def show_mats_count(self, ctx: discord.ApplicationContext):
        if os.path.exists(path):
            count: int
            with open(path, "r") as file:
                count = int(file.read())
            await ctx.respond(f"Крисс писал мат: {count} раз(а).")
        else:
            await ctx.respond(f"Крисс еще ни разу не матерился😱!")
