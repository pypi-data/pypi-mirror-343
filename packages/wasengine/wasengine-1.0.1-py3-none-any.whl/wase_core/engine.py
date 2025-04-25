from lupa import LuaRuntime
from wase_api import register_all
from core.stubs import register_core_api
from wase_api.frames import Frame  # Make sure this import is valid
import time

class WASEngine:
    def __init__(self):
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        register_all(self.lua)
        result = self.lua.execute("return math.min(1, 2)")
        print("math.min in Lua:", result)  # Should print 1
        register_core_api(self.lua)
        self.running = False
        self.FrameClass = Frame

    def run_lua(self, lua_code):
        return self.lua.execute(lua_code)

    def start_main_loop(self, duration=5, update_interval=0.1):
        # Start OnUpdate thread properly
        self.lua.globals()['StartUpdateThread']()
        self.running = True
        start_time = time.time()
        while self.running and (time.time() - start_time) < duration:
            time.sleep(update_interval)
        self.running = False

    def api_create_frame(self, name, frame_type="Frame", parent=None):
        return self.FrameClass(name, frame_type, parent)