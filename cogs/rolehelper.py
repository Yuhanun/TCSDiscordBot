import discord
from discord.ext import commands

import traceback

from backend.role_helper import trigger_role, send_error, simple_embed

class RoleHelper(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(name="year")
    async def _set_year(self, ctx, year: int) -> None:
        """
        Triggers role that matches current year into your studies.
        """
        result = await trigger_role(ctx.author, f"Year {year}", ctx.guild)
        await simple_embed(ctx, ("Removed " if not result else "Added ") + f"role `Year {year}`" )

    @commands.guild_only()
    @commands.command(name="bachelor")
    async def _set_bachelor(self, ctx) -> None:
        """
        Triggers bachelor role.
        """
        result = await trigger_role(ctx.author, "Bachelors", ctx.guild)
        await simple_embed(ctx, ("Removed " if not result else "Added ") + f"role `Bachelors`" )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            return await send_error(ctx, error)
        
        raise error

def setup(bot):
    bot.add_cog(RoleHelper(bot))