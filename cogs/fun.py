import random

import discord
from discord.ext import commands
from discord.ext.commands import Context

from backend import database


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

    # Send the leaderboards in the following format:
    # {ranking}. {name} - {positives} Positives and {negatives} Negatives
    @commands.command(name='wiezijnhetmooist',
                      aliases=['whoarehetmooist', 'spiegeltjespiegeltjeaandewand'])
    async def on_karma_leaderboard_request(self, ctx: Context):
        message = '\n'.join([f'{x[0] + 1}. {self.bot.get_user(x[1][0]).name} - '
                             f'{x[1][1]} Positives and {x[1][2]} Negatives'
                             for x in enumerate(database.get_top_karma(10))])
        await ctx.send(message if message else 'Nobody is mooi')

    # Send a current status for a given player in the following format:
    # {mention} - You currently have {positives} Positives and {negatives} Negatives
    @commands.command(name='hoemooibenik', aliases=['howmooiami'])
    async def on_karma_self_request(self, ctx: Context):
        author: discord.User = ctx.author
        response: (int, int) = database.get_karma(author.id)
        await ctx.send(f'{author.mention} - You currently have: {response[0]} '
                       f'Positives and {response[1]} Negatives')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, member: discord.Member):
        await self.change_count(reaction, member, True)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, member: discord.Member):
        await self.change_count(reaction, member, False)

    class KarmaEmotes(discord.Enum):
        POSITIVE = 'dasmooi'
        NEGATIVE = 'dasnietmooi'

    # Check if the karma count should be changed, if so, change it
    async def change_count(self, reaction: discord.Reaction, member: discord.Member,
                           increment: bool):
        # Check if the user doesn't want to give karma to themselves.
        # It is also important that Tegel's opinion doesn't count.
        if self.enabled and member != reaction.message.author \
                and not discord.utils.get(member.roles, name='Tegel'):
            emoji: discord.emoji.Emoji = reaction.emoji
            # Check if the emoji is a karma emoji
            if type(emoji) == discord.emoji.Emoji:
                if emoji.name == self.KarmaEmotes.POSITIVE.value:
                    # Update the positive karma
                    await database.update_karma(reaction.message.author.id,
                                                (1 if increment else -1, 0))
                elif emoji.name == self.KarmaEmotes.NEGATIVE.value:
                    # Update the negative karma
                    await database.update_karma(reaction.message.author.id,
                                                (0, 1 if increment else -1))


def setup(bot):
    bot.add_cog(Fun(bot))
