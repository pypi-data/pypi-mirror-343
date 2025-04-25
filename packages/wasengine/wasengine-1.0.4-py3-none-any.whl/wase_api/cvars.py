# wase_api/cvars.py

import json
import os

def register(lua_env):
    cvars = {
        "nameplateShowEnemies": "1",
        "Sound_EnableSFX": "1",
        "autoLootDefault": "0",
    }

    cvar_validations = {
        "nameplateShowEnemies": ["0", "1"],
        "Sound_EnableSFX": ["0", "1"],
        "autoLootDefault": ["0", "1"],
    }

    cvar_callbacks = {}
    read_only_cvars = ["readOnlyExample"]

    # --- Blizzard API Functions ---
    def GetCVar(name):
        value = cvars.get(name, "0")
        print(f"GetCVar('{name}') = '{value}'")
        return value

    def GetCVarBool(name):
        value = cvars.get(name, "0")
        bool_value = value == "1"
        print(f"GetCVarBool('{name}') = {bool_value}")
        return bool_value

    def SetCVar(name, value):
        str_value = str(value)
        if name in read_only_cvars:
            print(f"CVar '{name}' is read-only.")
            return
        if name in cvar_validations:
            allowed = cvar_validations[name]
            if str_value not in allowed:
                print(f"Invalid value '{str_value}' for CVar '{name}'. Allowed: {allowed}")
                return
        cvars[name] = str_value
        print(f"SetCVar('{name}', '{str_value}')")
        if name in cvar_callbacks:
            cvar_callbacks[name](str_value)

    # --- Extra Functions ---
    def RegisterCVarCallback(name, callback):
        cvar_callbacks[name] = callback
        print(f"Callback registered for CVar '{name}'")

    def ResetCVars():
        cvars.clear()
        print("All CVars reset")

    def DumpCVars():
        print("Current CVars:")
        for k, v in cvars.items():
            print(f"  {k} = {v}")

    # --- Inject into Lua ---
    lua_env.globals()['GetCVar'] = GetCVar
    lua_env.globals()['GetCVarBool'] = GetCVarBool
    lua_env.globals()['SetCVar'] = SetCVar
    lua_env.globals()['ResetCVars'] = ResetCVars
    lua_env.globals()['DumpCVars'] = DumpCVars
    lua_env.globals()['RegisterCVarCallback'] = RegisterCVarCallback
