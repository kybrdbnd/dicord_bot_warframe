from dateutil import parser
from .util import *
import requests
import typing

relics_tiers = ['Axi', 'Lith', 'Neo', 'Meso', 'Requiem']
mission_type = ['Capture', 'Mobile Defense', 'Defense', 'Rescue', 'Sabotage', 'Exterminate', 'All', 'Survival',
                'Assault', 'Spy', 'Excavation']
DEFAULT_MISSION_TYPE = 'Capture'


@bot.group(name='wi', help='Warframe Helpers')
async def warframe(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid warframe command passed...')


@warframe.command(name='ws', help='Check World State Status')
async def get_world_state(ctx):
    request = requests.get('https://api.warframestat.us/pc')
    request.raise_for_status()
    response = request.json()
    await ctx.send(f"Hunter World state is {response['timestamp']}")


@warframe.command(name='cycle', help='Display status of cycles', usage='<cycle> cetus|vallis')
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


@warframe.command(name='fissures', help='Display fissures',
                  usage='<fissure> <mission>=all|exterminate|sabotage|rescue|capture|spy|assault|excavation|mobile defense')
async def fissures(ctx, *args):
    fissures_list = []
    mission_filter_fissures = []
    request = requests.get('https://api.warframestat.us/pc/fissures')
    response = request.json()
    request.raise_for_status()
    relics, missions = [], []
    if len(args) == 0:
        pass
    else:
        for argument in args:
            if argument.title() in relics_tiers:
                relics.append(argument)
            elif argument.title() in mission_type:
                missions.append(argument)
    if len(relics) == 0:
        fissures_list = response
    else:
        for relic in relics:
            fissures_list.extend(list(filter(lambda x: x['tier'] == relic.title(), response)))
    if len(missions) == 0:
        mission_filter_fissures.extend(list(filter(lambda x: x['missionType'] == DEFAULT_MISSION_TYPE, fissures_list)))
    else:
        mission = missions[0]
        if mission == 'all':
            mission_filter_fissures = fissures_list
        else:
            mission_filter_fissures.extend(list(filter(lambda x: x['missionType'] == mission.title(), fissures_list)))
    for fissure in mission_filter_fissures:
        embedCard = discord.Embed(title=f'{fissure["tier"]}')
        embedCard.add_field(name='Node', value=fissure['node'], inline=True)
        embedCard.add_field(name='Enemy', value=fissure['enemy'], inline=True)
        embedCard.add_field(name='ETA', value=fissure['eta'], inline=False)
        embedCard.add_field(name='Type', value=fissure['missionType'], inline=True)

        await ctx.send(embed=embedCard)
    if len(mission_filter_fissures) == 0:
        await ctx.send(f"No missions found")


@warframe.command(name='sortie', help="Display Sortie Status")
async def get_sortie(ctx):
    request = requests.get('https://api.warframestat.us/pc/sortie')
    request.raise_for_status()
    response = request.json()
    embedCard = discord.Embed(title=f"{response['boss']}, {response['faction']}")
    for i in range(len(response['variants'])):
        variant = response['variants'][i]
        variantValue = f"**Type:** {variant['missionType']}   \n    **Modifier:** {variant['modifier']} \n " \
                       f"**Description:** {variant['modifierDescription']} \n **Node:** {variant['node']}"
        embedCard.add_field(name=f'Mission {i + 1}', value=variantValue, inline=False)

    await ctx.send(embed=embedCard)


@warframe.command(name='voidtrader', help='Display voidtrader status')
async def get_voidtrader(ctx):
    request = requests.get('https://api.warframestat.us/pc/voidTrader')
    request.raise_for_status()
    response = request.json()
    if response['active']:
        description = f"**Leaving in:** {response['endString']}"
        embedCard = discord.Embed(title=f"{response['character']}, {response['location']}", description=description)
        for i in range(len(response['inventory'])):
            variant = response['inventory'][i]
            variantValue = f"**Item:** {variant['item']}   \n    **Ducats:** {variant['ducats']} \n " \
                           f"**Credits:** {variant['credits']}"
            embedCard.add_field(name=f'Item {i + 1}', value=variantValue, inline=True)
    else:
        dt = parser.parse(response['activation'])
        newDt = dt.astimezone(timeZone)
        description = f"**Coming on:** {newDt.strftime('%A, %d %B %H:%M')}"

        embedCard = discord.Embed(title=f"{response['character']}, {response['location']}", description=description)

    await ctx.send(embed=embedCard)


@cycle.error
async def cycle_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Cycle is missing, valid values are cetus|vallis')


@fissures.error
async def fissure_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('I apologize for the inconvenience tenno!!! for not been able to serve you')
