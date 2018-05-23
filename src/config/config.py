#!/usr/bin/python
# -*- coding: <encoding name> -*-

import json
import discord
import os

class LoadConfig:
    """
    All config is collected here
    """
    def __init__(self):
        # Read our config file
        with open('src/config/Config.json') as fp:
            self.config = json.load(fp)

        # Initialize config

        self.ownerlist = self.config["ownerlist"]
        self.defaultprefix = self.config["prefix"]
        self.version = self.config["version"]
        self.display_name = self.config["display_name"]
        self.maintenance = self.config["maintenance"]
        self.embed_color = discord.Color(0x00FFFF)
        if self.maintenance == 'False':
            self.maintenance = False
        else:
            self.maintenance = True
