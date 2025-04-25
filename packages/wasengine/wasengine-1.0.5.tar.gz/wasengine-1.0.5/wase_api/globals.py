# wase_api/globals.py

def register(lua_env):
    # Lua utility functions (same as before)
    lua_env.execute('''
        function tinsert(t, v)
            table.insert(t, v)
        end

        function tremove(t, index)
            return table.remove(t, index)
        end

        function wipe(t)
            for k in pairs(t) do
                t[k] = nil
            end
        end
    ''')

    # Convert all dicts to Lua tables
    raid_class_colors = {
        "DEATHKNIGHT": {"r": 0.77, "g": 0.12, "b": 0.23, "colorStr": "ffC41F3B"},
        "DEMONHUNTER": {"r": 0.64, "g": 0.19, "b": 0.79, "colorStr": "ffa330c9"},
        "DRUID": {"r": 1.0, "g": 0.49, "b": 0.04, "colorStr": "ffff7d0a"},
        "EVOKER": {"r": 0.2, "g": 0.58, "b": 0.5, "colorStr": "ff33937f"},
        "HUNTER": {"r": 0.67, "g": 0.83, "b": 0.45, "colorStr": "ffabd473"},
        "MAGE": {"r": 0.41, "g": 0.8, "b": 0.94, "colorStr": "ff69ccf0"},
        "MONK": {"r": 0.0, "g": 1.0, "b": 0.59, "colorStr": "ff00ff96"},
        "PALADIN": {"r": 0.96, "g": 0.55, "b": 0.73, "colorStr": "fff58cba"},
        "PRIEST": {"r": 1.0, "g": 1.0, "b": 1.0, "colorStr": "ffffffff"},
        "ROGUE": {"r": 1.0, "g": 0.96, "b": 0.41, "colorStr": "fffff569"},
        "SHAMAN": {"r": 0.0, "g": 0.44, "b": 0.87, "colorStr": "ff0070dd"},
        "WARLOCK": {"r": 0.58, "g": 0.51, "b": 0.79, "colorStr": "ff9482c9"},
        "WARRIOR": {"r": 0.78, "g": 0.61, "b": 0.43, "colorStr": "ffc79c6e"}
    }
    lua_env.globals()['RAID_CLASS_COLORS'] = lua_env.table_from(raid_class_colors)

    debuff_colors = {
        "Magic": {"r": 0.2, "g": 0.6, "b": 1.0, "colorStr": "ff3393ff"},
        "Curse": {"r": 0.6, "g": 0.0, "b": 1.0, "colorStr": "ff8000ff"},
        "Disease": {"r": 0.6, "g": 0.4, "b": 0.0, "colorStr": "ff996600"},
        "Poison": {"r": 0.0, "g": 0.6, "b": 0.0, "colorStr": "ff009900"},
        "none": {"r": 0.8, "g": 0.0, "b": 0.0, "colorStr": "ffff0000"}
    }
    lua_env.globals()['DebuffTypeColor'] = lua_env.table_from(debuff_colors)

    faction_colors = {
        1: {"r": 0.8, "g": 0.13, "b": 0.13},
        2: {"r": 0.8, "g": 0.13, "b": 0.13},
        3: {"r": 0.75, "g": 0.27, "b": 0.0},
        4: {"r": 0.9, "g": 0.7, "b": 0.0},
        5: {"r": 0.0, "g": 0.6, "b": 0.1},
        6: {"r": 0.0, "g": 0.6, "b": 0.1},
        7: {"r": 0.0, "g": 0.6, "b": 0.1},
        8: {"r": 0.0, "g": 0.6, "b": 0.1}
    }
    lua_env.globals()['FACTION_BAR_COLORS'] = lua_env.table_from(faction_colors)
