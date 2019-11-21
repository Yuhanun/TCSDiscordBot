import random
import aiohttp
import time

import discord
from discord.ext import commands

async def on_message_tutkegel(self, message: discord.Message):
    if not random.randint(0, 100) == 50:
        return
    await message.add_reaction("<:tutkegel:620927895132569601>")

# Replies "Alexa, play Despacito" to messages containing "this is so sad"
async def on_message_alexa(self, message: discord.Message):
    if "this is so sad" not in message.content.lower():
        return
    await message.channel.send("Alexa, play Despacito")

# Replies "WHO DID THIS" together with laughing crying emoji's to messages that contain "lmao"
async def on_message_lmao(self, message: discord.Message):
    if "lmao" not in message.content.lower():
        return
    response = ("<:lol:646089960792916018>""<:lol:646089960792916018>""<:lol:646089960792916018>"
                "WHO DID THIS"
                "<:lol:646089960792916018>""<:lol:646089960792916018>""<:lol:646089960792916018>")

    await message.channel.send(response)


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.enabled = True
        self.bot = bot

    @commands.command(hidden=True)
    async def toggle(self, ctx):
        self.enabled = not self.enabled
        await ctx.send(f"Set enabled to: {self.enabled}")

    # Message listeners
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not self.enabled:
            return
        if message.author.bot:
            return
        await on_message_tutkegel(self, message)
        await on_message_alexa(self, message)
        await on_message_lmao(self, message)

    # Send 3x3 emote grid with tutkegel.
    # Emotes are from John's tutkegel discord,
    # therefore, there isn't a need to waste emote space on the TCS discord
    @commands.command(name="tutkegel")
    async def tutkegel(self, ctx):
        """
        Send 5x10 tutkegel emotes
        """
        await ctx.send(
"""<:teg001:646737006377959445><:teg002:646736996764614668><:teg003:646736971884003328><:teg004:646737001298657290><:teg005:646736981765914624><:teg006:646736984739676160><:teg007:646736998337347604><:teg008:646737019673772083><:teg009:646737018428194886><:teg010:646736963998711858>
<:teg011:646736974111178758><:teg012:646737023750897675><:teg013:646737016133779456><:teg014:646736977751834626><:teg015:646736970625581056><:teg016:646737012119830544><:teg017:646737008651272212><:teg018:646736988061302847><:teg019:646736969329672203><:teg020:646736976866836484>
<:teg021:646737004503236609><:teg022:646737013562671114><:teg023:646737007476998144><:teg024:646737022266114078><:teg025:646736978691489803><:teg026:646737000036171806><:teg027:646736966758694936><:teg028:646737014779150337><:teg029:646736985884721182><:teg030:646737021255286834>
<:teg031:646736975017017374><:teg032:646736993828470804><:teg033:646736983661608961><:teg034:646737003597135872><:teg035:646736980260159539><:teg036:646736992599539732><:teg037:646737011188957236><:teg038:646736995954982912><:teg039:646736972915802121><:teg040:646737009989124116>
<:teg041:646737002183524362><:teg042:646736967949746216><:teg043:646736982835462145><:teg044:646736965894406144><:teg045:646737025155727361><:teg046:646736964900356106><:teg047:646737017031491604><:teg048:646736986899742730><:teg049:646736999255900160><:teg050:646737023125946390>
""")

    @commands.command(name="vb")
    async def vb(self, ctx):
        """
        Check if VB is open and, if it is, send a screenshot of the webcam
        """
        try:
            async with ctx.channel.typing():
                session = self.bot._session
                async with session.get("https://www.vestingbar.nl/en/") as resp:
                    webpage = await resp.text()
        except ConnectionError:
            msg = "Cannot reach vestingbar.nl, is it down?"
            open = False

        if 'gfx/SignOpen.png' in webpage:
            msg = "Vestingbar seems to be open"
            open = True
        elif 'gfx/SignClosed.png' in webpage:
            msg = "Vestingbar seems to be closed"
            open = False
        else:
            msg = "Can't determine if vestingbar is open, did they change their webpage?"
            open = False

        if open:
            colour = discord.colour.Colour.green()
            img = "https://www.vestingbar.nl/webcam-images/image.jpg?"+str(time.time())
        else:
            colour = discord.colour.Colour.red()
            img = ''


        embed: discord.Embed = discord.Embed(title="Is VB open?",
                                             description=msg,
                                             url='https://www.vestingbar.nl/en/',
                                             colour=colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.command(name="avatar",aliases=['pf'])
    async def avatar(self, ctx, user: discord.User):
        """
        Show a user's discord profile picture/avatar
        """
        member = ctx.guild.get_member(user.id)

        embed: discord.Embed = discord.Embed(title=user.name+"'s avatar:",
                                             colour=member.colour)
        embed.set_image(url=user.avatar_url)
        embed.set_author(name=user.display_name, icon_url=user.avatar_url)
        await ctx.send(embed=embed)
    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a user")
            raise error
        elif isinstance(error, commands.BadArgument):
            await ctx.send('User not found')
            raise error

def setup(bot):
    bot.add_cog(Fun(bot))
