import discord
from discord.ext import commands
from discord.utils import get as dget

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
        response = responses.pairwiseInvestigate(target)
        await ctx.send(response)

    @commands.command(help='Nominate a player to be voted. Two nominations are required to go to vote.')
    async def nominate(self, ctx, player):
        response = responses.nominatePlayer(player)
        await ctx.send(response)

    @commands.command(help='Usage: "!vote yes/no". Vote a player out. A majority of players must vote yes for the vote to be successful.')
    async def vote(self, ctx, choice):
        response = responses.votePlayer(choice)
        await ctx.send(response)

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

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(help='Commands for playing the game.')
    async def game(self, ctx):
        pass

    @game.command(help='Starts the game and messages players their roles.')
    @commands.has_role("Moderator")
    async def start(self, ctx, reveal_roles:bool = False):
        players, response = responses.startGame()
        if reveal_roles:
            await ctx.author.send(response)
        else:
            await ctx.send('The game has started.')
        mafia_members = []
        for player in players:
            member = dget(ctx.channel.members, name=player.name)
            if player.role == "Mafia":
                mafia_members.append(member)
            try:
                await member.send(f'Your role is...')
                roleInfo = responses.getRoleInfo(player.role)
                await member.send(roleInfo)
            except Exception as e:
                print(e)
                await ctx.send(f'Failed to send role message to {member}')
        if len(mafia_members) <= 1:
            return
        for i,mafia in enumerate(mafia_members):
            teammates_string = ', '.join([f'{teammate}' for j, teammate in enumerate(mafia_members) if j!=i])
            await mafia.send(f'Your teammates are: {teammates_string}')

    @game.command(help='End the game.')
    @commands.has_role("Moderator")
    async def end(self, ctx):
        response = responses.endGame()
        await ctx.send(response)

    @game.command(help='Enter the night phase of the game and unlock all night actions.')
    @commands.has_role("Moderator")
    async def night(self, ctx):
        response = responses.goToNight()
        await ctx.send(response)

    @game.command(help='Enter the day phase of the game and unlock all day actions.')
    @commands.has_role("Moderator")
    async def day(self, ctx):
        response = responses.goToDay()
        await ctx.send(response)

    @game.command(help='See the active nominations.')
    async def nominations(self, ctx):
        response = responses.getNominations()
        await ctx.send(response)

    @game.command(help='Kill a player.')
    @commands.has_role("Moderator")
    async def forcekill(self, ctx, player: discord.Member):
        response = responses.forceKillPlayer(player)
        await ctx.send(response)

    @forcekill.error
    async def forcekill_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('I could not find that member...')

    @game.command(help='Revive a player.')
    @commands.has_role("Moderator")
    async def revive(self, ctx, player: discord.Member):
        response = responses.revivePlayer(player)
        await ctx.send(response)

    @revive.error
    async def revive_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('I could not find that member...')

    @game.command(help='Shows all players\' roles.')
    @commands.has_role("Moderator")
    async def roles(self, ctx):
        response = responses.getAllPlayerRoles()
        await ctx.author.send(response)

    @game.command(help='Shows medic save history.')
    @commands.has_role("Moderator")
    async def medichistory(self, ctx):
        response = responses.getMedicHistory()
        await ctx.send(response)

    @game.command(help='Shows cop check history.')
    @commands.has_role("Moderator")
    async def cophistory(self, ctx):
        response = responses.getCopHistory()
        await ctx.send(response)

    