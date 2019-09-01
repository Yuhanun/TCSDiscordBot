import datetime
from typing import Union, Optional

import discord
from discord.ext import commands


async def trigger_role(member: discord.Member, role: Union[discord.Role, int, str], guild: Optional[discord.Guild] = None) -> bool:
    """
    Triggers a role on a member.

    If member already has `role` then role is removed, if the member does not yet have the `role`, then it will be applied.

    If role is a discord.Role then nothing is pulled from cache
    If role is an integer then a discord.Role object is pulled from cache
    if role is a string, then a discord.Role object is pulled from the `guild.roles` cache.

    If `guild` is None, and `role` is int or str, then TypeError is raised

    Throws:
        TypeError, see above
        ValueError if the `role` cannot be retrieved from cache
        Whatever discord.Member.add_roles can throw


    returns False if role was removed, True if it was added
    """

    if type(role) == int:
        role = discord.utils.get(guild.roles, id=role)

    elif type(role) == str:
        role = discord.utils.get(guild.roles, name=role)

    elif not isinstance(role, discord.Role):
        raise TypeError(f"Expected discord.Role, got {type(role)}")

    if role is None:
        raise ValueError("Role could not be retrieved from cache")

    if guild is None and isinstance(role, (str, int, )):
        raise TypeError(
            "Expected a guild since role was str or int, but got None")

    def has_role(member: discord.Member, role: discord.Role) -> bool:
        """Returns True if the member has the role, false if not"""
        return role in member.roles

    if has_role(member, role):
        await member.remove_roles(role)
        return False

    await member.add_roles(role)
    return True


async def simple_embed(ctx, text):
    await ctx.send(
        embed=discord.Embed(title=text,
                            colour=discord.Colour(0x00FF00), timestamp=datetime.datetime.utcnow())
        .set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        .set_footer(text="Success!"))


async def send_error(ctx, error):
    await ctx.send(
        embed=discord.Embed(title=str(error),
                            colour=discord.Colour(0xFF0000), timestamp=datetime.datetime.utcnow())
        .set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        .set_footer(text="Guild only!"))
