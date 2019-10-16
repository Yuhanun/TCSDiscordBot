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
        if not random.randint(0, 100) == 50:
            return
        await message.add_reaction("<:tutkegel:620927895132569601>")

    @commands.command(hidden=True)
    async def toggle(self, ctx):
        self.enabled = not self.enabled
        await ctx.send(f"Set enabled to: {self.enabled}")

    # Send 3x3 emote grid with tutkegel
    # emotes are from Davvos11's test discord, so there wont be a need to use up emote space on the TCS discord
    @commands.command(name="tutkegel")
    async def tutkegel(self, ctx):
        await ctx.send("<:tegel9:634119527680180261><:tegel8:634119528158199841><:tegel7:634119527927513089>\n<:tegel6:634119527868661773><:tegel5:634119527877050399><:tegel4:634119528346812429>\n<:tegel3:634119528825094164><:tegel2:634119528330035200><:tegel1:634119528439218206>")


def setup(bot):
    bot.add_cog(Fun(bot))