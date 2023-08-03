import os
import sys

import discord
from discord.ext import commands

import game

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
        await bot.load_extension("cogs.basic")

        ### Player commands ###
        await bot.load_extension("cogs.player")

        ### Role commands ###
        await bot.load_extension("cogs.role")

        ### Game commands ###
        await bot.load_extension("cogs.game")

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

    @bot.command()
    @commands.is_owner()  # This decorator ensures only the bot owner can use the command
    async def reload(ctx, cog_name: str):
        try:
            await bot.reload_extension(f'cogs.{cog_name}')
            await ctx.send(f"Cog '{cog_name}' reloaded successfully.")
        except commands.ExtensionError as e:
            await ctx.send(f"Failed to reload cog: {e}")

    @bot.command()
    @commands.is_owner()  # This decorator ensures only the bot owner can use the command
    async def quit(ctx):
        sys.exit("Bot was shutdown from discord.")

    
        
    bot.run(TOKEN)