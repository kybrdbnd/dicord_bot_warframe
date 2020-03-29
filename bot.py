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


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(GENERAL_CHANNEL_ID))
    if member.bot is False:
        await channel.send(f"Hunter {member.mention}, Welcome to Warframe India Community!!!!. "
                           f"Make sure to #introduction channel to introduce yourself")


@bot.command(name='say')
async def say(ctx, *args):
    if len(args) > 0:
        await ctx.send(' '.join(args))
    else:
        await ctx.send("What do you wanna say!!!!")


bot.run(TOKEN)
