import discord
from discord.ext import commands

with open("token.txt") as file:
    TOKEN = file.read().strip()

bot = commands.Bot(".", case_insensitive=True)

bot.run(TOKEN)