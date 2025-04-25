# wase_api/spell.py

import os
import time as py_time
from wase_core import spell_updater

ICON_DIR = "wase_data/icons"
DEFAULT_ICON = os.path.join(ICON_DIR, "INV_Misc_QuestionMark.blp")

def get_texture_path(iconName):
    icon_filename = f"{iconName}.blp"
    icon_path = os.path.join(ICON_DIR, icon_filename)
    return icon_path if os.path.exists(icon_path) else DEFAULT_ICON

def register(lua_env):
    spells_data = spell_updater.ensure_spells_loaded()

    known_spells = {spellID: True for spellID in spells_data.keys()}
    spell_cooldowns = {spellID: {"start": 0, "duration": 0, "enabled": 0} for spellID in spells_data.keys()}

    def GetSpellInfo(spellID_or_name):
        for spellID, data in spells_data.items():
            name, iconName, castTime, _, _, _ = data
            if spellID_or_name == spellID or spellID_or_name == name:
                icon_path = get_texture_path(iconName.split("\\")[-1])
                return name, "", icon_path, castTime, None, 40
        return None

    def IsUsableSpell(spellID_or_name):
        for spellID, data in spells_data.items():
            if spellID_or_name == spellID or spellID_or_name == data[0]:
                return known_spells.get(spellID, False), True
        return False, False

    def IsSpellInRange(spell, unit):
        return True

    def GetSpellCooldown(spellID):
        cd = spell_cooldowns.get(spellID, {"start": 0, "duration": 0, "enabled": 0})
        return cd["start"], cd["duration"], cd["enabled"]

    def IsSpellKnown(spellID_or_name):
        for spellID, data in spells_data.items():
            if spellID_or_name == spellID or spellID_or_name == data[0]:
                return known_spells.get(spellID, False)
        return False

    def GetSpellTexture(spellID_or_name):
        for spellID, data in spells_data.items():
            if spellID_or_name == spellID or spellID_or_name == data[0]:
                return get_texture_path(data[1].split("\\")[-1])
        return DEFAULT_ICON

    def SetSpellCooldown(spellID, duration):
        start_time = py_time.time()
        spell_cooldowns[spellID] = {"start": start_time, "duration": duration, "enabled": 1}
        print(f"Set cooldown for spell {spellID}: {duration}s")

    def ClearSpellCooldown(spellID):
        spell_cooldowns[spellID] = {"start": 0, "duration": 0, "enabled": 0}
        print(f"Cleared cooldown for spell {spellID}")

    def LearnSpell(spellID):
        known_spells[spellID] = True
        print(f"Spell {spellID} learned")

    def UnlearnSpell(spellID):
        known_spells[spellID] = False
        print(f"Spell {spellID} unlearned")

    lua_env.globals()['GetSpellInfo'] = GetSpellInfo
    lua_env.globals()['IsUsableSpell'] = IsUsableSpell
    lua_env.globals()['IsSpellInRange'] = IsSpellInRange
    lua_env.globals()['GetSpellCooldown'] = GetSpellCooldown
    lua_env.globals()['IsSpellKnown'] = IsSpellKnown
    lua_env.globals()['GetSpellTexture'] = GetSpellTexture
    lua_env.globals()['SetSpellCooldown'] = SetSpellCooldown
    lua_env.globals()['ClearSpellCooldown'] = ClearSpellCooldown
    lua_env.globals()['LearnSpell'] = LearnSpell
    lua_env.globals()['UnlearnSpell'] = UnlearnSpell
