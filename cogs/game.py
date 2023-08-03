import discord
from discord.ext import commands
from discord.utils import get as dget

import responses

import os

#MAFIA_CHANNEL_ID = os.environ.get("MafiaChannelID")
MAFIA_CHANNEL_ID = 1136757303136231497

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
        global MAFIA_CHANNEL_ID
        if MAFIA_CHANNEL_ID == None:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            channel = await ctx.guild.create_text_channel('mafia', overwrites=overwrites)
            MAFIA_CHANNEL_ID = channel.id
            os.environ.encodekey
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

async def setup(bot):
    await bot.add_cog(Game(bot))