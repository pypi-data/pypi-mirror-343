# wase_api/actionbar.py

import time as py_time
import os

ICON_DIR = "wase_data/icons"
DEFAULT_ICON = os.path.join(ICON_DIR, "INV_Misc_QuestionMark.blp")

def get_texture_path(iconName):
    icon_filename = f"{iconName}.blp"
    icon_path = os.path.join(ICON_DIR, icon_filename)
    return icon_path if os.path.exists(icon_path) else DEFAULT_ICON

def register(lua_env):
    # --- Action Slots Simulation ---
    # Each slot: { "type": "spell"/"item", "id": spellID/itemID, "texture": path, "cooldown": dict }
    action_slots = {
        1: {"type": "spell", "id": 133, "texture": get_texture_path("Spell_Fire_FlameBolt"), "cooldown": {"start": 0, "duration": 0, "enabled": 0}},
        2: {"type": "spell", "id": 116, "texture": get_texture_path("Spell_Frost_FrostBolt02"), "cooldown": {"start": 0, "duration": 0, "enabled": 0}},
        # Add more slots as needed...
    }

    # --- API Functions ---
    def GetActionInfo(slot):
        action = action_slots.get(slot)
        if action:
            return action["type"], action["id"], action["texture"]
        return None, None, None

    def HasAction(slot):
        return slot in action_slots

    def UseAction(slot):
        action = action_slots.get(slot)
        if not action:
            print(f"No action in slot {slot}")
            return
        print(f"Using action in slot {slot}: {action['type']} {action['id']}")
        # Simulate casting or item use
        # Example: trigger spell cooldown
        now = py_time.time()
        action["cooldown"] = {"start": now, "duration": 5, "enabled": 1}  # 5 sec CD example
        lua_env.globals()['TriggerEvent']("ACTIONBAR_UPDATE_COOLDOWN")

    def IsActionUsable(slot):
        action = action_slots.get(slot)
        if not action:
            return False, False
        return True, True  # Usable, no mana check

    def GetActionCooldown(slot):
        action = action_slots.get(slot)
        if action:
            cd = action["cooldown"]
            return cd["start"], cd["duration"], cd["enabled"]
        return 0, 0, 0

    def GetActionTexture(slot):
        action = action_slots.get(slot)
        if action:
            return action["texture"]
        return DEFAULT_ICON

    # --- Simulation Helpers ---
    def SetAction(slot, actionType, actionID, iconName):
        texture = get_texture_path(iconName)
        action_slots[slot] = {"type": actionType, "id": actionID, "texture": texture, "cooldown": {"start": 0, "duration": 0, "enabled": 0}}
        print(f"Set action slot {slot}: {actionType} {actionID}")

    def ClearAction(slot):
        if slot in action_slots:
            del action_slots[slot]
            print(f"Cleared action slot {slot}")

    def ResetAllActionCooldowns():
        for action in action_slots.values():
            action["cooldown"] = {"start": 0, "duration": 0, "enabled": 0}
        print("All action cooldowns reset")
        lua_env.globals()['TriggerEvent']("ACTIONBAR_UPDATE_COOLDOWN")

    # --- Inject into Lua ---
    lua_env.globals()['GetActionInfo'] = GetActionInfo
    lua_env.globals()['HasAction'] = HasAction
    lua_env.globals()['UseAction'] = UseAction
    lua_env.globals()['IsActionUsable'] = IsActionUsable
    lua_env.globals()['GetActionCooldown'] = GetActionCooldown
    lua_env.globals()['GetActionTexture'] = GetActionTexture
    lua_env.globals()['SetAction'] = SetAction
    lua_env.globals()['ClearAction'] = ClearAction
    lua_env.globals()['ResetAllActionCooldowns'] = ResetAllActionCooldowns