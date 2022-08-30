import json

from logger import *

from database import *
from common import *
from Utils import FileHandling

from ConcertOfNationsEngine.GameObjects import *

#Deal with savegames
def setupNew_saveGame(savegame, world_name, gamerule_name):
    """
    Given a new savegame object, create a savefile for it and save it to the database.
    """
    logInfo("Setting up a new savegame in the savefiles and database")

    server_id = savegame.id
    
    #Update database
    db = getdb()
    cursor = db.cursor()

    stmt = "INSERT INTO Savegames (server_id, savefile, worldfile, gamerulefile) VALUES (%s, %s, %s, %s)"
    params = [server_id, savegame.name, world_name, gamerule_name]
    cursor.execute(stmt, params)
    db.commit()

    #Generate savefile for the game
    save_saveGame(savegame)

def save_saveGame(savegame):
    """
    Save the savegame to its file based on its id
    """
    FileHandling.easySave(savegame, savegame.name, savesDir)
    logInfo(f"Saved {savegame.name} to file: {savesDir}/{savegame.name}.json")

def load_saveGame(savegame_name):
    """
    Load a savegame object from its savefile
    """
    savegame = FileHandling.easyLoad(savegame_name, savesDir)
    logInfo(f"Savegame {savegame.name} successfully loaded")
    return savegame

def get_players(savegame_name):
    pass


#Deal with other files
def load_gamerule(gamerule_name):
    """
    Load a dictionary from a .json file representing a game's ruleset
    """
    gamerule = FileHandling.easyLoad(gamerule_name, gameruleDir)
    logInfo("Gamerule successfully loaded")
    return gamerule

def load_world(world_name):
    """
    Load a world from a .json file representing a map without nations, buildings etc; only terrain, resources etc.
    """
    world = FileHandling.easyLoad(world_name, worldsDir)
    logInfo(f"World {world.name} successfully loaded")
    return world


#Player
def add_Player(playerID):
    """
    Add a player by discord ID to the database
    """
    db = getdb()
    cursor = db.cursor()

    try:
        stmt = "INSERT INTO Players (discord_id) VALUES (%s)"
        params = [playerID]
        cursor.execute(stmt, params)
        db.commit()
    except Exception as e:
        raise Exception(f"Could not insert player into database: <{e}>")

    logInfo(f"Added player <{playerID}> to the database")

def get_Player(playerID):
        """
        Get the row in the database table Players pertaining to this player
        """

        db = getdb()
        cursor = db.cursor()

        stmt = "SELECT * FROM Players WHERE discord_id=%s LIMIT 1;"
        params = [playerID]
        cursor.execute(stmt, params)
        result = fetch_assoc(cursor)

        if not (result): return False

        logInfo(f"Retrieved player from database with id {result['id']}")
        return result


#Role
def add_Role(roleID, roleName):
    """
    Add a role by discord ID to the database
    """
    db = getdb()
    cursor = db.cursor()

    try:
        stmt = "INSERT INTO Roles (discord_id, name) VALUES (%s, %s)"
        params = [roleID, roleName]
        cursor.execute(stmt, params)
        db.commit()
    except Exception as e:
        raise Exception(f"Could not insert role into database: <{e}>")

    logInfo(f"Added role <{roleID}> to the database")

def get_Role(roleID):
        """
        Get the row in the database table Roles pertaining to this role
        """

        db = getdb()
        cursor = db.cursor()

        stmt = "SELECT * FROM Roles WHERE discord_id=%s LIMIT 1;"
        params = [roleID]
        cursor.execute(stmt, params)
        result = fetch_assoc(cursor)

        if not (result): return False

        logInfo(f"Retrieved role from database with id {result['id']}")
        return result


#Nation
def add_Nation(savegame, nation, playerID):
    """
    Add a nation as a role to the database
    """

    nation_name = nation.name
    roleID = nation.role_id

    db = getdb()
    cursor = db.cursor()

    savegameInfo = savegame.getRow()

    playerInfo = get_Player(playerID)

    #Insert player if need be
    if not (playerInfo):
        add_Player(playerID)
        playerInfo = get_Player(playerID)

    #Insert role

    if not (get_Role(roleID)):
        add_Role(roleID, nation_name)
        roleInfo = get_Role(roleID)

    else: 
        logInfo(f"Role <{roleID}> for \"{nation_name}\" already exists in the database")

    return

    try:
        stmt = "INSERT INTO PlayerGames (player_id, game_id, role_id) VALUES (%s, %s, %s)"
        params = [playerID, savegameInfo["id"], roleID]
        cursor.execute(stmt, params)
        db.commit()
    except Exception as e:
        raise Exception(f"Could not insert nation into database: <{e}>")

    logInfo(f"Added nation \"{nation_name}\" to database")