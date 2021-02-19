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
    print("Bot is ready")


# Helper method
def embed_constructor(title, description, author, footer):
    embed = discord.Embed(title=title, description=description)
    embed.set_author(name=author, icon_url=author.avatar_url)
    embed.set_footer(text=footer)
    return embed


@client.command()
async def poll(ctx, duration="0:0:0", multiple="single", question="Question", *answers):
    # Poll attributes
    duration = list(map(int, duration.split(":")))
    multi = False
    if multiple == "multiple":
        multi = True
    emoji_answer = {}
    voters = []
    votes = {}
    total_votes = 0
    end_datetime = datetime.datetime.now() + datetime.timedelta(hours=duration[0], minutes=duration[1],
                                                                seconds=duration[2])
    description = "*Voting open until "
    options = ""

    # Construct poll answers
    for i, answer in enumerate(answers):
        options += emojiLetters[i] + "     " + answer + "\n"
        emoji_answer[emojiLetters[i]] = answer

    # Construct poll description
    description += "`" + end_datetime.strftime("%b %d, %Y, %I:%M %p") + "`*\n\n" + options

    # Construct votes dictionary
    for answer in answers:
        votes[answer] = []

    # Send poll message
    message = await ctx.send(embed=
                             embed_constructor(question, description, ctx.author, "# of voters: " + str(len(voters)) + "\n# of votes: " + str(total_votes)))

    # Display poll in console
    print(question + "\n" + description + "\n" + str(votes))

    for i, answer in enumerate(answers):
        await message.add_reaction(emojiLetters[i])

    # Ensure reaction is to the poll message and the reactor is not the bot
    def check(reaction, user):
        return reaction.message.id == message.id and user.id != 797601108268155001

    # Close the poll after a certain amount of time has elapsed
    start_time = datetime.datetime.now()
    while True:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=0.1, check=check)
            await message.remove_reaction(reaction, user)

            # Check if the user has already voted
            if multi:
                if user not in voters:
                    voters.append(user)
                if user not in votes[emoji_answer[reaction.emoji]]:
                    votes[emoji_answer[reaction.emoji]].append(user)
                    total_votes += 1
                    await message.edit(
                        embed=embed_constructor(question, description, ctx.author, "# of voters: " + str(len(voters)) + "\n# of votes: " + str(total_votes)))

            if user not in voters:
                voters.append(user)
                votes[emoji_answer[reaction.emoji]].append(user)
                total_votes += 1
                await message.edit(
                    embed=embed_constructor(question, description, ctx.author, "# of voters: " + str(len(voters)) + "\n# of votes: " + str(total_votes)))

            print(str(votes) + " Total votes: " + str(total_votes))

        except asyncio.TimeoutError:
            if datetime.datetime.now() > start_time + datetime.timedelta(hours=duration[0], minutes=duration[1], seconds=duration[2]):
                break

    await message.delete()
    print("Poll closed")

    # Send message of poll results
    results = ""
    for i, answer in enumerate(votes):
        results += emojiLetters[i] + "`" + str(len(votes[answer])) + "` | "

    description = "*Voting results*\n\n" + options + "\n" + results

    await ctx.send(embed=embed_constructor(question, description[:-2], ctx.author, "# of voters: " + str(len(voters)) + "\n# of votes: " + str(total_votes)))


client.run(my_token)
