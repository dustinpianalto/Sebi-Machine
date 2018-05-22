# Sebi-Machine
Dedicated discord bot for Sebi's bot tutorial.

http://discord.gg/GWdhBSp

## Important things to know

This bot extends the rewrite version of discord.py. A couple of variables have been added to give you easy access to a couple of objects listed here.

> self.bot.ownerlist

self.ownerlist can be used to retrieve a `list` of user ID's. (`int`). Those ID's belong to contributors.
> self.bot.defaultprefix

self.defaultprefix can be used to retrieve a `str` object of the default prefix. 
> self.bot.version

self.version can be used to retrieve a `float` which represent the version number of the bot.
> self.bot.display_name

self.display_name returns a `str` which represent the display_name of the bot.
> self.bot.mainenance

self.maintenance is equal to `True` or `False`. If you would like to exclude code in the master branch, use this.
Make sure this one is installed.
example:
```py
if self.bot.mainenance:
    print('I am in the development branch')

if not self.bot.mainenance:
    print('I am in the master branch)
```
With other words. self.mainenance returns False in production and True in developer modus.

> self.bot.embed_color

self.embed_color can be used to use the default color of out embed theme.
```
discord.Embed(title='Foo', description='bar', color=self.bot.embed_color)
```
                           
## Initialize a cog
Cogs can be placed in `./src/cogs`. Overall the `src` folder is the place to put code in.
Make sure to update the `requirements.txt` and it is important to add the name of your cog file into the `cogs.txt` list. Otherwise it may turn out that your cog wont load.

## Update source code
There is a git command available provided by Dusty. `S!git pull` should pull the latest commits into the docker container. Make sure afterwards to reload the cog.
If you are stuck in any way shape or form you can always contact anyone who works on this project. Dont forget to check `S!help`.

## Trello
We do make use of Trello which can be found here: https://trello.com/b/x02goBbW/sebis-bot-tutorial-roadmap