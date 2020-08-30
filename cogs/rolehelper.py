import discord
from discord.ext import commands

from datetime import datetime
import re

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
            role = await ctx.guild.create_role(name=f"Year {year}")

        result = await trigger_role(ctx.author, role or f"Year {year}", ctx.guild)
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

    @commands.guild_only()
    @commands.has_any_role("Administrator", "Moderator")
    @commands.command(name="update_years")
    async def update_years(self, ctx, *args) -> None:
        """
        Updates the year roles of everyone in the server (that joined before last August)
        Optional arguments: "force" to also upgrade people that joined after last August, "downgrade" to downgrade
        """
        async with ctx.channel.typing():
            largs = [s.lower() for s in args]
            last_august = self._get_last_date(8, 1)
            count = 0
            guild = ctx.channel.guild
            too_old = []

            for member in guild.members:
                if "force" not in largs:
                    # If the member joined after last august
                    if member.joined_at > last_august:
                        continue

                try:
                    # Increase or decrease the roles
                    if "downgrade" in largs:
                        await self._change_year(member, -1)
                    else:
                        await self._change_year(member, 1)
                except MemberIsTooOld:
                    too_old.append(member.display_name)
                    continue
                except MemberHasNoYearRole:
                    continue

                count += 1

        await ctx.send("Changed the ranks of "+str(count) +
                       " members (this server has a total size of " + str(guild.member_count) + ")")
        if len(too_old) > 0:
            await ctx.send("Please manually change the roles of " + ", ".join(too_old))

    @staticmethod
    async def _change_year(member: discord.Member, amount: int = 1):
        # Get the current year of the user
        regex = re.compile("^Year [0-9]+$")
        try:
            current_role = [role for role in member.roles if regex.match(role.name)][0]
        except IndexError:  # If index 0 is out of range; the member does not have a year role
            raise MemberHasNoYearRole
        current_year = int(re.findall("[0-9]+", current_role.name)[0])

        # Get the new role of the user
        new_name = "Year " + str(current_year + amount)
        try:
            new_role = [role for role in member.guild.roles if role.name == new_name][0]
        except IndexError:  # If index 0 is out of range; a role with that year does not exist yet
            raise MemberIsTooOld

        # Remove old role and assign new role
        await member.remove_roles(current_role)
        await member.add_roles(new_role)


    @staticmethod
    def _get_last_date(month: int, day: int) -> datetime:
        """
        Gets the last occurrence of a date (month and date)
        :return: a datetime object on the last occurrence of the provided date
        """
        today = datetime.now()
        if today.month >= month and today.day >= day:
            return datetime(today.year, month, day)
        else:
            return datetime(today.year - 1, month, day)

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
            to_add = discord.utils.find(lambda role: role.name.lower(
            ) == message.content.lower(), member.guild.roles)
            if to_add is not None:
                _new_member["roles"].append(to_add)
            else:
                await member.send("Could not find that do-group, ask one of the admins to apply it later.")

        await member.send(f"Which house are you in?\nIf you are not in a house, then just send a `.`, otherwise just `red` or `blue`, etc")
        message = await self.bot.wait_for("message", check=_check_member_dm)

        if message.content != ".":
            to_add = discord.utils.find(lambda role: role.name.lower(
            ) == f"{message.content.lower()} house", member.guild.roles)
            _new_member["roles"].append(to_add)

        await member.edit(**_new_member)
        await member.send("Your roles have been applied! Welcome to the server, make sure to read the rules!")


def setup(bot):
    bot.add_cog(RoleHelper(bot))


class MemberHasNoYearRole(Exception):
    pass


class MemberIsTooOld(Exception):
    pass
