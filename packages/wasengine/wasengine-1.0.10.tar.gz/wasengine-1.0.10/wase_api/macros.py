# wase_api/macros.py

def register(lua_env):
    slash_commands = {}

    # --- Slash Command Registration ---
    def define_slash_command(slash_name, command, handler):
        if command not in slash_commands:
            slash_commands[command] = handler
            print(f"Slash command '{command}' registered as '{slash_name}'")

    # --- Blizzard-Style Registration ---
    def set_slash(name, index, value):
        if f"SLASH_{name}{index}" not in lua_env.globals():
            lua_env.globals()[f"SLASH_{name}{index}"] = value
            print(f"SLASH_{name}{index} = '{value}'")

    def set_slash_handler(name, handler):
        slash_commands.update({
            lua_env.globals()[f"SLASH_{name}1"]: handler
        })
        print(f"Slash handler set for '{name}'")

    # --- Macro Execution ---
    def RunMacroText(macro):
        lines = macro.split("\n")
        for line in lines:
            if line.startswith("/"):
                cmd_parts = line.split(" ", 1)
                cmd = cmd_parts[0].lower()
                arg = cmd_parts[1] if len(cmd_parts) > 1 else ""
                handler = slash_commands.get(cmd)
                if handler:
                    handler(arg)
                else:
                    print(f"Unknown slash command: {cmd}")
            else:
                print(f"Executing: {line}")

    # --- Chat Simulation ---
    def SendChatMessage(msg, chatType="SAY", language=None, target=None):
        print(f"[{chatType}] {msg}")

    # --- Inject into Lua ---
    lua_env.globals()['RunMacroText'] = RunMacroText
    lua_env.globals()['SendChatMessage'] = SendChatMessage
    lua_env.globals()['set_slash'] = set_slash
    lua_env.globals()['set_slash_handler'] = set_slash_handler
