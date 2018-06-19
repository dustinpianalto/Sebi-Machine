import asyncio
import inspect
import traceback
import weakref
from typing import Dict

import async_timeout
import dataclasses
import discord
from discord.ext import commands
import youtube_dl

# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyPackageRequirements
from utils import noblock


YT_DL_OPTS = {
	"format": 'mp3[abr>0]/bestaudio/best',
	"ignoreerrors": True,
	"default_search": "auto",
	"source_address": "0.0.0.0",
	'quiet': True
}


# Let it be waiting on an empty queue for about 30 minutes
# before closing the connection from being idle.
IDLE_FOR = 60 * 30


@dataclasses.dataclass(repr=True)
class Request:
	"""Track request."""
	who: discord.Member
	what: str         # Referral
	title: str        # Video title
	actual_url: str   # Actual URL to play

	def __str__(self):
		return self.title

	def __hash__(self):
		return hash(str(self.who.id) + self.what)


# noinspection PyBroadException
class Session:
	"""
	Each player being run is a session; (E.g. if you open a player in one server and I did in another).
	Sessions will have a queue, an event that can fire to stop the current track and move on, and a voice
	channel to bind to. This is defined as the voice channel the owner of the session was in when they made the channel.
	To create a session, call ``Session.new_session``. Do not call the constructor directly.
	Attributes:
		ctx: discord.ext.commands.Context
			The context of the original command invocation we are creating a session for.
		loop: asyncio.AbstractEventLoop
			The event loop to run this in.
		voice_client: discord.VoiceClient
			Voice client we are streaming audio through.
		queue: asyncio.Queue
			Track queue.
	"""
	@classmethod
	async def new_session(cls, ctx: commands.Context):
		"""
		Helper to make a new session. Invoke constructor using this, as it handles any errors. It also ensures
		we connect immediately.
		"""
		try:
			s = cls(ctx)
			await s.connect()
		except Exception as ex:
			traceback.print_exc()
			await ctx.send(f"I couldn't connect! Reason: {str(ex) or type(ex).__qualname__}")
			return None
		else:
			return s

	def __init__(self, ctx: commands.Context) -> None:
		"""Create a new session."""
		if ctx.author.voice is None:
			raise RuntimeError('Please enter a voice channel I have access to first.')

		# Holds the tasks currently running associated with this.
		self.voice_channel = ctx.author.voice.channel
		self.ctx: commands.Context = ctx
		self.voice_client: discord.VoiceClient = None
		self.loop: asyncio.AbstractEventLoop = weakref.proxy(self.ctx.bot.loop)
		self.queue = asyncio.Queue()

		# Lock-based event to allow firing a handler to advance to the next track.
		self._start_next_track_event = asyncio.Event()
		self._on_stop_event = asyncio.Event()
		self._player: asyncio.Task = None
		self._track: asyncio.Task = None

	@property
	def is_connected(self) -> bool:
		return self.voice_client and self.voice_client.is_connected()

	async def connect(self) -> None:
		"""Connects to the VC."""
		if not self.is_connected and not self._player:
			# noinspection PyUnresolvedReferences
			self.voice_client = await self.voice_channel.connect()
			self._start_next_track_event.clear()
			self._player = self.__spawn_player()
		else:
			raise RuntimeError('I already have a voice client/player running.')

	async def disconnect(self) -> None:
		"""Disconnects from the VC."""
		await self.voice_client.disconnect()
		self.voice_client = None

	def __spawn_player(self) -> asyncio.Task:
		"""Starts a new player."""
		async def player():
			try:
				while True:
					# Wait on an empty queue for a finite period of time.
					with async_timeout.timeout(IDLE_FOR):
						request = await self.queue.get()

					await self.ctx.send(f'Playing `{request}` requested by {request.who}')

					# Clear the skip event if it is set.
					self._start_next_track_event.clear()

					# Start the player if it was a valid request, else continue to the next track.
					if not self.__play(request.actual_url):
						await self.ctx.send(f'{request.referral} was a bad request and was skipped.')
						continue

					await self._start_next_track_event.wait()

					if self.voice_client.is_playing():
						self.voice_client.stop()

			except asyncio.CancelledError:
				# Hit when someone kills the player using stop().
				print('Requested to stop player', repr(self))
			except asyncio.TimeoutError:
				await self.ctx.send('Was idle for too long...')
				print('Player queue was empty for too long and was stopped', repr(self))
			except Exception:
				traceback.print_exc()
			finally:
				if self.voice_client.is_playing():
					await self.voice_client.stop()
				if self.is_connected:
					await self.disconnect()
		return self.loop.create_task(player())

	def __play(self, url):
		"""Tries to play the given URL. If it fails, we return False, else we return True."""
		try:
			ffmpeg_player = discord.FFmpegPCMAudio(url)

			# Play the stream. After we finish, either from being cancelled or otherwise, fire the
			# skip track event to start the next track.
			self.voice_client.play(ffmpeg_player, after=lambda error: self._start_next_track_event.set())
		except Exception:
			traceback.print_exc()
			return False
		else:
			return True

	def skip(self):
		"""Request to skip track."""
		self._start_next_track_event.set()

	def stop(self):
		"""Request to stop playing."""
		if self._player:
			self._player.cancel()
		self._on_stop_event.set()
		self._on_stop_event.clear()

	def on_exit(self, func):
		"""Decorates a function to invoke it on exit."""
		async def callback():
			await self._on_stop_event.wait()
			inspect.iscoroutinefunction(func) and await func() or func()
		self.loop.create_task(callback())
		return func


