import json
import os
from datetime import datetime
import discord
from pymongo import MongoClient
from discord.ext import commands
from util import filter_users, giveaway_winner
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')
GENERAL_CHANNEL_ID = os.getenv('GENERAL_CHANNEL_ID')
GIVEAWAY_CHANNEL_ID = os.getenv('GIVEAWAY_CHANNEL_ID')
USER_ID = os.getenv('USER_ID')

bot = commands.Bot(command_prefix='%')

conn = MongoClient('localhost:27017')
db = conn['warframe_india']
IGN_COLLECTION_NAME = 'IGN'


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )


@bot.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')

    if message.author == bot.user:
        return

    await bot.process_commands(message)


@bot.group()
async def giveaway(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid giveaway command passed...')


@giveaway.command()
async def start(ctx):
    channel = bot.get_channel(GIVEAWAY_CHANNEL_ID)
    if ctx.author.display_name == 'pucci':
        await channel.send('Giveaway! coming up when we cross 50 members!!!!!')
    else:
        await channel.send("You are not authorized to start giveaway!!!")


@giveaway.command()
async def price(ctx, giveaway_price: str):
    channel = bot.get_channel(GIVEAWAY_CHANNEL_ID)
    if ctx.author.display_name == 'pucci':
        with open("giveaway_price.txt", 'w+') as w:
            w.write(giveaway_price)
        await channel.send(f'Giveaway! Price is {giveaway_price}')
    else:
        await channel.send("You are not authorized to decide the price!!!")


@giveaway.command()
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


@bot.group()
async def ign(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid IGN command passed...')


@ign.command(name='save')
async def ign_save(ctx, ign_name: str):
    collection = db[IGN_COLLECTION_NAME]
    ignJSON = {
        'id': ctx.author.id,
        'ign': ign_name,
        'updatedOn': datetime.now()
    }
    collection.update_one({'id': ctx.author.id},
                          {'$set': ignJSON},
                          upsert=True)

    await ctx.send(f"name={ign}")


@ign.command(name='search')
async def ign_search(ctx, members: commands.Greedy[discord.Member], *, search='ign'):
    collection = db[IGN_COLLECTION_NAME]
    message = ''
    if len(members) > 0:
        for member in members:
            query = {
                'id': member.id
            }
            ignDoc = collection.find_one(query)
            if ignDoc is not None:
                message += f"{member.mention} IGN is {ignDoc['ign']} \n"
            else:
                message += f"{member.mention} IGN not found \n"
        await ctx.send(message)
    else:
        await ctx.send("Please enter atleast one user")


@ign.command(name='mine')
async def ign_mine(ctx):
    collection = db[IGN_COLLECTION_NAME]
    query = {
        'id': ctx.author.id
    }
    ignDoc = collection.find_one(query)
    if ignDoc is not None:
        await ctx.send(f"My IGN is {ignDoc['ign']}")
    else:
        await ctx.send(f"IGN not found")


@ign_save.error
async def info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Invalid IGN provided')


bot.run(TOKEN)
