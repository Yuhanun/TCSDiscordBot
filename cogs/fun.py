import random
import requests
import time

import discord
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
        """
        Send 3x3 tutkegel emotes
        """
        await ctx.send("<:tegel9:634119527680180261>"
                       "<:tegel8:634119528158199841>"
                       "<:tegel7:634119527927513089>"
                       "\n<:tegel6:634119527868661773>"
                       "<:tegel5:634119527877050399>"
                       "<:tegel4:634119528346812429>"
                       "\n<:tegel3:634119528825094164>"
                       "<:tegel2:634119528330035200>"
                       "<:tegel1:634119528439218206>")

    # Replies "Alexa, play Despacito" to messages containing "this is so sad"
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not self.enabled:
            return
        if message.author.bot:
            return
        if "this is so sad" not in message.content.lower():
            return
        await message.channel.send("Alexa, play Despacito")

    # Replies "WHO DID THIS" together with laughing crying emoji's to messages that contain "lmao"
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not self.enabled:
            return
        if message.author.bot:
            return
        if "lmao" not in message.content.lower():
            return
        response = ("<:lol:646089960792916018>""<:lol:646089960792916018>""<:lol:646089960792916018>"
                    "WHO DID THIS"
                    "<:lol:646089960792916018>""<:lol:646089960792916018>""<:lol:646089960792916018>")

        await message.channel.send(response)

    @commands.command(name="vb")
    async def vb(self, ctx):
        """
        Check if VB is open and, if it is, send a screenshot of the webcam
        """
        try:
            async with ctx.channel.typing():
                webpage = requests.get("https://www.vestingbar.nl/en/")
                webpage = webpage.content.decode('utf-8')
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
