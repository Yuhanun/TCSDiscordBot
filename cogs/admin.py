import discord
from discord.ext import commands

import io
import os
import sys
import json
import inspect
import textwrap
import importlib
import traceback
from contextlib import redirect_stdout


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        """Evaluates code"""

        def get_permitted():
            with open("backend/database.json", 'r') as file:
                return json.load(file)["permitted"]

        if ctx.message.author.id not in get_permitted():
            return await ctx.send("You do not have authorization to use this command")

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')
    
    @commands.command()
    async def lmgtfy(self, ctx, *, term):
        await ctx.send(f"https://lmgtfy.com/?q={term.replace(' ', '+')}")

def setup(bot):
    bot.setup_cog(Admin(bot))