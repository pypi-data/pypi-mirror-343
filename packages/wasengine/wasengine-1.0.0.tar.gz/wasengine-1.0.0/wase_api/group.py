# wase_api/group.py

def register(lua_env):
    group_data = {
        "isRaid": True,
        "members": [
            {"name": "TestPlayer", "class": "MAGE", "subgroup": 1, "level": 70},
            {"name": "DummyTarget", "class": "WARRIOR", "subgroup": 1, "level": 72}
        ]
    }

    lua_env.globals()['GetNumGroupMembers'] = lambda: len(group_data["members"])
    lua_env.globals()['IsInRaid'] = lambda: group_data["isRaid"]
    lua_env.globals()['IsInGroup'] = lambda: True  # Always in group if testing this

    def get_raid_roster_info(index):
        if index <= len(group_data["members"]):
            member = group_data["members"][index - 1]
            return member["name"], None, member["subgroup"], None, None, None, None, None, None, member["class"]
        return None

    lua_env.globals()['GetRaidRosterInfo'] = get_raid_roster_info
