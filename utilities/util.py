import os
import random
from discord.ext import commands
import discord
from pymongo import MongoClient
from utilities.dialogues import simaris_quotes, roast_quotes

TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')
GENERAL_CHANNEL_ID = os.getenv('GENERAL_CHANNEL_ID')
GIVEAWAY_CHANNEL_ID = os.getenv('GIVEAWAY_CHANNEL_ID')
USER_ID = os.getenv('USER_ID')
MONGO_URL = os.getenv('MONGO_URL')
INTRODUCTION_CHANNEL_ID = os.getenv('INTRODUCTION_CHANNEL_ID')

game = discord.Game("%help")

bot = commands.Bot(command_prefix='%', description='Assistance Provider', activity=game)

conn = MongoClient(MONGO_URL)
db = conn['warframe_india']


def filter_users(users):
    return list(filter(lambda x: x.bot is False, users))


def get_giveaway_winner(members: commands.Greedy[discord.Member]):
    return random.choice(members)


@bot.command(name='quotes', help='cephalon simaris quotes')
async def quotes(ctx):
    q = simaris_quotes.quotes
    message = random.choice(q)
    await ctx.send(message)


@bot.command(name='roast', help='roast your team members')
async def roast(ctx, members: commands.Greedy[discord.Member]):
    if len(members) > 0:
        q = roast_quotes.quotes
        message = random.choice(q)
        await ctx.send(message)
    else:
        await ctx.send("Mention your friends")


@bot.command(name='say', help='say to a specific channel', hidden=True)
async def say(ctx, channels: commands.Greedy[discord.TextChannel], *, args):
    if len(channels) == 0:
        await ctx.send("Enter valid channels")
    else:
        for channel in channels:
            if len(args) > 0:
                await channel.send(args)
            else:
                await ctx.send("What do you wanna say!!!!")

# @bot.command(name='capture')
# async def capture(ctx, members: commands.Greedy[discord.Member], *, sample='capture'):
#     author = ctx.author
#     message = ''
#     if len(members) > 0:
#         random_numbers = random.randint(1, len(members))
#         success_members = random.sample(members, random_numbers)
#         for member in success_members:
#             message += f"{member.mention}"
#         await ctx.send(f"{author.mention} you have synthesized {message}")
#     else:
#         await ctx.send("Hunter select targets to synthesize")
