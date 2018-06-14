import discord
from discord.ext import commands


class BotManager:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='claim', alaises=['makemine', 'gimme'])
    async def _claim_bot(self, ctx, bot: discord.Member=None, prefix: str=None):
        if not bot:
            raise RuntimeError('You must include the name of the bot you are trying to claim... Be exact.')
        if not prefix:
            if bot.display_name.startswith('['):
                prefix = bot.display_name.split(']')[0].strip('[')
            else:
                raise RuntimeError('Prefix not provided and can\'t be found in bot name.')
        if not bot.bot:
            raise RuntimeError('You can only claim bots.')

        em = discord.Embed()

        existing = await self.bot.db_con.fetchrow('select * from bots where id = $1', bot.id)
        if not existing:
            await self.bot.db_con.execute('insert into bots (id, owner, prefix) values ($1, $2, $3)',
                                          bot.id, ctx.author.id, prefix)
            em.colour = self.bot.embed_color
            em.title = 'Bot Claimed'
            em.description = f'You have claimed {bot.display_name} with a prefix of {prefix}\n' \
                             f'If there is an error please run command again to correct the prefix,\n' \
                             f'or {ctx.prefix}unclaim {bot.mention} to unclaim the bot.'
        elif existing['owner'] and existing['owner'] != ctx.author.id:
            em.colour = self.bot.error_color
            em.title = 'Bot Already Claimed'
            em.description = 'This bot has already been claimed by someone else.\n' \
                             'If this is actually your bot please let the guild Administrators know.'
        elif existing['owner'] and existing['owner'] == ctx.author.id:
            em.colour = self.bot.embed_color
            em.title = 'Bot Already Claimed'
            em.description = 'You have already claimed this bot.\n' \
                             'If the prefix you provided is different from what is already in the database' \
                             ' it will be updated for you.'
            if existing['prefix'] != prefix:
                await self.bot.db_con.execute("update bots set prefix = $1 where id = $2", prefix, bot.id)
        elif not existing['owner']:
            await self.bot.db_con.execute('update bots set owner = $1, prefix = $2 where id = $3',
                                          ctx.author.id, prefix, bot.id)
            em.colour = self.bot.embed_color
            em.title = 'Bot Claimed'
            em.description = f'You have claimed {bot.display_name} with a prefix of {prefix}\n' \
                             f'If there is an error please run command again to correct the prefix,\n' \
                             f'or {ctx.prefix}unclaim {bot.mention} to unclaim the bot.'
        else:
            em.colour = self.bot.error_color
            em.title = 'Something Went Wrong...'
        await ctx.send(embed=em)

    @commands.command(name='unclaim')
    async def _unclaim_bot(self, ctx, bot: discord.Member=None):
        if not bot:
            raise RuntimeError('You must include the name of the bot you are trying to claim... Be exact.')
        if not bot.bot:
            raise RuntimeError('You can only unclaim bots.')

        em = discord.Embed()

        existing = await self.bot.db_con.fetchrow('select * from bots where id = $1', bot.id)
        if not existing or not existing['owner']:
            em.colour = self.bot.error_color
            em.title = 'Bot Not Found'
            em.description = 'That bot is not claimed'
        elif existing['owner'] != ctx.author.id:
            em.colour = self.bot.error_color
            em.title = 'Not Not Claimed By You'
            em.description = 'That bot is claimed by someone else.\n' \
                             'You can\'t unclaim someone else\'s bot'
        else:
            await self.bot.db_con.execute('update bots set owner = null where id = $1', bot.id)
            em.colour = self.bot.embed_color
            em.title = 'Bot Unclaimed'
            em.description = f'You have unclaimed {bot.display_name}\n' \
                             f'If this is an error please reclaim using\n' \
                             f'{ctx.prefix}claim {bot.mention} {existing["prefix"]}'
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(BotManager(bot))