def register(lua_env):
    # Ensure Enum exists
    lua_env.execute("Enum = Enum or {}")

    # Item Quality
    lua_env.globals()['Enum']['ItemQuality'] = {
        'Poor': 0,
        'Common': 1,
        'Uncommon': 2,
        'Rare': 3,
        'Epic': 4,
        'Legendary': 5,
        'Artifact': 6,
        'Heirloom': 7,
        'WoWToken': 8,
    }

    # Inventory Types
    lua_env.globals()['Enum']['InventoryType'] = {
        'Head': 1,
        'Neck': 2,
        'Shoulder': 3,
        'Body': 4,
        'Chest': 5,
        'Waist': 6,
        'Legs': 7,
        'Feet': 8,
        'Wrist': 9,
        'Hands': 10,
        'Finger': 11,
        'Trinket': 12,
        'Weapon': 13,
        'Shield': 14,
        'Ranged': 15,
        'Cloak': 16,
        '2HWeapon': 17,
        'Bag': 18,
        'Tabard': 19,
        'Robe': 20,
        'MainHand': 21,
        'OffHand': 22,
        'Holdable': 23,
        'Ammo': 24,
        'Thrown': 25,
        'RangedRight': 26,
        'Quiver': 27,
        'Relic': 28,
    }

    # Item Bind Types
    lua_env.globals()['Enum']['ItemBind'] = {
        'None': 0,
        'OnAcquire': 1,
        'OnEquip': 2,
        'OnUse': 3,
        'Quest': 4,
    }

    # Unit Sex
    lua_env.globals()['Enum']['UnitSex'] = {
        'None': 1,
        'Male': 2,
        'Female': 3,
    }

    # Power Types
    lua_env.globals()['Enum']['PowerType'] = {
        'HealthCost': -2,
        'None': -1,
        'Mana': 0,
        'Rage': 1,
        'Focus': 2,
        'Energy': 3,
        'ComboPoints': 4,
        'Runes': 5,
        'RunicPower': 6,
        'SoulShards': 7,
        'LunarPower': 8,
        'HolyPower': 9,
        'Alternate': 10,
        'Maelstrom': 11,
        'Chi': 12,
        'Insanity': 13,
        'ArcaneCharges': 16,
        'Fury': 17,
        'Pain': 18,
        'Essence': 19,
    }

    # Unit Classification
    lua_env.globals()['Enum']['UnitClassification'] = {
        'Normal': 0,
        'Elite': 1,
        'RareElite': 2,
        'WorldBoss': 3,
        'Rare': 4,
    }

    # UI Map Types
    lua_env.globals()['Enum']['UIMapType'] = {
        'Cosmic': 0,
        'World': 1,
        'Continent': 2,
        'Zone': 3,
        'Dungeon': 4,
        'Micro': 5,
        'Orphan': 6,
    }

    # Specialization Type (Roles)
    lua_env.globals()['Enum']['SpecializationType'] = {
        'RoleTank': 1,
        'RoleHealer': 2,
        'RoleDamage': 3,
    }

    # Loot Slot Types
    lua_env.globals()['Enum']['LootSlotType'] = {
        'Item': 1,
        'Money': 2,
        'Currency': 3,
    }

    # Token Categories
    lua_env.globals()['Enum']['TokenCategory'] = {
        'Miscellaneous': 1,
        'DungeonAndRaid': 2,
        'PvP': 3,
        'Quest': 4,
        'Seasonal': 5,
        'Legacy': 6,
    }

    # Auction House Filters
    lua_env.globals()['Enum']['AuctionHouseFilter'] = {
        'BattlePets': 1,
        'Consumables': 2,
        'Equipment': 3,
        'TradeGoods': 4,
        'Miscellaneous': 5,
    }

    # UI Widget Visualization Types
    lua_env.globals()['Enum']['UIWidgetVisualizationType'] = {
        'IconAndText': 0,
        'CaptureBar': 1,
        'StatusBar': 2,
        'DoubleStatusBar': 3,
    }

    # Calendar Types
    lua_env.globals()['Enum']['CalendarType'] = {
        'Holiday': 0,
        'Recurring': 1,
        'RaidLockout': 2,
        'RaidReset': 3,
        'Festival': 4,
    }

    # Time Types
    lua_env.globals()['Enum']['TimeType'] = {
        'GameTime': 0,
        'LocalTime': 1,
    }

    # Client Locales
    lua_env.globals()['Enum']['ClientLocale'] = {
        'enUS': 1,
        'koKR': 2,
        'frFR': 3,
        'deDE': 4,
        'zhCN': 5,
        'zhTW': 6,
        'esES': 7,
        'esMX': 8,
        'ruRU': 9,
        'ptBR': 10,
        'itIT': 11,
    }

    print("Enum tables fully registered into Lua environment.")