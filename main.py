import discord
from discord.ext import commands
from config import token
from PollManager import PollManager
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
	activePoll = True
	
	# Create poll
	options = []
	description = ""
	for i, arg in enumerate(args):
		description += emojiLetters[i] + " " + arg + "\n"
		options.append(arg)

	my_poll = discord.Embed(
		title = question,
		description = description
		)
	message = await ctx.send(embed = my_poll)
	print(ctx.author)
	creator = ctx.author
	await creator.send(embed = my_poll)

	for i, option in enumerate(options):
		await message.add_reaction(emojiLetters[i])
	# TODO: Create poll object using PollManager

	# Get votes
	reaction = None
	# Ensure reaction is to the poll message and the reactor is not the bot
	def check(reaction, user):
		return reaction.message.id == message.id and user.id != 797601108268155001 

	while activePoll:
		reaction, user = await client.wait_for('reaction_add', check = check)
		await message.remove_reaction(reaction, user)
		# Check if the user has already voted
		if user not in voters:
			voters.append(user)
			user_name = user.display_name
			await creator.send(user_name + " voted for " + str(reaction))

	print("done")


client.run(my_token)