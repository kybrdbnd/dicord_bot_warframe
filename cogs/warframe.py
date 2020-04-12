from dateutil import parser
from cogs.utils.constants import *
import requests
import discord
from discord.ext import commands


class Warframe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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

    @warframe.command(name='search', help='search for any item', usage='<item name>')
    async def search(self, ctx, item: str):
        request = requests.get(f'https://api.warframestat.us/items/search/{item}')
        request.raise_for_status()
        response = request.json()
        if len(response) > 0:
            result = response[0]
            if result['type'] == 'Rifle':
                rifle = self.bot.get_cog('Rifle')
                embedCard = await rifle.display(result)
                await ctx.send(embed=embedCard)
            elif result['type'] == 'Relic':
                relic = self.bot.get_cog('Relic')
                embedCard = await relic.display(result)
                await ctx.send(embed=embedCard)
            elif result['type'] == 'Arcane':
                arcane = self.bot.get_cog('Arcane')
                embedCard = await arcane.display(result)
                await ctx.send(embed=embedCard)
            elif result['type'] == 'Warframe':
                warframe = self.bot.get_cog('Frame')
                embedCard = await warframe.display(result)
                await ctx.send(embed=embedCard)
            elif result['type'] == 'Melee':
                melee = self.bot.get_cog('Melee')
                embedCard = await melee.display(result)
                await ctx.send(embed=embedCard)

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
    def get_build_requirements(components):
        buildRequirementsValue = " "
        for component in components:
            buildRequirementsValue += f"**{component['name']}:** {component['itemCount']}\n"
        return buildRequirementsValue

    @staticmethod
    def get_drop_locations(components):
        dropLocations = []
        for component in components:
            if 'drops' in component:
                dropLocations.extend(list(map(lambda x: ' '.join(x['location'].split(' ')[:-1]), component['drops'])))
        return sorted(set(dropLocations))

    @staticmethod
    def get_weapon_damage(damageTypes):
        weaponDamageValue = " "
        for damageType, damageValue in damageTypes.items():
            weaponDamageValue += f"**{damageType.title()}**: {damageValue} \n"
        return weaponDamageValue

    async def display(self, result):
        embedCard = discord.Embed(title=f"{result['name']}", description=f"{result['description']}",
                                  url=result['wikiaUrl'])
        embedCard.set_thumbnail(url=result['wikiaThumbnail'])
        components = self.filter_components(result['components'])
        dropLocations = self.get_drop_locations(components)
        embedCard.add_field(name="Mastery Rank", value=result['masteryReq'], inline=True)
        embedCard.add_field(name="Build Price", value=result['buildPrice'], inline=True)
        embedCard.add_field(name="Build Time", value=f"{result['buildTime'] // 60 // 60} hrs", inline=True)
        embedCard.add_field(name="Riven Deposition", value=result['disposition'], inline=True)
        embedCard.add_field(name=f"Damage", value=self.get_weapon_damage(result['damageTypes']), inline=False)
        embedCard.add_field(name=f"Build Requirements", value=self.get_build_requirements(result['components']),
                            inline=False)
        embedCard.add_field(name=f"Drop Locations", value=', '.join(dropLocations), inline=False)
        return embedCard


