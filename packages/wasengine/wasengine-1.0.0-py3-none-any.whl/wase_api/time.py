# wase_api/time.py

import time as py_time
import threading

def register(lua_env):
    active_timers = []
    tickers = []

    # --- Blizzard's GetTime Simulation ---
    def GetTime():
        return py_time.time()

    # --- Blizzard's time() Function (returns epoch time) ---
    def time_func():
        return int(py_time.time())

    # --- C_Timer.After: Schedule a one-time delayed function ---
    def C_Timer_After(delay, func):
        def delayed_execution():
            py_time.sleep(delay)
            func()

        thread = threading.Thread(target=delayed_execution)
        thread.daemon = True
        thread.start()
        print(f"C_Timer.After scheduled: {delay} seconds")

    # --- C_Timer.NewTicker: Repeating timer with optional iteration limit ---
    class Ticker:
        def __init__(self, interval, func, iterations=None):
            self.interval = interval
            self.func = func
            self.iterations = iterations
            self.remaining = iterations
            self.next_trigger = py_time.time() + interval
            self.cancelled = False
            tickers.append(self)
            print(f"Ticker created: every {interval}s, iterations: {iterations}")

        def Cancel(self):
            self.cancelled = True
            print("Ticker cancelled")

        def Update(self, now):
            if self.cancelled:
                return
            if now >= self.next_trigger:
                self.func()
                if self.remaining is not None:
                    self.remaining -= 1
                    if self.remaining <= 0:
                        self.cancelled = True
                        return
                self.next_trigger = now + self.interval

    def C_Timer_NewTicker(interval, func, iterations=None):
        return Ticker(interval, func, iterations)

    # --- Manual Timer Simulation (non-threaded alternative) ---
    def SimulateTimer(delay, func):
        trigger_time = py_time.time() + delay
        active_timers.append((trigger_time, func))
        print(f"Simulated timer set for {delay} seconds")

    def ProcessTimers():
        now = py_time.time()
        # Process one-shot timers
        for timer in active_timers[:]:
            trigger_time, func = timer
            if now >= trigger_time:
                func()
                active_timers.remove(timer)
        # Process tickers
        for ticker in tickers[:]:
            ticker.Update(now)
            if ticker.cancelled:
                tickers.remove(ticker)

    # --- Inject into Lua ---
    lua_env.globals()['GetTime'] = GetTime
    lua_env.globals()['time'] = time_func
    lua_env.globals()['C_Timer'] = {
        'After': C_Timer_After,
        'NewTicker': C_Timer_NewTicker
    }
    lua_env.globals()['SimulateTimer'] = SimulateTimer
    lua_env.globals()['ProcessTimers'] = ProcessTimers
