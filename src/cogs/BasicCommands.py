#!/usr/bin/python
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

class BasicCommands:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def start(self, ctx):
		await ctx.send(f"Hello, {ctx.author.display_name}. Welcome to Sebi's Bot Tutorials. \nFirst off, would you like a quick walkthrough on the server channels?")
		
		channel_list = {'channel-1'             : self.bot.get_channel(333149949883842561).mention, 
		                'd.py-rewrite-start'    : self.bot.get_channel(386419285439938560).mention, 
		                'js-klasa-start'        : self.bot.get_channel(341816240186064897).mention, 
		                'd.js'                  : self.bot.get_channel(436771798303113217).mention} 

		bots_channels = (self.bot.get_channel(339112602867204097).mention, 
                         self.bot.get_channel(411586546551095296).mention)

		help_channels = (self.bot.get_channel(425315253153300488).mention, 
                         self.bot.get_channel(392215236612194305).mention, 
                         self.bot.get_channel(351034776985141250).mention)			

		def check(m):
			return True if m.author.id == ctx.author.id and m.channel.id == ctx.channel.id else False
		
		msg = await self.bot.wait_for('message', check = check, timeout = 15)

		agree = ("yes", "yep", "yesn't", "ya")

		if msg is None:
			await ctx.send("Sorry, {ctx.author.mention}, you didn't reply on time. You can run the command again when you're free :)")
		else:
			if msg.content.lower() in agree:
				async with ctx.typing():
					await ctx.send("Alrighty-Roo...")
					await ctx.send(f"""To start making your bot from scratch, you first need to head over to {channel_list['channel-1']} 
						               (Regardless of the language you're gonna use).""")
					await ctx.send(f"""After you have a bot account, you can either continue with {channel_list['d.py-rewrite-start']} 
						               if you want to make a bot in discord.py rewrite __or__ go to {channel_list['js-klasa-start']} or 
						               {channel_list['d.js']} for making a bot in JavaScript""")
					await ctx.send("...Read all the tutorials and still need help? You have two ways to get help.")
					await ctx.send(f"""**Method-1**\nThis is the best method of getting help. You help yourself.\n
						               To do so, head over to a bots dedicated channel (either {bots_channels[0]} or {bots_channels[1]}) 
						               and type `?rtfm rewrite thing_you_want_help_with`.\nThis will trigger the bot R.Danny Bot and will 
						               give you links on your query on the official discord.py rewrite docs. *PS: Let the page completely load*""")
					await ctx.send(f"""**Method-2**\nIf you haven't found anything useful with Method-1, feel free to ask your question 
						               in any of the related help channels. ({', '.join(help_channels)})\nMay the force be with you!!""")						
			else:
				return await ctx.send("Session terminated. You can run this command again whenever you want.")

def setup(bot):
	bot.add_cog(BasicCommands(bot))