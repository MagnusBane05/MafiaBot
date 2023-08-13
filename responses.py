import game

### Viewing or changing the players in the game ###

def playerJoins(username) -> str:
    return f'{username} joined the game.' if game.addPlayer(username) else f'{username} is already in the game.'
    
def playerLeaves(username):
    return f'{username} has left the game.' if game.removePlayer(username) else f'{username} is not in the game.'

def getPlayerList():
    player_list = game.getPlayerList()

    if len(player_list) == 0:
        return "No players."

    player_list_string = ""
    for player in player_list:
        player_list_string += "- " + player + "\n"

    player_list_string = player_list_string.rsplit('\n', 1)[0]

    return 'Players: \n' + player_list_string

def clearPlayerList():
    game.clearPlayerList()
    return 'Player list has been cleared.'

### Changing or viewing the roles that are active in the game ###

def getRoleList():
    role_list = '## Available roles\n' + '\n '.join([role["name"] for role in game.getAvailableRoleList()])
    return role_list

def addRole(role: str):
    try:
        game.addRole(role)
        return f'Added role: {role}'
    except ValueError as e:
        return e.__str__()

def removeRole(role: str):
    try:
        game.removeRole(role)
        return f'Removed role: {role} and replaced with Town'
    except ValueError as e:
        return e.__str__() 

def clearRoles():
    game.clearRoles()
    return 'Cleared roles.'

def addDefaultRoles(num_players: int):
    roles = game.addDefaultRoles(num_players)
    role_count = {role: roles.count(role) for role in roles}
    return '## Default roles added\n' + '\n'.join([f'{role} ({role_count[role]})' for role in role_count.keys()])

def getActiveRoles():
    roles = game.getGameRoles()
    role_count = {role: roles.count(role) for role in roles}
    return '## Active roles\n' + '\n'.join([f'{role} ({role_count[role]})' for role in role_count.keys()])

def getRoleInfo(role_name):
    role = game.getRole(role_name)
    if role is None:
        return f'No role found with name {role_name}'
    return f'## {role["name"]}\n**Description:** {role["night_description"]}\n**Night action:** `{role["night_action"]}`'

def assignRoles():
    active_players = game.assignRoles()
    if len(active_players) == 0:
        return 'No players are in the game or no roles are active.'
    return '\n'.join([f'{player.name} ({player.role})' for player in active_players])

def getPlayerRole(player):
    name = player.name
    found_player = game.getActivePlayer(name)
    return f'{name} ({found_player.role})' if found_player is not None else f'{name} is not an active player or does not have a role assigned.'

### Commands for during the game ###

def startGame():
    try:
        active_players = game.startGame()
    except Exception as e:
        return None, e.__str__()
    return active_players, '\n'.join([f'{player.name} ({player.role})' for player in active_players])

def getAllPlayerRoles():
    active_players = game.getGamePlayers()
    if len(active_players) == 0:
        return 'No active players.'
    return '\n'.join([f'{player.name} ({player.role})' for player in active_players])

def killPlayer(target: str):
    return 'No function yet'

def pairwiseInvestigate(target: str,author: str):
    return game.pairwiseInvestigate(target, author)

def protectPlayer(target: str):
    return ""

def nominatePlayer(target: str):
    return ""

def votePlayer(target: str):
    return ""

