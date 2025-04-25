# wase_api/secure.py

def register(lua_env):
    class SecureFrame:
        def __init__(self, name):
            self.name = name
            self.attributes = {}
            self.click_handlers = {}
            print(f"SecureFrame '{name}' created")

        def SetAttribute(self, key, value):
            self.attributes[key] = value
            print(f"SecureFrame '{self.name}' set attribute '{key}' = '{value}'")

        def GetAttribute(self, key):
            return self.attributes.get(key)

        def SetClickHandler(self, button, func):
            self.click_handlers[button] = func
            print(f"SecureFrame '{self.name}' set click handler for '{button}'")

        def Click(self, button="LeftButton"):
            if button in self.click_handlers:
                self.click_handlers[button](self)
                print(f"SecureFrame '{self.name}' clicked with '{button}'")
            else:
                print(f"No click handler for '{button}' on '{self.name}'")

    # --- Factory Function for Lua ---
    def CreateSecureFrame(name):
        return SecureFrame(name)

    lua_env.globals()['CreateSecureFrame'] = CreateSecureFrame
