import json
from dataclasses import dataclass
import random

players = []
active_roles = []
roles = []
active_players = []
checked_players = []
game_started = False
is_night = True
cop_checked = False

@dataclass
class Player():
    name: str
    role: str
    alive: bool = True

async def loadRoles():
    global roles
    with open('roles.json') as f:
        roles = json.load(f)
    f.close()

def getRole(role_name: str):
    role = next((r for r in roles if r["name"].lower() == role_name.lower()), None)
    return role

def addRole(role_name: str):
    role = getRole(role_name)
    if role is None:
        raise ValueError(f'Failed to add {role_name}. Not a valid role.')
    if len(active_roles) < len(players):
        active_roles.append(role["name"])
    elif role["team"] == "Town" or role["name"] == "Mafia":
        if len(list(filter(lambda r: (r == "Town"), active_roles))) > 0:
            active_roles.remove("Town")
            active_roles.append(role["name"])
        else:
            raise ValueError(f'Failed to add {role_name}. Active roles are full.')
    else:
        raise NotImplementedError("Roles other than default mafia, or special town have not been implemented.")
        
def removeRole(role_name: str):
    try:
        active_roles.remove(role_name)
    except ValueError as e:
        raise ValueError(f'Failed to remove role: {role_name}. Not in active roles.')
    active_roles.append("Town")

def clearRoles():
    active_roles.clear()

def addDefaultRoles(num_players: int):
    if num_players == -1:
        num_players = len(players)
    global active_roles
    active_roles = []
    if num_players < 4:
        raise ValueError("Not enought players.")
    num_mafia = int(num_players / 3)
    active_roles.append("Cop")
    active_roles.append("Medic")
    for _ in range(num_mafia):
        active_roles.append("Mafia")
    num_active_roles = len(active_roles)
    for _ in range(num_players - num_active_roles):
        active_roles.append("Town")
    return active_roles

def assignRoles():
    assert len(active_roles) == len(players)
    global active_players
    active_players = []
    r = active_roles.copy()
    for player in players:
        i = random.randint(0,len(r)-1)
        role = r.pop(i)
        active_players.append(Player(player, role))
    return active_players

def getActivePlayer(name):

    return next((player for player in active_players if player.name.lower() == name.lower()), None)


def startGame():
    if len(active_players) != len(players):
        assignRoles()
    
    global game_started
    global is_night
    global cop_checked
    game_started = True
    is_night = True
    cop_checked = False

    return active_players

def pairwiseInvestigate(target: str, authorname: str):
    author = getActivePlayer(authorname)
    authorrolename = author.role

    if authorrolename != 'Cop':
        return'You are not the cop'

    global cop_checked
    if cop_checked:
        return'You have already checked someone'

    checkedplayer = getActivePlayer(target)
    rolename = checkedplayer.role #role name
    roleobject = getRole(rolename)
    team = roleobject["team"] #team name

    if len(checked_players) == 0:

        checked_players.append(checkedplayer)
        cop_checked = True
        return 'This the first check'

    for player in checked_players:

        if target == player.name:

            return 'This player has already been checked'

    previouscheck = checked_players[-1]
    previousrolename = previouscheck.role
    previousroleobject = getRole(previousrolename)
    previousteam = previousroleobject["team"]


    checked_players.append(checkedplayer)
    cop_checked = True
    return 'Players are on the same team' if team == previousteam else 'Players are not on the same team'









