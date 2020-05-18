import random
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from cogs.utils.constants import *


def filter_users(users):
    return list(filter(lambda x: x.bot is False, users))


def check_user(ctx):
    return ctx.message.author.id == int(USER_ID)  # only pucci can do it


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(help='Giveaway Commands')
    async def giveaway(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid giveaway command passed...')

    @giveaway.command(name='start', help='Start Giveaway', hidden=True)
    @commands.check(check_user)
    async def giveaway_start(self, ctx, price: str):
        collection = db[GIVEAWAY_COLLECTION_NAME]
        giveawayDocs = list(collection.find({}).sort('createdOn', -1))
        newGiveaway = False
        if len(giveawayDocs) == 0:
            newGiveaway = True
        elif len(giveawayDocs) > 0:
            giveawayDoc = giveawayDocs[0]
            if 'winner' in giveawayDoc:
                newGiveaway = True
            else:
                await ctx.send(f"winner still to be decided for giveaway -> {giveawayDoc['price']}")
        if newGiveaway:
            giveawayJSON = {
                'startAt': datetime.now().strftime("%Y-%m-%d"),
                'price': price,
                'updatedOn': datetime.now(),
                'createdOn': datetime.now(),
                'onGoing': True
            }
            collection.insert(giveawayJSON)
        giveawayAnnouncementDate = datetime.now() + timedelta(days=6)
        giveawayChannel = self.bot.get_channel(int(GIVEAWAY_CHANNEL_ID))
        await giveawayChannel.send(
            f"Let's get excited with a giveaway! React to this post for a chance to win {price}. "
            f"Winner will be picked on {giveawayAnnouncementDate.strftime('%B %e')} at 6 PM IST")
        await ctx.send("Giveaway started successfully!!!")

    @giveaway.command(name='winner', help='Decide Giveaway winner', hidden=True)
    @commands.check(check_user)
    async def giveaway_winner(self, ctx):
        channel = self.bot.get_channel(int(GIVEAWAY_CHANNEL_ID))
        collection = db[GIVEAWAY_COLLECTION_NAME]

        giveawayDocs = list(collection.find({}).sort('createdOn', -1))
        if len(giveawayDocs) > 0:
            lastGiveawayDoc = giveawayDocs[0]
            if 'winner' in lastGiveawayDoc:
                await ctx.send("Create a new giveaway, winner already decided for last giveaway")
            else:
                giveaway_message = await channel.history(limit=2).flatten()
                giveaway_message = giveaway_message[1]
                totalReactions = giveaway_message.reactions
                usersReacted = []
                for reaction in totalReactions:
                    usersReacted.extend(await reaction.users().flatten())
                userIds = list(map(lambda x: x.id, usersReacted))
                uniqueUserIds = list(set(userIds))
                winnerId = random.choice(uniqueUserIds)
                giveawayWinner = self.bot.get_user(winnerId)
                collection.update({'_id': lastGiveawayDoc['_id']},
                                  {'$set': {'winner': giveawayWinner.name,
                                            'winner_id': giveawayWinner.id,
                                            'onGoing': False,
                                            'updatedOn': datetime.now()}}, upsert=True)

                await channel.send(f"Congratulations {giveawayWinner.mention} for winning {lastGiveawayDoc['price']}."
                                   f" ***Please ensure you have DMs from server members enabled!***")
        else:
            await ctx.send("No giveaways found!!!")

    @giveaway.command(name='current', help='Current giveaway info')
    async def giveaway_current(self, ctx):
        collection = db[GIVEAWAY_COLLECTION_NAME]
        giveawayPrice = "No price decided yet"
        winner = "No winner decided yet"
        giveawayDocs = list(collection.find({'onGoing': True}).sort('createdOn', -1))
        if len(giveawayDocs) > 0:
            lastGiveawayDoc = giveawayDocs[0]
            embedCard = discord.Embed(title="Giveaway!!!")
            if 'price' in lastGiveawayDoc:
                giveawayPrice = lastGiveawayDoc['price']
            if 'winner' in lastGiveawayDoc:
                winner = self.bot.get_user(lastGiveawayDoc['winner_id']).name
            embedCard.add_field(name='Winner', value=winner, inline=True)
            embedCard.add_field(name='Price', value=giveawayPrice, inline=True)
            await ctx.send(embed=embedCard)
        else:
            await ctx.send("No giveaways found!!!")

    @giveaway.command(name='last_winner', help='Get last giveaway winner info')
    async def giveaway_last_winner(self, ctx):
        collection = db[GIVEAWAY_COLLECTION_NAME]
        giveawayDocs = list(collection.find({}).sort('createdOn', -1))
        lastGiveawayDoc = None
        if len(giveawayDocs) > 0:
            for doc in giveawayDocs:
                if 'winner' in doc:
                    lastGiveawayDoc = doc
                    break
            if lastGiveawayDoc is not None:
                embedCard = discord.Embed(title="Giveaway!!!")
                giveawayPrice = lastGiveawayDoc['price']
                winner = self.bot.get_user(lastGiveawayDoc['winner_id']).name
                embedCard.add_field(name='Winner', value=winner, inline=True)
                embedCard.add_field(name='Price', value=giveawayPrice, inline=True)
                await ctx.send(embed=embedCard)
            else:
                await ctx.send("No winner has been decided yet in any giveaway")
        else:
            await ctx.send("No giveaways found!!!")

    @giveaway_start.error
    async def giveaway_start_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Provide the price')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('You are not authorized')


def setup(bot):
    bot.add_cog(Giveaway(bot))
