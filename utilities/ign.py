from datetime import datetime
from .util import *

IGN_COLLECTION_NAME = 'ign'


@bot.group(help='IGN Commands')
async def ign(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid IGN command passed...')


@ign.command(name='save', help='Saves your IGN', usage='<YOUR_IGN>')
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

    await ctx.send(f"Hunter your name has been updated to {ign_name}")


@ign.command(name='search', help='Search for a user IGN', usage='<@user>')
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
                message += f"Hunter {member.mention} IGN is {ignDoc['ign']} \n"
            else:
                message += f"Hunter {member.mention} IGN not found \n"
        await ctx.send(message)
    else:
        await ctx.send("Please enter atleast one user")


@ign.command(name='mine', help='display your IGN')
async def ign_mine(ctx):
    collection = db[IGN_COLLECTION_NAME]
    query = {
        'id': ctx.author.id
    }
    ignDoc = collection.find_one(query)
    if ignDoc is not None:
        await ctx.send(f"Hunter your IGN is {ignDoc['ign']}")
    else:
        await ctx.send(f"IGN not found")


@ign_save.error
async def info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Invalid IGN provided')
