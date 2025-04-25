# wase_api/auras.py

import os
import time as py_time

ICON_DIR = "wase_data/icons"
DEFAULT_ICON = os.path.join(ICON_DIR, "INV_Misc_QuestionMark.blp")

def get_texture_path(iconName):
    icon_filename = f"{iconName}.blp"
    icon_path = os.path.join(ICON_DIR, icon_filename)
    return icon_path if os.path.exists(icon_path) else DEFAULT_ICON

def register(lua_env):
    aura_icons = {}  # unit: [iconFrames]

    # --- Aura Icon Frame Simulation ---
    class AuraIcon:
        def __init__(self, parent, auraData):
            self.parent = parent
            self.name = auraData["name"]
            self.icon = get_texture_path(auraData["icon"].split("\\")[-1])
            self.duration = auraData["duration"]
            self.expiration = auraData["expirationTime"]
            self.visible = True
            print(f"AuraIcon created for '{self.name}'")

        def SetTexture(self, texturePath):
            self.icon = get_texture_path(texturePath.split("\\")[-1])
            print(f"AuraIcon texture set to '{self.icon}'")

        def SetCooldown(self, start, duration):
            self.duration = duration
            self.expiration = start + duration
            print(f"AuraIcon cooldown set: {duration}s")

        def Show(self):
            self.visible = True
            print(f"AuraIcon for '{self.name}' shown")

        def Hide(self):
            self.visible = False
            print(f"AuraIcon for '{self.name}' hidden")

    # --- Aura System Management ---
    def CreateAuraIconsForUnit(unit, auras):
        icons = []
        for aura in auras:
            icon = AuraIcon(unit, aura)
            icons.append(icon)
        aura_icons[unit] = icons
        print(f"Created {len(icons)} aura icons for unit '{unit}'")

    def ClearAuraIcons(unit):
        aura_icons[unit] = []
        print(f"Cleared aura icons for unit '{unit}'")

    def RefreshAuraIcons(unit, new_auras):
        ClearAuraIcons(unit)
        CreateAuraIconsForUnit(unit, new_auras)

    # --- Inject ---
    lua_env.globals()['CreateAuraIconsForUnit'] = CreateAuraIconsForUnit
    lua_env.globals()['ClearAuraIcons'] = ClearAuraIcons
    lua_env.globals()['RefreshAuraIcons'] = RefreshAuraIcons
