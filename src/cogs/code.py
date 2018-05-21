from discord.ext import commands
import traceback
import textwrap
from contextlib import redirect_stdout
import io


class REPL:
    """Python in Discords"""
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    def cleanup_code(self, content):
        """
        Automatically removes code blocks from the code.
        """
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return '{0.__class__.__name__}: {0}'.format(e)
        return '{0.text}{1:>{0.offset}}\n{2}: {0}'.format(e, '^', type(e).__name__)


    @commands.command(hidden=True, name='exec')
    async def _eval(self, ctx, *, body: str = None):
        """
        Execute python code in discord chat.
        Only the owner of this bot can use this command.

        Alias:
          - exec
        Usage:
          - exec < python code >
        Example:
          - exec print(546132)
        """
        if ctx.message.author.id not in self.bot.ownerlist:
            return await ctx.send('Only the owner of this bot can use this command')

        if body is None:
            return await ctx.send(
                'Please, use\n'
                f'`{self.bot.config["prefix"]}exec`\n\n'
                '\n`\\`\\`\\`py\n[python code]\n\\`\\`\\`\n'
                'to get the most out of the command')

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.message.channel,
            'author': ctx.message.author,
            'server': ctx.message.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = 'async def func():\n%s' % textwrap.indent(body, '  ')

        try:
            exec(to_compile, env)
        except SyntaxError as e:
            try:
                msg = await ctx.send(f'```py\n{self.get_syntax_error(e)}\n```')

            except Exception as e:
                error = [self.get_syntax_error(e)[i:i+2000] for i in range(0, len(self.get_syntax_error(e)), 2000)]
                for i in error:
                    msg = await ctx.send(f'```py\n{i}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            try:
                msg = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')

            except Exception as e:
                error = [value[i:i + 2000] for i in range(0, len(value), 2000)]
                for i in error:
                    await ctx.send(f'```py\n{i}\n```')

                tracebackerror = [traceback.format_exc()[i:i + 2000] for i in range(0, len(traceback.format_exc()), 2000)]
                for i in tracebackerror:
                    msg = await ctx.send(f'```py\n{i}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try:
                        msg = await ctx.send(f'```py\n{value}\n```')
                    except Exception as e:
                        code = [value[i:i + 1980] for i in range(0, len(value), 1980)]
                        for i in code:
                            msg = await ctx.send(f'```py\n{i}\n```')
            else:
                self._last_result = ret
                try:
                    code = [value[i:i + 1980] for i in range(0, len(value), 1980)]
                    for i in code:
                        msg = await ctx.send(f'```py\n{i}\n```')
                except Exception as e:
                    code = [value[i:i + 1980] for i in range(0, len(value), 1980)]
                    for i in code:
                        await ctx.send(f'```py\n{i}\n```')
                    modifyd_ret = [ret[i:i + 1980] for i in range(0, len(ret), 1980)]
                    for i in modifyd_ret:
                        msg = await ctx.send(f'```py\n{i}\n```')


def setup(bot):
    bot.add_cog(REPL(bot))