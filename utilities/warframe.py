from .util import *
import requests

relics_tiers = ['Axi', 'Lith', 'Neo', 'Meso', 'Requiem']
mission_type = ['Capture', 'Mobile Defense', 'Defense', 'Rescue', 'Sabotage', 'Exterminate']
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
                  usage='<fissure> mission[optional]=all|exterminate|sabotage|rescue|capture')
async def fissures(ctx, *args):
    fissures_list = []
    request = requests.get('https://api.warframestat.us/pc/fissures')
    response = request.json()
    request.raise_for_status()
    mission = None
    args = list(args)
    if len(args) == 0:
        fissures_list = response
    else:
        if len(args) >= 2:
            if args[-1].startswith('mission'):
                try:
                    mission = args[-1].split('=')[1]
                    args.pop()
                except Exception as err:
                    await ctx.send("Provide Mission Type")
        if len(args) == 1 and args[0].startswith('mission'):
            try:
                mission = args[-1].split('=')[1]
                args.pop()
                fissures_list = response
            except Exception as err:
                await ctx.send("Provide Mission Type")

        for relic in args:
            for fissure in response:
                if fissure['tier'] == relic.title():
                    fissures_list.append(fissure)
    if mission is None:
        mission = DEFAULT_MISSION_TYPE
    elif mission == 'all':
        mission = 'all'
    else:
        mission = mission.title()
    mission_filter_fissures = []

    if mission == 'all':
        mission_filter_fissures = fissures_list
    else:
        for fissure in fissures_list:
            if fissure['missionType'] == mission:
                mission_filter_fissures.append(fissure)

    for fissure in mission_filter_fissures:
        embedCard = discord.Embed(title=f'{fissure["tier"]}')
        embedCard.add_field(name='Node', value=fissure['node'], inline=True)
        embedCard.add_field(name='Enemy', value=fissure['enemy'], inline=True)
        embedCard.add_field(name='ETA', value=fissure['eta'], inline=False)
        embedCard.add_field(name='Type', value=fissure['missionType'], inline=True)

        await ctx.send(embed=embedCard)

    if len(mission_filter_fissures) == 0:
        await ctx.send(f"No {mission} missions found")


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
        embedCard = discord.Embed(title=f"{response['character']} ,{response['location']}", description=description)
        for i in range(len(response['inventory'])):
            variant = response['inventory'][i]
            variantValue = f"**Item:** {variant['item']}   \n    **Ducats:** {variant['ducats']} \n " \
                           f"**Credits:** {variant['credits']}"
            embedCard.add_field(name=f'Item {i + 1}', value=variantValue, inline=True)
    else:
        description = f"**Coming in:** {response['activation']}"

        embedCard = discord.Embed(title=f"{response['character']} ,{response['location']}", description=description)

    await ctx.send(embed=embedCard)


@cycle.error
async def cycle_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Cycle is missing, valid values are cetus|vallis')
