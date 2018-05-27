#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        now = ctx.message.created_at
        msg = await ctx.send('Pong')
        sub = msg.created_at - now
        await msg.edit(content=f'🏓Pong, **{sub.total_seconds() * 1000}ms**')
        

def setup(bot):
    bot.add_cog(CogName(bot))
