#!/usr/bin/python
# -*- coding: <encoding name> -*-

from discord.ext import commands
import discord
import traceback

class Upload:
    """
    CogName should be the name of the cog
    """
    def __init__(self, bot):
        self.bot = bot
        print('upload loaded')

    @commands.command()
    async def reload(self, ctx, *, extension: str):
        """Reload an extension."""
        await ctx.trigger_typing()
        if ctx.author.id not in self.bot.ownerlist:
            return await ctx.send('Only my contributors can use me like this :blush:', delete_after=10)

        extension = extension.lower()
        try:
            self.bot.unload_extension("src.cogs.{}".format(extension))
            self.bot.load_extension("src.cogs.{}".format(extension))
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f'Could not reload `{extension}` -> `{e}`')
        else:
            await ctx.send(f'Reloaded `{extension}`.')

    @commands.command()
    async def reloadall(self, ctx):
        """Reload all extensions."""
        await ctx.trigger_typing()
        if ctx.author.id not in self.bot.ownerlist:
            return await ctx.send('Only my contributors can use me like this :blush:', delete_after=10)

        try:
            for extension in self.bot.extensions:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
            await ctx.send(f"Reload success! :thumbsup:\n")
        except Exception as e:
            await ctx.send(f"Could not reload `{extension}` -> `{e}`.\n")

    @commands.command()
    async def unload(self, ctx, *, extension: str):
        """Unload an extension."""
        await ctx.trigger_typing()
        if ctx.author.id not in self.bot.ownerlist:
            return await ctx.send('Only my contributors can use me like this :blush:', delete_after=10)

        extension = extension.lower()
        try:
            self.bot.unload_extension("src.cogs.{}".format(extension))

        except Exception as e:
            traceback.print_exc()
            if ctx.message.author.id not in self.bot.owner_list:
                await ctx.send(f'Could not unload `{extension}` -> `{e}`')

        else:
            await ctx.send(f'Unloaded `{extension}`.')

    @commands.command()
    async def load(self, ctx,  *, extension: str):
        """Load an extension."""
        await ctx.trigger_typing()
        if ctx.author.id not in self.bot.ownerlist:
            return await ctx.send('Only my contributors can use me like this :blush:', delete_after=10)

        extension = extension.lower()
        try:
            self.bot.load_extension("src.cogs.{}".format(extension))
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f'Could not load `{extension}` -> `{e}`')
        else:
            await ctx.send(f'Loaded `{extension}`.')

    @commands.command()
    async def kick(self, ctx, member: discord.Member = None):
        """
        Kick a discord member from your server.
        Only contributors can use this command

        Usage:
          - kick <discord.member>

        """
        await ctx.trigger_typing()
        if ctx.author.id not in self.bot.ownerlist:
            return await ctx.send('Only my contributors can use me like this :blush:', delete_after=10)

        if member is None:
            await ctx.send('Are you sure you are capable of this command?')
        try:
            await member.kick()
            await ctx.send(f'You kicked **`{member.name}`** from **`{ctx.guild.name}`**')

        except Exception as e:
            await ctx.send('You may not use this command you do not have permission in server:\n\n**`{ctx.guild.name}`**'
                           f'\n\n```py\n{e}\n```')

def setup(bot):
    bot.add_cog(Upload(bot))