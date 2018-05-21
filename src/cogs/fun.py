#!/usr/bin/python
# -*- coding: <encoding name> -*-

from discord.ext import commands
import discord
import random

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
        source = await self.bot.brequest.aio_json('http://ikbengeslaagd.com/API/sebisauce.json')

        total_sebi = 0
        for key in dict.keys(source):
            total_sebi += 1

        im = random.randint(0, int(total_sebi) - 1)

        msg = await ctx.send(
            embed=discord.Embed(
                title='\t',
                description='\t',
                color=0xf20006).set_image(
                url=source[str(im)]))
        return await msg.add_reaction(self.bot.success)

def setup(bot):
    bot.add_cog(Fun(bot))
