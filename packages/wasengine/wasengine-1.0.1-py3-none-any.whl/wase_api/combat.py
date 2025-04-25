# wase_api/combat.py

import time as py_time
import random
import uuid

def register(lua_env):
    combat_log_listeners = []
    last_event_info = {}
    combat_units = set()

    # --- COMBAT_LOG_EVENT_UNFILTERED Event Simulation ---
    def RegisterCombatLogListener(callback):
        combat_log_listeners.append(callback)
        print("Combat log listener registered.")

    def TriggerCombatLogEvent(
        timestamp=None,
        event="SPELL_DAMAGE",
        sourceGUID=None, sourceName=None, sourceFlags=0, sourceRaidFlags=0,
        destGUID=None, destName=None, destFlags=0, destRaidFlags=0,
        *args
    ):
        nonlocal last_event_info
        timestamp = timestamp or py_time.time()
        sourceGUID = sourceGUID or str(uuid.uuid4())
        sourceName = sourceName or "UnknownSource"
        destGUID = destGUID or str(uuid.uuid4())
        destName = destName or "UnknownDest"

        event_data = (
            timestamp, event,
            sourceGUID, sourceName, sourceFlags, sourceRaidFlags,
            destGUID, destName, destFlags, destRaidFlags,
            *args
        )

        last_event_info = event_data  # Store last event

        for listener in combat_log_listeners:
            listener(event_data)

        print(f"Triggered combat log event: {event} from {sourceName} to {destName}")

    # --- Blizzard's API ---
    def CombatLogGetCurrentEventInfo():
        return last_event_info

    # --- Combat State Management ---
    def EnterCombatForUnit(unit):
        combat_units.add(unit)
        if unit == "player":
            lua_env.globals()['TriggerEvent']("PLAYER_REGEN_DISABLED")
            print(f"'{unit}' entered combat")

    def ExitCombatForUnit(unit):
        combat_units.discard(unit)
        if unit == "player":
            lua_env.globals()['TriggerEvent']("PLAYER_REGEN_ENABLED")
            print(f"'{unit}' left combat")

    def UnitAffectingCombat(unit):
        return unit in combat_units

    # --- Encounter Simulation ---
    def SimulateEncounterStart(encounterID=1, encounterName="Dummy Encounter", difficultyID=1):
        lua_env.globals()['TriggerEvent']("ENCOUNTER_START", encounterID, encounterName, difficultyID)
        print(f"Simulated ENCOUNTER_START: {encounterName}")

    def SimulateEncounterEnd(encounterID=1, encounterName="Dummy Encounter", difficultyID=1, success=True):
        lua_env.globals()['TriggerEvent']("ENCOUNTER_END", encounterID, encounterName, difficultyID, int(success))
        print(f"Simulated ENCOUNTER_END: {encounterName} {'Success' if success else 'Failure'}")

    # --- Pre-built Event Simulators ---
    def SimulateAttack(source="player", dest="target", spellID=133, spellName="Fireball", damage=1000):
        TriggerCombatLogEvent(
            None, "SPELL_DAMAGE",
            str(uuid.uuid4()), source, 0, 0,
            str(uuid.uuid4()), dest, 0, 0,
            spellID, spellName, 0, damage, 0, 0, 0
        )

    def SimulateSpellCast(source="player", dest="target", spellID=116, spellName="Frostbolt"):
        TriggerCombatLogEvent(
            None, "SPELL_CAST_START",
            str(uuid.uuid4()), source, 0, 0,
            str(uuid.uuid4()), dest, 0, 0,
            spellID, spellName, 0
        )

    def SimulateSpellSuccess(source="player", dest="target", spellID=116, spellName="Frostbolt"):
        TriggerCombatLogEvent(
            None, "SPELL_CAST_SUCCESS",
            str(uuid.uuid4()), source, 0, 0,
            str(uuid.uuid4()), dest, 0, 0,
            spellID, spellName, 0
        )

    # --- Blizzard Simulated Event Trigger ---
    def FireCombatLogEvent():
        lua_env.globals()['TriggerEvent']("COMBAT_LOG_EVENT_UNFILTERED")

    # --- Inject into Lua ---
    lua_env.globals()['RegisterCombatLogListener'] = RegisterCombatLogListener
    lua_env.globals()['TriggerCombatLogEvent'] = TriggerCombatLogEvent
    lua_env.globals()['CombatLogGetCurrentEventInfo'] = CombatLogGetCurrentEventInfo
    lua_env.globals()['FireCombatLogEvent'] = FireCombatLogEvent
    lua_env.globals()['SimulateAttack'] = SimulateAttack
    lua_env.globals()['SimulateSpellCast'] = SimulateSpellCast
    lua_env.globals()['SimulateSpellSuccess'] = SimulateSpellSuccess
    lua_env.globals()['SimulateEncounterStart'] = SimulateEncounterStart
    lua_env.globals()['SimulateEncounterEnd'] = SimulateEncounterEnd
    lua_env.globals()['EnterCombatForUnit'] = EnterCombatForUnit
    lua_env.globals()['ExitCombatForUnit'] = ExitCombatForUnit
    lua_env.globals()['UnitAffectingCombat'] = UnitAffectingCombat
