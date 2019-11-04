import aiohttp
import aiosqlite
import asyncio

import discord
from discord.ext import commands

from backend.config import DATABASE_LOCATION

if __name__ == "__main__":
    with open("token.txt") as file:
        TOKEN = file.read().strip()

bot = commands.Bot(".", case_insensitive=True)

@bot.event
async def on_ready():
    bot._session = aiohttp.ClientSession()
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print(discord.utils.oauth_url(bot.user.id))

async def connect_db():
    bot._db = await aiosqlite.connect(DATABASE_LOCATION)

if __name__ == "__main__":
    bot.loop.run_until_complete(connect_db())
    extensions = [
        "cogs.rolehelper",
        "cogs.moderation",
        "cogs.fun",
        "cogs.rtfm",
        "cogs.dasmooi",
        "cogs.laf"
    ]
    [bot.load_extension(ext) for ext in extensions]
    bot.run(TOKEN)
