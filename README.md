# Discord BOT (Warframe India) 
Custom discord bot for Warframe India Community

### Build Status:

![Deploy to Amazon ECS](https://github.com/kybrdbnd/discord_bot_warframe/workflows/Deploy%20to%20Amazon%20ECS/badge.svg)

### Pre-requisites:

1. MongoDB
2. Python >= 3.6
3. Docker

**Note: Make sure you are running linux containers on windows**

### Follow the steps to get the bot working:

1. Create the bot in discord application dashboard.
2. Invite the bot onto your server. (It will be offline, don't worry)
3. Make sure that mongoDB is running on your system.
4. Create a file .env, I have included example.env to help you.
5. Final step
```docker-compose up```
4. You will see the bot is now online and is ready to serve you.
5. Use ```%help``` to view the commands that bot has. 

### Functionalities:

Following functionalities are currently there:
1. **Giveaway** -> Decide the price to give in giveaway, and let the bot choose the winner.

2. **IGN** -> IGN stands for In-Game Name, save the member's game name, so that other members
can search for them, instead of asking again and again

3. **Warframe Status** -> Added support for warframe game status, like fissures info,
void trader info, more coming up soon

4. **Poll** -> Simple Poll support

Don't forget to join our discord server -> https://discord.gg/FQKc6q6

Find me on discord -> pucci#4435

<iframe src="https://discordapp.com/widget?id=501295892536492046&theme=dark" width="350" height="500" allowtransparency="true" frameborder="0"></iframe>
