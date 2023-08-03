import discord
from discord.ext import commands

import responses

class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(help='Commands for handling roles.')
    async def roles(self, ctx):
        pass

    @roles.command(help='Lists all available roles.')
    async def list(self, ctx):
        response = responses.getRoleList()
        await ctx.send(response)

    @roles.command(help='Adds a role to the game.')
    @commands.has_role("Moderator")
    async def add(self, ctx, role):
        response = responses.addRole(str(role).capitalize())
        await ctx.send(response)

    @roles.command(help='Removes a role from the game and replaces it with Town.')
    @commands.has_role("Moderator")
    async def remove(self, ctx, role):
        response = responses.removeRole(str(role).capitalize())
        await ctx.send(response)

    @roles.command(help='Lists all active roles.')
    async def active(self, ctx):
        response = responses.getActiveRoles()
        await ctx.send(response)

    @roles.command(help='Clears all roles from the game.')
    @commands.has_role("Moderator")
    async def clear(self, ctx):
        response = responses.clearRoles()
        await ctx.send(response)

    @roles.command(help='Usage: "!roles default [number of players]". Adds the default roles (Cop, Medic, and Mafia equal to the square root of town).')
    async def default(self, ctx, num_players : int=-1):
        try:
            response = responses.addDefaultRoles(num_players)
        except ValueError as e:
            response = e
        await ctx.send(response)
    
    @roles.command(help='Randomly assigns roles to players.')
    @commands.has_role("Moderator")
    async def assign(self, ctx, reveal_roles: bool = False):
        response = responses.assignRoles()
        if reveal_roles:
            await ctx.author.send(response)
        else:
            await ctx.send('Roles have been assigned.')


    @roles.command(help='Usage: "!roles role <player>". Privately messages you a player\'s role.')
    @commands.has_role("Moderator")
    async def role(self, ctx, player: discord.Member):
        response = responses.getPlayerRole(player)
        await ctx.author.send(response)

    @role.error
    async def role_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('I could not find that member...')

async def setup(bot):
    await bot.add_cog(Role(bot))