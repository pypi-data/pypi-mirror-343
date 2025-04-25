# __init__.py

# --- API Imports ---
from . import (
    time,
    misc,
    frames,
    events,
    unit,
    spells,
    combat,
    map,
    group,
    cvars,
    globals as wow_globals,
    inventory,
    macros,
    widgets,
    secure,
    update_loop,
    actionbar,
    auras,
    math,
    bit,
    enum
)

# --- Register All APIs into Lua ---
def register_all(lua_env):
    time.register(lua_env)
    misc.register(lua_env)
    frames.register(lua_env)
    events.register(lua_env)
    unit.register(lua_env)
    spells.register(lua_env)
    combat.register(lua_env)
    map.register(lua_env)
    group.register(lua_env)
    cvars.register(lua_env)
    wow_globals.register(lua_env)
    inventory.register(lua_env)
    macros.register(lua_env)
    widgets.register(lua_env)
    secure.register(lua_env)
    update_loop.register(lua_env)
    actionbar.register(lua_env)
    auras.register(lua_env)
    math.register_math(lua_env)
    bit.register(lua_env)
    enum.register_enum(lua_runtime)