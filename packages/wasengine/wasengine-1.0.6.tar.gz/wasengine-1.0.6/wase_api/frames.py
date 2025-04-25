# wase_api/frames.py

import time

__all__ = ['Frame', 'register']  # Explicit module exports

frames = {}  # Global registry of all created frames

class Frame:
    def __init__(self, frame_type="Frame", name=None, parent=None):
        self.frame_type = frame_type
        self.name = name or f"Frame_{len(frames)}"
        self.parent = parent
        self.scripts = {}
        self.children = []
        self.visible = True
        self.width = 100
        self.height = 100
        self.alpha = 1.0
        self.scale = 1.0
        self.point = ("CENTER", None, "CENTER", 0, 0)
        self.text = ""
        self.texture = "Interface\\Icons\\INV_Misc_QuestionMark"
        self.font = "wase_data/fonts/Arial.ttf"
        self.on_update_timer = 0
        frames[self.name] = self
        print(f"Created frame '{self.name}' of type '{self.frame_type}'")

    def SetScript(self, script_type, func):
        self.scripts[script_type] = func
        print(f"Script '{script_type}' set for frame '{self.name}'")

    def GetName(self):
        return self.name

    def Show(self):
        self.visible = True

    def Hide(self):
        self.visible = False

    def IsShown(self):
        return self.visible

    def SetWidth(self, width):
        self.width = width

    def SetHeight(self, height):
        self.height = height

    def SetAlpha(self, alpha):
        self.alpha = alpha

    def SetScale(self, scale):
        self.scale = scale

    def SetPoint(self, point, relative_to=None, relative_point=None, x=0, y=0):
        self.point = (point, relative_to, relative_point, x, y)

    def SetText(self, text):
        self.text = text

    def SetTexture(self, texture_path):
        self.texture = texture_path

    def SetFont(self, font_path, size=None, flags=None):
        self.font = font_path

    def ClearAllPoints(self):
        self.point = ("CENTER", None, "CENTER", 0, 0)

    def SetAllPoints(self, other_frame=None):
        # This is only a stub; actual logic may match all positioning
        print(f"SetAllPoints called on '{self.name}'")

    def TriggerEvent(self, event_name, *args):
        if "OnEvent" in self.scripts:
            print(f"[Event] {event_name}, args: {args}")
            self.scripts["OnEvent"](self, event_name, *args)

    def OnUpdate(self):
        if "OnUpdate" in self.scripts:
            elapsed = time.time() - self.on_update_timer
            self.scripts["OnUpdate"](self, elapsed)
            self.on_update_timer = time.time()

    def RegisterEvent(self, event_name):
        print(f"Frame '{self.name}' registered for event '{event_name}'")
        # You can track registered events if needed later
        self.scripts.setdefault("events", set()).add(event_name)

    def UnregisterEvent(self, event_name):
        print(f"Frame '{self.name}' unregistered from event '{event_name}'")
        if "events" in self.scripts and event_name in self.scripts["events"]:
            self.scripts["events"].remove(event_name)

    def RegisterUnitEvent(self, event, unit1, unit2=None):
        print(f"Frame '{self.name}' registered for unit event '{event}' with units: {unit1}, {unit2}")
        # For simulation, treat it like RegisterEvent
        self.RegisterEvent(event)

def register(lua_env):
    def create_frame(frame_type="Frame", name=None, parent=None, template=None):
        frame = Frame(frame_type, name, parent)
        lua_env.globals()[frame.name] = frame
        return frame

    def run_updates():
        for frame in frames.values():
            frame.OnUpdate()

    def trigger_frame_event(frame_name, event_name, *args):
        frame = frames.get(frame_name)
        if frame:
            frame.TriggerEvent(event_name, *args)

    lua_env.globals()['CreateFrame'] = create_frame
    lua_env.globals()['GetAllFrames'] = lambda: list(frames.values())
    lua_env.globals()['RunFrameUpdates'] = run_updates
    lua_env.globals()['TriggerFrameEvent'] = trigger_frame_event