class Melee(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.componentsName = ['Argon Crystal', 'Auroxium Alloy', 'Blueprint', 'Hespazym Alloy', 'Kuva', '']

    @staticmethod
    def get_weapon_damage(damageTypes):
        weaponDamageValue = " "
        for damageType, damageValue in damageTypes.items():
            weaponDamageValue += f"**{damageType.title()}**: {damageValue} \n"
        return weaponDamageValue

    @staticmethod
    def get_build_requirements(components):
        buildRequirementsValue = " "
        for component in components:
            buildRequirementsValue += f"**{component['name']}:** {component['itemCount']}\n"
        return buildRequirementsValue

    async def display(self, result):
        embedCard = discord.Embed(title=f"{result['name']}", description=f"{result['description']}",
                                  url=result['wikiaUrl'])
        embedCard.set_thumbnail(url=result['wikiaThumbnail'])
        embedCard.add_field(name="Mastery Rank", value=result['masteryReq'], inline=True)
        embedCard.add_field(name="Build Price", value=result['buildPrice'], inline=True)
        embedCard.add_field(name="Build Time", value=f"{result['buildTime'] // 60 // 60} hrs", inline=True)
        embedCard.add_field(name="Riven Deposition", value=result['disposition'], inline=True)
        embedCard.add_field(name=f"Damage", value=self.get_weapon_damage(result['damageTypes']), inline=False)
        embedCard.add_field(name=f"Build Requirements", value=self.get_build_requirements(result['components']),
                            inline=False)

        return embedCard


class Relic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def display(result):
        embedCard = discord.Embed(title=f"{result['name']}", description=f"{result['description']}")
        for dropLocation in result['drops'][:30]:
            dropLocationValue = f"**Type:** {dropLocation['type']}   \n    **Rarity:** {dropLocation['rarity']} \n " \
                                f"**Chance:** {dropLocation['chance']}"
            if 'rotation' in dropLocation:
                dropLocationValue += f"\n **Rotation:** {dropLocation['rotation']}"
            embedCard.add_field(name=f"{dropLocation['location']}", value=dropLocationValue, inline=True)
        return embedCard


class Arcane(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_stats(levelStats):
        statsValues = " "
        i = 0
        for stat in levelStats:
            statsValues += f"**Level {i + 1}**: {stat['stats'][0]}\n"
            i += 1
        return statsValues

    async def display(self, result):
        embedCard = discord.Embed(title=f"{result['name']}")
        embedCard.add_field(name="Rarity", value=result['rarity'], inline=False)
        statsValue = self.get_stats(result['levelStats'])
        embedCard.add_field(name="Stats", value=statsValue, inline=True)
        return embedCard


class Frame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.componentsName = ['Chassis', 'Blueprint', 'Neuroptics', 'Systems']

    def filter_components(self, components):
        return list(filter(lambda x: x['name'] in self.componentsName, components))

    @staticmethod
    def get_drop_locations(components):
        dropLocations = []
        for component in components:
            if 'drops' in component:
                dropLocations.extend(list(map(lambda x: ' '.join(x['location'].split(' ')[:-1]), component['drops'])))
        return sorted(set(dropLocations))

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

    async def display(self, result):
        embedCard = discord.Embed(title=f"{result['name']}", description=f"{result['description']}",
                                  url=result['wikiaUrl'])
        embedCard.set_thumbnail(url=result['wikiaThumbnail'])
        components = self.filter_components(result['components'])
        dropLocations = self.get_drop_locations(components)
        embedCard.add_field(name="Passive Ability", value=result['passiveDescription'], inline=False)
        embedCard.add_field(name="Attributes", value=self.get_frame_attributes(result), inline=False)
        embedCard.add_field(name="Mastery Rank", value=result['masteryReq'], inline=True)
        embedCard.add_field(name="Build Price", value=result['buildPrice'], inline=True)
        embedCard.add_field(name="Build Time", value=f"{result['buildTime'] // 60 // 60} hrs", inline=True)
        embedCard.add_field(name="Abilities", value=self.get_abilities(result['abilities']), inline=False)
        for component in components:
            componentValue = f"**SellingPrice:** {component['primeSellingPrice']} \n " \
                             f"**ItemCount:** {component['itemCount']}"
            embedCard.add_field(name=f"{component['name']}", value=componentValue, inline=True)
        embedCard.add_field(name=f"Drop Locations", value=', '.join(dropLocations), inline=False)
        return embedCard


def setup(bot):
    bot.add_cog(Warframe(bot))
    bot.add_cog(Rifle(bot))
    bot.add_cog(Melee(bot))
    bot.add_cog(Relic(bot))
    bot.add_cog(Arcane(bot))
    bot.add_cog(Frame(bot))
