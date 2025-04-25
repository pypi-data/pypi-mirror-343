# wase_api/update_loop.py

import time as py_time
import threading

def register(lua_env):
    update_frames = []

    # --- Frame Hook ---
    def AddUpdateFrame(frame):
        if frame not in update_frames:
            update_frames.append(frame)
            print(f"Frame '{frame.name}' added to OnUpdate loop")

    def RemoveUpdateFrame(frame):
        if frame in update_frames:
            update_frames.remove(frame)
            print(f"Frame '{frame.name}' removed from OnUpdate loop")

    # --- Main Update Loop ---
    def UpdateLoop():
        last_time = py_time.time()
        while True:
            now = py_time.time()
            elapsed = now - last_time
            for frame in update_frames:
                if "OnUpdate" in frame.scripts:
                    frame.scripts["OnUpdate"](frame, elapsed)
            last_time = now
            py_time.sleep(0.01)  # Simulate 100 FPS (~10ms/frame)

    # --- Start in Background Thread ---
    def StartUpdateThread():
        t = threading.Thread(target=UpdateLoop, daemon=True)
        t.start()
        print("Update loop started")

    # --- Inject ---
    lua_env.globals()['AddUpdateFrame'] = AddUpdateFrame
    lua_env.globals()['RemoveUpdateFrame'] = RemoveUpdateFrame
    lua_env.globals()['StartUpdateThread'] = StartUpdateThread
