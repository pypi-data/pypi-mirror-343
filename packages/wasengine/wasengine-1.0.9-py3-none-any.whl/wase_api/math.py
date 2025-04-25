import math as pymath
import random as pyrandom

def register_math(lua_runtime):
    def lua_log(x, base=None):
        if base is None:
            return pymath.log(x)
        return pymath.log(x, base)

    lua_math = {
        # Constants
        "pi": pymath.pi,
        "huge": float("inf"),
        "maxinteger": 2**63 - 1,
        "mininteger": -2**63,

        # Basic Functions
        "abs": pymath.fabs,
        "acos": pymath.acos,
        "asin": pymath.asin,
        "atan": pymath.atan,
        "atan2": pymath.atan2,
        "ceil": pymath.ceil,
        "cos": pymath.cos,
        "deg": pymath.degrees,
        "exp": pymath.exp,
        "floor": pymath.floor,
        "fmod": pymath.fmod,
        "log": lua_log,
        "log10": pymath.log10,
        "max": max,
        "min": min,
        "modf": pymath.modf,
        "pow": pymath.pow,
        "rad": pymath.radians,
        "sin": pymath.sin,
        "sqrt": pymath.sqrt,
        "tan": pymath.tan,
        "frexp": pymath.frexp,
        "ldexp": pymath.ldexp,

        # Lua-specific integer handling
        "tointeger": lambda x: int(x) if isinstance(x, (int, float)) and x == int(x) else None,
        "type": lambda x: "integer" if isinstance(x, int) else "float" if isinstance(x, float) else None,
        "ult": lambda m, n: m < n if isinstance(m, int) and isinstance(n, int) else False,

        # Random functions
        "random": lambda *args: pyrandom.randint(1, args[0]) if len(args) == 1 else pyrandom.uniform(0, 1) if len(args) == 0 else pyrandom.randint(args[0], args[1]),
        "randomseed": pyrandom.seed,
    }

    lua_runtime.globals()["math"] = lua_math
