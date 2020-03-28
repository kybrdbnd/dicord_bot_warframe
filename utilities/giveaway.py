from datetime import datetime

from .util import *

GIVEAWAY_COLLECTION_NAME = 'Giveaway'


def check_user(ctx):
    return ctx.message.author.id == int(USER_ID)  # only pucci can do it


@bot.group(help='Giveaway Commands')
async def giveaway(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid giveaway command passed...')


@giveaway.command(name='start', help='Start Giveaway')
@commands.check(check_user)
async def giveaway_start(ctx, condition: str):
    channel = bot.get_channel(int(GIVEAWAY_CHANNEL_ID))
    await channel.send(condition)


@giveaway.command(name='price', help='Giveaway Price', usage='<price>')
@commands.check(check_user)
async def price(ctx, giveaway_price: str):
    channel = bot.get_channel(int(GIVEAWAY_CHANNEL_ID))

    collection = db[GIVEAWAY_COLLECTION_NAME]
    priceJSON = {
        'price': giveaway_price,
        'startAt': datetime.now().strftime("%Y-%m-%d"),
        'createdOn': datetime.now()
    }
    collection.insert_one(priceJSON)

    await channel.send(f'Giveaway! Price is {giveaway_price}')


@giveaway.command(name='winner', help='Decide Giveaway winner')
@commands.check(check_user)
async def giveaway_winner(ctx):
    dt = datetime.now().strftime("%Y-%m-%d")
    channel = bot.get_channel(int(GIVEAWAY_CHANNEL_ID))
    collection = db[GIVEAWAY_COLLECTION_NAME]

    giveawayDocs = list(collection.find({}).sort('createdOn', -1))
    if len(giveawayDocs) > 0:
        lastGiveawayDoc = giveawayDocs[0]
        if 'winner' in lastGiveawayDoc:
            await ctx.send("Create a new giveaway, winner already decided for last giveaway")
        else:
            users = filter_users(bot.get_all_members())
            giveawayWinner = get_giveaway_winner(users)

            collection.update_one({'_id': lastGiveawayDoc['_id']},
                                  {'$set': {'winner': giveawayWinner.name,
                                            'updatedOn': dt}}, upsert=True)

            await channel.send(f"Congratulations {giveawayWinner.mention} for winning {lastGiveawayDoc['price']}")
    else:
        await ctx.send("No giveaways found!!!")


@giveaway_start.error
async def giveaway_start_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Provide the condition')
