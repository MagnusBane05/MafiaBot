import os

import discord
from discord.ext import commands

import game
from cogs import *

def runDiscordBot():
    TOKEN = os.environ.get('MafiaDiscordBotToken')
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    bot = commands.Bot(command_prefix='!',intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')

        ### Basic commands for players ###
        await bot.add_cog(Basic(bot))

        ### Player commands ###
        await bot.add_cog(Player(bot))

        ### Role commands ###
        await bot.add_cog(Role(bot))

        ### Game commands ###
        await bot.add_cog(Game(bot))

        ### Load game ###
        await game.loadRoles()
    
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            print(error)
            await ctx.send('Could not find that command. Type !help for a list of commands.')
        
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            print(error)
            await ctx.send('You are missing an argument for that command. Type !help <command> for more info.')
        
        elif isinstance(error, commands.errors.CommandInvokeError):
            print(error)
            await ctx.send('An error occured while processing that command.')
    
        
    bot.run(TOKEN)