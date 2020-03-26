import json
from datetime import datetime

from .util import *


@bot.group(help='Giveaway Commands')
async def giveaway(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid giveaway command passed...')


@giveaway.command(help='Start Giveaway')
async def start(ctx):
    channel = bot.get_channel(GIVEAWAY_CHANNEL_ID)
    if ctx.author.display_name == 'pucci':
        await channel.send('Giveaway! coming up when we cross 50 members!!!!!')
    else:
        await channel.send("You are not authorized to start giveaway!!!")


@giveaway.command(help='Giveaway Price', usage='<price>')
async def price(ctx, giveaway_price: str):
    channel = bot.get_channel(GIVEAWAY_CHANNEL_ID)
    if ctx.author.display_name == 'pucci':
        with open("giveaway_price.txt", 'w+') as w:
            w.write(giveaway_price)
        await channel.send(f'Giveaway! Price is {giveaway_price}')
    else:
        await channel.send("You are not authorized to decide the price!!!")


@giveaway.command(help='Decide Giveaway winner')
async def winner(ctx):
    dt = datetime.now().strftime("%Y-%m-%d")
    channel = bot.get_channel(GIVEAWAY_CHANNEL_ID)
    giveawayPrice = None
    if ctx.author.display_name == 'pucci':
        try:
            with open('giveaway_price.txt', 'r') as f:
                giveawayPrice = f.read()
        except Exception as err:
            await channel.send("Giveaway Price not decided")
        if giveawayPrice:
            users = filter_users(bot.get_all_members())
            giveawayWinner = giveaway_winner(users)
            with open(f"giveaways_prices/price_{dt}.json", 'w+') as f:
                f.write(json.dumps(
                    {
                        'price': giveawayPrice,
                        'winner': giveawayWinner.name
                    }
                ))
            os.remove("giveaway_price.txt")
            await channel.send(f"Congratulations {giveawayWinner.name} for winning {giveawayPrice}")
    else:
        await channel.send("You are not authorized to decide the winner!!!")
