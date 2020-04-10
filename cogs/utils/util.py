import random
from discord.ext import commands
import discord


def filter_users(users):
    return list(filter(lambda x: x.bot is False, users))


def get_giveaway_winner(members: commands.Greedy[discord.Member]):
    return random.choice(members)
