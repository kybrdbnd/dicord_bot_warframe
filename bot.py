from utilities.all_utilities import *


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )


@bot.event
async def on_message(message):
    # print(f'Message from {message.author}: {message.content}')

    if message.author == bot.user:
        return

    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    generalChannel = bot.get_channel(int(GENERAL_CHANNEL_ID))
    introductionChannel = bot.get_channel(int(INTRODUCTION_CHANNEL_ID))

    if member.bot is False:
        await generalChannel.send(f"Hunter {member.mention}, Welcome to Warframe India Community!!!!. "
                                  f"Make sure to go to <#{introductionChannel.id}> channel to introduce yourself")


bot.run(TOKEN)
