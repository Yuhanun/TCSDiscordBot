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
        role = discord.utils.get(ctx.guild.roles, name=f"Year {year}")
        if role is None:
            if year not in range(1, 11):
                return await ctx.send(f"{year} is too high to be a year, if you think this is a mistake, please ping one of the admins.")
            # role doesn't exist, create it
            await ctx.guild.create_role(name=f"Year {year}")

        result = await trigger_role(ctx.author, f"Year {year}", ctx.guild)
        await simple_embed(ctx, ("Removed " if not result else "Added ") + f"role `Year {year}`")

    @commands.guild_only()
    @commands.command(name="bachelor")
    async def _set_bachelor(self, ctx) -> None:
        """
        Triggers Bachelor role.
        """
        result = await trigger_role(ctx.author, "Bachelors", ctx.guild)
        await simple_embed(ctx, ("Removed " if not result else "Added ") + f"role `Bachelors`")

    @commands.guild_only()
    @commands.command(name="master")
    async def _set_master(self, ctx) -> None:
        """
        Triggers Masters role.
        """
        result = await trigger_role(ctx.author, "Masters", ctx.guild)
        await simple_embed(ctx, ("Removed " if not result else "Added ") + f"role `Masters`")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            return await send_error(ctx, error)

        else:
            await send_error(ctx, error)

        raise error

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """
        Listener for when a member joins, sends member questionaire for nickname etc
        """
        _new_member = {
            "nick": None,
            "roles": [],
        }

        def _integer_member_dm(message):
            def _is_integer():
                try:
                    int(message.content)
                    return True
                except ValueError:
                    return False

            return _is_integer() and _check_member_dm(message)

        def _check_member_dm(message):
            """Checks if message is sent in DM and whether it's sent by the original person that joined"""
            return message.author.id == member.id and isinstance(message.channel, discord.DMChannel)

        await member.send(f"To gain access to the rest of the channels in the server, you'll have to tell me a few things about yourself.\nPlease tell me your real firstname, for example: Michael")
        message = await self.bot.wait_for("message", check=_check_member_dm)

        _new_member["nick"] = f"{message.content} | {member.name}"[:31]

        await member.send(f"Perfect!\nAre you a bachelor or a masters student?\n0 for bachelor, 1 for masters.")
        message = await self.bot.wait_for("message", check=_check_member_dm)

        is_bachelor = not int(message.content)
        _new_member["roles"].append(
            discord.utils.get(member.guild.roles,
                              name="Bachelors" if is_bachelor else "Masters")
        )

        await member.send(f"Good to know!\nWhich year are you in? If you're in your masters it's either `1` or `2`, if you're in your bachelors then it's 1 through 3.")
        message = await self.bot.wait_for("message", check=_integer_member_dm)

        _new_member["roles"].append(
            discord.utils.get(member.guild.roles,
                              name=f"Year {int(message.content)}")
        )

        await member.send(f"Which do group were you in?\nIf you did not join in the kick-in, capital insensitive, then just send a `.`")
        message = await self.bot.wait_for("message", check=_check_member_dm)

        if message.content != ".":
            to_add = discord.utils.find(lambda role: role.name.lower() == message.content.lower(), member.guild.roles)
            if to_add is not None:
                _new_member["roles"].append(to_add)
            else:
                await member.send("Could not find that do-group, ask one of the admins to apply it later.")

        await member.send(f"Which do house are you in?\nIf you are not in a house, then just send a `.`, otherwise just `red` or `blue`, etc")
        message = await self.bot.wait_for("message", check=_check_member_dm)

        if message.content != ".":
            to_add = discord.utils.find(lambda role: role.name.lower() == f"{message.content.lower()} house", member.guild.roles)
            _new_member["roles"].append(to_add)

        await member.edit(**_new_member)
        await member.send("Your roles have been applied! Welcome to the server, make sure to read the rules!")


def setup(bot):
    bot.add_cog(RoleHelper(bot))
