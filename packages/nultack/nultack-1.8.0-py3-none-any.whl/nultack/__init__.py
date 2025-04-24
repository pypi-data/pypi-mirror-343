"""
  Enjoy Bro?
"""
from .encode import NültackEncoder
from .execute import NültackExecutor
from .protection import NültackProtector  # Ganti dari decode ke protection

__version__ = "1.8.0"
__all__ = ['encode', 'decode', 'execute', 'hide']

# Shortcut functions
def encode(source: str) -> str:
    return NültackEncoder().encode(source)

def decode(payload: str) -> str:
    return NültackProtector().decode(payload)

def execute(payload: str, globals=None, locals=None) -> None:
    return NültackExecutor().execute(payload, globals, locals)

def hide(source: str) -> str:
    """
    Shortcut untuk encode lalu bungkus dengan exec.
    """
    payload = encode(source)
    return f'import nultack; nultack.execute("{payload}")'
