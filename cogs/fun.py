import random

import discord
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.enabled = True
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not self.enabled:
            return
        if message.author.bot:
            return
        if random.randint(0, 100) == 50:
            return
        await message.add_reaction("<:tutkegel:620927895132569601>")

    @commands.command(hidden=True)
    async def toggle(self, ctx):
        self.enabled = not self.enabled
        await ctx.send(f"Set enabled to: {self.enabled}")


def setup(bot):
    bot.add_cog(Fun(bot))