import json
from dataclasses import dataclass
import random

@dataclass
class Player():
    name: str
    role: str
    alive: bool = True
    used_action: bool = False

# The players in the game
players: list[str] = []

# The roles to be used in the game
game_roles: list[str] = []

# All the available roles
available_roles: list[dict[str,str]] = []

# Players in the game with their assigned roles
game_players: list[Player] = []

# List of players the cop has checked
checked_players: list[Player] = []

game_started = False
is_night = True

# takes a player's username as a string and add's them to the players list if they are not already in it
# returns true if the player was successfully added, otherwise, returns false
def addPlayer(username: str) -> bool:
    if username not in players:
        players.append(username)
        return True
    return False

# removes a player from the players list based on their username
# returns true if the player was removed and false otherwise
def removePlayer(username: str) -> bool:
    if username in players:
        players.remove(username)
        return True
    return False

# gets the list of players
def getPlayerList() -> list[str]:
    return players

# clears the player list
def clearPlayerList():
    players.clear()

# loads roles from roles.json into the roles list
async def loadRoles():
    global available_roles
    with open('roles.json') as f:
        available_roles = json.load(f)
    f.close()

# Returns a Role object (defined in roles.json) if the role's name matches the parameter role_name
def getRole(role_name: str) -> dict[str, str]:
    return next((r for r in available_roles if r["name"].lower() == role_name.lower()), None)

# Adds a role to the active roles list based on the roles name
# Only adds roles up to the number of players in the game
# Adding a special role removes a town role if the role list is full
def addRole(role_name: str):
    role = getRole(role_name)
    if role is None:
        raise ValueError(f'Failed to add {role_name}. Not a valid role.')
    if len(game_roles) < len(players):
        game_roles.append(role["name"])
    elif role["team"] == "Town" or role["name"] == "Mafia":
        if len(list(filter(lambda r: (r == "Town"), game_roles))) > 0:
            game_roles.remove("Town")
            game_roles.append(role["name"])
        else:
            raise ValueError(f'Failed to add {role_name}. Active roles are full.')
    else:
        raise NotImplementedError("Roles other than default mafia, or special town have not been implemented.")
        
# removes a role based on its name
# replaces the roll with town
def removeRole(role_name: str):
    try:
        game_roles.remove(role_name)
    except ValueError as e:
        raise ValueError(f'Failed to remove role: {role_name}. Not in active roles.')
    game_roles.append("Town")

# Gets the list of available roles
def getAvailableRoleList() -> list[dict[str,str]]:
    return available_roles

# Gets the list of roles being used in the game
def getGameRoles() -> list[str]:
    return game_roles

# clears the list of roles in the game
def clearRoles():
    game_roles.clear()

# adds the default roles to the game
# these roles are:
# 1 Cop
# 1 Medic
# Mafia equal to the # of players divided by three, rounded down
# The rest town
# The roles are only added if there are at least 4 players in the game
# Returns the names of the roles that were added
def addDefaultRoles(num_players: int) -> list[str]:
    if num_players == -1:
        num_players = len(players)
    global game_roles
    game_roles = []
    if num_players < 4:
        raise ValueError("Not enought players.")
    num_mafia = int(num_players / 3)
    game_roles.append("Cop")
    game_roles.append("Medic")
    for _ in range(num_mafia):
        game_roles.append("Mafia")
    num_active_roles = len(game_roles)
    for _ in range(num_players - num_active_roles):
        game_roles.append("Town")
    return game_roles

# Assigns the roles that were added to the game to the players in the game
# Only works if the number of players in the game is equal to the number of roles added
# Returns the player objects containing their name and role
def assignRoles() -> list[Player]:
    assert len(game_roles) == len(players)
    global game_players
    game_players = []
    r = game_roles.copy()
    for player in players:
        i = random.randint(0,len(r)-1)
        role = r.pop(i)
        game_players.append(Player(player, role))
    return game_players

# Gets a player object based on that player's name
def getActivePlayer(name) -> Player:
    return next((player for player in game_players if player.name.lower() == name.lower()), None)

# Gets the list of all players in the game
def getGamePlayers() -> list[Player]:
    return game_players

# Starts the game
# If the roles aren't assigned, it assigns the roles
# Returns the players in the game
def startGame() -> list[Player]:
    if len(game_players) != len(players):
        assignRoles()
    
    global game_started
    global is_night
    game_started = True
    is_night = True

    for player in game_players:
        player.alive = True
        player.used_action = False

    return game_players

# The cop's night action
# Only works if the author's name has the cop role
# Returns a message based on whether or not the current and previous check are on the same team
def pairwiseInvestigate(target: str, authorname: str) -> str:
    author = getActivePlayer(authorname)
    authorrolename = author.role

    if authorrolename != 'Cop':
        return'You are not the cop'

    if author.used_action:
        return'You have already checked someone'

    checkedplayer = getActivePlayer(target)
    rolename = checkedplayer.role #role name
    roleobject = getRole(rolename)
    team = roleobject["team"] #team name

    if len(checked_players) == 0:

        checked_players.append(checkedplayer)
        author.used_action = True
        return 'This the first check'

    for player in checked_players:

        if target == player.name:

            return 'This player has already been checked'

    previouscheck = checked_players[-1]
    previousrolename = previouscheck.role
    previousroleobject = getRole(previousrolename)
    previousteam = previousroleobject["team"]


    checked_players.append(checkedplayer)
    author.used_action = True
    return 'Players are on the same team' if team == previousteam else 'Players are not on the same team'









