#!/usr/bin/python
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import random
import aiohttp

class Fun:
    """
    CogName should be the name of the cog
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sebisauce(self, ctx):
        """
        Get a image related to Sebi.
        Sebi is a random guy with perfect code related jokes.

        Usage:
          - sebisauce
        """
        await ctx.trigger_typing()
        url = 'http://ikbengeslaagd.com/API/sebisauce.json'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                source = await response.json(encoding='utf8')

        total_sebi = 0
        for key in dict.keys(source):
            total_sebi += 1

        im = random.randint(0, int(total_sebi) - 1)

        await ctx.send(embed=discord.Embed(
            title='\t',
            description='\t',
            color=self.bot.embed_color).set_image(
            url=source[str(im)]))

def setup(bot):
    bot.add_cog(Fun(bot))
