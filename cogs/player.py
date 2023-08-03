import discord
from discord.ext import commands

import responses

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(help='Commands for handling the players in the game.')
    async def players(self, ctx):
        pass

    @players.command(help='Usage: "!join <player>". Join another player to the game.')
    @commands.has_role("Moderator")
    async def join(self, ctx, *args: discord.Member):
        if len(args) == 0:
            await ctx.send('No member provided. Usage: "!players join [player1] [player2]..."')
        for member in args:
            name = member.name
            response = responses.playerJoins(name)
            await ctx.send(response)

    @join.error
    async def join_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('At least one player entered is not a member of this channel.')

    @players.command(help='Lists the players in the game.')
    async def list(self, ctx):
        response = responses.getPlayerList()
        await ctx.send(response)

    @players.command(help='Leaves the game. Use "!players leave [player1] [player2]..." to have other players leave the game.')
    @commands.has_role("Moderator")
    async def leave(self, ctx, *args: discord.Member):
        if len(args) == 0:
            await ctx.send('No member provided. Usage: "!players leave [player1] [player2]..."')
        else:
            for name in args:
                response = responses.playerLeaves(name)
                await ctx.send(response)

    @leave.error
    async def leave_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('At least one player entered is not a member of this channel.')

    @players.command(help="Removes all players from the game.")
    @commands.has_role("Moderator")
    async def clear(self, ctx):
        response = responses.clearPlayerList()
        await ctx.send(response)

async def setup(bot):
    await bot.add_cog(Player(bot))