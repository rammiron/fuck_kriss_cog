import os
import json
import discord
from discord.ext import commands

path = "counter.txt"
mats_list_path = "mats.json"


class FuckKrissCog(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    mats = ["бля"]

    @commands.Cog.listener()
    async def on_ready(self):
        with open(mats_list_path, "r") as file:
            temp: list = json.loads(file.read())
            self.mats = temp

    @commands.slash_command(name="add_kriss_mat", description="Добавить мат для распознавания из сообщений Крисса.")
    async def add_kriss_mat(self, ctx: discord.ApplicationContext, mat: str):
        with open(mats_list_path, "r") as file:
            temp: list = json.loads(file.read())
            self.mats = temp
        self.mats.append(mat)
        with open(mats_list_path, "w+") as file:
            file.write(json.dumps(self.mats))
        await ctx.respond(f"Готово, мат \"{mat}\" добавлен в список для распознавания.")

    @commands.slash_command(name="show_mat_list", description="Показывает список матов для распознавания.")
    async def show_mat_list(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"Список мата для распознавания: \n {self.mats}")

    @commands.slash_command(name="delete_mat_from_list", description="Удаляет указанный мат из листа матов.")
    async def delete_mat(self, ctx: discord.ApplicationContext, mat: str):
        if mat in self.mats:
            self.mats.remove(mat)
            with open(mats_list_path, "w+") as file:
                file.write(json.dumps(self.mats))
            await ctx.respond(f"Готово, мат \"{mat}\" удален.")
        else:
            await ctx.respond(f"Мат \"{mat}\" не обнаружен.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id != 1048600490562293850:
            return
        mats_in_message = False
        for mat in self.mats:
            if mat in message.content.lower():
                mats_in_message = True
                break
        if mats_in_message:
            if os.path.exists(path):
                count: int
                with open(path, "r") as file:
                    count = int(file.read()) + 1
                with open(path, "w+") as file:
                    file.write(str(count))
                return
            else:
                with open(path, "w+") as file:
                    file.write(str(mats_in_message))

    @commands.slash_command(name="show_kriss_mats_count", description="Отображает"
                                                                      " количество сообщений с матом отправленных "
                                                                      "Криссом.")
    async def show_mats_count(self, ctx: discord.ApplicationContext):
        if os.path.exists(path):
            count: int
            with open(path, "r") as file:
                count = int(file.read())
            await ctx.respond(f"Крисс отправил сообщений с матом: {count}.")
        else:
            await ctx.respond(f"Крисс еще ни разу не матерился😱!")
