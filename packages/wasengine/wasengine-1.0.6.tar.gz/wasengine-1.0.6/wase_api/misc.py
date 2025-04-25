# wase_api/misc.py

def register(lua_env):
    lua_env.globals()['GetLocale'] = lambda: "enUS"

    # Override Lua print to Python print
    lua_env.globals()['print'] = print
