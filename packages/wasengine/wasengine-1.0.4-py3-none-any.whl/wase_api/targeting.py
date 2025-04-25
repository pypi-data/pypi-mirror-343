# wase_api/targeting.py

def register(lua_env):
    current_target = None
    current_focus = None

    # --- Targeting Functions ---
    def TargetUnit(unit):
        nonlocal current_target
        current_target = unit
        lua_env.globals()['TriggerEvent']("PLAYER_TARGET_CHANGED")
        print(f"Target set to '{unit}'")

    def ClearTarget():
        nonlocal current_target
        current_target = None
        lua_env.globals()['TriggerEvent']("PLAYER_TARGET_CHANGED")
        print("Target cleared")

    def FocusUnit(unit):
        nonlocal current_focus
        current_focus = unit
        lua_env.globals()['TriggerEvent']("PLAYER_FOCUS_CHANGED")
        print(f"Focus set to '{unit}'")

    def ClearFocus():
        nonlocal current_focus
        current_focus = None
        lua_env.globals()['TriggerEvent']("PLAYER_FOCUS_CHANGED")
        print("Focus cleared")

    def UnitIsTarget(unit):
        return unit == current_target

    def UnitIsFocus(unit):
        return unit == current_focus

    # --- Expose Current Target/Focus ---
    def GetTarget():
        return current_target or "none"

    def GetFocus():
        return current_focus or "none"

    # --- Inject into Lua ---
    lua_env.globals()['TargetUnit'] = TargetUnit
    lua_env.globals()['ClearTarget'] = ClearTarget
    lua_env.globals()['FocusUnit'] = FocusUnit
    lua_env.globals()['ClearFocus'] = ClearFocus
    lua_env.globals()['UnitIsTarget'] = UnitIsTarget
    lua_env.globals()['UnitIsFocus'] = UnitIsFocus
    lua_env.globals()['GetTarget'] = GetTarget
    lua_env.globals()['GetFocus'] = GetFocus
