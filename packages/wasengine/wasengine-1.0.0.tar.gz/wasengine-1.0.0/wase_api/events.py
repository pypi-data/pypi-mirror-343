# wase_api/events.py

def register(lua_env):
    event_registry = {}  # eventName: [frame1, frame2, ...]
    all_events_frames = set()

    # --- Core Event API ---
    def RegisterEvent(eventName, frame):
        if eventName not in event_registry:
            event_registry[eventName] = []
        if frame not in event_registry[eventName]:
            event_registry[eventName].append(frame)
            print(f"Frame '{frame.name}' registered for event '{eventName}'")

    def UnregisterEvent(eventName, frame):
        if eventName in event_registry and frame in event_registry[eventName]:
            event_registry[eventName].remove(frame)
            print(f"Frame '{frame.name}' unregistered from event '{eventName}'")

    def RegisterAllEvents(frame):
        all_events_frames.add(frame)
        print(f"Frame '{frame.name}' registered for ALL events")

    def UnregisterAllEvents(frame):
        all_events_frames.discard(frame)
        print(f"Frame '{frame.name}' unregistered from ALL events")

    def TriggerEvent(eventName, *args):
        # Regular registered frames
        frames = event_registry.get(eventName, [])
        for frame in frames:
            if "OnEvent" in frame.scripts:
                frame.scripts["OnEvent"](frame, eventName, *args)
        # Frames registered for ALL events
        for frame in all_events_frames:
            if "OnEvent" in frame.scripts:
                frame.scripts["OnEvent"](frame, eventName, *args)
        print(f"Triggered event '{eventName}' with args {args}")

    # --- Inject into Lua ---
    lua_env.globals()['RegisterEvent'] = RegisterEvent
    lua_env.globals()['UnregisterEvent'] = UnregisterEvent
    lua_env.globals()['RegisterAllEvents'] = RegisterAllEvents
    lua_env.globals()['UnregisterAllEvents'] = UnregisterAllEvents
    lua_env.globals()['TriggerEvent'] = TriggerEvent
