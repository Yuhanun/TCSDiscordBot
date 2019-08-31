import aiohttp
import discord
from discord.ext import commands

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

if __name__ == "__main__":
    extensions = [
        "cogs.rolehelper",
        "cogs.moderation"
    ]
    [bot.load_extension(ext) for ext in extensions]
    bot.run(TOKEN)