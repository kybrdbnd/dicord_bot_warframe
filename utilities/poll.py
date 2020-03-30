from .util import *

REACTIONS_LIST = ['🇦', '🇧', '🇨', '🇩', '🇪']


@bot.command(name='poll', help='Poll Commands')
async def poll(ctx, *args):
    if len(args) == 1:
        message = await ctx.send(' '.join(args))
        reactions = ['👍', '👎']
        for emoji in reactions:
            await message.add_reaction(emoji)
    elif len(args) == 2:
        await ctx.send("There has to be atleast two choices")
    elif len(args) <= 6:
        question = args[0]
        description = ''
        options = args[1:]
        for i in range(len(options)):
            description += f'{REACTIONS_LIST[i]} {options[i]} \n\n'
        embed = discord.Embed(title=question, description=description)
        message = await ctx.send(embed=embed)
        for i in range(len(options)):
            await message.add_reaction(REACTIONS_LIST[i])
    else:
        await ctx.send("Only 5 options supported now")
