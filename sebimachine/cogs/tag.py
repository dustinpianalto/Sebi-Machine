import discord
from discord.ext import commands
import json
import aiofiles
import asyncio


class Tag:
    def __init__(self, bot):
        self.bot = bot
        with open("sebimachine/shared_libs/tags.json", "r") as fp:
            json_data = fp.read()
            global tags
            tags = json.loads(json_data)

    @commands.group(case_insensitive=True, invoke_without_command=True)
    async def tag(self, ctx, tag=None):
        """Gets a tag"""
        await ctx.trigger_typing()
        if tag is None:
            return await ctx.send(
                "Please provide a argument. Do `help tag` for more info"
            )

        found = tags.get(tag, None)

        if found is None:
            return await ctx.send("Tag not found")

        await ctx.send(found)

    @tag.command(case_insensitive=True)
    async def list(self, ctx):
        """Lists available tags"""
        await ctx.trigger_typing()
        desc = ""
        for i in tags:
            desc = desc + i + "\n"

        if desc == "":
            desc = "None"

        em = discord.Embed(
            title="Available tags:", description=desc, colour=discord.Colour(0x00FFFF)
        )

        await ctx.send(embed=em)

    @tag.command(case_insensitive=True)
    async def add(self, ctx, tag_name=None, *, tag_info=None):
        """Adds a new tag"""
        await ctx.trigger_typing()
        if not ctx.author.guild_permissions.manage_roles:
            return await ctx.send("You are not allowed to do this")

        if tag_name is None or tag_info is None:
            return await ctx.send(
                "Please provide a tag name and the tag info. Do `help tag` for more info"
            )

        exists = False
        for i in tags:
            if i == tag_name:
                exists = True

        if not exists:
            tags.update({tag_name: tag_info})

            async with aiofiles.open("src/shared_libs/tags.json", "w") as fp:
                json_data = json.dumps(tags)
                await fp.write(json_data)

            return await ctx.send("The tag has been added")

        await ctx.send("The tag already exists")

    @tag.command(case_insensitive=True)
    async def remove(self, ctx, tag=None):
        """Remove a existing tag"""
        await ctx.trigger_typing()
        if not ctx.author.guild_permissions.manage_roles:
            return await ctx.send("You are not allowed to do this")

        if tag is None:
            return await ctx.send(
                "Please provide a tag name and the tag info. Do `help tag` for more info"
            )

        found = None
        for i in tags:
            if i == tag:
                found = i

        if found is not None:
            del tags[found]
            async with aiofiles.open("src/shared_libs/tags.json", "w") as fp:
                json_data = json.dumps(tags)
                await fp.write(json_data)

            return await ctx.send("The tag has been removed")

        await ctx.send("The tag has not been found")


def setup(bot):
    bot.add_cog(Tag(bot))
