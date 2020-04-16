import random
import discord
from discord.ext import commands
from .utils import quotes


class Fun(commands.Cog):

    def __init(self, bot):
        self.bot = bot

    @commands.command(name='roast', help='roast your team members')
    async def roast(self, ctx, members: commands.Greedy[discord.Member]):
        if len(members) > 0:
            q = quotes.roast_quotes
            message = random.choice(q)
            await ctx.send(message)
        else:
            await ctx.send("Mention your friends")

    @commands.command(name='say', help='say to a specific channel', hidden=True)
    async def say(self, ctx, channels: commands.Greedy[discord.TextChannel], *, args):
        if len(channels) == 0:
            await ctx.send("Enter valid channels")
        else:
            for channel in channels:
                if len(args) > 0:
                    await channel.send(args)
                else:
                    await ctx.send("What do you wanna say!!!!")

    @commands.command(name='quotes', help='cephalon simaris quotes')
    async def quotes(self, ctx):
        q = quotes.simaris_quotes
        message = random.choice(q)
        await ctx.send(message)


def setup(bot):
    bot.add_cog(Fun(bot))
