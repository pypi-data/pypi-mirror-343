def register(lua_env):
    # Register hooksecurefunc in the Lua environment
    lua_env.execute("""
        HookRegistry = HookRegistry or {}

        function hooksecurefunc(funcName, hookFunc)
            HookRegistry[funcName] = HookRegistry[funcName] or {}
            table.insert(HookRegistry[funcName], hookFunc)
            print("hooksecurefunc hooked:", funcName)
        end
    """)

    print("hooksecurefunc registered into Lua environment.")
