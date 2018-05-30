# Sebi-Machine
Dedicated Discord bot for [Sebi's bot tutorial](http://discord.gg/GWdhBSp).

## Important things to know

This bot extends the rewrite version of discord.py. A couple of variables have been added to give you easy access to a couple of objects listed here.

> `self.bot.ownerlist`

`self.ownerlist` can be used to retrieve a `list` of user ID's. (`int`). Those ID's belong to contributors.

> `self.bot.defaultprefix`

`self.defaultprefix` can be used to retrieve a `str` object of the default prefix. 

> `self.bot.version`

`self.version` can be used to retrieve a `float` which represent the version number of the bot.

> `self.bot.display_name`

`self.display_name` returns a `str` which represent the `display_name` of the bot.

> `self.bot.mainenance`

`self.maintenance` is equal to `True` or `False`. If you would like to exclude code in the master branch, use this.
Make sure this one is installed. Example:

```py
if self.bot.mainenance:
    print('I am in the development branch')

if not self.bot.mainenance:
    print('I am in the master branch')
```
In other words. `self.mainenance` returns `False` in production and `True` in developer modes.

> `self.bot.embed_color`

`self.embed_color` can be used to use the default color of out embed theme.

```python
discord.Embed(title='Foo', description='bar', color=self.bot.embed_color)
```

## Docker environment
This bot is heavly based on docker. This means it will run in a container. Other words. The code will run in a jail. Dont be afraid for bugs that cause harm. or commands that could potential restarts the server. It's safe. 

There are a couple of things to know about docker within this project.

1. Please read the docs of docker first before editing the docker files;
2. If you need a pip package, place the name into requirements.txt: docker handles the rest;
3. Everything in project folder is the workfolder of the docker container;
4. Initialize cogs by adding them into `cogs.txt`: one line is one cogfile.
                           
## Initialize a cog
Put your cog in `src/cogs` and edit the `cogs.txt` file. Add the filename of your cog into `cogs.txt`. No absolute path, just the name.

## Update source code
There is a git command available provided by Dusty. `S!git pull` should pull the latest commits into the docker container. Make sure afterwards to reload the cog.
If you are stuck in any way shape or form you can always contact anyone who works on this project. Dont forget to check `S!help`.

## Project links:
- http://discord.gg/GWdhBSp
- http://chillout.ueuo.com
- http://trello.com/b/x02goBbW/sebis-bot-tutorial-roadmap

## Deploy to heroku

For testing purposes you can click the link below to build your own copy of this repo you just pick an app name fill in the config variables then switch it on in resources tab.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Annihilator708/Sebi-Machine/tree/development)
