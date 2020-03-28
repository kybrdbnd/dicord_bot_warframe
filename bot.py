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
    print(f'Message from {message.author}: {message.content}')

    if message.author == bot.user:
        return

    await bot.process_commands(message)


@bot.command(name='say')
async def say(ctx):
    channel = bot.get_channel(int(GENERAL_CHANNEL_ID))
    await channel.send("HUNTER THE SANCTUARY CAN GO WITHOUT YOU !!!!!")


bot.run(TOKEN)
