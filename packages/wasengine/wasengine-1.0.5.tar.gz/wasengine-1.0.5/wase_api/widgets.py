# wase_api/widgets.py

import os

ICON_DIR = "wase_data/icons"
FONT_DIR = "wase_data/fonts"
DEFAULT_FONT = os.path.join(FONT_DIR, "Arial.ttf")
DEFAULT_ICON = os.path.join(ICON_DIR, "INV_Misc_QuestionMark.blp")

def register(lua_env):
    class FontString:
        def __init__(self, parent):
            self.parent = parent
            self.text = ""
            self.font = (DEFAULT_FONT, 12, "OUTLINE")
            self.visible = True
            self.position = None
            print(f"FontString created for frame '{parent.name}'")

        def SetText(self, text):
            self.text = text
            print(f"FontString text set to '{text}'")

        def GetText(self):
            return self.text

        def SetFont(self, path, size, outline=""):
            # Always fallback to Arial
            self.font = (DEFAULT_FONT, size, outline)
            print(f"FontString font set to {self.font}")

        def SetPoint(self, anchor, relativeTo=None, relativePoint=None, xOffset=0, yOffset=0):
            self.position = (anchor, relativeTo, relativePoint, xOffset, yOffset)
            print(f"FontString positioned at {self.position}")

        def Show(self):
            self.visible = True
            print("FontString shown")

        def Hide(self):
            self.visible = False
            print("FontString hidden")

        def IsShown(self):
            return self.visible

    class Texture:
        def __init__(self, parent):
            self.parent = parent
            self.texture = self.get_texture_path("INV_Misc_QuestionMark")
            self.width = 0
            self.height = 0
            self.alpha = 1.0
            self.visible = True
            self.position = None
            print(f"Texture created for frame '{parent.name}'")

        def get_texture_path(self, iconName):
            icon_filename = f"{iconName}.blp"
            icon_path = os.path.join(ICON_DIR, icon_filename)
            if os.path.exists(icon_path):
                return icon_path
            else:
                return DEFAULT_ICON

        def SetTexture(self, texturePath):
            icon_name = texturePath.split("\\")[-1]
            self.texture = self.get_texture_path(icon_name)
            print(f"Texture path set to '{self.texture}'")

        def SetWidth(self, width):
            self.width = width
            print(f"Texture width set to {width}")

        def SetHeight(self, height):
            self.height = height
            print(f"Texture height set to {height}")

        def SetAlpha(self, alpha):
            self.alpha = alpha
            print(f"Texture alpha set to {alpha}")

        def SetPoint(self, anchor, relativeTo=None, relativePoint=None, xOffset=0, yOffset=0):
            self.position = (anchor, relativeTo, relativePoint, xOffset, yOffset)
            print(f"Texture positioned at {self.position}")

        def Show(self):
            self.visible = True
            print("Texture shown")

        def Hide(self):
            self.visible = False
            print("Texture hidden")

        def IsShown(self):
            return self.visible

    # --- Injected Functions for Frame Widget Creation ---
    def CreateFontString(parent):
        return FontString(parent)

    def CreateTexture(parent):
        return Texture(parent)

    lua_env.globals()['CreateFontString'] = CreateFontString
    lua_env.globals()['CreateTexture'] = CreateTexture
