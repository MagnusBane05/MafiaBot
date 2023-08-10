from discord.ext import commands

import responses


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='Joins the game.')
    async def join(self, ctx):
        response = responses.playerJoins(ctx.author.name)
        await ctx.send(response)        

    @commands.command(help='Leaves the game.')
    async def leave(self, ctx):
        response = responses.playerLeaves(ctx.author.name)
        await ctx.send(response)

    @commands.command(help='Privately messages you your role.')
    async def myrole(self, ctx):
        response = responses.getPlayerRole(ctx.author.name)
        await ctx.author.send(response)

    @commands.command(help='Usage: "!info <role>". Shows information about the given role.')
    async def info(self, ctx, role):
        response = responses.getRoleInfo(role)
        await ctx.send(response)

    @commands.command(help='Vote to kill a player. All members of your team must be in agreement.')
    async def kill(self, ctx, target):
        response = responses.killPlayer(target)
        await ctx.send(response)

    @commands.command(help='Heal a player. You cannot heal the same player twice in a row.')
    async def heal(self, ctx, target):
        response = responses.protectPlayer(target)
        await ctx.send(response)

    @commands.command(help='Compare a player to the player you chose the night before. \nFor example: Night 1 -> checked Evan, Night 2 -> checked Emma, Response: They are on opposite teams!\nIf the players are on the same team, they are either both town, both mafia, or both neutrals.')
    async def check(self, ctx, target):
        response = responses.pairwiseInvestigate(target, ctx.author.name)
        await ctx.send(response)

    @commands.command(help='Nominate a player to be voted. Two nominations are required to go to vote.')
    async def nominate(self, ctx, player):
        response = responses.nominatePlayer(player)
        await ctx.send(response)

    @commands.command(help='Usage: "!vote yes/no". Vote a player out. A majority of players must vote yes for the vote to be successful.')
    async def vote(self, ctx, choice):
        response = responses.votePlayer(choice)
        await ctx.send(response)

async def setup(bot):
    await bot.add_cog(Basic(bot))