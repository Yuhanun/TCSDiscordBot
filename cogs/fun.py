import random
from typing import Union

import discord
from discord import User, Member
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

    # Send 3x3 emote grid with tutkegel.
    # Emotes are from Davvos11's test discord,
    # therefore, there isn't a need to waste emote space on the TCS discord
    @commands.command(name="tutkegel")
    async def tutkegel(self, ctx):
        await ctx.send("<:tegel9:634119527680180261>"
                       "<:tegel8:634119528158199841>"
                       "<:tegel7:634119527927513089>"
                       "\n<:tegel6:634119527868661773>"
                       "<:tegel5:634119527877050399>"
                       "<:tegel4:634119528346812429>"
                       "\n<:tegel3:634119528825094164>"
                       "<:tegel2:634119528330035200>"
                       "<:tegel1:634119528439218206>")

    class Emotes(discord.Enum):
        DAS_MOOI = ':dasmooi:'
        DAS_NIET_MOOI = 'dasnietmooi'

    def change_count(self, user: Union[Member, User], reaction: discord.Reaction, increment: bool):
        if self.enabled:
            emoji: discord.Emoji = reaction.emoji
            message: discord.Message = reaction.message
            if emoji.name == self.Emotes.DAS_MOOI:
                if increment:
                    # Increment
                    pass
                else:
                    # Decrement
                    pass
            elif emoji.name == self.Emotes.DAS_NIET_MOOI:
                if increment:
                    # Increment
                    pass
                else:
                    # Decrement
                    pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: Union[Member, User]):
        self.change_count(user, reaction, True)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: Union[Member, User]):
        self.change_count(user, reaction, False)


def setup(bot):
    bot.add_cog(Fun(bot))
