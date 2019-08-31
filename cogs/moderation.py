from typing import List

import discord
from discord.ext import commands

from backend.role_helper import simple_embed

class Moderation(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.command()
    @commands.has_any_role("Administrator", "Moderator")
    async def kick(self, ctx, to_kick: discord.Member, reason: str = ""):
        """
        Kicks `to_kick` from the server
        """
        await to_kick.kick(reason=reason)
        await simple_embed(ctx, f"Kicked {to_kick}")

    @commands.command()
    @commands.has_any_role("Administrator", "Moderator")
    async def ban(self, ctx, to_ban: discord.Member, reason: str = ""):
        """
        Bans `to_ban` from the server
        """
        await to_ban.ban(reason=reason)
        await simple_embed(ctx, f"Banned {to_ban}")

    @commands.command(alias=["purge", "prune"])
    @commands.has_any_role("Administrator", "Moderator")
    async def purge(self, ctx, limit: int = 100, member: discord.Member = None):
        """
        Purges `limit` messages
        """
        def _to_delete(message):
            return (message.author == member) if member is not None else True

        deleted: List[discord.Message] = await ctx.channel.purge(limit=limit, check=_to_delete)
        await simple_embed(ctx, f"Removed {len(deleted)} messages" + (f" by user {member}" if member is not None else ""))



def setup(bot):
    bot.add_cog(Moderation(bot))