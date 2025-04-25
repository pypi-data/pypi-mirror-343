# wase_api/map.py

import math
import random

def register(lua_env):
    current_zone = {
        "zoneText": "Stormwind City",
        "realZoneText": "Stormwind City",
        "subZoneText": "Trade District",
        "minimapZoneText": "Stormwind",
        "zonePVPInfo": "friendly",  # "contested", "hostile", "friendly", "sanctuary", "arena"
        "instanceType": None,  # "none", "party", "raid", "pvp", "arena", "scenario"
        "instanceName": "",
        "difficultyID": 1,
        "mapID": 84,
        "continentID": 2,
        "zoneID": 1,
    }

    player_position = {
        "x": 0.5,
        "y": 0.5,
        "facing": random.uniform(0, 2 * math.pi)
    }

    world_map_open = False

    # --- Blizzard API Functions ---
    def GetZoneText(): return current_zone["zoneText"]
    def GetRealZoneText(): return current_zone["realZoneText"]
    def GetSubZoneText(): return current_zone["subZoneText"]
    def GetMinimapZoneText(): return current_zone["minimapZoneText"]
    def GetZonePVPInfo(): return current_zone["zonePVPInfo"]
    def IsInInstance():
        instance_type = current_zone["instanceType"]
        return instance_type is not None and instance_type != "none"
    def GetInstanceInfo():
        return (current_zone["instanceName"], current_zone["instanceType"], current_zone["difficultyID"], current_zone["mapID"])
    def GetMapID(): return current_zone["mapID"]

    # --- Player Position ---
    def C_Map_GetBestMapForUnit(unit):
        return current_zone["mapID"]

    def C_Map_GetPlayerMapPosition(mapID, unit):
        return player_position["x"], player_position["y"]

    def GetPlayerFacing():
        return player_position["facing"]

    # --- World Map Simulation ---
    def ToggleWorldMap():
        nonlocal world_map_open
        world_map_open = not world_map_open
        state = "shown" if world_map_open else "hidden"
        print(f"World Map {state}")

    def IsWorldMapShown():
        return world_map_open

    # --- Continent/Zone Info ---
    def GetCurrentMapContinent(): return current_zone["continentID"]
    def GetCurrentMapZone(): return current_zone["zoneID"]

    # --- Simulation Helpers ---
    def SetZone(zoneText, subZoneText=None, pvpType=None, mapID=None, continentID=None, zoneID=None):
        current_zone["zoneText"] = zoneText
        current_zone["realZoneText"] = zoneText
        if subZoneText: current_zone["subZoneText"] = subZoneText
        if pvpType: current_zone["zonePVPInfo"] = pvpType
        if mapID: current_zone["mapID"] = mapID
        if continentID: current_zone["continentID"] = continentID
        if zoneID: current_zone["zoneID"] = zoneID
        lua_env.globals()['TriggerEvent']("ZONE_CHANGED")
        lua_env.globals()['TriggerEvent']("ZONE_CHANGED_NEW_AREA")
        print(f"Zone changed to '{zoneText}', subzone '{current_zone['subZoneText']}'")

    def SetInstance(instanceName, instanceType="party", difficultyID=1, mapID=1001):
        current_zone["instanceName"] = instanceName
        current_zone["instanceType"] = instanceType
        current_zone["difficultyID"] = difficultyID
        current_zone["mapID"] = mapID
        lua_env.globals()['TriggerEvent']("ZONE_CHANGED_NEW_AREA")
        print(f"Entered instance '{instanceName}' ({instanceType}, difficulty {difficultyID})")

    def SetPlayerPosition(x, y):
        player_position["x"] = max(0.0, min(1.0, x))
        player_position["y"] = max(0.0, min(1.0, y))
        print(f"Player position set to ({x:.2f}, {y:.2f})")

    def SetPlayerFacing(angle):
        player_position["facing"] = angle % (2 * math.pi)
        print(f"Player facing set to {player_position['facing']:.2f} radians")

    # --- Inject into Lua ---
    lua_env.globals()['GetZoneText'] = GetZoneText
    lua_env.globals()['GetRealZoneText'] = GetRealZoneText
    lua_env.globals()['GetSubZoneText'] = GetSubZoneText
    lua_env.globals()['GetMinimapZoneText'] = GetMinimapZoneText
    lua_env.globals()['GetZonePVPInfo'] = GetZonePVPInfo
    lua_env.globals()['IsInInstance'] = IsInInstance
    lua_env.globals()['GetInstanceInfo'] = GetInstanceInfo
    lua_env.globals()['GetMapID'] = GetMapID
    lua_env.globals()['C_Map'] = {
        'GetBestMapForUnit': C_Map_GetBestMapForUnit,
        'GetPlayerMapPosition': C_Map_GetPlayerMapPosition
    }
    lua_env.globals()['GetPlayerFacing'] = GetPlayerFacing
    lua_env.globals()['ToggleWorldMap'] = ToggleWorldMap
    lua_env.globals()['IsWorldMapShown'] = IsWorldMapShown
    lua_env.globals()['GetCurrentMapContinent'] = GetCurrentMapContinent
    lua_env.globals()['GetCurrentMapZone'] = GetCurrentMapZone
    lua_env.globals()['SetZone'] = SetZone
    lua_env.globals()['SetInstance'] = SetInstance
    lua_env.globals()['SetPlayerPosition'] = SetPlayerPosition
    lua_env.globals()['SetPlayerFacing'] = SetPlayerFacing
