import json, datetime, pprint, traceback, re

import discord
from discord.ext import commands
from discord.utils import get

from common import *
from database import *
from logger import *

from GameUtils import Operations as ops

from DiscordUtils.menuembed import *
from DiscordUtils.GetGameInfo import *

from ConcertOfNationsEngine.GameHandling import *
from ConcertOfNationsEngine.CustomExceptions import *
import ConcertOfNationsEngine.Buildings as buildings
import ConcertOfNationsEngine.Territories as territories


#The cog itself
class BuildingCommands(commands.Cog):
    """ A cog that allows its client bot to watch member statuses """
    
    def __init__(self, client):
        self.client = client
        
    @commands.command(aliases = ["buybuilding", "buy-building"])
    async def buy_building(self, ctx, terrID, buildingName):
        """ As a nation, this is an order to expend resources to purchase a building """
        logInfo(f"buy_building(({ctx.guild.id}, {terrID}, {buildingName})")

        savegame = get_SavegameFromCtx(ctx)
        if not (savegame): 
            return #Error will already have been handled

        world = savegame.getWorld()
        if not (world):
            raise InputError("Savegame's world could not be retrieved")

        if terrID.isdigit(): terrID = int(terrID)

        #Territory info from the map
        world_terrInfo = world[terrID]

        if not world_terrInfo:
            raise InputError(f"Invalid Territory Name or ID \"{terrID}\"")
        
        territoryName = world_terrInfo.name

        playerinfo = get_player_byGame(savegame, ctx.author.id)

        if not (playerinfo):
            raise InputError(f"Could not get a nation for player <@{ctx.author.id}>")

        roleid = playerinfo['role_discord_id']

        nation = get_NationFromRole(ctx, roleid, savegame)
        if not (nation): 
            return #Error will already have been handled

        #Validate that building can be bought

        if not (nation.canBuyBuilding(savegame, buildingName, buildings.get_blueprint(buildingName, savegame), territoryName)):
            raise InputError(f"Could not buy {buildingName}")

        nation.addBuilding(buildingName, territoryName, savegame)

        await ctx.send(f"Successfully bought {buildingName} in {territoryName}!")

        save_saveGame(savegame)

    @commands.command(aliases = ["togglebuilding", "toggle-building"])
    async def toggle_building(self, ctx, terrID, buildingName):
        """ Switch a building's status between Active and Inactive """
        logInfo(f"toggle_building({ctx.guild.id}, {terrID}, {buildingName})")

        savegame = get_SavegameFromCtx(ctx)
        if not (savegame): 
            return #Error will already have been handled

        world = savegame.getWorld()
        if not (world):
            raise InputError("Savegame's world could not be retrieved")

        if terrID.isdigit(): terrID = int(terrID)

        #Territory info from the map
        world_terrInfo = world[terrID]

        if not world_terrInfo:
            raise InputError(f"Invalid Territory Name or ID \"{terrID}\"")
        
        territoryName = world_terrInfo.name

        playerinfo = get_player_byGame(savegame, ctx.author.id)

        if not (playerinfo):
            raise InputError(f"Could not get a nation for player <@{ctx.author.id}>")

        roleid = playerinfo['role_discord_id']

        nation = get_NationFromRole(ctx, roleid, savegame)
        if not (nation): 
            return #Error will already have been handled

        if (territoryName not in nation.territories.keys()):
            raise InputError(f"Nation {nation.name} does not own territory \"{territoryName}\"")

        newstatus = territories.territory_togglebuilding(nation, territoryName, buildingName)

        await ctx.send(f"New building status: {newstatus}")

        save_saveGame(savegame)

    @commands.command(aliases = ["destroybuilding", "destroy-building", "deletebuilding", "delete_building", "delete-building"])
    async def destroy_building(self, ctx, terrID, buildingName):
        """ Remove a building from a territory owned by the user """
        logInfo(f"destroy_building({ctx.guild.id}, {terrID}, {buildingName})")

        savegame = get_SavegameFromCtx(ctx)
        if not (savegame): 
            return #Error will already have been handled

        world = savegame.getWorld()
        if not (world):
            raise InputError("Savegame's world could not be retrieved")

        if terrID.isdigit(): terrID = int(terrID)

        #Territory info from the map
        world_terrInfo = world[terrID]

        if not world_terrInfo:
            raise InputError(f"Invalid Territory Name or ID \"{terrID}\"")
        
        territoryName = world_terrInfo.name

        #Nation info
        playerinfo = get_player_byGame(savegame, ctx.author.id)

        if not (playerinfo):
            raise InputError(f"Could not get a nation for player <@{ctx.author.id}>")

        roleid = playerinfo['role_discord_id']

        nation = get_NationFromRole(ctx, roleid, savegame)
        if not (nation): 
            return #Error will already have been handled

        #Can we do the operation on this territory

        if (territoryName not in nation.territories.keys()):
            raise InputError(f"Nation {nation.name} does not own territory \"{territoryName}\"")

        if (not territories.territory_hasbuilding(nation, territoryName, buildingName)):
            raise InputError(f"Territory {territoryName} does not have building {buildingName}")

        newstatus = territories.territory_destroybuilding(nation, territoryName, buildingName)

        await ctx.send(f"Building {buildingName} has successfully been deleted from territory {territoryName}")

        save_saveGame(savegame)



async def setup(client):
    await client.add_cog(BuildingCommands(client))