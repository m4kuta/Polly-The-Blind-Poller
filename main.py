import asyncio
import datetime

import discord
from discord.ext import commands

from config import token

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

client = commands.Bot(command_prefix='/')


@client.event
async def on_ready():
    print("Bot is active")


@client.command()
async def poll(ctx, duration, question, *answers):
    emoji_answer_map = {}
    total_votes = 0
    voters = []
    vote_counts = {}
    end_datetime = datetime.datetime.now() + datetime.timedelta(minutes=int(duration))

    # Create poll message
    description = "This poll will be open until " + end_datetime.strftime("%B %d, %Y, %H:%M") + "\n\n"

    for i, answer in enumerate(answers):
        description += emojiLetters[i] + "     " + answer + "\n"
        emoji_answer_map[emojiLetters[i]] = answer

    print(emoji_answer_map)

    # Initialize vote_counts dictionary
    for answer in answers:
        vote_counts[answer] = 0
    print(vote_counts)
    my_poll = discord.Embed(
        title=question,
        description=description + "\n Total votes: " + str(total_votes)
    )
    creator = ctx.author
    message = await ctx.send(embed=my_poll)
    print("Poll opened")
    start_time = datetime.datetime.now()

    for i, answer in enumerate(answers):
        await message.add_reaction(emojiLetters[i])
    # TODO: Create poll object using PollManager

    # Get votes
    reaction = None

    # Ensure reaction is to the poll message and the reactor is not the bot
    def check(reaction, user):
        return reaction.message.id == message.id and user.id != 797601108268155001

    while True:  # Exit after a certain time
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=5.0, check=check)
            await message.remove_reaction(reaction, user)

            # Check if the user has already voted
            if user not in voters:
                voters.append(user)
                vote_counts[emoji_answer_map[reaction.emoji]] += 1
                print(vote_counts)

                total_votes += 1
                print("Total votes: " + str(total_votes))

                updated_poll = discord.Embed(
                    title=question,
                    description=description + "\n Total votes: " + str(total_votes)
                )
                await message.edit(embed=updated_poll)

        except asyncio.TimeoutError:
            if datetime.datetime.now() > start_time + datetime.timedelta(minutes=int(duration)):
                break

    # Send messages of results
    print("Poll closed")
    await message.clear_reactions()
    description = "This poll is closed\n\n"

    for i, answer in enumerate(answers):
        description += emojiLetters[i] + "     " + answer + "\n"
        emoji_answer_map[emojiLetters[i]] = answer

    updated_poll = discord.Embed(
        title=question,
        description=description + "\n Total votes: " + str(total_votes)
    )
    await message.edit(embed=updated_poll)

    results = ""
    for answer in vote_counts:
        results += answer + ": " + str(vote_counts[answer]) + "\n"
    results += "\n Total votes: " + str(total_votes)
    results_message = discord.Embed(
        title=question,
        description=results
    )
    await ctx.send(embed=results_message)


client.run(my_token)
