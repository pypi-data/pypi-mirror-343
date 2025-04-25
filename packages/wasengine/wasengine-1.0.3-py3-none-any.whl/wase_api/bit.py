# WASEngine/wase_api/bit.py

# WoW Lua-compatible bitwise operations for the WASEngine Blizzard API simulation.

# The original WoW environment mixes Lua 5.1 and bit/bit32-style APIs.
# We replicate wase_core functionality here.

def band(*args):
    """Bitwise AND of all arguments."""
    result = 0xFFFFFFFF
    for arg in args:
        result &= arg & 0xFFFFFFFF
    return result

def bor(*args):
    """Bitwise OR of all arguments."""
    result = 0
    for arg in args:
        result |= arg & 0xFFFFFFFF
    return result

def bxor(*args):
    """Bitwise XOR of all arguments."""
    result = 0
    for arg in args:
        result ^= arg & 0xFFFFFFFF
    return result

def bnot(x):
    """Bitwise NOT."""
    return (~x) & 0xFFFFFFFF

def lshift(x, n):
    """Logical left shift."""
    return (x << n) & 0xFFFFFFFF

def rshift(x, n):
    """Logical right shift."""
    return (x % 0x100000000) >> n

def arshift(x, n):
    """Arithmetic right shift."""
    if x & 0x80000000:
        return ((x >> n) | (0xFFFFFFFF << (32 - n))) & 0xFFFFFFFF
    else:
        return (x >> n) & 0xFFFFFFFF

def rol(x, n):
    """Rotate bits left."""
    n = n % 32
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def ror(x, n):
    """Rotate bits right."""
    n = n % 32
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def bswap(x):
    """Byte swap."""
    x = x & 0xFFFFFFFF
    return ((x & 0xFF) << 24) | ((x & 0xFF00) << 8) | ((x >> 8) & 0xFF00) | ((x >> 24) & 0xFF)

# Aliases to match WoW’s mix of bit/bit32
bit = {
    'band': band,
    'bor': bor,
    'bxor': bxor,
    'bnot': bnot,
    'lshift': lshift,
    'rshift': rshift,
    'arshift': arshift,
    'rol': rol,
    'ror': ror,
    'bswap': bswap,
}

bit32 = {
    'band': band,
    'bor': bor,
    'bxor': bxor,
    'bnot': bnot,
    'lshift': lshift,
    'rshift': rshift,
    'arshift': arshift,
    'rol': rol,
    'ror': ror,
    'bswap': bswap,
}

# Direct function exports if preferred
__all__ = [
    'band', 'bor', 'bxor', 'bnot',
    'lshift', 'rshift', 'arshift',
    'rol', 'ror', 'bswap',
    'bit', 'bit32',
]

# Registration function for WASEngine
def register(lua_env):
    # Inject 'bit' and 'bit32' tables into the Lua environment
    lua_env.globals()['bit'] = bit
    lua_env.globals()['bit32'] = bit32
