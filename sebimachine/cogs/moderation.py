#!/usr/bin/python
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord


class Moderation:
    """
    Moderation Commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, member: discord.Member = None):
        """
        Kick a discord member from your server.
        Only contributors can use this command.

        Usage:
          - kick <discord.member>

        """
        await ctx.trigger_typing()
        if ctx.author.id not in self.bot.ownerlist:
            return await ctx.send(
                "Only my contributors can use me like this :blush:", delete_after=10
            )

        if member is None:
            await ctx.send("Are you sure you are capable of this command?")
        try:
            await member.kick()
            await ctx.send(
                f"You kicked **`{member.name}`** from **`{ctx.guild.name}`**"
            )

        except Exception as e:
            await ctx.send(
                "You may not use this command, as you do not have permission to do so:\n\n**`{ctx.guild.name}`**"
                f"\n\n```py\n{e}\n```"
            )

    @commands.command()
    async def ban(self, ctx, member: discord.Member = None):
        """
        Ban a discord member from your server.
        Only contributors can use this command.

        Usage:
          - ban <discord.member>

        """
        await ctx.trigger_typing()
        if ctx.author.id not in self.bot.ownerlist:
            return await ctx.send(
                "Only my contributors can use me like this :blush:", delete_after=10
            )

        if member is None:
            await ctx.send("Are you sure you are capable of this command?")
        try:
            await member.ban()
            await ctx.send(
                f"You banned **`{member.name}`** from **`{ctx.guild.name}`**"
            )

        except Exception as e:
            await ctx.send(
                "You may not use this command, as you do not have permission to do so:\n\n**`{ctx.guild.name}`**"
                f"\n\n```py\n{e}\n```"
            )


def setup(bot):
    bot.add_cog(Moderation(bot))
