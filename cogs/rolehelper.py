import discord
from discord.ext import commands

class RoleHelper(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="year")
    async def _set_year(self, ctx, year: int) -> None:
        """
        Sets your current year into your studies
        """


    @commands.command(name="bachelor")
    async def _set_bachelor(self, ctx) -> None:
        """
        Applies bachelor role.

        Removes Masters role if already set, removes bachelor role if already set
        """
        

    @_set_year.error
    async def _set_year_error(self, ctx, error):
        await ctx.send(error)

def setup(bot):
    bot.add_cog(RoleHelper(bot))