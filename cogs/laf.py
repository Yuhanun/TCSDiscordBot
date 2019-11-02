import discord
from discord.ext import commands
from discord.ext.commands import Context

from backend import database

class Laf(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.enabled = True
        self.bot = bot
    
    # Increments the laf_counter if someone gets called laf
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not self.enabled:
            return
        if message.author.bot:
            return
        if "laf" not in message.content.lower():
            return
        if not message.mentions:
            return

        # checks if the message is a valid command
        # otherwise .hoelafis @user would also increase the count
        # im sorry about the try catch block
        try:
            ctx = await bot.get_context(message)
        except NameError:
            return  
        if ctx.valid:
            return
        
        for mention in message.mentions:
            await database.update_laf(mention.id, 1)

    # Send the leaderboards:
    @commands.command(name='wiezijnhetlafst',
                      aliases=['whoarehetlafst', 'laffebende',
                               'wieishetlafst', 'laffehomos' , 'kleinespelers'])
    async def on_karma_leaderboard_request(self, ctx: Context):
        """
        Show the most laf users
        """
        message = self.order_leaderboard(await database.get_top_karma(10))
        await ctx.send(message if message else 'Nobody is mooi')

    # Send the negative leaderboards:
    @commands.command(name='wiezijnhetminstlaf',
                      aliases=['whoarehetleastlaf', 'grotespelers', 'whoishetleastlaf',
                               'wieishetminstlaf'])
    async def on_karma_worst_leaderboard_request(self, ctx: Context):
        """
        Show the least laf users
        """
        message = self.order_leaderboard(await database.get_reversed_top_laf(10))
        await ctx.send(message if message else "Why don't you guys call someone laf? @P1mguin, for example")


    # Returns a string in the following format:
    # {ranking}. {name} got called laf {score}x
    def order_leaderboard(self, karma):
        return '\n'.join([f'{x[0] + 1}. {self.bot.get_user(x[1][0]).name} '
                          f'got called laf {x[1][1]}x'
                          for x in enumerate(karma)])

    # Send a current status for the player that requested it in the following format:
    # {mention} - Your were called laf {score}x
    @commands.command(name='hoelafbenik', aliases=['howlafami'])
    async def on_karma_self_request(self, ctx: Context):
        """
        Show how laf you are
        """
        author: discord.User = ctx.author
        response: (int, int) = await database.get_laf(author.id)
        await ctx.send(
            f'{author.mention} - Your were called laf {response}x ')

    # Send a current status for a given player in the following format:
    # {mention} - Your were called laf {score}x
    @commands.command(name='hoelafis', aliases=['howlafis'])
    async def on_karma_user_request(self, ctx: Context, user: discord.User):
        """
        Show how laf someone is
        """
        response: (int, int) = await database.get_laf(user.id)
        await ctx.send(
            f'{user.name} has been called laf {response}x ')

def setup(bot):
    bot.add_cog(Laf(bot))