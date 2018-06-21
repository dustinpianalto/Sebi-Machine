# !/usr/bin/python
# -*- coding: utf8 -*-
"""
App entry point.

Something meaningful here, eventually.
"""
import asyncio
import json
import logging
import os
import random
import sys
import traceback
from typing import Dict

import discord
from discord.ext import commands

from .config.config import LoadConfig
from .shared_libs import database
from .shared_libs.ioutils import in_here
from .shared_libs.loggable import Loggable


# Init logging to output on INFO level to stderr.
logging.basicConfig(level="INFO")


# If uvloop is installed, change to that eventloop policy as it
# is more efficient
try:
    # https://stackoverflow.com/a/45700730
    if sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
        logging.warning("Detected Windows. Changing event loop to ProactorEventLoop.")
    else:
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        del uvloop
except BaseException as ex:
    logging.warning(
        f"Could not load uvloop. {type(ex).__qualname__}: {ex};",
        "reverting to default impl.",
    )
else:
    logging.info(f"Using uvloop for asyncio event loop policy.")


# Bot Class
# Might be worth moving this to it's own file?
class SebiMachine(commands.Bot, LoadConfig, Loggable):
    """This discord is dedicated to http://www.discord.gg/GWdhBSp"""

    def __init__(self):
        # Initialize and attach config / settings
        LoadConfig.__init__(self)
        commands.Bot.__init__(self, command_prefix=self.defaultprefix)
        with open(in_here("config", "PrivateConfig.json")) as fp:
            self.bot_secrets = json.load(fp)
        self.db_con = database.DatabaseConnection(**self.bot_secrets["db-con"])
        self.failed_cogs_on_startup = {}
        self.book_emojis: Dict[str, str] = {
            "unlock": "🔓",
            "start": "⏮",
            "back": "◀",
            "hash": "#\N{COMBINING ENCLOSING KEYCAP}",
            "forward": "▶",
            "end": "⏭",
            "close": "🇽",
        }

        # Load plugins
        # Add your cog file name in this list
        with open(in_here("extensions.txt")) as cog_file:
            cogs = cog_file.readlines()

        for cog in cogs:
            # Could this just be replaced with `strip()`?
            try:
                cog = cog.replace("\n", "")
                self.load_extension(f"src.cogs.{cog}")
                self.logger.info(f"Loaded: {cog}")
            except (ModuleNotFoundError, ImportError) as ex:
                logging.exception(f'Could not load {cog}', exc_info=(type(ex), ex, ex.__traceback__))
                self.failed_cogs_on_startup[cog] = ex
                                  
    async def on_ready(self):
        """On ready function"""
        self.maintenance and self.logger.warning("MAINTENANCE ACTIVE")
        with open(f"src/config/reboot", "r") as f:
            reboot = f.readlines()
        if int(reboot[0]) == 1:
            await self.get_channel(int(reboot[1])).send("Restart Finished.")
            for cog, ex in self.failed_cogs_on_startup.items():
                tb = ''.join(traceback.format_exception(type(ex), ex, ex.__traceback__))[-1500:]
                await ctx.send(
                    f'FAILED TO LOAD {cog} BECAUSE OF {type(ex).__name__}: {ex}\n'
                    f'{tb}'
                )
        with open(f"src/config/reboot", "w") as f:
            f.write(f"0")

    async def on_command_error(self, ctx, error):
        """
        The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception
        """
        jokes = [
            "I'm a bit tipsy, I took to many screenshots...",
            "I am rushing to the 24/7 store to get myself anti-bug spray...",
            "Organizing turtle race...",
            "There is no better place then 127.0.0.1...",
            "Recycling Hex Decimal...",
            "No worry, I get fixed :^)...",
            "R.I.P, press F for respect...",
            "The bug repellent dit not work...",
            "You found a bug in the program. Unfortunately the joke did not fit here, better luck next time...",
        ]

        # CommandErrors triggered by other propagating errors tend to get wrapped. This means
        # if we have a cause, we should probably consider unwrapping that so we get a useful
        # message.

        # If command is not found, return
        em = discord.Embed(colour=self.error_color)
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            em.title = "Command Not Found"
            em.description = f"{ctx.prefix}{ctx.invoked_with} is not a valid command."
        else:
            error = error.__cause__ or error
            tb = traceback.format_exception(
                type(error), error, error.__traceback__, limit=2, chain=False
            )
            tb = "".join(tb)
            joke = random.choice(jokes)
            fmt = (
                f"**`{self.defaultprefix}{ctx.command}`**\n{joke}\n\n**{type(error).__name__}:**:\n```py\n{tb}\n```"
            )
            em.title = (
                f"**{type(error).__name__}** in command {ctx.prefix}{ctx.command}"
            )
            em.description = str(error)

        await ctx.send(embed=em)

    async def on_message(self, message):
        # Make sure people can't change the username
        if message.guild:
            if message.guild.me.display_name != self.display_name:
                try:
                    await message.guild.me.edit(nick=self.display_name)
                except:
                    pass
        else:
            if (
                "exec" in message.content
                or "repl" in message.content
                or "token" in message.content
            ) and message.author != self.user:
                await self.get_user(351794468870946827).send(
                    f"{message.author.name} ({message.author.id}) is using me "
                    f"in DMs\n{message.content}"
                )

        # If author is a bot, ignore the message
        if message.author.bot:
            return

        # Make sure the command get processed as if it was typed with lowercase
        # Split message.content one first space
        command = message.content.split(None, 1)
        if command:
            command[0] = command[0].lower()
            message.content = " ".join(command)
        message.content = " ".join(command)

        # process command
        await self.process_commands(message)


client = SebiMachine()

client.run(client.bot_secrets["bot-key"])
