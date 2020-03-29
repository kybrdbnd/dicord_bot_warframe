import os
import random
from discord.ext import commands
import discord
from pymongo import MongoClient

TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')
GENERAL_CHANNEL_ID = os.getenv('GENERAL_CHANNEL_ID')
GIVEAWAY_CHANNEL_ID = os.getenv('GIVEAWAY_CHANNEL_ID')
USER_ID = os.getenv('USER_ID')
MONGO_URL = os.getenv('MONGO_URL')
game = discord.Game("%help")

bot = commands.Bot(command_prefix='%', description='Assistance Provider', activity=game)

conn = MongoClient(MONGO_URL)
db = conn['warframe_india']


def filter_users(users):
    return list(filter(lambda x: x.bot is False, users))


def get_giveaway_winner(members: commands.Greedy[discord.Member]):
    return random.choice(members)
