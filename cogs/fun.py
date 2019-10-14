import random

import discord
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if random.random() < 0.1:
            await message.add_reaction("tutkegel:633289948711092234")

def setup(bot):
    bot.add_cog(Fun(bot))