"""
===

MIT License

Copyright (c) 2018 Dusty.P https://github.com/dustinpianalto

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""


import discord
from discord.ext import commands
import logging
from ..shared_libs.utils import paginate, run_command, loggable
import asyncio


class Git(loggable.Loggable):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(case_insensitive=True, invoke_without_command=True)
    async def git(self, ctx):
        """Run help git for more info"""
        await ctx.send('https://github.com/Annihilator708/Sebi-Machine/')
    
    @commands.command(case_insensitive=True, brief='Gets the Trello link.')
    async def trello(self, ctx):
        await ctx.send('<https://trello.com/b/x02goBbW/sebis-bot-tutorial-roadmap>')

    @git.command()
    async def pull(self, ctx):
        self.logger.warning('Invoking git-pull')
        await ctx.trigger_typing()
        if ctx.author.id not in self.bot.ownerlist:
            return await ctx.send('Only my contributors can use me like this :blush:', delete_after=10)
        em = discord.Embed(style='rich',
                           title=f'Git Pull',
                           color=self.bot.embed_color)
        em.set_thumbnail(url=f'{ctx.guild.me.avatar_url}')

        # Pretty sure you can just do await run_command() if that is async,
        # or run in a TPE otherwise.
        result = await asyncio.wait_for(self.bot.loop.create_task(
            run_command('git fetch --all')), 120) + '\n'
        result += await asyncio.wait_for(self.bot.loop.create_task(
            run_command('git reset --hard origin/$(git rev-parse '
                        '--symbolic-full-name --abbrev-ref HEAD)')),
            120) + '\n\n'
        result += await asyncio.wait_for(self.bot.loop.create_task(
            run_command('git show --stat | sed "s/.*@.*[.].*/ /g"')), 10)

        results = paginate(result, maxlen=1014)
        for page in results[:5]:
            em.add_field(name='\uFFF0', value=f'{page}')
        await ctx.send(embed=em)

    @git.command()
    async def status(self, ctx):
        await ctx.trigger_typing()
        if ctx.author.id not in self.bot.ownerlist:
            return await ctx.send('Only my contributors can use me like this :blush:', delete_after=10)
        em = discord.Embed(style='rich',
                           title=f'Git Status',
                           color=self.bot.embed_color)
        em.set_thumbnail(url=f'{ctx.guild.me.avatar_url}')
        result = await asyncio.wait_for(self.bot.loop.create_task(
            run_command('git status')), 10)
        results = paginate(result, maxlen=1014)
        for page in results[:5]:
            em.add_field(name='\uFFF0', value=f'{page}')
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Git(bot))
