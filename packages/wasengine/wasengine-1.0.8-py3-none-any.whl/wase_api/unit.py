# wase_api/unit.py

import random
import uuid

def register(lua_env):
    units = {
        "player": {
            "name": "PlayerOne",
            "guid": str(uuid.uuid4()),
            "health": 5000,
            "max_health": 5000,
            "exists": True,
            "faction": "Alliance",
            "class": "MAGE",
            "is_dead": False,
            "range": 10,
            "is_visible": True,
            "auras": [],
            "casting": None,
        },
        "target": {
            "name": "TargetDummy",
            "guid": str(uuid.uuid4()),
            "health": 10000,
            "max_health": 10000,
            "exists": True,
            "faction": "Neutral",
            "class": "WARRIOR",
            "is_dead": False,
            "range": 10,
            "is_visible": True,
            "auras": [],
            "casting": None,
        }
    }

    # --- Core Unit APIs ---
    def UnitExists(unit): return units.get(unit, {}).get("exists", False)
    def UnitName(unit): return units.get(unit, {}).get("name", "Unknown")
    def UnitGUID(unit): return units.get(unit, {}).get("guid", "")
    def UnitHealth(unit): return units.get(unit, {}).get("health", 0)
    def UnitHealthMax(unit): return units.get(unit, {}).get("max_health", 0)
    def UnitIsDead(unit): return units.get(unit, {}).get("is_dead", False)
    def UnitFactionGroup(unit): return units.get(unit, {}).get("faction", "Neutral")
    def UnitClass(unit): unit_data = units.get(unit, {}); c = unit_data.get("class", "UNKNOWN"); return c, c
    def UnitIsUnit(unit1, unit2): return UnitGUID(unit1) == UnitGUID(unit2)
    def UnitIsVisible(unit): return units.get(unit, {}).get("is_visible", False)
    def CheckInteractDistance(unit, distIndex): return units.get(unit, {}).get("range", 999) <= 10
    def UnitInRange(unit): return units.get(unit, {}).get("range", 999) <= 40

    # --- Aura / Buff / Debuff APIs ---
    def UnitAura(unit, index, filter=None):
        unit_data = units.get(unit, {})
        auras = unit_data.get("auras", [])
        if index <= len(auras):
            aura = auras[index - 1]
            # Returns: name, icon, count, debuffType, duration, expirationTime, source, isStealable, etc.
            return aura["name"], aura["icon"], aura["count"], aura["debuffType"], aura["duration"], aura["expirationTime"], aura["source"], aura["isStealable"]
        return None

    def UnitBuff(unit, index):
        return UnitAura(unit, index, "HELPFUL")

    def UnitDebuff(unit, index):
        return UnitAura(unit, index, "HARMFUL")

    def AddAura(unit, name, icon="Interface\\Icons\\Spell_Nature_Rejuvenation", duration=10, debuffType=None, count=0, source="player", isStealable=False):
        expirationTime = random.uniform(10, 20)
        aura = {
            "name": name,
            "icon": icon,
            "count": count,
            "debuffType": debuffType,
            "duration": duration,
            "expirationTime": expirationTime,
            "source": source,
            "isStealable": isStealable
        }
        units[unit]["auras"].append(aura)
        print(f"Aura '{name}' added to '{unit}'")

    def ClearAuras(unit):
        units[unit]["auras"] = []
        print(f"Auras cleared from '{unit}'")

    # --- Casting APIs ---
    def UnitCastingInfo(unit):
        casting = units.get(unit, {}).get("casting", None)
        if casting:
            # Returns: name, icon, startTime, endTime, isTradeSkill, castID, notInterruptible, spellID
            return casting["name"], casting["icon"], casting["startTime"], casting["endTime"], False, 1, False, casting["spellID"]
        return None

    def UnitChannelInfo(unit):
        # For simplicity, not implementing channels separately
        return None

    def StartCasting(unit, spellID, spellName, castTime):
        startTime = random.uniform(1000, 2000)
        endTime = startTime + castTime
        casting = {
            "spellID": spellID,
            "name": spellName,
            "icon": "Interface\\Icons\\Spell_Nature_Lightning",
            "startTime": startTime,
            "endTime": endTime
        }
        units[unit]["casting"] = casting
        print(f"'{unit}' started casting '{spellName}'")

    def StopCasting(unit):
        units[unit]["casting"] = None
        print(f"'{unit}' stopped casting")

    # --- Manipulate Units for Simulation Purposes ---
    def SetUnitHealth(unit, health):
        if unit in units:
            units[unit]["health"] = max(0, min(health, units[unit]["max_health"]))
            units[unit]["is_dead"] = units[unit]["health"] <= 0

    def SetUnitExists(unit, exists):
        if unit not in units:
            units[unit] = {}
        units[unit]["exists"] = exists

    # --- Inject into Lua ---
    lua_env.globals()['UnitExists'] = UnitExists
    lua_env.globals()['UnitName'] = UnitName
    lua_env.globals()['UnitGUID'] = UnitGUID
    lua_env.globals()['UnitHealth'] = UnitHealth
    lua_env.globals()['UnitHealthMax'] = UnitHealthMax
    lua_env.globals()['UnitIsDead'] = UnitIsDead
    lua_env.globals()['UnitFactionGroup'] = UnitFactionGroup
    lua_env.globals()['UnitClass'] = UnitClass
    lua_env.globals()['UnitIsUnit'] = UnitIsUnit
    lua_env.globals()['UnitIsVisible'] = UnitIsVisible
    lua_env.globals()['CheckInteractDistance'] = CheckInteractDistance
    lua_env.globals()['UnitInRange'] = UnitInRange
    lua_env.globals()['UnitAura'] = UnitAura
    lua_env.globals()['UnitBuff'] = UnitBuff
    lua_env.globals()['UnitDebuff'] = UnitDebuff
    lua_env.globals()['UnitCastingInfo'] = UnitCastingInfo
    lua_env.globals()['UnitChannelInfo'] = UnitChannelInfo

    # --- Simulation Control ---
    lua_env.globals()['SetUnitHealth'] = SetUnitHealth
    lua_env.globals()['SetUnitExists'] = SetUnitExists
    lua_env.globals()['AddAura'] = AddAura
    lua_env.globals()['ClearAuras'] = ClearAuras
    lua_env.globals()['StartCasting'] = StartCasting
    lua_env.globals()['StopCasting'] = StopCasting
