import discord
from discord.ext import commands
from cogs.utils.constants import *

COGS = ["cogs.poll", "cogs.fun", "cogs.ign", "cogs.giveaway", "cogs.warframe"]


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(self)

        game = discord.Game("%help")
        self.command_prefix = '%'
        self.description = 'Assistance Provider'
        self.activity = game

        for cog in COGS:
            self.load_extension(cog)

    async def on_ready(self):
        print('Connected!')
        print('Bot: {0.name}\nID: {0.id}'.format(self.user))

    async def on_message(self, message):

        if message.author.bot:
            return

        await self.process_commands(message)

    async def on_member_join(self, member):
        generalChannel = self.get_channel(int(GENERAL_CHANNEL_ID))
        introductionChannel = self.get_channel(int(INTRODUCTION_CHANNEL_ID))

        if member.bot is False:
            await generalChannel.send(f"Hunter {member.mention}, Welcome to Warframe Lovers Community!!!!. "
                                      f"Make sure to go to <#{introductionChannel.id}> channel to introduce yourself")


bot = Bot()

bot.run(TOKEN)
