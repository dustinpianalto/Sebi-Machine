# !/usr/bin/python
# -*- coding: utf8 -*-
"""
App entry point.

Something meaningful here, eventually.
"""
import asyncio
import json
import logging
import random
import traceback
import os
import sys

import discord
from discord.ext import commands

from src.config.config import LoadConfig
from src.shared_libs.loggable import Loggable
from src.shared_libs.ioutils import in_here


# Init logging to output on INFO level to stderr.
logging.basicConfig(level='INFO')        


# If uvloop is installed, change to that eventloop policy as it 
# is more efficient
try:
    # https://stackoverflow.com/a/45700730
    if sys.platform == 'win32':
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
        logging.warning('Detected Windows. Changing event loop to ProactorEventLoop.')
    else:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        del uvloop
except BaseException as ex:
    logging.warning(f'Could not load uvloop. {type(ex).__qualname__}: {ex};',
                    'reverting to default impl.')
else:
    logging.info(f'Using uvloop for asyncio event loop policy.')


# Bot Class
# Might be worth moving this to it's own file? 
class SebiMachine(commands.Bot, LoadConfig, Loggable):
    """This discord is dedicated to http://www.discord.gg/GWdhBSp"""
    def __init__(self):
        # Initialize and attach config / settings
        LoadConfig.__init__(self)
        commands.Bot.__init__(self, command_prefix=self.defaultprefix)

        # Load plugins
        # Add your cog file name in this list
        with open(in_here('cogs.txt')) as cog_file:
            cogs = cog_file.readlines()
            
        for cog in cogs:
            # Could this just be replaced with `strip()`?
            cog = cog.replace('\n', '')
            self.load_extension(f'src.cogs.{cog}')
            self.logger.info(f'Loaded: {cog}')

    async def on_ready(self):
        """On ready function"""
        self.maintenance and self.logger.warning('MAINTENANCE ACTIVE')

    async def on_command_error(self, ctx, error):
        """
        The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception
        """
        jokes = ["I\'m a bit tipsy, I took to many screenshots...",
                 "I am rushing to the 24/7 store to get myself anti-bug spray...",
                 "Organizing turtle race...",
                 "There is no better place then 127.0.0.1...",
                 "Recycling Hex Decimal...",
                 "No worry, I get fixed :^)...",
                 "R.I.P, press F for respect...",
                 "The bug repellent dit not work...",
                 "You found a bug in the program. Unfortunately the joke did not fit here, better luck next time..."]

        # CommandErrors triggered by other propagating errors tend to get wrapped. This means
        # if we have a cause, we should probably consider unwrapping that so we get a useful
        # message.

        # If command is not found, return
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            return

        error = error.__cause__ or error
        tb = traceback.format_exception(type(error), error, error.__traceback__, limit=2, chain=False)
        tb = ''.join(tb)
        joke = random.choice(jokes)
        fmt = f'**`{self.defaultprefix}{ctx.command}`**\n{joke}\n\n**{type(error).__name__}:**:\n```py\n{tb}\n```'
        
        # Stops the error handler erroring.
        try:
            await ctx.send(fmt)
        except:
            traceback.print_exc()

    async def on_message(self, message):
        # Make sure people can't change the username
        if message.guild:
            if message.guild.me.display_name != self.display_name:
                try:
                    await message.guild.me.edit(nick=self.display_name)
                except:
                    pass
        else:
            if ('exec' in message.content or 'repl' in message.content or 'token' in message.content) \
                    and message.author != self.user:
                await self.get_user(351794468870946827).send(f'{message.author.name} ({message.author.id}) is using me '
                                                             f'in DMs\n{message.content}')

        # If author is a bot, ignore the message
        if message.author.bot: return

        # Make sure the command get processed as if it was typed with lowercase
        # Split message.content one first space
        command = message.content.split(None, 1)
        if command:
            command[0] = command[0].lower()
            message.content = ' '.join(command)
        message.content = ' '.join(command)

        # process command
        await self.process_commands(message)


client = SebiMachine()
# Make sure the key stays private.
# I am 99% certain this is valid!
with open(in_here('config', 'PrivateConfig.json')) as fp:
    PrivateConfig = json.load(fp)
if PrivateConfig["bot-key"] == '':
    PrivateConfig["bot-key"] = os.getenv('botkey')

client.run(PrivateConfig["bot-key"])
