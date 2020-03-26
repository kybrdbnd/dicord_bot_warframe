import random


def filter_users(users):
    return list(filter(lambda x: x.bot is False, users))


def giveaway_winner(users: object) -> object:
    return random.choice(users)