# noinspection PyBroadException
class PlayerCog:
	def __init__(self):
		self.sessions: Dict[discord.Guild, Session] = {}

	# noinspection PyMethodMayBeStatic
	async def __local_check(self, ctx):
		return ctx.guild

	@commands.command()
	async def join(self, ctx):
		if ctx.guild not in self.sessions:
			p = await Session.new_session(ctx)
			if p:
				self.sessions[ctx.guild] = p

				@p.on_exit
				def when_terminated():
					try:
						self.sessions.pop(ctx.guild)
					finally:
						return

				await ctx.send("*hacker voice*\n**I'm in.**", delete_after=15)
		else:
			await ctx.send(f'I am already playing in {self.sessions[ctx.guild].voice_channel.mention}')

	# noinspection PyNestedDecorators
	@staticmethod
	@noblock.no_block
	def _get_video_meta(referral):
		downloader = youtube_dl.YoutubeDL(YT_DL_OPTS)
		info = downloader.extract_info(referral, download=False)
		return info

	@commands.command()
	async def queue(self, ctx):
		if ctx.guild not in self.sessions:
			return await ctx.send('Please join me into a voice channel first.')

		sesh = self.sessions[ctx.guild]
		if sesh.queue.empty():
			return await ctx.send(
				'There is nothing in the queue at the moment!\n\n'
				'Add something by running `<>play https://url` or `<>play search term`!')

		# We cannot faff around with the actual queue so make a shallow copy of the internal
		# non-async dequeue.
		# noinspection PyProtectedMember
		agenda = sesh.queue._queue.copy()

		message = ['**Queue**']

		for i, item in enumerate(list(agenda)[:15]):
			message.append(f'`{i+1: >2}: {item.title} ({item.who})`')

		if len(agenda) >= 15:
			message.append('')
			message.append(f'There are {len(agenda)} items in the queue currently.')

		await ctx.send('\n'.join(message)[:2000])

	@commands.command()
	async def play(self, ctx, *, referral):
		if ctx.guild not in self.sessions:
			return await ctx.send('Please join me into a voice channel first.')

		try:
			try:
				info = await self._get_video_meta(referral)

				# If it was interpreted as a search, it appears this happens?
				# The documentation is so nice.
				if info.get('_type') == 'playlist':
					info = info['entries'][0]

				# ...wait... did I say nice? I meant "non existent."

				url = info['url']
				title = info.get('title') or referral
			except IndexError:
				return await ctx.send('No results...', delete_after=15)
			except Exception as ex:
				return await ctx.send(f"Couldn't add this to the queue... reason: {ex!s}")

			await self.sessions[ctx.guild].queue.put(Request(ctx.author, referral, title, url))
			await ctx.send(f'Okay. Queued `{title or referral}`.')
		except KeyError:
			await ctx.send('I am not playing in this server.')

	@commands.command()
	async def stop(self, ctx):
		try:
			await self.sessions[ctx.guild].stop()
		except KeyError:
			await ctx.send('I am not playing in this server.')
		except TypeError:
			await ctx.send("I wasn't playing anything, but okay.", delete_after=15)

	@commands.command()
	async def skip(self, ctx):
		try:
			self.sessions[ctx.guild].skip()
			try:
				await ctx.message.add_reaction('\N{OK HAND SIGN}')
			except discord.Forbidden:
				await ctx.send('\N{OK HAND SIGN}')
		except KeyError:
			await ctx.send('I am not playing in this server.')
			
	@commands.command()
	async def disconnect(self, ctx):
		await self.sessions[ctx.guild].stop()
		await self.disconnect()


def setup(bot):
	bot.add_cog(PlayerCog())
