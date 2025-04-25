# WASEngine/wase_core/stubs.py

def register_core_api(lua_runtime):
    # C_AddOns Stub with _G scope
    lua_runtime.execute("""
    _G.C_AddOns = _G.C_AddOns or {}
    C_AddOns = _G.C_AddOns
    C_AddOns.IsAddOnLoaded = function(name)
        return true
    end
    """)
    print("Core Blizzard API stubs registered.")