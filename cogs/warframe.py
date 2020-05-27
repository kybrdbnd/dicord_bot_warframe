import json
from datetime import datetime

import requests
import discord
from discord.ext import commands
from cogs.utils.constants import *
from cogs.utils.warframe import *
from dateutil import parser


class Warframe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.stupidItems = ['Glyph', 'Ship Decoration']

    @commands.group(name='wi', help='Warframe Helpers')
    async def warframe(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid warframe command passed...')

    @warframe.command(name='ws', help='Check World State Status')
    async def get_world_state(self, ctx):
        request = requests.get('https://api.warframestat.us/pc')
        request.raise_for_status()
        response = request.json()
        await ctx.send(f"Hunter World state is {response['timestamp']}")

    @warframe.command(name='cycle', help='Display status of cycles', usage='<cycle> cetus|vallis')
    async def cycle(self, ctx, place: str):
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

    @warframe.command(name='farm', help='Display preferred place to farm for resources',
                      usage='<resource name> plastids|oxium|neurodes|neural sensor|hexenon|polymer bundle|argon crystal|gallium|orokin cell')
    async def farm_resources(self, ctx, item: str):
        currentDirectory = os.path.dirname(os.path.abspath(__file__))
        itemDirectory = os.path.join(currentDirectory, "utils", "warframe_items", "farm.json")
        with open(itemDirectory, 'r') as f:
            items_farm_json = json.load(f)
        if item in items_farm_json:
            itemJson = items_farm_json[item]
            embedCard = discord.Embed(title=f'{item.title()}')
            embedCard.add_field(name='Best Location', value=itemJson['BestLocationName'], inline=False)
            if len(itemJson['OtherLocations']) > 0:
                embedCard.add_field(name='Other Locations', value=', '.join(itemJson['OtherLocations']), inline=False)
            await ctx.send(embed=embedCard)
        else:
            await ctx.send("We are adding the resource that you requested")

    @warframe.command(name='fissures', help='Display fissures',
                      usage='<fissure> <mission>=all|exterminate|sabotage|rescue|capture|spy|assault|excavation|mobile defense')
    async def fissures(self, ctx, *args):
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
            mission_filter_fissures.extend(
                list(filter(lambda x: x['missionType'] == DEFAULT_MISSION_TYPE, fissures_list)))
        else:
            mission = missions[0]
            if mission == 'all':
                mission_filter_fissures = fissures_list
            else:
                mission_filter_fissures.extend(
                    list(filter(lambda x: x['missionType'] == mission.title(), fissures_list)))
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
    async def get_sortie(self, ctx):
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
    async def get_voidtrader(self, ctx):
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

    @warframe.command(name='arbi', help='Display Arbitration status')
    async def get_arbitration(self, ctx):
        request = requests.get('https://api.warframestat.us/pc/arbitration')
        request.raise_for_status()
        response = request.json()
        embedCard = discord.Embed(title="Arbitration")
        embedCard.add_field(name="Enemy", value=response['enemy'], inline=True)
        embedCard.add_field(name="Type", value=response['type'], inline=True)
        embedCard.add_field(name="Node", value=response['node'], inline=False)
        currentTime = datetime.now().astimezone(timeZone)
        arbiTime = parser.parse(response['expiry']).astimezone(timeZone)
        timediff = (arbiTime - currentTime).seconds
        embedCard.add_field(name="TimeLeft", value=f"{timediff // 60} mins", inline=False)

        await ctx.send(embed=embedCard)

    def remove_stupid_items(self, result):
        return list(filter(lambda x: x['type'] not in self.stupidItems, result))

    @warframe.command(name='search', help='search for any item', usage='<item name>')
    async def search(self, ctx, item: str):
        request = requests.get(f'https://api.warframestat.us/items/search/{item}')
        isPrime = False
        if 'prime' in item:
            isPrime = True
        request.raise_for_status()
        response = request.json()
        if len(response) > 0:
            response = self.remove_stupid_items(response)
            result = response[0]
            if result['category'] == 'Primary':
                if result['type'] == 'Bow':
                    bow = self.bot.get_cog('Bow')
                    embedCard = await bow.display(result, isPrime)
                    await ctx.send(embed=embedCard)
                else:
                    rifle = self.bot.get_cog('Rifle')
                    embedCard = await rifle.display(result, isPrime)
                    await ctx.send(embed=embedCard)
            elif result['category'] == 'Relics':
                relic = self.bot.get_cog('Relic')
                embedCard = await relic.display(result)
                await ctx.send(embed=embedCard)
            elif result['category'] == 'Arcanes':
                arcane = self.bot.get_cog('Arcane')
                embedCard = await arcane.display(result)
                await ctx.send(embed=embedCard)
            elif result['category'] == 'Warframes':
                warframe = self.bot.get_cog('Frame')
                embedCard = await warframe.display(result, isPrime)
                await ctx.send(embed=embedCard)
            elif result['category'] == 'Melee':
                melee = self.bot.get_cog('Melee')
                embedCard = await melee.display(result, isPrime)
                await ctx.send(embed=embedCard)
            elif result['category'] == 'Sentinels':
                sentinel = self.bot.get_cog('Sentinel')
                embedCard = await sentinel.display(result, isPrime)
                await ctx.send(embed=embedCard)
            elif result['category'] == 'Mods':
                mods = self.bot.get_cog('Mods')
                embedCard = await mods.display(result)
                await ctx.send(embed=embedCard)

            else:
                await ctx.send("Give it time, I will display your result")

        else:
            await ctx.send(f"No results found for the item {item}")

    @search.error
    async def cycle_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please provide item to be searched for')

    @cycle.error
    async def cycle_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Cycle is missing, valid values are cetus|vallis')

    @farm_resources.error
    async def farm_resources_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Resource name missing')

    @fissures.error
    async def fissure_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('I apologize for the inconvenience tenno!!! for not been able to serve you')


class Rifle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.componentsName = ['Barrel', 'Blueprint', 'Receiver', 'Stock']

    def filter_components(self, components):
        return list(filter(lambda x: x['name'] in self.componentsName, components))

    @staticmethod
    def get_weapon_damage(damageTypes):
        weaponDamageValue = " "
        for damageType, damageValue in damageTypes.items():
            weaponDamageValue += f"**{damageType.title()}**: {damageValue} \n"
        return weaponDamageValue

    async def display(self, result, isPrime):
        embedCard = discord.Embed(title=f"{result['name']}", description=f"{result['description']}",
                                  url=result['wikiaUrl'])
        embedCard.set_thumbnail(url=result['wikiaThumbnail'])
        embedCard.add_field(name="Mastery Rank", value=result['masteryReq'], inline=True)
        embedCard.add_field(name="Build Price", value=result['buildPrice'], inline=True)
        embedCard.add_field(name="Build Time", value=f"{result['buildTime'] // 60 // 60} hrs", inline=True)
        embedCard.add_field(name="Riven Deposition", value=result['disposition'], inline=True)
        embedCard.add_field(name=f"Damage", value=self.get_weapon_damage(result['damageTypes']), inline=False)
        embedCard.add_field(name=f"Build Requirements", value=get_build_requirements(result['components']),
                            inline=False)
        if isPrime:
            components = self.filter_components(result['components'])
            dropLocations = get_relics_drop_locations(components)
            embedCard.add_field(name=f"Drop Locations", value=', '.join(dropLocations), inline=False)
        return embedCard


class Melee(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.componentsName = ['Barrel', 'Blueprint', 'Receiver', 'Stock', 'Chain', 'Handle']

    def filter_components(self, components):
        return list(filter(lambda x: x['name'] in self.componentsName, components))

    @staticmethod
    def get_weapon_damage(damageTypes):
        weaponDamageValue = " "
        for damageType, damageValue in damageTypes.items():
            weaponDamageValue += f"**{damageType.title()}**: {damageValue} \n"
        return weaponDamageValue

    async def display(self, result, isPrime):
        embedCard = discord.Embed(title=f"{result['name']}", description=f"{result['description']}",
                                  url=result['wikiaUrl'])
        embedCard.set_thumbnail(url=result['wikiaThumbnail'])
        embedCard.add_field(name="Mastery Rank", value=result['masteryReq'], inline=True)
        embedCard.add_field(name="Build Price", value=result['buildPrice'], inline=True)
        embedCard.add_field(name="Build Time", value=f"{result['buildTime'] // 60 // 60} hrs", inline=True)
        embedCard.add_field(name="Riven Deposition", value=result['disposition'], inline=True)
        embedCard.add_field(name=f"Damage", value=self.get_weapon_damage(result['damageTypes']), inline=False)
        embedCard.add_field(name=f"Build Requirements", value=get_build_requirements(result['components']),
                            inline=False)
        if isPrime:
            components = self.filter_components(result['components'])
            dropLocations = get_relics_drop_locations(components)
            embedCard.add_field(name=f"Drop Locations", value=', '.join(dropLocations), inline=False)

        return embedCard


class Relic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def display(result):
        embedCard = discord.Embed(title=f"{result['name']}", description=f"{result['description']}")
        if 'drops' in result:
            for dropLocation in result['drops'][:30]:
                dropLocationValue = f"**Type:** {dropLocation['type']}   \n    **Rarity:** {dropLocation['rarity']} \n " \
                                    f"**Chance:** {dropLocation['chance']}"
                if 'rotation' in dropLocation:
                    dropLocationValue += f"\n **Rotation:** {dropLocation['rotation']}"
                embedCard.add_field(name=f"{dropLocation['location']}", value=dropLocationValue, inline=True)
        else:
            embedCard.add_field(name="Vaulted", value="True", inline=True)
        return embedCard


class Arcane(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def display(result):
        embedCard = discord.Embed(title=f"{result['name']}")
        if 'rarity' in result:
            embedCard.add_field(name="Rarity", value=result['rarity'], inline=False)
        statsValue = get_stats(result['levelStats'])
        embedCard.add_field(name="Stats", value=statsValue, inline=True)
        if 'drops' in result:
            embedCard.add_field(name=f"Drop Locations", value=get_drop_locations(result['drops']), inline=False)
        return embedCard


class Frame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.componentsName = ['Chassis', 'Blueprint', 'Neuroptics', 'Systems']

    def filter_components(self, components):
        return list(filter(lambda x: x['name'] in self.componentsName, components))

    @staticmethod
    def get_abilities(abilities):
        abilityValues = " "
        for ability in abilities:
            abilityValues += f"**{ability['name']}**: {ability['description']}\n\n"
        return abilityValues

    @staticmethod
    def get_frame_attributes(result):
        frameAttributesValues = ""
        frameAttributesValues += f"**Health**: {result['health']}\n"
        frameAttributesValues += f"**Shield**: {result['shield']}\n"
        frameAttributesValues += f"**Armor**: {result['armor']}\n"
        frameAttributesValues += f"**Stamina**: {result['stamina']}\n"
        frameAttributesValues += f"**Sprint Speed**: {result['sprintSpeed']}\n"

        return frameAttributesValues

    async def display(self, result, isPrime):
        embedCard = discord.Embed(title=f"{result['name']}", description=f"{result['description']}",
                                  url=result['wikiaUrl'])
        embedCard.set_thumbnail(url=result['wikiaThumbnail'])
        embedCard.add_field(name="Passive Ability", value=result['passiveDescription'], inline=False)
        embedCard.add_field(name="Attributes", value=self.get_frame_attributes(result), inline=False)
        embedCard.add_field(name="Mastery Rank", value=result['masteryReq'], inline=True)
        embedCard.add_field(name="Abilities", value=self.get_abilities(result['abilities']), inline=False)
        if 'components' in result:
            embedCard.add_field(name="Build Price", value=result['buildPrice'], inline=True)
            embedCard.add_field(name="Build Time", value=f"{result['buildTime'] // 60 // 60} hrs", inline=True)
            embedCard.add_field(name=f"Build Requirements", value=get_build_requirements(result['components']),
                                inline=False)
        if isPrime and 'components' in result:
            components = self.filter_components(result['components'])
            dropLocations = get_relics_drop_locations(components)
            embedCard.add_field(name=f"Drop Locations", value=', '.join(dropLocations), inline=False)
        return embedCard


class Sentinel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.componentsName = ['Blueprint', 'Carapace', 'Cerebrum', 'Systems']

    def filter_components(self, components):
        return list(filter(lambda x: x['name'] in self.componentsName, components))

    @staticmethod
    def get_frame_attributes(result):
        frameAttributesValues = ""
        frameAttributesValues += f"**Health**: {result['health']}\n"
        frameAttributesValues += f"**Shield**: {result['shield']}\n"
        frameAttributesValues += f"**Armor**: {result['armor']}\n"
        frameAttributesValues += f"**Stamina**: {result['stamina']}\n"
        frameAttributesValues += f"**Power**: {result['power']}\n"

        return frameAttributesValues

    async def display(self, result, isPrime):
        embedCard = discord.Embed(title=f"{result['name']}", description=f"{result['description']}")
        if 'masteryReq' in result:
            embedCard.add_field(name="Mastery Rank", value=result['masteryReq'], inline=True)
        embedCard.add_field(name="Build Price", value=result['buildPrice'], inline=True)
        embedCard.add_field(name="Build Time", value=f"{result['buildTime'] // 60 // 60} hrs", inline=True)
        embedCard.add_field(name="Attributes", value=self.get_frame_attributes(result), inline=False)
        embedCard.add_field(name=f"Build Requirements", value=get_build_requirements(result['components']),
                            inline=False)
        if isPrime:
            components = self.filter_components(result['components'])
            dropLocations = get_relics_drop_locations(components)
            embedCard.add_field(name=f"Drop Locations", value=', '.join(dropLocations), inline=False)
        return embedCard


class Bow(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.componentsName = ['Blueprint', 'Grip', 'Lower Limb', 'String', 'Upper Limb']

    @staticmethod
    def get_weapon_damage(damageTypes):
        weaponDamageValue = " "
        for damageType, damageValue in damageTypes.items():
            weaponDamageValue += f"**{damageType.title()}**: {damageValue} \n"
        return weaponDamageValue

    def filter_components(self, components):
        return list(filter(lambda x: x['name'] in self.componentsName, components))

    async def display(self, result, isPrime):
        embedCard = discord.Embed(title=f"{result['name']}", description=f"{result['description']}",
                                  url=result['wikiaUrl'])
        embedCard.set_thumbnail(url=result['wikiaThumbnail'])
        embedCard.add_field(name="Mastery Rank", value=result['masteryReq'], inline=True)
        if 'buildPrice' in result:
            embedCard.add_field(name="Build Price", value=result['buildPrice'], inline=True)
        if 'buildTime' in result:
            embedCard.add_field(name="Build Time", value=f"{result['buildTime'] // 60 // 60} hrs", inline=True)
        embedCard.add_field(name="Riven Deposition", value=result['disposition'], inline=True)
        embedCard.add_field(name=f"Damage", value=self.get_weapon_damage(result['damageTypes']), inline=False)
        if 'components' in result:
            embedCard.add_field(name=f"Build Requirements", value=get_build_requirements(result['components']),
                                inline=False)
        if isPrime and 'components' in result:
            components = self.filter_components(result['components'])
            dropLocations = get_relics_drop_locations(components)
            embedCard.add_field(name=f"Drop Locations", value=', '.join(dropLocations), inline=False)
        return embedCard


class Mods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def display(result):
        description = 'Description Not available'
        if 'description' in result:
            description = result['description']
        embedCard = discord.Embed(title=f"{result['name']}", description=f"{description}")
        if 'drops' in result:
            dropValues = get_drop_locations(result['drops'])
            embedCard.add_field(name="Drop Locations", value=dropValues, inline=False)
        if 'levelStats' in result:
            statsValue = get_stats(result['levelStats'])
            embedCard.add_field(name="Stats", value=statsValue, inline=True)
        return embedCard


def setup(bot):
    bot.add_cog(Warframe(bot))
    bot.add_cog(Rifle(bot))
    bot.add_cog(Melee(bot))
    bot.add_cog(Relic(bot))
    bot.add_cog(Arcane(bot))
    bot.add_cog(Frame(bot))
    bot.add_cog(Sentinel(bot))
    bot.add_cog(Bow(bot))
    bot.add_cog(Mods(bot))
