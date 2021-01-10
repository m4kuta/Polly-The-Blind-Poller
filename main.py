import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
	print("Bot is ready.")

@client.command()
async def poll(ctx, question, *args):
	# Create poll
	description = ""
	for arg in args:
		description += arg + "\n"
	my_poll = discord.Embed(
		title = question,
		description = description

		)

	message = await ctx.send(embed = my_poll)
	
	# Get votes

	# Clear reactions after vote
	await message.clear_reactions()
	#await message.add_reaction('A')
    #await message.add_reaction('B')
    #await message.add_reaction('C')
    #await message.add_reaction('D')
    #try:
    #    reaction, user = await client.wait_for('reaction_add', timeout = 30.0, check = check)
    #    await message.remove_reaction(reaction, user)
    #except:
    #    break

client.run('Nzk3NjAxMTA4MjY4MTU1MDAx.X_o16g.R6c2FInOFSYoR-gClmb69wKjW4Q')
