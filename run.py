# !/usr/bin/python
# -*- coding: utf8 -*-

# Import packages
import discord
from discord.ext import commands
import json

# Import custom files
from src.config.config import LoadConfig


# Bot Class
class SebiMachine(commands.Bot, LoadConfig):
    """This discord is dedicated to http://www.discord.gg/GWdhBSp"""
    def __init__(self):
        # Initialize and attach config / settings
        LoadConfig.__init__(self)
        commands.Bot.__init__(self, command_prefix=self.defaultprefix)
        self.embed_color = discord.Color(0x00FFFF)

        # Load plugins
        # Add your cog file name in this list
        cogs = ['example', 'upload', 'git']

        for cog in cogs:
            print(cog)
            self.load_extension(f'src.cogs.{cog}')

    async def on_ready(self):
        """On ready function"""
        if self.maintenance:
            print('MAINTENANCE ACTIVE')

if __name__ == '__main__':
    client = SebiMachine()
    # Make sure the key stays private.
    with open('src/config/PrivateConfig.json') as fp:
        PrivateConfig = json.load(fp)
        fp.close()
    client.run(PrivateConfig["bot-key"])