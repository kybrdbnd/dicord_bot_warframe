from utilities.all_utilities import *
from utilities.constants import *


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
    generalChannel = bot.get_channel(int(GENERAL_CHANNEL_ID))
    introductionChannel = bot.get_channel(int(INTRODUCTION_CHANNEL_ID))

    if member.bot is False:
        await generalChannel.send(f"Hunter {member.mention}, Welcome to Warframe India Community!!!!. "
                                  f"Make sure to go to <#{introductionChannel.id}> channel to introduce yourself")


@bot.command(name='say')
async def say(ctx, *args):
    if len(args) > 0:
        await ctx.send(' '.join(args))
    else:
        await ctx.send("What do you wanna say!!!!")


@bot.command(name='quotes')
async def quotes(ctx):
    simaris_quotes = cephalon_simaris_quotes
    message = random.choice(simaris_quotes)
    await ctx.send(message)


@bot.command(name='capture')
async def capture(ctx, members: commands.Greedy[discord.Member], *, sample='capture'):
    author = ctx.author
    message = ''
    if len(members) > 0:
        random_numbers = random.randint(1, len(members))
        success_members = random.sample(members, random_numbers)
        for member in success_members:
            message += f"{member.mention}"
        await ctx.send(f"{author.mention} you have synthesized {message}")
    else:
        await ctx.send("Hunter select targets to synthesize")


bot.run(TOKEN)
