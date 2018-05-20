#!/usr/bin/python
# -*- coding: <encoding name> -*-

from discord.ext import commands
import discord

class CogName:
    """
    CogName should be the name of the cog
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Say pong"""
        await ctx.send('Pong')

def setup(bot):
    bot.add_cog(CogName(bot))