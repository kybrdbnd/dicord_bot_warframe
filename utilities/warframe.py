from .util import *
import requests

relics_tiers = ['Axi', 'Lith', 'Neo', 'Meso', 'Requiem']


# def test(ctx):
#     return ctx.message.author.id == 592912657833787394
# @commands.check(test)

@bot.group(name='wi', help='Warframe Helpers')
async def warframe(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid warframe command passed...')


@warframe.command(name='ws')
async def get_world_state(ctx):
    request = requests.get('https://api.warframestat.us/pc')
    request.raise_for_status()
    response = request.json()
    await ctx.send(f"Hunter your name has been updated to {response['timestamp']}")


@warframe.command(name='cycle', help='Display status of cycles, cetus|vallis', usage='<cycle>')
async def cycle(ctx, place: str):
    if place == 'cetus':
        request = requests.get('https://api.warframestat.us/pc/cetusCycle')
    elif place == 'vallis':
        request = requests.get('https://api.warframestat.us/pc/vallisCycle')
    else:
        await ctx.send(f"Invalid cycle entered, valid values are cetus|vallis")
    request.raise_for_status()
    response = request.json()
    embedCard = discord.Embed(title=f'{place.title()} Cycle')
    embedCard.add_field(name='Cycle', value=response['state'].title(), inline=True)
    embedCard.add_field(name='timeleft', value=response['timeLeft'], inline=True)
    embedCard.add_field(name='Next Cycle', value=response['shortString'], inline=False)

    await ctx.send(embed=embedCard)


@warframe.command(name='fissures', help='Display fissures', usage='<fissure>')
async def fissures(ctx, *args):
    fissures_list = []
    request = requests.get('https://api.warframestat.us/pc/fissures')
    response = request.json()
    request.raise_for_status()
    if len(args) == 0:
        fissures_list = response
    else:
        for relic in args:
            for fissure in response:
                if fissure['tier'] == relic.title():
                    fissures_list.append(fissure)

    for fissure in fissures_list:
        embedCard = discord.Embed(title=f'{fissure["tier"]}')
        embedCard.add_field(name='Node', value=fissure['node'], inline=True)
        embedCard.add_field(name='Enemy', value=fissure['enemy'], inline=True)
        embedCard.add_field(name='ETA', value=fissure['eta'], inline=False)
        embedCard.add_field(name='Type', value=fissure['missionType'], inline=True)

        await ctx.send(embed=embedCard)


@get_world_state.error
async def world_state_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You are not authorized!!')


@cycle.error
async def cycle_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Cycle is missing, valid values are cetus|vallis')
