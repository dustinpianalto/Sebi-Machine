#!/usr/bin/python
# -*- coding: <encoding name> -*-

import json
import psycopg2
import psycopg2.extensions

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
        if self.maintenance == 'False':
            self.maintenance = False
        else:
            self.maintenance = True
