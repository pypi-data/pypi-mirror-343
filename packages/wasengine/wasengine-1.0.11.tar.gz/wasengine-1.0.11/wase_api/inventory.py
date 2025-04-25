# wase_api/inventory.py

import os
import time as py_time

ICON_DIR = "wase_data/icons"
DEFAULT_ICON = os.path.join(ICON_DIR, "INV_Misc_QuestionMark.blp")

def get_texture_path(iconName):
    icon_filename = f"{iconName}.blp"
    icon_path = os.path.join(ICON_DIR, icon_filename)
    return icon_path if os.path.exists(icon_path) else DEFAULT_ICON

def register(lua_env):
    inventory = {
        1: {"itemID": 12345, "name": "Mighty Helmet", "texture": get_texture_path("INV_Helmet_03"), "cooldown": 0},
        2: {"itemID": 67890, "name": "Shiny Necklace", "texture": get_texture_path("INV_Jewelry_Necklace_04"), "cooldown": 0},
    }

    item_cooldowns = {
        12345: {"start": 0, "duration": 0, "enabled": 0},
        67890: {"start": 0, "duration": 0, "enabled": 0},
    }

    def GetInventoryItemID(unit, slot):
        item = inventory.get(slot)
        return item["itemID"] if item else None

    def GetInventoryItemLink(unit, slot):
        item = inventory.get(slot)
        return f"|cff0070dd|Hitem:{item['itemID']}::::::::::::|h[{item['name']}]|h|r" if item else None

    def GetInventoryItemTexture(unit, slot):
        item = inventory.get(slot)
        return item["texture"] if item else None

    def GetInventoryItemCooldown(unit, slot):
        item = inventory.get(slot)
        if item:
            cd = item_cooldowns.get(item["itemID"], {"start": 0, "duration": 0, "enabled": 0})
            return cd["start"], cd["duration"], cd["enabled"]
        return 0, 0, 0

    def GetItemCooldown(itemID):
        cd = item_cooldowns.get(itemID, {"start": 0, "duration": 0, "enabled": 0})
        return cd["start"], cd["duration"], cd["enabled"]

    def IsEquippedItem(itemID_or_name):
        return any(itemID_or_name in (item["itemID"], item["name"]) for item in inventory.values())

    def HasWandEquipped():
        return any(item["name"] == "Magic Wand" for item in inventory.values())

    def EquipItem(slot, itemID, name, texture="INV_Misc_QuestionMark"):
        resolved_texture = get_texture_path(texture.split("\\")[-1])
        inventory[slot] = {"itemID": itemID, "name": name, "texture": resolved_texture, "cooldown": 0}
        item_cooldowns[itemID] = {"start": 0, "duration": 0, "enabled": 0}
        print(f"Equipped '{name}' in slot {slot}")

    def SetItemCooldown(itemID, duration):
        start_time = py_time.time()
        item_cooldowns[itemID] = {"start": start_time, "duration": duration, "enabled": 1}
        print(f"Set cooldown for item {itemID}: {duration}s")

    def ClearItemCooldown(itemID):
        item_cooldowns[itemID] = {"start": 0, "duration": 0, "enabled": 0}
        print(f"Cleared cooldown for item {itemID}")

    lua_env.globals()['GetInventoryItemID'] = GetInventoryItemID
    lua_env.globals()['GetInventoryItemLink'] = GetInventoryItemLink
    lua_env.globals()['GetInventoryItemTexture'] = GetInventoryItemTexture
    lua_env.globals()['GetInventoryItemCooldown'] = GetInventoryItemCooldown
    lua_env.globals()['GetItemCooldown'] = GetItemCooldown
    lua_env.globals()['IsEquippedItem'] = IsEquippedItem
    lua_env.globals()['HasWandEquipped'] = HasWandEquipped
    lua_env.globals()['EquipItem'] = EquipItem
    lua_env.globals()['SetItemCooldown'] = SetItemCooldown
    lua_env.globals()['ClearItemCooldown'] = ClearItemCooldown
