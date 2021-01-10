import discord
import datetime
from discord.ext import commands
from config import token
from PollManager import PollManager
import asyncio
my_token = token
emojiLetters = [
            "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER E}", 
            "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"]

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
	print("Bot is ready.")


@client.command()
async def poll(ctx, question, *args):
	voters = []
	vote_counts = {}
	
	# Create poll
	options = []
	react_to_option = {}
	description = ""
	for i, arg in enumerate(args):
		description += emojiLetters[i] + " " + arg + "\n"
		options.append(arg)
		react_to_option[emojiLetters[i]] = arg
	print(react_to_option)
	# Initialize vote_counts dictionary
	for option in options:
		vote_counts[option] = 0
	print(vote_counts)
	my_poll = discord.Embed(
		title = question,
		description = description
		)
	creator = ctx.author
	message = await ctx.send(embed = my_poll)
	start_time = datetime.datetime.now()

	for i, option in enumerate(options):
		await message.add_reaction(emojiLetters[i])
	# TODO: Create poll object using PollManager

	# Get votes
	reaction = None
	# Ensure reaction is to the poll message and the reactor is not the bot
	def check(reaction, user):
		return reaction.message.id == message.id and user.id != 797601108268155001 

	while True: # Exit after a certain time
		try:
			reaction, user = await client.wait_for('reaction_add', timeout = 5.0, check = check)
			await message.remove_reaction(reaction, user)
			# Check if the user has already voted
			if user not in voters:
				voters.append(user)
				vote_counts[react_to_option[reaction.emoji]] += 1
				print(vote_counts)
		except asyncio.TimeoutError:
			if datetime.datetime.now() > start_time + datetime.timedelta(seconds = 15):
				break		
		
	# Send messages of results 
	print("done")
	results = ""
	for option in vote_counts:
		results += option + ": " + str(vote_counts[option]) + "\n"
	results_message = discord.Embed(
		title = question,
		description = results
		)
	await message.clear_reactions()
	await ctx.send(embed = results_message)

client.run(my_token)